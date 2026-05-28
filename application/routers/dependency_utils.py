from typing import Annotated, AsyncIterator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from core.settings import app_settings
from infrastructure.databases.database import get_monitored_db_session
from infrastructure.repositories.language_repository import LanguageRepository
from infrastructure.repositories.german_noun_repository import GermanNounRepository
from infrastructure.repositories.german_verb_repository import GermanVerbRepository
from infrastructure.repositories.user_profile_repository import UserProfileRepository
from infrastructure.repositories.exercise_repository import ExerciseRepository
from application.services.token_service import TokenService
from application.services.authorization_service import AuthorizationService
from application.services.german_noun_catalog_service import GermanNounCatalogService
from application.services.german_verb_catalog_service import GermanVerbCatalogService
from application.services.user_profile_service import UserProfileService
from application.services.exercise_service import ExerciseService
from domain.entities.token_claims import UserClaims
from domain.exceptions.auth_errors import MissingRoleError
from domain.interfaces.llm_provider import LLMProviderInterface


async def get_db_session() -> AsyncIterator[AsyncSession]:
    async with get_monitored_db_session() as db:
        yield db


def get_language_repository(db: Annotated[AsyncSession, Depends(get_db_session)]) -> LanguageRepository:
    return LanguageRepository(db)


def get_german_noun_repository(db: Annotated[AsyncSession, Depends(get_db_session)]) -> GermanNounRepository:
    return GermanNounRepository(db)


def get_german_verb_repository(db: Annotated[AsyncSession, Depends(get_db_session)]) -> GermanVerbRepository:
    return GermanVerbRepository(db)


def get_user_profile_repository(db: Annotated[AsyncSession, Depends(get_db_session)]) -> UserProfileRepository:
    return UserProfileRepository(db)


def get_exercise_repository(db: Annotated[AsyncSession, Depends(get_db_session)]) -> ExerciseRepository:
    return ExerciseRepository(db)


def get_llm_provider() -> LLMProviderInterface:
    from infrastructure.llm.langchain_provider import LangChainProvider
    return LangChainProvider(
        provider=app_settings.llm_provider,
        api_key=app_settings.llm_api_key,
        model=app_settings.llm_model,
        max_tokens=app_settings.llm_max_tokens,
        temperature=app_settings.llm_temperature,
    )


def get_german_verb_catalog_service(
    repo: Annotated[GermanVerbRepository, Depends(get_german_verb_repository)],
) -> GermanVerbCatalogService:
    return GermanVerbCatalogService(repo)


def get_german_noun_catalog_service(
    repo: Annotated[GermanNounRepository, Depends(get_german_noun_repository)],
) -> GermanNounCatalogService:
    return GermanNounCatalogService(repo)


def get_user_profile_service(
    profile_repo: Annotated[UserProfileRepository, Depends(get_user_profile_repository)],
    language_repo: Annotated[LanguageRepository, Depends(get_language_repository)],
) -> UserProfileService:
    return UserProfileService(profile_repo, language_repo)


def get_exercise_service(
    exercise_repo: Annotated[ExerciseRepository, Depends(get_exercise_repository)],
    noun_repo: Annotated[GermanNounRepository, Depends(get_german_noun_repository)],
    verb_repo: Annotated[GermanVerbRepository, Depends(get_german_verb_repository)],
    profile_repo: Annotated[UserProfileRepository, Depends(get_user_profile_repository)],
    language_repo: Annotated[LanguageRepository, Depends(get_language_repository)],
    llm: Annotated[LLMProviderInterface, Depends(get_llm_provider)],
) -> ExerciseService:
    return ExerciseService(exercise_repo, noun_repo, verb_repo, profile_repo, language_repo, llm)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=app_settings.token_url)


def get_token_service() -> TokenService:
    return TokenService(
        secret_key=app_settings.secret_token_key,
        algorithm=app_settings.auth_algorithm,
    )


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    token_svc: Annotated[TokenService, Depends(get_token_service)],
) -> UserClaims:
    return token_svc.decode_token(token)


def require_role(role_name: str):
    async def _check(
        current_user: Annotated[UserClaims, Depends(get_current_user)],
    ) -> UserClaims:
        auth = AuthorizationService(app_settings.service_name)
        try:
            auth.check_role(current_user, role_name)
        except MissingRoleError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Role required: {role_name}")
        return current_user
    return _check


GermanNounSvcDep = Annotated[GermanNounCatalogService, Depends(get_german_noun_catalog_service)]
GermanVerbSvcDep = Annotated[GermanVerbCatalogService, Depends(get_german_verb_catalog_service)]
UserProfileSvcDep = Annotated[UserProfileService, Depends(get_user_profile_service)]
ExerciseSvcDep = Annotated[ExerciseService, Depends(get_exercise_service)]
LanguageRepoDep = Annotated[LanguageRepository, Depends(get_language_repository)]
CurrentUserDep = Annotated[UserClaims, Depends(get_current_user)]
