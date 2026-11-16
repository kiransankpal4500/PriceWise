import asyncio
import os
import sys
from pathlib import Path

# Add backend to sys.path
backend_dir = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from sqlalchemy import select, func
from app.database.session import AsyncSessionLocal
from app.models import Product, Category, ProductVariant, MarketplaceListing, PriceHistory, User


async def main():
    async with AsyncSessionLocal() as session:
        c = await session.scalar(select(func.count(Category.id)))
        p = await session.scalar(select(func.count(Product.id)))
        v = await session.scalar(select(func.count(ProductVariant.id)))
        l = await session.scalar(select(func.count(MarketplaceListing.id)))
        ph = await session.scalar(select(func.count(PriceHistory.id)))
        u = await session.scalar(select(func.count(User.id)))
        print(f"Categories: {c}")
        print(f"Products: {p}")
        print(f"Variants: {v}")
        print(f"Marketplace Listings: {l}")
        print(f"Price History Observations: {ph}")
        print(f"Users: {u}")
        assert c >= 10, "Expected at least 10 categories"
        assert p >= 10, "Expected at least 10 products"
        assert l >= 10, "Expected listings"
        print("ALL DATABASE CHECKS PASSED!")


if __name__ == "__main__":
    asyncio.run(main())
