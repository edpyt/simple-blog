import os
from fastapi import FastAPI

from src.api.di.providers.db import get_db_url
from src.api.routes import blog
from src.infrastructure.db.main import create_engine
from src.infrastructure.db.models.base import Base


def build_app() -> FastAPI:
    app = FastAPI()

    db_engine = create_engine(get_db_url())
    
    app.include_router(blog.router)

    return app
