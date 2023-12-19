from httpx import AsyncClient
import pytest

from src.domain.blog.dto.post import PostDTO


@pytest.mark.asyncio
async def test_get_today_posts_route(
    test_client: AsyncClient, created_post_dto: PostDTO
) -> None:
    """Test get today posts"""
    response = await test_client.get('/post/')

    assert response.status_code == 200
    assert response.json() == [created_post_dto.model_dump(mode='json')]


# @pytest.mark.asyncio
# async def test_create_post_by_user(
#     test_client: AsyncClient
# )
