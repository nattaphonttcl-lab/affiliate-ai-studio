from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user import UserRepository
from app.utils.security import get_password_hash


class UserService:
    def __init__(self, repository: UserRepository | None = None):
        self.repository = repository or UserRepository()

    async def create_user(self, db: AsyncSession, email: str, password: str) -> User:
        hashed = get_password_hash(password)
        user = User(email=email, hashed_password=hashed)
        await self.repository.add(db, user)
        await db.commit()
        await db.refresh(user)
        return user

    async def get_by_email(self, db: AsyncSession, email: str) -> User | None:
        return await self.repository.get_by_email(db, email)
