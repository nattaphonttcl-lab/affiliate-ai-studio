import uuid
from datetime import datetime
from typing import List

from sqlalchemy import DateTime, String, Text, Boolean, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.audit import AuditBaseModel


class AffiliateLink(AuditBaseModel, Base):
    __tablename__ = "affiliate_links"

    id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    url: Mapped[str] = mapped_column(String(2048), nullable=False)
    tracking_code: Mapped[str] = mapped_column(String(128), nullable=False, unique=True, index=True)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    product_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("products.id"), nullable=False, index=True)
    creator_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now(), nullable=False)

    product: Mapped["Product"] = relationship("Product", back_populates="affiliate_links")
    creator: Mapped["User"] = relationship("User", back_populates="affiliate_links")
    analytics: Mapped[List["Analytics"]] = relationship("Analytics", back_populates="affiliate_link")
