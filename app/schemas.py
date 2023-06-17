from pydantic import BaseModel


class CatCreateMysql(BaseModel):
    comment: str
    image_url: str
    x: float
    y: float
    upload_time: str


class CatCreateRedis(BaseModel):
    comment: str
    image_url: str
    x: float
    y: float
    cat_tower: str
    hour: int
    min: int


class CatResponse(BaseModel):
    x: float
    y: float
    comment: str
    url: str

    class Config:
        orm_mode = True

