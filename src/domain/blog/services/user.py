from typing import Optional

from sqlalchemy import Sequence
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.interfaces import ORMOption
from src.domain.blog.dto.user import CreateUserDTO
from src.domain.blog.exceptions.user import UserWithThisUserNameExists

from src.infrastructure.db.dao.user import UserDAO
from src.infrastructure.db.models.user import User


class UserService:
    def __init__(self, user_dao: UserDAO) -> None:
        self.user_dao = user_dao

    async def get_all_users(self) -> Sequence[User]:
        """Get all users from db"""
        return await self.user_dao.get_all_users()

    async def get_user(self, *options: Sequence[ORMOption]) -> Optional[User]:
        """Get single user filtered by options

        :param options: SQLAlchemy options sequen
        """
        return await self.user_dao.get_user(*options)

    async def filter_users(
        self, *options: Sequence[ORMOption]
    ) -> Sequence[User]:
        """Get filtered users

        :param options: SQLAlchemy options sequen
        """
        return await self.user_dao.get_filtered_users(*options)

    async def create_user(self, create_user_dto: CreateUserDTO) -> User:
        """Create user

        :param create_user_dto: DTO for creating user
        """
        create_user = User(
            username=create_user_dto.username, password=create_user_dto.password
        )
        try:
            return await self.user_dao.create_user(create_user)
        except IntegrityError:
            raise UserWithThisUserNameExists
