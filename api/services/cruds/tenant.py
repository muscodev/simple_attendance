from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import func, desc
from typing import List
import uuid
from datetime import date, datetime, timedelta
from sqlalchemy import select
from ...models import (
    Tenant, TenantCreate, TenantUpdate,
    User, UserCreate, UserUpdate,
    Employee, EmployeeCreate, EmployeeUpdate,
    GeoMarking, GeoMarkingCreate, GeoMarkingUpdate,
    Attendance, AttendanceCreate
    )
from api.models.token import Token, TokenCreate, TokenUpdate
from .base import CRUDBase


class TenantRepo(CRUDBase[Tenant, TenantCreate, TenantUpdate]):

    async def deactivate(self, db: AsyncSession, id: uuid.UUID):
        tenant = await self.get(db, id)
        if not tenant:
            return None
        obj_in = TenantUpdate.model_validate(tenant)
        obj_in.is_active = False
        return await super().update(db, id, obj_in)

    async def activate(self, db: AsyncSession, id: uuid.UUID):
        tenant = await self.get(db, id)
        if not tenant:
            return None
        obj_in = TenantUpdate.model_validate(tenant)
        obj_in.is_active = True
        return await super().update(db, id, obj_in)


class userRepo(CRUDBase[User, UserCreate, UserUpdate]):

    async def deactivate(self, db: AsyncSession, id: uuid.UUID):
        user = await self.get(db, id)
        if not user: 
            return None                
        obj_in = UserUpdate.model_validate(user)
        obj_in.is_active = False
        return await super().update(db, id, obj_in)

    async def activate(self, db: AsyncSession, id: uuid.UUID):
        user = await self.get(db, id)
        if not user: 
            return None        
        obj_in = UserUpdate.model_validate(user)
        obj_in.is_active = True
        return await super().update(db, id, obj_in)

    async def get_user_by_email(self, db: AsyncSession, email: str)-> User | None:
        """ get user details with email(username) or None"""
        result = await db.execute(select(self.model).where(self.model.email == email))
        return result.scalar_one_or_none()


class EmployeeRepo(CRUDBase[Employee, EmployeeCreate, EmployeeUpdate]):

    async def get(self, db: AsyncSession, tenant_id: uuid.UUID, id: uuid.UUID):
        return await self._get(db, select(self.model).where(self.model.tenant_id == tenant_id))
    
    async def get_all(self, db, tenant_id: uuid.UUID):
        return await super()._get_all(db, query=select(self.model).where(self.model.tenant_id == tenant_id))
    
    async def update(self, db: AsyncSession, tenant_id: uuid.UUID, id: uuid.UUID, obj_in):
        return await super().update(db, id, obj_in, query=select(self.model).where(self.model.tenant_id == tenant_id))

    async def deactivate(self, db: AsyncSession, tenant_id: uuid.UUID,  id: uuid.UUID):
        employee = await self.get(db, tenant_id, id)
        if not employee: 
            return None
        obj_in = EmployeeUpdate.model_validate(employee)
        obj_in.is_active = False
        return await super().update(db, id, obj_in)

    async def activate(self, db: AsyncSession, tenant_id: uuid.UUID,  id: uuid.UUID):
        employee = await self.get(db, tenant_id, id)
        if not employee: 
            return None        
        obj_in = EmployeeUpdate.model_validate(employee)
        obj_in.is_active = True
        return await super().update(db, id, obj_in)


class TokenRepo(CRUDBase[Token, TokenCreate, TokenUpdate]):
    
    async def get_token_by(self, db: AsyncSession, tenant_id: uuid.UUID, employee_id: uuid.UUID, token_type: str):
        return await self._get(
            db,
            select(
                Token
            ).where(
                Token.tenant_id == tenant_id
            ).where(
                Token.employee_id == employee_id
            ).where(
                Token.token_type == token_type
            )

        )
    async def get_token_token(self, db: AsyncSession, token: str):
        return await self._get(
            db,
            select(
                Token
            ).where(
                Token.token_hash == token
            )
            
        )


class GeoMarkingRepo(CRUDBase[GeoMarking, GeoMarkingCreate, GeoMarkingUpdate]):

    async def get_all_by_tenant(self, db: AsyncSession, tenant_id: uuid.UUID):
        return await self._get_all(
            db,
            select(
                GeoMarking
            ).where(
                GeoMarking.tenant_id == tenant_id
            )
        )

    async def get(self, db: AsyncSession, tenant_id: uuid.UUID, id: uuid.UUID):
        return await self._get(
            db,
            select(
                GeoMarking
            ).where(
                GeoMarking.tenant_id == tenant_id
            ).where(
                GeoMarking.id == id
            )

        )


class AttendanceRepo(CRUDBase[Attendance, AttendanceCreate, AttendanceCreate]):

    async def get_today(
        self,
        db: AsyncSession,
        tenant_id: uuid.UUID,
        employee_id: uuid.UUID
    ) -> List[Attendance]:
        return await self._get_all(
            db,
            select(
                Attendance
            ).where(
                Attendance.tenant_id == tenant_id
            ).where(
                Attendance.employee_id == employee_id
            ).where(
                func.date(Attendance.timestamp) == date.today()
            )
        )

    async def last_mark_today(
        self,
        db: AsyncSession,
        tenant_id: uuid.UUID,
        employee_id: uuid.UUID
    ) -> Attendance:

        today = date.today()  # <class 'datetime.date'>
        start_of_today = datetime.combine(today, datetime.min.time())
        start_of_tomorrow = start_of_today + timedelta(days=1)
        query = (
            select(Attendance)
            .where(Attendance.tenant_id == tenant_id)
            .where(Attendance.employee_id == employee_id)
            .where(Attendance.timestamp >= start_of_today)
            .where(Attendance.timestamp < start_of_tomorrow)
            .order_by(desc(Attendance.timestamp))
            .limit(1)
        )
        return await self._get(db, query)


tenant_repo = TenantRepo(Tenant)
user_repo = userRepo(User)
employee_repo = EmployeeRepo(Employee)
token_repo = TokenRepo(Token)
geomarking_repo = GeoMarkingRepo(GeoMarking)
attendance_repo = AttendanceRepo(Attendance)
