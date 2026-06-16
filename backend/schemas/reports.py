from pydantic import BaseModel, Field


class ReportPeriod(BaseModel):
    created_from: str | None = None
    created_to: str | None = None


class ReportTotals(BaseModel):
    pacientes: int = Field(ge=0)
    prontuarios: int = Field(ge=0)
    prescricoes: int = Field(ge=0)
    prescricoes_pendentes: int = Field(ge=0)
    consultas: int = Field(ge=0)
    consultas_agendadas: int = Field(ge=0)
    consultas_realizadas: int = Field(ge=0)
    consultas_canceladas: int = Field(ge=0)
    medicamentos: int = Field(ge=0)
    medicamentos_baixo_estoque: int = Field(ge=0)
    movimentacoes_estoque: int = Field(ge=0)
    usuarios_ativos: int = Field(ge=0)
    usuarios_inativos: int = Field(ge=0)


class ReportBucket(BaseModel):
    label: str
    value: int = Field(ge=0)


class IndicatorsReport(BaseModel):
    period: ReportPeriod
    totals: ReportTotals
    prescriptions_by_status: list[ReportBucket]
    appointments_by_status: list[ReportBucket]
    stock_movements_by_type: list[ReportBucket]
    patients_by_month: list[ReportBucket]
    records_by_day: list[ReportBucket]
    appointments_by_day: list[ReportBucket]
    stock_movements_by_day: list[ReportBucket]
    top_diagnoses: list[ReportBucket]
