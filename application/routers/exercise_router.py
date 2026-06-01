from fastapi import APIRouter, Depends

from application.routers.dependency_utils import (
    ExerciseSvcDep,
    CurrentUserDep,
    require_role,
)
from application.schemas.exercise_schema import (
    NounGenderExerciseGenerateRequest,
    NounGenderExerciseGenerateResponse,
    NounGenderExerciseItemResponse,
    NounGenderExerciseEvaluateRequest,
    NounGenderExerciseEvaluateResponse,
    NounExerciseGenerateRequest,
    NounExerciseGenerateResponse,
    NounExerciseEvaluateRequest,
    NounExerciseEvaluateResponse,
    VerbExerciseGenerateRequest,
    VerbExerciseGenerateResponse,
    VerbExerciseEvaluateRequest,
    VerbExerciseEvaluateResponse,
)

router = APIRouter(
    prefix="/api/v1/exercises",
    tags=["Exercises"],
    dependencies=[Depends(require_role("deutsch-user"))],
)


@router.post("/nouns/gender/generate", response_model=NounGenderExerciseGenerateResponse)
async def generate_noun_gender_exercise(
    payload: NounGenderExerciseGenerateRequest,
    svc: ExerciseSvcDep,
    current_user: CurrentUserDep,
):
    nouns = await svc.generate_noun_gender_exercise(
        user_id=current_user.user_id,
        count=payload.count,
    )
    return NounGenderExerciseGenerateResponse(
        target_score=payload.target_score,
        nouns=[
            NounGenderExerciseItemResponse(
                german_noun_id=n.german_noun_id,
                singular=n.singular,
                definition=n.definition,
                incorrect_attempts=n.incorrect_attempts,
                correct_attempts=n.correct_attempts,
            )
            for n in nouns
        ],
    )


@router.post("/nouns/gender/evaluate", response_model=NounGenderExerciseEvaluateResponse)
async def evaluate_noun_gender_answer(
    payload: NounGenderExerciseEvaluateRequest,
    svc: ExerciseSvcDep,
    current_user: CurrentUserDep,
):
    evaluation = await svc.evaluate_noun_gender_answer(
        user_id=current_user.user_id,
        german_noun_id=payload.german_noun_id,
        selected_article=payload.selected_article,
    )
    return NounGenderExerciseEvaluateResponse(
        is_correct=evaluation.is_correct,
        correct_article=(evaluation.correct_example or "").split(" ", 1)[0],
        feedback=evaluation.feedback,
    )


@router.post("/nouns/generate", response_model=NounExerciseGenerateResponse)
async def generate_noun_exercise(
    payload: NounExerciseGenerateRequest,
    svc: ExerciseSvcDep,
    current_user: CurrentUserDep,
):
    prompt = await svc.generate_noun_exercise(
        user_id=current_user.user_id,
        exercise_mode=payload.exercise_mode,
        german_noun_id=payload.german_noun_id,
        situation=payload.situation,
    )
    assert prompt.german_noun_id is not None
    return NounExerciseGenerateResponse(
        german_noun_id=prompt.german_noun_id,
        target_language_code=prompt.target_language_code,
        exercise_mode=prompt.exercise_mode,
        scenario_native=prompt.scenario_native,
        prompt_native=prompt.prompt_native,
        expected_answer=prompt.expected_answer,
    )


@router.post("/nouns/evaluate", response_model=NounExerciseEvaluateResponse)
async def evaluate_noun_answer(
    payload: NounExerciseEvaluateRequest,
    svc: ExerciseSvcDep,
    current_user: CurrentUserDep,
):
    evaluation = await svc.evaluate_noun_answer(
        user_id=current_user.user_id,
        german_noun_id=payload.german_noun_id,
        exercise_mode=payload.exercise_mode,
        scenario_native=payload.scenario_native,
        prompt_native=payload.prompt_native,
        expected_answer=payload.expected_answer,
        user_answer=payload.user_answer,
    )
    return NounExerciseEvaluateResponse(
        is_correct=evaluation.is_correct,
        feedback=evaluation.feedback,
        correct_example=evaluation.correct_example,
    )


@router.post("/verbs/generate", response_model=VerbExerciseGenerateResponse)
async def generate_verb_exercise(
    payload: VerbExerciseGenerateRequest,
    svc: ExerciseSvcDep,
    current_user: CurrentUserDep,
):
    prompt = await svc.generate_verb_exercise(
        user_id=current_user.user_id,
        tense=payload.tense,
        person=payload.person,
        german_verb_id=payload.german_verb_id,
        situation=payload.situation,
    )
    assert prompt.german_verb_id is not None
    return VerbExerciseGenerateResponse(
        german_verb_id=prompt.german_verb_id,
        target_language_code=prompt.target_language_code,
        tense=prompt.tense,
        person=prompt.person,
        scenario_native=prompt.scenario_native,
        prompt_native=prompt.prompt_native,
        expected_answer=prompt.expected_answer,
    )


@router.post("/verbs/evaluate", response_model=VerbExerciseEvaluateResponse)
async def evaluate_verb_answer(
    payload: VerbExerciseEvaluateRequest,
    svc: ExerciseSvcDep,
    current_user: CurrentUserDep,
):
    evaluation = await svc.evaluate_verb_answer(
        user_id=current_user.user_id,
        german_verb_id=payload.german_verb_id,
        tense=payload.tense,
        person=payload.person,
        scenario_native=payload.scenario_native,
        prompt_native=payload.prompt_native,
        expected_answer=payload.expected_answer,
        user_answer=payload.user_answer,
    )
    return VerbExerciseEvaluateResponse(
        is_correct=evaluation.is_correct,
        feedback=evaluation.feedback,
        correct_example=evaluation.correct_example,
    )
