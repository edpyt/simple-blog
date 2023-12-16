import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.models import User


@pytest.mark.asyncio
async def test_user_create(db_session: AsyncSession) -> None:
    """Test create user"""
    create_user = User(username='testuser', password='ahaagsd')

    db_session.add(create_user)
    await db_session.commit()
    await db_session.refresh(create_user)
    created_user = (await db_session.execute(select(User))).first()[0]

    assert create_user is created_user


@pytest.mark.asyncio
async def test_user_password_hashes(db_session: AsyncSession) -> None:
    ...
