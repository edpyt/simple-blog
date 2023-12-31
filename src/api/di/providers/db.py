import os
from typing import AsyncGenerator, Optional

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


def get_db_url() -> Optional[str]:
    db_url: Optional[str] = os.environ['DATABASE_URL']
    return db_url


class DataBaseProvider:
    def __init__(self, pool: async_sessionmaker[AsyncSession]) -> None:
        self.pool = pool

    async def provide_db(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.pool() as session:
            yield session


def db_provider() -> AsyncSession:
    ...
