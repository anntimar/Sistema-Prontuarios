from pydantic import BaseModel, ConfigDict

from backend.core.config import Role


class AuthenticatedUser(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    id: str
    email: str
    role: Role


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
