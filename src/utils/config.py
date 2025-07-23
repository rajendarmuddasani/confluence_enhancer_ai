"""
Configuration management for Confluence Enhancer
"""
import os
from typing import Optional, List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application Settings
    APP_NAME: str = "Confluence Content Intelligence & Enhancement System"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    ENVIRONMENT: str = "development"
    
    # Database Settings
    ORACLE_HOST: str = "localhost"
    ORACLE_PORT: int = 1521
    ORACLE_SERVICE: str = "XE"
    ORACLE_USER: str = "confluence_user"
    ORACLE_PASSWORD: str = ""
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    
    @property
    def oracle_dsn(self) -> str:
        return f"{self.ORACLE_USER}/{self.ORACLE_PASSWORD}@{self.ORACLE_HOST}:{self.ORACLE_PORT}/{self.ORACLE_SERVICE}"
    
    # AI/ML Settings
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4"
    OPENAI_MAX_TOKENS: int = 4000
    OPENAI_TEMPERATURE: float = 0.3
    
    ANTHROPIC_API_KEY: str = ""
    ANTHROPIC_MODEL: str = "claude-3-sonnet-20240229"
    
    # Confluence API Settings
    CONFLUENCE_BASE_URL: str = ""
    CONFLUENCE_USERNAME: str = ""
    CONFLUENCE_API_TOKEN: str = ""
    
    # OAuth 2.0 Settings
    CONFLUENCE_CLIENT_ID: str = ""
    CONFLUENCE_CLIENT_SECRET: str = ""
    CONFLUENCE_REDIRECT_URI: str = "http://localhost:8000/auth/callback"
    
    # Security Settings
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS Settings
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:5173"
    ALLOWED_METHODS: str = "GET,POST,PUT,DELETE,OPTIONS"
    ALLOWED_HEADERS: str = "*"
    
    # Processing Settings
    MAX_CONTENT_SIZE: int = 10 * 1024 * 1024  # 10MB
    MAX_PROCESSING_TIME: int = 300  # 5 minutes
    CHUNK_SIZE: int = 4000  # For AI processing
    MAX_CONCURRENT_REQUESTS: int = 10
    
    # Visualization Settings
    MAX_CHART_DATA_POINTS: int = 10000
    DEFAULT_CHART_HEIGHT: int = 400
    DEFAULT_CHART_WIDTH: int = 600
    CHART_CACHE_TTL: int = 3600
    
    # Caching Settings
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_PASSWORD: str = ""
    REDIS_DB: int = 0
    CACHE_TTL: int = 3600
    
    # Logging Settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    LOG_FILE: str = "logs/confluence_enhancer.log"
    
    # Storage Settings
    STORAGE_TYPE: str = "local"
    STORAGE_PATH: str = "./storage"
    
    # Health Check Settings
    HEALTH_CHECK_INTERVAL: int = 30
    HEALTH_CHECK_TIMEOUT: int = 5
    
    # Metrics Settings
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
