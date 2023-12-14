import os
from typing import AsyncGenerator, Optional

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.infrastructure.db.uow import UnitOfWork


def get_db_url() -> Optional[str]:
    return os.environ.get('DATABASE_URL')


class DataBaseProvider:
    def __init__(self, pool: async_sessionmaker[AsyncSession]) -> None:
        self.pool = pool

    async def provide_db(self) -> AsyncGenerator[UnitOfWork, None]:
        async with self.pool() as session:
            yield session


def uow_provider():
    ...
