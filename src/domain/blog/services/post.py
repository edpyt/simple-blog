from datetime import date

from sqlalchemy import Sequence, func
from sqlalchemy.orm.interfaces import ORMOption

from src.domain.blog.dto.post import CreatePostDTO, PostDTO
from src.infrastructure.db.dao.post import PostDAO
from src.infrastructure.db.models.post import Post


class PostService:
    def __init__(self, post_dao: PostDAO) -> None:
        self.post_dao = post_dao

    async def create_post(self, create_post_dto: CreatePostDTO) -> Post:
        """Create post

        :param create_post_dto: DTO for create post
        :return: Post
        """
        create_post = Post(
            title=create_post_dto.title, body=create_post_dto.body
        )
        return await self.post_dao.create_post(create_post)

    async def get_posts(self, *options: Sequence[ORMOption]) -> list[PostDTO]:
        """Get posts

        :param options: Optional param of SQLAlchemy options
        :return: list `Post`
        """
        return [
            PostDTO.model_validate(post)
            for post in await self.post_dao.get_posts(*options)
        ]

    async def get_today_posts(self) -> list[PostDTO]:
        """Get today posts

        :return: list `Post`
        """
        return await self.get_posts(func.DATE(Post.created_at) == date.today())
