from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "CyberPsyche"
    API_V1_STR: str = "/api/v1"
    
    # Security Secrets
    SECRET_KEY: str = "SUPER_SECRET_KEY_CHANGE_IN_PRODUCTION_CYBERPSYCHE_2026"
    CSRF_SECRET: str = "SUPER_CSRF_SECRET_CHANGE_IN_PRODUCTION_CYBERPSYCHE_2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # Database
    DATABASE_URL: str = "sqlite:///./cyberpsyche_dev.db"  # Defaults to local SQLite for testing; overridden by env for PostgreSQL
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # Session Constraints
    BASELINE_SCENARIO_COUNT: int = 6
    RETEST_SCENARIO_COUNT: int = 6
    TRANSFER_SCENARIO_COUNT: int = 6
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()
