from datetime import datetime
from uuid import UUID

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import DBAPIError, IntegrityError

from src.infrastructure.db.models.post import Post


@pytest.mark.asyncio
async def test_valid_create_post(db_session: AsyncSession) -> None:
    """Test right create post"""
    new_post = Post(title='hi', body='hello')
    db_session.add(new_post)

    await db_session.commit()  # Should not raise error
    await db_session.refresh(new_post)


@pytest.mark.asyncio
@pytest.mark.parametrize('title,body', [
    (None, None),
    ('', None),
    (None, ''),
    (1, 2),
    (2312.123, 321321.4444)
])
async def test_bad_create_post(
    db_session: AsyncSession,
    title: int | float | None,
    body: int | float | None
) -> None:
    """Test not valid create post"""
    new_post = Post(title=title, body=body)
    db_session.add(new_post)

    with pytest.raises((DBAPIError, IntegrityError)):
        await db_session.commit()


@pytest.mark.asyncio
async def test_get_posts(db_session: AsyncSession) -> None:
    """Test retrieve posts"""
    posts = list(await db_session.execute(select(Post)))

    assert len(posts) == 0


@pytest.mark.asyncio
async def test_created_posts_have_unique_uuids(
    db_session: AsyncSession
) -> None:
    """Test created posts uniques"""
    created_post_first = Post(title='sda', body='dev')
    created_post_second = Post(title='sda', body='dev')

    db_session.add_all([created_post_first, created_post_second])
    await db_session.commit()

    assert created_post_first.uuid != created_post_second.uuid


@pytest.mark.asyncio
async def test_created_post_fields(
    db_session: AsyncSession
) -> None:
    """Test created post fields"""
    post_create_title = 'My First Post'
    post_create_body = 'Only here i can be what i want!'
    new_post = Post(title=post_create_title, body=post_create_body)
    db_session.add(new_post)
    await db_session.commit()
    await db_session.refresh(new_post)

    assert isinstance(new_post.uuid, UUID)
    assert isinstance(new_post.created_at, datetime)
    assert new_post.title == post_create_title
    assert new_post.body == post_create_body
