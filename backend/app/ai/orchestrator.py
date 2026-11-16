import re
import uuid
import json
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.ai.gemini_client import gemini_client
from app.ai.guardrails import AIGuardrails
from app.ai.tools.registry import InternalAITools
from app.schemas.assistant import ChatRequest, ChatResponse, ExtractedRequirement
from app.schemas.products import ProductSummarySchema


class ShoppingAssistantOrchestrator:
    SYSTEM_INSTRUCTION = (
        "You are PriceWise AI, an expert, objective consumer electronics advisor in India. "
        "Your role is to help users select the best electronics based on real technical specifications and prices in INR (₹). "
        "STRICT GROUNDING RULES:\n"
        "1. Recommend ONLY products present in the provided VERIFIED_CATALOG_DATA.\n"
        "2. State prices in Indian Rupees (e.g. ₹74,999).\n"
        "3. Highlight real specifications (processor, battery, camera, RAM/storage).\n"
        "4. Be transparent about compromises and tradeoffs.\n"
        "5. Never invent models, prices, or ratings not in the verified data.\n"
        "6. Keep responses clear, helpful, and concise."
    )

    @classmethod
    def extract_requirements(cls, message: str) -> ExtractedRequirement:
        text = message.lower()
        budget = None
        category = None
        priorities = []
        preferred_brands = []

        # Budget extraction (e.g. ₹50,000, 50k, 50000, 1.5 lakh)
        b_match = re.search(r"(?:₹|rs\.?|inr)?\s*(\d+(?:,\d+)*(?:\.\d+)?)\s*(?:k|thousand|lakh|lac)?", text)
        if b_match:
            raw_num = b_match.group(1).replace(",", "")
            try:
                val = float(raw_num)
                if "lakh" in text or "lac" in text:
                    val *= 100000
                elif "k" in text and val < 1000:
                    val *= 1000
                if val >= 1000:  # Sensible minimum electronics price
                    budget = val
            except ValueError:
                pass

        # Category detection
        if any(w in text for w in ["phone", "mobile", "smartphone", "iphone", "galaxy"]):
            category = "smartphones"
        elif any(w in text for w in ["laptop", "notebook", "macbook", "pc"]):
            category = "laptops"
        elif any(w in text for w in ["headphone", "audio", "xm5", "sony"]):
            category = "headphones"
        elif any(w in text for w in ["earbud", "airpod", "tws"]):
            category = "earbuds"
        elif any(w in text for w in ["watch", "smartwatch"]):
            category = "smartwatches"
        elif any(w in text for w in ["tv", "television", "oled"]):
            category = "televisions"
        elif any(w in text for w in ["gpu", "graphic", "rtx", "component"]):
            category = "computer-components"

        # Priorities
        if "camera" in text or "photo" in text or "video" in text:
            priorities.append("camera")
        if "battery" in text or "charging" in text:
            priorities.append("battery")
        if "game" in text or "gaming" in text or "fps" in text:
            priorities.append("gaming")
        if "code" in text or "programming" in text or "ai" in text or "develop" in text:
            priorities.append("development")
        if "anc" in text or "noise cancel" in text:
            priorities.append("noise_cancellation")

        # Brands
        for b in ["apple", "samsung", "oneplus", "sony", "lenovo", "dell", "lg", "nvidia"]:
            if b in text:
                preferred_brands.append(b.capitalize())

        return ExtractedRequirement(
            category_slug=category,
            budget=budget,
            preferred_brands=preferred_brands,
            key_priorities=priorities,
        )

    @classmethod
    async def process_chat(cls, db: AsyncSession, request: ChatRequest) -> ChatResponse:
        conv_id = request.conversation_id or str(uuid.uuid4())

        # 1. Guardrail input check
        guard_result = AIGuardrails.sanitize_input(request.message)
        if not guard_result.is_safe:
            return ChatResponse(
                conversation_id=conv_id,
                message=guard_result.rejection_reason or "Request rejected by security guardrails.",
                model_used="guardrails",
                suggested_follow_ups=["Best smartphones under ₹50,000", "Laptops for programming and AI"],
            )

        # 2. Extract structured requirements
        extracted = cls.extract_requirements(guard_result.sanitized_text)
        if request.category_slug:
            extracted.category_slug = request.category_slug
        if request.max_budget:
            extracted.budget = request.max_budget

        # 3. Retrieve verified products from internal database
        products = await InternalAITools.search_products(
            db=db,
            query=guard_result.sanitized_text if not extracted.category_slug else "",
            category_slug=extracted.category_slug,
            max_budget=extracted.budget,
            limit=4,
        )

        # If strict search returned empty, broaden search without budget constraint
        if not products and extracted.category_slug:
            products = await InternalAITools.search_products(
                db=db,
                category_slug=extracted.category_slug,
                limit=3,
            )

        # Map to ProductSummarySchema for response cards
        summary_cards: List[ProductSummarySchema] = []
        for p in products:
            disc = round(((p["mrp"] - p["best_price"]) / p["mrp"] * 100), 1) if p["mrp"] > p["best_price"] else 0.0
            summary_cards.append(
                ProductSummarySchema(
                    id=p["product_id"],
                    name=p["name"],
                    slug=p["name"].lower().replace(" ", "-"),
                    brand_name=p["brand"],
                    brand_slug=p["brand"].lower(),
                    category_name=p["category"],
                    category_slug=extracted.category_slug or "electronics",
                    image_url=p.get("image_url"),
                    best_price=p["best_price"],
                    mrp=p["mrp"],
                    discount_percentage=disc,
                    marketplace_count=2,
                    rating=p["rating"],
                    review_count=p["review_count"],
                    is_demo=False,
                    primary_variant_id=p["variant_id"],
                )
            )

        # 4. Generate grounded synthesis with Gemini or deterministic fallback
        catalog_context = json.dumps(products, indent=2)
        prompt = (
            f"User Query: {guard_result.sanitized_text}\n\n"
            f"Extracted Requirements:\n"
            f"- Category: {extracted.category_slug or 'Not specified'}\n"
            f"- Budget Limit: ₹{int(extracted.budget):,} if specified else 'Flexible'\n"
            f"- Priorities: {', '.join(extracted.key_priorities) or 'Balanced value'}\n\n"
            f"VERIFIED_CATALOG_DATA:\n{catalog_context}\n\n"
            f"Provide an insightful, well-structured shopping recommendation in 2 to 3 paragraphs."
        )

        gemini_text = None
        if gemini_client.is_available:
            gemini_text = await gemini_client.generate_text(
                prompt=prompt,
                system_instruction=cls.SYSTEM_INSTRUCTION,
            )

        # 5. Deterministic fallback if Gemini is offline or quota reached
        if not gemini_text:
            if summary_cards:
                top = summary_cards[0]
                gemini_text = (
                    f"Based on your requirements, the **{top.name}** is our top recommendation at **₹{int(top.best_price):,}** "
                    f"(discounted from MRP ₹{int(top.mrp):,}). It offers strong performance, an exceptional user rating of {top.rating}★, "
                    f"and matches your criteria. Check out the options below for full side-by-side technical comparison and marketplace prices."
                )
            else:
                gemini_text = (
                    "I searched our verified catalog but couldn't find a direct match for that exact specification. "
                    "Try exploring our top categories: Smartphones, Laptops, Headphones, or adjust your budget range."
                )

        follow_ups = [
            "Compare top 2 options side-by-side",
            "Show historical price trend",
            "Set a price drop alert",
        ]

        return ChatResponse(
            conversation_id=conv_id,
            message=gemini_text,
            extracted_requirements=extracted,
            recommended_products=summary_cards,
            suggested_follow_ups=follow_ups,
            model_used=gemini_client.model_name if gemini_client.is_available else "deterministic-engine",
        )
