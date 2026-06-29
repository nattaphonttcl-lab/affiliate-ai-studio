import uuid
from datetime import datetime

from sqlalchemy import DateTime, Integer, String, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.audit import AuditBaseModel


class Analytics(AuditBaseModel, Base):
    __tablename__ = "analytics"

    id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    affiliate_link_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("affiliate_links.id"), nullable=False, index=True)
    clicks: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    conversions: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    source: Mapped[str | None] = mapped_column(String(255), nullable=True)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    affiliate_link: Mapped["AffiliateLink"] = relationship("AffiliateLink", back_populates="analytics")
