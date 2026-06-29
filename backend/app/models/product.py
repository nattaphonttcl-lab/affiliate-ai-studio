import uuid
from datetime import datetime
from typing import List

from sqlalchemy import DateTime, String, Text, Numeric, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.audit import AuditBaseModel


class Product(AuditBaseModel, Base):
    __tablename__ = "products"

    id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    seller_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    category_id: Mapped[uuid.UUID | None] = mapped_column(PGUUID(as_uuid=True), ForeignKey("categories.id"), nullable=True, index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now(), nullable=False)

    seller: Mapped["User"] = relationship("User", back_populates="products")
    category: Mapped["Category" | None] = relationship("Category", back_populates="products")
    affiliate_links: Mapped[List["AffiliateLink"]] = relationship("AffiliateLink", back_populates="product")
