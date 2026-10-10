import uuid

from application.dto import QuestionDto
from application.dto import QuestionGroupDto
from application.dto import QuestionnaireDto
from domain.entities import Question, QuestionGroup
from domain.exceptions import QuestionnaireNotFoundError
from domain.repositories import QuestionnaireRepository


class GetQuestionnaire:
    def __init__(
        self,
        questionnaire_repository: QuestionnaireRepository,
    ) -> None:
        self.questionnaire_repository = questionnaire_repository

    async def execute(self, questionnaire_id: uuid.UUID) -> QuestionnaireDto:
        questionnaire_details = await self.questionnaire_repository.get_details_by_id(questionnaire_id)

        if questionnaire_details is None:
            raise QuestionnaireNotFoundError(questionnaire_id)
        
        groups, ungrouped_questions = self._group_questions(
            questionnaire_details.groups, questionnaire_details.questions
            )

        return QuestionnaireDto.from_entity(
            entity=questionnaire_details,
            groups=groups,
            ungrouped_questions=ungrouped_questions
        )
    
    def _group_questions(
        self, groups: list[QuestionGroup], questions: list[Question]
    ) -> tuple[list[QuestionGroupDto], list[QuestionDto]]:
        groups_by_code = {group.code: [] for group in groups}
        ungrouped = []

        for question in questions:
            question_dto = QuestionDto.from_entity(question)
            if question.group_code == 0 or question.group_code is None:
                ungrouped.append(question_dto)
            elif (group := groups_by_code.get(question.group_code)) is not None:
                group.append(question_dto)

        grouped_dtos = [
            QuestionGroupDto.from_entity(group, groups_by_code.get(group.code)) for group in groups
        ]
        return self._order_groups(grouped_dtos, ungrouped)
    
    def _order_groups(
        self, groups: list[QuestionGroupDto], questions: list[QuestionDto]
    ) -> tuple[list[QuestionGroupDto], list[QuestionDto]]:
        ordered_groups = sorted(groups, key=lambda g: g.name)
        for group in ordered_groups:
            group.questions.sort(key=lambda q: q.order)

        ordered_questions = sorted(questions, key=lambda q: q.order)

        return ordered_groups, ordered_questions
