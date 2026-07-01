from pydantic_settings import BaseSettings
from typing import List
import json
from pydantic import field_validator

class Settings(BaseSettings):
    ENV: str = "development"
    SECRET_KEY: str
    DATABASE_URL: str
    REDIS_URL: str
    OPENAI_API_KEY: str
    USE_MOCK_EMBEDDINGS: bool = False
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: str = ""
    ENCRYPTION_KEY: str
    LINKEDIN_CLIENT_ID: str = ""
    LINKEDIN_CLIENT_SECRET: str = ""
    LINKEDIN_REDIRECT_URI: str = "http://localhost:8000/auth/linkedin/callback"
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_allowed_origins(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return [x.strip() for x in v.split(",") if x.strip()]
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
