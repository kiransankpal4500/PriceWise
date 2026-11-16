from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from app.schemas.products import ProductSummarySchema


class ChatMessage(BaseModel):
    role: str  # user, assistant, system
    content: str


class ChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: str = Field(..., min_length=1, max_length=2000)
    category_slug: Optional[str] = None
    max_budget: Optional[float] = None


class ExtractedRequirement(BaseModel):
    category_slug: Optional[str] = None
    budget: Optional[float] = None
    preferred_brands: List[str] = []
    key_priorities: List[str] = []  # e.g. ["battery", "gaming", "camera"]


class ChatResponse(BaseModel):
    conversation_id: str
    message: str
    extracted_requirements: Optional[ExtractedRequirement] = None
    recommended_products: List[ProductSummarySchema] = []
    suggested_follow_ups: List[str] = []
    tokens_used: Optional[int] = 0
    model_used: str
