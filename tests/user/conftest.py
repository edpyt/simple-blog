import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.utils.auth import create_access_token
from src.domain.blog.dto.user import CreateUserDTO
from src.infrastructure.db.dao.user import UserDAO
from src.infrastructure.db.models.user import User


@pytest.fixture(name='user_dao')
def get_user_dao(db_session: AsyncSession) -> UserDAO:
    return UserDAO(db_session)


@pytest_asyncio.fixture(name='created_user')
async def create_user(user_dao: UserDAO) -> User:
    user_dto = CreateUserDTO(username='test', password='testpass123')
    created_user = await user_dao.create_user(user_dto)
    return created_user


@pytest.fixture(name='created_token')
def get_created_token(created_user: User) -> str:
    return create_access_token(data={'sub': created_user.username})
