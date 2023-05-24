from sqlalchemy.orm import Session

from app import models, schemas


class CrudCat():
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
        return db

    def get_24h(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Cat).offset(skip).limit(limit).all()







