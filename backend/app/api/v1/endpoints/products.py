from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from app.database.session import get_db
from app.models.catalog import Product, ProductVariant, Category, Brand, Specification
from app.models.marketplaces import Marketplace, MarketplaceListing, PriceHistory, Review
from app.intelligence.analytics.price_prediction import PricePredictionEngine
from app.intelligence.reviews.analyzer import ReviewAnalyzer
from app.schemas.products import (
    ProductSummarySchema,
    ProductDetailSchema,
    ProductVariantSchema,
    MarketplaceListingSchema,
    SpecificationSchema,
    BrandSchema,
    CategorySchema,
)

router = APIRouter()


@router.get("", response_model=List[ProductSummarySchema])
async def list_products(
    category_slug: Optional[str] = None,
    brand_slug: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by: str = Query("relevance", pattern="^(relevance|price_asc|price_desc|rating)$"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(Product, Brand, Category, ProductVariant, MarketplaceListing, Marketplace)
        .join(Brand, Brand.id == Product.brand_id)
        .join(Category, Category.id == Product.category_id)
        .join(ProductVariant, ProductVariant.product_id == Product.id)
        .join(MarketplaceListing, MarketplaceListing.variant_id == ProductVariant.id)
        .join(Marketplace, Marketplace.id == MarketplaceListing.marketplace_id)
        .where(MarketplaceListing.current_price > 0)
    )

    if category_slug:
        stmt = stmt.where(Category.slug == category_slug)
    if brand_slug:
        stmt = stmt.where(Brand.slug == brand_slug)
    if min_price:
        stmt = stmt.where(MarketplaceListing.current_price >= min_price)
    if max_price:
        stmt = stmt.where(MarketplaceListing.current_price <= max_price)

    if sort_by == "price_asc":
        stmt = stmt.order_by(MarketplaceListing.current_price.asc())
    elif sort_by == "price_desc":
        stmt = stmt.order_by(MarketplaceListing.current_price.desc())
    elif sort_by == "rating":
        stmt = stmt.order_by(MarketplaceListing.rating.desc())

    offset = (page - 1) * page_size
    stmt = stmt.offset(offset).limit(page_size * 2)

    res = await db.execute(stmt)
    rows = res.all()

    seen_products = set()
    summaries: List[ProductSummarySchema] = []

    for p, b, c, v, l, mp in rows:
        if p.id in seen_products:
            continue
        seen_products.add(p.id)

        mrp = float(v.mrp)
        price = float(l.current_price)
        if price <= 0:
            continue
        disc = round(((mrp - price) / mrp) * 100.0, 1) if mrp > price else 0.0
        if disc > 90.0:
            disc = 0.0

        pred = PricePredictionEngine.analyze_price(price, mrp, [price, mrp * 0.95, mrp])
        summaries.append(
            ProductSummarySchema(
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
                best_price=price,
                mrp=mrp,
                discount_percentage=disc,
                marketplace_count=2,
                rating=l.rating,
                review_count=l.review_count,
                is_demo=l.is_demo,
                primary_variant_id=v.id,
                best_offer_url=l.product_url,
                best_offer_marketplace=mp.name,
                price_prediction=pred,
            )
        )
        if len(summaries) >= page_size:
            break

    return summaries


@router.get("/{id_or_slug}", response_model=ProductDetailSchema)
async def get_product_detail(id_or_slug: str, db: AsyncSession = Depends(get_db)):
    stmt = (
        select(Product, Brand, Category)
        .join(Brand, Brand.id == Product.brand_id)
        .join(Category, Category.id == Product.category_id)
        .where(or_(Product.id == id_or_slug, Product.slug == id_or_slug))
    )
    res = await db.execute(stmt)
    row = res.first()
    if not row:
        raise HTTPException(status_code=404, detail="Product not found")

    product, brand, category = row

    # Fetch variants
    v_res = await db.execute(select(ProductVariant).where(ProductVariant.product_id == product.id))
    variants = v_res.scalars().all()

    variants_schemas: List[ProductVariantSchema] = []
    all_prices = []
    best_listing_schema: Optional[MarketplaceListingSchema] = None
    min_price = float("inf")

    for v in variants:
        # Specs
        s_res = await db.execute(select(Specification).where(Specification.variant_id == v.id))
        specs = s_res.scalars().all()
        specs_schema = [SpecificationSchema(spec_group=s.spec_group, name=s.name, value=s.value) for s in specs]

        # Listings
        l_stmt = (
            select(MarketplaceListing, Marketplace)
            .join(Marketplace, Marketplace.id == MarketplaceListing.marketplace_id)
            .where(MarketplaceListing.variant_id == v.id)
        )
        l_res = await db.execute(l_stmt)
        listings_rows = l_res.all()

        listings_schemas: List[MarketplaceListingSchema] = []
        variant_best_price = None

        for l, mp in listings_rows:
            p = float(l.current_price)
            if p <= 0:
                continue
            all_prices.append(p)
            if p < min_price:
                min_price = p

            mrp_val = float(l.original_mrp or v.mrp)
            disc = round(((mrp_val - p) / mrp_val) * 100.0, 1) if mrp_val > p else 0.0
            if disc > 90.0:
                disc = 0.0

            ls = MarketplaceListingSchema(
                id=l.id,
                marketplace_id=mp.id,
                marketplace_name=mp.name,
                marketplace_slug=mp.slug,
                marketplace_logo=mp.logo_url,
                external_id=l.external_id,
                title=l.title,
                product_url=l.product_url,
                image_url=l.image_url or product.default_image_url,
                current_price=p,
                original_mrp=mrp_val,
                discount_percentage=disc,
                availability=l.availability,
                seller_name=l.seller_name,
                rating=l.rating,
                review_count=l.review_count,
                is_demo=l.is_demo,
                last_scraped_at=l.last_scraped_at,
            )
            listings_schemas.append(ls)

            if variant_best_price is None or p < variant_best_price:
                variant_best_price = p
            if best_listing_schema is None or p < best_listing_schema.current_price:
                best_listing_schema = ls

        variants_schemas.append(
            ProductVariantSchema(
                id=v.id,
                product_id=v.product_id,
                name=v.name,
                sku=v.sku,
                ram=v.ram,
                storage=v.storage,
                color=v.color,
                mrp=float(v.mrp),
                best_price=variant_best_price,
                specifications=specs_schema,
                listings=listings_schemas,
            )
        )

    # Calculate price stats from all historical observations
    hist_stmt = (
        select(PriceHistory.price)
        .join(MarketplaceListing, MarketplaceListing.id == PriceHistory.listing_id)
        .join(ProductVariant, ProductVariant.id == MarketplaceListing.variant_id)
        .where(ProductVariant.product_id == product.id)
    )
    h_res = await db.execute(hist_stmt)
    hist_prices = [float(p) for p in h_res.scalars().all()]
    if all_prices:
        hist_prices.extend(all_prices)

    low_p = min(hist_prices) if hist_prices else None
    high_p = max(hist_prices) if hist_prices else None
    avg_p = round(sum(hist_prices) / len(hist_prices), 2) if hist_prices else None

    # Review sentiment stats
    rev_stmt = (
        select(Review.sentiment, func.count(Review.id))
        .join(MarketplaceListing, MarketplaceListing.id == Review.listing_id)
        .join(ProductVariant, ProductVariant.id == MarketplaceListing.variant_id)
        .where(ProductVariant.product_id == product.id)
        .group_by(Review.sentiment)
    )
    rev_res = await db.execute(rev_stmt)
    sentiment_map = {}
    total_revs = 0
    for sent, count in rev_res.all():
        sentiment_map[sent or "NEUTRAL"] = count
        total_revs += count

    current_best_p = min_price if min_price != float("inf") else (low_p or 0.0)
    primary_mrp = float(variants[0].mrp) if variants else current_best_p
    pred = PricePredictionEngine.analyze_price(current_best_p, primary_mrp, hist_prices)

    review_intel = ReviewAnalyzer.analyze(
        rating=best_listing_schema.rating if best_listing_schema else 4.2,
        review_count=best_listing_schema.review_count if best_listing_schema else total_revs,
        category=category.name,
    )

    return ProductDetailSchema(
        id=product.id,
        name=product.name,
        slug=product.slug,
        brand=BrandSchema(id=brand.id, name=brand.name, slug=brand.slug, logo_url=brand.logo_url),
        category=CategorySchema(id=category.id, name=category.name, slug=category.slug, description=category.description, icon_name=category.icon_name),
        model_number=product.model_number,
        description=product.description,
        default_image_url=product.default_image_url,
        variants=variants_schemas,
        best_offer=best_listing_schema,
        lowest_recorded_price=low_p,
        highest_recorded_price=high_p,
        average_price=avg_p,
        total_reviews_analyzed=total_revs,
        sentiment_distribution=sentiment_map,
        price_prediction=pred,
        review_intelligence=review_intel,
    )


@router.get("/{id_or_slug}/redirect-best-deal")
async def redirect_to_best_deal(id_or_slug: str, db: AsyncSession = Depends(get_db)):
    stmt = (
        select(MarketplaceListing, Product, Marketplace)
        .join(ProductVariant, ProductVariant.id == MarketplaceListing.variant_id)
        .join(Product, Product.id == ProductVariant.product_id)
        .join(Marketplace, Marketplace.id == MarketplaceListing.marketplace_id)
        .where(or_(Product.id == id_or_slug, Product.slug == id_or_slug))
        .order_by(MarketplaceListing.current_price.asc())
    )
    res = await db.execute(stmt)
    row = res.first()
    if not row:
        raise HTTPException(status_code=404, detail="No active marketplace deal found for this product")

    best_listing, product, marketplace = row
    target_url = best_listing.product_url

    # Fallback only if URL is completely missing
    if not target_url:
        import urllib.parse
        encoded = urllib.parse.quote_plus(product.name)
        if "flipkart" in marketplace.slug.lower():
            target_url = f"https://www.flipkart.com/search?q={encoded}"
        else:
            target_url = f"https://www.amazon.in/s?k={encoded}"

    from fastapi.responses import RedirectResponse
    return RedirectResponse(url=target_url, status_code=307)


@router.get("/listings/{listing_id}/redirect")
async def redirect_listing(listing_id: str, db: AsyncSession = Depends(get_db)):
    stmt = (
        select(MarketplaceListing, Product, Marketplace)
        .join(ProductVariant, ProductVariant.id == MarketplaceListing.variant_id)
        .join(Product, Product.id == ProductVariant.product_id)
        .join(Marketplace, Marketplace.id == MarketplaceListing.marketplace_id)
        .where(MarketplaceListing.id == listing_id)
    )
    res = await db.execute(stmt)
    row = res.first()
    if not row:
        raise HTTPException(status_code=404, detail="Marketplace listing not found")

    listing, product, marketplace = row
    target_url = listing.product_url

    # Fallback only if URL is completely missing
    if not target_url:
        import urllib.parse
        encoded = urllib.parse.quote_plus(product.name)
        if "flipkart" in marketplace.slug.lower():
            target_url = f"https://www.flipkart.com/search?q={encoded}"
        else:
            target_url = f"https://www.amazon.in/s?k={encoded}"

    from fastapi.responses import RedirectResponse
    return RedirectResponse(url=target_url, status_code=307)
