from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from backend.core.config import settings

engine = create_async_engine(settings.DATABASE_URL)

async_session = async_sessionmaker(bind=engine,class_=AsyncSession)

async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            session.close() 
