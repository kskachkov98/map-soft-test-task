from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from common.configuration import DbConfig

# 1. Создаем асинхронный движок
# echo=True полезен на этапе разработки для логирования SQL-запросов в консоль
engine = create_async_engine(
    DbConfig.database_url,
    echo=False,
    pool_pre_ping=True,  # Проверяет живое ли соединение перед отправкой запроса
)

# 2. Создаем фабрику асинхронных сессий
async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Защищает от транзакционных ошибок при обращении к атрибутам вне сессии
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
