import uuid
from uuid import UUID

from sqlalchemy import func, case, select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.exercise_model import (
    NounExerciseHistoryRecord,
    VerbExerciseHistoryRecord,
    GermanNounStats,
    GermanVerbStats,
)
from domain.interfaces.exercise_repository import ExerciseRepositoryInterface
from infrastructure.databases.models import NounExerciseResultDataModel, VerbExerciseResultDataModel


class ExerciseRepository(ExerciseRepositoryInterface):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_noun_result(self, record: NounExerciseHistoryRecord) -> NounExerciseHistoryRecord:
        db_item = NounExerciseResultDataModel(
            id=record.id or uuid.uuid4(),
            user_id=record.user_id,
            german_noun_id=record.german_noun_id,
            exercise_type=record.exercise_type,
            target_language_code=record.target_language_code,
            exercise_mode=record.exercise_mode,
            scenario_native=record.scenario_native,
            prompt_native=record.prompt_native,
            expected_answer=record.expected_answer,
            user_answer=record.user_answer,
            is_correct=record.is_correct,
            feedback=record.feedback,
        )
        self.db.add(db_item)
        await self.db.flush()
        await self.db.refresh(db_item)
        return self._to_noun_domain(db_item)

    async def save_verb_result(self, record: VerbExerciseHistoryRecord) -> VerbExerciseHistoryRecord:
        db_item = VerbExerciseResultDataModel(
            id=record.id or uuid.uuid4(),
            user_id=record.user_id,
            german_verb_id=record.german_verb_id,
            exercise_type=record.exercise_type,
            target_language_code=record.target_language_code,
            tense=record.tense,
            person=record.person,
            scenario_native=record.scenario_native,
            prompt_native=record.prompt_native,
            expected_answer=record.expected_answer,
            user_answer=record.user_answer,
            is_correct=record.is_correct,
            feedback=record.feedback,
        )
        self.db.add(db_item)
        await self.db.flush()
        await self.db.refresh(db_item)
        return self._to_verb_domain(db_item)

    async def get_noun_stats_by_user(
        self,
        user_id: UUID,
        exercise_type: str | None = None,
    ) -> list[GermanNounStats]:
        stmt = (
            select(
                NounExerciseResultDataModel.german_noun_id,
                func.count().label("total"),
                func.sum(case((NounExerciseResultDataModel.is_correct.is_(True), 1), else_=0)).label("correct"),
            )
            .where(NounExerciseResultDataModel.user_id == user_id)
            .group_by(NounExerciseResultDataModel.german_noun_id)
        )
        if exercise_type is not None:
            stmt = stmt.where(NounExerciseResultDataModel.exercise_type == exercise_type)
        result = await self.db.execute(stmt)
        return [
            GermanNounStats(
                german_noun_id=row.german_noun_id,
                total_attempts=row.total,
                correct_attempts=row.correct or 0,
            )
            for row in result.all()
        ]

    @staticmethod
    def _to_noun_domain(row: NounExerciseResultDataModel) -> NounExerciseHistoryRecord:
        return NounExerciseHistoryRecord(
            id=row.id,
            user_id=row.user_id,
            german_noun_id=row.german_noun_id,
            exercise_type=row.exercise_type,
            target_language_code=row.target_language_code,
            exercise_mode=row.exercise_mode,
            scenario_native=row.scenario_native,
            prompt_native=row.prompt_native,
            expected_answer=row.expected_answer,
            user_answer=row.user_answer,
            is_correct=row.is_correct,
            feedback=row.feedback,
            created_at=row.created_at,
        )

    async def get_verb_stats_by_user(self, user_id: UUID) -> list[GermanVerbStats]:
        stmt = (
            select(
                VerbExerciseResultDataModel.german_verb_id,
                func.count().label("total"),
                func.sum(case((VerbExerciseResultDataModel.is_correct.is_(True), 1), else_=0)).label("correct"),
            )
            .where(VerbExerciseResultDataModel.user_id == user_id)
            .group_by(VerbExerciseResultDataModel.german_verb_id)
        )
        result = await self.db.execute(stmt)
        return [
            GermanVerbStats(
                german_verb_id=row.german_verb_id,
                total_attempts=row.total,
                correct_attempts=row.correct or 0,
            )
            for row in result.all()
        ]

    @staticmethod
    def _to_verb_domain(row: VerbExerciseResultDataModel) -> VerbExerciseHistoryRecord:
        return VerbExerciseHistoryRecord(
            id=row.id,
            user_id=row.user_id,
            german_verb_id=row.german_verb_id,
            exercise_type=row.exercise_type,
            target_language_code=row.target_language_code,
            tense=row.tense,
            person=row.person,
            scenario_native=row.scenario_native,
            prompt_native=row.prompt_native,
            expected_answer=row.expected_answer,
            user_answer=row.user_answer,
            is_correct=row.is_correct,
            feedback=row.feedback,
            created_at=row.created_at,
        )
