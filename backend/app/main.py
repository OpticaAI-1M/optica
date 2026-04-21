"""
FastAPI application entry point for Optica.
"""

from fastapi import FastAPI

from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)


@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    """
    Health endpoint used by Docker, monitoring,
    and startup verification.
    """
    return {"status": "ok"}