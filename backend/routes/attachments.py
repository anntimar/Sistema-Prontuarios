from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, Query, UploadFile, status

from backend.core.security import role_required
from backend.schemas.attachments import AttachmentCreate, AttachmentType
from backend.schemas.auth import AuthenticatedUser
from backend.schemas.common import MessageResponse, PaginatedResponse
from backend.services.attachments import (
    create_attachment,
    create_uploaded_attachment,
    delete_attachment,
    list_attachments,
)
from backend.services.audit import write_audit_log


router = APIRouter(prefix="/anexos")


@router.post("", status_code=status.HTTP_201_CREATED)
def create_anexo(
    attachment: AttachmentCreate,
    user: AuthenticatedUser = Depends(role_required("admin", "medico", "recepcao")),
):
    created = create_attachment(attachment, user=user)
    write_audit_log(
        user,
        action="attachment.create",
        resource_type="attachment",
        resource_id=created.get("id"),
        metadata={
            "id_paciente": attachment.id_paciente,
            "id_prontuario": attachment.id_prontuario,
            "tipo": attachment.tipo,
        },
    )
    return created


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_anexo(
    id_paciente: Annotated[str, Form(min_length=1)],
    tipo: Annotated[AttachmentType, Form()],
    titulo: Annotated[str, Form(min_length=3, max_length=160)],
    file: Annotated[UploadFile, File()],
    id_prontuario: Annotated[str | None, Form(min_length=1)] = None,
    observacoes: Annotated[str, Form(max_length=1000)] = "",
    user: AuthenticatedUser = Depends(role_required("admin", "medico", "recepcao")),
):
    content = await file.read()
    created = create_uploaded_attachment(
        id_paciente=id_paciente,
        id_prontuario=id_prontuario,
        tipo=tipo,
        titulo=titulo,
        observacoes=observacoes,
        filename=file.filename,
        content_type=file.content_type,
        content=content,
        user=user,
    )
    write_audit_log(
        user,
        action="attachment.upload",
        resource_type="attachment",
        resource_id=created.get("id"),
        metadata={
            "id_paciente": id_paciente,
            "id_prontuario": id_prontuario,
            "tipo": tipo,
            "file_name": created.get("file_name"),
        },
    )
    return created


@router.get("", response_model=PaginatedResponse)
def list_anexos(
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
    id_paciente: Annotated[str | None, Query(min_length=1)] = None,
    id_prontuario: Annotated[str | None, Query(min_length=1)] = None,
    tipo: AttachmentType | None = None,
    user: AuthenticatedUser = Depends(role_required("admin", "medico", "recepcao")),
):
    items = list_attachments(
        limit=limit,
        offset=offset,
        id_paciente=id_paciente,
        id_prontuario=id_prontuario,
        tipo=tipo,
    )
    return PaginatedResponse(items=items, limit=limit, offset=offset)


@router.delete("/{id_anexo}", response_model=MessageResponse)
def delete_anexo(
    id_anexo: str,
    user: AuthenticatedUser = Depends(role_required("admin")),
):
    delete_attachment(id_anexo)
    write_audit_log(
        user,
        action="attachment.delete",
        resource_type="attachment",
        resource_id=id_anexo,
    )
    return MessageResponse(message="Anexo removido.")
