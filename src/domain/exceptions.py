import uuid


class QuestionnaireNotFoundError(Exception):
    def __init__(self, questionnaire_id: uuid.UUID) -> None:
        self.questionnaire_id = questionnaire_id
        self.message = f"Questionnaire {questionnaire_id} was not found"
        super().__init__(self.message)
