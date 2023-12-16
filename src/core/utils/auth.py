from datetime import datetime, timedelta
import os
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.di.providers.db import db_provider
from src.domain.blog.dto.user import CreateUserDTO

from src.infrastructure.db.models.user import User

SECRET_KEY = os.environ.get('SECRET_KEY', '39ed72383e')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def get_user(db_session: AsyncSession, username: str) -> Optional[User]:
    # TODO: Use DAO here
    user_get_query = select(User).where(User.username == username)
    user = (await db_session.execute(user_get_query)).one_or_none()
    if user:
        user = user[0]
    return user


async def authenticate_user(
    db_session: AsyncSession, username: str, password: str
) -> bool | User:
    user = await get_user(db_session, username=username)
    if not user or not verify_password(password, user.password):
        return False
    return user


async def register_user(
    db_session: AsyncSession, create_user_dto: CreateUserDTO
) -> bool:
    username, password = create_user_dto.username, create_user_dto.password
    if await get_user(db_session, username):
        raise HTTPException(403, 'User with this username already created!')
    hashed_password = get_password_hash(password)
    # TODO: Use DAO here
    user = User(username=username, password=hashed_password)
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return True


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
    db_session: Annotated[AsyncSession, Depends(db_provider)]
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
    user = await get_user(db_session, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    print(current_user)
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
