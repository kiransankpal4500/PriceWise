import asyncio
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from app.models import Product, ProductVariant, Category, Brand, MarketplaceListing, Specification, PriceHistory
from app.intelligence.ranking.engine import RecommendationEngine, ScoredCandidate
from app.schemas.recommendations import RecommendationRequest
from app.schemas.products import ProductSummarySchema


class InternalAITools:
    @classmethod
    async def get_categories(cls, db: AsyncSession) -> List[Dict[str, Any]]:
        result = await db.execute(select(Category))
        categories = result.scalars().all()
        return [{"name": c.name, "slug": c.slug, "description": c.description} for c in categories]

    @classmethod
    async def search_products(
        cls,
        db: AsyncSession,
        query: str = "",
        category_slug: Optional[str] = None,
        max_budget: Optional[float] = None,
        limit: int = 5,
    ) -> List[Dict[str, Any]]:
        stmt = (
            select(Product, ProductVariant, MarketplaceListing, Brand, Category)
            .join(ProductVariant, ProductVariant.product_id == Product.id)
            .join(MarketplaceListing, MarketplaceListing.variant_id == ProductVariant.id)
            .join(Brand, Brand.id == Product.brand_id)
            .join(Category, Category.id == Product.category_id)
        )

        if category_slug:
            stmt = stmt.where(Category.slug == category_slug)

        if query:
            q_term = f"%{query}%"
            stmt = stmt.where(
                or_(
                    Product.name.ilike(q_term),
                    Brand.name.ilike(q_term),
                    ProductVariant.name.ilike(q_term),
                )
            )

        if max_budget and max_budget > 0:
            stmt = stmt.where(MarketplaceListing.current_price <= max_budget)

        stmt = stmt.order_by(MarketplaceListing.current_price.asc()).limit(limit * 2)
        result = await db.execute(stmt)
        rows = result.all()

        seen_products = set()
        matched = []
        for p, v, l, b, c in rows:
            if p.id in seen_products:
                continue
            seen_products.add(p.id)
            matched.append({
                "product_id": p.id,
                "variant_id": v.id,
                "name": p.name,
                "brand": b.name,
                "category": c.name,
                "variant_name": v.name,
                "ram": v.ram,
                "storage": v.storage,
                "best_price": float(l.current_price),
                "mrp": float(v.mrp),
                "rating": float(l.rating or 4.5),
                "review_count": int(l.review_count or 100),
                "product_url": l.product_url,
                "image_url": p.default_image_url,
            })
            if len(matched) >= limit:
                break

        return matched

    @classmethod
    async def get_product_details(cls, db: AsyncSession, product_id_or_slug: str) -> Optional[Dict[str, Any]]:
        stmt = (
            select(Product, Brand, Category)
            .join(Brand, Brand.id == Product.brand_id)
            .join(Category, Category.id == Product.category_id)
            .where(or_(Product.id == product_id_or_slug, Product.slug == product_id_or_slug))
        )
        result = await db.execute(stmt)
        row = result.first()
        if not row:
            return None

        product, brand, category = row

        # Fetch variants and listings
        v_stmt = select(ProductVariant).where(ProductVariant.product_id == product.id)
        v_res = await db.execute(v_stmt)
        variants = v_res.scalars().all()

        variants_data = []
        for v in variants:
            # Specs
            s_stmt = select(Specification).where(Specification.variant_id == v.id)
            s_res = await db.execute(s_stmt)
            specs = s_res.scalars().all()

            # Listings
            l_stmt = (
                select(MarketplaceListing, Marketplace)
                .join(Marketplace, Marketplace.id == MarketplaceListing.marketplace_id)
                .where(MarketplaceListing.variant_id == v.id)
            )
            l_res = await db.execute(l_stmt)
            listings = l_res.all()

            variants_data.append({
                "variant_id": v.id,
                "variant_name": v.name,
                "ram": v.ram,
                "storage": v.storage,
                "color": v.color,
                "mrp": float(v.mrp),
                "specifications": [{"group": s.spec_group, "name": s.name, "value": s.value} for s in specs],
                "offers": [
                    {
                        "marketplace": mp.name,
                        "price": float(l.current_price),
                        "mrp": float(l.original_mrp or v.mrp),
                        "rating": float(l.rating or 4.5),
                        "url": l.product_url,
                    }
                    for l, mp in listings
                ],
            })

        return {
            "product_id": product.id,
            "name": product.name,
            "brand": brand.name,
            "category": category.name,
            "description": product.description,
            "image_url": product.default_image_url,
            "variants": variants_data,
        }

    @classmethod
    async def get_price_history(cls, db: AsyncSession, variant_id: str) -> List[Dict[str, Any]]:
        stmt = (
            select(PriceHistory, MarketplaceListing, Marketplace)
            .join(MarketplaceListing, MarketplaceListing.id == PriceHistory.listing_id)
            .join(Marketplace, Marketplace.id == MarketplaceListing.marketplace_id)
            .where(MarketplaceListing.variant_id == variant_id)
            .order_by(PriceHistory.observed_at.asc())
        )
        result = await db.execute(stmt)
        rows = result.all()
        return [
            {
                "observed_at": ph.observed_at.isoformat(),
                "price": float(ph.price),
                "marketplace": mp.name,
                "source": ph.source,
            }
            for ph, l, mp in rows
        ]
