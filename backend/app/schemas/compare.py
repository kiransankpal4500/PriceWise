from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from app.schemas.products import ProductVariantSchema, MarketplaceListingSchema


class CompareRequest(BaseModel):
    variant_ids: List[str] = Field(..., min_length=2, max_length=4)


class ProductCompareColumn(BaseModel):
    variant_id: str
    product_id: str
    product_name: str
    variant_name: str
    brand_name: str
    category_name: str
    image_url: Optional[str] = None
    best_price: float
    mrp: float
    rating: float
    review_count: int
    listings: List[MarketplaceListingSchema] = []
    specs: Dict[str, Dict[str, str]] = {}  # group -> {spec_name: spec_value}


class CompareResponse(BaseModel):
    products: List[ProductCompareColumn]
    all_spec_groups: List[str]
    specs_matrix: Dict[str, Dict[str, List[Optional[str]]]]  # group -> {spec_name -> [p1_val, p2_val, ...]}
    winner_variant_id: Optional[str] = None
    winner_rationale: Optional[str] = None
    compromises: Dict[str, List[str]] = {}  # variant_id -> [compromise 1, compromise 2]
