import uuid
from typing import Optional
from sqlalchemy import String, Integer, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class ReferenceItemDb(Base):
    """
    Универсальный справочник (анкеты, группы вопросов, варианты ответов).
    Тип записи определяется полем Ident.
    """
    __tablename__ = "reference_items"

    uid: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        name="UID"
    )
    ident: Mapped[int] = mapped_column(
        Integer, 
        nullable=False, 
        name="Ident"
    )
    cod: Mapped[Optional[int]] = mapped_column(
        Integer, 
        nullable=True, 
        name="Cod"
    )
    name: Mapped[Optional[str]] = mapped_column(
        String(60), 
        nullable=True, 
        name="Name"
    )
    tip2: Mapped[Optional[int]] = mapped_column(
        Integer, 
        nullable=True, 
        name="Tip2"
    )
    flag_deleted: Mapped[bool] = mapped_column(
        Boolean, 
        nullable=False, 
        default=False, 
        name="FlagDeleted"
    )

    def __repr__(self) -> str:
        return f"<ReferenceItemDb uid={self.uid} ident={self.ident} cod={self.cod} name={self.name}>"


class QuestionDb(Base):
    """
    Таблица вопросов анкет.
    Связывается с анкетами через ID_2 (Cod анкеты) и группами через Count_5 (Cod группы).
    """
    __tablename__ = "questions"

    uid: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        name="UID"
    )
    cod: Mapped[Optional[int]] = mapped_column(
        Integer, 
        nullable=True, 
        name="Cod"
    )
    id_1: Mapped[Optional[int]] = mapped_column(
        Integer, 
        nullable=True, 
        name="ID_1"
    )
    id_2: Mapped[Optional[int]] = mapped_column(
        Integer, 
        nullable=True, 
        name="ID_2"
    )  # Ссылка на Cod анкеты
    count_1: Mapped[Optional[int]] = mapped_column(
        Integer, 
        nullable=True, 
        name="Count_1"
    )  # Порядковый номер вопроса
    count_5: Mapped[Optional[int]] = mapped_column(
        Integer, 
        nullable=True, 
        name="Count_5"
    )  # Ссылка на Cod группы (0 — нет группы)
    str_1: Mapped[Optional[str]] = mapped_column(
        String(60), 
        nullable=True, 
        name="STR_1"
    )  # Короткая формулировка
    text_1: Mapped[Optional[str]] = mapped_column(
        Text, 
        nullable=True, 
        name="Text_1"
    )  # Полная формулировка
    boolean_1: Mapped[Optional[bool]] = mapped_column(
        Boolean, 
        nullable=True, 
        default=False, 
        name="Boolean_1"
    )  # Обязательность
    count_4: Mapped[Optional[int]] = mapped_column(
        Integer, 
        nullable=True, 
        name="Count_4"
    )  # Актуальность (0 — актуален)

    def __repr__(self) -> str:
        return f"<QuestionDb uid={self.uid} id_2={self.id_2} count_1={self.count_1}>"
