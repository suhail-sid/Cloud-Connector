"""
Configuration module for GitHub Connector
Handles environment variables and application settings
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Basic settings
    debug: bool = False
    log_level: str = "INFO"
    github_api_base_url: str = "https://api.github.com"
    
    # PAT Authentication (optional, for backward compatibility)
    github_token: Optional[str] = None
    
    # OAuth 2.0 settings
    oauth_enabled: bool = False
    oauth_client_id: Optional[str] = None
    oauth_client_secret: Optional[str] = None
    oauth_redirect_uri: Optional[str] = None
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance
    Returns cached settings to avoid reloading environment variables
    """
    return Settings()
