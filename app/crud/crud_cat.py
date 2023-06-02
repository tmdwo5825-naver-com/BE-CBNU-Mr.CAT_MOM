from app import models, schemas
from app.models import Cat
from app.database.set_redis import get_redis

from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session


def save_data(data):
    print("call save data")
    r = get_redis()
    print("get redis obj")
    # 고유한 ID 생성
    unique_id = r.incr('cat_data_id')
    key = f'cat_data:{unique_id}'
    print("get unique id")

    # 데이터 저장
    r.hmset(key, data)
    # TTL 설정 (3시간)
    r.expire(key, 3 * 60 * 60)
    print(data)


def get_all_data():
    r = get_redis()
    # 저장된 모든 데이터 가져오기
    all_keys = r.keys('cat_data:*')
    all_data = []

    for key in all_keys:
        data = r.hgetall(key)
        data_str = {k.decode(): v.decode() for k, v in data.items()}
        if 'cat_tower' in data_str:
            del data_str['cat_tower']  # 'cat_tower' 필드가 있는 경우 삭제

        all_data.append(data_str)

    return all_data


class CrudCat():
    # noinspection PyMethodMayBeStatic
    def create_24h_content(self, db: Session, cat_in: schemas.CatCreate):
        db_cat = models.Cat(
            x=cat_in.x,
            y=cat_in.y,
            image_url=cat_in.image_url,
            comment=cat_in.comment,
            cat_tower=cat_in.cat_tower
        )
        db.add(db_cat)
        db.commit()
        db.refresh(db_cat)
        return db_cat

    # noinspection PyMethodMayBeStatic
    def get_24h(self, db: Session):

        try:
            # 현재 시간
            current_time = datetime.now()

            # 24시간 이내의 데이터를 조회하기 위한 시간 범위 계산
            time_threshold = current_time - timedelta(hours=24)

            # 쿼리 실행
            query = db.query(Cat).filter(Cat.created_at >= time_threshold).all()

            # 결과 반환
            return query

        except SQLAlchemyError as e:
            # 예외 처리
            print("SQLAlchemy Error:", str(e))
            return []

    # noinspection PyMethodMayBeStatic
    def create_3h_content(self, cat_in: schemas.CatCreate):
        print("crud func call done")
        # 필드와 값을 함께 저장
        data = {
            'image_url': cat_in.image_url,
            'comment': cat_in.comment,
            'x': cat_in.x,
            'y': cat_in.y,
            'cat_tower': cat_in.cat_tower
        }
        save_data(data)

    # noinspection PyMethodMayBeStatic
    def get_3h(self):
        response = get_all_data()
        print(response)
        return response

    def count_data(self):
        r = get_redis()
        all_keys = r.keys('cat_data:*')
        n14_count = 0
        lib_count = 0
        domitory_sungjae_count = 0
        domitory_jinjae_count = 0

        for key in all_keys:
            data = r.hgetall(key)
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


crud_cat = CrudCat()

