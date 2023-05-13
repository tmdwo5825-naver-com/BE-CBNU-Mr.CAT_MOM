from fastapi import Depends, FastAPI, HTTPException, status
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

@app.post("/content-create/")
def create_dummy(request: schemas.CatCreate, db: Session = Depends(get_db) ):
    if not request.image:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No image found"
        )
    crud.create_cat(db,request)

@app.get("/", response_model= list[schemas.Test])
def get_dummy(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    response = crud.get_cat(db= db, skip= skip, limit= limit)
    if response is None:
        raise HTTPException(status_code=404, detail= "dummy not found")
    return response

