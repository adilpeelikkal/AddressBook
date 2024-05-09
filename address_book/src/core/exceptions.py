import logging
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import (
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from src.core.config import configure_logging

configure_logging(logger_level=logging.ERROR)

logger = logging.getLogger(__name__)


def form_error_message(errors: List[dict]) -> List[str]:
    """
    Make valid pydantic `ValidationError` messages list.
    """
    messages = []
    for error in errors:
        field, message = error["loc"][-1], error["msg"]
        messages.append({"field": field, "error": message})
    return messages


class BaseInternalException(Exception):
    """
    Base error class for inherit all internal errors.
    """

    def __init__(self, message: str, status_code: int) -> None:
        self.message = message
        self.status_code = status_code


class ObjectNotFoundException(BaseInternalException):
    """
    Exception raised when `address_id` field from JSON body not found.
    """


class DuplicateException(BaseInternalException):
    """
    Exception raised when creating a duplicate object.
    """


def add_internal_exception_handler(app: FastAPI) -> None:
    """
    Handle all internal exceptions.
    """

    @app.exception_handler(BaseInternalException)
    async def _exception_handler(
        _: Request, exc: BaseInternalException
    ) -> JSONResponse:
        logger.error(f"Internal Exception: {exc.message}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "status": exc.status_code,
                "type": type(exc).__name__,
                "message": exc.message,
            },
        )


def add_validation_exception_handler(app: FastAPI) -> None:
    """
    Handle `pydantic` validation errors exceptions.
    """

    @app.exception_handler(ValidationError)
    async def _exception_handler(_: Request, exc: ValidationError) -> JSONResponse:
        logger.error(f"Validation Error: {exc.errors()}")
        return JSONResponse(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "status": HTTP_422_UNPROCESSABLE_ENTITY,
                "type": "ValidationError",
                "message": "Schema validation error",
                "errors": form_error_message(errors=exc.errors()),
            },
        )


def add_request_exception_handler(app: FastAPI) -> None:
    """
    Handle request validation errors exceptions.
    """

    @app.exception_handler(RequestValidationError)
    async def _exception_handler(
        _: Request, exc: RequestValidationError
    ) -> JSONResponse:
        logger.error(f"Request Validation Error: {exc.errors()}")
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "status": HTTP_422_UNPROCESSABLE_ENTITY,
                "type": "RequestValidationError",
                "message": "Schema validation error",
                "errors": form_error_message(errors=exc.errors()),
            },
        )


def add_http_exception_handler(app: FastAPI) -> None:
    """
    Handle http exceptions.
    """

    @app.exception_handler(HTTPException)
    async def _exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
        logger.error(f"HTTP Exception: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "status": exc.status_code,
                "type": "HTTPException",
                "message": exc.detail,
            },
        )


def add_internal_server_error_handler(app: FastAPI) -> None:
    """
    Handle http exceptions.
    """

    @app.exception_handler(Exception)
    async def _exception_handler(_: Request, exc: Exception) -> JSONResponse:
        logger.error(f"Internal Server Error: {exc}")
        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "status": HTTP_500_INTERNAL_SERVER_ERROR,
                "type": "HTTPException",
                "message": "Internal Server Error",
            },
        )


def add_exceptions_handlers(app: FastAPI) -> None:
    """
    Base exception handlers.
    """
    add_internal_exception_handler(app=app)
    add_validation_exception_handler(app=app)
    add_request_exception_handler(app=app)
    add_http_exception_handler(app=app)
    add_internal_server_error_handler(app=app)
