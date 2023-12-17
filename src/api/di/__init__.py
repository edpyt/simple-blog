from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.api.di.providers.db import db_provider, DataBaseProvider
from src.api.di.providers.holder import (
    HolderProvider,
    holder_provider,
    user_dao,
)


def setup_di(app: FastAPI, pool: async_sessionmaker[AsyncSession]) -> None:
    provider_database = DataBaseProvider(pool)
    provider_holder = HolderProvider(pool)

    app.dependency_overrides[db_provider] = provider_database.provide_db
    app.dependency_overrides[holder_provider] = provider_holder.provide_holder
    app.dependency_overrides[user_dao] = app.dependency_overrides[
        holder_provider
    ].user
