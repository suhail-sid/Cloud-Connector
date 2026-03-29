"""
Configuration module for GitHub Connector
Handles environment variables and application settings
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    github_token: str
    github_api_base_url: str = "https://api.github.com"
    debug: bool = False
    log_level: str = "INFO"
    
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
