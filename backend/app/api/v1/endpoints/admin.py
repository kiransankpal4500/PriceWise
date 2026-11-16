from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.session import get_db
from app.models.tracking import ApiSyncLog
from app.workers.scheduler import sync_marketplace_prices_job

router = APIRouter()


@router.post("/sync-prices")
async def trigger_price_sync():
    """Manually trigger immediate marketplace price sync across the entire catalog."""
    await sync_marketplace_prices_job()
    return {
        "status": "COMPLETED",
        "message": "Marketplace prices synchronized successfully and alerts evaluated.",
    }


@router.get("/sync-logs")
async def get_sync_logs(db: AsyncSession = Depends(get_db)):
    """Retrieve recent automated sync execution logs."""
    stmt = select(ApiSyncLog).order_by(ApiSyncLog.executed_at.desc()).limit(20)
    res = await db.execute(stmt)
    logs = res.scalars().all()
    return [
        {
            "id": log.id,
            "provider_name": log.provider_name,
            "status": log.status,
            "items_fetched": log.items_fetched,
            "error_message": log.error_message,
            "executed_at": log.executed_at.isoformat(),
        }
        for log in logs
    ]
