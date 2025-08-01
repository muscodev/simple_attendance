from fastapi import Request
from typing import Optional
import re
import hashlib
from datetime import datetime, timedelta
import time
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError
import logging
from .settings import settings


logger = logging.getLogger()


SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"


def create_token(payload: dict, expire_second: int = None) -> str:
    "Default NO expiry"
    payload = payload.copy()
    if expire_second is not None:
        payload["exp"] = time.time() + expire_second
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def validate_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError as e:
        logger.error(f"ExpiredSignatureError:{str(e)}")
        return None
    except JWTError as e:
        logger.error(f"JWTError:{str(e)}")        
        return None


def rotate_token(payload: dict, expires_delta: timedelta = None) -> str:
    return create_token(payload, expires_in=expires_delta)


def revoke_token(token: str):
    # Add to blacklist or ignore (if stateless)
    pass


def ip_from_request(request: Request):
    "Return ip address"
    x_forwarded_for = request.headers.get('x-forwarded-for')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # In case of multiple proxies
    else:
        ip = request.client.host
    return ip


def device_hash(request: Request):

    return hashlib.sha256(request.headers.get("user-agent").encode()).hexdigest()


def is_mobile(request: Request):

    ua = request.headers.get("user-agent")

    if re.search('Mobi|Android|iPhone|iPad|iPod', ua):
        return True

    return False

