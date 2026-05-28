from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.german_verb_model import GermanVerbModel


class GermanVerbRepositoryInterface(ABC):
    @abstractmethod
    async def get_catalog(self, skip: int = 0, limit: int = 100) -> list[GermanVerbModel]:
        pass

    @abstractmethod
    async def get_by_id(self, verb_id: UUID) -> GermanVerbModel | None:
        pass

    @abstractmethod
    async def create(self, verb: GermanVerbModel) -> GermanVerbModel:
        pass

    @abstractmethod
    async def update(self, verb: GermanVerbModel) -> GermanVerbModel:
        pass

    @abstractmethod
    async def delete(self, verb_id: UUID) -> bool:
        pass
