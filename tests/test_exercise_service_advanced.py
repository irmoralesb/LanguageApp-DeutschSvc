import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from application.services.exercise_service import ExerciseService, _normalize_answer
from domain.entities.german_noun_model import GermanNounModel
from domain.entities.german_verb_model import GermanVerbModel, GermanVerbConjugationModel
from domain.entities.exercise_model import GermanNounStats, GermanVerbStats
from domain.exceptions.exercise_errors import ExerciseGenerationError


def _noun(**kwargs) -> GermanNounModel:
    defaults = dict(
        id=uuid4(),
        singular="Haus",
        plural="Häuser",
        article_singular="das",
        article_plural="die",
        definition="house",
    )
    defaults.update(kwargs)
    return GermanNounModel(**defaults)


def _verb(infinitive="gehen") -> GermanVerbModel:
    vid = uuid4()
    conjugations = [
        GermanVerbConjugationModel(id=uuid4(), verb_id=vid, tense="present", person="3sg", conjugated_form="geht"),
        GermanVerbConjugationModel(id=uuid4(), verb_id=vid, tense="present", person="1sg", conjugated_form="gehe"),
        GermanVerbConjugationModel(id=uuid4(), verb_id=vid, tense="past", person="3sg", conjugated_form="ging"),
    ]
    return GermanVerbModel(id=vid, infinitive=infinitive, definition="to go", conjugations=conjugations)


@pytest.fixture
def svc():
    return ExerciseService(
        exercise_repo=AsyncMock(),
        noun_repo=AsyncMock(),
        verb_repo=AsyncMock(),
        user_profile_repo=AsyncMock(),
        language_repo=AsyncMock(),
        llm_provider=AsyncMock(),
    )


@pytest.mark.asyncio
async def test_normalize_plural_answer():
    assert _normalize_answer("  Die  Häuser ") == "die häuser"


@pytest.mark.asyncio
async def test_gender_scope_selections_requires_selections(svc):
    user_id = uuid4()
    svc.user_profile_repo.get_german_noun_selections.return_value = []
    with pytest.raises(ExerciseGenerationError):
        await svc._nouns_for_gender_scope(user_id, "selections")


@pytest.mark.asyncio
async def test_plural_exercise_builds_options(svc):
    user_id = uuid4()
    noun = _noun()
    pool = [noun, _noun(id=uuid4(), singular="Auto", plural="Autos", article_singular="das", article_plural="die")]
    svc.user_profile_repo.get_german_noun_selections.return_value = [MagicMock(german_noun_id=n.id) for n in pool]
    svc.noun_repo.get_by_id.side_effect = lambda nid: next(n for n in pool if n.id == nid)
    svc.exercise_repo.get_noun_stats_by_user.return_value = []

    prompt = await svc.generate_noun_plural_exercise(user_id, german_noun_id=noun.id)
    assert prompt.german_noun_id == noun.id
    assert len(prompt.options) >= 2
    assert "die häuser" in [o.lower() for o in prompt.options]


@pytest.mark.asyncio
async def test_conjugation_evaluate_correct(svc):
    user_id = uuid4()
    verb = _verb()
    svc.verb_repo.get_by_id.return_value = verb
    result = await svc.evaluate_verb_conjugation_answer(
        user_id, verb.id, "present", "3sg", "geht",
    )
    assert result.is_correct is True
    svc.exercise_repo.save_verb_result.assert_awaited_once()
