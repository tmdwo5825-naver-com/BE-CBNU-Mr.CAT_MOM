import redis
from app.core.config import settings
from app.database.set_redis import get_redis

r = get_redis()
r.flushall()
