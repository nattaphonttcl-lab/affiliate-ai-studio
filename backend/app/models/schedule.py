import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.audit import AuditBaseModel

import enum


class ScheduleStatus(enum.Enum):
    pending = "pending"
    scheduled = "scheduled"
    published = "published"
    failed = "failed"


class Schedule(AuditBaseModel, Base):
    __tablename__ = "schedules"

    id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("contents.id"), nullable=False, index=True)
    channel_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("channels.id"), nullable=False, index=True)
    scheduled_for: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[ScheduleStatus] = mapped_column(Enum(ScheduleStatus), nullable=False, default=ScheduleStatus.pending)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now(), nullable=False)

    content: Mapped["Content"] = relationship("Content", back_populates="schedules")
    channel: Mapped["Channel"] = relationship("Channel")
