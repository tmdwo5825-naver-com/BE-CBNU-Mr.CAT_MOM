from app import schemas
from app.database.set_redis import get_redis
from app.api.common.process_time import process_time

from fastapi import HTTPException
from redis.exceptions import ConnectionError, RedisError


def save_data(data):
    print("call save data")
    try:
        redis_conn = get_redis()
        redis_conn.ping()  # 커넥션 확인
    except ConnectionError as ce:
        raise HTTPException(status_code=500, detail="Redis Connection Error") from ce

    try:
        print("get redis obj")
        # 고유한 ID 생성
        unique_id = redis_conn.incr('cat_data_id')
        key = f'cat_data:{unique_id}'
        print("get unique id")

        # 데이터 저장
        redis_conn.hmset(key, data)
        # TTL 설정 (3시간)
        redis_conn.expire(key, 3 * 60 * 60)
        print(data)
    except RedisError as re:
        raise HTTPException(status_code=500, detail="Redis Data Save Error") from re
    finally:
        redis_conn.close()


def get_all_data():
    try:
        redis_conn = get_redis()
        redis_conn.ping()
    except ConnectionError as ce:
        raise HTTPException(status_code=500, detail="Redis Connection Error") from ce

    try:
        all_keys = redis_conn.keys('cat_data:*')
        all_data = []

        for key in all_keys:
            data = redis_conn.hgetall(key)
            data_str = {k.decode(): v.decode() for k, v in data.items()}
            if 'cat_tower' in data_str:
                del data_str['cat_tower']  # 'cat_tower' 필드가 있는 경우 삭제

            recent_time = process_time.get_recent_time(hour_ago=data_str['hour'], min_ago=data_str['min'])
            del data_str['hour']
            del data_str['min']
            data_str['upload_time'] = recent_time

            data_str['x'] = float(data_str['x'])
            data_str['y'] = float(data_str['y'])

            all_data.append(data_str)

        return all_data
    except RedisError as re:
        raise HTTPException(status_code=500, detail="Redis get Error") from re
    finally:
        redis_conn.close()

def count_data():
    redis_conn = get_redis()
    all_keys = redis_conn.keys('cat_data:*')
    n14_count = 0
    lib_count = 0
    domitory_sungjae_count = 0
    domitory_jinjae_count = 0

    for key in all_keys:
        data = redis_conn.hgetall(key)
        data_str = {k.decode(): v.decode() for k, v in data.items()}
        print(data_str.get('cat_tower'))
        if data_str.get('cat_tower') == "n14":
            n14_count += 1
        elif data_str.get('cat_tower') == "lib":
            lib_count += 1
        elif data_str.get('cat_tower') == "sungjae":
            domitory_sungjae_count += 1
        elif data_str.get('cat_tower') == "jinjae":
            domitory_jinjae_count += 1

    return {
        "data2": [
            {
                "id": 1,
                "count": domitory_sungjae_count
            },
            {
                "id": 2,
                "count": n14_count
            },
            {
                "id": 3,
                "count": lib_count
            },
            {
                "id": 4,
                "count": domitory_jinjae_count
            }
        ]
    }


class CrudRedis():

    # noinspection PyMethodMayBeStatic
    def create_3h_content(self, cat_in: schemas.CatCreateRedis):
        print("crud func call done")

        # 필드와 값을 함께 저장
        data = {
            'image_url': cat_in.image_url,
            'comment': cat_in.comment,
            'x': cat_in.x,
            'y': cat_in.y,
            'cat_tower': cat_in.cat_tower,
            'hour': cat_in.hour,
            'min': cat_in.min
        }
        save_data(data)

    # noinspection PyMethodMayBeStatic
    def get_3h(self):
        response = get_all_data()
        print(response)
        return response

    # noinspection PyMethodMayBeStatic
    def get_3h_count(self):
        count_response = count_data()
        return count_response


crud_redis = CrudRedis()
