import uuid

from pydantic import ConfigDict
from pydantic import BaseModel


class ApiAnswerOption(BaseModel):
    uid: uuid.UUID
    code: int | None
    name: str | None

    model_config = ConfigDict(from_attributes=True)


class ApiQuestion(BaseModel):
    uid: uuid.UUID
    order: int | None
    short_text: str | None
    full_text: str | None
    required: bool

    model_config = ConfigDict(from_attributes=True)


class ApiQuestionGroup(BaseModel):
    uid: uuid.UUID
    name: str | None
    questions: list[ApiQuestion]

    model_config = ConfigDict(from_attributes=True)


class ApiQuestionnaireDetails(BaseModel):
    uid: uuid.UUID
    name: str | None
    answer_options: list[ApiAnswerOption]
    question_groups: list[ApiQuestionGroup]
    ungrouped_questions: list[ApiQuestion]

    model_config = ConfigDict(from_attributes=True)


class ApiQuestionnaireListItem(BaseModel):
    uid: uuid.UUID
    name: str | None

    model_config = ConfigDict(from_attributes=True)
