
from typing import Optional
from pydantic_settings import BaseSettings
import logging


logging.basicConfig(level=logging.INFO)


class Settings(BaseSettings):
    db_url: str
    owner_username: str
    owner_password: str
    secret_key: str
    owner_access_token_expiry_minute: Optional[int] = 15
    admin_access_token_expiry_minute: Optional[int] = 60
    emplployee_login_token_expiry_minute: Optional[int] = 5
    employee_access_token_expiry_minute: Optional[int] = 5
    allowed_origin: Optional[str] = '*'
    production: Optional[bool] = False

    COOKIE_PATH: Optional[str] = "/"
    COOKIE_SAMESITE: Optional[str] = "lax"  # options: lax, strict, none for cross site
    COOKIE_DOMAIN: Optional[str] = None
    COOKIE_SECURE: Optional[bool] = False

    class Config:
        env_file = ".env"


settings = Settings()
