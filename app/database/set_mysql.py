from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .. core.config import settings


DB_URL = "mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8mb4" % (
    settings.mysql_user,
    settings.mysql_password,
    settings.mysql_host,
    settings.mysql_port,
    settings.mysql_database
)

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
