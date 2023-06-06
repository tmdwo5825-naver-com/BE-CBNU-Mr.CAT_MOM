import redis
from app.core.config import settings

# Redis 서버 정보
REDIS_HOST = "ec2-3-39-25-103.ap-northeast-2.compute.amazonaws.com"
REDIS_PORT = 6379
REDIS_DB = 3

# Redis 클라이언트 생성 및 연결
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

# 값 저장
redis_client.set('mykey', 'myvalue')

# 값 읽기
value = redis_client.get('mykey')
print(value)
