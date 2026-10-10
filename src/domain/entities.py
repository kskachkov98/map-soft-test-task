import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class Questionnaire:
    """Шапка анкеты. `code` нужен репозиторию, в API-DTO не уходит."""

    uid: uuid.UUID
    code: int
    name: str | None


@dataclass(frozen=True)
class AnswerOption:
    uid: uuid.UUID
    code: int | None
    name: str | None


@dataclass(frozen=True)
class QuestionGroup:
    uid: uuid.UUID
    code: int
    name: str | None


@dataclass(frozen=True)
class Question:
    uid: uuid.UUID
    order: int | None         # (Count_1)
    short_text: str | None    # (STR_1)
    full_text: str | None     # (Text_1)
    required: bool            # (Boolean_1)
    group_code: int | None    # (Count_5)


@dataclass(frozen=True)
class QuestionnaireDetails:
    """Плоский снимок анкеты: группировку вопросов делает application → DTO."""

    questionnaire: Questionnaire
    answer_options: list[AnswerOption]
    groups: list[QuestionGroup]
    questions: list[Question]
