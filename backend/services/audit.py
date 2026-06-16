from datetime import date, datetime, time, timezone
from typing import Any

from backend.database.supabase import get_supabase_client
from backend.schemas.auth import AuthenticatedUser


def write_audit_log(
    user: AuthenticatedUser,
    *,
    action: str,
    resource_type: str,
    resource_id: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> None:
    data = {
        "actor_id": user.id,
        "actor_email": user.email,
        "actor_role": user.role,
        "action": action,
        "resource_type": resource_type,
        "resource_id": resource_id,
        "metadata": metadata or {},
    }

    try:
        get_supabase_client().table("audit_logs").insert(data).execute()
    except Exception:
        # Auditoria nao deve impedir a operacao principal em ambientes ainda sem migration.
        return


def list_audit_logs(
    *,
    limit: int = 20,
    offset: int = 0,
    action: str | None = None,
    resource_type: str | None = None,
    actor_email: str | None = None,
    created_from: date | None = None,
    created_to: date | None = None,
) -> list[dict]:
    query = get_supabase_client().table("audit_logs").select("*")

    if action:
        query = query.eq("action", action)
    if resource_type:
        query = query.eq("resource_type", resource_type)
    if actor_email:
        query = query.ilike("actor_email", f"%{actor_email.strip().lower()}%")
    if created_from:
        starts_at = datetime.combine(created_from, time.min, tzinfo=timezone.utc)
        query = query.gte("created_at", starts_at.isoformat())
    if created_to:
        ends_at = datetime.combine(created_to, time.max, tzinfo=timezone.utc)
        query = query.lte("created_at", ends_at.isoformat())

    response = (
        query.order("created_at", desc=True)
        .range(offset, offset + limit - 1)
        .execute()
    )
    return response.data


def first_resource_id(data) -> str | None:
    if isinstance(data, list) and data:
        return data[0].get("id")
    if isinstance(data, dict):
        return data.get("id")
    return None
