from fastapi import FastAPI

from src.api.di.providers.db import get_db_url
from src.api.routes import blog
from src.infrastructure.db.main import create_engine


def build_app() -> FastAPI:
    app = FastAPI()

    create_engine(get_db_url())

    app.include_router(blog.router)

    return app
