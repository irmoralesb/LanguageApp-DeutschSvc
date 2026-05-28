from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.exercise_model import (
    NounExerciseHistoryRecord,
    VerbExerciseHistoryRecord,
    GermanNounStats,
    GermanVerbStats,
)


class ExerciseRepositoryInterface(ABC):
    @abstractmethod
    async def save_noun_result(self, record: NounExerciseHistoryRecord) -> NounExerciseHistoryRecord:
        pass

    @abstractmethod
    async def save_verb_result(self, record: VerbExerciseHistoryRecord) -> VerbExerciseHistoryRecord:
        pass

    @abstractmethod
    async def get_noun_stats_by_user(self, user_id: UUID) -> list[GermanNounStats]:
        pass

    @abstractmethod
    async def get_verb_stats_by_user(self, user_id: UUID) -> list[GermanVerbStats]:
        pass
