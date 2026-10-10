from typing import Protocol
import uuid

from .entities import Questionnaire, QuestionnaireDetails


class QuestionnaireRepository(Protocol):
    async def list_available(self) -> list[Questionnaire]:
        ...

    async def get_details_by_id(self, questionnaire_id: uuid.UUID) -> QuestionnaireDetails | None:
        ...
