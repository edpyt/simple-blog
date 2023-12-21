from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import ConfigDict
from pydantic.main import BaseModel


class BasePostDTO(BaseModel):
    title: str
    body: str


class CreatePostDTO(BasePostDTO):
    ...


class UpdatePostDTO(BasePostDTO):
    model_config = ConfigDict(from_attributes=True)

    title: Optional[str] = None  # type: ignore
    body: Optional[str] = None  # type: ignore
    created_at: Optional[datetime] = None  # type: ignore


class PostDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uuid: UUID
    title: str
    body: str
    created_at: datetime
