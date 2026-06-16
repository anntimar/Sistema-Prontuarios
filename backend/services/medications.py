import re
import unicodedata
from collections import Counter

from fastapi import HTTPException, status

from backend.database.supabase import get_supabase_client
from backend.schemas.auth import AuthenticatedUser
from backend.schemas.medications import (
    MedicationCreate,
    MedicationUpdate,
    StockMovementCreate,
)


def list_medications(
    *,
    limit: int = 20,
    offset: int = 0,
    search: str | None = None,
    ativo: bool | None = None,
    baixo_estoque: bool = False,
) -> list[dict]:
    query = get_supabase_client().table("medications").select("*")

    if search:
        query = query.ilike("nome", f"%{search}%")
    if ativo is not None:
        query = query.eq("ativo", ativo)

    response = query.order("nome").range(offset, offset + limit - 1).execute()
    items = enrich_medications(response.data)
    if baixo_estoque:
        return [item for item in items if item["baixo_estoque"]]
    return items


def list_stock_movements(
    *,
    limit: int = 20,
    offset: int = 0,
    id_medicamento: str | None = None,
    tipo: str | None = None,
) -> list[dict]:
    query = get_supabase_client().table("medication_movements").select("*")

    if id_medicamento:
        query = query.eq("id_medicamento", id_medicamento)
    if tipo:
        query = query.eq("tipo", tipo)

    response = (
        query.order("created_at", desc=True)
        .range(offset, offset + limit - 1)
        .execute()
    )
    return enrich_stock_movements(response.data)


def create_medication(medication: MedicationCreate) -> dict:
    response = (
        get_supabase_client()
        .table("medications")
        .insert(medication.model_dump())
        .execute()
    )
    return enrich_medications(response.data)[0]


def update_medication(id_medicamento: str, medication: MedicationUpdate) -> dict:
    data = medication.model_dump(exclude_unset=True, exclude_none=True)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nenhum campo informado para atualizacao.",
        )

    response = (
        get_supabase_client()
        .table("medications")
        .update(data)
        .eq("id", id_medicamento)
        .execute()
    )
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medicamento nao encontrado.",
        )
    return enrich_medications(response.data)[0]


def create_stock_movement(
    id_medicamento: str,
    movement: StockMovementCreate,
    *,
    user: AuthenticatedUser,
    id_prescricao: str | None = None,
) -> dict:
    medication = _get_medication(id_medicamento)
    previous_quantity = int(medication["quantidade"])
    delta = movement.quantidade if movement.tipo == "Entrada" else -movement.quantidade
    new_quantity = previous_quantity + delta
    if new_quantity < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Estoque insuficiente para esta saida.",
        )

    updated = (
        get_supabase_client()
        .table("medications")
        .update({"quantidade": new_quantity})
        .eq("id", id_medicamento)
        .execute()
    )
    if not updated.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medicamento nao encontrado.",
        )

    movement_data = {
        "id_medicamento": id_medicamento,
        "tipo": movement.tipo,
        "quantidade": movement.quantidade,
        "quantidade_anterior": previous_quantity,
        "quantidade_atual": new_quantity,
        "observacoes": movement.observacoes,
        "id_prescricao": id_prescricao,
        "created_by": user.id,
        "created_by_email": user.email,
    }
    get_supabase_client().table("medication_movements").insert(movement_data).execute()
    return enrich_medications(updated.data)[0]


def apply_prescription_stock_movements(
    prescription: dict,
    *,
    user: AuthenticatedUser,
) -> list[dict]:
    structured_items = prescription.get("itens") or []
    if structured_items:
        return _apply_structured_prescription_items(
            prescription,
            structured_items,
            user=user,
        )

    inventory = _active_medications()
    matches = [
        match
        for item in prescription.get("medicamentos", [])
        if (match := _match_medication(str(item), inventory))
    ]
    if not matches:
        return []

    quantities = Counter(item["id"] for item in matches)
    by_id = {item["id"]: item for item in matches}
    for id_medicamento, quantity in quantities.items():
        medication = by_id[id_medicamento]
        if int(medication["quantidade"]) < quantity:
            label = medication_label(medication)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Estoque insuficiente para {label}.",
            )

    updated_items = []
    for id_medicamento, quantity in quantities.items():
        movement = StockMovementCreate(
            tipo="Saida",
            quantidade=quantity,
            observacoes="Baixa automatica por dispensacao de prescricao.",
        )
        updated_items.append(
            create_stock_movement(
                id_medicamento,
                movement,
                user=user,
                id_prescricao=prescription["id"],
            )
        )
    return updated_items


def _apply_structured_prescription_items(
    prescription: dict,
    items: list[dict],
    *,
    user: AuthenticatedUser,
) -> list[dict]:
    medications = _medications_by_id({item["id_medicamento"] for item in items})
    for item in items:
        medication = medications.get(item["id_medicamento"])
        if not medication:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Medicamento da prescricao nao encontrado.",
            )
        if int(medication["quantidade"]) < int(item["quantidade"]):
            label = medication_label(medication)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Estoque insuficiente para {label}.",
            )

    updated_items = []
    for item in items:
        movement = StockMovementCreate(
            tipo="Saida",
            quantidade=int(item["quantidade"]),
            observacoes="Baixa automatica por item estruturado da prescricao.",
        )
        updated_items.append(
            create_stock_movement(
                item["id_medicamento"],
                movement,
                user=user,
                id_prescricao=prescription["id"],
            )
        )
    return updated_items


def enrich_medications(items: list[dict]) -> list[dict]:
    return [
        {
            **item,
            "baixo_estoque": int(item.get("quantidade") or 0) <= int(item.get("estoque_minimo") or 0),
        }
        for item in items
    ]


def enrich_stock_movements(items: list[dict]) -> list[dict]:
    if not items:
        return items

    medications = _medications_by_id({item["id_medicamento"] for item in items})
    return [
        {
            **item,
            "medicamento_nome": medications.get(item["id_medicamento"], {}).get("nome"),
            "medicamento_apresentacao": medications.get(item["id_medicamento"], {}).get("apresentacao"),
        }
        for item in items
    ]


def medication_label(medication: dict) -> str:
    return f"{medication['nome']} {medication['apresentacao']}".strip()


def _get_medication(id_medicamento: str) -> dict:
    response = (
        get_supabase_client()
        .table("medications")
        .select("*")
        .eq("id", id_medicamento)
        .execute()
    )
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medicamento nao encontrado.",
        )
    return response.data[0]


def _active_medications() -> list[dict]:
    response = (
        get_supabase_client()
        .table("medications")
        .select("*")
        .eq("ativo", True)
        .execute()
    )
    return response.data


def _medications_by_id(ids: set[str]) -> dict[str, dict]:
    if not ids:
        return {}
    response = (
        get_supabase_client()
        .table("medications")
        .select("id,nome,apresentacao,quantidade,estoque_minimo,ativo")
        .in_("id", list(ids))
        .execute()
    )
    return {item["id"]: item for item in response.data}


def _match_medication(text: str, inventory: list[dict]) -> dict | None:
    normalized_text = _normalize(text)
    matches = [
        item
        for item in inventory
        if _normalize(medication_label(item)) in normalized_text
        or _normalize(item["nome"]) in normalized_text
    ]
    if not matches:
        return None
    return max(matches, key=lambda item: len(_normalize(medication_label(item))))


def _normalize(value: str) -> str:
    normalized = (
        unicodedata.normalize("NFKD", value)
        .encode("ascii", "ignore")
        .decode("ascii")
        .lower()
    )
    return re.sub(r"[^a-z0-9]+", " ", normalized).strip()
