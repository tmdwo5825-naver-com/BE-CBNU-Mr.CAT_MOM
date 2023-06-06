from app import models, schemas
from app.models import Cat

from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session


class CrudMysql():
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


crud_mysql = CrudMysql()

