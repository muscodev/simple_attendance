
from pydantic_settings import BaseSettings
import logging


logging.basicConfig(level=logging.INFO)


class Settings(BaseSettings):
    db_url: str
    username: str
    password: str
    secret_key: str
    owner_access_token_expiry_minute: int = 15
    admin_access_token_expiry_minute: int = 60

    class Config:
        env_file = ".env"


settings = Settings()
