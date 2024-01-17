import logging
from urllib.parse import urlencode

import cython
from httpx import HTTPError
from shapely.geometry import Point

from src.config import NOMINATIM_URL
from src.lib_cython.translation import primary_translation_language, translation_languages
from src.services.cache_service import CacheService
from src.utils import HTTP

if cython.compiled:
    print(f'{__name__}: 🐇 compiled')

_cache_context = 'Nominatim'


class Nominatim:
    @staticmethod
    async def reverse_name(point: Point, zoom: int) -> str:
        """
        Reverse geocode a point into a human-readable name.
        """

        path = '/reverse?' + urlencode(
            {
                'format': 'jsonv2',
                'lon': point.x,
                'lat': point.y,
                'zoom': zoom,
                'accept-language': primary_translation_language(),
            }
        )

        async def factory() -> str:
            logging.debug('Nominatim cache miss for path %r', path)
            r = await HTTP.get(NOMINATIM_URL + path, timeout=4)
            r.raise_for_status()
            data = await r.json()
            return data['display_name']

        try:
            display_name = await CacheService.get_one_by_key(path, _cache_context, factory)
        except HTTPError:
            logging.warning('Nominatim reverse geocoding failed', exc_info=True)
            display_name = None

        if display_name:
            return display_name
        else:
            # always succeed, return coordinates as a fallback
            return f'{point.y:.3f}, {point.x:.3f}'