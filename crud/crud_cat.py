from app import models, schemas

from sqlalchemy.orm import Session
from app.database.set_redis import get_redis


class CrudCat():
    # noinspection PyMethodMayBeStatic
    def create_24h_content(self, db: Session, cat_in: schemas.CatCreate):
        db_cat = models.Cat(
            x=cat_in.x,
            y=cat_in.y,
            image_url=cat_in.image_url,
            comment=cat_in.comment
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
        r = get_redis()

        data_id = r.zcard('data_ids') + 1

        # 데이터 ID를 Sorted Set에 추가
        r.zadd('data_ids', {f'data:{data_id}': data_id})

        # 필드와 값을 함께 저장
        r.hset(f'data:{data_id}', 'image_url', cat_in.image_url)
        r.hset(f'data:{data_id}', 'comment', cat_in.comment)
        r.hset(f'data:{data_id}', 'x', cat_in.x)
        r.hset(f'data:{data_id}', 'y', cat_in.y)

    # noinspection PyMethodMayBeStatic
    def get_3h(self):
        r = get_redis()

        # 모든 데이터 ID 가져 오기
        data_ids = r.zrange('data_ids', 0, -1)

        # 데이터 복원
        all_data = []
        for data_id in data_ids:
            data = r.hgetall(data_id)
            all_data.append(data)

        return all_data


crud_cat = CrudCat()
