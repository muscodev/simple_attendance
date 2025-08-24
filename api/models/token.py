import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel, UniqueConstraint


# --- Table Model ---
class Token(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    tenant_id: uuid.UUID = Field(foreign_key="tenant.id")
    employee_id: uuid.UUID = Field(foreign_key="employee.id")
    token_type: str = "access_token_employee"
    token_hash: str
    device_hash: str
    expires_at: datetime
    used_at: Optional[datetime] = None
    ip_address: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    __table_args__ = (
        UniqueConstraint("employee_id", "token_type", name="uq_employee_tokens"),
    )


# --- Create Model ---
class TokenCreate(SQLModel):
    tenant_id: uuid.UUID
    employee_id: uuid.UUID
    token_type: Optional[str] = "access_token_employee"
    token_hash: str
    device_hash: str
    expires_at: datetime
    ip_address: Optional[str] = None


# --- Update Model ---
class TokenUpdate(SQLModel):
    used_at: Optional[datetime] = None
    ip_address: Optional[str] = None


# --- Read/Out Model ---
class TokenRead(SQLModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    employee_id: uuid.UUID
    token_type: str
    token_hash: str
    device_hash: str
    expires_at: datetime
    used_at: Optional[datetime]
    ip_address: Optional[str]
    created_at: datetime
