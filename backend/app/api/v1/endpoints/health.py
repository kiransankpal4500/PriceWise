from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.config import settings
from app.database.session import get_db
from app.integrations.registry import integration_registry
from app.ai.gemini_client import gemini_client

router = APIRouter()


@router.get("/health")
async def health_check():
    from app.database.session import AsyncSessionLocal
    from app.models import Product
    from sqlalchemy import select, func
    import os
    from pathlib import Path

    db_status = "HEALTHY"
    product_count = 0
    try:
        async with AsyncSessionLocal() as session:
            res = await session.execute(select(func.count(Product.id)))
            product_count = res.scalar() or 0
    except Exception as e:
        db_status = f"UNHEALTHY: {str(e)}"

    return {
        "status": "UP",
        "service": "PriceWise Backend API",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "database": db_status,
        "product_count": product_count,
        "database_url": settings.DATABASE_URL,
        "cwd": os.getcwd(),
        "root_db_exists": Path("pricewise.db").exists(),
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
