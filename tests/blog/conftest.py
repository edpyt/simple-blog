from datetime import datetime, timedelta

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.blog.dto.post import CreatePostDTO, PostDTO
from src.domain.blog.services.post import PostService
from src.infrastructure.db.dao.post import PostDAO
from src.infrastructure.db.holder import Holder
from src.infrastructure.db.models.post import Post


@pytest_asyncio.fixture(name='post_dao')
async def get_post_dao(holder_dao: Holder) -> PostDAO:
    return holder_dao.post


@pytest_asyncio.fixture(name='post_service')
async def get_post_service(post_dao: PostDAO) -> PostService:
    return PostService(post_dao=post_dao)


@pytest_asyncio.fixture(name='created_post')
async def create_post(post_service: PostService) -> Post:
    create_post = CreatePostDTO(title='hello', body='world')
    created_post = await post_service.create_post(create_post)
    return created_post


@pytest_asyncio.fixture(name='created_posts')
async def create_posts(
    post_service: PostService, db_session: AsyncSession
) -> list[Post]:
    posts = []
    for i in range(10):
        dt = datetime.now() - timedelta(days=i)
        for _ in range(10):
            create_post = CreatePostDTO(title='hello', body='world')
            created_post = await post_service.create_post(create_post)
            created_post.created_at = dt
            await db_session.commit()
            posts.append(created_post)
    return posts


@pytest_asyncio.fixture(name='created_post_dto')
async def get_created_post_dto(created_post: Post) -> PostDTO:
    return PostDTO(
        uuid=created_post.uuid,
        title=created_post.title,
        body=created_post.body,
        created_at=created_post.created_at,
    )
