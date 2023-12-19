from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.interfaces import ORMOption

from src.infrastructure.db.dao.base import BaseDAO
from src.infrastructure.db.models.post import Post


class PostDAO(BaseDAO):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Post, session)

    async def create_post(self, create_post: Post) -> Post:
        """
        Create post method

        :param create_post: SqlAlchemy Model object `Post`
        :return: Post object
        """
        return await self._create(create_post)

    async def get_posts(self, *options: Sequence[ORMOption]) -> Sequence[Post]:
        """
        Get posts

        :param options: Optional param of SQLAlchemy options
        :return: list `Post`
        """
        return await self._get_all(options)
