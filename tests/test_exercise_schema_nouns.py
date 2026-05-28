"""Pydantic schema validation tests."""

import pytest
from pydantic import ValidationError
from uuid import uuid4

from application.schemas.exercise_schema import (
    NounExerciseEvaluateRequest,
    NounExerciseGenerateRequest,
)


def test_exercise_generate_accepts_optional_noun_and_situation() -> None:
    r = NounExerciseGenerateRequest(exercise_mode="singular", situation="office")
    assert r.exercise_mode == "singular"
    assert r.situation == "office"
    assert r.german_noun_id is None


def test_exercise_generate_defaults_to_singular() -> None:
    r = NounExerciseGenerateRequest()
    assert r.exercise_mode == "singular"


def test_exercise_evaluate_requires_german_noun_id() -> None:
    with pytest.raises(ValidationError):
        NounExerciseEvaluateRequest(
            scenario_native="a",
            prompt_native="b",
            expected_answer="das Haus",
            user_answer="das Haus",
        )


def test_exercise_evaluate_accepts_valid_payload() -> None:
    vid = uuid4()
    req = NounExerciseEvaluateRequest(
        german_noun_id=vid,
        exercise_mode="plural",
        scenario_native="Im Garten.",
        prompt_native="Schreibe die Pluralform.",
        expected_answer="die Häuser",
        user_answer="die Häuser",
    )
    assert req.exercise_mode == "plural"
    assert req.expected_answer == "die Häuser"


def test_exercise_generate_rejects_invalid_mode() -> None:
    with pytest.raises(ValidationError):
        NounExerciseGenerateRequest(exercise_mode="invalid")
