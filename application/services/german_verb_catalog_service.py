from uuid import UUID



from domain.entities.german_verb_model import GermanVerbModel

from domain.exceptions.german_verb_errors import GermanVerbNotFoundError

from domain.interfaces.german_verb_repository import GermanVerbRepositoryInterface





class GermanVerbCatalogService:

    def __init__(self, repo: GermanVerbRepositoryInterface) -> None:

        self.repo = repo



    async def get_catalog(self, skip: int = 0, limit: int = 100) -> list[GermanVerbModel]:

        return await self.repo.get_catalog(skip=skip, limit=limit)



    async def get_by_id(self, verb_id: UUID) -> GermanVerbModel:

        verb = await self.repo.get_by_id(verb_id)

        if verb is None:

            raise GermanVerbNotFoundError(verb_id)

        return verb



    async def add_custom_term(self, user_id: UUID, verb: GermanVerbModel) -> GermanVerbModel:

        verb.is_catalog = False

        verb.created_by_user_id = user_id

        return await self.repo.create(verb)


