import unicodedata
from functools import cache
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import msgspec
from aiohttp import ClientSession, ClientTimeout

from app.config import USER_AGENT

JSON_ENCODE = msgspec.json.Encoder(decimal_format='number', order='sorted').encode
JSON_DECODE = msgspec.json.Decoder().decode


def json_encodes(obj: Any) -> str:
    """
    Like JSON_ENCODE, but returns a string.

    >>> json_encodes({'foo': 'bar'})
    '{"foo": "bar"}'
    """
    return JSON_ENCODE(obj).decode()


@cache
def http():
    """
    Caching HTTP client factory.
    """
    return ClientSession(
        headers={'User-Agent': USER_AGENT},
        json_serialize=json_encodes,
        timeout=ClientTimeout(total=15, connect=10),
    )


# TODO: reporting of deleted accounts (prometheus)
# NOTE: breaking change


def unicode_normalize(text: str) -> str:
    """
    Normalize a string to NFC form.
    """
    return unicodedata.normalize('NFC', text)


def extend_query_params(uri: str, params: dict[str, str]) -> str:
    """
    Extend the query parameters of a URI.

    >>> extend_query_params('http://example.com', {'foo': 'bar'})
    'http://example.com?foo=bar'
    """
    if not params:
        return uri
    uri_ = urlsplit(uri)
    query = parse_qsl(uri_.query, keep_blank_values=True)
    query.extend(params.items())
    return urlunsplit(uri_._replace(query=urlencode(query)))
