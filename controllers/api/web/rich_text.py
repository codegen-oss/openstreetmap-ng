from typing import Annotated

from fastapi import APIRouter, Form

from lib.auth import web_user
from lib.rich_text import RichText
from models.db.user import User
from models.text_format import TextFormat

router = APIRouter(prefix='/rich_text')


@router.post('/preview')
async def preview(
    text: Annotated[str, Form()],
    text_format: Annotated[TextFormat, Form()],
    _: Annotated[User, web_user()],
) -> str:
    cache = await RichText.get_cache(text, None, text_format)
    return cache.value
