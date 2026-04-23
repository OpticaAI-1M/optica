"""
FastAPI application entry point for Optica.
"""

from fastapi import FastAPI, Depends
from typing import Dict, Any

from app.core.config import get_settings
from app.api.deps import get_current_user

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)


@app.get("/health", tags=["Health"])
async def health_check(
    user: Dict[str, Any] = Depends(get_current_user),
) -> dict:
    """
    Protected health endpoint.
    Requires valid JWT token.
    """
    return {
        "status": "ok",
        "user": user.get("preferred_username"),
    }