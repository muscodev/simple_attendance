import uuid

from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import UserCreateSchema
from ..sa.auth import (
    Levels,
    create_agent_hash,
    create_owner_access_token,
    get_password_hash,
)
from ..sa.db import get_session
from ..sa.settings import settings
from ..schema.general import LoginPost
from ..services.cruds.tenant import TenantCreate, UserCreate, tenant_repo, user_repo

router_no_auth = APIRouter(tags=["Owner"])

router = APIRouter(tags=["Owner"])


@router_no_auth.get("/owner/login", response_class=HTMLResponse)
async def owner_login(request: Request):
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Owner Login</title>
        <style>
            body { font-family: Arial; background-color: #f7f7f7; padding: 50px; }
            .login-box {
                background-color: white;
                max-width: 400px;
                margin: auto;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
            input[type="text"], input[type="password"] {
                width: 100%;
                padding: 10px;
                margin: 10px 0;
                border-radius: 4px;
                border: 1px solid #ccc;
            }
            button {
                padding: 10px 20px;
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                width: 100%;
            }
        </style>
    </head>
    <body>
        <div class="login-box">
            <h2>Owner Login</h2>
            <form action="/api/owner/login" method="post">
                <label for="username">Username:</label><br>
                <input type="text" id="username" name="username" required><br>

                <label for="password">Password:</label><br>
                <input type="password" id="password" name="password" required><br><br>

                <button type="submit">Login</button>
            </form>
        </div>
    </body>
    </html>
    """


@router_no_auth.post("/owner/login")
async def owner_login_post(
    request: Request,
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
):

    if settings.owner_username != username or settings.owner_password != password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    payload = create_agent_hash(request)
    token = create_owner_access_token(
        payload, settings.owner_access_token_expiry_minute * 60
    )
    response.set_cookie(
        "access_token",
        token,
        httponly=True,
        max_age=settings.owner_access_token_expiry_minute * 60,
    )
    return {"access_token": token}


@router.post("/owner/tenant")
async def create_tenant(tenant: TenantCreate, db: AsyncSession = Depends(get_session)):
    return await tenant_repo.create(db, tenant)


@router.get("/owner/tenant/{id}")
async def get_tenant(id: uuid.UUID, db: AsyncSession = Depends(get_session)):
    return await tenant_repo.get(db, id)


@router.get("/owner/tenant/{id}/deactivate")
async def deactivate_tenant(id: uuid.UUID, db: AsyncSession = Depends(get_session)):
    return await tenant_repo.deactivate(db, id)


@router.get("/owner/tenant/{id}/activate")
async def activate_tenant(id: uuid.UUID, db: AsyncSession = Depends(get_session)):
    return await tenant_repo.activate(db, id)


@router.get("/owner/tenants")
async def get_tenants(db: AsyncSession = Depends(get_session)):
    return await tenant_repo.get_all(db)


# user apis
@router.post("/owner/tenants/user")
async def create_tenant_user(
    tenant_user: UserCreateSchema, db: AsyncSession = Depends(get_session)
):
    hashed_pw = get_password_hash(tenant_user.password)
    # Create the real user create model
    user_data = UserCreate(
        tenant_id=tenant_user.tenant_id,
        email=tenant_user.email,
        password_hash=hashed_pw,
        role=tenant_user.role,
        is_active=tenant_user.is_active,
    )

    return await user_repo.create(db, user_data)


@router.get("/owner/tenant/{tenant_id}/user/{id}")
async def get_tenant_user(
    tenant_id: uuid.UUID, id: uuid.UUID, db: AsyncSession = Depends(get_session)
):
    return await user_repo.get(db, id)


@router.get("/owner/tenant/{tenant_id}/user/{id}/deactivate")
async def deactivate_tenant_user(
    tenant_id: uuid.UUID, id: uuid.UUID, db: AsyncSession = Depends(get_session)
):
    return await user_repo.deactivate(db, id)


@router.get("/owner/tenant/{tenant_id}/user/{id}/deactivate")
async def activate_tenant_user(
    tenant_id: uuid.UUID, id: uuid.UUID, db: AsyncSession = Depends(get_session)
):
    return await user_repo.activate(db, id)


@router.get("/owner/tenant/{tenant_id}/users")
async def get_tenant_users(db: AsyncSession = Depends(get_session)):
    return await user_repo.get_all(db)
