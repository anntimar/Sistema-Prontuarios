from datetime import date
import re
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


ONLY_DIGITS = re.compile(r"\D+")


class PatientBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    nome: str = Field(min_length=3, max_length=120)
    cpf: str = Field(min_length=11, max_length=14)
    data_nascimento: date
    telefone: str = Field(min_length=10, max_length=15)

    @field_validator("cpf")
    @classmethod
    def validate_cpf(cls, value: str) -> str:
        digits = ONLY_DIGITS.sub("", value)
        if len(digits) != 11:
            raise ValueError("CPF deve conter 11 digitos.")
        return digits

    @field_validator("telefone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        digits = ONLY_DIGITS.sub("", value)
        if len(digits) not in (10, 11):
            raise ValueError("Telefone deve conter 10 ou 11 digitos.")
        return digits


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    nome: str | None = Field(default=None, min_length=3, max_length=120)
    cpf: str | None = Field(default=None, min_length=11, max_length=14)
    data_nascimento: date | None = None
    telefone: str | None = Field(default=None, min_length=10, max_length=15)

    @field_validator("cpf")
    @classmethod
    def validate_cpf(cls, value: str | None) -> str | None:
        if value is None:
            return value
        digits = ONLY_DIGITS.sub("", value)
        if len(digits) != 11:
            raise ValueError("CPF deve conter 11 digitos.")
        return digits

    @field_validator("telefone")
    @classmethod
    def validate_phone(cls, value: str | None) -> str | None:
        if value is None:
            return value
        digits = ONLY_DIGITS.sub("", value)
        if len(digits) not in (10, 11):
            raise ValueError("Telefone deve conter 10 ou 11 digitos.")
        return digits


class PatientCreateResponse(BaseModel):
    message: str
    data: list[dict[str, Any]]
