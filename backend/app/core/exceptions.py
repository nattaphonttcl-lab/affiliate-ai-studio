from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.logging import logger


class AppException(Exception):
    def __init__(self, status_code: int = 400, detail: str = "Bad request"):
        self.status_code = status_code
        self.detail = detail


async def app_exception_handler(request: Request, exc: AppException):
    logger.warning("app_exception", path=request.url.path, detail=exc.detail)
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.warning("http_exception", path=request.url.path, status_code=exc.status_code, detail=str(exc.detail))
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.info("validation_error", path=request.url.path, errors=exc.errors())
    return JSONResponse({"detail": exc.errors()}, status_code=422)


async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception("unhandled_exception", path=request.url.path, error=str(exc))
    return JSONResponse({"detail": "Internal server error"}, status_code=500)


def register_exception_handlers(app):
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
