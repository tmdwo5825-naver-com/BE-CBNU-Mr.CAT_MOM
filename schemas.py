from fastapi import File, UploadFile, Form

from pydantic import BaseModel


class CatCreate(BaseModel):
    comment: str
    image_url: str
    x: int
    y: int


class CatResponse(BaseModel):
    x: int
    y: int
    created_at: str
    comment: str
    url: str

    geo_id: int

    class Config:
        orm_mode = True


