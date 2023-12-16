import asyncio
from typing import AsyncGenerator

from fastapi import FastAPI
from httpx import AsyncClient
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from src.infrastructure.db.main import build_session, create_engine
from src.infrastructure.db.models import Base, Post  # noqa: F401
from src.main import app
from tests.setup import get_test_db_url, setup_test_di


@pytest.fixture(scope="module")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.SelectorEventLoop()
    yield loop
    loop.close()


@pytest.fixture(name='db_engine')
def get_db_engine() -> AsyncEngine:
    db_url: str = get_test_db_url()
    return create_engine(db_url)


@pytest_asyncio.fixture(name='tables')
async def create_drop_tables(
    db_engine: AsyncEngine,
) -> AsyncGenerator[None, None]:
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(name='db_session')
async def get_db_session(
    db_engine: AsyncEngine, tables: None
) -> AsyncGenerator[AsyncSession, None]:
    session_ = build_session(db_engine)
    async with session_() as session:
        yield session


@pytest_asyncio.fixture(name='app_')
async def get_app(db_session: AsyncSession) -> FastAPI:
    setup_test_di(app, db_session)
    return app


@pytest_asyncio.fixture(name='test_client')
async def get_test_client(app_: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app_, base_url='http://test') as async_client:
        yield async_client
