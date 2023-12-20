from typing import Any

from fastapi import HTTPException
from pydantic import ValidationError
import pytest

from src.core.utils.auth import (
    authenticate_user,
    get_current_user,
    register_user,
)
from src.domain.blog.dto.user import CreateUserDTO
from src.domain.blog.services.user import UserService
from src.infrastructure.db.models.user import User


@pytest.mark.asyncio
async def test_valid_register_user(user_service: UserService) -> None:
    """Test create user with hashed password"""
    new_user = CreateUserDTO(username='test', password='testpass123')

    await register_user(user_service, new_user)

    assert len(await user_service.get_all_users()) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'username,password',
    [
        (12321, 3321),
        (123.12, b'dsa'),
    ],
)
async def test_not_valid_register_user(
    user_service: UserService, username: Any, password: Any
) -> None:
    """Test pydantic validate data"""
    with pytest.raises(ValidationError):
        new_user = CreateUserDTO(username=username, password=password)

        await register_user(user_service, new_user)


@pytest.mark.asyncio
async def test_cant_create_two_users_with_same_username(
    user_service: UserService,
) -> None:
    """Test cant create user with same username"""
    user_twin_one = CreateUserDTO(username='twin', password='imtwin')
    user_twin_two = CreateUserDTO(username='twin', password='noimtwin')

    await register_user(user_service, user_twin_one)
    with pytest.raises(HTTPException, match='User with this username exists!'):
        await register_user(user_service, user_twin_two)


@pytest.mark.asyncio
async def test_authenticate_user(
    user_service: UserService, created_user: User
) -> None:
    """Test created user authentication"""
    user = await authenticate_user(
        user_service, created_user.username, 'testpass123'
    )

    assert isinstance(user, User)
    assert user.username == created_user.username


@pytest.mark.asyncio
async def test_get_current_user(
    user_service: UserService, created_user: User, created_token: str
) -> None:
    """Test get current(created) user by created token"""
    user = await get_current_user(
        created_token, user_service
    )  # Should not raise error

    assert user.username == created_user.username
