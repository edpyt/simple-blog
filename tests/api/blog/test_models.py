import pytest

from src.infrastructure.db.models.post import Post


@pytest.mark.asyncio
async def test_create_post() -> None:
    Post()