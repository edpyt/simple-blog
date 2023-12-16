from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.db.models.base import BaseUUIDModel


class Post(BaseUUIDModel):
    __tablename__ = 'posts'

    title: Mapped[str] = mapped_column(String(128), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
