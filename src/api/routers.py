import uuid

from api.deps import get_questionnaire_repo
from typing import Annotated

from fastapi import APIRouter, Depends

from api.schemas import ApiQuestionnaireListItem, ApiQuestionnaireDetails
from application.get_questionnaire import GetQuestionnaire
from application.list_questionnaires import ListQuestionnaires
from domain.repositories import QuestionnaireRepository

questionnaires_router = APIRouter(prefix="/questionnaires", tags=["Questionnaires"])


@questionnaires_router.get("/", response_model=list[ApiQuestionnaireListItem])
async def list_questionnaires(
    questionnaire_repository: Annotated[QuestionnaireRepository, Depends(get_questionnaire_repo)],
) -> list[ApiQuestionnaireListItem]:
    use_case = ListQuestionnaires(questionnaire_repository)
    questionnaires = await use_case.execute()
    return [ApiQuestionnaireListItem.model_validate(q) for q in questionnaires]


@questionnaires_router.get("/{questionnaire_id}/", response_model=ApiQuestionnaireDetails)
async def get_questionnaire_details(
    questionnaire_id: uuid.UUID,
    questionnaire_repository: Annotated[QuestionnaireRepository, Depends(get_questionnaire_repo)],
) -> ApiQuestionnaireDetails:
    use_case = GetQuestionnaire(questionnaire_repository)
    questionnaire_details = await use_case.execute(questionnaire_id)
    return ApiQuestionnaireDetails.model_validate(questionnaire_details)
