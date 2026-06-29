from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: UUID
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class UserUpdate(BaseModel):
    password: Optional[str] = None
    is_active: Optional[bool] = None