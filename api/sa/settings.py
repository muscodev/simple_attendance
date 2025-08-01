
from pydantic_settings import BaseSettings
import logging


logging.basicConfig(level=logging.INFO)


class Settings(BaseSettings):
    db_url: str
    username: str
    password: str
    secret_key: str

    class Config:
        env_file = ".env"


settings = Settings()
