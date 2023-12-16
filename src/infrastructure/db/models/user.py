from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.db.models.base import BaseUUIDModel


class User(BaseUUIDModel):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(
        String(128), nullable=False, unique=True
    )
    password: Mapped[str] = mapped_column(String(60))
    disabled: Mapped[bool] = mapped_column(Boolean, default=False)
