from sqlalchemy import Column, Integer, VARCHAR, DateTime, text
from .database import Base

class Test(Base):
    __tablename__ = "test"
    geo_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    x = Column(Integer)
    y = Column(Integer)
    created_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    storage_URL = Column(VARCHAR(500))
    comment = Column(VARCHAR(500))
