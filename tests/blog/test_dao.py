from datetime import date
import pytest

from src.infrastructure.db.dao.post import PostDAO
from src.infrastructure.db.models.post import Post
from src.infrastructure.db.models.user import User


@pytest.mark.asyncio
async def test_create_post(post_dao: PostDAO, created_user: User) -> None:
    create_post = Post(title='hello', body='world', created_by=created_user)

    created_post = await post_dao.create_post(create_post)

    assert created_post.title == 'hello'
    assert created_post.body == 'world'
    assert created_post.created_at.date() == date.today()
    assert create_post.created_by == created_user
