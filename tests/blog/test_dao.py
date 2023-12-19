from datetime import date
import pytest

from src.infrastructure.db.dao.post import PostDAO
from src.infrastructure.db.models.post import Post


@pytest.mark.asyncio
async def test_create_post(post_dao: PostDAO) -> None:
    create_post = Post(title='hello', body='world')

    created_post = await post_dao.create_post(create_post)

    assert created_post.title == 'hello'
    assert created_post.body == 'world'
    assert created_post.created_at.date() == date.today()
