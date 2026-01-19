from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    
    # JWT
    JWT_ACCESS_SECRET: str
    JWT_REFRESH_SECRET: str
    JWT_ACCESS_EXPIRY: int = 15  # minutes
    JWT_REFRESH_EXPIRY: int = 10080  # 7 days in minutes
    JWT_ALGORITHM: str = "HS256"
    
    # Server
    PORT: int = 5000
    DEBUG: bool = True
    
    # CORS
    CORS_ORIGIN: str = "http://localhost:3000"
    
    # Email
    EMAIL_FROM: str = "noreply@cohortly.com"
    EMAIL_ENABLED: bool = False
    SENDGRID_API_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
