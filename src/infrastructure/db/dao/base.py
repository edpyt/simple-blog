from typing import Any, Generic, Optional, Sequence, Type, TypeVar

from sqlalchemy import select, update
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
        """Get all rows from db

        :return: Sequence of SQLAlchemy models
        """
        stmt = select(self.model).where(*options)
        result = (await self.session.execute(stmt)).scalars().all()
        return result

    async def _get_one(self, options: Sequence[ORMOption]) -> Optional[User]:
        """Get one or none object from db

        :param kwargs: Filter object keys
        :return: Object or None
        """
        stmt = select(self.model).where(*options)
        result = (await self.session.execute(stmt)).scalar_one_or_none()
        return result

    async def _create(self, create_model: Model) -> Model:
        """Create new row and retrieve instance

        :param create_model: SQLAlchemy model
        :return: Created SQLAlchemy model
        """
        self.session.add(create_model)
        await self.session.commit()
        return create_model

    async def _delete(self, options: Sequence[ORMOption]) -> None:
        """Delete record from db

        :param search_key: String model field key for search
        :param search_value: Model field value for search
        """
        obj = await self._get_one(options)
        await self.session.delete(obj)

    async def _update(
        self,
        search_key: str,
        search_value: Any,
        **update_data
    ) -> None:
        stmt = (
            update(self.model)
            .where(getattr(self.model, search_key) == search_value)
            .values(**update_data)
        )
        await self.session.execute(stmt)

    async def _refresh_object(self, model: Model) -> Model:
        await self.session.refresh(model)
        return model
