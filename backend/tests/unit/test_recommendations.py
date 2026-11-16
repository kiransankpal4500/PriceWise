import pytest
from app.intelligence.ranking.engine import RecommendationEngine, ScoredCandidate
from app.schemas.recommendations import RecommendationRequest
from app.schemas.products import ProductSummarySchema


def test_price_score_budget_penalty():
    # Exceeding budget should be severely penalized
    score_within = RecommendationEngine.calculate_price_score(price=45000, budget=50000)
    score_over = RecommendationEngine.calculate_price_score(price=60000, budget=50000)
    assert score_within > score_over
    assert score_over < 70.0


def test_rating_score_scaling():
    score_5 = RecommendationEngine.calculate_rating_score(5.0)
    score_4 = RecommendationEngine.calculate_rating_score(4.0)
    score_3 = RecommendationEngine.calculate_rating_score(3.0)
    assert score_5 == 100.0
    assert score_4 == 75.0
    assert score_3 == 50.0


def test_deterministic_ranking():
    c1 = ScoredCandidate(
        product=ProductSummarySchema(
            id="p1", name="Budget Phone", slug="budget-phone", brand_name="BrandA",
            brand_slug="branda", category_name="Smartphones", category_slug="smartphones",
            best_price=20000, mrp=25000, marketplace_count=2, rating=4.5, review_count=500, primary_variant_id="v1"
        ),
        variant_id="v1", price=20000, mrp=25000, rating=4.5, review_count=500, category_slug="smartphones"
    )
    c2 = ScoredCandidate(
        product=ProductSummarySchema(
            id="p2", name="Expensive Phone", slug="expensive-phone", brand_name="BrandB",
            brand_slug="brandb", category_name="Smartphones", category_slug="smartphones",
            best_price=80000, mrp=90000, marketplace_count=2, rating=4.7, review_count=200, primary_variant_id="v2"
        ),
        variant_id="v2", price=80000, mrp=90000, rating=4.7, review_count=200, category_slug="smartphones"
    )
    req = RecommendationRequest(max_budget=50000, intent="best_budget")
    resp = RecommendationEngine.rank_candidates([c1, c2], req)
    assert len(resp.recommendations) == 2
    assert resp.recommendations[0].variant_id == "v1"
    assert resp.recommendations[0].scores.overall_score > resp.recommendations[1].scores.overall_score
