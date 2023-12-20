from typing import Annotated, Sequence
from fastapi import APIRouter, Depends

from src.api.di.providers.service import post_service
from src.core.utils.auth import get_current_active_user, oauth2_scheme
from src.domain.blog.dto.post import CreatePostDTO, PostDTO
from src.domain.blog.services.post import PostService
from src.infrastructure.db.models.user import User

router = APIRouter(prefix='/post')


@router.get('/')
async def today_posts(
    token: Annotated[str, Depends(oauth2_scheme)],
    post_service: PostService = Depends(post_service),
) -> Sequence[PostDTO]:
    """Return today posts"""
    posts = await post_service.get_today_posts()
    return posts


@router.post('/create/')
async def create_post(
    create_post_dto: CreatePostDTO,
    current_user: Annotated[User, Depends(get_current_active_user)],
    post_service: PostService = Depends(post_service)
) -> dict[str, str]:
    await post_service.create_post(
        create_post_dto, current_user
    )
    return {'status': 'success'}
