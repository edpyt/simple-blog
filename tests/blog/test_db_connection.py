import pytest
from sqlalchemy import ScalarResult, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.models import Base, Post


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'model_obj',
    [
        Post(),
    ],
)
async def test_db_tables_creation(
    db_session: AsyncSession, model_obj: Base
) -> None:
    """Test that the tables was created"""
    query = select(type(model_obj))

    # Should not raise error
    result: ScalarResult = await db_session.scalars(query)

    assert list(result) == []


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'model_obj',
    [
        Post(),
    ],
)
async def test_create_record(db_session: AsyncSession, model_obj: Base) -> None:
    """Test creation new record into the table"""
    db_session.add(model_obj)
    await db_session.commit()

    result: list = list(await db_session.scalars(select(type(model_obj))))

    assert len(result) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'model_obj',
    [
        Post(),
    ],
)
async def test_that_records_are_not_saving_through_test_session(
    db_session: AsyncSession, model_obj: Base
) -> None:
    """Test records are not saving in test database"""
    result: list = list(await db_session.scalars(select(type(model_obj))))

    assert len(result) == 0
