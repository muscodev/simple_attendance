import logging

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse

from api.sa.settings import settings

from .endpoints import admin, employee, owner
from .sa.auth import validate_owner

logger = logging.getLogger("sa")
logging.basicConfig(level=logging.DEBUG)

if settings.production:
    logger.info("App is runnnig on production..")
    app = FastAPI(
        title="SimpleAttendance", docs_url=None, redoc_url=None, openapi_url=None
    )

    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui(user=Depends(validate_owner)):
        return get_swagger_ui_html(
            openapi_url="/openapi.json",
            title="Admin Docs",
        )

    @app.get("/openapi.json", include_in_schema=False)
    async def get_open_api_endpoint(user=Depends(validate_owner)):
        return JSONResponse(
            get_openapi(
                title="FastAPI",
                version="1.0.0",
                routes=app.routes,
            )
        )


if not settings.production:
    logging.info("App is runnnig on development..")
    app = FastAPI(
        title="SimpleAttendance",
    )

app.include_router(admin.router, prefix="/api")
app.include_router(employee.router, prefix="/api")
app.include_router(
    owner.router,
    prefix="/api",
    dependencies=[Depends(validate_owner)],
)
app.include_router(owner.router_no_auth, prefix="/api")


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origin.split(','),
    allow_methods=settings.allow_methods.split(','),
    allow_headers=settings.allow_headers.split(','),
    allow_credentials=True,
)

