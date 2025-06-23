from redis.asyncio import Redis
from core.config import settings

redis = Redis.from_url(url=settings.REDIS_URL)