import os
import  configparser
from pathlib import Path
import redis

path = Path(__file__)
ROOT_DIR = path.parent.absolute()
config_path = os.path.join(ROOT_DIR, "redis/config.ini")

config = configparser.ConfigParser()
config.read(config_path)

host = config('redis', 'host')
port = config('redis', 'port')
database = config('redis', 'database')


def get_redis():

    rd = redis.Redis(host=host, port=port, db=database)
    return rd

