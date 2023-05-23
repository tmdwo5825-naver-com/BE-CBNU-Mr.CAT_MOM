from sqlalchemy.orm import Session

from . import models, schemas


def create_cat(db: Session, cat: schemas.CatCreate):
    db_cat = models.Cat(
        x=cat.x,
        y=cat.y,
        image_url=cat.image_url,
        comment=cat.comment
    )
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db


def get_cat(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Cat).offset(skip).limit(limit).all()
