from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine



models.Base.metadata.create_all(bind = engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/test/", response_model=schemas.Test)
def create_dummy(dummy: schemas.TestCreate, db:Session = Depends(get_db) ):
    return crud.create_test(db= db, test= dummy)

@app.get("/test/get_test/", response_model= list[schemas.Test])
def get_dummy(skip: int = 0, limit: int = 100, db: Session = Depends(get_db) ):
    dummys = crud.get_test(db= db, skip= skip, limit= limit)
    if dummys[0] is None:
        raise HTTPException(status_code=404, detail= "dummy not found")
    return dummys

