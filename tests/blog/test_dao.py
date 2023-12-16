import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.dao.base import BaseDAO
from src.infrastructure.db.models.post import Post


@pytest.mark.asyncio
async def test_dao_functional(db_session: AsyncSession) -> None:
    post_dao = BaseDAO(Post, db_session)
    await post_dao._get_all()  # Should not raise error
