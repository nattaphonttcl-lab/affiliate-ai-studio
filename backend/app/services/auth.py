from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.user import UserService
from app.utils.security import verify_password, create_access_token


class AuthService:
    def __init__(self, user_service: UserService | None = None):
        self.user_service = user_service or UserService()

    async def authenticate(self, db: AsyncSession, email: str, password: str):
        user = await self.user_service.get_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def create_token(self, user_id: str) -> str:
        return create_access_token(subject=user_id, expires_delta=timedelta(minutes=60))
