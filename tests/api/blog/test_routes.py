from fastapi.testclient import TestClient
import pytest


@pytest.mark.asyncio
async def test_get_main_route(test_client: TestClient) -> None:
    response = await test_client.get('/')
    
    assert response.status_code == 200