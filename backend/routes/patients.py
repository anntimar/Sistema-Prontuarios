from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from backend.core.security import role_required
from backend.schemas.auth import AuthenticatedUser
from backend.schemas.common import MessageResponse, PaginatedResponse
from backend.schemas.patients import PatientCreate, PatientCreateResponse, PatientUpdate
from backend.services.audit import first_resource_id, write_audit_log
from backend.services.patients import (
    create_patient,
    delete_patient,
    get_patient,
    list_patients,
    update_patient,
)


router = APIRouter(prefix="/pacientes")


@router.post("", response_model=PatientCreateResponse, status_code=status.HTTP_201_CREATED)
def create_paciente(
    patient: PatientCreate,
    user: AuthenticatedUser = Depends(role_required("admin", "recepcao")),
):
    data = create_patient(patient)
    write_audit_log(
        user,
        action="patient.create",
        resource_type="patient",
        resource_id=first_resource_id(data),
    )
    return PatientCreateResponse(message="Paciente cadastrado.", data=data)


@router.get("", response_model=PaginatedResponse)
def list_pacientes(
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
    search: Annotated[str | None, Query(min_length=2, max_length=100)] = None,
    cpf: Annotated[str | None, Query(min_length=11, max_length=14)] = None,
    user: AuthenticatedUser = Depends(role_required("admin", "medico", "recepcao")),
):
    items = list_patients(limit=limit, offset=offset, search=search, cpf=cpf)
    return PaginatedResponse(items=items, limit=limit, offset=offset)


@router.get("/{id_paciente}")
def get_paciente(
    id_paciente: str,
    user: AuthenticatedUser = Depends(role_required("admin", "medico", "recepcao")),
):
    return get_patient(id_paciente)


@router.patch("/{id_paciente}")
def update_paciente(
    id_paciente: str,
    patient: PatientUpdate,
    user: AuthenticatedUser = Depends(role_required("admin", "recepcao")),
):
    updated = update_patient(id_paciente, patient)
    write_audit_log(
        user,
        action="patient.update",
        resource_type="patient",
        resource_id=id_paciente,
    )
    return updated


@router.delete("/{id_paciente}", response_model=MessageResponse)
def delete_paciente(
    id_paciente: str,
    user: AuthenticatedUser = Depends(role_required("admin")),
):
    delete_patient(id_paciente)
    write_audit_log(
        user,
        action="patient.delete",
        resource_type="patient",
        resource_id=id_paciente,
    )
    return MessageResponse(message="Paciente removido.")
