from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload

from domain.entities.german_verb_model import GermanVerbModel, GermanVerbConjugationModel
from domain.exceptions.german_verb_errors import GermanVerbNotFoundError, GermanVerbDataAccessError
from domain.interfaces.german_verb_repository import GermanVerbRepositoryInterface
from infrastructure.databases.models import GermanVerbDataModel, GermanVerbConjugationDataModel


class GermanVerbRepository(GermanVerbRepositoryInterface):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    def _to_domain(self, row: GermanVerbDataModel) -> GermanVerbModel:
        conjugations = [
            GermanVerbConjugationModel(
                id=c.id,
                verb_id=c.verb_id,
                tense=c.tense,
                person=c.person,
                conjugated_form=c.conjugated_form,
            )
            for c in row.conjugations
        ]
        return GermanVerbModel(
            id=row.id,
            infinitive=row.infinitive,
            definition=row.definition,
            conjugations=conjugations,
            is_catalog=row.is_catalog,
            created_by_user_id=row.created_by_user_id,
        )

    async def get_catalog(self, skip: int = 0, limit: int = 100) -> list[GermanVerbModel]:
        try:
            stmt = (
                select(GermanVerbDataModel)
                .options(selectinload(GermanVerbDataModel.conjugations))
                .where(GermanVerbDataModel.is_catalog == 1)
                .order_by(GermanVerbDataModel.infinitive)
                .offset(skip)
                .limit(limit)
            )
            result = await self.db.execute(stmt)
            return [self._to_domain(r) for r in result.scalars().all()]
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise GermanVerbDataAccessError() from e

    async def get_by_id(self, verb_id: UUID) -> GermanVerbModel | None:
        try:
            stmt = (
                select(GermanVerbDataModel)
                .options(selectinload(GermanVerbDataModel.conjugations))
                .where(GermanVerbDataModel.id == verb_id)
            )
            result = await self.db.execute(stmt)
            row = result.scalars().first()
            return self._to_domain(row) if row else None
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise GermanVerbDataAccessError() from e

    async def create(self, verb: GermanVerbModel) -> GermanVerbModel:
        try:
            row = GermanVerbDataModel(
                infinitive=verb.infinitive,
                definition=verb.definition,
                is_catalog=verb.is_catalog,
                created_by_user_id=verb.created_by_user_id,
            )
            self.db.add(row)
            await self.db.flush()
            for c in verb.conjugations:
                self.db.add(GermanVerbConjugationDataModel(
                    verb_id=row.id,
                    tense=c.tense,
                    person=c.person,
                    conjugated_form=c.conjugated_form,
                ))
            await self.db.commit()
            await self.db.refresh(row, attribute_names=["conjugations"])
            return self._to_domain(row)
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise GermanVerbDataAccessError() from e

    async def update(self, verb: GermanVerbModel) -> GermanVerbModel:
        try:
            stmt = (
                select(GermanVerbDataModel)
                .options(selectinload(GermanVerbDataModel.conjugations))
                .where(GermanVerbDataModel.id == verb.id)
            )
            result = await self.db.execute(stmt)
            row = result.scalars().first()
            if row is None:
                raise GermanVerbNotFoundError(verb.id)
            row.infinitive = verb.infinitive
            row.definition = verb.definition
            row.is_catalog = verb.is_catalog
            await self.db.commit()
            await self.db.refresh(row, attribute_names=["conjugations"])
            return self._to_domain(row)
        except GermanVerbNotFoundError:
            raise
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise GermanVerbDataAccessError() from e

    async def delete(self, verb_id: UUID) -> bool:
        try:
            stmt = select(GermanVerbDataModel).where(GermanVerbDataModel.id == verb_id)
            result = await self.db.execute(stmt)
            row = result.scalars().first()
            if row is None:
                return False
            await self.db.delete(row)
            await self.db.commit()
            return True
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise GermanVerbDataAccessError() from e

