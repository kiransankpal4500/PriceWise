import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.session import get_db
from app.models.users import User, UserPreference
from app.core.security import verify_password, get_password_hash, create_access_token
from app.schemas.auth import (
    UserCreate,
    UserLogin,
    Token,
    UserResponse,
    UserPreferenceUpdate,
    UserPreferenceResponse,
)
from app.api.deps import require_current_user

router = APIRouter()


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    # Check if user already exists
    res = await db.execute(select(User).where(User.email == user_in.email))
    if res.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists",
        )

    user = User(
        id=str(uuid.uuid4()),
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        is_active=True,
    )
    db.add(user)
    await db.flush()

    # Create default preference
    pref = UserPreference(
        id=str(uuid.uuid4()),
        user_id=user.id,
        default_budget=50000.0,
        preferred_brands=[],
        preferred_categories=[],
        priority_weights={"price": 0.35, "specs": 0.30, "rating": 0.20, "reviews": 0.10, "value": 0.05},
    )
    db.add(pref)
    await db.commit()

    token = create_access_token(subject=user.id)
    return Token(
        access_token=token,
        token_type="bearer",
        user_id=user.id,
        email=user.email,
        full_name=user.full_name,
    )


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(User).where(User.email == credentials.email))
    user = res.scalar_one_or_none()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive",
        )

    token = create_access_token(subject=user.id)
    return Token(
        access_token=token,
        token_type="bearer",
        user_id=user.id,
        email=user.email,
        full_name=user.full_name,
    )


@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: User = Depends(require_current_user),
    db: AsyncSession = Depends(get_db),
):
    res = await db.execute(select(UserPreference).where(UserPreference.user_id == current_user.id))
    pref = res.scalar_one_or_none()

    pref_resp = None
    if pref:
        pref_resp = UserPreferenceResponse(
            default_budget=float(pref.default_budget) if pref.default_budget else None,
            preferred_brands=pref.preferred_brands or [],
            preferred_categories=pref.preferred_categories or [],
            priority_weights=pref.priority_weights or {},
        )

    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
        is_admin=current_user.is_admin,
        created_at=current_user.created_at,
        preferences=pref_resp,
    )
