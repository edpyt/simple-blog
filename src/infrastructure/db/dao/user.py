from typing import Any, Sequence

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.interfaces import ORMOption

from src.domain.blog.dto.user import CreateUserDTO
from src.domain.blog.exceptions.user import UserWithThisUserNameExists
from src.infrastructure.db.dao.base import BaseDAO
from src.infrastructure.db.models.user import User


class UserDAO(BaseDAO):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(User, session)

    async def create_user(self, user_dto: CreateUserDTO) -> User:
        """
        Create user method

        :param user_dto: User create DTO
        :return: User object
        """
        create_user = User(
            username=user_dto.username,
            password=user_dto.password
        )
        try:
            return await self._create(create_user)
        except IntegrityError:
            raise UserWithThisUserNameExists

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

    async def get_user(self, *options: Sequence[ORMOption]) -> User:
        """
        Get single user object

        :param options: SQLAlchemy ORMOption`s parameters
        :return: User object
        """
        return await self._get_one(options)
