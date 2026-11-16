import uuid
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import String, Text, Numeric, Float, Integer, Boolean, ForeignKey, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.session import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Marketplace(Base):
    __tablename__ = "marketplaces"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    base_url: Mapped[str] = mapped_column(String(255), nullable=False)
    logo_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    listings: Mapped[List["MarketplaceListing"]] = relationship("MarketplaceListing", back_populates="marketplace")


class MarketplaceListing(Base):
    __tablename__ = "marketplace_listings"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    variant_id: Mapped[str] = mapped_column(String(36), ForeignKey("product_variants.id", ondelete="CASCADE"), nullable=False, index=True)
    marketplace_id: Mapped[str] = mapped_column(String(36), ForeignKey("marketplaces.id"), nullable=False, index=True)
    external_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True)  # e.g. ASIN or Flipkart FSN
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    product_url: Mapped[str] = mapped_column(String(1000), nullable=False)
    image_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    current_price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, index=True)
    original_mrp: Mapped[Optional[float]] = mapped_column(Numeric(12, 2), nullable=True)
    availability: Mapped[str] = mapped_column(String(50), default="IN_STOCK", nullable=False)  # IN_STOCK, OUT_OF_STOCK
    seller_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    rating: Mapped[Optional[float]] = mapped_column(Float, default=0.0)
    review_count: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    is_demo: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    last_scraped_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_utc_now)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_utc_now, onupdate=get_utc_now)

    variant: Mapped["ProductVariant"] = relationship("ProductVariant", back_populates="listings")
    marketplace: Mapped["Marketplace"] = relationship("Marketplace", back_populates="listings")
    price_history: Mapped[List["PriceHistory"]] = relationship("PriceHistory", back_populates="listing", cascade="all, delete-orphan")
    reviews: Mapped[List["Review"]] = relationship("Review", back_populates="listing", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_listing_mp_ext", "marketplace_id", "external_id", unique=True),
    )


class PriceHistory(Base):
    __tablename__ = "price_history"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    listing_id: Mapped[str] = mapped_column(String(36), ForeignKey("marketplace_listings.id", ondelete="CASCADE"), nullable=False, index=True)
    price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="INR", nullable=False)
    availability: Mapped[str] = mapped_column(String(50), default="IN_STOCK", nullable=False)
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_utc_now, index=True)
    source: Mapped[str] = mapped_column(String(50), default="SYNC_JOB", nullable=False)

    listing: Mapped["MarketplaceListing"] = relationship("MarketplaceListing", back_populates="price_history")

    __table_args__ = (
        Index("idx_price_history_listing_date", "listing_id", "observed_at"),
    )


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    listing_id: Mapped[str] = mapped_column(String(36), ForeignKey("marketplace_listings.id", ondelete="CASCADE"), nullable=False, index=True)
    author_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    headline: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    review_text: Mapped[str] = mapped_column(Text, nullable=False)
    is_verified_purchase: Mapped[bool] = mapped_column(Boolean, default=True)
    review_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    sentiment: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # POSITIVE, NEUTRAL, NEGATIVE
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_utc_now)

    listing: Mapped["MarketplaceListing"] = relationship("MarketplaceListing", back_populates="reviews")
