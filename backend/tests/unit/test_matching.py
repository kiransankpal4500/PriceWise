import pytest
from app.intelligence.matching.matcher import ProductMatchingEngine, MatchOutcome


def test_attribute_extraction():
    attrs = ProductMatchingEngine.extract_attributes("Samsung Galaxy S25 5G (Onyx Black, 12GB RAM, 256GB Storage)")
    assert attrs.brand == "Samsung"
    assert attrs.ram == "12GB"
    assert attrs.storage == "256GB"
    assert attrs.color == "Onyx Black"


def test_strict_storage_isolation():
    # Attempting to match a 128GB target variant with a 256GB listing must be REJECTED
    result = ProductMatchingEngine.match_variant_with_listing(
        variant_name="128GB Storage, Onyx Black",
        variant_ram="12GB",
        variant_storage="128GB",
        variant_color="Onyx Black",
        product_name="Samsung Galaxy S25 5G",
        listing_title="Samsung Galaxy S25 5G (Onyx Black, 12GB RAM, 256GB Storage)",
    )
    assert result.outcome == MatchOutcome.REJECTED_MATCH
    assert "Storage mismatch" in result.rejection_reason


def test_confirmed_variant_match():
    # Identical variant attributes across title and variant
    result = ProductMatchingEngine.match_variant_with_listing(
        variant_name="128GB Storage, Onyx Black",
        variant_ram="12GB",
        variant_storage="128GB",
        variant_color="Onyx Black",
        product_name="Samsung Galaxy S25 5G",
        listing_title="Samsung Galaxy S25 5G (Onyx Black, 12GB RAM, 128GB Storage)",
    )
    assert result.outcome == MatchOutcome.CONFIRMED_MATCH
    assert result.confidence_score >= 0.85
