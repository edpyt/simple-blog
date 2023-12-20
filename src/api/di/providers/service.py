from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.di.providers.db import db_provider

from src.domain.blog.services.user import UserService
from src.domain.blog.services.post import PostService
from src.infrastructure.db.holder import Holder


class ServiceProvider:
    async def provide_user_service(
        self, db_session: Annotated[AsyncSession, Depends(db_provider)]
    ) -> AsyncGenerator[UserService, None]:
        """User service provider method"""
        holder = Holder(db_session)
        yield UserService(holder.user)

    async def provide_post_service(
        self, db_session: Annotated[AsyncSession, Depends(db_provider)]
    ) -> AsyncGenerator[PostService, None]:
        """Post service provider method"""
        holder = Holder(db_session)
        yield PostService(holder.post)


def user_service() -> UserService:  # type: ignore
    ...


def post_service() -> PostService:  # type: ignore
    ...
