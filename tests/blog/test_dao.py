from datetime import date

import pytest

from src.domain.blog.dto.post import UpdatePostDTO
from src.infrastructure.db.dao.post import PostDAO
from src.infrastructure.db.models.post import Post
from src.infrastructure.db.models.user import User


@pytest.mark.asyncio
async def test_create_post(post_dao: PostDAO, created_user: User) -> None:
    """Test create `Post`"""
    create_post = Post(title='hello', body='world', created_by=created_user)

    created_post = await post_dao.create_post(create_post)

    assert created_post.title == 'hello'
    assert created_post.body == 'world'
    assert created_post.created_at.date() == date.today()
    assert create_post.created_by == created_user


@pytest.mark.asyncio
async def test_get_post(post_dao: PostDAO, created_post: Post) -> None:
    """Test get single `Post`"""
    post = await post_dao.get_post(Post.uuid == created_post.uuid)

    assert post == created_post


@pytest.mark.asyncio
async def test_update_post(post_dao: PostDAO, created_post: Post) -> None:
    """Test update `Post`"""
    update_post_dto = UpdatePostDTO(title='Hello world')

    await post_dao.update_post(created_post.uuid, update_post_dto)
    await post_dao.refresh_post(created_post)

    assert created_post.title == 'Hello world'


@pytest.mark.asyncio
async def test_delete_post(post_dao: PostDAO, created_post: Post) -> None:
    """Test delete `Post` record"""
    await post_dao.delete_post(created_post.uuid)

    assert await post_dao.get_posts() == []
