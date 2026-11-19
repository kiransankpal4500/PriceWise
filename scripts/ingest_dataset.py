"""
PriceWise Dataset Ingestion Script.
Usage:
    python scripts/ingest_dataset.py --file path/to/dataset.json
Supports bulk ingestion of electronics datasets with category/brand resolution and variant matching.
"""
import sys
import os
import json
import uuid
import asyncio
import argparse
from pathlib import Path
from datetime import datetime, timezone

# Add backend to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from sqlalchemy import select
from app.database.session import AsyncSessionLocal
from app.models import Category, Brand, Product, ProductVariant, Specification, MarketplaceListing, Marketplace, PriceHistory


async def ingest_products_from_json(file_path: str):
    path = Path(file_path)
    if not path.exists():
        print(f"ERROR: File not found: {file_path}")
        return

    print(f"Loading dataset from {file_path}...")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        print("ERROR: Dataset must be a JSON array of product objects.")
        return

    now = datetime.now(timezone.utc)
    ingested = 0

    async with AsyncSessionLocal() as session:
        # Load existing categories, brands, marketplaces
        cats = {c.slug: c for c in (await session.execute(select(Category))).scalars().all()}
        brands = {b.slug: b for b in (await session.execute(select(Brand))).scalars().all()}
        marketplaces = {m.slug: m for m in (await session.execute(select(Marketplace))).scalars().all()}

        # Default marketplace if not specified
        default_mp = marketplaces.get("amazon") or list(marketplaces.values())[0]

        for item in data:
            cat_slug = item.get("category_slug", "smartphones").lower()
            brand_slug = item.get("brand_slug", "generic").lower()

            # Create category if missing
            if cat_slug not in cats:
                new_cat = Category(
                    id=str(uuid.uuid4()),
                    name=cat_slug.replace("-", " ").title(),
                    slug=cat_slug,
                    description=f"{cat_slug.title()} electronics",
                )
                session.add(new_cat)
                await session.flush()
                cats[cat_slug] = new_cat

            # Create brand if missing
            if brand_slug not in brands:
                new_brand = Brand(
                    id=str(uuid.uuid4()),
                    name=brand_slug.replace("-", " ").title(),
                    slug=brand_slug,
                )
                session.add(new_brand)
                await session.flush()
                brands[brand_slug] = new_brand

            cat_obj = cats[cat_slug]
            brand_obj = brands[brand_slug]

            # Create Product
            prod_name = item.get("name", "Unknown Electronic Device")
            prod_slug = item.get("slug") or prod_name.lower().replace(" ", "-")[:50] + f"-{uuid.uuid4().hex[:6]}"

            product = Product(
                id=str(uuid.uuid4()),
                category_id=cat_obj.id,
                brand_id=brand_obj.id,
                name=prod_name,
                slug=prod_slug,
                model_number=item.get("model_number"),
                description=item.get("description", "High performance electronics product."),
                default_image_url=item.get("image_url", "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800"),
            )
            session.add(product)
            await session.flush()

            # Create Variant
            mrp = float(item.get("mrp", item.get("price", 10000)))
            price = float(item.get("price", mrp * 0.9))

            variant = ProductVariant(
                id=str(uuid.uuid4()),
                product_id=product.id,
                name=item.get("variant_name", "Standard Edition"),
                sku=f"SKU-{uuid.uuid4().hex[:8].upper()}",
                ram=item.get("ram"),
                storage=item.get("storage"),
                color=item.get("color"),
                mrp=mrp,
            )
            session.add(variant)
            await session.flush()

            # Create Specs
            specs_data = item.get("specifications", {})
            if isinstance(specs_data, dict):
                for k, v in specs_data.items():
                    spec = Specification(
                        id=str(uuid.uuid4()),
                        variant_id=variant.id,
                        spec_group="General",
                        name=k,
                        value=str(v),
                    )
                    session.add(spec)

            # Create Marketplace Listing with exact product URL via QuickCommerceAPI or item data
            raw_url = item.get("product_url")
            if not raw_url or raw_url == "https://www.amazon.in":
                # Try to fetch exact link from QuickCommerceAPI
                try:
                    import urllib.request
                    import json
                    platform = "Flipkart" if "flipkart" in default_mp.slug.lower() else "Amazon"
                    q_enc = urllib.parse.quote(prod_name.strip())
                    qc_url = f"https://api.quickcommerceapi.com/v1/search?q={q_enc}&platform={platform}&lat=28.6139&lon=77.2090"
                    qc_req = urllib.request.Request(qc_url, headers={"X-API-Key": "47861caa-b7aa-4d20-9ee3-9a2f1179eea3", "User-Agent": "Mozilla/5.0"})
                    with urllib.request.urlopen(qc_req, timeout=5) as qc_resp:
                        qc_data = json.loads(qc_resp.read().decode())
                        qc_prods = qc_data.get("data", {}).get("products", [])
                        if qc_prods and qc_prods[0].get("deeplink"):
                            marketplace_url = qc_prods[0].get("deeplink")
                        else:
                            marketplace_url = f"https://www.amazon.in/dp/B0DGJHBX5Y"
                except Exception:
                    clean_term = urllib.parse.quote_plus(prod_name.strip())
                    marketplace_url = f"https://www.flipkart.com/search?q={clean_term}" if "flipkart" in default_mp.slug.lower() else f"https://www.amazon.in/s?k={clean_term}"
            else:
                marketplace_url = raw_url

            listing = MarketplaceListing(
                id=str(uuid.uuid4()),
                variant_id=variant.id,
                marketplace_id=default_mp.id,
                external_id=f"EXT-{uuid.uuid4().hex[:10].upper()}",
                title=f"{prod_name} ({variant.name})",
                product_url=marketplace_url,
                image_url=product.default_image_url,
                current_price=price,
                original_mrp=mrp,
                availability="IN_STOCK",
                seller_name="Verified Retailer",
                rating=float(item.get("rating", 4.5)),
                review_count=int(item.get("review_count", 150)),
                is_demo=item.get("is_demo", False),
                last_scraped_at=now,
            )
            session.add(listing)
            await session.flush()

            # Initial price history point
            ph = PriceHistory(
                id=str(uuid.uuid4()),
                listing_id=listing.id,
                price=price,
                currency="INR",
                availability="IN_STOCK",
                observed_at=now,
                source="BULK_INGESTION",
            )
            session.add(ph)

            ingested += 1

        await session.commit()
        print(f"SUCCESS: Ingested {ingested} products into PriceWise database!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest JSON dataset into PriceWise")
    parser.add_argument("--file", type=str, required=True, help="Path to JSON dataset file")
    args = parser.parse_args()

    asyncio.run(ingest_products_from_json(args.file))
