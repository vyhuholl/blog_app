"""
Configuration management for the blog application.

Uses Pydantic Settings for environment variable loading and validation.
"""

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    database_url: str = Field(default="sqlite://./blog.db", env="DATABASE_URL")

    # JWT Configuration
    jwt_secret: str = Field(..., env="JWT_SECRET")
    jwt_algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    jwt_expire_minutes: int = Field(default=1440, env="JWT_EXPIRE_MINUTES")

    # Password Hashing
    bcrypt_rounds: int = Field(default=12, env="BCRYPT_ROUNDS")

    # Environment
    environment: str = Field(default="development", env="ENVIRONMENT")

    # Server
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")

    class Config:
        """Pydantic configuration."""

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()

