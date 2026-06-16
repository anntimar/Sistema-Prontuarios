from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


MovementType = Literal["Entrada", "Saida"]


class MedicationCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    nome: str = Field(min_length=2, max_length=120)
    apresentacao: str = Field(min_length=1, max_length=120)
    quantidade: int = Field(default=0, ge=0)
    estoque_minimo: int = Field(default=0, ge=0)
    ativo: bool = True


class MedicationUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    nome: str | None = Field(default=None, min_length=2, max_length=120)
    apresentacao: str | None = Field(default=None, min_length=1, max_length=120)
    quantidade: int | None = Field(default=None, ge=0)
    estoque_minimo: int | None = Field(default=None, ge=0)
    ativo: bool | None = None


class StockMovementCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    tipo: MovementType
    quantidade: int = Field(gt=0)
    observacoes: str = Field(default="", max_length=500)
