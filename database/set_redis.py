from .. core.config import settings
import redis


def get_redis():
    rd = redis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=settings.redis_database
    )
    return rd

