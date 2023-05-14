from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database.db import SessionLocal, engine



models.Base.metadata.create_all(bind = engine)

app = FastAPI()

