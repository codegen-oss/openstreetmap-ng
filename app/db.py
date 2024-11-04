from contextlib import asynccontextmanager

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from valkey.asyncio import ConnectionPool, Valkey

from app.config import POSTGRES_URL, VALKEY_URL
from app.utils import JSON_DECODE, json_encodes

_DB_ENGINE = create_async_engine(
    POSTGRES_URL,
    json_deserializer=JSON_DECODE,
    json_serializer=json_encodes,
    query_cache_size=1024,
    pool_size=100,  # concurrent connections target
    max_overflow=-1,  # unlimited concurrent connections overflow
)

_VALKEY_POOL = ConnectionPool.from_url(VALKEY_URL)

# TODO: test unicode normalization comparison


@asynccontextmanager
async def db():
    """
    Get a database session.
    """
    async with AsyncSession(
        _DB_ENGINE,
        expire_on_commit=False,
        close_resets_only=False,  # prevent closed sessions from being reused
    ) as session:
        yield session


@asynccontextmanager
async def db_commit():
    """
    Get a database session that commits on exit.
    """
    async with db() as session:
        yield session
        await session.commit()


async def db_update_stats(*, vacuum: bool = False) -> None:
    """
    Update the database statistics.
    """
    async with db() as session:
        await session.connection(execution_options={'isolation_level': 'AUTOCOMMIT'})
        await session.execute(text('VACUUM ANALYZE') if vacuum else text('ANALYZE'))


@asynccontextmanager
async def valkey():
    async with Valkey(connection_pool=_VALKEY_POOL) as r:
        yield r
