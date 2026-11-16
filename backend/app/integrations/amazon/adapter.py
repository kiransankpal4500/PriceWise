import re
import asyncio
from datetime import datetime, timezone
from typing import List, Optional
import httpx
from bs4 import BeautifulSoup
from app.integrations.base import BaseMarketplaceAdapter, MarketplaceRawProduct, ProviderStatus

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-IN,en;q=0.9",
    "Referer": "https://www.amazon.in/",
}


class AmazonIndiaAdapter(BaseMarketplaceAdapter):
    def __init__(self):
        super().__init__(name="Amazon India", slug="amazon", is_demo=False)
        self.base_url = "https://www.amazon.in"

    def get_capabilities(self) -> List[str]:
        return ["search", "product_details", "price_check"]

    async def search_products(self, query: str, limit: int = 10) -> List[MarketplaceRawProduct]:
        # Check if rate-limited
        info = self.get_info()
        if info.status == ProviderStatus.RATE_LIMITED:
            return []

        search_url = f"{self.base_url}/s"
        params = {"k": query}

        try:
            async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
                resp = await client.get(search_url, params=params, headers=HEADERS)

                # Check for anti-robot checks or 503
                if resp.status_code == 503 or "api-services-support@amazon.com" in resp.text or "validateCaptcha" in resp.text:
                    self.set_rate_limited(cooldown_seconds=120, error_msg="Amazon robot-check triggered (status 503/captcha)")
                    return []

                if resp.status_code != 200:
                    self.status = ProviderStatus.DEGRADED
                    self.last_error = f"HTTP {resp.status_code}"
                    return []

                self.last_successful_request = datetime.now(timezone.utc)
                self.status = ProviderStatus.AVAILABLE

                soup = BeautifulSoup(resp.text, "lxml")
                items: List[MarketplaceRawProduct] = []

                # Find product cards
                cards = soup.select('div[data-component-type="s-search-result"]')
                for card in cards[:limit]:
                    asin = card.get("data-asin")
                    if not asin:
                        continue

                    title_elem = card.select_one("h2 span")
                    if not title_elem:
                        continue
                    title = title_elem.text.strip()

                    # Price
                    price_whole = card.select_one(".a-price-whole")
                    if not price_whole:
                        continue
                    price_str = price_whole.text.replace(",", "").replace(".", "").strip()
                    try:
                        price = float(price_str)
                    except ValueError:
                        continue

                    # MRP
                    mrp = None
                    mrp_elem = card.select_one(".a-price.a-text-price span.a-offscreen")
                    if mrp_elem:
                        mrp_clean = re.sub(r"[^\d.]", "", mrp_elem.text.replace(",", ""))
                        try:
                            mrp = float(mrp_clean)
                        except ValueError:
                            pass

                    # Rating
                    rating = 0.0
                    rating_elem = card.select_one('i[class*="a-star-"] span.a-icon-alt')
                    if rating_elem:
                        r_match = re.search(r"([\d.]+)\s+out of", rating_elem.text)
                        if r_match:
                            try:
                                rating = float(r_match.group(1))
                            except ValueError:
                                pass

                    # Review count
                    review_count = 0
                    rev_elem = card.select_one('span[aria-label*="ratings"], a[href*="#customerReviews"] span')
                    if rev_elem:
                        c_clean = re.sub(r"[^\d]", "", rev_elem.text)
                        if c_clean:
                            try:
                                review_count = int(c_clean)
                            except ValueError:
                                pass

                    # Image URL
                    img_elem = card.select_one("img.s-image")
                    image_url = img_elem.get("src") if img_elem else None

                    # Product URL
                    link_elem = card.select_one("h2 a")
                    product_url = f"{self.base_url}{link_elem.get('href')}" if link_elem and link_elem.get("href") else f"{self.base_url}/dp/{asin}"

                    items.append(
                        MarketplaceRawProduct(
                            marketplace_slug="amazon",
                            external_id=asin,
                            title=title,
                            product_url=product_url,
                            image_url=image_url,
                            current_price=price,
                            original_mrp=mrp or price,
                            rating=rating,
                            review_count=review_count,
                            seller_name="Amazon India Seller",
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
        # Check if rate-limited
        info = self.get_info()
        if info.status == ProviderStatus.RATE_LIMITED:
            return None

        url = f"{self.base_url}/dp/{external_id}"
        try:
            async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
                resp = await client.get(url, headers=HEADERS)
                if resp.status_code == 503 or "validateCaptcha" in resp.text:
                    self.set_rate_limited(cooldown_seconds=120, error_msg="Amazon rate wall active")
                    return None
                if resp.status_code != 200:
                    return None

                soup = BeautifulSoup(resp.text, "lxml")
                title_elem = soup.select_one("#productTitle")
                if not title_elem:
                    return None
                title = title_elem.text.strip()

                price = 0.0
                price_elem = soup.select_one(".a-price-whole")
                if price_elem:
                    price_str = price_elem.text.replace(",", "").replace(".", "").strip()
                    try:
                        price = float(price_str)
                    except ValueError:
                        pass

                return MarketplaceRawProduct(
                    marketplace_slug="amazon",
                    external_id=external_id,
                    title=title,
                    product_url=url,
                    current_price=price,
                    original_mrp=price,
                    availability="IN_STOCK",
                    is_demo=False,
                )
        except Exception as e:
            self.last_error = str(e)
            return None
