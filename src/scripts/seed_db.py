import asyncio
import json
import os
import sys
from typing import List, Dict, Any
from sqlalchemy import insert, delete
from infrastructure.db.session import async_session_maker, engine
from infrastructure.db.models import ReferenceItemDb, QuestionDb

# Путь к JSON-файлу с данными (можно вынести в переменные окружения)
JSON_FILES_PATH = os.getenv("JSON_FILES_PATH", "/seed_files/")
QUESTIONS_FILE_NAME = os.getenv("REFERENCE_ITEMS_FILE_NAME", "questions.json")
REFERENCE_ITEMS_FILE_NAME = os.getenv("REFERENCE_ITEMS_FILE_NAME", "reference_items_.json")

QUESTIONS_FILE_PATH = JSON_FILES_PATH + QUESTIONS_FILE_NAME
REFERENCE_ITEMS_FILE_PATH = JSON_FILES_PATH + REFERENCE_ITEMS_FILE_NAME

async def seed_data():
    print(f"Запуск импорта данных из файлов: [{QUESTIONS_FILE_PATH}, {REFERENCE_ITEMS_FILE_PATH}] ...")

    if not os.path.exists(QUESTIONS_FILE_PATH):
        print(f"❌ Ошибка: Файл {QUESTIONS_FILE_PATH} не найден!", file=sys.stderr)
        sys.exit(1)
    
    if not os.path.exists(REFERENCE_ITEMS_FILE_PATH):
        print(f"❌ Ошибка: Файл {REFERENCE_ITEMS_FILE_PATH} не найден!", file=sys.stderr)
        sys.exit(1)

    try:
        with open(QUESTIONS_FILE_PATH, "r", encoding="utf-8") as qf:
            questions_data = json.load(qf)
            raw_questions: List[Dict[str, Any]] = questions_data.get("questions", [])
        
        with open(REFERENCE_ITEMS_FILE_PATH, "r", encoding="utf-8") as rif:
            reference_items_data = json.load(rif)
            raw_reference_items: List[Dict[str, Any]] = reference_items_data.get("reference_items", [])

        if not raw_reference_items and not raw_questions:
            print("⚠️ Предупреждение: В JSON-файле нет данных для импорта.")
            return

        async with async_session_maker() as session:
            async with session.begin():
                # 1. Пакетная вставка в таблицу reference_items
                if raw_reference_items:
                    print(f"Загрузка {len(raw_reference_items)} записей в reference_items...")
                    reference_items = [
                        dict(
                            uid=raw_item.get("UID"),
                            ident=raw_item.get("Ident"),
                            cod=raw_item.get("Cod"),
                            name=raw_item.get("Name"),
                            tip2=raw_item.get("Tip2"),
                            flag_deleted=raw_item.get("FlagDeleted"),
                        ) for raw_item in raw_reference_items
                    ]
                    await session.execute(delete(ReferenceItemDb))
                    await session.execute(insert(ReferenceItemDb), reference_items)

                # 2. Пакетная вставка в таблицу questions
                if raw_questions:
                    print(f"Загрузка {len(raw_questions)} записей в questions...")
                    questions = [
                        dict(
                            uid=raw_question.get("UID"),
                            cod=raw_question.get("Cod"),
                            id_1=raw_question.get("ID_1"),
                            id_2=raw_question.get("ID_2"),
                            count_1=raw_question.get("Count_1"),
                            count_4=raw_question.get("Count_4"),
                            count_5=raw_question.get("Count_5"),
                            str_1=raw_question.get("STR_1"),
                            text_1=raw_question.get("Text_1"),
                            boolean_1=raw_question.get("Boolean_1"),
                        ) for raw_question in raw_questions
                    ]
                    await session.execute(delete(QuestionDb))
                    await session.execute(insert(QuestionDb), questions)

            # session.begin() автоматически сделает COMMIT, если не возникло ошибок
            print("🎉 База данных успешно наполнена данными!")

    except json.JSONDecodeError:
        print("❌ Ошибка: Файл содержит некорректный JSON.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Произошла ошибка при наполнении БД: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed_data())
