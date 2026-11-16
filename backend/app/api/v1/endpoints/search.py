import math
from typing import Optional, List, Dict
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, func
from app.database.session import get_db
from app.models.catalog import Product, Brand, Category, ProductVariant
from app.models.marketplaces import MarketplaceListing
from app.schemas.search import SearchResponse
from app.schemas.products import ProductSummarySchema
from app.integrations.registry import integration_registry

router = APIRouter()


@router.get("", response_model=SearchResponse)
async def search_products(
    q: str = Query("", min_length=0, max_length=150),
    category: Optional[str] = None,
    brand: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    include_live_scraping: bool = Query(False),
    db: AsyncSession = Depends(get_db),
):
    query_clean = q.strip()

    stmt = (
        select(Product, Brand, Category, ProductVariant, MarketplaceListing)
        .join(Brand, Brand.id == Product.brand_id)
        .join(Category, Category.id == Product.category_id)
        .join(ProductVariant, ProductVariant.product_id == Product.id)
        .join(MarketplaceListing, MarketplaceListing.variant_id == ProductVariant.id)
    )

    if query_clean:
        q_wild = f"%{query_clean}%"
        stmt = stmt.where(
            or_(
                Product.name.ilike(q_wild),
                Brand.name.ilike(q_wild),
                Category.name.ilike(q_wild),
                ProductVariant.name.ilike(q_wild),
                Product.model_number.ilike(q_wild),
            )
        )

    if category:
        stmt = stmt.where(Category.slug == category)
    if brand:
        stmt = stmt.where(Brand.slug == brand)
    if min_price:
        stmt = stmt.where(MarketplaceListing.current_price >= min_price)
    if max_price:
        stmt = stmt.where(MarketplaceListing.current_price <= max_price)

    stmt = stmt.order_by(MarketplaceListing.current_price.asc())

    res = await db.execute(stmt)
    rows = res.all()

    seen_products = set()
    items: List[ProductSummarySchema] = []
    categories_found = set()
    brands_found = set()

    for p, b, c, v, l in rows:
        categories_found.add(c.name)
        brands_found.add(b.name)
        if p.id in seen_products:
            continue
        seen_products.add(p.id)

        mrp = float(v.mrp)
        price = float(l.current_price)
        disc = round(((mrp - price) / mrp) * 100.0, 1) if mrp > price else 0.0

        items.append(
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
            )
        )

    # Optional live scraping trigger if requested
    providers_status = {p.slug: p.status.value for p in integration_registry.list_providers()}
    if include_live_scraping and query_clean and len(items) < 3:
        # Fan out to marketplace adapters
        scraped = await integration_registry.search_all(query=query_clean, limit_per_provider=2)
        for slug, prods in scraped.items():
            for sp in prods:
                items.append(
                    ProductSummarySchema(
                        id=f"ext-{sp.external_id}",
                        name=sp.title[:80],
                        slug=f"ext-{sp.external_id}".lower(),
                        brand_name=sp.brand_hint or "Electronics",
                        brand_slug="electronics",
                        category_name="Search Results",
                        category_slug="search",
                        image_url=sp.image_url,
                        best_price=sp.current_price,
                        mrp=sp.original_mrp or sp.current_price,
                        discount_percentage=0.0,
                        marketplace_count=1,
                        rating=sp.rating,
                        review_count=sp.review_count,
                        is_demo=sp.is_demo,
                        primary_variant_id=f"ext-var-{sp.external_id}",
                    )
                )

    total_results = len(items)
    offset = (page - 1) * page_size
    paginated_items = items[offset : offset + page_size]
    total_pages = max(1, math.ceil(total_results / page_size))

    return SearchResponse(
        query=query_clean,
        total_results=total_results,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        items=paginated_items,
        categories_found=sorted(list(categories_found)),
        brands_found=sorted(list(brands_found)),
        providers_consulted=providers_status,
    )
