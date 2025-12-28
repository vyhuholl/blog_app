"""
Configuration management for the blog application.

Uses Pydantic Settings for environment variable loading and validation.
"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    database_url: str = Field(default="sqlite://./blog.db")

    # JWT Configuration
    jwt_secret: str
    jwt_algorithm: str = Field(default="HS256")
    jwt_expire_minutes: int = Field(default=1440)

    # Password Hashing
    bcrypt_rounds: int = Field(default=12)

    # Environment
    environment: str = Field(default="development")

    # Server
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False
    )


# Global settings instance
settings = Settings()

