from uuid import UUID

from domain.entities.german_noun_model import GermanNounModel
from domain.exceptions.german_noun_errors import GermanNounNotFoundError
from domain.interfaces.german_noun_repository import GermanNounRepositoryInterface


class GermanNounCatalogService:
    def __init__(self, repo: GermanNounRepositoryInterface) -> None:
        self.repo = repo

    async def get_catalog(self, skip: int = 0, limit: int = 100) -> list[GermanNounModel]:
        return await self.repo.get_catalog(skip=skip, limit=limit)

    async def get_by_id(self, noun_id: UUID) -> GermanNounModel:
        noun = await self.repo.get_by_id(noun_id)
        if noun is None:
            raise GermanNounNotFoundError(noun_id)
        return noun

    async def add_custom_term(self, user_id: UUID, noun: GermanNounModel) -> GermanNounModel:
        noun.is_catalog = False
        noun.created_by_user_id = user_id
        return await self.repo.create(noun)

    async def add_to_catalog(self, noun: GermanNounModel) -> GermanNounModel:
        noun.is_catalog = True
        noun.created_by_user_id = None
        return await self.repo.create(noun)

    async def update(self, noun: GermanNounModel) -> GermanNounModel:
        return await self.repo.update(noun)

    async def delete(self, noun_id: UUID) -> bool:
        return await self.repo.delete(noun_id)
