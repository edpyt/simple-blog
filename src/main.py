from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from src.api.di import setup_di
from src.api.di.providers.db import get_db_url
from src.api.routes import blog
from src.infrastructure.db.main import build_session, create_engine


app = FastAPI()


@asynccontextmanager
async def setup_dependencies(app: FastAPI) -> AsyncGenerator[None, None]:
    db_engine = create_engine(get_db_url())  # type: ignore
    setup_di(app, build_session(db_engine))
    yield


app.include_router(blog.router)
