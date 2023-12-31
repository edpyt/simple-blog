from typing import AsyncGenerator

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from src.core.utils.auth import authenticate_user, create_access_token
from src.domain.blog.dto.user import CreateUserDTO
from src.domain.blog.services.user import UserService
from src.infrastructure.db.dao.user import UserDAO
from src.infrastructure.db.holder import Holder
from src.infrastructure.db.main import build_session, create_engine
from src.infrastructure.db.models import Base, Post  # noqa: F401
from src.infrastructure.db.models.user import User  # noqa: F401
from src.main import app
from tests.setup import get_test_db_url, setup_test_di


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
    async with AsyncClient(
        app=app_, base_url='http://test'
    ) as async_client, LifespanManager(app_):
        yield async_client


@pytest_asyncio.fixture(name='test_client_authenticated')
async def get_authenticated_test_client(
    app_: FastAPI, user_service: UserService, created_user: User
) -> AsyncGenerator[AsyncClient, None]:
    # TODO: Add authenticated client
    authenticated_user = await authenticate_user(
        user_service, created_user.username, 'testpass123'
    )
    access_token = create_access_token(
        data={'sub': authenticated_user.username}  # type: ignore
    )
    async with AsyncClient(
        app=app_,
        base_url='http://test',
        headers={'Authorization': f'Bearer {access_token}'}
    ) as async_client, LifespanManager(app_):

        yield async_client


@pytest.fixture(name='holder_dao')
def get_holder_dao(db_session: AsyncSession) -> Holder:
    return Holder(db_session)


# User service
@pytest.fixture(name='user_dao')
def get_user_dao(holder_dao: Holder) -> UserDAO:
    return holder_dao.user


@pytest.fixture(name='user_service')
def get_user_service(user_dao: UserDAO) -> UserService:
    return UserService(user_dao=user_dao)


@pytest_asyncio.fixture(name='created_user')
async def create_user(user_service: UserService) -> User:
    user_dto = CreateUserDTO(username='test', password='testpass123')
    created_user = await user_service.create_user(user_dto)
    return created_user
