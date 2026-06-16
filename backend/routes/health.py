from fastapi import APIRouter

from backend.core.config import get_settings
from backend.schemas.health import HealthResponse


router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health_check():
    settings = get_settings()
    return HealthResponse(
        status="ok",
        supabase_configured=not settings.missing_supabase_settings,
        secret_key_configured=bool(settings.secret_key),
    )
