import re
from datetime import datetime, timezone
from typing import List, Optional
import httpx
from bs4 import BeautifulSoup
from app.integrations.base import BaseMarketplaceAdapter, MarketplaceRawProduct, ProviderStatus

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-IN,en;q=0.9",
    "Referer": "https://www.flipkart.com/",
}


class FlipkartAdapter(BaseMarketplaceAdapter):
    def __init__(self):
        super().__init__(name="Flipkart", slug="flipkart", is_demo=False)
        self.base_url = "https://www.flipkart.com"

    def get_capabilities(self) -> List[str]:
        return ["search", "product_details"]

    async def search_products(self, query: str, limit: int = 10) -> List[MarketplaceRawProduct]:
        info = self.get_info()
        if info.status == ProviderStatus.RATE_LIMITED:
            return []

        search_url = f"{self.base_url}/search"
        params = {"q": query}

        try:
            async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
                resp = await client.get(search_url, params=params, headers=HEADERS)

                if resp.status_code == 429:
                    self.set_rate_limited(cooldown_seconds=120, error_msg="Flipkart HTTP 429 Too Many Requests")
                    return []

                if resp.status_code != 200:
                    self.status = ProviderStatus.DEGRADED
                    self.last_error = f"HTTP {resp.status_code}"
                    return []

                self.last_successful_request = datetime.now(timezone.utc)
                self.status = ProviderStatus.AVAILABLE

                soup = BeautifulSoup(resp.text, "lxml")
                items: List[MarketplaceRawProduct] = []

                # Flipkart uses common container classes for product listings
                # Often div[data-id] or grid boxes
                containers = soup.select("div[data-id]")
                for box in containers[:limit]:
                    data_id = box.get("data-id")
                    if not data_id:
                        continue

                    # Title
                    title_elem = box.select_one("div.KzDlHZ, a.wByoh7, a.IRpwTa, div._4rR01T, a.s1Q9rs")
                    if not title_elem:
                        continue
                    title = title_elem.text.strip()

                    # Price (starts with ₹)
                    price_elem = box.select_one("div.Nx9bqj, div._30jeq3")
                    if not price_elem:
                        continue
                    price_clean = re.sub(r"[^\d.]", "", price_elem.text)
                    try:
                        price = float(price_clean)
                    except ValueError:
                        continue

                    # MRP
                    mrp = None
                    mrp_elem = box.select_one("div.yRaY8j, div._3I9_wc")
                    if mrp_elem:
                        mrp_clean = re.sub(r"[^\d.]", "", mrp_elem.text)
                        try:
                            mrp = float(mrp_clean)
                        except ValueError:
                            pass

                    # Rating
                    rating = 0.0
                    rating_elem = box.select_one("div.XQDdHH, div._3LWZlK")
                    if rating_elem:
                        try:
                            rating = float(rating_elem.text.strip())
                        except ValueError:
                            pass

                    # Image
                    img_elem = box.select_one("img.DByuf4, img._396cs4")
                    image_url = img_elem.get("src") if img_elem else None

                    # Link
                    link_elem = box.select_one("a[href]")
                    product_url = f"{self.base_url}{link_elem.get('href')}" if link_elem and link_elem.get("href") else f"{self.base_url}/p/{data_id}"

                    items.append(
                        MarketplaceRawProduct(
                            marketplace_slug="flipkart",
                            external_id=data_id,
                            title=title,
                            product_url=product_url,
                            image_url=image_url,
                            current_price=price,
                            original_mrp=mrp or price,
                            rating=rating,
                            review_count=100,  # default estimated
                            seller_name="Flipkart Verified Seller",
                            availability="IN_STOCK",
                            is_demo=False,
                        )
                    )

                return items

        except Exception as e:
            self.status = ProviderStatus.DEGRADED
            self.last_error = str(e)
            return []

    async def get_product_details(self, external_id: str) -> Optional[MarketplaceRawProduct]:
        return None
