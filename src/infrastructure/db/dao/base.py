from typing import Generic, Optional, Sequence, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.interfaces import ORMOption

from src.infrastructure.db.models.base import Base
from src.infrastructure.db.models.user import User

Model = TypeVar("Model", bound=Base)


class BaseDAO(Generic[Model]):
    def __init__(self, model: Type[Model], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def _get_all(
        self, options: Sequence[ORMOption] = tuple()
    ) -> Sequence[Model]:
        """
        Get all rows from db

        :return: Sequence of SQLAlchemy models
        """
        stmt = select(self.model).where(*options)
        result = (await self.session.execute(stmt)).scalars().all()
        return result

    async def _get_one(self, options: Sequence[ORMOption]) -> Optional[User]:
        """
        Get one or none object from db

        :param kwargs: Filter object keys
        :return: Object or None
        """
        stmt = select(self.model).where(*options)
        result = (await self.session.execute(stmt)).scalar_one_or_none()
        return result

    async def _create(self, create_model: Model) -> Model:
        """
        Create new row and retrieve instance

        :param create_model: SQLAlchemy model
        :return: Created SQLAlchemy model
        """
        self.session.add(create_model)
        await self.session.flush()
        return create_model
