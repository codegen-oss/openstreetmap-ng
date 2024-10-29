import json
from math import isclose
from pathlib import Path

import uvloop
from pytz import country_timezones
from shapely.geometry import shape
from zstandard import ZstdDecompressor

from app.utils import http_get


def get_timezone_country_dict() -> dict[str, str]:
    result = {}
    print('Processing country timezones')
    for code, timezones in country_timezones.items():
        for timezone in timezones:
            if timezone in result:
                raise ValueError(f'Duplicate timezone {timezone!r}')
            result[timezone] = code
    return result


async def get_country_bbox_dict() -> dict[str, tuple[float, float, float, float]]:
    print('Downloading country data')
    async with http_get(
        'https://osm-countries-geojson.monicz.dev/osm-countries-0-1.geojson.zst',
        raise_for_status=True,
    ) as r:
        content = await r.read()

    content = ZstdDecompressor().decompress(content)
    features = json.loads(content)['features']
    result = {}

    print('Processing country boundaries')
    for feature in features:
        tags: dict[str, str] = feature['properties']['tags']
        country = tags.get('ISO3166-1:alpha2', tags.get('ISO3166-1'))
        if country is None:
            raise ValueError(f'Country code not found in {tags!r}')

        bbox = shape(feature['geometry']).bounds

        if country == 'FJ':
            bbox = (-182.870666, -20.67597, 181.575562, -12.480111)
        elif country == 'RU':
            bbox = (19.25, 41.188862, 190.95, 81.857361)
        elif country == 'TV':
            bbox = (176.064865, -10.801169, 179.863281, -5.641972)
        elif country == 'US':
            bbox = (-124.733253, 24.544245, -66.954811, 49.388611)

        if isclose(bbox[0], -180) and isclose(bbox[2], 180):
            print(f'[⚠️] {country}: spanning over 180° meridian')

        if country in result:
            raise ValueError(f'Duplicate country code {country!r}')

        result[country] = bbox

    return result


def generate_typescript_file(data: dict[str, tuple[float, float, float, float]]) -> str:
    print('Generating TypeScript file')

    lines: list[str] = []
    for timezone, bbox in sorted(data.items()):
        lines.append(f'    ["{timezone}", [{bbox[0]}, {bbox[1]}, {bbox[2]}, {bbox[3]}]]')

    header = '// This file is auto-generated by `timezone-bbox-update`'
    return (
        f'{header}\n\nexport const timezoneBoundsMap: Map<string, [number, number, number, number]>  = new Map([\n'
        + ',\n'.join(lines)
        + ',\n])\n'
    )


async def main() -> None:
    country_bbox = await get_country_bbox_dict()
    timezone_country = get_timezone_country_dict()
    result = {}

    print('Merging timezones with boundaries')
    for timezone, country in timezone_country.items():
        bbox = country_bbox.get(country)

        if bbox is None:
            print(f'[❔] {timezone}: missing {country!r} boundary')
            continue

        result[timezone] = bbox

    output = generate_typescript_file(result)
    output_path = Path('app/static/js/_timezone-bbox.ts')
    output_path.write_text(output)


if __name__ == '__main__':
    uvloop.run(main())
