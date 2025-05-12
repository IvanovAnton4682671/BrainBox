from sqlalchemy.orm import declarative_base
from core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator

Base = declarative_base()

engine = create_async_engine(
    settings.POSTGRES_URL,
    echo=settings.APP_DEBUG,
    future=True,
    pool_pre_ping=True
)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Генератор сессий для dependency injection в FastAPI
    Использование:
        async with get_db() as db:
            await db.execute(...)
    """
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()