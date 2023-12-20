from datetime import date
import pytest
from src.domain.blog.dto.post import CreatePostDTO

from src.domain.blog.services.post import PostService
from src.infrastructure.db.models.user import User


@pytest.mark.asyncio
async def test_create_post(
    post_service: PostService, created_user: User
) -> None:
    """Test creating posts via `PostService`"""
    create_post = CreatePostDTO(title='hello', body='world')

    created_post = await post_service.create_post(create_post, created_user)

    assert created_post.title == 'hello'
    assert created_post.body == 'world'
    assert created_post.created_at.date() == date.today()
