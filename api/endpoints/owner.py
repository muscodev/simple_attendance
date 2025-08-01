from fastapi import APIRouter, HTTPException, Request, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from ..schema.general import LoginPost
from ..sa.settings import settings
from ..sa.db import get_session
from ..sa.auth import (
    create_owner_access_token,
    get_password_hash,
    Levels,
    create_agent_hash,
    )

from ..services.cruds.tenant import (
    tenant_repo, TenantCreate,
    user_repo, UserCreate
) 
from ..models import UserCreateSchema

router_no_auth = APIRouter(tags=['Owner'])

router = APIRouter(tags=['Owner'])


@router_no_auth.post('/owner/login')
async def owner_login(request: Request, credential: LoginPost, response: Response):

    if settings.username != credential.username or settings.password != credential.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    payload = create_agent_hash(request)
    token = create_owner_access_token(data=payload)
    response.set_cookie("access_token", token, httponly=True, max_age=3600 * 24)
    return {"access_token": token}


@router.post('/owner/tenant')
async def create_tenant(tenant: TenantCreate, db: AsyncSession= Depends(get_session)):
    return await tenant_repo.create(db, tenant)


@router.get('/owner/tenant/{id}')
async def get_tenant(id: uuid.UUID, db: AsyncSession= Depends(get_session)):
    return await tenant_repo.get(db, id)



@router.get('/owner/tenant/{id}/deactivate')
async def deactivate_tenant(id: uuid.UUID, db: AsyncSession= Depends(get_session)):
    return await tenant_repo.deactivate(db, id)


@router.get('/owner/tenant/{id}/activate')
async def activate_tenant(id: uuid.UUID, db: AsyncSession= Depends(get_session)):
    return await tenant_repo.activate(db, id)


@router.get('/owner/tenants')
async def get_tenants(db: AsyncSession = Depends(get_session)):
    return await tenant_repo.get_all(db)



# user apis
@router.post('/owner/tenants/user')
async def create_tenant_user(tenant_user: UserCreateSchema, db: AsyncSession = Depends(get_session)):
    hashed_pw = get_password_hash(tenant_user.password)
        # Create the real user create model
    user_data = UserCreate(
        tenant_id=tenant_user.tenant_id,
        email=tenant_user.email,
        password_hash=hashed_pw,
        role=tenant_user.role,
        is_active=tenant_user.is_active
    )

    return await user_repo.create(db, user_data)


@router.get('/owner/tenant/{tenant_id}/user/{id}')
async def get_tenant_user(tenant_id: uuid.UUID, id: uuid.UUID, db: AsyncSession = Depends(get_session)):
    return await user_repo.get(db, id)


@router.get('/owner/tenant/{tenant_id}/user/{id}/deactivate')
async def deactivate_tenant_user(tenant_id: uuid.UUID, id: uuid.UUID, db: AsyncSession = Depends(get_session)):
    return await user_repo.deactivate(db, id)


@router.get('/owner/tenant/{tenant_id}/user/{id}/deactivate')
async def activate_tenant_user(tenant_id: uuid.UUID, id: uuid.UUID, db: AsyncSession = Depends(get_session)):
    return await user_repo.activate(db, id)


@router.get('/owner/tenant/{tenant_id}/users')
async def get_tenant_users(db: AsyncSession = Depends(get_session)):
    return await user_repo.get_all(db)
