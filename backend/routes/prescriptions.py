from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from backend.core.security import role_required
from backend.schemas.auth import AuthenticatedUser
from backend.schemas.common import MessageResponse, PaginatedResponse
from backend.schemas.prescriptions import (
    PrescriptionCreate,
    PrescriptionStatus,
    PrescriptionUpdate,
)
from backend.services.audit import first_resource_id, write_audit_log
from backend.services.prescriptions import (
    create_prescription,
    dispense_prescription,
    get_prescription,
    list_prescriptions,
    update_prescription,
)


router = APIRouter(prefix="/prescricoes")


@router.post("", status_code=status.HTTP_201_CREATED)
def create_prescricao(
    prescription: PrescriptionCreate,
    user: AuthenticatedUser = Depends(role_required("medico")),
):
    created = create_prescription(prescription, id_medico=user.id)
    write_audit_log(
        user,
        action="prescription.create",
        resource_type="prescription",
        resource_id=first_resource_id(created),
        metadata={
            "id_prontuario": prescription.id_prontuario,
            "itens": len(prescription.itens or []),
        },
    )
    return created


@router.get("", response_model=PaginatedResponse)
def list_prescricoes(
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
    id_prontuario: Annotated[str | None, Query(min_length=1)] = None,
    status_filter: Annotated[PrescriptionStatus | None, Query(alias="status")] = None,
    user: AuthenticatedUser = Depends(role_required("admin", "medico", "farmaceutico")),
):
    selected_id_medico = user.id if user.role == "medico" else None
    items = list_prescriptions(
        limit=limit,
        offset=offset,
        id_prontuario=id_prontuario,
        status_filter=status_filter,
        id_medico=selected_id_medico,
    )
    return PaginatedResponse(items=items, limit=limit, offset=offset)


@router.get("/{id_prescricao}")
def get_prescricao(
    id_prescricao: str,
    user: AuthenticatedUser = Depends(role_required("admin", "medico", "farmaceutico")),
):
    selected_id_medico = user.id if user.role == "medico" else None
    return get_prescription(id_prescricao, id_medico=selected_id_medico)


@router.patch("/{id_prescricao}")
def update_prescricao(
    id_prescricao: str,
    prescription: PrescriptionUpdate,
    user: AuthenticatedUser = Depends(role_required("medico")),
):
    updated = update_prescription(id_prescricao, prescription, id_medico=user.id)
    write_audit_log(
        user,
        action="prescription.update",
        resource_type="prescription",
        resource_id=id_prescricao,
        metadata={
            "status": prescription.status,
            "itens": len(prescription.itens or []),
        },
    )
    return updated


@router.patch("/{id_prescricao}/dispensar", response_model=MessageResponse)
def dispensar_medicamento(
    id_prescricao: str,
    user: AuthenticatedUser = Depends(role_required("farmaceutico")),
):
    stock_updates = dispense_prescription(id_prescricao, user=user)
    write_audit_log(
        user,
        action="prescription.dispense",
        resource_type="prescription",
        resource_id=id_prescricao,
        metadata={"estoque_baixado": len(stock_updates)},
    )
    return MessageResponse(message="Dispensado com sucesso.")
