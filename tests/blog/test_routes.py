from httpx import AsyncClient
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.blog.dto.post import PostDTO
from src.infrastructure.db.models.post import Post


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
    response = await test_client.post('/post/create/', json=create_post_data)

    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}


@pytest.mark.asyncio
async def test_get_all_posts(test_client_authenticated: AsyncClient) -> None:
    """Test get all posts"""
    response = await test_client_authenticated.get('/post/all')

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_one_post(
    test_client_authenticated: AsyncClient, created_post: Post
) -> None:
    """Test get one post"""
    response = await test_client_authenticated.get(f'/post/{created_post.uuid}')

    assert response.status_code == 200

    post_serialized = (
        PostDTO
        .model_validate(created_post)
        .model_dump(mode='json')
    )

    assert response.json() == post_serialized


@pytest.mark.asyncio
async def test_update_post(
    test_client_authenticated: AsyncClient,
    created_post: Post,
    db_session: AsyncSession
) -> None:
    """Test update post"""
    await test_client_authenticated.put(
        f'/post/{created_post.uuid}',
        json={'title': 'Hello world'}
    )
    await db_session.refresh(created_post)

    assert created_post.title == 'Hello world'


@pytest.mark.asyncio
async def test_delete_post(
    test_client_authenticated: AsyncClient,
    created_post: Post
) -> None:
    """Test delete post"""
    response = await test_client_authenticated.delete(
        f'/post/{created_post.uuid}'
    )

    assert response.status_code == 200
    assert response.json() == {'is_deleted': True}
