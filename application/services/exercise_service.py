import random as rand_mod
from uuid import UUID

from domain.entities.exercise_model import (
    NounExercisePrompt,
    NounGenderExerciseItem,
    VerbExercisePrompt,
    ExerciseEvaluation,
    NounExerciseHistoryRecord,
    VerbExerciseHistoryRecord,
)
from domain.entities.german_verb_model import TENSES, PERSONS
from domain.exceptions.exercise_errors import ExerciseGenerationError
from domain.exceptions.german_noun_errors import GermanNounNotFoundError
from domain.exceptions.german_verb_errors import GermanVerbNotFoundError
from domain.interfaces.exercise_repository import ExerciseRepositoryInterface
from domain.interfaces.german_noun_repository import GermanNounRepositoryInterface
from domain.interfaces.german_verb_repository import GermanVerbRepositoryInterface
from domain.interfaces.language_repository import LanguageRepositoryInterface
from domain.interfaces.llm_provider import LLMProviderInterface
from domain.interfaces.user_profile_repository import UserProfileRepositoryInterface
from domain.exceptions.user_profile_errors import UserProfileNotFoundError


class ExerciseService:
    GENDER_ARTICLES = ("der", "die", "das")

    def __init__(
        self,
        exercise_repo: ExerciseRepositoryInterface,
        noun_repo: GermanNounRepositoryInterface,
        verb_repo: GermanVerbRepositoryInterface,
        user_profile_repo: UserProfileRepositoryInterface,
        language_repo: LanguageRepositoryInterface,
        llm_provider: LLMProviderInterface,
    ):
        self.exercise_repo = exercise_repo
        self.noun_repo = noun_repo
        self.verb_repo = verb_repo
        self.user_profile_repo = user_profile_repo
        self.language_repo = language_repo
        self.llm = llm_provider

    async def generate_noun_gender_exercise(
        self,
        user_id: UUID,
        count: int = 9,
    ) -> list[NounGenderExerciseItem]:
        catalog = await self.noun_repo.get_catalog(skip=0, limit=1000)
        nouns = [
            noun for noun in catalog
            if noun.singular and noun.article_singular.lower() in self.GENDER_ARTICLES
        ]
        if not nouns:
            raise ExerciseGenerationError("No singular German nouns available.")

        stats_by_noun = {
            stat.german_noun_id: stat
            for stat in await self.exercise_repo.get_noun_stats_by_user(user_id, exercise_type="gender")
        }
        weights = []
        for noun in nouns:
            stat = stats_by_noun.get(noun.id)
            incorrect_attempts = 0 if stat is None else stat.total_attempts - stat.correct_attempts
            weights.append(1 + max(incorrect_attempts, 0) * 2)

        selected = rand_mod.choices(nouns, weights=weights, k=count)
        items: list[NounGenderExerciseItem] = []
        for noun in selected:
            assert noun.id is not None
            stat = stats_by_noun.get(noun.id)
            total_attempts = 0 if stat is None else stat.total_attempts
            correct_attempts = 0 if stat is None else stat.correct_attempts
            items.append(
                NounGenderExerciseItem(
                    german_noun_id=noun.id,
                    singular=noun.singular,
                    definition=noun.definition,
                    incorrect_attempts=max(total_attempts - correct_attempts, 0),
                    correct_attempts=correct_attempts,
                )
            )
        return items

    async def evaluate_noun_gender_answer(
        self,
        user_id: UUID,
        german_noun_id: UUID,
        selected_article: str,
    ) -> ExerciseEvaluation:
        noun = await self.noun_repo.get_by_id(german_noun_id)
        if noun is None:
            raise GermanNounNotFoundError(german_noun_id)

        selected = selected_article.lower().strip()
        correct_article = noun.article_singular.lower()
        is_correct = selected == correct_article
        feedback = (
            f"Correct: {correct_article} {noun.singular}."
            if is_correct
            else f"{noun.singular} uses {correct_article}: {correct_article} {noun.singular}."
        )
        record = NounExerciseHistoryRecord(
            id=None,
            user_id=user_id,
            german_noun_id=german_noun_id,
            exercise_type="gender",
            target_language_code="de",
            exercise_mode="singular",
            scenario_native="Sort the German noun by grammatical gender.",
            prompt_native=noun.singular,
            expected_answer=correct_article,
            user_answer=selected,
            is_correct=is_correct,
            feedback=feedback,
        )
        await self.exercise_repo.save_noun_result(record)
        return ExerciseEvaluation(
            is_correct=is_correct,
            feedback=feedback,
            correct_example=f"{correct_article} {noun.singular}",
        )

    async def generate_noun_exercise(
        self,
        user_id: UUID,
        exercise_mode: str = "singular",
        german_noun_id: UUID | None = None,
        situation: str | None = None,
    ) -> NounExercisePrompt:
        profile = await self.user_profile_repo.get_by_user_id(user_id)
        if profile is None:
            raise UserProfileNotFoundError(user_id)

        native_lang = await self.language_repo.get_by_id(profile.native_language_id)
        if native_lang is None:
            raise ExerciseGenerationError("Native language not found in catalog.")

        if exercise_mode not in ("singular", "plural"):
            exercise_mode = "singular"

        if german_noun_id is not None:
            noun = await self.noun_repo.get_by_id(german_noun_id)
            if noun is None:
                raise GermanNounNotFoundError(german_noun_id)
        else:
            selections = await self.user_profile_repo.get_german_noun_selections(user_id)
            if selections:
                sel = rand_mod.choice(selections)
                noun = await self.noun_repo.get_by_id(sel.german_noun_id)
                if noun is None:
                    raise GermanNounNotFoundError(sel.german_noun_id)
            else:
                catalog = await self.noun_repo.get_catalog(skip=0, limit=100)
                if not catalog:
                    raise ExerciseGenerationError("No German nouns available.")
                noun = rand_mod.choice(catalog)

        prompt = await self.llm.generate_noun_exercise(
            noun=noun,
            native_language=native_lang.name,
            exercise_mode=exercise_mode,
            situation=situation,
        )
        prompt.german_noun_id = noun.id
        prompt.target_language_code = "de"
        return prompt

    async def evaluate_noun_answer(
        self,
        user_id: UUID,
        german_noun_id: UUID,
        exercise_mode: str,
        scenario_native: str,
        prompt_native: str,
        expected_answer: str,
        user_answer: str,
    ) -> ExerciseEvaluation:
        noun = await self.noun_repo.get_by_id(german_noun_id)
        if noun is None:
            raise GermanNounNotFoundError(german_noun_id)

        evaluation = await self.llm.evaluate_noun_answer(
            noun=noun,
            exercise_mode=exercise_mode,
            prompt_native=prompt_native,
            expected_answer=expected_answer,
            user_answer=user_answer,
        )

        record = NounExerciseHistoryRecord(
            id=None,
            user_id=user_id,
            german_noun_id=german_noun_id,
            exercise_type="writing",
            target_language_code="de",
            exercise_mode=exercise_mode,
            scenario_native=scenario_native,
            prompt_native=prompt_native,
            expected_answer=expected_answer,
            user_answer=user_answer,
            is_correct=evaluation.is_correct,
            feedback=evaluation.feedback,
        )
        await self.exercise_repo.save_noun_result(record)
        return evaluation

    async def generate_verb_exercise(
        self,
        user_id: UUID,
        tense: str = "present",
        person: str = "3sg",
        german_verb_id: UUID | None = None,
        situation: str | None = None,
    ) -> VerbExercisePrompt:
        profile = await self.user_profile_repo.get_by_user_id(user_id)
        if profile is None:
            raise UserProfileNotFoundError(user_id)

        native_lang = await self.language_repo.get_by_id(profile.native_language_id)
        if native_lang is None:
            raise ExerciseGenerationError("Native language not found in catalog.")

        if tense not in TENSES:
            tense = "present"
        if person not in PERSONS:
            person = "3sg"

        if german_verb_id is not None:
            verb = await self.verb_repo.get_by_id(german_verb_id)
            if verb is None:
                raise GermanVerbNotFoundError(german_verb_id)
        else:
            selections = await self.user_profile_repo.get_german_verb_selections(user_id)
            if selections:
                sel = rand_mod.choice(selections)
                verb = await self.verb_repo.get_by_id(sel.german_verb_id)
                if verb is None:
                    raise GermanVerbNotFoundError(sel.german_verb_id)
            else:
                catalog = await self.verb_repo.get_catalog(skip=0, limit=100)
                if not catalog:
                    raise ExerciseGenerationError("No German verbs available.")
                verb = rand_mod.choice(catalog)

        prompt = await self.llm.generate_verb_exercise(
            verb=verb,
            native_language=native_lang.name,
            tense=tense,
            person=person,
            situation=situation,
        )
        prompt.german_verb_id = verb.id
        prompt.target_language_code = "de"
        return prompt

    async def evaluate_verb_answer(
        self,
        user_id: UUID,
        german_verb_id: UUID,
        tense: str,
        person: str,
        scenario_native: str,
        prompt_native: str,
        expected_answer: str,
        user_answer: str,
    ) -> ExerciseEvaluation:
        verb = await self.verb_repo.get_by_id(german_verb_id)
        if verb is None:
            raise GermanVerbNotFoundError(german_verb_id)

        evaluation = await self.llm.evaluate_verb_answer(
            verb=verb,
            tense=tense,
            person=person,
            prompt_native=prompt_native,
            expected_answer=expected_answer,
            user_answer=user_answer,
        )

        record = VerbExerciseHistoryRecord(
            id=None,
            user_id=user_id,
            german_verb_id=german_verb_id,
            exercise_type="writing",
            target_language_code="de",
            tense=tense,
            person=person,
            scenario_native=scenario_native,
            prompt_native=prompt_native,
            expected_answer=expected_answer,
            user_answer=user_answer,
            is_correct=evaluation.is_correct,
            feedback=evaluation.feedback,
        )
        await self.exercise_repo.save_verb_result(record)
        return evaluation
