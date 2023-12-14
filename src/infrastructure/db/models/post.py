import uuid as guid

from sqlalchemy import types
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.db.models.base import Base


class Post(Base):
    __tablename__ = 'posts'

    uuid: Mapped[guid.UUID] = mapped_column(
        types.Uuid,
        primary_key=True
    )
