from typing import Sequence
from fastapi import APIRouter, Depends

from src.api.di.providers.service import post_service
from src.domain.blog.dto.post import PostDTO
from src.domain.blog.services.post import PostService

router = APIRouter(prefix='/post')


@router.get('/')
async def today_posts(
    post_service: PostService = Depends(post_service),
) -> Sequence[PostDTO]:
    """Return today posts"""
    posts = await post_service.get_today_posts()
    return posts
