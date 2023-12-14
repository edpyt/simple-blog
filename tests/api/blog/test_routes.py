from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_get_main_route(test_client: AsyncClient) -> None:
    response = await test_client.get('/')

    assert response.status_code == 200
