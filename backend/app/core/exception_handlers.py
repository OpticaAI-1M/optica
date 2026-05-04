"""
Global exception handlers.
"""

from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    AppException,
    ValidationException,
    NotFoundException,
    ConflictException,
)


def app_exception_handler(request: Request, exc: AppException):
    """
    Handle base application exceptions.
    """
    return JSONResponse(
        status_code=400,
        content={
            "error": "APPLICATION_ERROR",
            "message": exc.message,
        },
    )


def validation_exception_handler(request: Request, exc: ValidationException):
    """
    Handle validation exceptions.
    """
    return JSONResponse(
        status_code=400,
        content={
            "error": "VALIDATION_ERROR",
            "message": exc.message,
        },
    )


def not_found_exception_handler(request: Request, exc: NotFoundException):
    """
    Handle not found exceptions.
    """
    return JSONResponse(
        status_code=404,
        content={
            "error": "NOT_FOUND",
            "message": exc.message,
        },
    )


def conflict_exception_handler(request: Request, exc: ConflictException):
    """
    Handle conflict exceptions.
    """
    return JSONResponse(
        status_code=409,
        content={
            "error": "CONFLICT",
            "message": exc.message,
        },
    )