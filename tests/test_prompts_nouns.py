"""Unit tests for infrastructure.llm.prompts."""

from uuid import uuid4

from domain.entities.german_noun_model import GermanNounModel
from infrastructure.llm.prompts import (
    EXERCISE_EVALUATION_SYSTEM,
    EXERCISE_GENERATION_SYSTEM,
    build_noun_evaluation_prompt,
    build_noun_exercise_prompt,
)


def _sample_noun() -> GermanNounModel:
    return GermanNounModel(
        id=uuid4(),
        singular="Haus",
        plural="Häuser",
        article_singular="das",
        article_plural="die",
        definition="Gebäude zum Wohnen.",
    )


def test_system_prompts_are_non_empty() -> None:
    assert EXERCISE_GENERATION_SYSTEM
    assert "JSON" in EXERCISE_GENERATION_SYSTEM
    assert EXERCISE_EVALUATION_SYSTEM
    assert "article" in EXERCISE_EVALUATION_SYSTEM.lower()


def test_build_noun_exercise_prompt_contains_inputs() -> None:
    noun = _sample_noun()
    msg = build_noun_exercise_prompt(
        noun=noun,
        native_language="es",
        exercise_mode="singular",
        situation="work",
    )
    assert "Haus" in msg
    assert "das Haus" in msg
    assert "Gebäude" in msg
    assert "es" in msg
    assert "work" in msg


def test_build_noun_exercise_prompt_plural_mode() -> None:
    noun = _sample_noun()
    msg = build_noun_exercise_prompt(
        noun=noun,
        native_language="de",
        exercise_mode="plural",
        situation=None,
    )
    assert "plural" in msg.lower()
    assert "die Häuser" in msg
    assert "everyday" in msg.lower() or "context" in msg.lower()


def test_build_noun_evaluation_prompt_contains_answer() -> None:
    noun = _sample_noun()
    msg = build_noun_evaluation_prompt(
        noun=noun,
        exercise_mode="singular",
        prompt_native="Schreibe das Nomen im Singular.",
        expected_answer="das Haus",
        user_answer="die Haus",
    )
    assert "Haus" in msg
    assert "das Haus" in msg
    assert "die Haus" in msg
    assert "singular" in msg
