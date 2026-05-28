from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from domain.entities.german_noun_model import GermanNounModel
from domain.exceptions.german_noun_errors import GermanNounNotFoundError, GermanNounDataAccessError
from domain.interfaces.german_noun_repository import GermanNounRepositoryInterface
from infrastructure.databases.models import GermanNounDataModel


class GermanNounRepository(GermanNounRepositoryInterface):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    def _to_domain(self, row: GermanNounDataModel) -> GermanNounModel:
        return GermanNounModel(
            id=row.id,
            singular=row.singular,
            plural=row.plural,
            article_singular=row.article_singular,
            article_plural=row.article_plural,
            definition=row.definition,
            is_catalog=row.is_catalog,
            created_by_user_id=row.created_by_user_id,
        )

    async def get_catalog(self, skip: int = 0, limit: int = 100) -> list[GermanNounModel]:
        try:
            stmt = (
                select(GermanNounDataModel)
                .where(GermanNounDataModel.is_catalog == 1)
                .order_by(GermanNounDataModel.singular)
                .offset(skip)
                .limit(limit)
            )
            result = await self.db.execute(stmt)
            return [self._to_domain(r) for r in result.scalars().all()]
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise GermanNounDataAccessError() from e

    async def get_by_id(self, noun_id: UUID) -> GermanNounModel | None:
        try:
            stmt = select(GermanNounDataModel).where(GermanNounDataModel.id == noun_id)
            result = await self.db.execute(stmt)
            row = result.scalars().first()
            return self._to_domain(row) if row else None
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise GermanNounDataAccessError() from e

    async def create(self, noun: GermanNounModel) -> GermanNounModel:
        try:
            row = GermanNounDataModel(
                singular=noun.singular,
                plural=noun.plural,
                article_singular=noun.article_singular,
                article_plural=noun.article_plural,
                definition=noun.definition,
                is_catalog=noun.is_catalog,
                created_by_user_id=noun.created_by_user_id,
            )
            self.db.add(row)
            await self.db.commit()
            await self.db.refresh(row)
            return self._to_domain(row)
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise GermanNounDataAccessError() from e

    async def update(self, noun: GermanNounModel) -> GermanNounModel:
        try:
            stmt = select(GermanNounDataModel).where(GermanNounDataModel.id == noun.id)
            result = await self.db.execute(stmt)
            row = result.scalars().first()
            if row is None:
                raise GermanNounNotFoundError(noun.id)
            row.singular = noun.singular
            row.plural = noun.plural
            row.article_singular = noun.article_singular
            row.article_plural = noun.article_plural
            row.definition = noun.definition
            row.is_catalog = noun.is_catalog
            await self.db.commit()
            await self.db.refresh(row)
            return self._to_domain(row)
        except GermanNounNotFoundError:
            raise
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise GermanNounDataAccessError() from e

    async def delete(self, noun_id: UUID) -> bool:
        try:
            stmt = select(GermanNounDataModel).where(GermanNounDataModel.id == noun_id)
            result = await self.db.execute(stmt)
            row = result.scalars().first()
            if row is None:
                return False
            await self.db.delete(row)
            await self.db.commit()
            return True
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise GermanNounDataAccessError() from e
