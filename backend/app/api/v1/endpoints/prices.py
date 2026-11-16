from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.database.session import get_db
from app.models.catalog import ProductVariant
from app.models.marketplaces import Marketplace, MarketplaceListing, PriceHistory

router = APIRouter()


@router.get("/{variant_id}/prices")
async def get_price_history(
    variant_id: str,
    days: int = Query(90, ge=7, le=365),
    db: AsyncSession = Depends(get_db),
):
    # Verify variant exists
    v_res = await db.execute(select(ProductVariant).where(ProductVariant.id == variant_id))
    variant = v_res.scalar_one_or_none()
    if not variant:
        raise HTTPException(status_code=404, detail="Product variant not found")

    since_date = datetime.now(timezone.utc) - timedelta(days=days)

    stmt = (
        select(PriceHistory, MarketplaceListing, Marketplace)
        .join(MarketplaceListing, MarketplaceListing.id == PriceHistory.listing_id)
        .join(Marketplace, Marketplace.id == MarketplaceListing.marketplace_id)
        .where(
            and_(
                MarketplaceListing.variant_id == variant_id,
                PriceHistory.observed_at >= since_date,
            )
        )
        .order_by(PriceHistory.observed_at.asc())
    )
    res = await db.execute(stmt)
    rows = res.all()

    points = []
    prices_list = []
    for ph, l, mp in rows:
        p = float(ph.price)
        prices_list.append(p)
        points.append({
            "date": ph.observed_at.strftime("%Y-%m-%d"),
            "price": p,
            "marketplace": mp.name,
            "marketplace_slug": mp.slug,
            "source": ph.source,
        })

    lowest = min(prices_list) if prices_list else float(variant.mrp)
    highest = max(prices_list) if prices_list else float(variant.mrp)
    avg = round(sum(prices_list) / len(prices_list), 2) if prices_list else float(variant.mrp)
    current = prices_list[-1] if prices_list else float(variant.mrp)

    trend = "STABLE"
    if len(prices_list) >= 2:
        if prices_list[-1] < prices_list[0]:
            trend = "DOWNWARD"
        elif prices_list[-1] > prices_list[0]:
            trend = "UPWARD"

    return {
        "variant_id": variant_id,
        "variant_name": variant.name,
        "currency": "INR",
        "days_covered": days,
        "lowest_price": lowest,
        "highest_price": highest,
        "average_price": avg,
        "current_price": current,
        "trend": trend,
        "history": points,
    }
