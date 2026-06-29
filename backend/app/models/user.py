import uuid
from datetime import datetime
from typing import List

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.audit import AuditBaseModel


class User(AuditBaseModel, Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(256), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now(), nullable=False)

    # relationships
    channels: Mapped[List["Channel"]] = relationship("Channel", back_populates="owner", cascade="all, delete-orphan")
    products: Mapped[List["Product"]] = relationship("Product", back_populates="seller")
    affiliate_links: Mapped[List["AffiliateLink"]] = relationship("AffiliateLink", back_populates="creator")
    contents: Mapped[List["Content"]] = relationship("Content", back_populates="author")
