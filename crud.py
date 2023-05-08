from sqlalchemy.orm import Session

from . import models, schemas

def get_test(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Test).offset(skip).limit(limit).all()

def create_test(db: Session, test: schemas.TestCreate):
    db_test = models.Test(
        x=test.x
        , y=test.y
        , created_at=test.created_at
        , comment=test.comment
        , storage_URL = test.storage_URL
        )
    db.add(db_test)
    db.commit()
    db.refresh(db_test)
    return db_test
    