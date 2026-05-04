"""
FastAPI application entry point for Optica.
"""

from fastapi import FastAPI, Depends
from typing import Dict, Any

from app.core.config import get_settings
from app.api.deps import get_current_user, require_roles
from app.api.routes.incident_router import router as incident_router

from app.core.exceptions import (
    AppException,
    ValidationException,
    NotFoundException,
    ConflictException,
)

from app.core.exception_handlers import (
    app_exception_handler,
    validation_exception_handler,
    not_found_exception_handler,
    conflict_exception_handler,
)

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.include_router(incident_router)

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(ValidationException, validation_exception_handler)
app.add_exception_handler(NotFoundException, not_found_exception_handler)
app.add_exception_handler(ConflictException, conflict_exception_handler)


@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    """
    Health endpoint used by Docker, monitoring,
    and startup verification.
    """
    return {"status": "ok"}