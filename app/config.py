import os
from pathlib import Path
from functools import lru_cache
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


def _default_database_url() -> str:
    """Use /tmp on Vercel — project dir is read-only in serverless."""
    if os.environ.get("VERCEL") or os.environ.get("VERCEL_ENV"):
        return "sqlite:////tmp/panchaayat.db"
    return "sqlite:///./panchaayat.db"


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    app_name: str = "Panchaayat"
    secret_key: str = "panchaayat-dev-secret-change-in-production"
    database_url: str = Field(default_factory=_default_database_url)
    azure_openai_api_key: str = ""
    azure_openai_endpoint: str = ""
    azure_openai_deployment: str = "gpt-4o-mini"
    azure_openai_api_version: str = "2024-08-01-preview"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7

    class Config:
        env_file = ".env"

    @field_validator("database_url", mode="before")
    @classmethod
    def resolve_database_url(cls, value):
        if value is None or (isinstance(value, str) and not value.strip()):
            return _default_database_url()
        return value

    @field_validator("secret_key", mode="before")
    @classmethod
    def resolve_secret_key(cls, value):
        if value is None or (isinstance(value, str) and not value.strip()):
            return "panchaayat-dev-secret-change-in-production"
        return value

    @property
    def is_vercel(self) -> bool:
        return bool(os.environ.get("VERCEL") or os.environ.get("VERCEL_ENV"))

    @property
    def upload_dir(self) -> Path:
        if self.is_vercel:
            return Path("/tmp/panchaayat-uploads")
        return _project_root() / "uploads"

    @property
    def static_dir(self) -> Path:
        return _project_root() / "static" / "dist"


@lru_cache
def get_settings() -> Settings:
    return Settings()
