from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from src.api.di import setup_di
from src.api.di.providers.db import get_db_url
from src.api.routes import blog, user
from src.infrastructure.db.main import build_session, create_engine


@asynccontextmanager
async def setup_dependencies(app: FastAPI) -> AsyncGenerator[None, None]:
    if not app.dependency_overrides.get(get_db_url):
        app.dependency_overrides[get_db_url] = get_db_url()
    db_url = app.dependency_overrides[get_db_url]
    db_engine = create_engine(db_url)  # type: ignore
    session = build_session(db_engine)
    setup_di(app, session)
    yield


app = FastAPI(lifespan=setup_dependencies)

app.include_router(blog.router)
app.include_router(user.router)
