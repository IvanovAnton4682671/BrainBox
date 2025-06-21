from redis.asyncio import Redis
from core.config import settings

redis = Redis.from_url("redis://localhost:30006/0")