class BlogBaseException(BaseException):
    error_msg: str

    def __str__(self) -> str:
        return self.error_msg
