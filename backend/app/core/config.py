from typing import List
from pydantic import AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"   # <-- สำคัญ
    )

    PROJECT_NAME: str = "Affiliate AI Studio - API"
    DEBUG: bool = False

    DATABASE_URL: AnyUrl

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    ALEMBIC_INI_LOCATION: str = "alembic.ini"
    CORS_ORIGINS: List[str] = ["*"]


settings = Settings()