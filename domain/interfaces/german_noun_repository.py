from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities.german_noun_model import GermanNounModel


class GermanNounRepositoryInterface(ABC):
    @abstractmethod
    async def get_catalog(self, skip: int = 0, limit: int = 100) -> list[GermanNounModel]:
        pass

    @abstractmethod
    async def get_by_id(self, noun_id: UUID) -> GermanNounModel | None:
        pass

    @abstractmethod
    async def create(self, noun: GermanNounModel) -> GermanNounModel:
        pass

    @abstractmethod
    async def update(self, noun: GermanNounModel) -> GermanNounModel:
        pass

    @abstractmethod
    async def delete(self, noun_id: UUID) -> bool:
        pass
