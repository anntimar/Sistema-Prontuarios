from pydantic import BaseModel, ConfigDict, Field, field_validator

from backend.core.config import Role


class UserPublic(BaseModel):
    id: str
    email: str
    role: Role
    nome: str | None = None
    ativo: bool
    created_at: str | None = None
    updated_at: str | None = None


class UserCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    email: str = Field(min_length=3, max_length=254)
    senha: str = Field(min_length=8, max_length=128)
    role: Role
    nome: str | None = Field(default=None, max_length=120)
    ativo: bool = True

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        email = value.strip().lower()
        if "@" not in email or "." not in email.split("@")[-1]:
            raise ValueError("Informe um e-mail valido.")
        return email

    @field_validator("nome")
    @classmethod
    def normalize_name(cls, value: str | None) -> str | None:
        if value is None:
            return value
        name = value.strip()
        return name or None


class UserUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    email: str | None = Field(default=None, min_length=3, max_length=254)
    senha: str | None = Field(default=None, min_length=8, max_length=128)
    role: Role | None = None
    nome: str | None = Field(default=None, max_length=120)
    ativo: bool | None = None

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str | None) -> str | None:
        if value is None:
            return value
        email = value.strip().lower()
        if "@" not in email or "." not in email.split("@")[-1]:
            raise ValueError("Informe um e-mail valido.")
        return email

    @field_validator("nome")
    @classmethod
    def normalize_name(cls, value: str | None) -> str | None:
        if value is None:
            return value
        name = value.strip()
        return name or None
