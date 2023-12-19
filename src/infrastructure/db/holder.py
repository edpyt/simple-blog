from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.dao.post import PostDAO
from src.infrastructure.db.dao.user import UserDAO


class Holder:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.user = UserDAO(session)
        self.post = PostDAO(session)
