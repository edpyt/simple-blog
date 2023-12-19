import pytest
import pytest_asyncio

from src.core.utils.auth import create_access_token
from src.domain.blog.dto.user import CreateUserDTO
from src.domain.blog.services.user import UserService
from src.infrastructure.db.dao.user import UserDAO
from src.infrastructure.db.holder import Holder
from src.infrastructure.db.models.user import User


@pytest.fixture(name='user_dao')
def get_user_dao(holder_dao: Holder) -> UserDAO:
    return holder_dao.user


@pytest.fixture(name='created_token')
def get_created_token(created_user: User) -> str:
    return create_access_token(data={'sub': created_user.username})


@pytest.fixture(name='user_service')
def get_user_service(user_dao: UserDAO) -> UserService:
    return UserService(user_dao=user_dao)


@pytest_asyncio.fixture(name='created_user')
async def create_user(user_service: UserService) -> User:
    user_dto = CreateUserDTO(username='test', password='testpass123')
    created_user = await user_service.create_user(user_dto)
    return created_user
