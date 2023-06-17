from sqlalchemy import Column, Integer, VARCHAR, DateTime, text, FLOAT, String

from app.database.set_mysql import Base


class Cat(Base):
    __tablename__ = "cat_mom"
    geo_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True )
    created_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    image_url = Column(VARCHAR(500))
    comment = Column(VARCHAR(500), nullable=True)
    x = Column(FLOAT)
    y = Column(FLOAT)
    upload_time = Column(String(100))





