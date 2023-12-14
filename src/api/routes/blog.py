from fastapi import APIRouter

router = APIRouter()


@router.get('/')
async def main_page() -> str:
    return 'Hello!'
