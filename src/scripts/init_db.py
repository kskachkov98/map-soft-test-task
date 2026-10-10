import asyncio
import sys

from infrastructure.db.session import engine
from infrastructure.db.models import Base

async def create_db_schema():
    print("Инициализация схемы базы данных...")
    try:
        async with engine.begin() as conn:
            # Создаем все таблицы, зарегистрированные в Base.metadata
            await conn.run_sync(Base.metadata.create_all)
        print(" Схема базы данных успешно создана!")
    except Exception as e:
        print(f"Ошибка при создании схемы БД: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(create_db_schema())
