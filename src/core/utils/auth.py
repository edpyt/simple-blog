from datetime import datetime, timedelta
import os
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.di.providers.db import db_provider
from src.api.di.providers.holder import user_dao
from src.core.utils.password import verify_password
from src.domain.blog.dto.user import CreateUserDTO
from src.domain.blog.exceptions.user import UserWithThisUserNameExists
from src.infrastructure.db.dao.user import UserDAO

from src.infrastructure.db.models.user import User

SECRET_KEY = os.environ['SECRET_KEY']
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


async def authenticate_user(
    user_dao: UserDAO, username: str, password: str
) -> bool | User:
    """
    Authenticate user

    :param user_dao: User DAO object
    :param username: Username
    :param password: Password

    :return: If user not created return False, else User object
    """
    user = await user_dao.get_user(User.username == username)
    if not user or not verify_password(password, user.password):
        return False
    return user


async def register_user(
    user_dao: UserDAO, create_user_dto: CreateUserDTO
) -> None:
    """
    Create user, if user with provided username exists throw HTTPException

    :param user_dao: User DAO object
    :param create_user_dto: Create User DTO object
    """
    try:
        await user_dao.create_user(create_user_dto)
    except UserWithThisUserNameExists as e:
        raise HTTPException(403, e.error_msg)


def create_access_token(
    data: dict, expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_dao: Annotated[UserDAO, Depends(user_dao)]
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await user_dao.get_user(User.username == token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
