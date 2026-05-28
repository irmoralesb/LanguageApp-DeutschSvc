from uuid import UUID

from fastapi import APIRouter, Depends, status

from application.routers.dependency_utils import (
    UserProfileSvcDep,
    CurrentUserDep,
    require_role,
)
from application.schemas.user_profile_schema import (
    UserProfileCreate,
    UserProfileUpdate,
    UserProfileResponse,
    AddLearningLanguage,
    AddGermanNounSelection,
    GermanNounSelectionResponse,
    AddGermanVerbSelection,
    GermanVerbSelectionResponse,
)

router = APIRouter(
    prefix="/api/v1/profile",
    tags=["User Profile"],
    dependencies=[Depends(require_role("deutsch-user"))],
)


def _profile_response(profile) -> UserProfileResponse:
    return UserProfileResponse(
        id=profile.id,
        user_id=profile.user_id,
        native_language_id=profile.native_language_id,
        learning_language_ids=profile.learning_language_ids,
        created_at=profile.created_at,
        updated_at=profile.updated_at,
    )


@router.get("", response_model=UserProfileResponse)
async def get_profile(svc: UserProfileSvcDep, current_user: CurrentUserDep):
    return _profile_response(await svc.get_profile(current_user.user_id))


@router.post("", response_model=UserProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_profile(payload: UserProfileCreate, svc: UserProfileSvcDep, current_user: CurrentUserDep):
    profile = await svc.create_profile(
        user_id=current_user.user_id,
        native_language_id=payload.native_language_id,
        learning_language_ids=payload.learning_language_ids,
    )
    return _profile_response(profile)


@router.put("", response_model=UserProfileResponse)
async def update_profile(payload: UserProfileUpdate, svc: UserProfileSvcDep, current_user: CurrentUserDep):
    profile = await svc.update_profile(current_user.user_id, payload.native_language_id)
    return _profile_response(profile)


@router.post("/learning-languages", status_code=status.HTTP_204_NO_CONTENT)
async def add_learning_language(payload: AddLearningLanguage, svc: UserProfileSvcDep, current_user: CurrentUserDep):
    await svc.add_learning_language(current_user.user_id, payload.language_id)


@router.delete("/learning-languages/{language_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_learning_language(language_id: UUID, svc: UserProfileSvcDep, current_user: CurrentUserDep):
    await svc.remove_learning_language(current_user.user_id, language_id)


@router.get("/german-nouns", response_model=list[GermanNounSelectionResponse])
async def get_noun_selections(svc: UserProfileSvcDep, current_user: CurrentUserDep):
    selections = await svc.get_german_noun_selections(current_user.user_id)
    return [
        GermanNounSelectionResponse(
            id=s.id,
            user_id=s.user_id,
            german_noun_id=s.german_noun_id,
            added_at=s.added_at,
        )
        for s in selections
    ]


@router.post("/german-nouns", response_model=GermanNounSelectionResponse, status_code=status.HTTP_201_CREATED)
async def add_noun_selection(payload: AddGermanNounSelection, svc: UserProfileSvcDep, current_user: CurrentUserDep):
    sel = await svc.add_german_noun_selection(current_user.user_id, payload.german_noun_id)
    return GermanNounSelectionResponse(
        id=sel.id,
        user_id=sel.user_id,
        german_noun_id=sel.german_noun_id,
        added_at=sel.added_at,
    )


@router.delete("/german-nouns/{german_noun_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_noun_selection(german_noun_id: UUID, svc: UserProfileSvcDep, current_user: CurrentUserDep):
    await svc.remove_german_noun_selection(current_user.user_id, german_noun_id)


@router.get("/german-verbs", response_model=list[GermanVerbSelectionResponse])
async def get_verb_selections(svc: UserProfileSvcDep, current_user: CurrentUserDep):
    selections = await svc.get_german_verb_selections(current_user.user_id)
    return [
        GermanVerbSelectionResponse(
            id=s.id,
            user_id=s.user_id,
            german_verb_id=s.german_verb_id,
            added_at=s.added_at,
        )
        for s in selections
    ]


@router.post("/german-verbs", response_model=GermanVerbSelectionResponse, status_code=status.HTTP_201_CREATED)
async def add_verb_selection(payload: AddGermanVerbSelection, svc: UserProfileSvcDep, current_user: CurrentUserDep):
    sel = await svc.add_german_verb_selection(current_user.user_id, payload.german_verb_id)
    return GermanVerbSelectionResponse(
        id=sel.id,
        user_id=sel.user_id,
        german_verb_id=sel.german_verb_id,
        added_at=sel.added_at,
    )


@router.delete("/german-verbs/{german_verb_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_verb_selection(german_verb_id: UUID, svc: UserProfileSvcDep, current_user: CurrentUserDep):
    await svc.remove_german_verb_selection(current_user.user_id, german_verb_id)
