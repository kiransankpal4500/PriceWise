import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.session import get_db
from app.models.users import User
from app.models.tracking import Watchlist
from app.models.catalog import Product, ProductVariant, Brand, Category
from app.models.marketplaces import MarketplaceListing
from app.api.deps import require_current_user
from app.schemas.products import ProductSummarySchema

router = APIRouter()


class WatchlistAddRequest(BaseModel):
    variant_id: str


@router.get("", response_model=List[ProductSummarySchema])
async def get_watchlist(
    current_user: User = Depends(require_current_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(Watchlist, ProductVariant, Product, Brand, Category, MarketplaceListing)
        .join(ProductVariant, ProductVariant.id == Watchlist.variant_id)
        .join(Product, Product.id == ProductVariant.product_id)
        .join(Brand, Brand.id == Product.brand_id)
        .join(Category, Category.id == Product.category_id)
        .join(MarketplaceListing, MarketplaceListing.variant_id == ProductVariant.id)
        .where(Watchlist.user_id == current_user.id)
        .order_by(Watchlist.created_at.desc())
    )
    res = await db.execute(stmt)
    rows = res.all()

    seen = set()
    items = []
    for w, v, p, b, c, l in rows:
        if v.id in seen:
            continue
        seen.add(v.id)

        mrp = float(v.mrp)
        price = float(l.current_price)
        disc = round(((mrp - price) / mrp) * 100.0, 1) if mrp > price else 0.0

        items.append(
            ProductSummarySchema(
                id=p.id,
                name=f"{p.name} ({v.name})",
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
    return items


@router.post("", status_code=status.HTTP_201_CREATED)
async def add_to_watchlist(
    body: WatchlistAddRequest,
    current_user: User = Depends(require_current_user),
    db: AsyncSession = Depends(get_db),
):
    # Check if already in watchlist
    stmt = select(Watchlist).where(
        Watchlist.user_id == current_user.id,
        Watchlist.variant_id == body.variant_id,
    )
    res = await db.execute(stmt)
    if res.scalar_one_or_none():
        return {"status": "ALREADY_SAVED", "message": "Product is already in your watchlist"}

    item = Watchlist(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        variant_id=body.variant_id,
    )
    db.add(item)
    await db.commit()
    return {"status": "SUCCESS", "message": "Product saved to watchlist"}


@router.delete("/{variant_id}")
async def remove_from_watchlist(
    variant_id: str,
    current_user: User = Depends(require_current_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Watchlist).where(
        Watchlist.user_id == current_user.id,
        Watchlist.variant_id == variant_id,
    )
    res = await db.execute(stmt)
    item = res.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found in watchlist")

    await db.delete(item)
    await db.commit()
    return {"status": "SUCCESS", "message": "Item removed from watchlist"}
