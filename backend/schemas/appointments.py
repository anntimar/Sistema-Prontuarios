from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


AppointmentStatus = Literal["Agendada", "Realizada", "Cancelada"]


class AppointmentCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    id_paciente: str = Field(min_length=1)
    id_medico: str = Field(min_length=1)
    scheduled_at: datetime
    observacoes: str = Field(default="", max_length=2000)


class AppointmentUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    id_paciente: str | None = Field(default=None, min_length=1)
    id_medico: str | None = Field(default=None, min_length=1)
    scheduled_at: datetime | None = None
    status: AppointmentStatus | None = None
    observacoes: str | None = Field(default=None, max_length=2000)
