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
    created_at: str
    comment: str
    url: str
    cat_tower: str
    geo_id: int

    class Config:
        orm_mode = True


