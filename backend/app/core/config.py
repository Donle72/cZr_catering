"""
Application configuration using Pydantic Settings
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import List, Union
import os
import secrets


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """
    # Project
    PROJECT_NAME: str = "cZr Catering System"
    VERSION: str = "0.3.0"  # Updated: Tags system, Unit display refactor, Proposals
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    
    # Database - REQUIRED from .env
    DATABASE_URL: str
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Security - REQUIRED from .env
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: Union[List[str], str] = "http://localhost:3020,http://localhost:5173"
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    UPLOAD_DIR: str = "./uploads"
    
    # Timezone
    TIMEZONE: str = "America/Argentina/Buenos_Aires"
    
    @field_validator('CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        """Parse CORS_ORIGINS from string or list"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v
    
    @field_validator('SECRET_KEY')
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        """Validate SECRET_KEY is secure"""
        if v == "your-super-secret-key-change-this-in-production":
            raise ValueError(
                "⚠️  SECURITY ERROR: SECRET_KEY must be set in .env file! "
                "Generate one with: python -c 'import secrets; print(secrets.token_urlsafe(32))'"
            )
        if len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long")
        return v
    
    @field_validator('DATABASE_URL')
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Validate DATABASE_URL is set"""
        if not v or v == "":
            raise ValueError("DATABASE_URL must be set in .env file")
        return v
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra='ignore'
    )


# Create settings instance
settings = Settings()

