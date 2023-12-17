from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.infrastructure.db.dao.user import UserDAO

from src.infrastructure.db.holder import Holder


class HolderProvider:
    def __init__(self, pool: async_sessionmaker) -> None:
        self.pool = pool

    async def provide_holder(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.pool() as session:
            yield Holder(session)


def holder_provider() -> HolderProvider:
    ...


def user_dao() -> UserDAO:
    ...
