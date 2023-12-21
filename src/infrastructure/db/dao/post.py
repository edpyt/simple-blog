from typing import Optional, Sequence
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.interfaces import ORMOption

from src.domain.blog.dto.post import UpdatePostDTO
from src.infrastructure.db.dao.base import BaseDAO
from src.infrastructure.db.models.post import Post


class PostDAO(BaseDAO):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Post, session)

    async def create_post(self, create_post: Post) -> Post:
        """Create post method

        :param create_post: SqlAlchemy Model object `Post`
        :return: Post object
        """
        return await self._create(create_post)

    async def get_posts(self, *options: Sequence[ORMOption]) -> Sequence[Post]:
        """Get posts

        :param options: Optional param of SQLAlchemy options

        :return: list `Post`
        """
        return await self._get_all(options)

    async def get_post(self, *options: Sequence[ORMOption]) -> Optional[Post]:
        """Get single post

        :param options: Optional param of SQLAlchemy options

        :return: `Post` or None
        """
        return await self._get_one(options)

    async def update_post(
        self, post_uuid: UUID | str, update_post_dto: UpdatePostDTO
    ) -> Post:
        """Update post

        :param update_post_dto: Update `Post` DTO

        :return: `Post` SQLAlchemy object
        """
        await self._update(
            'uuid',
            post_uuid,
            **update_post_dto.model_dump(exclude_none=True)
        )
        return await self.get_post(Post.uuid == post_uuid)  # type: ignore

    async def delete_post(self, post_uuid: UUID | str) -> None:
        """Delete post

        :param post_uuid: UUID of `Post`
        """
        await self._delete([Post.uuid == post_uuid])

    async def refresh_post(self, post: Post) -> Post:
        """Refresh post

        :param post: Post SQLAlchemy object

        :return: Post SQLAlchemy object
        """
        return await self._refresh_object(post)
