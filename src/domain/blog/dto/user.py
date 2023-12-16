from uuid import UUID
from pydantic.main import BaseModel


class BaseUserDTO(BaseModel):
    username: str
    password: str


class CreateUserDTO(BaseUserDTO):
    ...


class UserDTO(BaseModel):
    uuid: UUID
    username: str
    password: str

    class Config:
        from_attributes = True
