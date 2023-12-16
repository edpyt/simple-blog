import pytest
from src.core.utils.password import verify_password

from src.domain.blog.dto.user import CreateUserDTO


@pytest.mark.asyncio
async def test_user_dto_create() -> None:
    user = CreateUserDTO(username='test', password='test')

    assert user.username == 'test'
    assert verify_password('test', user.password)
