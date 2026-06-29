from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import configure_logging
from app.core.exceptions import register_exception_handlers
from app.api.v1 import router as api_v1_router


def create_app() -> FastAPI:
    configure_logging()

    app = FastAPI(title=settings.PROJECT_NAME)

    # CORS
    origins = settings.CORS_ORIGINS or ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register global exception handlers
    register_exception_handlers(app)

    # API versioned router: mounted at /api/v1
    app.include_router(api_v1_router, prefix="/api")

    @app.get("/health", tags=["health"])
    async def health_root() -> dict:
        return {"status": "ok"}

    return app


app = create_app()
