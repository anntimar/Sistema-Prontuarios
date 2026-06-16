from typing import Any

from pydantic import BaseModel, Field


class AuditLog(BaseModel):
    id: str
    actor_id: str | None = None
    actor_email: str
    actor_role: str
    action: str
    resource_type: str
    resource_id: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: str | None = None
