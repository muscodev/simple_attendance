from fastapi import Cookie, Request, Depends, HTTPException, status, Response
import logging
import uuid
from ..services.cruds.tenant import user_repo
from api.services.employee_service import employee_service
from .auth import validate_admin
from .db import get_session, AsyncSession
from .utils import device_hash, is_mobile
from api.sa.settings import settings

logger = logging.getLogger()


async def get_admin(request: Request, token: dict = Depends(validate_admin), db: AsyncSession = Depends(get_session) ):
    """
    get active admin from tenant and id
    """
    try:

        admin = await user_repo.get(db, id=uuid.UUID(token.get('id')))

        if not admin or not admin.is_active or admin.tenant_id != uuid.UUID(token.get('tenant_id')) :
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated (not valid active user))"
            )
        return admin
    except Exception as e:
        logger.debug(str(e))
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated (admin not validated))"
            )


async def get_employee(
        request: Request,
        response: Response,
        db: AsyncSession = Depends(get_session),
        act_employee: str = Cookie(None),
        rft_employee: str = Cookie(None)
    ):
    """
    get active employee from session
    """
    try:

        # handle missing cookies

        if rft_employee is None:
            logger.error('refresh token is missing')            
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing Session"
            )    
        
        # if not mobile device raise error        
        if not is_mobile(request):
            logger.error('invalid mobile device')              
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Device"
            )      
        device = device_hash(request)

        token, new_session = await employee_service.validate_employee_session(db, act_employee, rft_employee, device)
        if token is None:
            logger.error('session validation error')  
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid session"
            )

        # get employee details

        employee = await employee_service.employee_repo.get(
            db,
            token.tenant_id,
            token.employee_id
        )

        if not employee or not employee.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="account is deactive or missing"
            )
        if new_session:
            response.set_cookie(
                "act_employee", token.token_hash, httponly=True,
                max_age=settings.employee_access_token_expiry_minute*60,
                path=settings.COOKIE_PATH,
                secure=settings.COOKIE_SECURE,
                samesite=settings.COOKIE_SAMESITE
            )  
        return employee
           

    except Exception as e:
        # raise
        logger.error(str(e),exc_info=1)
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated (some auth issue))"
            )
