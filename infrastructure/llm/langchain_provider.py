import logging
from typing import Optional

from pydantic import BaseModel
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage

from domain.entities.exercise_model import NounExercisePrompt, VerbExercisePrompt, ExerciseEvaluation
from domain.entities.german_noun_model import GermanNounModel
from domain.entities.german_verb_model import GermanVerbModel
from domain.exceptions.exercise_errors import LLMProviderError
from domain.interfaces.llm_provider import LLMProviderInterface
from infrastructure.llm.prompts import (
    EXERCISE_GENERATION_SYSTEM,
    EXERCISE_EVALUATION_SYSTEM,
    build_noun_exercise_prompt,
    build_noun_evaluation_prompt,
    build_verb_exercise_prompt,
    build_verb_evaluation_prompt,
)

logger = logging.getLogger(__name__)


class _ExerciseOutput(BaseModel):
    scenario_native: str
    prompt_native: str
    expected_answer: str


class _EvaluationOutput(BaseModel):
    is_correct: bool
    feedback: str
    correct_example: Optional[str] = None


class LangChainProvider(LLMProviderInterface):
    def __init__(
        self,
        provider: str,
        api_key: str,
        model: str,
        max_tokens: int = 1024,
        temperature: float = 0.7,
    ) -> None:
        self._provider = provider
        try:
            llm = init_chat_model(
                model=model,
                model_provider=provider,
                temperature=temperature,
                max_tokens=max_tokens,
                api_key=api_key,
            )
        except ImportError as exc:
            raise LLMProviderError(
                provider,
                f"Missing integration package for provider '{provider}'. Original error: {exc}",
            )
        self._exercise_chain = llm.with_structured_output(_ExerciseOutput)
        self._eval_chain = llm.with_structured_output(_EvaluationOutput)

    async def generate_noun_exercise(
        self,
        noun: GermanNounModel,
        native_language: str,
        exercise_mode: str,
        situation: str | None = None,
    ) -> NounExercisePrompt:
        user_msg = build_noun_exercise_prompt(noun, native_language, exercise_mode, situation)
        messages = [
            SystemMessage(content=EXERCISE_GENERATION_SYSTEM),
            HumanMessage(content=user_msg),
        ]
        try:
            result: _ExerciseOutput = await self._exercise_chain.ainvoke(messages)
            return NounExercisePrompt(
                german_noun_id=noun.id,
                target_language_code="de",
                exercise_mode=exercise_mode,
                scenario_native=result.scenario_native,
                prompt_native=result.prompt_native,
                expected_answer=result.expected_answer,
            )
        except Exception as exc:
            logger.error("Exercise generation failed: %s", exc, exc_info=True)
            raise LLMProviderError(self._provider, str(exc))

    async def evaluate_noun_answer(
        self,
        noun: GermanNounModel,
        exercise_mode: str,
        prompt_native: str,
        expected_answer: str,
        user_answer: str,
    ) -> ExerciseEvaluation:
        user_msg = build_noun_evaluation_prompt(
            noun, exercise_mode, prompt_native, expected_answer, user_answer,
        )
        messages = [
            SystemMessage(content=EXERCISE_EVALUATION_SYSTEM),
            HumanMessage(content=user_msg),
        ]
        try:
            result: _EvaluationOutput = await self._eval_chain.ainvoke(messages)
            return ExerciseEvaluation(
                is_correct=result.is_correct,
                feedback=result.feedback,
                correct_example=result.correct_example,
            )
        except Exception as exc:
            logger.error("Exercise evaluation failed: %s", exc, exc_info=True)
            raise LLMProviderError(self._provider, str(exc))

    async def generate_verb_exercise(
        self,
        verb: GermanVerbModel,
        native_language: str,
        tense: str,
        person: str,
        situation: str | None = None,
    ) -> VerbExercisePrompt:
        user_msg = build_verb_exercise_prompt(verb, native_language, tense, person, situation)
        messages = [
            SystemMessage(content=EXERCISE_GENERATION_SYSTEM),
            HumanMessage(content=user_msg),
        ]
        try:
            result: _ExerciseOutput = await self._exercise_chain.ainvoke(messages)
            return VerbExercisePrompt(
                german_verb_id=verb.id,
                target_language_code="de",
                tense=tense,
                person=person,
                scenario_native=result.scenario_native,
                prompt_native=result.prompt_native,
                expected_answer=result.expected_answer,
            )
        except Exception as exc:
            logger.error("Exercise generation failed: %s", exc, exc_info=True)
            raise LLMProviderError(self._provider, str(exc))

    async def evaluate_verb_answer(
        self,
        verb: GermanVerbModel,
        tense: str,
        person: str,
        prompt_native: str,
        expected_answer: str,
        user_answer: str,
    ) -> ExerciseEvaluation:
        user_msg = build_verb_evaluation_prompt(
            verb, tense, person, prompt_native, expected_answer, user_answer,
        )
        messages = [
            SystemMessage(content=EXERCISE_EVALUATION_SYSTEM),
            HumanMessage(content=user_msg),
        ]
        try:
            result: _EvaluationOutput = await self._eval_chain.ainvoke(messages)
            return ExerciseEvaluation(
                is_correct=result.is_correct,
                feedback=result.feedback,
                correct_example=result.correct_example,
            )
        except Exception as exc:
            logger.error("Exercise evaluation failed: %s", exc, exc_info=True)
            raise LLMProviderError(self._provider, str(exc))

