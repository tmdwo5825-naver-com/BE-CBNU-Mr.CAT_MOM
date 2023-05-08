from pydantic import BaseModel
from datetime import datetime

class TestBase(BaseModel):
    x: int
    y: int
    storage_URL: str
    comment: str
    created_at: datetime

class TestCreate(TestBase):
    pass

class Test(TestBase):
    geo_id: int
    
    class config:
        orm_mode = True