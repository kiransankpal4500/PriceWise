from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    email: str
    full_name: Optional[str] = None


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: Optional[int] = None
    type: Optional[str] = None


class UserPreferenceUpdate(BaseModel):
    default_budget: Optional[float] = None
    preferred_brands: Optional[List[str]] = None
    preferred_categories: Optional[List[str]] = None
    priority_weights: Optional[Dict[str, float]] = None


class UserPreferenceResponse(BaseModel):
    default_budget: Optional[float] = None
    preferred_brands: List[str] = []
    preferred_categories: List[str] = []
    priority_weights: Dict[str, float] = {}

    model_config = {"from_attributes": True}


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: Optional[str] = None
    is_active: bool
    is_admin: bool
    created_at: datetime
    preferences: Optional[UserPreferenceResponse] = None

    model_config = {"from_attributes": True}
