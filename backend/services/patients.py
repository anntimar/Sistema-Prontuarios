import re

from fastapi import HTTPException, status

from backend.database.supabase import get_supabase_client
from backend.schemas.patients import PatientCreate, PatientUpdate


ONLY_DIGITS = re.compile(r"\D+")


def create_patient(patient: PatientCreate):
    response = (
        get_supabase_client()
        .table("pacientes")
        .insert(patient.model_dump(mode="json"))
        .execute()
    )
    return response.data


def get_patient(id_paciente: str):
    response = (
        get_supabase_client()
        .table("pacientes")
        .select("*")
        .eq("id", id_paciente)
        .execute()
    )
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente nao encontrado.",
        )
    return response.data[0]


def list_patients(
    *,
    limit: int = 20,
    offset: int = 0,
    search: str | None = None,
    cpf: str | None = None,
):
    query = get_supabase_client().table("pacientes").select("*")

    if cpf:
        query = query.eq("cpf", ONLY_DIGITS.sub("", cpf))
    if search:
        query = query.ilike("nome", f"%{search.strip()}%")

    response = query.range(offset, offset + limit - 1).execute()
    return response.data


def update_patient(id_paciente: str, patient: PatientUpdate):
    data = patient.model_dump(mode="json", exclude_unset=True, exclude_none=True)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nenhum campo informado para atualizacao.",
        )

    response = (
        get_supabase_client()
        .table("pacientes")
        .update(data)
        .eq("id", id_paciente)
        .execute()
    )
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente nao encontrado.",
        )
    return response.data[0]


def delete_patient(id_paciente: str) -> None:
    response = (
        get_supabase_client()
        .table("pacientes")
        .delete()
        .eq("id", id_paciente)
        .execute()
    )
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente nao encontrado.",
        )
