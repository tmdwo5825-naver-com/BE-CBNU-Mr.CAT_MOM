from sqlalchemy import Column, Integer, VARCHAR, DateTime, text
from .database.db import Base


class Cat(Base):
    __tablename__ = "Cat_mom"
    geo_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    created_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    storage_URL = Column(VARCHAR(500))
    comment = Column(VARCHAR(500), nullable=True)

    x = Column(Integer)
    y = Column(Integer)

