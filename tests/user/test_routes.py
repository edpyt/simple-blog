from httpx import AsyncClient
import pytest

from src.infrastructure.db.models import User


@pytest.mark.asyncio
async def test_get_token(
    test_client: AsyncClient, user_service, created_user: User
) -> None:
    """Test get token from api"""
    response = await test_client.post(
        '/token',
        data={'username': created_user.username, 'password': 'testpass123'},
    )
    print(response)
