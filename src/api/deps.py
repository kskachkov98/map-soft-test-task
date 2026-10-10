
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from domain.repositories import QuestionnaireRepository
from infrastructure.db.session import get_async_session
from infrastructure.repositories.sql import SqlQuestionnaireRepositoryImpl


async def get_questionnaire_repo(
    session: AsyncSession = Depends(get_async_session)
) -> QuestionnaireRepository:
    return SqlQuestionnaireRepositoryImpl(session)
