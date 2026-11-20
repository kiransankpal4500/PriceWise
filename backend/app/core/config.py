import os
from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent


def resolve_database_urls():
    env_url = os.environ.get("DATABASE_URL")
    if env_url:
        sync_url = env_url.replace("+aiosqlite", "").replace("+asyncpg", "")
        return env_url, sync_url

    # Check locations in order of preference
    locations = [
        Path.cwd() / "pricewise.db",
        Path.cwd() / "backend" / "pricewise.db",
        BASE_DIR / "pricewise.db",
        Path("/tmp/pricewise.db"),
    ]
    for loc in locations:
        if loc.exists() and loc.is_file() and loc.stat().st_size > 0:
            try:
                # Test writability
                with open(loc, "a+b"):
                    pass
                p = loc.resolve().as_posix()
                return f"sqlite+aiosqlite:///{p}", f"sqlite:///{p}"
            except Exception:
                pass

    # If none writable, copy seed db to /tmp/pricewise.db
    tmp_path = Path("/tmp/pricewise.db")
    for src in [Path.cwd() / "pricewise.db", Path.cwd() / "backend" / "pricewise.db", BASE_DIR / "pricewise.db"]:
        if src.exists() and src.is_file() and src.stat().st_size > 0:
            try:
                import shutil
                shutil.copyfile(src, tmp_path)
                p = tmp_path.as_posix()
                return f"sqlite+aiosqlite:///{p}", f"sqlite:///{p}"
            except Exception:
                pass

    return "sqlite+aiosqlite:///pricewise.db", "sqlite:///pricewise.db"


_DEFAULT_DB_URL, _DEFAULT_SYNC_DB_URL = resolve_database_urls()


class Settings(BaseSettings):
    PROJECT_NAME: str = "PriceWise"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    # Database
    DATABASE_URL: str = _DEFAULT_DB_URL
    DATABASE_URL_SYNC: str = _DEFAULT_SYNC_DB_URL

    @field_validator("DATABASE_URL", mode="before")
    def fix_database_url(cls, v: str) -> str:
        if isinstance(v, str):
            if v.startswith("postgres://"):
                return v.replace("postgres://", "postgresql+asyncpg://", 1)
            elif v.startswith("postgresql://") and not v.startswith("postgresql+"):
                return v.replace("postgresql://", "postgresql+asyncpg://", 1)
        return v

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str):
            if v.strip() == "*":
                return ["*"]
            if not v.startswith("["):
                return [i.strip() for i in v.split(",") if i.strip()]
        return v

    # Security & JWT
    SECRET_KEY: str = "pricewise-super-secret-key-change-in-production-min32chars"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Google Gemini AI
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-3.5-flash-lite"

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "https://price-wise-azmu.vercel.app",
        "https://pricewise.vercel.app",
    ]

    # Marketplace Scraping / Integration
    QUICKCOMMERCE_API_KEY: str = "47861caa-b7aa-4d20-9ee3-9a2f1179eea3"
    MARKETPLACE_REQUEST_TIMEOUT: int = 15
    MARKETPLACE_RATE_LIMIT_DELAY: float = 2.0
    ENABLE_DEMO_DATA: bool = True

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
