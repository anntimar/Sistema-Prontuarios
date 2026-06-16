from datetime import date, datetime, time, timezone

from fastapi import HTTPException, status

from backend.database.supabase import get_supabase_client
from backend.schemas.records import MedicalRecordCreate, MedicalRecordUpdate
from backend.services.clinical_context import enrich_medical_records


def create_medical_record(record: MedicalRecordCreate, id_medico: str):
    if record.id_consulta:
        _assert_appointment_can_generate_record(
            id_consulta=record.id_consulta,
            id_paciente=record.id_paciente,
            id_medico=id_medico,
        )

    data = record.model_dump()
    data["id_medico"] = id_medico
    data["created_at"] = datetime.now(timezone.utc).isoformat()
    response = get_supabase_client().table("medical_records").insert(data).execute()
    return enrich_medical_records(response.data)


def list_medical_records(
    *,
    limit: int = 20,
    offset: int = 0,
    id_paciente: str | None = None,
    id_medico: str | None = None,
    created_from: date | None = None,
    created_to: date | None = None,
):
    query = get_supabase_client().table("medical_records").select("*")

    if id_paciente:
        query = query.eq("id_paciente", id_paciente)
    if id_medico:
        query = query.eq("id_medico", id_medico)
    if created_from:
        starts_at = datetime.combine(created_from, time.min, tzinfo=timezone.utc)
        query = query.gte("created_at", starts_at.isoformat())
    if created_to:
        ends_at = datetime.combine(created_to, time.max, tzinfo=timezone.utc)
        query = query.lte("created_at", ends_at.isoformat())

    response = query.order("created_at", desc=True).range(offset, offset + limit - 1).execute()
    return enrich_medical_records(response.data)


def get_medical_record(id_prontuario: str, *, id_medico: str | None = None):
    query = (
        get_supabase_client()
        .table("medical_records")
        .select("*")
        .eq("id", id_prontuario)
    )
    if id_medico:
        query = query.eq("id_medico", id_medico)

    response = query.execute()
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prontuario nao encontrado.",
        )
    return enrich_medical_records(response.data)[0]


def _assert_appointment_can_generate_record(
    *,
    id_consulta: str,
    id_paciente: str,
    id_medico: str,
) -> None:
    response = (
        get_supabase_client()
        .table("appointments")
        .select("id,id_paciente,id_medico,status")
        .eq("id", id_consulta)
        .eq("id_medico", id_medico)
        .execute()
    )
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consulta nao encontrada.",
        )

    appointment = response.data[0]
    if appointment["id_paciente"] != id_paciente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Consulta nao pertence ao paciente informado.",
        )
    if appointment["status"] != "Realizada":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Apenas consultas realizadas podem gerar prontuario.",
        )


def update_medical_record(
    id_prontuario: str,
    record: MedicalRecordUpdate,
    *,
    id_medico: str | None = None,
):
    data = record.model_dump(exclude_unset=True, exclude_none=True)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nenhum campo informado para atualizacao.",
        )

    query = (
        get_supabase_client()
        .table("medical_records")
        .update(data)
        .eq("id", id_prontuario)
    )
    if id_medico:
        query = query.eq("id_medico", id_medico)

    response = query.execute()
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prontuario nao encontrado.",
        )
    return enrich_medical_records(response.data)[0]
