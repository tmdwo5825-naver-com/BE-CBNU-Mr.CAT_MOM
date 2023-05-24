from app.core.config import settings
import redis


def get_redis():
    r = redis.StrictRedis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=settings.redis_database
    )
    return r

