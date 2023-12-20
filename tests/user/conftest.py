import pytest

from src.core.utils.auth import create_access_token
from src.infrastructure.db.models.user import User


@pytest.fixture(name='created_token')
def get_created_token(created_user: User) -> str:
    return create_access_token(data={'sub': created_user.username})
