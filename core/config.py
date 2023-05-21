from pydantic import BaseSettings


class Settings(BaseSettings):
    mysql_user: str
    mysql_password: str
    mysql_port: str
    mysql_database: str

    redis_host: str
    redis_port: str
    redis_database: str

    aws_access_key_id: str
    aws_secret_access_key: str

    class Config:
        evn_file = ".env"


settings = Settings()
