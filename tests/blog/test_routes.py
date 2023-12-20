from httpx import AsyncClient
import pytest

from src.domain.blog.dto.post import PostDTO


@pytest.mark.asyncio
async def test_get_today_posts_route(
    test_client_authenticated: AsyncClient, created_post_dto: PostDTO
) -> None:
    """Test get today posts"""
    response = await test_client_authenticated.get('/post/')

    assert response.status_code == 200
    assert response.json() == [created_post_dto.model_dump(mode='json')]


@pytest.mark.asyncio
async def test_create_post_by_user(
    test_client_authenticated: AsyncClient
) -> None:
    """Test create post"""
    create_post_data = {
        'title': 'My first post', 'body': 'First created post!'
    }
    response = await test_client_authenticated.post(
        '/post/create/', json=create_post_data
    )

    assert response.status_code == 200
    assert response.json() == {'status': 'success'}


@pytest.mark.parametrize('invalid_create_post_data', [
    {'title': 1, 'body': 4},
    {'title': None, 'body': 1.2},
    {'title': .1, 'body': 'AHAH'}
])
@pytest.mark.asyncio
async def test_create_post_by_user_invalid(
    test_client_authenticated: AsyncClient,
    invalid_create_post_data: dict
) -> None:
    """Test create post with invalid data"""
    response = await test_client_authenticated.post(
        '/post/create/', json=invalid_create_post_data
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_trying_to_create_post_without_authenticate(
    test_client: AsyncClient
) -> None:
    """Test trying to create post without authenticated"""
    create_post_data = {
        'title': 'My first post', 'body': 'First created post!'
    }
    response = await test_client.post('/post/create', json=create_post_data)

    assert response.status_code == 307
