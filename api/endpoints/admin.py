from fastapi import (
    APIRouter,HTTPException,
    Request, Response, Depends,status
    )
import logging
import uuid
from ..schema.general import LoginPost
from ..sa.settings import settings
from ..sa.auth import (
    create_admin_access_token,
    verify_password
    )
from ..sa.db import get_session, AsyncSession
from ..sa.depend import get_admin
from ..services.cruds.tenant import (
    user_repo, User, employee_repo,
    Employee, EmployeeCreate, EmployeeUpdate,
    GeoMarking, GeoMarkingCreate, GeoMarkingUpdate, geomarking_repo
    )
from api.services.employee_service import employee_service
from api.models import EmployeeCreateSchema


logger = logging.getLogger()
router = APIRouter(tags=['Admin'])


@router.post('/admin/login')
async def admin_login(
    request: Request,
    credential: LoginPost,
    response: Response,
    db: AsyncSession = Depends(get_session)
):
    try:
        admin: User = await user_repo.get_user_by_email(db, credential.username)
        if not admin or not admin.is_active or not verify_password(credential.password, admin.password_hash):
            raise HTTPException(status_code=400, detail="Invalid credentials or inactive")
    except Exception as e:
        logger.debug(str(e))
        raise HTTPException(status_code=400, detail="invalid credentials")
    payload = {'id': admin.id, 'tenant_id': admin.tenant_id}
    token = create_admin_access_token(request, payload, settings.admin_access_token_expiry_minute*60)
    response.set_cookie(
        "access_token_admin", 
        token, 
        httponly=True,
        max_age=settings.admin_access_token_expiry_minute,
        path=settings.COOKIE_PATH,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE
        )
    return {"access_token": token}


@router.post('/admin/logout')
def logout(response: Response):
    response.delete_cookie("access_token_admin")  # or your cookie name
    return {"message": "Logged out"}


@router.get('/admin/me')
async def get_me(admin=Depends(get_admin)):
    return admin


# user apis
@router.post('/admin/tenant/employee')
async def create_tenant_employee(employee: EmployeeCreateSchema, admin: User = Depends(get_admin), db: AsyncSession = Depends(get_session)):
    employee_create = EmployeeCreate.model_validate(
        {
         **employee.model_dump(),
         'tenant_id': admin.tenant_id
         }
    )
    # employee_create.tenant_id = admin.tenant_id
    return await employee_repo.create(db, employee_create)


@router.get('/admin/tenant/employee/{id}')
async def get_tenant_employee(id: uuid.UUID, admin: User = Depends(get_admin), db: AsyncSession = Depends(get_session)):
    return await employee_repo.get(db, admin.tenant_id, id)


@router.put('/admin/tenant/employee/{id}/deactivate')
async def deactivate_tenant_employee(id: uuid.UUID, admin: User = Depends(get_admin), db: AsyncSession = Depends(get_session)):
    return await employee_repo.deactivate(db, admin.tenant_id, id)


@router.put('/admin/tenant/employee/{id}/activate')
async def activate_tenant_employee(id: uuid.UUID, admin: User = Depends(get_admin), db: AsyncSession = Depends(get_session)):
    return await employee_repo.activate(db, admin.tenant_id, id)


@router.get('/admin/tenant/employees')
async def get_tenant_employees(admin: User = Depends(get_admin), db: AsyncSession = Depends(get_session)):
    return await employee_repo.get_all(db, admin.tenant_id)


@router.get('/admin/tenant/employees/status')
async def get_tenant_employees(admin: User = Depends(get_admin), db: AsyncSession = Depends(get_session)):
    return await employee_repo.get_employee_status(db,admin.tenant_id)


@router.post('/admin/tenant/employees/{id}/idtoken')
async def get_tenant_employee_id_token(
    id: uuid.UUID,
    admin: User = Depends(get_admin),
    db: AsyncSession = Depends(get_session),
):

    token = await employee_service.create_employee_token(db, admin.tenant_id, id)
    if token:
        return token

    raise HTTPException(status.HTTP_208_ALREADY_REPORTED, "token not generated")

@router.delete('/admin/tenant/employees/{id}/session')
async def clear_employee_seesion_in_db(
    id: uuid.UUID,
    admin: User = Depends(get_admin),
    db: AsyncSession = Depends(get_session),
):
    try:

        cleared = await employee_service.clear_session(admin.tenant_id, id, db)
        if cleared:
            return "OK"
    except Exception as e:
        logger.error(str(e), stack_info=True)

        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "token not cleared")


# Geomarking service
@router.post('/admin/tenants/geomarking')
async def create_tenant_geomarking(geolocation: GeoMarkingCreate, admin: User = Depends(get_admin), db: AsyncSession = Depends(get_session)):
    geolocation.tenant_id = admin.tenant_id
    return await geomarking_repo.create(db, geolocation)


@router.get('/admin/tenant/geomarking/{id}')
async def get_tenant_geomarking(id: uuid.UUID, admin: User = Depends(get_admin), db: AsyncSession = Depends(get_session)):
    return await geomarking_repo.get(db, admin.tenant_id, id)


@router.get('/admin/tenant/geomarking')
async def get_tenant_geomarkings(admin: User = Depends(get_admin), db: AsyncSession = Depends(get_session)):
    return await geomarking_repo.get_all_by_tenant(db, admin.tenant_id)

@router.put('/admin/tenant/geomarking/{id}')
async def update_tenant_geomarking(id: uuid.UUID, update_location: GeoMarkingUpdate, admin: User = Depends(get_admin), db: AsyncSession = Depends(get_session)):
    return await geomarking_repo.update(db, id, update_location)
