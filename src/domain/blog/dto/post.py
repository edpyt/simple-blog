from datetime import datetime
from uuid import UUID
from pydantic import ConfigDict
from pydantic.main import BaseModel


class BasePostDTO(BaseModel):
    title: str
    body: str


class CreatePostDTO(BasePostDTO):
    ...


class PostDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uuid: UUID
    title: str
    body: str
    created_at: datetime
