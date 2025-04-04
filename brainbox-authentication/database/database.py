from sqlalchemy.orm import declarative_base
from core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator

#базовый класс для моделей SQLAlchemy
Base = declarative_base() #для объявления моделей

#настройка подключения к БД
engine = create_async_engine( #асинхронное подключение
    settings.DATABASE_URL,
    echo=settings.APP_DEBUG, #логировать sql-запросы
    future=True, #использовать новые возможности SQLAlchemy 2.0
    pool_pre_ping=True #проверить соединение перед использованием
)

#фабрика сессий для работы с БД
async_session_maker = async_sessionmaker( #для асинхронных сессий
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

async def create_tables():
    """
    Создание таблиц в БД (для использования при инициализации)
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def drop_tables():
    """
    Удаление таблиц БД (для тестов)
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)