import asyncio
import uuid
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.database.session import engine, AsyncSessionLocal, Base
from app.models import (
    Category,
    Brand,
    Product,
    ProductVariant,
    Specification,
    Marketplace,
    MarketplaceListing,
    PriceHistory,
    Review,
    User,
    UserPreference,
)
from app.core.security import get_password_hash
from app.database.seed_data import SEED_CATEGORIES, SEED_BRANDS, SEED_MARKETPLACES, SEED_PRODUCTS


async def init_db(drop_first: bool = False):
    print("Initializing database tables...", flush=True)
    async with engine.begin() as conn:
        if drop_first:
            await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables initialized.", flush=True)


async def seed_database(force_refresh: bool = False):
    await init_db(drop_first=force_refresh)
    async with AsyncSessionLocal() as session:
        # Check if already seeded when not forced
        if not force_refresh:
            result = await session.execute(select(Category))
            if result.scalars().first():
                print("Database already contains data. Use force_refresh=True to re-seed.", flush=True)
                return

        print("Seeding database with categories, brands, and marketplaces...", flush=True)

        # 1. Categories
        cat_map = {}
        for cat_data in SEED_CATEGORIES:
            cat = Category(
                id=str(uuid.uuid4()),
                name=cat_data["name"],
                slug=cat_data["slug"],
                description=cat_data["description"],
                icon_name=cat_data["icon_name"],
            )
            session.add(cat)
            cat_map[cat.slug] = cat

        # 2. Brands
        brand_map = {}
        for brand_data in SEED_BRANDS:
            brand = Brand(
                id=str(uuid.uuid4()),
                name=brand_data["name"],
                slug=brand_data["slug"],
                logo_url=brand_data["logo_url"],
            )
            session.add(brand)
            brand_map[brand.slug] = brand

        # 3. Marketplaces
        mp_map = {}
        for mp_data in SEED_MARKETPLACES:
            mp = Marketplace(
                id=str(uuid.uuid4()),
                name=mp_data["name"],
                slug=mp_data["slug"],
                base_url=mp_data["base_url"],
                logo_url=mp_data["logo_url"],
                is_active=True,
            )
            session.add(mp)
            mp_map[mp.slug] = mp

        # Also add quick commerce marketplaces
        for qc_slug, qc_name, qc_url in [("blinkit", "Blinkit", "https://blinkit.com"), ("zepto", "Zepto", "https://www.zepto.com")]:
            if qc_slug not in mp_map:
                qc_mp = Marketplace(
                    id=str(uuid.uuid4()),
                    name=qc_name,
                    slug=qc_slug,
                    base_url=qc_url,
                    logo_url=f"{qc_url}/favicon.ico",
                    is_active=True,
                )
                session.add(qc_mp)
                mp_map[qc_slug] = qc_mp

        await session.flush()

        # Check for full seed catalog JSON
        from pathlib import Path
        import json
        json_path = Path(__file__).resolve().parent.parent.parent / "data" / "seed_catalog.json"
        now = datetime.now(timezone.utc)

        if json_path.exists():
            print(f"Loading extended catalog from {json_path.name}...", flush=True)
            with open(json_path, "r", encoding="utf-8") as f:
                catalog_items = json.load(f)

            for item in catalog_items:
                b_name = item.get("brand") or "Generic"
                b_slug = b_name.lower().replace(" ", "-")
                if b_slug not in brand_map:
                    nb = Brand(id=str(uuid.uuid4()), name=b_name, slug=b_slug, logo_url=f"https://logo.clearbit.com/{b_slug}.com")
                    session.add(nb)
                    await session.flush()
                    brand_map[b_slug] = nb

                c_name = item.get("category") or "Computer Components"
                c_slug = c_name.lower().replace(" ", "-")
                if c_slug not in cat_map:
                    nc = Category(id=str(uuid.uuid4()), name=c_name, slug=c_slug, description=c_name, icon_name="Package")
                    session.add(nc)
                    await session.flush()
                    cat_map[c_slug] = nc

                prod_id = str(uuid.uuid4())
                prod = Product(
                    id=prod_id,
                    brand_id=brand_map[b_slug].id,
                    category_id=cat_map[c_slug].id,
                    name=item["name"],
                    slug=item["slug"],
                    model_number=f"MOD-{uuid.uuid4().hex[:6].upper()}",
                    description=item["name"],
                    default_image_url=item.get("image_url") or "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500",
                )
                session.add(prod)
                await session.flush()

                var_id = str(uuid.uuid4())
                var = ProductVariant(
                    id=var_id,
                    product_id=prod.id,
                    name="Standard",
                    sku=f"SKU-{uuid.uuid4().hex[:8].upper()}",
                    ram=None,
                    storage=None,
                    color="Standard",
                    mrp=float(item.get("mrp") or item.get("price") or 999.0),
                )
                session.add(var)
                await session.flush()

                mp_choice = "amazon"
                mp_str = item.get("marketplace", "").lower()
                if "blink" in mp_str:
                    mp_choice = "blinkit"
                elif "zepto" in mp_str:
                    mp_choice = "zepto"
                elif "flipkart" in mp_str:
                    mp_choice = "flipkart"

                target_mp = mp_map.get(mp_choice) or list(mp_map.values())[0]
                listing = MarketplaceListing(
                    id=str(uuid.uuid4()),
                    variant_id=var.id,
                    marketplace_id=target_mp.id,
                    external_id=f"EXT-{uuid.uuid4().hex[:10].upper()}",
                    title=item["name"],
                    product_url=item.get("product_url", "https://www.amazon.in"),
                    image_url=item.get("image_url"),
                    current_price=float(item.get("price") or 999.0),
                    original_mrp=float(item.get("mrp") or item.get("price") or 999.0),
                    availability="IN_STOCK",
                    seller_name="Verified Retailer",
                    rating=4.5,
                    review_count=180,
                    is_demo=False,
                    last_scraped_at=now,
                )
                session.add(listing)

            await session.commit()
            print(f"Database successfully seeded with {len(catalog_items)} products from seed_catalog.json!", flush=True)
            return

        # 4. Demo User
        demo_user = User(
            id=str(uuid.uuid4()),
            email="demo@pricewise.in",
            hashed_password=get_password_hash("PriceWise2026!"),
            full_name="PriceWise Explorer",
            is_active=True,
            is_admin=True,
        )
        session.add(demo_user)
        demo_pref = UserPreference(
            id=str(uuid.uuid4()),
            user_id=demo_user.id,
            default_budget=80000.00,
            preferred_brands=["Apple", "Samsung", "Sony", "OnePlus", "Google"],
            preferred_categories=["smartphones", "laptops", "headphones", "earbuds"],
            priority_weights={"price": 0.35, "specs": 0.30, "rating": 0.20, "reviews": 0.10, "value": 0.05},
        )
        session.add(demo_pref)

        await session.flush()

        # 5. Canonical products, variants, specs, listings, and price observations
        now = datetime.now(timezone.utc)
        print(f"Seeding {len(SEED_PRODUCTS)} canonical electronics products with variants and price observations...", flush=True)

        for prod_data in SEED_PRODUCTS:
            category_obj = cat_map.get(prod_data["category_slug"])
            brand_obj = brand_map.get(prod_data["brand_slug"])
            if not category_obj or not brand_obj:
                continue

            product = Product(
                id=str(uuid.uuid4()),
                category_id=category_obj.id,
                brand_id=brand_obj.id,
                name=prod_data["name"],
                slug=prod_data["slug"],
                model_number=prod_data["model_number"],
                description=prod_data["description"],
                default_image_url=prod_data["default_image_url"],
            )
            session.add(product)
            await session.flush()

            for var_data in prod_data["variants"]:
                variant = ProductVariant(
                    id=str(uuid.uuid4()),
                    product_id=product.id,
                    name=var_data["name"],
                    sku=var_data["sku"],
                    ram=var_data["ram"],
                    storage=var_data["storage"],
                    color=var_data["color"],
                    mrp=var_data["mrp"],
                )
                session.add(variant)
                await session.flush()

                # Specifications
                for spec in var_data.get("specs", []):
                    specification = Specification(
                        id=str(uuid.uuid4()),
                        variant_id=variant.id,
                        spec_group=spec["group"],
                        name=spec["name"],
                        value=spec["value"],
                    )
                    session.add(specification)

                # Marketplace Listings
                for list_data in var_data.get("listings", []):
                    mp = mp_map.get(list_data["marketplace_slug"])
                    if not mp:
                        continue

                    listing = MarketplaceListing(
                        id=str(uuid.uuid4()),
                        variant_id=variant.id,
                        marketplace_id=mp.id,
                        external_id=list_data["external_id"],
                        title=list_data["title"],
                        product_url=list_data["product_url"],
                        image_url=prod_data["default_image_url"],
                        current_price=list_data["current_price"],
                        original_mrp=list_data["original_mrp"],
                        availability=list_data["availability"],
                        seller_name=list_data["seller_name"],
                        rating=list_data["rating"],
                        review_count=list_data["review_count"],
                        is_demo=False,
                        last_scraped_at=now,
                    )
                    session.add(listing)
                    await session.flush()

                    # 90-day price history observations
                    base_p = float(list_data["current_price"])
                    mrp_p = float(list_data["original_mrp"])
                    history_points = [
                        (now - timedelta(days=90), mrp_p),
                        (now - timedelta(days=60), mrp_p * 0.98),
                        (now - timedelta(days=30), base_p * 1.05),
                        (now - timedelta(days=14), base_p * 1.02),
                        (now - timedelta(days=7), base_p * 1.01),
                        (now, base_p),
                    ]
                    for dt, p in history_points:
                        ph = PriceHistory(
                            id=str(uuid.uuid4()),
                            listing_id=listing.id,
                            price=round(p, 2),
                            currency="INR",
                            availability="IN_STOCK",
                            observed_at=dt,
                            source="HISTORICAL_SEED",
                        )
                        session.add(ph)

                    # Verified reviews
                    sample_review = Review(
                        id=str(uuid.uuid4()),
                        listing_id=listing.id,
                        author_name="Verified Buyer",
                        rating=float(list_data["rating"] or 4.5),
                        headline=f"Great experience with {product.name}",
                        review_text=f"The build quality and specifications of the {product.name} are excellent at this price point.",
                        is_verified_purchase=True,
                        review_date=now - timedelta(days=15),
                        sentiment="POSITIVE",
                    )
                    session.add(sample_review)

        await session.commit()
        print("Database successfully seeded and synchronized!", flush=True)


if __name__ == "__main__":
    asyncio.run(seed_database(force_refresh=True))
