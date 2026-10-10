import uuid

from domain.entities import QuestionnaireDetails, Questionnaire, AnswerOption, Question, QuestionGroup
from dataclasses import dataclass


@dataclass(frozen=True)
class QuestionnaireListItem:
    uid: uuid.UUID
    name: str | None

    @classmethod
    def from_entity(cls, entity: Questionnaire) -> 'QuestionnaireListItem':
        return cls(uid=entity.uid, name=entity.name)


@dataclass(frozen=True)
class AnswerOptionDto:
    uid: uuid.UUID
    code: int | None
    name: str | None

    @classmethod
    def from_entity(cls, entity: AnswerOption) -> 'AnswerOptionDto':
        return cls(uid=entity.uid, code=entity.code, name=entity.name)


@dataclass(frozen=True)
class QuestionDto:
    uid: uuid.UUID
    order: int | None
    short_text: str | None
    full_text: str | None
    required: bool

    @classmethod
    def from_entity(cls, entity: Question) -> 'QuestionDto':
        return cls(
            uid=entity.uid,
            order=entity.order,
            short_text=entity.short_text,
            full_text=entity.full_text,
            required=entity.required,
        )

@dataclass(frozen=True)
class QuestionGroupDto:
    uid: uuid.UUID
    name: str | None
    questions: list[QuestionDto]

    @classmethod
    def from_entity(cls, entity: QuestionGroup, questions: list[Question]) -> 'QuestionGroupDto':
        return cls(
            uid=entity.uid,
            name=entity.name,
            questions=[QuestionDto.from_entity(question) for question in questions],
        )


@dataclass(frozen=True)
class QuestionnaireDto:
    uid: uuid.UUID
    name: str | None
    answer_options: list[AnswerOptionDto]
    question_groups: list[QuestionGroupDto]
    ungrouped_questions: list[QuestionDto]

    @classmethod
    def from_entity(
        cls,
        entity: QuestionnaireDetails,
        groups: list[QuestionGroupDto],
        ungrouped_questions: list[QuestionDto]
    ) -> 'QuestionnaireDto':

        return cls(
            uid=entity.questionnaire.uid,
            name=entity.questionnaire.name,
            answer_options=[AnswerOptionDto.from_entity(option) for option in entity.answer_options],
            question_groups=groups,
            ungrouped_questions=ungrouped_questions,
        )
