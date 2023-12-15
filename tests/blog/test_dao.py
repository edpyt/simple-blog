import pytest

from src.infrastructure.db.dao.base import BaseDAO
from src.infrastructure.db.models.post import Post


@pytest.mark.asyncio
async def test_base_dao_creation() -> None:
    post_dao = BaseDAO(Post)
    print(await post_dao._get_all())