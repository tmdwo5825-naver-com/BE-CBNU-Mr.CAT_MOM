from pydantic import BaseModel


class CatCreate(BaseModel):
    comment: str
    image_url: str
    x: float
    y: float
    cat_tower: str


class CatResponse(BaseModel):
    x: float
    y: float
    comment: str
    url: str

    class Config:
        orm_mode = True

