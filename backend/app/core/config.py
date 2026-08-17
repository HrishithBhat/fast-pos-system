from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    app_name: str = Field(default="POS Backend")
    secret_key: str = Field(default="change-me")
    access_token_expire_minutes: int = Field(default=60 * 24)
    # Default to SQLite for local dev convenience; override to Postgres in prod
    database_url: str = Field(default="sqlite+aiosqlite:///./pos.db")
    # CORS
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000", "http://127.0.0.1:3000"]) 

settings = Settings()
