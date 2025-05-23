
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from config import settings
from database.database import async_session


async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session

redis_client = Redis.from_url(settings.redis.url, decode_responses=True)

async def get_redis() -> Redis:
    return redis_client
