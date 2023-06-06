from app.core.config import settings
import redis
from redis.exceptions import ConnectionError


def get_redis():
    r = redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=0,
    )
    return r
