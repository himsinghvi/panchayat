from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "Panchaayat"
    secret_key: str = "panchaayat-dev-secret-change-in-production"
    database_url: str = "sqlite:///./panchaayat.db"
    azure_openai_api_key: str = ""
    azure_openai_endpoint: str = ""
    azure_openai_deployment: str = "gpt-4o-mini"
    azure_openai_api_version: str = "2024-08-01-preview"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
