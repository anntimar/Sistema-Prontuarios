from typing import Any

from pydantic import BaseModel, Field


class MessageResponse(BaseModel):
    message: str


class PaginatedResponse(BaseModel):
    items: list[dict[str, Any]]
    limit: int = Field(ge=1, le=100)
    offset: int = Field(ge=0)
