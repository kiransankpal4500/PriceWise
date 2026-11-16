from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.database.session import get_db
from app.integrations.registry import integration_registry
from app.ai.gemini_client import gemini_client

router = APIRouter()


@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    db_status = "HEALTHY"
    try:
        await db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"UNHEALTHY: {str(e)}"

    return {
        "status": "UP",
        "service": "PriceWise Backend API",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "database": db_status,
        "ai_engine": {
            "status": "AVAILABLE" if gemini_client.is_available else "OFFLINE",
            "model": gemini_client.model_name,
        },
    }


@router.get("/health/providers")
async def provider_health():
    providers = integration_registry.list_providers()
    return {
        "total_providers": len(providers),
        "providers": [p.model_dump() for p in providers],
    }
