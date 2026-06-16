from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, status

from backend.core.config import Role
from backend.core.security import (
    create_access_token,
    get_current_user,
    hash_password,
    role_required,
    verify_password,
)
from backend.schemas.auth import AuthenticatedUser, TokenResponse
from backend.schemas.common import MessageResponse
from backend.services.users import create_user, find_user_by_email


router = APIRouter()


@router.post("/register", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def register_user(
    email: Annotated[str, Form(min_length=3, max_length=254)],
    senha: Annotated[str, Form(min_length=8, max_length=128)],
    role: Annotated[Role, Form()],
    user: AuthenticatedUser = Depends(role_required("admin")),
):
    normalized_email = email.strip().lower()
    if find_user_by_email(normalized_email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail ja cadastrado.",
        )

    create_user(
        email=normalized_email,
        password_hash=hash_password(senha),
        role=role,
    )
    return MessageResponse(message="Usuario criado com sucesso.")


@router.post("/login", response_model=TokenResponse)
def login(
    email: Annotated[str, Form(min_length=3, max_length=254)],
    senha: Annotated[str, Form(min_length=1, max_length=128)],
):
    normalized_email = email.strip().lower()
    user = find_user_by_email(normalized_email)
    if not user or not user.get("ativo", True) or not verify_password(senha, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Credenciais invalidas.",
        )

    token = create_access_token(
        {"sub": normalized_email, "role": user["role"], "user_id": user["id"]}
    )
    return TokenResponse(access_token=token)


@router.get("/me", response_model=AuthenticatedUser)
def get_me(user: AuthenticatedUser = Depends(get_current_user)):
    return user
