import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.api import api_router
from app.workers.scheduler import start_scheduler, stop_scheduler

logging.basicConfig(level=logging.INFO if not settings.DEBUG else logging.DEBUG)
logger = logging.getLogger("pricewise")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing PriceWise platform...")
    # Auto-bootstrap database tables and catalog if empty
    try:
        from app.database.session import engine, Base, AsyncSessionLocal
        from app.models import Product
        from sqlalchemy import select, func
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            
        async with AsyncSessionLocal() as session:
            count = (await session.execute(select(func.count(Product.id)))).scalar() or 0
            if count == 0:
                logger.info("Database is empty. Automatically bootstrapping catalog data...")
                from app.database.init_db import seed_database
                await seed_database(force_refresh=False)
    except Exception as e:
        logger.warning(f"Database bootstrap notice: {e}")

    start_scheduler()
    yield
    logger.info("Shutting down PriceWise platform...")
    stop_scheduler()


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI-powered electronics price comparison and shopping intelligence platform.",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    docs_url=f"{settings.API_V1_PREFIX}/docs",
    redoc_url=f"{settings.API_V1_PREFIX}/redoc",
    lifespan=lifespan,
)

# Set up CORS
cors_origins = [str(o) for o in settings.BACKEND_CORS_ORIGINS]
if "*" in cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_origin_regex=r"https://.*\.vercel\.app",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include API v1 router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/", tags=["Root"])
async def root():
    return {
        "project": settings.PROJECT_NAME,
        "status": "OPERATIONAL",
        "version": "1.0.0",
        "docs_url": f"{settings.API_V1_PREFIX}/docs",
        "api_v1": settings.API_V1_PREFIX,
    }
