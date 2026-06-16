from pydantic import BaseModel, ConfigDict, Field


class MedicalRecordBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    id_paciente: str = Field(min_length=1)
    id_consulta: str | None = Field(default=None, min_length=1)
    anamnese: str = Field(min_length=5)
    diagnostico: str = Field(min_length=3)
    observacoes: str = Field(default="", max_length=2000)


class MedicalRecordCreate(MedicalRecordBase):
    pass


class MedicalRecordUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    anamnese: str | None = Field(default=None, min_length=5)
    diagnostico: str | None = Field(default=None, min_length=3)
    observacoes: str | None = Field(default=None, max_length=2000)
