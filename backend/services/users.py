from fastapi import HTTPException, status

from backend.core.config import Role
from backend.database.supabase import get_supabase_client
from backend.schemas.users import UserCreate, UserUpdate


def find_user_by_email(email: str):
    response = (
        get_supabase_client().table("users").select("*").eq("email", email).execute()
    )
    return response.data[0] if response.data else None


def create_user(
    *,
    email: str,
    password_hash: str,
    role: Role,
    nome: str | None = None,
    ativo: bool = True,
):
    data = {
        "email": email,
        "password_hash": password_hash,
        "role": role,
        "nome": nome,
        "ativo": ativo,
    }
    response = get_supabase_client().table("users").insert(data).execute()
    return response.data[0] if response.data else None


def list_users(
    *,
    limit: int = 20,
    offset: int = 0,
    search: str | None = None,
    role: Role | None = None,
    ativo: bool | None = None,
):
    query = get_supabase_client().table("users").select(_public_fields())

    if search:
        query = query.ilike("email", f"%{search.strip().lower()}%")
    if role:
        query = query.eq("role", role)
    if ativo is not None:
        query = query.eq("ativo", ativo)

    response = query.order("created_at", desc=True).range(offset, offset + limit - 1).execute()
    return response.data


def list_active_doctors():
    response = (
        get_supabase_client()
        .table("users")
        .select(_public_fields())
        .eq("role", "medico")
        .eq("ativo", True)
        .order("nome")
        .execute()
    )
    return response.data


def get_user(id_usuario: str):
    response = (
        get_supabase_client()
        .table("users")
        .select(_public_fields())
        .eq("id", id_usuario)
        .execute()
    )
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario nao encontrado.",
        )
    return response.data[0]


def create_managed_user(user: UserCreate, *, password_hash: str):
    if find_user_by_email(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail ja cadastrado.",
        )
    created = create_user(
        email=user.email,
        password_hash=password_hash,
        role=user.role,
        nome=user.nome,
        ativo=user.ativo,
    )
    return _without_password(created)


def update_user(id_usuario: str, user: UserUpdate, *, password_hash: str | None = None):
    data = user.model_dump(exclude_unset=True, exclude_none=True)
    if password_hash:
        data["password_hash"] = password_hash
    data.pop("senha", None)

    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nenhum campo informado para atualizacao.",
        )

    if "email" in data:
        existing = find_user_by_email(data["email"])
        if existing and existing["id"] != id_usuario:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="E-mail ja cadastrado.",
            )

    response = (
        get_supabase_client()
        .table("users")
        .update(data)
        .eq("id", id_usuario)
        .execute()
    )
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario nao encontrado.",
        )
    return _without_password(response.data[0])


def _public_fields() -> str:
    return "id,email,role,nome,ativo,created_at,updated_at"


def _without_password(user: dict | None):
    if not user:
        return user
    return {key: value for key, value in user.items() if key != "password_hash"}
