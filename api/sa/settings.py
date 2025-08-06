
from pydantic_settings import BaseSettings
import logging


logging.basicConfig(level=logging.INFO)


class Settings(BaseSettings):
    db_url: str
    owner_username: str
    owner_password: str
    secret_key: str
    owner_access_token_expiry_minute: int = 15
    admin_access_token_expiry_minute: int = 60
    allowed_origin: str
    production: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
