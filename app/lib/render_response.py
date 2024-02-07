import cython
import orjson
from starlette.responses import HTMLResponse

from app.config import API_URL, ID_URL, ID_VERSION, RAPID_URL, RAPID_VERSION
from app.lib.auth_context import auth_user
from app.lib.translation import render, translation_languages
from app.limits import MAP_QUERY_AREA_MAX_SIZE, NOTE_QUERY_AREA_MAX_SIZE


@cython.cfunc
def _get_default_data() -> dict:
    user = auth_user()
    languages = translation_languages()

    if (user is not None) and (user_home_point := user.home_point) is not None:
        home_point = (user_home_point.x, user_home_point.y)
    else:
        home_point = None

    config = {
        'apiUrl': API_URL,
        'idUrl': ID_URL,
        'idVersion': ID_VERSION,
        'rapidUrl': RAPID_URL,
        'rapidVersion': RAPID_VERSION,
        'languages': languages,
        'homePoint': home_point,
        'mapQueryAreaMaxSize': MAP_QUERY_AREA_MAX_SIZE,
        'noteQueryAreaMaxSize': NOTE_QUERY_AREA_MAX_SIZE,
    }

    return {
        'lang': languages[0],
        'config': orjson.dumps(config).decode(),
    }


def render_response(template_name: str, **template_data: dict) -> HTMLResponse:
    """
    Render the given Jinja2 template with translation.
    """

    data = _get_default_data()
    data.update(template_data)
    return HTMLResponse(render(template_name, **data))
