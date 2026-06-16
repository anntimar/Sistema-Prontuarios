from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from backend.core.security import role_required
from backend.schemas.auth import AuthenticatedUser
from backend.schemas.common import PaginatedResponse
from backend.schemas.records import MedicalRecordCreate, MedicalRecordUpdate
from backend.services.audit import first_resource_id, write_audit_log
from backend.services.medical_records import (
    create_medical_record,
    get_medical_record,
    list_medical_records,
    update_medical_record,
)


router = APIRouter(prefix="/prontuarios")


@router.post("", status_code=status.HTTP_201_CREATED)
def create_prontuario(
    record: MedicalRecordCreate,
    user: AuthenticatedUser = Depends(role_required("medico")),
):
    created = create_medical_record(record, id_medico=user.id)
    write_audit_log(
        user,
        action="medical_record.create",
        resource_type="medical_record",
        resource_id=first_resource_id(created),
        metadata={
            "id_paciente": record.id_paciente,
            "id_consulta": record.id_consulta,
        },
    )
    return created


@router.get("", response_model=PaginatedResponse)
def list_prontuarios(
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
    id_paciente: Annotated[str | None, Query(min_length=1)] = None,
    id_medico: Annotated[str | None, Query(min_length=1)] = None,
    created_from: date | None = None,
    created_to: date | None = None,
    user: AuthenticatedUser = Depends(role_required("admin", "medico", "recepcao")),
):
    selected_id_medico = user.id if user.role == "medico" else id_medico
    items = list_medical_records(
        limit=limit,
        offset=offset,
        id_paciente=id_paciente,
        id_medico=selected_id_medico,
        created_from=created_from,
        created_to=created_to,
    )
    return PaginatedResponse(items=items, limit=limit, offset=offset)


@router.get("/{id_prontuario}")
def get_prontuario(
    id_prontuario: str,
    user: AuthenticatedUser = Depends(role_required("admin", "medico", "recepcao")),
):
    id_medico = user.id if user.role == "medico" else None
    return get_medical_record(id_prontuario, id_medico=id_medico)


@router.patch("/{id_prontuario}")
def update_prontuario(
    id_prontuario: str,
    record: MedicalRecordUpdate,
    user: AuthenticatedUser = Depends(role_required("medico")),
):
    updated = update_medical_record(id_prontuario, record, id_medico=user.id)
    write_audit_log(
        user,
        action="medical_record.update",
        resource_type="medical_record",
        resource_id=id_prontuario,
    )
    return updated
