from datetime import datetime
import uuid as guid

from sqlalchemy import MetaData, types
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

constraint_naming_conventions = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(
        types.DateTime, default=datetime.utcnow
    )
    metadata = MetaData(naming_convention=constraint_naming_conventions)


class BaseUUIDModel(Base):
    __abstract__ = True

    uuid: Mapped[guid.UUID] = mapped_column(
        types.Uuid, primary_key=True, default=guid.uuid4
    )
