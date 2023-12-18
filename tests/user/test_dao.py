import pytest

from sqlalchemy.exc import IntegrityError

from src.infrastructure.db.dao import UserDAO
from src.infrastructure.db.models.user import User


@pytest.mark.asyncio
async def test_create_user(user_dao: UserDAO) -> None:
    """Test can create user in DAO"""
    create_user = User(username='testuser123', password='not_hashed_password')

    created_user = await user_dao.create_user(create_user)

    assert created_user.username == 'testuser123'
    assert created_user.password == 'not_hashed_password'


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
    user: User = await user_dao.get_user(  # type: ignore
        User.username == created_user.username
    )

    assert user.username == created_user.username
    assert user.password == created_user.password


@pytest.mark.asyncio
async def test_cant_create_user_with_same_username(
    user_dao: UserDAO, created_user: User
) -> None:
    """Test can't create user with the same usernames"""
    with pytest.raises(IntegrityError):
        create_user = User(
            username=created_user.username, password='testpass123'
        )
        await user_dao.create_user(create_user)
