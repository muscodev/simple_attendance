from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware
from api.sa.settings import settings
from .endpoints import employee, owner, admin
from .sa.auth import validate_owner


app = FastAPI(title="SimpleAttendance")

app.include_router(admin.router, prefix='/api')
app.include_router(employee.router, prefix='/api')
app.include_router(owner.router, prefix='/api', dependencies=[Depends(validate_owner)])
app.include_router(owner.router_no_auth, prefix='/api')

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origin.split(','),
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.get('/api')
async def home():
    return "Hello From AttendanceApp"
