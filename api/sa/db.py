from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from .settings import settings

DATABASE_URL = settings.db_url

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


#  Use this function as FastAPI dependency
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session