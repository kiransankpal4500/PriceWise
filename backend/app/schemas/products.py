from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from app.intelligence.analytics.price_prediction import PricePredictionVerdict
from app.intelligence.reviews.analyzer import ReviewIntelligence


class CategorySchema(BaseModel):
    id: str
    name: str
    slug: str
    description: Optional[str] = None
    icon_name: Optional[str] = None
    product_count: Optional[int] = 0

    model_config = {"from_attributes": True}


class BrandSchema(BaseModel):
    id: str
    name: str
    slug: str
    logo_url: Optional[str] = None

    model_config = {"from_attributes": True}


class SpecificationSchema(BaseModel):
    spec_group: str
    name: str
    value: str

    model_config = {"from_attributes": True}


class PriceHistoryPointSchema(BaseModel):
    price: float
    currency: str = "INR"
    availability: str = "IN_STOCK"
    observed_at: datetime
    source: str

    model_config = {"from_attributes": True}


class MarketplaceListingSchema(BaseModel):
    id: str
    marketplace_id: str
    marketplace_name: str
    marketplace_slug: str
    marketplace_logo: Optional[str] = None
    external_id: str
    title: str
    product_url: str
    image_url: Optional[str] = None
    current_price: float
    original_mrp: Optional[float] = None
    discount_percentage: Optional[float] = None
    availability: str
    seller_name: Optional[str] = None
    rating: Optional[float] = 0.0
    review_count: Optional[int] = 0
    is_demo: bool = False
    last_scraped_at: datetime

    model_config = {"from_attributes": True}


class ProductVariantSchema(BaseModel):
    id: str
    product_id: str
    name: str
    sku: str
    ram: Optional[str] = None
    storage: Optional[str] = None
    color: Optional[str] = None
    mrp: float
    best_price: Optional[float] = None
    specifications: List[SpecificationSchema] = []
    listings: List[MarketplaceListingSchema] = []

    model_config = {"from_attributes": True}


class ProductSummarySchema(BaseModel):
    id: str
    name: str
    slug: str
    brand_name: str
    brand_slug: str
    category_name: str
    category_slug: str
    model_number: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    best_price: float
    mrp: float
    discount_percentage: Optional[float] = None
    marketplace_count: int
    rating: Optional[float] = 0.0
    review_count: Optional[int] = 0
    is_demo: bool = False
    primary_variant_id: str
    best_offer_url: Optional[str] = None
    best_offer_marketplace: Optional[str] = None
    price_prediction: Optional[PricePredictionVerdict] = None

    model_config = {"from_attributes": True}


class ProductDetailSchema(BaseModel):
    id: str
    name: str
    slug: str
    brand: BrandSchema
    category: CategorySchema
    model_number: Optional[str] = None
    description: Optional[str] = None
    default_image_url: Optional[str] = None
    variants: List[ProductVariantSchema] = []
    best_offer: Optional[MarketplaceListingSchema] = None
    lowest_recorded_price: Optional[float] = None
    highest_recorded_price: Optional[float] = None
    average_price: Optional[float] = None
    total_reviews_analyzed: int = 0
    sentiment_distribution: Dict[str, float] = {}
    price_prediction: Optional[PricePredictionVerdict] = None
    review_intelligence: Optional[ReviewIntelligence] = None

    model_config = {"from_attributes": True}
