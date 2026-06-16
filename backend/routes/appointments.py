from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from backend.core.security import role_required
from backend.schemas.appointments import (
    AppointmentCreate,
    AppointmentStatus,
    AppointmentUpdate,
)
from backend.schemas.auth import AuthenticatedUser
from backend.schemas.common import PaginatedResponse
from backend.services.audit import write_audit_log
from backend.services.appointments import (
    create_appointment,
    get_appointment,
    list_appointments,
    update_appointment,
)


router = APIRouter(prefix="/consultas")


@router.post("", status_code=status.HTTP_201_CREATED)
def create_consulta(
    appointment: AppointmentCreate,
    user: AuthenticatedUser = Depends(role_required("admin", "recepcao")),
):
    created = create_appointment(appointment)
    write_audit_log(
        user,
        action="appointment.create",
        resource_type="appointment",
        resource_id=created.get("id"),
        metadata={
            "id_paciente": appointment.id_paciente,
            "id_medico": appointment.id_medico,
            "scheduled_at": appointment.scheduled_at.isoformat(),
        },
    )
    return created


@router.get("", response_model=PaginatedResponse)
def list_consultas(
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
    id_paciente: Annotated[str | None, Query(min_length=1)] = None,
    id_medico: Annotated[str | None, Query(min_length=1)] = None,
    status_filter: Annotated[AppointmentStatus | None, Query(alias="status")] = None,
    scheduled_from: date | None = None,
    scheduled_to: date | None = None,
    user: AuthenticatedUser = Depends(role_required("admin", "medico", "recepcao")),
):
    selected_id_medico = user.id if user.role == "medico" else id_medico
    items = list_appointments(
        limit=limit,
        offset=offset,
        id_paciente=id_paciente,
        id_medico=selected_id_medico,
        status_filter=status_filter,
        scheduled_from=scheduled_from,
        scheduled_to=scheduled_to,
    )
    return PaginatedResponse(items=items, limit=limit, offset=offset)


@router.get("/{id_consulta}")
def get_consulta(
    id_consulta: str,
    user: AuthenticatedUser = Depends(role_required("admin", "medico", "recepcao")),
):
    selected_id_medico = user.id if user.role == "medico" else None
    return get_appointment(id_consulta, id_medico=selected_id_medico)


@router.patch("/{id_consulta}")
def update_consulta(
    id_consulta: str,
    appointment: AppointmentUpdate,
    user: AuthenticatedUser = Depends(role_required("admin", "medico", "recepcao")),
):
    if user.role == "medico" and (
        appointment.id_paciente or appointment.id_medico or appointment.scheduled_at
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Medico pode atualizar apenas status e observacoes da propria consulta.",
        )

    selected_id_medico = user.id if user.role == "medico" else None
    updated = update_appointment(
        id_consulta,
        appointment,
        id_medico=selected_id_medico,
    )
    write_audit_log(
        user,
        action="appointment.update",
        resource_type="appointment",
        resource_id=id_consulta,
        metadata={"status": appointment.status},
    )
    return updated
