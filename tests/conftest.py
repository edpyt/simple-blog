from typing import AsyncGenerator
from fastapi import FastAPI
import pytest_asyncio
from httpx import AsyncClient

from src.main import build_app


@pytest_asyncio.fixture(name='app_')
async def get_app() -> FastAPI:
    return build_app()


@pytest_asyncio.fixture(name='test_client')
async def get_test_client(app_) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        app=app_, base_url='http://localhost:8000'
    ) as async_client:
        yield async_client
