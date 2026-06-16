from pathlib import Path
import re
import unicodedata
from uuid import uuid4

from fastapi import HTTPException, status

from backend.core.config import get_settings
from backend.database.supabase import get_supabase_client
from backend.schemas.attachments import AttachmentCreate, AttachmentType
from backend.schemas.auth import AuthenticatedUser


ALLOWED_UPLOAD_TYPES = {
    "application/pdf": ".pdf",
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}


def create_attachment(attachment: AttachmentCreate, *, user: AuthenticatedUser):
    _assert_patient_exists(attachment.id_paciente)
    if attachment.id_prontuario:
        _assert_record_belongs_to_patient(
            id_prontuario=attachment.id_prontuario,
            id_paciente=attachment.id_paciente,
            user=user,
        )

    data = attachment.model_dump(exclude_none=True)
    data["uploaded_by"] = user.id
    data["uploaded_by_email"] = user.email

    response = get_supabase_client().table("clinical_attachments").insert(data).execute()
    return enrich_attachments(response.data)[0]


def create_uploaded_attachment(
    *,
    id_paciente: str,
    id_prontuario: str | None,
    tipo: AttachmentType,
    titulo: str,
    observacoes: str,
    filename: str | None,
    content_type: str | None,
    content: bytes,
    user: AuthenticatedUser,
):
    _validate_uploaded_file(content=content, content_type=content_type)
    _assert_patient_exists(id_paciente)
    if id_prontuario:
        _assert_record_belongs_to_patient(
            id_prontuario=id_prontuario,
            id_paciente=id_paciente,
            user=user,
        )

    settings = get_settings()
    bucket = settings.clinical_attachments_bucket
    safe_filename = _safe_filename(filename or "anexo")
    storage_path = f"pacientes/{id_paciente}/{uuid4().hex}-{safe_filename}"

    _upload_to_storage(
        bucket=bucket,
        storage_path=storage_path,
        content=content,
        content_type=content_type or "application/octet-stream",
    )

    data = {
        "id_paciente": id_paciente,
        "tipo": tipo,
        "titulo": titulo,
        "arquivo_url": f"storage://{bucket}/{storage_path}",
        "observacoes": observacoes,
        "storage_bucket": bucket,
        "storage_path": storage_path,
        "file_name": safe_filename,
        "content_type": content_type,
        "file_size": len(content),
        "uploaded_by": user.id,
        "uploaded_by_email": user.email,
    }
    if id_prontuario:
        data["id_prontuario"] = id_prontuario

    try:
        response = get_supabase_client().table("clinical_attachments").insert(data).execute()
    except Exception:
        _remove_storage_file(bucket, storage_path)
        raise

    return enrich_attachments(response.data)[0]


def list_attachments(
    *,
    limit: int = 20,
    offset: int = 0,
    id_paciente: str | None = None,
    id_prontuario: str | None = None,
    tipo: AttachmentType | None = None,
):
    query = get_supabase_client().table("clinical_attachments").select("*")

    if id_paciente:
        query = query.eq("id_paciente", id_paciente)
    if id_prontuario:
        query = query.eq("id_prontuario", id_prontuario)
    if tipo:
        query = query.eq("tipo", tipo)

    response = (
        query.order("created_at", desc=True)
        .range(offset, offset + limit - 1)
        .execute()
    )
    return enrich_attachments(response.data)


def delete_attachment(id_anexo: str) -> None:
    existing = (
        get_supabase_client()
        .table("clinical_attachments")
        .select("*")
        .eq("id", id_anexo)
        .execute()
    )
    if not existing.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Anexo nao encontrado.",
        )

    response = (
        get_supabase_client()
        .table("clinical_attachments")
        .delete()
        .eq("id", id_anexo)
        .execute()
    )
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Anexo nao encontrado.",
        )

    attachment = existing.data[0]
    if attachment.get("storage_bucket") and attachment.get("storage_path"):
        _remove_storage_file(attachment["storage_bucket"], attachment["storage_path"])


def enrich_attachments(attachments: list[dict]) -> list[dict]:
    if not attachments:
        return attachments

    patient_names = _fetch_patient_names({item["id_paciente"] for item in attachments})
    record_map = _fetch_record_map(
        {
            item["id_prontuario"]
            for item in attachments
            if item.get("id_prontuario")
        }
    )

    return [
        {
            **item,
            "paciente_nome": patient_names.get(item["id_paciente"]),
            "prontuario_diagnostico": record_map.get(item.get("id_prontuario"), {}).get("diagnostico"),
            "download_url": _download_url_for(item),
        }
        for item in attachments
    ]


def _validate_uploaded_file(*, content: bytes, content_type: str | None) -> None:
    if not content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Arquivo vazio.",
        )

    max_size = get_settings().max_attachment_size_mb * 1024 * 1024
    if len(content) > max_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Arquivo maior que {get_settings().max_attachment_size_mb} MB.",
        )

    if content_type not in ALLOWED_UPLOAD_TYPES:
        allowed = ", ".join(sorted(ALLOWED_UPLOAD_TYPES))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tipo de arquivo nao permitido. Use: {allowed}.",
        )


def _upload_to_storage(
    *,
    bucket: str,
    storage_path: str,
    content: bytes,
    content_type: str,
) -> None:
    try:
        get_supabase_client().storage.from_(bucket).upload(
            storage_path,
            content,
            {
                "content-type": content_type,
                "x-upsert": "false",
            },
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Nao foi possivel enviar o arquivo para o Storage.",
        ) from exc


def _remove_storage_file(bucket: str, storage_path: str) -> None:
    try:
        get_supabase_client().storage.from_(bucket).remove([storage_path])
    except Exception:
        pass


def _download_url_for(attachment: dict) -> str | None:
    bucket = attachment.get("storage_bucket")
    storage_path = attachment.get("storage_path")
    if not bucket or not storage_path:
        return attachment.get("arquivo_url")

    try:
        signed = get_supabase_client().storage.from_(bucket).create_signed_url(
            storage_path,
            get_settings().attachment_signed_url_expires_seconds,
            {"download": attachment.get("file_name") or True},
        )
        return signed.get("signedUrl") or signed.get("signedURL")
    except Exception:
        return None


def _safe_filename(filename: str) -> str:
    raw = Path(filename).name
    ascii_name = (
        unicodedata.normalize("NFKD", raw)
        .encode("ascii", "ignore")
        .decode("ascii")
        .lower()
    )
    safe = re.sub(r"[^a-z0-9._-]+", "-", ascii_name).strip(".-")
    return safe[:120] or "anexo"


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


def _assert_record_belongs_to_patient(
    *,
    id_prontuario: str,
    id_paciente: str,
    user: AuthenticatedUser,
) -> None:
    response = (
        get_supabase_client()
        .table("medical_records")
        .select("id,id_paciente,id_medico")
        .eq("id", id_prontuario)
        .execute()
    )
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prontuario nao encontrado.",
        )

    record = response.data[0]
    if record["id_paciente"] != id_paciente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Prontuario nao pertence ao paciente informado.",
        )
    if user.role == "medico" and record["id_medico"] != user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prontuario nao encontrado.",
        )


def _fetch_patient_names(ids: set[str]) -> dict[str, str]:
    if not ids:
        return {}

    response = (
        get_supabase_client()
        .table("pacientes")
        .select("id,nome")
        .in_("id", list(ids))
        .execute()
    )
    return {item["id"]: item["nome"] for item in response.data}


def _fetch_record_map(ids: set[str]) -> dict[str, dict]:
    if not ids:
        return {}

    response = (
        get_supabase_client()
        .table("medical_records")
        .select("id,diagnostico")
        .in_("id", list(ids))
        .execute()
    )
    return {item["id"]: item for item in response.data}
