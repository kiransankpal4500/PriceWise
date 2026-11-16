from datetime import datetime, timezone
from typing import List, Optional
import httpx
from app.integrations.base import BaseMarketplaceAdapter, MarketplaceRawProduct, ProviderStatus


class DummyJSONDemoAdapter(BaseMarketplaceAdapter):
    """
    Demo/Fallback adapter using DummyJSON public API.
    All data is strictly marked with is_demo=True and labeled DEMO DATA in UI.
    """
    def __init__(self):
        super().__init__(name="DummyJSON Demo Provider", slug="demo", is_demo=True)
        self.base_url = "https://dummyjson.com/products"

    def get_capabilities(self) -> List[str]:
        return ["search", "product_details", "demo_mode"]

    async def search_products(self, query: str, limit: int = 10) -> List[MarketplaceRawProduct]:
        try:
            url = f"{self.base_url}/search"
            params = {"q": query, "limit": limit}
            async with httpx.AsyncClient(timeout=8.0) as client:
                resp = await client.get(url, params=params)
                if resp.status_code != 200:
                    self.status = ProviderStatus.DEGRADED
                    return []

                data = resp.json()
                products = data.get("products", [])
                items: List[MarketplaceRawProduct] = []

                for p in products:
                    # Convert USD to approximate INR for display realism
                    price_usd = float(p.get("price", 100))
                    price_inr = round(price_usd * 86.0, 2)
                    discount_pct = float(p.get("discountPercentage", 10))
                    mrp_inr = round(price_inr * (1 + discount_pct / 100.0), 2)

                    items.append(
                        MarketplaceRawProduct(
                            marketplace_slug="demo",
                            external_id=f"DEMO-{p.get('id')}",
                            title=f"[DEMO DATA] {p.get('title')}",
                            product_url=f"https://dummyjson.com/products/{p.get('id')}",
                            image_url=p.get("thumbnail"),
                            current_price=price_inr,
                            original_mrp=mrp_inr,
                            rating=float(p.get("rating", 4.0)),
                            review_count=len(p.get("reviews", [])) * 10,
                            seller_name="Demo Market Vendor",
                            availability="IN_STOCK",
                            is_demo=True,
                            brand_hint=p.get("brand"),
                        )
                    )

                self.status = ProviderStatus.AVAILABLE
                self.last_successful_request = datetime.now(timezone.utc)
                return items
        except Exception as e:
            self.status = ProviderStatus.DEGRADED
            self.last_error = str(e)
            return []

    async def get_product_details(self, external_id: str) -> Optional[MarketplaceRawProduct]:
        try:
            raw_id = external_id.replace("DEMO-", "")
            url = f"{self.base_url}/{raw_id}"
            async with httpx.AsyncClient(timeout=8.0) as client:
                resp = await client.get(url)
                if resp.status_code != 200:
                    return None
                p = resp.json()
                price_usd = float(p.get("price", 100))
                price_inr = round(price_usd * 86.0, 2)
                return MarketplaceRawProduct(
                    marketplace_slug="demo",
                    external_id=external_id,
                    title=f"[DEMO DATA] {p.get('title')}",
                    product_url=f"https://dummyjson.com/products/{p.get('id')}",
                    image_url=p.get("thumbnail"),
                    current_price=price_inr,
                    original_mrp=price_inr * 1.1,
                    rating=float(p.get("rating", 4.0)),
                    availability="IN_STOCK",
                    is_demo=True,
                )
        except Exception:
            return None
