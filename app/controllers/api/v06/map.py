from typing import Annotated

from fastapi import APIRouter, Query

from app.format06 import Format06
from app.lib.exceptions_context import raise_for
from app.lib.geo_utils import parse_bbox
from app.lib.xmltodict import xattr
from app.limits import MAP_QUERY_AREA_MAX_SIZE, MAP_QUERY_LEGACY_NODES_LIMIT
from app.repositories.element_repository import ElementRepository

router = APIRouter()


@router.get('/map')
@router.get('/map.xml')
@router.get('/map.json')
async def map_read(
    bbox: Annotated[str, Query(min_length=1)],
) -> dict:
    geometry = parse_bbox(bbox)

    if geometry.area > MAP_QUERY_AREA_MAX_SIZE:
        raise_for().map_query_area_too_big()

    elements = await ElementRepository.find_many_by_query(
        geometry,
        nodes_limit=MAP_QUERY_LEGACY_NODES_LIMIT,
        legacy_nodes_limit=True,
    )

    bounds = geometry.bounds
    minx = bounds[0]
    miny = bounds[1]
    maxx = bounds[2]
    maxy = bounds[3]

    return {
        'bounds': {
            xattr('minlon'): minx,
            xattr('minlat'): miny,
            xattr('maxlon'): maxx,
            xattr('maxlat'): maxy,
        },
        **Format06.encode_elements(elements),
    }