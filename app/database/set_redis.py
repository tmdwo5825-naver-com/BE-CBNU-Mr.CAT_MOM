from app.core.config import settings
import redis


def get_redis():
    r = redis.Redis(
        host='redis_container',
        port=6379,
        db=0,
    )
    return r

