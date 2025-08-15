# db/base.py
import uuid
from typing import TypeVar, Generic, Type, Optional, List
from sqlmodel import SQLModel, select
from sqlalchemy.sql import Select
from sqlmodel.ext.asyncio.session import AsyncSession

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
updateSchemaType = TypeVar("updateSchemaType", bound=SQLModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, updateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def _get(
        self,
        db: AsyncSession,
        query: Optional[Select] = None
    ) -> Optional[ModelType]:
        query = query if query is not None else select(self.model)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def _getfirst(
        self,
        db: AsyncSession,
        query: Optional[Select] = None
    ) -> Optional[ModelType]:
        query = query if query is not None else select(self.model)
        result = (await db.exec(query)).first()
        return result
    
    async def get(
        self,
        db: AsyncSession,
        id: uuid.UUID,
        query: Optional[Select] = None
    ) -> Optional[ModelType]:
        query = query if query is not None else select(self.model).where(self.model.id == id)        
        return await self._get(db, query)

    async def _get_all(
        self,
        db: AsyncSession,
        query: Optional[Select] = None
    ) -> List[ModelType]:
        query = query if query is not None else select(self.model)
        result = await db.execute(query)
        return result.scalars().all()

    async def get_all(
        self,
        db: AsyncSession,
        query: Optional[Select] = None
    ) -> List[ModelType]:
        return await self._get_all(db)

    async def create(self, db: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model.model_validate(obj_in)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def create_in_transaction(self, db: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model.model_validate(obj_in)
        db.add(db_obj)
        return db_obj
    
    async def delete(self, db: AsyncSession, id: uuid.UUID) -> None:
        obj = await self._get(db, select(self.model).where(self.model.id == id))
        if obj:
            await db.delete(obj)
            await db.commit()

    async def _update(
        self,
        db: AsyncSession,
        db_obj: ModelType,
        obj_in: updateSchemaType
    ) -> Optional[ModelType]:

        if db_obj:
            for field, value in obj_in.model_dump().items():
                setattr(db_obj, field, value)
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            return db_obj
        return None

    async def update(
        self,
        db: AsyncSession,
        id: uuid.UUID,
        obj_in: updateSchemaType,
        query: Optional[Select] = None
    ) -> Optional[ModelType]:
        query = query if query is not None else select(self.model).where(self.model.id == id) 
        db_obj = await self._get(db, query=query)

        return await self._update(db, db_obj, obj_in)
