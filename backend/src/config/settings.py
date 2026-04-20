"""Application configuration and settings."""
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    DATABASE_URL: str = "postgresql://ugm_schedule:password@localhost:5432/ugm_schedule"
    DATABASE_ECHO: bool = False

    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_V1_PREFIX: str = "/api/v1"

    # Logging
    LOG_LEVEL: str = "INFO"

    # CORS
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    # TopScore API Integration
    TOPSCORE_BASE_URL: str = "https://aum.usetopscore.com"
    TOPSCORE_CLIENT_ID: str = ""
    TOPSCORE_CLIENT_SECRET: str = ""
    TOPSCORE_CSRF_TOKEN: str = ""

    # Scraper/Sync
    SCRAPER_USER_AGENT: str = "UGMScheduleScraper/1.0"
    SCRAPER_TIMEOUT: int = 30
    SCRAPER_SCHEDULE_TIME: str = "02:00"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


# Global settings instance
settings = Settings()
