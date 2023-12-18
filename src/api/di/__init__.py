from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.api.di.providers.db import db_provider, DataBaseProvider
from src.api.di.providers.service import ServiceProvider, user_service


def setup_di(app: FastAPI, pool: async_sessionmaker[AsyncSession]) -> None:
    if not app.dependency_overrides.get(db_provider):
        provider_database = DataBaseProvider(pool)
        app.dependency_overrides[db_provider] = provider_database.provide_db
    
    provider_service = ServiceProvider()
    app.dependency_overrides[
        user_service
    ] = provider_service.provide_user_service
