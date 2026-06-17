from functools import lru_cache
import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel, Field


Role = Literal["admin", "medico", "farmaceutico", "recepcao"]
DataBackend = Literal["json", "supabase"]


class Settings(BaseModel):
    data_backend: DataBackend = Field(default="json", alias="DATA_BACKEND")
    local_data_path: str = Field(default="backend/data/local_db.json", alias="LOCAL_DATA_PATH")
    local_storage_path: str = Field(default="backend/data/storage", alias="LOCAL_STORAGE_PATH")
    supabase_url: str | None = Field(default=None, alias="SUPABASE_URL")
    supabase_key: str | None = Field(default=None, alias="SUPABASE_KEY")
    secret_key: str | None = Field(default=None, alias="SECRET_KEY")
    algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    access_token_expires_hours: int = Field(default=8, alias="ACCESS_TOKEN_EXPIRES_HOURS")
    clinical_attachments_bucket: str = Field(
        default="clinical-attachments",
        alias="CLINICAL_ATTACHMENTS_BUCKET",
    )
    attachment_signed_url_expires_seconds: int = Field(
        default=3600,
        alias="ATTACHMENT_SIGNED_URL_EXPIRES_SECONDS",
    )
    max_attachment_size_mb: int = Field(default=10, alias="MAX_ATTACHMENT_SIZE_MB")
    frontend_origins: str = Field(
        default=(
            "http://127.0.0.1:5173,http://localhost:5173,"
            "http://127.0.0.1:5174,http://localhost:5174"
        ),
        alias="FRONTEND_ORIGINS",
    )

    @property
    def missing_supabase_settings(self) -> list[str]:
        if self.data_backend == "json":
            return []
        missing = []
        if not self.supabase_url:
            missing.append("SUPABASE_URL")
        if not self.supabase_key:
            missing.append("SUPABASE_KEY")
        return missing

    @property
    def cors_origins(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.frontend_origins.split(",")
            if origin.strip()
        ]

    @property
    def local_data_file(self) -> Path:
        return Path(self.local_data_path)

    @property
    def local_storage_dir(self) -> Path:
        return Path(self.local_storage_path)


@lru_cache
def get_settings() -> Settings:
    load_dotenv()
    data_backend = os.getenv("DATA_BACKEND", "json")
    return Settings(
        DATA_BACKEND=data_backend,
        LOCAL_DATA_PATH=os.getenv("LOCAL_DATA_PATH", "backend/data/local_db.json"),
        LOCAL_STORAGE_PATH=os.getenv("LOCAL_STORAGE_PATH", "backend/data/storage"),
        SUPABASE_URL=os.getenv("SUPABASE_URL"),
        SUPABASE_KEY=os.getenv("SUPABASE_KEY"),
        SECRET_KEY=os.getenv("SECRET_KEY")
        or ("dev-local-secret-change-me-please-rotate" if data_backend == "json" else None),
        JWT_ALGORITHM=os.getenv("JWT_ALGORITHM", "HS256"),
        ACCESS_TOKEN_EXPIRES_HOURS=int(os.getenv("ACCESS_TOKEN_EXPIRES_HOURS", "8")),
        CLINICAL_ATTACHMENTS_BUCKET=os.getenv(
            "CLINICAL_ATTACHMENTS_BUCKET",
            "clinical-attachments",
        ),
        ATTACHMENT_SIGNED_URL_EXPIRES_SECONDS=int(
            os.getenv("ATTACHMENT_SIGNED_URL_EXPIRES_SECONDS", "3600")
        ),
        MAX_ATTACHMENT_SIZE_MB=int(os.getenv("MAX_ATTACHMENT_SIZE_MB", "10")),
        FRONTEND_ORIGINS=os.getenv(
            "FRONTEND_ORIGINS",
            (
                "http://127.0.0.1:5173,http://localhost:5173,"
                "http://127.0.0.1:5174,http://localhost:5174"
            ),
        ),
    )
