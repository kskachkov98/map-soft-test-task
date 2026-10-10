import uuid

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from common.configuration import Config
from domain.entities import AnswerOption, Question, QuestionGroup, Questionnaire, QuestionnaireDetails
from infrastructure.db.models import QuestionDb, ReferenceItemDb


class SqlQuestionnaireRepositoryImpl:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def list_available(self) -> list[Questionnaire]:
        """
        Получить список доступных анкет.
        Фильтруем: Ident = 43005, FlagDeleted = False, Tip2 = 0 или NULL.
        Сортировка: по названию по возрастанию.
        """
        query = (
            select(ReferenceItemDb)
            .where(
                and_(
                    ReferenceItemDb.ident == Config.QUESTIONNAIRE_IDENT,
                    ReferenceItemDb.flag_deleted == False,
                    (ReferenceItemDb.tip2 == 0) | (ReferenceItemDb.tip2.is_(None)),
                )
            )
            .order_by(ReferenceItemDb.name.asc())
        )
        res = await self.session.execute(query)
        questionnaires = res.scalars().all()
        
        return [Questionnaire(uid=q.uid, name=q.name, code=q.cod) for q in questionnaires]

    async def get_details_by_id(self, questionnaire_id: uuid.UUID) -> QuestionnaireDetails | None:
        """
        Получить конкретную анкету со всей структурой.
        (Код метода полностью соответствует ранее написанному асинхронному репозиторию).
        """
        questionnaire_query = select(ReferenceItemDb).where(
            and_(
                ReferenceItemDb.uid == questionnaire_id,
                ReferenceItemDb.ident == Config.QUESTIONNAIRE_IDENT,
                ReferenceItemDb.flag_deleted == False,
                (ReferenceItemDb.tip2 == 0) | (ReferenceItemDb.tip2.is_(None)),
            )
        )
        questionnaire_row = await self.session.execute(questionnaire_query)
        questionnaire_db: ReferenceItemDb | None = questionnaire_row.scalar_one_or_none()

        if not questionnaire_db:
            return None
        
        questionnaire = Questionnaire(
            uid=questionnaire_db.uid,
            code=questionnaire_db.cod,
            name=questionnaire_db.name,
        )

        # Варианты ответов: Ident = 79000 + Cod анкеты
        answer_ident = Config.ANSWER_BASE_IDENT + questionnaire.code
        answer_query = (
            select(ReferenceItemDb)
            .where(
                and_(
                    ReferenceItemDb.ident == answer_ident,
                    ReferenceItemDb.flag_deleted == False,
                )
            )
            .order_by(ReferenceItemDb.cod.asc())
        )
        answer_rows = await self.session.execute(answer_query)
        answers_db = answer_rows.scalars().all()
        answers = [
            AnswerOption(uid=opt.uid, code=opt.cod, name=opt.name or "") for opt in answers_db
        ]

        # Группы вопросов: Ident = 43010
        question_group_ident = Config.QUESTION_GROUP_IDENT
        question_group_query = (
            select(ReferenceItemDb)
            .where(
                and_(
                    ReferenceItemDb.ident == question_group_ident,
                    ReferenceItemDb.flag_deleted == False,
                )
            )
            .order_by(ReferenceItemDb.name.asc())
        )
        question_group_rows = await self.session.execute(question_group_query)
        question_groups_db = question_group_rows.scalars().all()
        question_groups = [
            QuestionGroup(uid=qg.uid, code=qg.cod, name=qg.name or "") for qg in question_groups_db
        ]

        # Вопросы для анкет:  = 41
        questions_query = (
            select(QuestionDb)
            .where(
                and_(
                    QuestionDb.cod == Config.QUESTION_CODE,
                    QuestionDb.id_2 == questionnaire.code,
                    QuestionDb.count_4 == 0
                )
            )
            .order_by(QuestionDb.count_1.asc()))
        question_rows = await self.session.execute(questions_query)
        questions_db: list[QuestionDb] = question_rows.scalars().all()
        questions = [
            Question(
                uid=q.uid,
                short_text=q.str_1,
                full_text=q.text_1,
                order=q.count_1,
                required=q.boolean_1 or False,
                group_code=q.count_5,
            ) for q in questions_db
        ]
        

        return QuestionnaireDetails(
            questionnaire=questionnaire,
            answer_options=answers,
            groups=question_groups,
            questions=questions,
        )