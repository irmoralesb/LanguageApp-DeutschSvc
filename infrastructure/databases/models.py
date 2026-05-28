import datetime
import uuid

from sqlalchemy import String, Boolean, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER, DATETIME2

from infrastructure.databases.database import Base


class LanguageDataModel(Base):
    __tablename__ = "languages"

    id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True), default=uuid.uuid4, primary_key=True)
    code: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_target_language: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_native_language: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


class GermanNounDataModel(Base):
    __tablename__ = "german_nouns"
    __table_args__ = (
        UniqueConstraint("singular", "created_by_user_id", name="uq_german_noun_user"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True), default=uuid.uuid4, primary_key=True)
    singular: Mapped[str] = mapped_column(String(100), nullable=False)
    plural: Mapped[str | None] = mapped_column(String(100), nullable=True)
    article_singular: Mapped[str] = mapped_column(String(10), nullable=False)
    article_plural: Mapped[str | None] = mapped_column(String(10), nullable=True)
    definition: Mapped[str] = mapped_column(String(500), nullable=False)
    is_catalog: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_by_user_id: Mapped[uuid.UUID | None] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DATETIME2(precision=6), server_default=func.sysutcdatetime(), nullable=False)


class GermanVerbDataModel(Base):
    __tablename__ = "german_verbs"
    __table_args__ = (
        UniqueConstraint("infinitive", "created_by_user_id", name="uq_german_verb_user"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True), default=uuid.uuid4, primary_key=True)
    infinitive: Mapped[str] = mapped_column(String(100), nullable=False)
    definition: Mapped[str] = mapped_column(String(500), nullable=False)
    is_catalog: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_by_user_id: Mapped[uuid.UUID | None] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DATETIME2(precision=6), server_default=func.sysutcdatetime(), nullable=False)

    conjugations = relationship(
        "GermanVerbConjugationDataModel", back_populates="verb", lazy="selectin", cascade="all, delete-orphan")


class GermanVerbConjugationDataModel(Base):
    __tablename__ = "german_verb_conjugations"
    __table_args__ = (
        UniqueConstraint("verb_id", "tense", "person", name="uq_verb_tense_person"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True), default=uuid.uuid4, primary_key=True)
    verb_id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True),
        ForeignKey("german_verbs.id", ondelete="CASCADE"),
        nullable=False,
    )
    tense: Mapped[str] = mapped_column(String(20), nullable=False)
    person: Mapped[str] = mapped_column(String(10), nullable=False)
    conjugated_form: Mapped[str] = mapped_column(String(100), nullable=False)

    verb = relationship("GermanVerbDataModel", back_populates="conjugations")


class UserProfileDataModel(Base):
    __tablename__ = "user_profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True), default=uuid.uuid4, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True), nullable=False, unique=True)
    native_language_id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True),
        ForeignKey("languages.id"),
        nullable=False,
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DATETIME2(precision=6), server_default=func.sysutcdatetime(), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DATETIME2(precision=6), server_default=func.sysutcdatetime(), nullable=False)

    native_language = relationship("LanguageDataModel", lazy="joined")
    learning_languages = relationship(
        "UserLearningLanguageDataModel", back_populates="profile", lazy="joined")
    noun_selections = relationship(
        "UserGermanNounSelectionDataModel", back_populates="profile", lazy="selectin")
    verb_selections = relationship(
        "UserGermanVerbSelectionDataModel", back_populates="profile", lazy="selectin")


class UserLearningLanguageDataModel(Base):
    __tablename__ = "user_learning_languages"
    __table_args__ = (
        UniqueConstraint("user_id", "language_id", name="uq_user_learning_language"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True), default=uuid.uuid4, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True),
        ForeignKey("user_profiles.user_id"),
        nullable=False,
    )
    language_id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True),
        ForeignKey("languages.id"),
        nullable=False,
    )

    profile = relationship("UserProfileDataModel", back_populates="learning_languages")
    language = relationship("LanguageDataModel", lazy="joined")


class UserGermanNounSelectionDataModel(Base):
    __tablename__ = "user_german_noun_selections"
    __table_args__ = (
        UniqueConstraint("user_id", "german_noun_id", name="uq_user_german_noun"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True), default=uuid.uuid4, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True),
        ForeignKey("user_profiles.user_id"),
        nullable=False,
    )
    german_noun_id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True),
        ForeignKey("german_nouns.id"),
        nullable=False,
    )
    added_at: Mapped[datetime.datetime] = mapped_column(
        DATETIME2(precision=6), server_default=func.sysutcdatetime(), nullable=False)

    profile = relationship("UserProfileDataModel", back_populates="noun_selections")
    german_noun = relationship("GermanNounDataModel", lazy="joined")


class UserGermanVerbSelectionDataModel(Base):
    __tablename__ = "user_german_verb_selections"
    __table_args__ = (
        UniqueConstraint("user_id", "german_verb_id", name="uq_user_german_verb"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True), default=uuid.uuid4, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True),
        ForeignKey("user_profiles.user_id"),
        nullable=False,
    )
    german_verb_id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True),
        ForeignKey("german_verbs.id"),
        nullable=False,
    )
    added_at: Mapped[datetime.datetime] = mapped_column(
        DATETIME2(precision=6), server_default=func.sysutcdatetime(), nullable=False)

    profile = relationship("UserProfileDataModel", back_populates="verb_selections")
    german_verb = relationship("GermanVerbDataModel", lazy="joined")


class NounExerciseResultDataModel(Base):
    __tablename__ = "noun_exercise_results"

    id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True), default=uuid.uuid4, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True), nullable=False, index=True)
    german_noun_id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True),
        ForeignKey("german_nouns.id"),
        nullable=False,
    )
    exercise_type: Mapped[str] = mapped_column(String(50), nullable=False)
    target_language_code: Mapped[str] = mapped_column(String(10), nullable=False)
    exercise_mode: Mapped[str] = mapped_column(String(30), nullable=False, default="singular")
    scenario_native: Mapped[str] = mapped_column(String, nullable=False)
    prompt_native: Mapped[str] = mapped_column(String, nullable=False)
    expected_answer: Mapped[str] = mapped_column(String, nullable=False)
    user_answer: Mapped[str] = mapped_column(String, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    feedback: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DATETIME2(precision=6), server_default=func.sysutcdatetime(), nullable=False)

    german_noun = relationship("GermanNounDataModel", lazy="joined")


class VerbExerciseResultDataModel(Base):
    __tablename__ = "verb_exercise_results"

    id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True), default=uuid.uuid4, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True), nullable=False, index=True)
    german_verb_id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER(as_uuid=True),
        ForeignKey("german_verbs.id"),
        nullable=False,
    )
    exercise_type: Mapped[str] = mapped_column(String(50), nullable=False)
    target_language_code: Mapped[str] = mapped_column(String(10), nullable=False)
    tense: Mapped[str] = mapped_column(String(20), nullable=False)
    person: Mapped[str] = mapped_column(String(10), nullable=False)
    scenario_native: Mapped[str] = mapped_column(String, nullable=False)
    prompt_native: Mapped[str] = mapped_column(String, nullable=False)
    expected_answer: Mapped[str] = mapped_column(String, nullable=False)
    user_answer: Mapped[str] = mapped_column(String, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    feedback: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DATETIME2(precision=6), server_default=func.sysutcdatetime(), nullable=False)

    german_verb = relationship("GermanVerbDataModel", lazy="joined")
