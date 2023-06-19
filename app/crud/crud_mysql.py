from app import models, schemas
from app.models import Cat

from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, load_only


class CrudMysql():
    # noinspection PyMethodMayBeStatic
    def create_24h_content(self, db: Session, cat_in: schemas.CatCreateMysql):
        db_cat = models.Cat(
            x=cat_in.x,
            y=cat_in.y,
            image_url=cat_in.image_url,
            comment=cat_in.comment,
            upload_time=cat_in.upload_time
        )
        db.add(db_cat)
        db.commit()
        db.refresh(db_cat)
        db.close()
        return db_cat

    # noinspection PyMethodMayBeStatic
    def get_24h(self, db: Session):

        try:
            # 현재 시간
            current_time = datetime.now()

            # 24시간 이내의 데이터를 조회하기 위한 시간 범위 계산
            time_threshold = current_time - timedelta(hours=24)

            # 쿼리 실행
            query = db.query(Cat).options(load_only(Cat.image_url, Cat.comment, Cat.x, Cat.y, Cat.upload_time)).filter(Cat.created_at >= time_threshold).all()
            db.close()
            # 결과 반환
            return query

        except SQLAlchemyError as e:
            # 예외 처리
            print("SQLAlchemy Error:", str(e))
            return []


crud_mysql = CrudMysql()

