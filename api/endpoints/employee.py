from fastapi import APIRouter, HTTPException, Response, Depends, Request, status
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from ..schema.general import Coordinate
from api.services.cruds.tenant  import geomarking_repo, AttendanceCreate
from api.models import Employee
from api.services.employee_service import employee_service
from api.sa.settings import settings
from api.sa.db import AsyncSession, get_session
from api.sa.depend import get_employee
from api.sa.utils import device_hash, is_mobile
from ..utlis import geo
import logging

router = APIRouter(tags=["Employee"])
logger = logging.getLogger()


@router.get("/e/t/{token}")
async def employee_login(
    request: Request,
    token: str,
    response: Response,
    db: AsyncSession = Depends(get_session),
):

    # if not mobile device raise error        
    if not is_mobile(request):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Device"
        )

    data = employee_service.validate_employee_token(token=token)
    # create refreshtoken and access token
    if not data:
        raise HTTPException(
            status_code=400, detail="Invalid token validation failed"
        )
    try:

        refresh, access = await employee_service.get_tokens(
            data.tenant_id,
            data.employee_id,
            device_hash(request=request),
            db
        )
        response.set_cookie(
            "act_employee", access, httponly=True,
            max_age=settings.employee_access_token_expiry_minute,
            path=settings.COOKIE_PATH,
            secure=settings.COOKIE_SECURE,
            samesite=settings.COOKIE_SAMESITE
        )
        response.set_cookie(
            "rft_employee",
            refresh,
            httponly=True,
            path=settings.COOKIE_PATH,
            secure=settings.COOKIE_SECURE,
            samesite=settings.COOKIE_SAMESITE
        )        
        return {'refresh': refresh, 'access': access}
    
    except IntegrityError:
        logger.info("employee login attempt failed due to token already exist")
        raise HTTPException(status_code=400, detail="token login got error")


@router.get("/employee/me")
async def get_me(
    employee: Employee = Depends(get_employee),
    db: AsyncSession = Depends(get_session),
):
    states = await employee_service.get_state(employee.tenant_id, employee.id, db)

    return {
        **employee.model_dump(),
        **states
    }


@router.post("/employee/markin")
async def mark_in(
    coordinates: Coordinate,
    employee: Employee = Depends(get_employee),
    db: AsyncSession = Depends(get_session),
):
    attenadance, near_geo_mark = await employee_service.mark_attendance_in(
        employee,
        coordinates,
        db
    )

    if attenadance is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="invalid option")
    response = attenadance.model_dump()
    response.update({"place": near_geo_mark.name})
    return response
    # return {
    #     "time": datetime.now().isoformat(),
    #     "state": "IN",
    #     "nearest": {"place": nearest.model_dump(), "dist": dist},
    # }


@router.post("/employee/markout")
async def mark_out(
    coordinates: Coordinate,
    employee: Employee = Depends(get_employee),
    db: AsyncSession = Depends(get_session),
):

    attenadance, near_geo_mark = await employee_service.mark_attendance_out(
        employee,
        coordinates,
        db
    )

    if attenadance is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="invalid option"
        )
    response = attenadance.model_dump()
    response.update({"place": near_geo_mark.name})
    return response

@router.get("/employee/nears")
async def get_near_locations():
    return
