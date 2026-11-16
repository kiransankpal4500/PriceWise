import uuid
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.session import get_db
from app.models.users import User
from app.models.tracking import PriceAlert
from app.models.catalog import Product, ProductVariant
from app.models.marketplaces import MarketplaceListing
from app.api.deps import require_current_user

router = APIRouter()


class CreateAlertRequest(BaseModel):
    variant_id: str
    target_price: float = Field(..., gt=0)


class AlertResponse(BaseModel):
    id: str
    variant_id: str
    product_name: str
    variant_name: str
    image_url: Optional[str] = None
    current_price: float
    target_price: float
    is_triggered: bool
    created_at: datetime


@router.get("", response_model=List[AlertResponse])
async def list_alerts(
    current_user: User = Depends(require_current_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(PriceAlert, ProductVariant, Product, MarketplaceListing)
        .join(ProductVariant, ProductVariant.id == PriceAlert.variant_id)
        .join(Product, Product.id == ProductVariant.product_id)
        .join(MarketplaceListing, MarketplaceListing.variant_id == ProductVariant.id)
        .where(PriceAlert.user_id == current_user.id)
        .order_by(PriceAlert.created_at.desc())
    )
    res = await db.execute(stmt)
    rows = res.all()

    seen_alerts = set()
    alerts = []
    for alert, v, p, l in rows:
        if alert.id in seen_alerts:
            continue
        seen_alerts.add(alert.id)

        alerts.append(
            AlertResponse(
                id=alert.id,
                variant_id=v.id,
                product_name=p.name,
                variant_name=v.name,
                image_url=p.default_image_url,
                current_price=float(l.current_price),
                target_price=float(alert.target_price),
                is_triggered=alert.is_triggered,
                created_at=alert.created_at,
            )
        )
    return alerts


@router.post("", response_model=AlertResponse, status_code=status.HTTP_201_CREATED)
async def create_alert(
    body: CreateAlertRequest,
    current_user: User = Depends(require_current_user),
    db: AsyncSession = Depends(get_db),
):
    # Verify variant
    stmt = (
        select(ProductVariant, Product, MarketplaceListing)
        .join(Product, Product.id == ProductVariant.product_id)
        .join(MarketplaceListing, MarketplaceListing.variant_id == ProductVariant.id)
        .where(ProductVariant.id == body.variant_id)
    )
    res = await db.execute(stmt)
    row = res.first()
    if not row:
        raise HTTPException(status_code=404, detail="Product variant not found")
    v, p, l = row

    alert = PriceAlert(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        variant_id=body.variant_id,
        target_price=body.target_price,
        is_active=True,
        is_triggered=float(l.current_price) <= body.target_price,
    )
    db.add(alert)
    await db.commit()

    return AlertResponse(
        id=alert.id,
        variant_id=v.id,
        product_name=p.name,
        variant_name=v.name,
        image_url=p.default_image_url,
        current_price=float(l.current_price),
        target_price=float(alert.target_price),
        is_triggered=alert.is_triggered,
        created_at=alert.created_at,
    )


@router.delete("/{alert_id}")
async def delete_alert(
    alert_id: str,
    current_user: User = Depends(require_current_user),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(PriceAlert).where(
        PriceAlert.id == alert_id,
        PriceAlert.user_id == current_user.id,
    )
    res = await db.execute(stmt)
    alert = res.scalar_one_or_none()
    if not alert:
        raise HTTPException(status_code=404, detail="Price alert not found")

    await db.delete(alert)
    await db.commit()
    return {"status": "SUCCESS", "message": "Price alert deleted"}
