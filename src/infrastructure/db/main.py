from sqlalchemy.ext.asyncio import (
    AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
)


def create_engine(db_url: str) -> AsyncEngine:
    return create_async_engine(db_url)


def build_session(engine: AsyncEngine) -> AsyncSession:
    return async_sessionmaker(
        bind=engine,
        autoflush=True,
        expire_on_commit=False
    )
