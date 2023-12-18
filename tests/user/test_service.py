import pytest
from src.domain.blog.dto.user import CreateUserDTO

from src.domain.blog.services.user import UserService
from src.infrastructure.db.models.user import User


@pytest.mark.asyncio
async def test_get_empty_users(user_service: UserService) -> None:
    """Test get users"""
    users = await user_service.get_all_users()

    assert users == []


@pytest.mark.asyncio
async def test_get_users_with_created_user(
    user_service: UserService, created_user: User
) -> None:
    """Test get users with created user fixture"""
    users = await user_service.get_all_users()

    assert users == [created_user]


@pytest.mark.asyncio
@pytest.mark.parametrize('search_field', ['username', 'uuid'])
async def test_get_created_user(
    user_service: UserService, created_user: User, search_field: str
) -> None:
    """Test get created user from db"""
    user = await user_service.get_user(
        getattr(User, search_field) == getattr(created_user, search_field)
    )

    assert user == created_user


@pytest.mark.asyncio
async def test_invalid_get_user(user_service: UserService) -> None:
    """Test trying to get user"""
    user = await user_service.get_user(User.username == 'im not here')

    assert user is None


@pytest.mark.asyncio
async def test_get_filtered_users(user_service: UserService) -> None:
    """Test get list users filtered by some fields"""
    users = await user_service.filter_users(User.username == 'notcreateduser')

    assert users == []


@pytest.mark.asyncio
async def test_create_user(user_service: UserService) -> None:
    """Test create user"""
    create_user = CreateUserDTO(username='testuser1', password='testpass123')

    user = await user_service.create_user(create_user)
    users = await user_service.get_all_users()

    assert user
    assert user in users
