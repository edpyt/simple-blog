import os

from fastapi import FastAPI

from src.api.di.providers.db import db_provider, get_db_url


def get_test_db_url() -> str:
    db_url = os.environ['TEST_DATABASE_URL']
    return db_url


def setup_test_di(app: FastAPI, db_session) -> None:
    app.dependency_overrides[get_db_url] = get_test_db_url()
    app.dependency_overrides[db_provider] = db_session
