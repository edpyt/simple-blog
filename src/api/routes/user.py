from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src.api.di.providers.service import user_service
from src.core.utils.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    Token,
    authenticate_user,
    create_access_token,
    get_current_active_user,
    register_user,
)
from src.domain.blog.dto.user import CreateUserDTO
from src.domain.blog.services.user import UserService
from src.infrastructure.db.models.user import User

router = APIRouter()


@router.post('/token', response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: UserService = Depends(user_service),
) -> dict[str, str]:
    user = await authenticate_user(
        user_service, form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(403, 'ERROR')
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},  # type: ignore
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/register')
async def create_new_user(
    user_dto: CreateUserDTO, user_service: UserService = Depends(user_service)
) -> dict[str, bool]:
    await register_user(user_service, user_dto)
    return {'is_created': True}


@router.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user
