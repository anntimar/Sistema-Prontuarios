from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


AttachmentType = Literal["Exame", "Laudo", "Imagem", "Outro"]


class AttachmentCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    id_paciente: str = Field(min_length=1)
    id_prontuario: str | None = Field(default=None, min_length=1)
    tipo: AttachmentType
    titulo: str = Field(min_length=3, max_length=160)
    arquivo_url: str = Field(min_length=8, max_length=1000)
    observacoes: str = Field(default="", max_length=1000)

    @field_validator("arquivo_url")
    @classmethod
    def validate_file_url(cls, value: str) -> str:
        if not value.startswith(("http://", "https://")):
            raise ValueError("Informe uma URL iniciada por http:// ou https://.")
        return value
