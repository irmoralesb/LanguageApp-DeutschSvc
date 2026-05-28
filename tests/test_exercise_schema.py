"""Pydantic schema validation tests."""

import pytest
from pydantic import ValidationError
from uuid import uuid4

from application.schemas.exercise_schema import (
    VerbExerciseEvaluateRequest,
    VerbExerciseGenerateRequest,
)


def test_exercise_generate_accepts_optional_verb_and_situation() -> None:
    r = VerbExerciseGenerateRequest(tense="present", person="1sg", situation="office")
    assert r.tense == "present"
    assert r.person == "1sg"
    assert r.situation == "office"
    assert r.german_verb_id is None


def test_exercise_generate_defaults_to_present_third_person_singular() -> None:
    r = VerbExerciseGenerateRequest()
    assert r.tense == "present"
    assert r.person == "3sg"


def test_exercise_evaluate_requires_german_verb_id() -> None:
    with pytest.raises(ValidationError):
        VerbExerciseEvaluateRequest(
            tense="present",
            person="1sg",
            scenario_native="a",
            prompt_native="b",
            expected_answer="gehe",
            user_answer="gehe",
        )


def test_exercise_evaluate_accepts_valid_payload() -> None:
    vid = uuid4()
    req = VerbExerciseEvaluateRequest(
        german_verb_id=vid,
        tense="past",
        person="3sg",
        scenario_native="Im Park.",
        prompt_native="Schreibe die Verbform.",
        expected_answer="ging",
        user_answer="ging",
    )
    assert req.tense == "past"
    assert req.person == "3sg"
    assert req.expected_answer == "ging"


def test_exercise_generate_rejects_invalid_tense() -> None:
    with pytest.raises(ValidationError):
        VerbExerciseGenerateRequest(tense="invalid")


def test_exercise_generate_rejects_invalid_person() -> None:
    with pytest.raises(ValidationError):
        VerbExerciseGenerateRequest(person="invalid")
