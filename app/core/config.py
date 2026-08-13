from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    PROJECT_NAME: str = "FastAPI Template Application"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database Settings
    # Defaulting to an async SQLite URL, but easily configurable via env variables
    DATABASE_URL: str = "sqlite+aiosqlite:///./sql_app.db"
    
    # Security Settings
    SECRET_KEY: str = "change_me_in_production_extremely_secret_key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


@lru_cache
def get_settings() -> Settings:
    """Get cached settings object."""
    return Settings()
