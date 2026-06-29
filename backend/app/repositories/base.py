from typing import Generic, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    async def add(self, db: AsyncSession, obj: T) -> T:
        db.add(obj)
        await db.flush()
        return obj

    async def get(self, db: AsyncSession, id):
        q = select(self.model).where(self.model.id == id)
        res = await db.execute(q)
        return res.scalar_one_or_none()

    async def list(self, db: AsyncSession, offset: int = 0, limit: int = 100):
        q = select(self.model).offset(offset).limit(limit)
        res = await db.execute(q)
        return res.scalars().all()

    async def delete(self, db: AsyncSession, obj: T) -> None:
        await db.delete(obj)
        await db.flush()
