# models.py
import uuid
from datetime import datetime, timezone
from typing import Annotated, Optional

from pydantic import BeforeValidator
from sqlmodel import Column, DateTime, Field, SQLModel

from .token import Token


def ensure_utc(v: datetime) -> datetime:
    if isinstance(v, str):
        v = datetime.fromisoformat(v)

    if v.tzinfo is None:
        return v.replace(tzinfo=timezone.utc)
    return v.astimezone(timezone.utc)


UTCDatetime = Annotated[datetime, BeforeValidator(ensure_utc)]


# Base model (shared fields)
class TenantBase(SQLModel):
    name: str
    icon: str
    is_active: bool = True


# Create model (input for POST)
class TenantCreate(TenantBase):
    pass


# Update model (input for PATCH/PUT - all optional)
class TenantUpdate(SQLModel):
    name: Optional[str] = None
    icon: Optional[str] = None
    is_active: Optional[bool] = None


# Full model / DB model
class Tenant(TenantBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)


class UserBase(SQLModel):
    tenant_id: uuid.UUID = Field(foreign_key="tenant.id")
    email: str
    password_hash: str
    role: str = "admin"
    is_active: bool = True


class UserCreate(UserBase):
    pass


#  Used when creating a new user
class UserCreateSchema(SQLModel):
    tenant_id: uuid.UUID
    email: str
    password: str
    role: str = "admin"
    is_active: bool = True


#  Used when updating a user (PATCH/PUT)
class UserUpdate(SQLModel):
    email: Optional[str] = None
    password_hash: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None


#  ORM/DB model
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)


class EmployeeBase(SQLModel):
    employee_no: str
    tenant_id: uuid.UUID = Field(foreign_key="tenant.id")
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool = True


class EmployeeCreateSchema(SQLModel):
    employee_no: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool = True


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(SQLModel):
    employee_no: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None


class Employee(EmployeeBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)


class EmployeeRead(EmployeeBase):
    id: uuid.UUID
    created_at: datetime


# Base model: shared fields (no table)
class AttendanceBase(SQLModel):
    tenant_id: uuid.UUID = Field(foreign_key="tenant.id")
    employee_id: uuid.UUID = Field(foreign_key="employee.id")
    timestamp: UTCDatetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    latitude: float
    longitude: float
    geo_marking_id: uuid.UUID = Field(foreign_key="geomarking.id")
    distance_from_marking: float
    status: str = Field(default="IN", max_length=5)


# Model for creation
class AttendanceCreate(AttendanceBase):
    pass


# Model for reading/getting (typically includes ID and timestamp fields)
class AttendanceRead(AttendanceBase):
    id: uuid.UUID


# Actual DB model
class Attendance(AttendanceBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


# ✅ Shared Base (for Create/Update)
class GeoMarkingBase(SQLModel):
    name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    radius_meters: Optional[float] = 2000


# ✅ Create model (all fields required except radius_meters)
class GeoMarkingCreate(GeoMarkingBase):
    tenant_id: uuid.UUID
    name: str
    latitude: float
    longitude: float
    active: bool = Field(default=True)


class GeoMarkingCreateschema(GeoMarkingBase):
    pass


# ✅ Read model
class GeoMarkingRead(GeoMarkingBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    name: str
    latitude: float
    longitude: float
    radius_meters: float
    created_at: datetime


#  Update model (all fields optional)
class GeoMarkingUpdate(GeoMarkingBase):
    pass


#  Main DB model
class GeoMarking(GeoMarkingBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    tenant_id: uuid.UUID = Field(foreign_key="tenant.id")
    created_at: datetime = Field(default_factory=datetime.now)
