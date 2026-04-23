"""
FastAPI application entry point for Optica.
"""

from fastapi import FastAPI, Depends
from typing import Dict, Any

from app.core.config import get_settings
from app.api.deps import get_current_user, require_roles

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)


@app.get("/health", tags=["Health"])
async def health_check(
    user: Dict[str, Any] = Depends(require_roles(["support_engineer"])),
) -> dict:
    """
    Protected health endpoint with RBAC.
    Only support_engineer role allowed.
    """
    return {
        "status": "ok",
        "user": user.get("preferred_username"),
    }