from dataclasses import dataclass, field
from typing import Optional, Tuple
import uuid
import logging
import time
from api.services.cruds.tenant import (
    employee_repo, EmployeeRepo,attendance_repo, AttendanceRepo, Attendance,  
    TokenRepo, token_repo, TokenCreate, Token,AttendanceCreate, Employee, GeoMarking,
    geomarking_repo, 
    )
from api.sa.utils import (
    create_token, validate_token,
    rotate_token, revoke_token
    )
from datetime import datetime
from api.utlis import geo
from api.sa.auth import Levels
from api.sa.db import AsyncSession
from api.sa.settings import settings
from api.schema.general import Coordinate
from pydantic import BaseModel

logger = logging.getLogger()


class JwtToken(BaseModel):
    employee_id: str
    tenant_id: str
    employee_id: str
    purpose: str
    level_: str


@dataclass(slots=True, frozen=True)
class EmployeeService:
    employee_repo: EmployeeRepo = field(default=employee_repo, init=False, repr=False)
    token_repo: TokenRepo = field(default=token_repo, init=False, repr=False)
    attendance_repo: AttendanceRepo = field(default=attendance_repo, init=False, repr=False)
    
    # 1. Create a login or attendance token (short-lived)
    async def create_employee_token(
            self,
            db,tenant_id: uuid.UUID, employee_id: uuid.UUID) -> str:
        """Create login token if no refresh_token is issued already"""
        token = await token_repo.get_token_by(db, tenant_id, employee_id, 'refresh_token_employee')
        if token:
            logger.info("refresh token already available, cannot create new login token")
            return None
        payload = JwtToken(
            employee_id=str(employee_id),
            tenant_id=str(tenant_id),
            level_=Levels.EMPLOYEE.value,
            purpose="login",
        )
        return create_token(
            payload.model_dump(), expire_second=60
        )  # 1 minute

    # 2. Validate the token and return employee_id
    def validate_employee_token(self, token: str) -> JwtToken | None:
        
        data = validate_token(token)
        if not data:
            return None
   
        return JwtToken(**data)

    # 3. Create access token (for full login or long session)
    async def create_access_token(self, tenant: uuid.UUID, employee_id: uuid.UUID) -> str:
        payload = {"employee_id": str(employee_id), "tenant_id": str(tenant), "level_": Levels.EMPLOYEE.value, "purpose": "auth"}
        return create_token(payload, expire_second=60)  # 24 hrs

    async def create_refresh_token(self, tenant: uuid.UUID, employee_id: uuid.UUID) -> str:
        payload = {"employee_id": str(employee_id), "tenant_id": str(tenant),"level_": Levels.EMPLOYEE.value, "purpose": "auth_refresh"}
        return create_token(payload) 

    def validate_access_token(self, token: str = None) -> JwtToken | None:
        if token is None:
            return None
        data = validate_token(token)
        if not data or data.get("purpose") != "auth":
            return None
        return JwtToken(**data) if data is not None and data.get("level_") == Levels.EMPLOYEE.value else None

    def validate_refresh_token(self, token: str = None) -> JwtToken | None:
        """ Retun True|None"""
        if token is None:
            return None        
        data = validate_token(token)
        if not data or data.get("purpose") != "auth_refresh":
            return None
        return JwtToken(**data) if data is not None and data.get("level_") == Levels.EMPLOYEE.value else None

    async def validate_employee_session(
        self,
        db: AsyncSession,
        access_token: str,
        refresh_token: str,
        device_hash: str
    ) -> Token | None:
        # jwt verify
        data = self.validate_access_token(access_token)

        if data is None:
            logger.error("jwt access token expired or missing")
            # jwt expied 
            # validate refresh jwt token
            refresh = self.validate_refresh_token(refresh_token)
            
            # expired refresh token
            if refresh is None:
                logger.error("jwt refresh token expired or missing")
            # return expired please contact Admin
                return None
            
            # valid refresh token
            # verify token in database
            refresh_token_db = await self.get_refresh_token(
                uuid.UUID(refresh.tenant_id), 
                uuid.UUID(refresh.employee_id),
                db
                )
            # validate device
            if refresh_token_db.device_hash != device_hash:
                logger.debug("refresh token device and current active device are not matching")
                return None
            # if available
            if refresh_token_db is not None:
                # delete access token in database
                access_token = await self.get_access_token(
                    refresh_token_db.tenant_id,
                    refresh_token_db.employee_id,
                    db
                )
                await self.token_repo.delete(db, access_token.id)                
            # create new access token
                new_access_token_create = await self.create_access_token( 
                    refresh_token_db.tenant_id,
                    refresh_token_db.employee_id   
                )
            # store token in database

                new_access_token = await self.store_access_token(
                    new_access_token_create,
                    refresh_token_db.tenant_id,
                    refresh_token_db.employee_id,
                    device_hash,
                    db
                )
                logger.debug("new access token generated")
            # set access token in response
                return new_access_token
            # return Token details
        
        # on access jwt verified

        # check token availablity in database
        access_token = await self.get_access_token(
            uuid.UUID(data.tenant_id), uuid.UUID(data.employee_id), db
        )
        if not access_token and access_token.device_hash != device_hash:
            return None
        return access_token
        # return token details

    async def get_tokens(
        self,
        tenant: uuid.UUID, 
        employee_id: uuid.UUID,
        device_hash: str,
        db: AsyncSession
    ) -> Tuple[str, str]:

        refresh = await self.create_refresh_token(
            tenant,
            employee_id,
        )
        access = await self.create_access_token(
            tenant,
            employee_id,
        )

        # store access token and refresh token
        await self.store_refresh_token(
            refresh,
            tenant,
            employee_id,
            device_hash,
            db,
        )
        await self.store_access_token(
            access,
            tenant,
            employee_id,
            device_hash,
            db,
        )
 
        return refresh, access

    #  Store access token in database
    async def store_access_token(
        self,
        access: str,
        tenant: uuid.UUID,
        employee_id: uuid.UUID,
        device_hash: str,
        db: AsyncSession
    ) -> str:
        new_token = TokenCreate(
            tenant_id=tenant,
            employee_id=employee_id,
            token_type='access_token_employee',
            token_hash=access,
            device_hash=device_hash,
            expires_at=time.time() + 5*60
        )
        return await token_repo.create(db, new_token)

    #  Store refresh token in database
    async def store_refresh_token(
        self,
        refresh: str,
        tenant: uuid.UUID,
        employee_id: uuid.UUID,
        device_hash: str,
        db: AsyncSession
    ) -> str:
        new_token = TokenCreate(
            tenant_id=tenant,
            employee_id=employee_id,
            token_type='refresh_token_employee',
            token_hash=refresh,
            device_hash=device_hash,
            expires_at=time.time() + 60
        )
        return await token_repo.create(db, new_token)

    #  Get access token in database
    async def get_access_token(
        self,
        tenant: uuid.UUID,
        employee_id: uuid.UUID,
        db: AsyncSession
    ) -> Token | None:
        return await self.token_repo.get_token_by(
            db,
            tenant,
            employee_id,
            'access_token_employee'
        )

    #  Get refresh token in database
    async def get_refresh_token(
        self,
        tenant: uuid.UUID,
        employee_id: uuid.UUID,
        db: AsyncSession
    ) -> Token | None:
        return await self.token_repo.get_token_by(
            db,
            tenant,
            employee_id,
            'refresh_token_employee'
        )

    # 4. Remove (revoke) token (log out or session expire)
    async def clear_session(
        self,
        tenant: uuid.UUID,
        employee_id: uuid.UUID,
        db: AsyncSession
    ):
        access_token = await self.get_access_token(
                    tenant,
                    employee_id,
                    db
                )

        refresh_token = await self.get_refresh_token(
                    tenant,
                    employee_id,
                    db
                )

        if access_token:

            await self.token_repo.delete(db, access_token.id)
        if refresh_token:

            await self.token_repo.delete(db, refresh_token.id)

        return True

    # 4. Remove (revoke) token (log out or session expire)
    async def remove_access_token(self, token: str) -> None:
        revoke_token(token)  # Maybe add to denylist or mark in DB

    # 5. Rotate token (refresh -> new token)
    async def rotate_access_token(self, old_token: str) -> Optional[str]:
        payload = validate_token(old_token)
        if not payload:
            return None
        new_payload = {**payload}
        return rotate_token(new_payload)

    # 6. Mark attendance "in"
    async def mark_attendance_in(
        self,
        employee: Employee,
        coordinates: Coordinate,
        db: AsyncSession
    ) -> Tuple[Attendance, GeoMarking] | Tuple[None, None]:
        marked_locations = await geomarking_repo.get_all_by_tenant(
            db,
            employee.tenant_id
        )
        nearest, dist = None, 0
        if marked_locations:
            nearest, dist = geo.find_nearest(
                marked_locations,
                coordinates.model_dump(),
                location_extract_method=lambda loc: (loc.latitude, loc.longitude)
            )
        obj_in = AttendanceCreate(
            tenant_id=employee.tenant_id,
            employee_id=employee.id,
            timestamp=datetime.now(),
            latitude=coordinates.lat,
            longitude=coordinates.lon,
            geo_marking_id=nearest.id if nearest else None,
            distance_from_marking=dist
        )
        # verify the last status of attendance
        _, last_mark = await self.attendance_repo.last_mark_today(
            db,
            employee.tenant_id,
            employee.id

        )
        if last_mark and last_mark.status == 'IN':
            return None, None
        # mark attendance in to table
        return await self.attendance_repo.create(db, obj_in), nearest

    # 7. Mark attendance "out"
    async def mark_attendance_out(
        self,
        employee: Employee,
        coordinates: Coordinate,
        db: AsyncSession
    ) -> Tuple[Attendance, GeoMarking] | Tuple[None, None]:
        marked_locations = await geomarking_repo.get_all_by_tenant(
            db,
            employee.tenant_id
        )

        nearest, dist = geo.find_nearest(
            marked_locations,
            coordinates.model_dump(),
            location_extract_method=lambda loc: (loc.latitude, loc.longitude)
        )
        obj_in = AttendanceCreate(
            tenant_id=employee.tenant_id,
            employee_id=employee.id,
            timestamp=datetime.now(),
            latitude=coordinates.lat,
            longitude=coordinates.lon,
            geo_marking_id=nearest.id,
            distance_from_marking=dist,
            status='OUT'
        )        
        # verify the last status of attendance
        _, last_mark = await self.attendance_repo.last_mark_today(
            db,
            employee.tenant_id,
            employee.id

        )
        if not last_mark or (last_mark and last_mark.status == 'OUT'):
            return None, None
        # mark attendance in to table
        return await self.attendance_repo.create(db, obj_in), nearest


    async def get_state(self, tenant_id: uuid.UUID, employee_id: uuid.UUID, db: AsyncSession):
        state_near, state = await self.attendance_repo.last_mark_today(db, tenant_id, employee_id)
        today_in_near, today_in = await self.attendance_repo.today_in(db, tenant_id, employee_id)
        return {
            'state': state.model_dump() if state else {},
            'state_near': state_near.model_dump() if state_near else None,
            'today_in_near': today_in_near.model_dump() if today_in_near else None,
            'today_in': today_in.model_dump() if today_in else {}
        }


employee_service = EmployeeService()
