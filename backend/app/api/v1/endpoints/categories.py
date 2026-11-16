from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database.session import get_db
from app.models.catalog import Category, Product
from app.schemas.products import CategorySchema

router = APIRouter()


@router.get("", response_model=List[CategorySchema])
async def list_categories(db: AsyncSession = Depends(get_db)):
    # Count products per category
    stmt = (
        select(Category, func.count(Product.id).label("product_count"))
        .outerjoin(Product, Product.category_id == Category.id)
        .group_by(Category.id)
        .order_by(Category.name.asc())
    )
    res = await db.execute(stmt)
    rows = res.all()

    items = []
    for cat, count in rows:
        items.append(
            CategorySchema(
                id=cat.id,
                name=cat.name,
                slug=cat.slug,
                description=cat.description,
                icon_name=cat.icon_name,
                product_count=count,
            )
        )
    return items
