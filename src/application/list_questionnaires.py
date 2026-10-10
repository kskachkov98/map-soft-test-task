from application.dto import QuestionnaireListItem
from domain.repositories import QuestionnaireRepository


class ListQuestionnaires:
    def __init__(self, questionnaire_repository: QuestionnaireRepository) -> None:
        self.questionnaire_repository = questionnaire_repository

    async def execute(self) -> list[QuestionnaireListItem]:
        questionnaires = await self.questionnaire_repository.list_available()
        return [QuestionnaireListItem.from_entity(questionnaire) for questionnaire in questionnaires]
