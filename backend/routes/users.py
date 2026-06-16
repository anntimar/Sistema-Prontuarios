from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from backend.core.config import Role
from backend.core.security import hash_password, role_required
from backend.schemas.auth import AuthenticatedUser
from backend.schemas.common import PaginatedResponse
from backend.schemas.users import UserCreate, UserPublic, UserUpdate
from backend.services.audit import write_audit_log
from backend.services.users import (
    create_managed_user,
    get_user,
    list_active_doctors,
    list_users,
    update_user,
)


router = APIRouter(prefix="/usuarios")


@router.post("", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def create_usuario(
    user_data: UserCreate,
    current_user: AuthenticatedUser = Depends(role_required("admin")),
):
    created = create_managed_user(
        user_data,
        password_hash=hash_password(user_data.senha),
    )
    write_audit_log(
        current_user,
        action="user.create",
        resource_type="user",
        resource_id=created.get("id"),
        metadata={
            "target_email": created.get("email"),
            "target_role": created.get("role"),
            "target_active": created.get("ativo"),
        },
    )
    return created


@router.get("", response_model=PaginatedResponse)
def list_usuarios(
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
    search: Annotated[str | None, Query(min_length=2, max_length=100)] = None,
    role_filter: Annotated[Role | None, Query(alias="role")] = None,
    ativo: bool | None = None,
    current_user: AuthenticatedUser = Depends(role_required("admin")),
):
    items = list_users(
        limit=limit,
        offset=offset,
        search=search,
        role=role_filter,
        ativo=ativo,
    )
    return PaginatedResponse(items=items, limit=limit, offset=offset)


@router.get("/medicos", response_model=list[UserPublic])
def list_medicos(
    current_user: AuthenticatedUser = Depends(role_required("admin", "medico", "recepcao")),
):
    return list_active_doctors()


@router.get("/{id_usuario}", response_model=UserPublic)
def get_usuario(
    id_usuario: str,
    current_user: AuthenticatedUser = Depends(role_required("admin")),
):
    return get_user(id_usuario)


@router.patch("/{id_usuario}", response_model=UserPublic)
def update_usuario(
    id_usuario: str,
    user_data: UserUpdate,
    current_user: AuthenticatedUser = Depends(role_required("admin")),
):
    if id_usuario == current_user.id:
        if user_data.ativo is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nao e possivel inativar o proprio usuario.",
            )
        if user_data.role and user_data.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nao e possivel remover o proprio perfil de admin.",
            )

    password_hash = hash_password(user_data.senha) if user_data.senha else None
    updated = update_user(id_usuario, user_data, password_hash=password_hash)
    write_audit_log(
        current_user,
        action="user.update",
        resource_type="user",
        resource_id=id_usuario,
        metadata={
            "target_email": updated.get("email"),
            "target_role": updated.get("role"),
            "target_active": updated.get("ativo"),
        },
    )
    return updated
