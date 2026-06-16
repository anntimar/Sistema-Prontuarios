from datetime import datetime, timezone

from fastapi import HTTPException, status

from backend.database.supabase import get_supabase_client
from backend.schemas.auth import AuthenticatedUser
from backend.schemas.prescriptions import (
    PrescriptionCreate,
    PrescriptionItemPayload,
    PrescriptionUpdate,
)
from backend.services.clinical_context import enrich_prescriptions
from backend.services.medications import apply_prescription_stock_movements


def _assert_medico_owns_record(id_prontuario: str, id_medico: str) -> None:
    response = (
        get_supabase_client()
        .table("medical_records")
        .select("id")
        .eq("id", id_prontuario)
        .eq("id_medico", id_medico)
        .execute()
    )
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prontuario nao encontrado.",
        )


def _list_record_ids_for_medico(id_medico: str) -> list[str]:
    response = (
        get_supabase_client()
        .table("medical_records")
        .select("id")
        .eq("id_medico", id_medico)
        .execute()
    )
    return [item["id"] for item in response.data]


def create_prescription(prescription: PrescriptionCreate, *, id_medico: str):
    _assert_medico_owns_record(prescription.id_prontuario, id_medico)
    items = prescription.itens or []
    _validate_prescription_items(items)
    data = prescription.model_dump(exclude={"itens"}, exclude_none=True)
    if items and not data.get("medicamentos"):
        data["medicamentos"] = _medication_lines_for_items(items)
    data["status"] = "Pendente"
    response = get_supabase_client().table("prescriptions").insert(data).execute()
    if items:
        _replace_prescription_items(response.data[0]["id"], items)
    return enrich_prescriptions(response.data)


def list_prescriptions(
    *,
    limit: int = 20,
    offset: int = 0,
    id_prontuario: str | None = None,
    status_filter: str | None = None,
    id_medico: str | None = None,
):
    query = get_supabase_client().table("prescriptions").select("*")

    if id_prontuario:
        if id_medico:
            _assert_medico_owns_record(id_prontuario, id_medico)
        query = query.eq("id_prontuario", id_prontuario)
    elif id_medico:
        record_ids = _list_record_ids_for_medico(id_medico)
        if not record_ids:
            return []
        query = query.in_("id_prontuario", record_ids)

    if status_filter:
        query = query.eq("status", status_filter)

    response = query.order("created_at", desc=True).range(offset, offset + limit - 1).execute()
    return enrich_prescriptions(response.data)


def get_prescription(id_prescricao: str, *, id_medico: str | None = None):
    response = (
        get_supabase_client()
        .table("prescriptions")
        .select("*")
        .eq("id", id_prescricao)
        .execute()
    )
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prescricao nao encontrada.",
        )
    prescription = response.data[0]
    if id_medico:
        _assert_medico_owns_record(prescription["id_prontuario"], id_medico)
    return enrich_prescriptions([prescription])[0]


def update_prescription(
    id_prescricao: str,
    prescription: PrescriptionUpdate,
    *,
    id_medico: str,
):
    current = get_prescription(id_prescricao, id_medico=id_medico)
    if current["status"] != "Pendente":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Apenas prescricoes pendentes podem ser alteradas.",
        )

    update_items = "itens" in prescription.model_fields_set
    items = prescription.itens or []
    data = prescription.model_dump(exclude={"itens"}, exclude_unset=True, exclude_none=True)
    if data.get("status") == "Entregue":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Use a rota de dispensacao para marcar prescricao como entregue.",
        )
    if update_items:
        _validate_prescription_items(items)
    if update_items and items and "medicamentos" not in data:
        data["medicamentos"] = _medication_lines_for_items(items)
    if not data:
        if update_items:
            _replace_prescription_items(id_prescricao, items)
            return get_prescription(id_prescricao, id_medico=id_medico)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nenhum campo informado para atualizacao.",
        )

    response = (
        get_supabase_client()
        .table("prescriptions")
        .update(data)
        .eq("id", id_prescricao)
        .execute()
    )
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prescricao nao encontrada.",
        )
    if update_items:
        _replace_prescription_items(id_prescricao, items)
    return enrich_prescriptions(response.data)[0]


def dispense_prescription(id_prescricao: str, *, user: AuthenticatedUser) -> list[dict]:
    current = get_prescription(id_prescricao)
    if current["status"] != "Pendente":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Apenas prescricoes pendentes podem ser dispensadas.",
        )
    stock_updates = apply_prescription_stock_movements(current, user=user)

    response = (
        get_supabase_client()
        .table("prescriptions")
        .update(
            {
                "status": "Entregue",
                "dispensed_at": datetime.now(timezone.utc).isoformat(),
            }
        )
        .eq("id", id_prescricao)
        .execute()
    )

    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prescricao nao encontrada.",
        )
    return stock_updates


def _replace_prescription_items(
    id_prescricao: str,
    items: list[PrescriptionItemPayload],
) -> None:
    get_supabase_client().table("prescription_items").delete().eq("id_prescricao", id_prescricao).execute()
    if not items:
        return
    data = [
        {
            "id_prescricao": id_prescricao,
            "id_medicamento": item.id_medicamento,
            "quantidade": item.quantidade,
            "posologia": item.posologia,
        }
        for item in items
    ]
    get_supabase_client().table("prescription_items").insert(data).execute()


def _validate_prescription_items(items: list[PrescriptionItemPayload]) -> None:
    if not items:
        return
    medications = _medications_by_id({item.id_medicamento for item in items})
    missing_ids = {item.id_medicamento for item in items} - set(medications)
    if missing_ids:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medicamento da prescricao nao encontrado.",
        )
    if any(not medications[item.id_medicamento].get("ativo", True) for item in items):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Medicamento inativo nao pode ser prescrito.",
        )


def _medication_lines_for_items(items: list[PrescriptionItemPayload]) -> list[str]:
    medications = _medications_by_id({item.id_medicamento for item in items})
    lines = []
    for item in items:
        medication = medications.get(item.id_medicamento)
        label = (
            f"{medication['nome']} {medication['apresentacao']}"
            if medication
            else item.id_medicamento
        )
        lines.append(f"{label} - qtd. {item.quantidade} - {item.posologia}")
    return lines


def _medications_by_id(ids: set[str]) -> dict[str, dict]:
    if not ids:
        return {}
    response = (
        get_supabase_client()
        .table("medications")
        .select("id,nome,apresentacao,ativo")
        .in_("id", list(ids))
        .execute()
    )
    return {item["id"]: item for item in response.data}
