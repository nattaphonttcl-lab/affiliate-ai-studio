import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column


class AuditBaseModel:
    """Mixin providing common audit fields.

    Fields:
    - created_at: timezone-aware creation timestamp
    - updated_at: timezone-aware last update timestamp
    - deleted_at: soft-delete timestamp
    - created_by: FK to `users.id` for creator
    - updated_by: FK to `users.id` for last modifier
    """

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), server_onupdate=func.now(), nullable=False)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True, index=True)

    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True)
    updated_by: Mapped[Optional[uuid.UUID]] = mapped_column(PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True)
