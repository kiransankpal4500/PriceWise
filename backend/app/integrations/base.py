from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime, timezone, timedelta
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ProviderStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    DEGRADED = "DEGRADED"
    RATE_LIMITED = "RATE_LIMITED"
    UNAVAILABLE = "UNAVAILABLE"
    NOT_CONFIGURED = "NOT_CONFIGURED"
    DISABLED = "DISABLED"


class MarketplaceRawProduct(BaseModel):
    marketplace_slug: str
    external_id: str
    title: str
    product_url: str
    image_url: Optional[str] = None
    current_price: float
    original_mrp: Optional[float] = None
    rating: Optional[float] = 0.0
    review_count: Optional[int] = 0
    seller_name: Optional[str] = None
    availability: str = "IN_STOCK"
    is_demo: bool = False
    brand_hint: Optional[str] = None
    ram_hint: Optional[str] = None
    storage_hint: Optional[str] = None
    color_hint: Optional[str] = None
    model_number_hint: Optional[str] = None
    raw_specs: Dict[str, str] = {}


class ProviderInfo(BaseModel):
    name: str
    slug: str
    status: ProviderStatus
    capabilities: List[str]
    last_successful_request: Optional[datetime] = None
    last_error: Optional[str] = None
    rate_limit_cooldown_until: Optional[datetime] = None
    is_demo: bool = False


class BaseMarketplaceAdapter(ABC):
    def __init__(self, name: str, slug: str, is_demo: bool = False):
        self.name = name
        self.slug = slug
        self.is_demo = is_demo
        self.status = ProviderStatus.AVAILABLE
        self.last_successful_request: Optional[datetime] = None
        self.last_error: Optional[str] = None
        self.rate_limit_cooldown_until: Optional[datetime] = None

    def get_info(self) -> ProviderInfo:
        # Check if rate limit cooldown expired
        now = datetime.now(timezone.utc)
        if self.status == ProviderStatus.RATE_LIMITED and self.rate_limit_cooldown_until:
            if now >= self.rate_limit_cooldown_until:
                self.status = ProviderStatus.AVAILABLE
                self.rate_limit_cooldown_until = None

        return ProviderInfo(
            name=self.name,
            slug=self.slug,
            status=self.status,
            capabilities=self.get_capabilities(),
            last_successful_request=self.last_successful_request,
            last_error=self.last_error,
            rate_limit_cooldown_until=self.rate_limit_cooldown_until,
            is_demo=self.is_demo,
        )

    def set_rate_limited(self, cooldown_seconds: int = 60, error_msg: str = "Rate limited by marketplace"):
        self.status = ProviderStatus.RATE_LIMITED
        self.last_error = error_msg
        self.rate_limit_cooldown_until = datetime.now(timezone.utc) + timedelta(seconds=cooldown_seconds)

    @abstractmethod
    def get_capabilities(self) -> List[str]:
        pass

    @abstractmethod
    async def search_products(self, query: str, limit: int = 10) -> List[MarketplaceRawProduct]:
        pass

    @abstractmethod
    async def get_product_details(self, external_id: str) -> Optional[MarketplaceRawProduct]:
        pass
