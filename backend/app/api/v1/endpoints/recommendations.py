from typing import List, Dict, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.session import get_db
from app.models.catalog import Product, ProductVariant, Brand, Category, Specification
from app.models.marketplaces import MarketplaceListing
from app.schemas.recommendations import RecommendationRequest, RecommendationResponse
from app.intelligence.ranking.engine import RecommendationEngine, ScoredCandidate
from app.schemas.products import ProductSummarySchema

router = APIRouter()


@router.post("", response_model=RecommendationResponse)
async def get_recommendations(body: RecommendationRequest, db: AsyncSession = Depends(get_db)):
    stmt = (
        select(Product, Brand, Category, ProductVariant, MarketplaceListing)
        .join(Brand, Brand.id == Product.brand_id)
        .join(Category, Category.id == Product.category_id)
        .join(ProductVariant, ProductVariant.product_id == Product.id)
        .join(MarketplaceListing, MarketplaceListing.variant_id == ProductVariant.id)
    )

    if body.category_slug:
        stmt = stmt.where(Category.slug == body.category_slug)
    if body.preferred_brands:
        stmt = stmt.where(Brand.name.in_(body.preferred_brands))

    res = await db.execute(stmt)
    rows = res.all()

    seen_variants = set()
    candidates: List[ScoredCandidate] = []

    for p, b, c, v, l in rows:
        if v.id in seen_variants:
            continue
        seen_variants.add(v.id)

        # Get specs
        s_res = await db.execute(select(Specification).where(Specification.variant_id == v.id))
        specs = s_res.scalars().all()
        spec_dict = {s.name: s.value for s in specs}

        mrp_val = float(v.mrp)
        price_val = float(l.current_price)
        disc = round(((mrp_val - price_val) / mrp_val) * 100.0, 1) if mrp_val > price_val else 0.0

        prod_summary = ProductSummarySchema(
            id=p.id,
            name=p.name,
            slug=p.slug,
            brand_name=b.name,
            brand_slug=b.slug,
            category_name=c.name,
            category_slug=c.slug,
            model_number=p.model_number,
            description=p.description,
            image_url=p.default_image_url,
            best_price=price_val,
            mrp=mrp_val,
            discount_percentage=disc,
            marketplace_count=2,
            rating=l.rating,
            review_count=l.review_count,
            is_demo=l.is_demo,
            primary_variant_id=v.id,
        )

        candidates.append(
            ScoredCandidate(
                product=prod_summary,
                variant_id=v.id,
                price=price_val,
                mrp=mrp_val,
                rating=float(l.rating or 4.5),
                review_count=int(l.review_count or 100),
                category_slug=c.slug,
                specs=spec_dict,
            )
        )

    return RecommendationEngine.rank_candidates(candidates=candidates, request=body)
