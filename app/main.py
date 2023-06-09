import os

current_directory = os.getcwd()
os.environ['PYTHONPATH'] = current_directory

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.api.endpoint import router
import uvicorn


app = FastAPI()

app.include_router(router.router)


origins = [
    "https://catmom22.vercel.app",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
