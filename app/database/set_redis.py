from app.core.config import settings
import redis
from redis.exceptions import ConnectionError


async def get_redis():
    try:
        r = redis.Redis(
            host=settings.redis_host,
            port=6379,
            db=0,
            socket_timeout=30,
            socket_connect_timeout=30
        )
    except ConnectionError as e:
        print("Redis connection error:", e)
        return None
    return r