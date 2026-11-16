from fastapi import APIRouter
from app.api.v1.endpoints import (
    health,
    auth,
    categories,
    products,
    search,
    compare,
    recommendations,
    prices,
    watchlist,
    alerts,
    assistant,
)

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(categories.router, prefix="/categories", tags=["Categories"])
api_router.include_router(products.router, prefix="/products", tags=["Products"])
api_router.include_router(search.router, prefix="/search", tags=["Search"])
api_router.include_router(compare.router, prefix="/compare", tags=["Comparison"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["Recommendations"])
api_router.include_router(prices.router, prefix="/products", tags=["Price Intelligence"])
api_router.include_router(watchlist.router, prefix="/watchlist", tags=["Watchlist"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["Price Alerts"])
api_router.include_router(assistant.router, prefix="/assistant", tags=["AI Shopping Assistant"])
