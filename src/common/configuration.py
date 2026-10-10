from sqlalchemy.util import classproperty
import datetime
from typing import List, Union

import os


class Config:
    """
    Helper class for service configuration.
    """
    PORT = int(os.getenv('PORT', '8000'))

    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()

    ANSWER_BASE_IDENT = os.environ.get('ANSWER_BASE_IDENT', 79000)
    QUESTION_GROUP_IDENT = os.environ.get('QUESTION_GROUP_IDENT', 43010)
    QUESTIONNAIRE_IDENT = os.environ.get('QUESTIONNAIRE_IDENT', 43005)
    QUESTION_CODE = os.environ.get('QUESTION_FOR_QUESTIONNAIRE_CODE', 41)


class DbConfig:
    POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
    POSTGRES_USER = os.environ.get('POSTGRES_USER')
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
    POSTGRES_DB = os.environ.get('POSTGRES_DB')
    POSTGRES_PORT = os.environ.get('POSTGRES_PORT', 5432)

    # Вычисляемое поле для асинхронной строки подключения
    DATABASE_URL = os.environ.get('DATABASE_URL', '')

    @classproperty
    def database_url(cls) -> str:
        # if cls.DATABASE_URL:
        #     return cls.DATABASE_URL
        
        database_url = f'postgresql+asyncpg://{cls.POSTGRES_USER}:{cls.POSTGRES_PASSWORD}@{cls.POSTGRES_HOST}:{cls.POSTGRES_PORT}/{cls.POSTGRES_DB}'
        return database_url
