from uuid import UUID

from fastapi import APIRouter, Depends, status

from application.routers.dependency_utils import (
    GermanNounSvcDep,
    CurrentUserDep,
    require_role,
)
from application.schemas.german_noun_schema import (
    GermanNounCreate,
    GermanNounResponse,
)
from domain.entities.german_noun_model import GermanNounModel

router = APIRouter(
    prefix="/api/v1/german-nouns",
    tags=["German nouns"],
)


def _to_response(n: GermanNounModel) -> GermanNounResponse:
    return GermanNounResponse(
        id=n.id,
        singular=n.singular,
        plural=n.plural,
        article_singular=n.article_singular,
        article_plural=n.article_plural,
        definition=n.definition,
        is_catalog=n.is_catalog,
    )


@router.get(
    "/catalog",
    response_model=list[GermanNounResponse],
    dependencies=[Depends(require_role("deutsch-user"))],
)
async def get_catalog(svc: GermanNounSvcDep, current_user: CurrentUserDep, skip: int = 0, limit: int = 100):
    items = await svc.get_catalog(skip=skip, limit=limit)
    return [_to_response(i) for i in items]


@router.get(
    "/{german_noun_id}",
    response_model=GermanNounResponse,
    dependencies=[Depends(require_role("deutsch-user"))],
)
async def get_noun(german_noun_id: UUID, svc: GermanNounSvcDep, current_user: CurrentUserDep):
    return _to_response(await svc.get_by_id(german_noun_id))


@router.post(
    "/custom",
    response_model=GermanNounResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role("deutsch-user"))],
)
async def create_custom(payload: GermanNounCreate, svc: GermanNounSvcDep, current_user: CurrentUserDep):
    noun = GermanNounModel(
        id=None,
        singular=payload.singular,
        plural=payload.plural,
        article_singular=payload.article_singular,
        article_plural=payload.article_plural,
        definition=payload.definition,
    )
    return _to_response(await svc.add_custom_term(current_user.user_id, noun))
