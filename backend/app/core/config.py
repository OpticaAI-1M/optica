"""
Application configuration module.

Uses pydantic-settings so all runtime configuration
comes from environment variables and can later be
overridden via .env, Docker, or CI/CD secrets.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralized application settings."""

    app_name: str = "Optica API"
    app_version: str = "0.1.0"
    environment: str = "development"

    postgres_db: str = "optica"
    postgres_user: str = "optica"
    postgres_password: str = "optica"

    keycloak_admin: str = "admin"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Return a cached Settings instance.

    lru_cache ensures the settings object is created
    only once during the application lifecycle.
    """
    return Settings()