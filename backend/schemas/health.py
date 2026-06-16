from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    supabase_configured: bool
    secret_key_configured: bool
