
from fastapi import Cookie, HTTPException, status, Request
from datetime import datetime, timedelta
from jose import jwt
import time
from passlib.hash import pbkdf2_sha256
import base64
from enum import Enum
import hashlib
import logging
from .settings import settings
from ..utlis.sa import ip_from_request
from .utils import create_token

logger = logging.getLogger()


class Levels(Enum):
    OWNER = 'OWNER'
    ADMIN = 'ADMIN'
    EMPLOYEE = 'EMPLOYEE'


SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
EMPLOYEE_ACCESS_TOKEN_EXPIRE_MINUTES = 20*60


def create_agent_hash(request: Request):
    """This will create hash of user agent"""
    return {
        'UA': hashlib.sha256(request.headers.get("user-agent").encode()).hexdigest(),
        'IP': ip_from_request(request)
        }


def verify_password(plain, hashed):
    " verify the plain password with hashed password"
    return pbkdf2_sha256.verify(plain, hashed)


def get_password_hash(password):
    " Create a has using Cryptocontext"
    return pbkdf2_sha256.hash(password)


def create_owner_access_token(data: dict, expire_second: int = None):
    "create jwt token for and update level_ to the owner"
    data['level_'] = Levels.OWNER.value
    to_encode = data.copy()
    if expire_second:
        to_encode.update({"exp": time.time() + expire_second})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_admin_access_token(request: Request, data: dict, expire_second: int = None):
    "create jwt token for admin, and update level_ to the admin "
    data.update(create_agent_hash(request))
    data['level_'] = Levels.ADMIN.value
    to_encode = {k: base64.b64encode(str(v).encode("utf-8")).decode("utf-8")+'0' for k, v in data.items()}
    if expire_second:
        to_encode.update({"exp": time.time() + expire_second})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_employee_access_token(data: dict, expires_delta: timedelta = None):
    "create jwt token for and update level_ to the employee"

    data['level_'] = Levels.EMPLOYEE.value
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=EMPLOYEE_ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def validate_owner(request: Request, access_token: str = Cookie(None)):
    """
    validate owner access token and UA
    validate ip address TOBEDONE
    """

    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated (cookie missing)"
        )
    try:

        token = jwt.decode(access_token, SECRET_KEY, algorithms=ALGORITHM)
    except Exception as e:
        logger.debug(str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated (wrong signature))"
        )
    if not ('level_' in token and token['level_'] == Levels.OWNER.value):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated (not valid user))"
        )

    hash = create_agent_hash(request)
    if hash.get('UA') != token.get('UA'):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated (not valid device)"
        )
    # validate ip address , only allow the short session
    if hash.get('IP') != token.get('IP'):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session invalid, Login Again"
        )

    return True


async def validate_admin(request: Request, access_token_admin: str = Cookie(None)):
    """ 
    Validate admin access token and UA
    Validate tenant TOBEDONE
    """ 
    if access_token_admin is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated (cookie missing)"
        )
    try:
        token = jwt.decode(access_token_admin, SECRET_KEY, algorithms=ALGORITHM)
        token = {k: base64.b64decode(v[:-1].encode('utf-8')).decode('utf-8') for k, v in token.items() if k != 'exp'}
    except Exception as e:
        logger.debug(str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated (wrong signature))"
        )

    if not ('level_' in token and token['level_'] == Levels.ADMIN.value):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated (not valid user))"
        )

    ua = create_agent_hash(request)

    if ua['UA'] != token['UA']:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated (not valid device)"
        )
    if not token.get('tenant_id') or not token.get('id'):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated (informations are missing)"
        )
    return token

async def validate_employee(request: Request, access_token: str = Cookie(None)):
    """ 
    Validate admin access token and UA
    Validate tenant  TOBEDONE
    Validate employee status TOBEDONE
    """   
    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated (cookie missing)"
        )

    token = jwt.decode(access_token, SECRET_KEY, algorithms=ALGORITHM)

    if not ('level_' in token and token['level_'] == Levels.EMPLOYEE.value):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated (not valid user))"
        )   
    ua = create_agent_hash(request)

    if ua['UA'] != token['UA']:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated (not valid device)"
        )       

    return True
