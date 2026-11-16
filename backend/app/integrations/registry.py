import asyncio
from typing import Dict, List, Optional
from app.integrations.base import BaseMarketplaceAdapter, MarketplaceRawProduct, ProviderInfo, ProviderStatus
from app.integrations.amazon.adapter import AmazonIndiaAdapter
from app.integrations.flipkart.adapter import FlipkartAdapter
from app.integrations.demo.adapter import DummyJSONDemoAdapter
from app.core.config import settings


class IntegrationRegistry:
    def __init__(self):
        self._adapters: Dict[str, BaseMarketplaceAdapter] = {}
        # Register core adapters
        self.register(AmazonIndiaAdapter())
        self.register(FlipkartAdapter())
        if settings.ENABLE_DEMO_DATA:
            self.register(DummyJSONDemoAdapter())

    def register(self, adapter: BaseMarketplaceAdapter):
        self._adapters[adapter.slug] = adapter

    def get_adapter(self, slug: str) -> Optional[BaseMarketplaceAdapter]:
        return self._adapters.get(slug)

    def list_providers(self) -> List[ProviderInfo]:
        return [adapter.get_info() for adapter in self._adapters.values()]

    async def search_all(self, query: str, limit_per_provider: int = 5) -> Dict[str, List[MarketplaceRawProduct]]:
        """
        Queries all available adapters concurrently with graceful failure.
        """
        results: Dict[str, List[MarketplaceRawProduct]] = {}
        tasks = []
        slugs = []

        for slug, adapter in self._adapters.items():
            info = adapter.get_info()
            # Do not query rate-limited, disabled or unavailable adapters
            if info.status in [ProviderStatus.RATE_LIMITED, ProviderStatus.DISABLED, ProviderStatus.UNAVAILABLE]:
                results[slug] = []
                continue

            slugs.append(slug)
            tasks.append(adapter.search_products(query=query, limit=limit_per_provider))

        if not tasks:
            return results

        responses = await asyncio.gather(*tasks, return_exceptions=True)
        for slug, res in zip(slugs, responses):
            if isinstance(res, Exception):
                results[slug] = []
            else:
                results[slug] = res

        return results


# Global singleton registry
integration_registry = IntegrationRegistry()
