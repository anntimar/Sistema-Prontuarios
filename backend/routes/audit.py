from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from backend.core.security import role_required
from backend.schemas.audit import AuditLog
from backend.schemas.auth import AuthenticatedUser
from backend.schemas.common import PaginatedResponse
from backend.services.audit import list_audit_logs


router = APIRouter(prefix="/auditoria")


@router.get("", response_model=PaginatedResponse)
def list_auditoria(
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
    action: Annotated[str | None, Query(min_length=2, max_length=80)] = None,
    resource_type: Annotated[str | None, Query(min_length=2, max_length=80)] = None,
    actor_email: Annotated[str | None, Query(min_length=2, max_length=254)] = None,
    created_from: date | None = None,
    created_to: date | None = None,
    user: AuthenticatedUser = Depends(role_required("admin")),
):
    items: list[AuditLog] = list_audit_logs(
        limit=limit,
        offset=offset,
        action=action,
        resource_type=resource_type,
        actor_email=actor_email,
        created_from=created_from,
        created_to=created_to,
    )
    return PaginatedResponse(items=items, limit=limit, offset=offset)
