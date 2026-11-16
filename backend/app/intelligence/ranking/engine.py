import math
from typing import List, Dict, Optional, Any, Tuple
from pydantic import BaseModel
from app.schemas.recommendations import (
    RecommendationRequest,
    RecommendationResponse,
    RecommendedProductItem,
    RecommendationScoreDetail,
)
from app.schemas.products import ProductSummarySchema


class ScoredCandidate(BaseModel):
    product: ProductSummarySchema
    variant_id: str
    price: float
    mrp: float
    rating: float
    review_count: int
    category_slug: str
    specs: Dict[str, str] = {}


class RecommendationEngine:
    ALGORITHM_VERSION = "v1.2-deterministic"

    DEFAULT_WEIGHTS = {
        "price": 0.35,
        "specs": 0.30,
        "rating": 0.20,
        "reviews": 0.10,
        "value": 0.05,
    }

    INTENT_WEIGHT_OVERRIDES = {
        "best_budget": {
            "price": 0.50,
            "specs": 0.20,
            "rating": 0.15,
            "reviews": 0.05,
            "value": 0.10,
        },
        "best_performance": {
            "price": 0.15,
            "specs": 0.55,
            "rating": 0.15,
            "reviews": 0.10,
            "value": 0.05,
        },
        "best_rated": {
            "price": 0.20,
            "specs": 0.25,
            "rating": 0.35,
            "reviews": 0.15,
            "value": 0.05,
        },
        "best_value": {
            "price": 0.30,
            "specs": 0.30,
            "rating": 0.15,
            "reviews": 0.10,
            "value": 0.15,
        },
    }

    @classmethod
    def calculate_price_score(cls, price: float, budget: Optional[float]) -> float:
        """
        Calculates price score (0 - 100).
        If user specified a budget, heavily penalizes exceeding budget.
        """
        if not budget or budget <= 0:
            # Baseline price affordability score relative to typical market points
            return 80.0

        if price > budget:
            over = (price - budget) / budget
            return max(0.0, 100.0 - (over * 200.0))
        else:
            # Price is within budget. Staying under budget gets 70 base + bonus for savings
            savings_ratio = (budget - price) / budget
            return min(100.0, 75.0 + (savings_ratio * 25.0))

    @classmethod
    def calculate_rating_score(cls, rating: float) -> float:
        """
        Converts 1.0 - 5.0 star rating to 0 - 100.
        Rating < 3.0 receives severe penalty.
        """
        if not rating or rating <= 0:
            return 50.0  # Neutral prior if no rating
        # 5.0 -> 100, 4.5 -> 87.5, 4.0 -> 75, 3.0 -> 50
        return max(0.0, min(100.0, (rating - 1.0) * 25.0))

    @classmethod
    def calculate_review_volume_score(cls, review_count: int) -> float:
        """
        Logarithmic credibility curve for review volume.
        """
        if review_count <= 0:
            return 30.0
        # log10(1000) = 3 -> 75 score; log10(10000) = 4 -> 100 score
        log_val = math.log10(review_count + 1)
        return min(100.0, (log_val / 4.0) * 100.0)

    @classmethod
    def calculate_value_discount_score(cls, current_price: float, mrp: float) -> float:
        """
        Calculates verified value savings percentage.
        """
        if not mrp or mrp <= current_price:
            return 50.0  # Selling at MRP
        discount = (mrp - current_price) / mrp
        return min(100.0, 50.0 + (discount * 100.0))

    @classmethod
    def calculate_category_spec_score(cls, category_slug: str, specs: Dict[str, str]) -> Tuple[float, List[str], List[str]]:
        """
        Evaluates category-specific technical attributes.
        Returns (spec_score, strengths, tradeoffs).
        """
        strengths: List[str] = []
        tradeoffs: List[str] = []
        spec_text = " ".join(specs.values()).lower()

        score = 75.0  # Base spec score

        if category_slug == "smartphones":
            # Processor
            if "snapdragon 8 elite" in spec_text or "a18" in spec_text or "dimensity 9400" in spec_text:
                score += 15
                strengths.append("Flagship 3nm processor with elite gaming & AI capabilities")
            # Camera
            if "ois" in spec_text or "50mp" in spec_text or "periscope" in spec_text:
                score += 5
                strengths.append("Advanced high-res OIS camera system")
            # Battery & Charging
            if "6000" in spec_text or "100w" in spec_text:
                score += 5
                strengths.append("Exceptional battery capacity and ultra-fast charging")
            elif "4000" in spec_text:
                tradeoffs.append("Compact 4000 mAh battery; requires daily recharging under heavy use")

        elif category_slug == "laptops":
            # GPU / CPU
            if "rtx 40" in spec_text or "m3" in spec_text or "core i7" in spec_text:
                score += 15
                strengths.append("Dedicated workstation-grade CPU/GPU performance")
            # RAM
            if "16gb" in spec_text or "32gb" in spec_text:
                score += 5
                strengths.append("16GB+ memory for heavy multitasking and development")
            else:
                tradeoffs.append("8GB baseline memory may bottleneck intensive creative or developer workloads")
            # Screen
            if "oled" in spec_text or "retina" in spec_text or "240hz" in spec_text:
                score += 5
                strengths.append("High-refresh rate / professional color-accurate display")

        elif category_slug in ["headphones", "earbuds"]:
            if "anc" in spec_text or "noise cancelling" in spec_text or "adaptive audio" in spec_text:
                score += 15
                strengths.append("Industry-leading active noise cancellation")
            if "30 hours" in spec_text or "ldac" in spec_text:
                score += 10
                strengths.append("High-res lossless audio codecs and long battery life")

        return min(100.0, score), strengths, tradeoffs

    @classmethod
    def rank_candidates(
        cls,
        candidates: List[ScoredCandidate],
        request: RecommendationRequest,
    ) -> RecommendationResponse:
        # Determine weights
        weights = cls.DEFAULT_WEIGHTS.copy()
        if request.intent and request.intent in cls.INTENT_WEIGHT_OVERRIDES:
            weights = cls.INTENT_WEIGHT_OVERRIDES[request.intent].copy()
        if request.priorities:
            for k, v in request.priorities.items():
                if k in weights:
                    weights[k] = float(v)
            # Re-normalize weights to sum to 1.0
            total_w = sum(weights.values())
            weights = {k: v / total_w for k, v in weights.items()}

        ranked_items: List[RecommendedProductItem] = []

        for cand in candidates:
            price_s = cls.calculate_price_score(cand.price, request.max_budget)
            rating_s = cls.calculate_rating_score(cand.rating)
            reviews_s = cls.calculate_review_volume_score(cand.review_count)
            value_s = cls.calculate_value_discount_score(cand.price, cand.mrp)
            spec_s, strengths, tradeoffs = cls.calculate_category_spec_score(cand.category_slug, cand.specs)

            overall = (
                weights["price"] * price_s
                + weights["specs"] * spec_s
                + weights["rating"] * rating_s
                + weights["reviews"] * reviews_s
                + weights["value"] * value_s
            )

            # Assign explanatory badge
            badge = None
            if overall >= 88.0:
                badge = "Top Recommendation"
            elif value_s >= 80.0:
                badge = "Best Value"
            elif price_s >= 90.0:
                badge = "Budget Champion"

            score_breakdown = RecommendationScoreDetail(
                overall_score=round(overall, 1),
                price_score=round(price_s, 1),
                spec_score=round(spec_s, 1),
                rating_score=round(rating_s, 1),
                review_volume_score=round(reviews_s, 1),
                value_score=round(value_s, 1),
                badge=badge,
                key_strengths=strengths,
                tradeoffs=tradeoffs,
            )

            # Generate natural language explanation
            explanation = (
                f"Ranks #{len(ranked_items) + 1} with an overall score of {round(overall, 1)}/100. "
                f"Offered at ₹{int(cand.price):,} vs MRP ₹{int(cand.mrp):,}. "
                f"Key advantage: {strengths[0] if strengths else 'High user rating and reliable performance'}. "
                f"Tradeoff: {tradeoffs[0] if tradeoffs else 'None observed at this price tier'}."
            )

            ranked_items.append(
                RecommendedProductItem(
                    product=cand.product,
                    variant_id=cand.variant_id,
                    scores=score_breakdown,
                    explanation=explanation,
                )
            )

        # Sort descending by overall score
        ranked_items.sort(key=lambda x: x.scores.overall_score, reverse=True)

        return RecommendationResponse(
            category_slug=request.category_slug,
            budget_applied=request.max_budget,
            algorithm_version=cls.ALGORITHM_VERSION,
            weights_applied=weights,
            recommendations=ranked_items[:request.limit],
        )
