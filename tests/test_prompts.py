"""Unit tests for infrastructure.llm.prompts."""

from uuid import uuid4

from domain.entities.german_verb_model import GermanVerbConjugationModel, GermanVerbModel
from infrastructure.llm.prompts import (
    EXERCISE_EVALUATION_SYSTEM,
    EXERCISE_GENERATION_SYSTEM,
    build_verb_evaluation_prompt,
    build_verb_exercise_prompt,
)


def _sample_verb() -> GermanVerbModel:
    verb_id = uuid4()
    return GermanVerbModel(
        id=verb_id,
        infinitive="gehen",
        definition="Zu Fuß sich bewegen.",
        conjugations=[
            GermanVerbConjugationModel(
                id=uuid4(),
                verb_id=verb_id,
                tense="present",
                person="1sg",
                conjugated_form="gehe",
            ),
            GermanVerbConjugationModel(
                id=uuid4(),
                verb_id=verb_id,
                tense="past",
                person="3sg",
                conjugated_form="ging",
            ),
        ],
    )


def test_system_prompts_are_non_empty() -> None:
    assert EXERCISE_GENERATION_SYSTEM
    assert "JSON" in EXERCISE_GENERATION_SYSTEM
    assert EXERCISE_EVALUATION_SYSTEM
    assert "tense" in EXERCISE_EVALUATION_SYSTEM.lower()


def test_build_verb_exercise_prompt_contains_inputs() -> None:
    verb = _sample_verb()
    msg = build_verb_exercise_prompt(
        verb=verb,
        native_language="es",
        tense="present",
        person="1sg",
        situation="work",
    )
    assert "gehen" in msg
    assert "gehe" in msg
    assert "Zu Fuß" in msg
    assert "es" in msg
    assert "work" in msg


def test_build_verb_exercise_prompt_without_situation() -> None:
    verb = _sample_verb()
    msg = build_verb_exercise_prompt(
        verb=verb,
        native_language="de",
        tense="past",
        person="3sg",
        situation=None,
    )
    assert "Präteritum" in msg
    assert "ging" in msg
    assert "everyday" in msg.lower() or "context" in msg.lower()


def test_build_verb_evaluation_prompt_contains_answer() -> None:
    verb = _sample_verb()
    msg = build_verb_evaluation_prompt(
        verb=verb,
        tense="present",
        person="1sg",
        prompt_native="Schreibe die richtige Verbform.",
        expected_answer="gehe",
        user_answer="geht",
    )
    assert "gehen" in msg
    assert "gehe" in msg
    assert "geht" in msg
    assert "ich" in msg
