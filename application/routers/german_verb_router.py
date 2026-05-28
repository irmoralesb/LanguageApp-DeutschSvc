from uuid import UUID

from fastapi import APIRouter, Depends, status

from application.routers.dependency_utils import (
    GermanVerbSvcDep,
    CurrentUserDep,
    require_role,
)
from application.schemas.german_verb_schema import (
    GermanVerbCreate,
    GermanVerbResponse,
    GermanVerbConjugationResponse,
)
from domain.entities.german_verb_model import GermanVerbModel

router = APIRouter(
    prefix="/api/v1/german-verbs",
    tags=["German verbs"],
)


def _to_response(v: GermanVerbModel) -> GermanVerbResponse:
    return GermanVerbResponse(
        id=v.id,
        infinitive=v.infinitive,
        definition=v.definition,
        is_catalog=v.is_catalog,
        conjugations=[
            GermanVerbConjugationResponse(
                id=c.id,
                tense=c.tense,
                person=c.person,
                conjugated_form=c.conjugated_form,
            )
            for c in v.conjugations
        ],
    )


@router.get(
    "/catalog",
    response_model=list[GermanVerbResponse],
    dependencies=[Depends(require_role("deutsch-user"))],
)
async def get_catalog(svc: GermanVerbSvcDep, current_user: CurrentUserDep, skip: int = 0, limit: int = 100):
    items = await svc.get_catalog(skip=skip, limit=limit)
    return [_to_response(i) for i in items]


@router.get(
    "/{german_verb_id}",
    response_model=GermanVerbResponse,
    dependencies=[Depends(require_role("deutsch-user"))],
)
async def get_verb(german_verb_id: UUID, svc: GermanVerbSvcDep, current_user: CurrentUserDep):
    return _to_response(await svc.get_by_id(german_verb_id))


@router.post(
    "/custom",
    response_model=GermanVerbResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role("deutsch-user"))],
)
async def create_custom(payload: GermanVerbCreate, svc: GermanVerbSvcDep, current_user: CurrentUserDep):
    verb = GermanVerbModel(
        id=None,
        infinitive=payload.infinitive,
        definition=payload.definition,
    )
    return _to_response(await svc.add_custom_term(current_user.user_id, verb))
