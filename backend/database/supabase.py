from fastapi import HTTPException, status
from supabase import Client, create_client

from backend.core.config import get_settings


_client: Client | None = None


def get_supabase_client() -> Client:
    global _client

    if _client is not None:
        return _client

    settings = get_settings()
    missing = settings.missing_supabase_settings
    if missing:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Configuracao ausente: {', '.join(missing)}.",
        )

    _client = create_client(settings.supabase_url, settings.supabase_key)
    return _client
