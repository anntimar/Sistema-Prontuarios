from fastapi import HTTPException, status
from supabase import Client, create_client

from backend.core.config import get_settings
from backend.database.local_json import LocalJsonClient


_client: Client | LocalJsonClient | None = None
_client_backend: str | None = None


def get_supabase_client() -> Client | LocalJsonClient:
    global _client, _client_backend

    settings = get_settings()
    if _client is not None and _client_backend == settings.data_backend:
        return _client

    if settings.data_backend == "json":
        _client = LocalJsonClient(
            data_path=settings.local_data_file,
            storage_path=settings.local_storage_dir,
        )
        _client_backend = settings.data_backend
        return _client

    missing = settings.missing_supabase_settings
    if missing:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Configuracao ausente: {', '.join(missing)}.",
        )

    _client = create_client(settings.supabase_url, settings.supabase_key)
    _client_backend = settings.data_backend
    return _client
