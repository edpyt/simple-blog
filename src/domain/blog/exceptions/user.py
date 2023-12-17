from src.domain.blog.exceptions.base import BlogBaseException


class UserWithThisUserNameExists(BlogBaseException):
    error_msg = 'User with this username exists!'
