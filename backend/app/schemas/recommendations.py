from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from app.schemas.products import ProductSummarySchema


class RecommendationRequest(BaseModel):
    category_slug: Optional[str] = None
    max_budget: Optional[float] = None
    preferred_brands: Optional[List[str]] = None
    priorities: Optional[Dict[str, float]] = None  # e.g. {"price": 0.4, "specs": 0.4, "rating": 0.2}
    intent: Optional[str] = "best_overall"  # best_overall, best_budget, best_performance, best_camera, best_value
    limit: int = 5


class RecommendationScoreDetail(BaseModel):
    overall_score: float
    price_score: float
    spec_score: float
    rating_score: float
    review_volume_score: float
    value_score: float
    badge: Optional[str] = None  # "Top Pick", "Best Value", "Budget Champion"
    key_strengths: List[str] = []
    tradeoffs: List[str] = []


class RecommendedProductItem(BaseModel):
    product: ProductSummarySchema
    variant_id: str
    scores: RecommendationScoreDetail
    explanation: str


class RecommendationResponse(BaseModel):
    category_slug: Optional[str] = None
    budget_applied: Optional[float] = None
    algorithm_version: str = "v1.2-deterministic"
    weights_applied: Dict[str, float]
    recommendations: List[RecommendedProductItem]
