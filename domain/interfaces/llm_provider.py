from abc import ABC, abstractmethod

from domain.entities.exercise_model import NounExercisePrompt, VerbExercisePrompt, ExerciseEvaluation
from domain.entities.german_noun_model import GermanNounModel
from domain.entities.german_verb_model import GermanVerbModel


class LLMProviderInterface(ABC):
    @abstractmethod
    async def generate_noun_exercise(
        self,
        noun: GermanNounModel,
        native_language: str,
        exercise_mode: str,
        situation: str | None = None,
    ) -> NounExercisePrompt:
        pass

    @abstractmethod
    async def evaluate_noun_answer(
        self,
        noun: GermanNounModel,
        exercise_mode: str,
        prompt_native: str,
        expected_answer: str,
        user_answer: str,
    ) -> ExerciseEvaluation:
        pass

    @abstractmethod
    async def generate_verb_exercise(
        self,
        verb: GermanVerbModel,
        native_language: str,
        tense: str,
        person: str,
        situation: str | None = None,
    ) -> VerbExercisePrompt:
        pass

    @abstractmethod
    async def evaluate_verb_answer(
        self,
        verb: GermanVerbModel,
        tense: str,
        person: str,
        prompt_native: str,
        expected_answer: str,
        user_answer: str,
    ) -> ExerciseEvaluation:
        pass
