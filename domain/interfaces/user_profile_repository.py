from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.user_profile_model import (
    UserProfileModel,
    UserGermanNounSelectionModel,
    UserGermanVerbSelectionModel,
)


class UserProfileRepositoryInterface(ABC):
    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> UserProfileModel | None:
        pass

    @abstractmethod
    async def create(self, profile: UserProfileModel) -> UserProfileModel:
        pass

    @abstractmethod
    async def update(self, profile: UserProfileModel) -> UserProfileModel | None:
        pass

    @abstractmethod
    async def add_learning_language(self, user_id: UUID, language_id: UUID) -> None:
        pass

    @abstractmethod
    async def remove_learning_language(self, user_id: UUID, language_id: UUID) -> None:
        pass

    @abstractmethod
    async def get_german_noun_selections(self, user_id: UUID) -> list[UserGermanNounSelectionModel]:
        pass

    @abstractmethod
    async def add_german_noun_selection(
        self, user_id: UUID, german_noun_id: UUID,
    ) -> UserGermanNounSelectionModel:
        pass

    @abstractmethod
    async def remove_german_noun_selection(self, user_id: UUID, german_noun_id: UUID) -> bool:
        pass

    @abstractmethod
    async def get_german_verb_selections(self, user_id: UUID) -> list[UserGermanVerbSelectionModel]:
        pass

    @abstractmethod
    async def add_german_verb_selection(
        self, user_id: UUID, german_verb_id: UUID,
    ) -> UserGermanVerbSelectionModel:
        pass

    @abstractmethod
    async def remove_german_verb_selection(self, user_id: UUID, german_verb_id: UUID) -> bool:
        pass
