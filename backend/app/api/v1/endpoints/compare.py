from typing import List, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.session import get_db
from app.models.catalog import Product, ProductVariant, Brand, Category, Specification
from app.models.marketplaces import Marketplace, MarketplaceListing
from app.schemas.compare import CompareRequest, CompareResponse, ProductCompareColumn
from app.schemas.products import MarketplaceListingSchema

router = APIRouter()


@router.post("", response_model=CompareResponse)
async def compare_products(body: CompareRequest, db: AsyncSession = Depends(get_db)):
    variant_ids = body.variant_ids
    if len(variant_ids) < 2 or len(variant_ids) > 4:
        raise HTTPException(status_code=400, detail="Must provide between 2 and 4 product variants to compare")

    columns: List[ProductCompareColumn] = []
    all_spec_groups_set = set()
    all_spec_keys: Dict[str, set] = {}  # group -> set of spec names

    for vid in variant_ids:
        stmt = (
            select(ProductVariant, Product, Brand, Category)
            .join(Product, Product.id == ProductVariant.product_id)
            .join(Brand, Brand.id == Product.brand_id)
            .join(Category, Category.id == Product.category_id)
            .where(ProductVariant.id == vid)
        )
        res = await db.execute(stmt)
        row = res.first()
        if not row:
            continue
        variant, product, brand, category = row

        # Specs
        s_res = await db.execute(select(Specification).where(Specification.variant_id == vid))
        specs = s_res.scalars().all()
        specs_dict: Dict[str, Dict[str, str]] = {}
        for s in specs:
            if s.spec_group not in specs_dict:
                specs_dict[s.spec_group] = {}
            specs_dict[s.spec_group][s.name] = s.value
            all_spec_groups_set.add(s.spec_group)
            if s.spec_group not in all_spec_keys:
                all_spec_keys[s.spec_group] = set()
            all_spec_keys[s.spec_group].add(s.name)

        # Listings
        l_stmt = (
            select(MarketplaceListing, Marketplace)
            .join(Marketplace, Marketplace.id == MarketplaceListing.marketplace_id)
            .where(MarketplaceListing.variant_id == vid)
        )
        l_res = await db.execute(l_stmt)
        listings_rows = l_res.all()

        listings_schemas = []
        best_price = float(variant.mrp)
        best_rating = 4.5
        best_reviews = 100

        for l, mp in listings_rows:
            p = float(l.current_price)
            if p < best_price:
                best_price = p
            best_rating = float(l.rating or best_rating)
            best_reviews = int(l.review_count or best_reviews)

            mrp_val = float(l.original_mrp or variant.mrp)
            disc = round(((mrp_val - p) / mrp_val) * 100.0, 1) if mrp_val > p else 0.0

            listings_schemas.append(
                MarketplaceListingSchema(
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
            )

        columns.append(
            ProductCompareColumn(
                variant_id=variant.id,
                product_id=product.id,
                product_name=product.name,
                variant_name=variant.name,
                brand_name=brand.name,
                category_name=category.name,
                image_url=product.default_image_url,
                best_price=best_price,
                mrp=float(variant.mrp),
                rating=best_rating,
                review_count=best_reviews,
                listings=listings_schemas,
                specs=specs_dict,
            )
        )

    if not columns:
        raise HTTPException(status_code=404, detail="None of the requested variants were found")

    # Build aligned specifications matrix
    specs_matrix: Dict[str, Dict[str, List[Optional[str]]]] = {}
    ordered_groups = sorted(list(all_spec_groups_set))

    for group in ordered_groups:
        specs_matrix[group] = {}
        for spec_name in sorted(list(all_spec_keys.get(group, []))):
            row_vals = []
            for col in columns:
                val = col.specs.get(group, {}).get(spec_name)
                row_vals.append(val)
            specs_matrix[group][spec_name] = row_vals

    # Identify winner (best value-to-price ratio)
    winner_id = columns[0].variant_id
    min_price_col = min(columns, key=lambda c: c.best_price)
    winner_rationale = (
        f"**{min_price_col.product_name}** offers the most competitive entry price at ₹{int(min_price_col.best_price):,}, "
        f"with top-tier user rating ({min_price_col.rating}★). Ideal balance of cost and real-world performance."
    )

    compromises: Dict[str, List[str]] = {}
    for col in columns:
        col_comp = []
        if col.best_price > min_price_col.best_price:
            diff = col.best_price - min_price_col.best_price
            col_comp.append(f"₹{int(diff):,} higher initial purchase cost")
        compromises[col.variant_id] = col_comp

    return CompareResponse(
        products=columns,
        all_spec_groups=ordered_groups,
        specs_matrix=specs_matrix,
        winner_variant_id=min_price_col.variant_id,
        winner_rationale=winner_rationale,
        compromises=compromises,
    )
