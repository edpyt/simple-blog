from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from src.api.di.providers.service import post_service
from src.core.utils.auth import get_current_active_user
from src.domain.blog.dto.post import CreatePostDTO, PostDTO, UpdatePostDTO
from src.domain.blog.services.post import PostService
from src.infrastructure.db.models.user import User

router = APIRouter(
    prefix='/post', dependencies=[Depends(get_current_active_user)]
)


@router.get('/')
async def today_posts(
    post_service: PostService = Depends(post_service),
) -> list[PostDTO]:
    """Return today posts

    :param post_service: Usecases for Post object

    :return: List of today Post`s in json
    """
    posts = await post_service.get_today_posts()
    return posts


@router.get('/all')
async def get_all_posts(
    post_service: PostService = Depends(post_service)
) -> list[PostDTO]:
    """Get all posts

    :param post_service: Usecases for Post object

    :return: List of today Post`s in json
    """
    posts = await post_service.get_posts()
    return posts


@router.get('/{post_uuid}')
async def get_post_by_uuid(
    post_uuid: UUID,
    post_service: PostService = Depends(post_service)
) -> PostDTO:
    """Return single post getting by UUID

    :param post_service: Usecases for Post object

    :return: Single `Post` DTO object
    """
    post = await post_service.get_post_by_uuid(post_uuid=post_uuid)
    return post


@router.post('/create/')
async def create_post(
    create_post_dto: CreatePostDTO,
    current_user: Annotated[User, Depends(get_current_active_user)],
    post_service: PostService = Depends(post_service)
) -> dict[str, str]:
    """Create post

    :param create_post_dto: DTO object for create Post
    :param current_user: Only authenticated user can create post. User object
    :param post_service: Usecases for Post object

    :return: Status message
    """
    await post_service.create_post(
        create_post_dto, current_user
    )
    return {'status': 'success'}


@router.put('/update/{post_uuid}')
async def update_post(
    post_uuid: str,
    post_update_dto: UpdatePostDTO,
    post_service: PostService = Depends(post_service)
) -> PostDTO:
    """Update post

    :param post_uuid: Post object uuid
    :param post_service: Usecases for Post object

    :return: Post object in json
    """
    post = await post_service.update_post(post_uuid, post_update_dto)
    return post
