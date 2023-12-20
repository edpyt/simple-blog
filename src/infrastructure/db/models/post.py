from uuid import UUID
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.db.models.base import BaseUUIDModel
from src.infrastructure.db.models.user import User


class Post(BaseUUIDModel):
    __tablename__ = 'posts'

    title: Mapped[str] = mapped_column(String(128), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)

    created_by_uuid: Mapped[UUID] = mapped_column(ForeignKey('users.uuid'))
    created_by: Mapped[User] = relationship(back_populates='posts')
