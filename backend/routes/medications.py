from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from backend.core.security import role_required
from backend.schemas.auth import AuthenticatedUser
from backend.schemas.common import PaginatedResponse
from backend.schemas.medications import (
    MedicationCreate,
    MedicationUpdate,
    StockMovementCreate,
)
from backend.services.audit import write_audit_log
from backend.services.medications import (
    create_medication,
    create_stock_movement,
    list_medications,
    list_stock_movements,
    update_medication,
)


router = APIRouter(prefix="/medicamentos")


@router.get("", response_model=PaginatedResponse)
def list_medicamentos(
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
    search: Annotated[str | None, Query(min_length=2, max_length=100)] = None,
    ativo: bool | None = None,
    baixo_estoque: bool = False,
    user: AuthenticatedUser = Depends(role_required("admin", "medico", "farmaceutico")),
):
    items = list_medications(
        limit=limit,
        offset=offset,
        search=search,
        ativo=ativo,
        baixo_estoque=baixo_estoque,
    )
    return PaginatedResponse(items=items, limit=limit, offset=offset)


@router.get("/movimentacoes", response_model=PaginatedResponse)
def list_movimentacoes_estoque(
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
    id_medicamento: Annotated[str | None, Query(min_length=1)] = None,
    tipo: Annotated[str | None, Query(pattern="^(Entrada|Saida)$")] = None,
    user: AuthenticatedUser = Depends(role_required("admin", "medico", "farmaceutico")),
):
    items = list_stock_movements(
        limit=limit,
        offset=offset,
        id_medicamento=id_medicamento,
        tipo=tipo,
    )
    return PaginatedResponse(items=items, limit=limit, offset=offset)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_medicamento(
    medication: MedicationCreate,
    user: AuthenticatedUser = Depends(role_required("admin", "farmaceutico")),
):
    created = create_medication(medication)
    write_audit_log(
        user,
        action="medication.create",
        resource_type="medication",
        resource_id=created.get("id"),
        metadata={"nome": created.get("nome"), "quantidade": created.get("quantidade")},
    )
    return created


@router.patch("/{id_medicamento}")
def update_medicamento(
    id_medicamento: str,
    medication: MedicationUpdate,
    user: AuthenticatedUser = Depends(role_required("admin", "farmaceutico")),
):
    updated = update_medication(id_medicamento, medication)
    write_audit_log(
        user,
        action="medication.update",
        resource_type="medication",
        resource_id=id_medicamento,
    )
    return updated


@router.post("/{id_medicamento}/movimentacoes")
def create_movimentacao_estoque(
    id_medicamento: str,
    movement: StockMovementCreate,
    user: AuthenticatedUser = Depends(role_required("admin", "farmaceutico")),
):
    updated = create_stock_movement(id_medicamento, movement, user=user)
    write_audit_log(
        user,
        action="medication.stock_movement",
        resource_type="medication",
        resource_id=id_medicamento,
        metadata={
            "tipo": movement.tipo,
            "quantidade": movement.quantidade,
            "quantidade_atual": updated.get("quantidade"),
        },
    )
    return updated
