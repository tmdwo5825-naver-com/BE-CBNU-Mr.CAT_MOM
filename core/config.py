from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    mysql_user: str
    mysql_password: str
    mysql_host: str
    mysql_port: str
    mysql_database: str

    redis_host: str
    redis_port: str
    redis_database: str

    aws_access_key_id: str
    aws_secret_access_key: str

    class Config:
        env_file = f"{os.path.dirname(os.path.abspath(__file__))}/.env"


settings = Settings()
