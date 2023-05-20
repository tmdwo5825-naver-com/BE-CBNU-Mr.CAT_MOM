from fastapi import FastAPI
import models
from . database.set_mysql import engine

models.Base.metadata.create_all(bind = engine)


app = FastAPI()

