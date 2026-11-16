import re
from enum import Enum
from typing import Optional, Dict, Any, Tuple
from pydantic import BaseModel
from rapidfuzz import fuzz


class MatchOutcome(str, Enum):
    CONFIRMED_MATCH = "CONFIRMED_MATCH"
    PROBABLE_MATCH = "PROBABLE_MATCH"
    REJECTED_MATCH = "REJECTED_MATCH"


class ExtractedAttributes(BaseModel):
    normalized_title: str
    brand: Optional[str] = None
    model_number: Optional[str] = None
    ram: Optional[str] = None
    storage: Optional[str] = None
    color: Optional[str] = None
    raw_specs: Dict[str, str] = {}


class MatchResult(BaseModel):
    outcome: MatchOutcome
    confidence_score: float  # 0.0 to 1.0
    evidence: Dict[str, Any]
    rejection_reason: Optional[str] = None


class ProductMatchingEngine:
    KNOWN_BRANDS = [
        "apple", "samsung", "oneplus", "google", "xiaomi", "dell",
        "lenovo", "hp", "asus", "sony", "bose", "lg", "canon", "nvidia", "intel"
    ]

    # Sort colors by length descending so compound colors match before simple ones
    COMMON_COLORS = sorted([
        "black", "white", "grey", "gray", "silver", "gold", "blue", "green",
        "red", "purple", "violet", "titanium", "graphite", "space grey",
        "ultramarine", "onyx black", "marble gray", "midnight ocean"
    ], key=len, reverse=True)

    @classmethod
    def normalize_title(cls, title: str) -> str:
        t = title.lower()
        # Remove noisy suffixes like "5g", special characters, multiple spaces
        t = re.sub(r"[^\w\s\-\.]", " ", t)
        t = re.sub(r"\s+", " ", t).strip()
        return t

    @classmethod
    def extract_attributes(cls, title: str) -> ExtractedAttributes:
        norm = cls.normalize_title(title)
        t_lower = title.lower()

        # 1. Brand extraction
        brand = None
        for b in cls.KNOWN_BRANDS:
            if re.search(rf"\b{b}\b", norm):
                brand = b.capitalize()
                break

        # 2. RAM extraction (e.g., "12gb ram", "12 gb", "16gb unified memory")
        ram = None
        ram_match = re.search(r"\b(\d{1,2})\s*(?:gb|gigabyte)?\s*(?:ram|unified memory|ddr\d?)\b", t_lower)
        if not ram_match:
            ram_match = re.search(r"\b(\d{1,2})\s*gb\b", t_lower)
        if ram_match:
            val = ram_match.group(1)
            # Only consider standard RAM sizes (4, 6, 8, 12, 16, 18, 24, 32, 36, 64)
            if int(val) in [4, 6, 8, 12, 16, 18, 24, 32, 36, 64]:
                ram = f"{val}GB"

        # 3. Storage extraction (e.g., "128gb", "256 gb", "512gb", "1tb", "2tb ssd")
        storage = None
        tb_match = re.search(r"\b([124])\s*(?:tb|terabyte)\s*(?:ssd|storage|rom)?\b", t_lower)
        if tb_match:
            storage = f"{tb_match.group(1)}TB"
        else:
            gb_match = re.search(r"\b(64|128|256|512)\s*(?:gb)?\s*(?:storage|ssd|rom|rom\b)?\b", t_lower)
            if gb_match:
                storage = f"{gb_match.group(1)}GB"

        # 4. Color extraction
        color = None
        for c in cls.COMMON_COLORS:
            if re.search(rf"\b{c}\b", t_lower):
                color = c.title()
                break

        # 5. Model number pattern (e.g. SM-S931B, 16IRX9, MRXN3HN/A)
        model = None
        model_match = re.search(r"\b([a-z]{1,3}\d{3,5}[a-z0-9\/\-]*)\b", t_lower)
        if model_match:
            model = model_match.group(1).upper()

        return ExtractedAttributes(
            normalized_title=norm,
            brand=brand,
            model_number=model,
            ram=ram,
            storage=storage,
            color=color,
        )

    @classmethod
    def match_variant_with_listing(
        cls,
        variant_name: str,
        variant_ram: Optional[str],
        variant_storage: Optional[str],
        variant_color: Optional[str],
        product_name: str,
        listing_title: str,
    ) -> MatchResult:
        """
        Determines whether an external marketplace listing matches an exact canonical variant.
        Enforces strict variant isolation: different storage or RAM results in REJECTED_MATCH.
        """
        listing_attrs = cls.extract_attributes(listing_title)
        v_lower = variant_name.lower()
        p_lower = product_name.lower()

        evidence: Dict[str, Any] = {
            "listing_extracted": listing_attrs.model_dump(),
            "target_variant": {
                "ram": variant_ram,
                "storage": variant_storage,
                "color": variant_color,
                "product_name": product_name,
            }
        }

        # 1. Strict Storage Invariant: If both specify storage and they differ -> REJECT
        if variant_storage and listing_attrs.storage:
            v_s = re.sub(r"\s+", "", variant_storage.upper())
            l_s = re.sub(r"\s+", "", listing_attrs.storage.upper())
            if v_s != l_s:
                return MatchResult(
                    outcome=MatchOutcome.REJECTED_MATCH,
                    confidence_score=0.1,
                    evidence=evidence,
                    rejection_reason=f"Storage mismatch: target={v_s} vs listing={l_s}",
                )

        # 2. Strict RAM Invariant: If both specify RAM and they differ -> REJECT
        if variant_ram and listing_attrs.ram:
            v_r = re.sub(r"\s+", "", variant_ram.upper())
            l_r = re.sub(r"\s+", "", listing_attrs.ram.upper())
            if v_r != l_r:
                return MatchResult(
                    outcome=MatchOutcome.REJECTED_MATCH,
                    confidence_score=0.1,
                    evidence=evidence,
                    rejection_reason=f"RAM mismatch: target={v_r} vs listing={l_r}",
                )

        # 3. Base product title similarity using RapidFuzz
        clean_listing_title = cls.normalize_title(listing_title)
        clean_product_name = cls.normalize_title(product_name)

        # Token set ratio handles word reordering across marketplaces
        token_ratio = fuzz.token_set_ratio(clean_product_name, clean_listing_title)
        partial_ratio = fuzz.partial_ratio(clean_product_name, clean_listing_title)
        title_similarity = (token_ratio * 0.7 + partial_ratio * 0.3) / 100.0

        evidence["title_similarity"] = round(title_similarity, 3)

        if title_similarity < 0.65:
            return MatchResult(
                outcome=MatchOutcome.REJECTED_MATCH,
                confidence_score=round(title_similarity, 3),
                evidence=evidence,
                rejection_reason="Product title similarity too low",
            )

        # 4. Attribute bonus
        bonus = 0.0
        if variant_storage and listing_attrs.storage and variant_storage.upper() == listing_attrs.storage.upper():
            bonus += 0.15
        if variant_ram and listing_attrs.ram and variant_ram.upper() == listing_attrs.ram.upper():
            bonus += 0.10
        if variant_color and listing_attrs.color and variant_color.lower() in listing_title.lower():
            bonus += 0.05

        final_score = min(1.0, title_similarity + bonus)
        evidence["final_score"] = round(final_score, 3)

        if final_score >= 0.85:
            return MatchResult(
                outcome=MatchOutcome.CONFIRMED_MATCH,
                confidence_score=round(final_score, 3),
                evidence=evidence,
            )
        elif final_score >= 0.70:
            return MatchResult(
                outcome=MatchOutcome.PROBABLE_MATCH,
                confidence_score=round(final_score, 3),
                evidence=evidence,
            )
        else:
            return MatchResult(
                outcome=MatchOutcome.REJECTED_MATCH,
                confidence_score=round(final_score, 3),
                evidence=evidence,
                rejection_reason="Confidence below threshold",
            )
