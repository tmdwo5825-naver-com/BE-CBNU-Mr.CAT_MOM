from fastapi import FastAPI
from .router.router import router

app = FastAPI()

app.include_router(router)

