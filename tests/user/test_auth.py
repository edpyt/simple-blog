from typing import Any
from fastapi import HTTPException
from pydantic import ValidationError
import pytest

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.utils.auth import register_user
from src.domain.blog.dto.user import CreateUserDTO
from src.infrastructure.db.models.user import User


@pytest.mark.asyncio
async def test_valid_register_user(db_session: AsyncSession) -> None:
    """Test create user with hashed password"""
    new_user = CreateUserDTO(username='test', password='testpass123')

    is_created = await register_user(db_session, new_user)

    assert is_created
    assert (await db_session.execute(select(User))).one_or_none()


@pytest.mark.asyncio
@pytest.mark.parametrize('username,password', [
    (12321, 3321),
    (123.12, b'dsa'),
])
async def test_not_valid_register_user(
    db_session: AsyncSession, username: Any, password: Any
) -> None:
    """Test pydantic works well"""
    with pytest.raises(ValidationError):
        new_user = CreateUserDTO(username=username, password=password)

        is_created = await register_user(db_session, new_user)

        assert not is_created


@pytest.mark.asyncio
async def test_cant_create_two_users_with_same_username(
    db_session: AsyncSession
) -> None:
    """Test cant create user with same username"""
    user_twin_one = CreateUserDTO(username='twin', password='imtwin')
    user_twin_two = CreateUserDTO(username='twin', password='noimtwin')

    await register_user(db_session, user_twin_one)
    with pytest.raises(
        HTTPException, match='User with this username already created!'
    ):
        await register_user(db_session, user_twin_two)
