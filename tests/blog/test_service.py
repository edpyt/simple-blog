from datetime import date

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.blog.dto.post import CreatePostDTO, PostDTO, UpdatePostDTO
from src.domain.blog.services.post import PostService
from src.infrastructure.db.models.post import Post
from src.infrastructure.db.models.user import User


@pytest.mark.asyncio
async def test_create_post(
    post_service: PostService, created_user: User
) -> None:
    """Test creating post"""
    create_post = CreatePostDTO(title='hello', body='world')

    created_post = await post_service.create_post(create_post, created_user)

    assert created_post.title == 'hello'
    assert created_post.body == 'world'
    assert created_post.created_at.date() == date.today()


@pytest.mark.asyncio
async def test_get_post(
    post_service: PostService, created_post: Post
) -> None:
    post = await post_service.get_post_by_uuid(post_uuid=created_post.uuid)

    assert post == PostDTO.model_validate(created_post)


@pytest.mark.asyncio
async def test_update_post(
    post_service: PostService,
    db_session: AsyncSession,
    created_post: Post,
) -> None:
    """Test update post"""
    update_post_dto = UpdatePostDTO.model_validate(created_post)
    update_post_dto.title = 'Hello world'

    await post_service.update_post(created_post.uuid, update_post_dto)
    await db_session.refresh(created_post)

    assert created_post.title == 'Hello world'
