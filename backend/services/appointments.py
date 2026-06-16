from datetime import date, datetime, time, timezone

from fastapi import HTTPException, status

from backend.database.supabase import get_supabase_client
from backend.schemas.appointments import (
    AppointmentCreate,
    AppointmentStatus,
    AppointmentUpdate,
)
from backend.services.clinical_context import enrich_appointments


def create_appointment(appointment: AppointmentCreate):
    _assert_patient_exists(appointment.id_paciente)
    _assert_active_doctor(appointment.id_medico)

    data = appointment.model_dump()
    data["scheduled_at"] = appointment.scheduled_at.isoformat()
    data["status"] = "Agendada"

    response = get_supabase_client().table("appointments").insert(data).execute()
    return enrich_appointments(response.data)[0]


def list_appointments(
    *,
    limit: int = 20,
    offset: int = 0,
    id_paciente: str | None = None,
    id_medico: str | None = None,
    status_filter: AppointmentStatus | None = None,
    scheduled_from: date | None = None,
    scheduled_to: date | None = None,
):
    query = get_supabase_client().table("appointments").select("*")

    if id_paciente:
        query = query.eq("id_paciente", id_paciente)
    if id_medico:
        query = query.eq("id_medico", id_medico)
    if status_filter:
        query = query.eq("status", status_filter)
    if scheduled_from:
        starts_at = datetime.combine(scheduled_from, time.min, tzinfo=timezone.utc)
        query = query.gte("scheduled_at", starts_at.isoformat())
    if scheduled_to:
        ends_at = datetime.combine(scheduled_to, time.max, tzinfo=timezone.utc)
        query = query.lte("scheduled_at", ends_at.isoformat())

    response = (
        query.order("scheduled_at")
        .range(offset, offset + limit - 1)
        .execute()
    )
    return enrich_appointments(response.data)


def get_appointment(id_consulta: str, *, id_medico: str | None = None):
    query = (
        get_supabase_client()
        .table("appointments")
        .select("*")
        .eq("id", id_consulta)
    )
    if id_medico:
        query = query.eq("id_medico", id_medico)

    response = query.execute()
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consulta nao encontrada.",
        )
    return enrich_appointments(response.data)[0]


def update_appointment(
    id_consulta: str,
    appointment: AppointmentUpdate,
    *,
    id_medico: str | None = None,
):
    data = appointment.model_dump(exclude_unset=True, exclude_none=True)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nenhum campo informado para atualizacao.",
        )

    if appointment.id_paciente:
        _assert_patient_exists(appointment.id_paciente)
    if appointment.id_medico:
        _assert_active_doctor(appointment.id_medico)
    if appointment.scheduled_at:
        data["scheduled_at"] = appointment.scheduled_at.isoformat()

    query = (
        get_supabase_client()
        .table("appointments")
        .update(data)
        .eq("id", id_consulta)
    )
    if id_medico:
        query = query.eq("id_medico", id_medico)

    response = query.execute()
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consulta nao encontrada.",
        )
    return enrich_appointments(response.data)[0]


def _assert_patient_exists(id_paciente: str) -> None:
    response = (
        get_supabase_client()
        .table("pacientes")
        .select("id")
        .eq("id", id_paciente)
        .execute()
    )
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente nao encontrado.",
        )


def _assert_active_doctor(id_medico: str) -> None:
    response = (
        get_supabase_client()
        .table("users")
        .select("id")
        .eq("id", id_medico)
        .eq("role", "medico")
        .eq("ativo", True)
        .execute()
    )
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medico nao encontrado ou inativo.",
        )
