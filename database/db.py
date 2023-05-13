import configparser
import os
from pathlib import Path
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

path = Path(__file__)
ROOT_DIR = path.parent.absolute()
config_path = os.path.join(ROOT_DIR, "config.ini")

config = configparser.ConfigParser()
config.read(config_path)

user = config.get('mysql', 'user')
password = config.get('mysql', 'password')
host = config.get('mysql', 'host')
port = config.get('mysql', 'port')
database = config.get('mysql', 'database')

DB_URL = "mysql+pymysql://%s:%s@%s:%s/%s" % (user, password, host, port, database)

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
