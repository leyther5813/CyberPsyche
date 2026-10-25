
from typing import List

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "CyberPsyche"
    API_V1_STR: str = "/api/v1"

    # Set ENVIRONMENT=production in a deployed environment.
    ENVIRONMENT: str = "development"

    # Development-only defaults. Configure unique secrets in production.
    SECRET_KEY: str = "SUPER_SECRET_KEY_CHANGE_IN_PRODUCTION_CYBERPSYCHE_2026"
    CSRF_SECRET: str = "SUPER_CSRF_SECRET_CHANGE_IN_PRODUCTION_CYBERPSYCHE_2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # Database
    DATABASE_URL: str = "sqlite:///./cyberpsyche_dev.db"

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    # Session Constraints
    BASELINE_SCENARIO_COUNT: int = 6
    RETEST_SCENARIO_COUNT: int = 6
    TRANSFER_SCENARIO_COUNT: int = 6

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )

    @model_validator(mode="after")
    def validate_production_secrets(self):
        if self.ENVIRONMENT.lower() == "production":
            placeholder_secrets = {
                "SUPER_SECRET_KEY_CHANGE_IN_PRODUCTION_CYBERPSYCHE_2026",
                "SUPER_CSRF_SECRET_CHANGE_IN_PRODUCTION_CYBERPSYCHE_2026",
            }

            if (
                self.SECRET_KEY in placeholder_secrets
                or self.CSRF_SECRET in placeholder_secrets
            ):
                raise ValueError(
                    "Production requires unique SECRET_KEY and CSRF_SECRET values."
                )

            if len(self.SECRET_KEY) < 32 or len(self.CSRF_SECRET) < 32:
                raise ValueError(
                    "Production SECRET_KEY and CSRF_SECRET must each be at least 32 characters."
                )

        return self


settings = Settings()
