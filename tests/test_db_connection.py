import pytest
from sqlalchemy import ScalarResult, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.models import Base, Post
from src.infrastructure.db.models.user import User


@pytest.mark.asyncio
@pytest.mark.parametrize('model_obj', [User, Post])
async def test_db_tables_creation(
    db_session: AsyncSession, model_obj: Base
) -> None:
    """Test that the tables was created"""
    query = select(model_obj)

    # Should not raise error
    result: ScalarResult = await db_session.scalars(query)

    assert list(result) == []


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'model_obj',
    [
        User(username='testuser', password='testpassword123'),
        Post(title='test', body='test'),
    ],
)
async def test_create_record(
    db_session: AsyncSession,
    model_obj: Base
) -> None:
    """Test creation new record into the table"""
    if isinstance(model_obj, Post):
        created_user = User(username='test', password='testpass123')
        db_session.add(created_user)
        model_obj.created_by = created_user

    db_session.add(model_obj)
    await db_session.commit()

    result: list = list(await db_session.scalars(select(type(model_obj))))

    assert len(result) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize('model_obj', [User, Post])
async def test_that_records_are_not_saving_through_test_session(
    db_session: AsyncSession, model_obj: Base
) -> None:
    """Test records are not saving in test database"""
    result: list = list(await db_session.scalars(select(model_obj)))

    assert len(result) == 0
