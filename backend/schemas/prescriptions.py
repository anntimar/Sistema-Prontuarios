from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


PrescriptionStatus = Literal["Pendente", "Entregue", "Cancelada"]


class PrescriptionItemPayload(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    id_medicamento: str = Field(min_length=1)
    quantidade: int = Field(gt=0)
    posologia: str = Field(min_length=3, max_length=500)


class PrescriptionCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    id_prontuario: str = Field(min_length=1)
    medicamentos: list[str] | None = Field(default=None, min_length=1)
    itens: list[PrescriptionItemPayload] | None = Field(default=None, min_length=1)

    @model_validator(mode="after")
    def validate_content(self):
        if not self.medicamentos and not self.itens:
            raise ValueError("Informe pelo menos um medicamento.")
        return self

    @field_validator("medicamentos")
    @classmethod
    def validate_medications(cls, value: list[str] | None) -> list[str] | None:
        if value is None:
            return value
        medications = [item.strip() for item in value if item.strip()]
        if not medications:
            raise ValueError("Informe pelo menos um medicamento.")
        return medications


class PrescriptionUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    medicamentos: list[str] | None = Field(default=None, min_length=1)
    itens: list[PrescriptionItemPayload] | None = Field(default=None, min_length=1)
    status: PrescriptionStatus | None = None

    @field_validator("medicamentos")
    @classmethod
    def validate_medications(cls, value: list[str] | None) -> list[str] | None:
        if value is None:
            return value
        medications = [item.strip() for item in value if item.strip()]
        if not medications:
            raise ValueError("Informe pelo menos um medicamento.")
        return medications
