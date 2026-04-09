import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from src.domain.exceptions import AppError


logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError):
        logger.warning(
            "AppError on %s %s: %s", request.method, request.url.path, exc.message
        )
        return JSONResponse(
            status_code=exc.code,
            content={
                "code": exc.__class__.__name__,
                "message": exc.message,
                "details": exc.details,
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_handler(request: Request, exc: RequestValidationError):
        logger.info("Validation error on %s %s", request.method, request.url.path)
        return JSONResponse(
            status_code=422,
            content={
                "code": "ValidationError",
                "message": "Request validation failed",
                "details": {"errors": exc.errors()},
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_handler(request: Request, exc: Exception):
        logger.exception("Unhandled error on %s %s", request.method, request.url.path)
        return JSONResponse(
            status_code=500,
            content={
                "code": "InternalServerError",
                "message": "Internal server error",
                "details": {},
            },
        )
