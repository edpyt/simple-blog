from datetime import date
from uuid import UUID

from sqlalchemy import Sequence, func
from sqlalchemy.orm.interfaces import ORMOption

from src.domain.blog.dto.post import CreatePostDTO, PostDTO, UpdatePostDTO
from src.infrastructure.db.dao.post import PostDAO
from src.infrastructure.db.models.post import Post
from src.infrastructure.db.models.user import User


class PostService:
    def __init__(self, post_dao: PostDAO) -> None:
        self.post_dao = post_dao

    async def create_post(
        self, create_post_dto: CreatePostDTO, user: User
    ) -> Post:
        """Create post (only with provided user)

        :param create_post_dto: DTO for create post
        :return: `Post`
        """
        create_post = Post(
            title=create_post_dto.title,
            body=create_post_dto.body,
            created_by=user
        )
        return await self.post_dao.create_post(create_post)

    async def get_post_by_uuid(self, post_uuid: str | UUID) -> PostDTO:
        """Get single post object by UUID

        :param kwargs: Filter for get instance
        :return: `Post` DTO
        """
        post = await self.post_dao.get_post(Post.uuid == post_uuid)
        return PostDTO.model_validate(post)

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

    async def update_post(
        self, post_uuid: str | UUID, update_post_dto: UpdatePostDTO
    ) -> PostDTO:
        """Update post

        :param update_post_dto: Update `Post` DTO

        :return: `Post` DTO
        """
        post = await self.post_dao.update_post(post_uuid, update_post_dto)
        return PostDTO.model_validate(post)
