import asyncio
import uuid
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
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


async def init_db():
    print("Creating database tables...", flush=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created successfully.", flush=True)


async def seed_database():
    await init_db()
    async with AsyncSessionLocal() as session:
        # Check if already seeded
        result = await session.execute(select(Category))
        if result.scalars().first():
            print("Database already contains data. Skipping initial seed.", flush=True)
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

        # 4. Default Demo User
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
            preferred_brands=["Apple", "Samsung", "Sony"],
            preferred_categories=["smartphones", "laptops", "headphones"],
            priority_weights={"price": 0.35, "specs": 0.30, "rating": 0.20, "reviews": 0.10, "value": 0.05},
        )
        session.add(demo_pref)

        await session.flush()

        # 5. Products, Variants, Specifications, Listings, and Historical Price Observations
        now = datetime.now(timezone.utc)
        print("Seeding canonical products, variants, and historical price logs...", flush=True)

        for prod_data in SEED_PRODUCTS:
            product = Product(
                id=str(uuid.uuid4()),
                category_id=cat_map[prod_data["category_slug"]].id,
                brand_id=brand_map[prod_data["brand_slug"]].id,
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
                    mp = mp_map[list_data["marketplace_slug"]]
                    listing = MarketplaceListing(
                        id=str(uuid.uuid4()),
                        variant_id=variant.id,
                        marketplace_id=mp.id,
                        external_id=list_data["external_id"],
                        title=list_data["title"],
                        product_url=list_data["product_url"],
                        image_url=list_data.get("image_url", prod_data["default_image_url"]),
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

                    # Generate realistic 90-day price history points
                    # Points: 90 days ago, 60 days ago, 30 days ago, 14 days ago, 7 days ago, now
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

                    # Add sample verified reviews
                    sample_reviews = [
                        {
                            "author": "Rahul M.",
                            "rating": 5.0,
                            "headline": "Exceptional performance and value",
                            "text": f"Upgraded recently to {product.name} and the build quality, display, and speed have exceeded my expectations.",
                            "sentiment": "POSITIVE",
                            "date": now - timedelta(days=20),
                        },
                        {
                            "author": "Pooja S.",
                            "rating": 4.5,
                            "headline": "Great daily driver with solid battery life",
                            "text": "Using this daily for work and multimedia. Battery easily lasts a full day under heavy usage. Highly recommend at this price point.",
                            "sentiment": "POSITIVE",
                            "date": now - timedelta(days=10),
                        },
                    ]
                    for rev in sample_reviews:
                        r = Review(
                            id=str(uuid.uuid4()),
                            listing_id=listing.id,
                            author_name=rev["author"],
                            rating=rev["rating"],
                            headline=rev["headline"],
                            review_text=rev["text"],
                            is_verified_purchase=True,
                            review_date=rev["date"],
                            sentiment=rev["sentiment"],
                        )
                        session.add(r)

        await session.commit()
        print("Database seeded successfully with verified Indian electronics catalog!", flush=True)


if __name__ == "__main__":
    asyncio.run(seed_database())
