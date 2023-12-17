import pytest

from src.core.utils.password import verify_password
from src.domain.blog.dto.user import CreateUserDTO
from src.domain.blog.exceptions.user import UserWithThisUserNameExists
from src.infrastructure.db.dao import UserDAO
from src.infrastructure.db.models.user import User


@pytest.mark.asyncio
async def test_create_user(user_dao: UserDAO) -> None:
    """Test can create user in DAO"""
    user_dto = CreateUserDTO(username='testuser', password='testpass123')

    created_user = await user_dao.create_user(user_dto)

    assert created_user.username == 'testuser'
    assert created_user.password != 'testpass123'
    assert verify_password('testpass123', created_user.password)


@pytest.mark.asyncio
async def test_get_all_users(user_dao: UserDAO, created_user: User) -> None:
    users = await user_dao.get_all_users()

    assert created_user in users


@pytest.mark.asyncio
async def test_get_filtered_users(
    user_dao: UserDAO, created_user: User
) -> None:
    """Test get filtered users"""
    filtered_users = await user_dao.get_filtered_users(
        User.username == created_user.username
    )

    assert created_user in filtered_users


@pytest.mark.asyncio
async def test_get_user_by_username(
    user_dao: UserDAO, created_user: User
) -> None:
    """Test get user by username in DAO"""
    user: User = await user_dao.get_user(User.username == created_user.username)

    assert user.username == created_user.username
    assert user.password == created_user.password


@pytest.mark.asyncio
async def test_cant_create_user_with_same_username(
    user_dao: UserDAO, created_user: User
) -> None:
    """Test can't create user with the same usernames"""
    with pytest.raises(UserWithThisUserNameExists):
        create_user_dto = CreateUserDTO(
            username=created_user.username, password='testpass123'
        )
        await user_dao.create_user(create_user_dto)
