from app import models, schemas

from sqlalchemy.orm import Session
from app.database.set_redis import get_redis


def save_data(data):
    r = get_redis()
    # 고유한 ID 생성
    unique_id = r.incr('cat_data_id')
    key = f'cat_data:{unique_id}'

    # 데이터 저장
    r.hmset(key, data)
    # TTL 설정 (3시간)
    r.expire(key, 3 * 60 * 60)


def get_all_data():
    r = get_redis()
    # 저장된 모든 데이터 가져오기
    all_keys = r.keys('cat_data:*')
    all_data = []

    for key in all_keys:
        data = r.hgetall(key)
        data_str = {k.decode(): v.decode() for k, v in data.items()}
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
    def get_24h(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Cat).offset(skip).limit(limit).all()

    # noinspection PyMethodMayBeStatic
    def create_3h_content(self, cat_in: schemas.CatCreate):
        # 필드와 값을 함께 저장
        data = {
            'image_url': cat_in.image_url,
            'comment': cat_in.comment,
            'x': cat_in.x,
            'y': cat_in.y
        }
        save_data(data)

    # noinspection PyMethodMayBeStatic
    def get_3h(self):
        response = get_all_data()
        print(response)


#        db_size = r.dbsize()
#
        # 데이터 복원
#        all_data = []
#        for data_id in range(0, db_size):
#            data = r.hgetall(data_id)
#            all_data.append(data)

#        return all_data


crud_cat = CrudCat()

