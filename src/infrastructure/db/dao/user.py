from typing import Optional, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.interfaces import ORMOption

from src.infrastructure.db.dao.base import BaseDAO
from src.infrastructure.db.models.user import User


class UserDAO(BaseDAO):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(User, session)

    async def create_user(self, create_user: User) -> User:
        """
        Create user method

        :param user_dto: User create DTO
        :return: User object
        """
        return await self._create(create_user)

    async def get_all_users(self) -> Sequence[User]:
        """
        Get all users objects

        :return: Sequence of User objects
        """
        return await self._get_all()

    async def get_filtered_users(
        self, *options: Sequence[ORMOption]
    ) -> Sequence[User]:
        """
        Get filtered users objects

        :param options: SQLAlchemy ORMOption`s parameters
        :return: Sequence of User objects
        """
        return await self._get_all(options)

    async def get_user(self, *options: Sequence[ORMOption]) -> Optional[User]:
        """
        Get single user object

        :param options: SQLAlchemy ORMOption`s parameters
        :return: User object
        """
        return await self._get_one(options)
