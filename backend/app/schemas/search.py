from typing import Optional, List, Dict
from pydantic import BaseModel, Field
from app.schemas.products import ProductSummarySchema


class SearchResponse(BaseModel):
    query: str
    total_results: int
    page: int
    page_size: int
    total_pages: int
    items: List[ProductSummarySchema]
    categories_found: List[str] = []
    brands_found: List[str] = []
    providers_consulted: Dict[str, str] = {}  # e.g. {"amazon": "AVAILABLE", "flipkart": "AVAILABLE"}
