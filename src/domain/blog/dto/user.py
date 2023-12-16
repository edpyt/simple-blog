from uuid import UUID

from pydantic import field_validator
from pydantic.main import BaseModel

from src.core.utils.password import get_password_hash


class BaseUserDTO(BaseModel):
    username: str
    password: str


class CreateUserDTO(BaseUserDTO):
    @field_validator('password')
    @classmethod
    def hash_password(cls, password: str) -> str:
        """Auto hash password"""
        return get_password_hash(password)


class UserDTO(BaseModel):
    uuid: UUID
    username: str
    password: str

    class Config:
        from_attributes = True
