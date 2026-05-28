import uuid
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.user_profile_model import (
    UserProfileModel,
    UserGermanNounSelectionModel,
    UserGermanVerbSelectionModel,
)
from domain.interfaces.user_profile_repository import UserProfileRepositoryInterface
from infrastructure.databases.models import (
    UserProfileDataModel,
    UserLearningLanguageDataModel,
    UserGermanNounSelectionDataModel,
    UserGermanVerbSelectionDataModel,
)


class UserProfileRepository(UserProfileRepositoryInterface):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_user_id(self, user_id: UUID) -> UserProfileModel | None:
        result = await self.db.execute(
            select(UserProfileDataModel).where(UserProfileDataModel.user_id == user_id)
        )
        row = result.scalars().first()
        if row is None:
            return None
        return self._to_domain(row)

    async def create(self, profile: UserProfileModel) -> UserProfileModel:
        db_profile = UserProfileDataModel(
            id=profile.id or uuid.uuid4(),
            user_id=profile.user_id,
            native_language_id=profile.native_language_id,
        )
        self.db.add(db_profile)
        await self.db.flush()

        for lang_id in profile.learning_language_ids:
            ll = UserLearningLanguageDataModel(
                id=uuid.uuid4(),
                user_id=profile.user_id,
                language_id=lang_id,
            )
            self.db.add(ll)

        await self.db.flush()
        await self.db.refresh(db_profile)
        return self._to_domain(db_profile)

    async def update(self, profile: UserProfileModel) -> UserProfileModel | None:
        result = await self.db.execute(
            select(UserProfileDataModel).where(UserProfileDataModel.user_id == profile.user_id)
        )
        db_profile = result.scalars().first()
        if db_profile is None:
            return None

        db_profile.native_language_id = profile.native_language_id
        db_profile.updated_at = datetime.now(timezone.utc)

        await self.db.flush()
        await self.db.refresh(db_profile)
        return self._to_domain(db_profile)

    async def add_learning_language(self, user_id: UUID, language_id: UUID) -> None:
        ll = UserLearningLanguageDataModel(
            id=uuid.uuid4(),
            user_id=user_id,
            language_id=language_id,
        )
        self.db.add(ll)
        await self.db.flush()

    async def remove_learning_language(self, user_id: UUID, language_id: UUID) -> None:
        await self.db.execute(
            delete(UserLearningLanguageDataModel).where(
                UserLearningLanguageDataModel.user_id == user_id,
                UserLearningLanguageDataModel.language_id == language_id,
            )
        )

    async def get_german_noun_selections(self, user_id: UUID) -> list[UserGermanNounSelectionModel]:
        result = await self.db.execute(
            select(UserGermanNounSelectionDataModel)
            .where(UserGermanNounSelectionDataModel.user_id == user_id)
            .order_by(UserGermanNounSelectionDataModel.added_at.desc())
        )
        return [
            UserGermanNounSelectionModel(
                id=r.id,
                user_id=r.user_id,
                german_noun_id=r.german_noun_id,
                added_at=r.added_at,
            )
            for r in result.scalars().all()
        ]

    async def add_german_noun_selection(
        self,
        user_id: UUID,
        german_noun_id: UUID,
    ) -> UserGermanNounSelectionModel:
        sel = UserGermanNounSelectionDataModel(
            id=uuid.uuid4(),
            user_id=user_id,
            german_noun_id=german_noun_id,
        )
        self.db.add(sel)
        await self.db.flush()
        await self.db.refresh(sel)
        return UserGermanNounSelectionModel(
            id=sel.id,
            user_id=sel.user_id,
            german_noun_id=sel.german_noun_id,
            added_at=sel.added_at,
        )

    async def remove_german_noun_selection(self, user_id: UUID, german_noun_id: UUID) -> bool:
        result = await self.db.execute(
            delete(UserGermanNounSelectionDataModel).where(
                UserGermanNounSelectionDataModel.user_id == user_id,
                UserGermanNounSelectionDataModel.german_noun_id == german_noun_id,
            )
        )
        return result.rowcount > 0

    async def get_german_verb_selections(self, user_id: UUID) -> list[UserGermanVerbSelectionModel]:
        result = await self.db.execute(
            select(UserGermanVerbSelectionDataModel)
            .where(UserGermanVerbSelectionDataModel.user_id == user_id)
            .order_by(UserGermanVerbSelectionDataModel.added_at.desc())
        )
        return [
            UserGermanVerbSelectionModel(
                id=r.id,
                user_id=r.user_id,
                german_verb_id=r.german_verb_id,
                added_at=r.added_at,
            )
            for r in result.scalars().all()
        ]

    async def add_german_verb_selection(
        self, user_id: UUID, german_verb_id: UUID,
    ) -> UserGermanVerbSelectionModel:
        sel = UserGermanVerbSelectionDataModel(
            id=uuid.uuid4(),
            user_id=user_id,
            german_verb_id=german_verb_id,
        )
        self.db.add(sel)
        await self.db.flush()
        await self.db.refresh(sel)
        return UserGermanVerbSelectionModel(
            id=sel.id,
            user_id=sel.user_id,
            german_verb_id=sel.german_verb_id,
            added_at=sel.added_at,
        )

    async def remove_german_verb_selection(self, user_id: UUID, german_verb_id: UUID) -> bool:
        result = await self.db.execute(
            delete(UserGermanVerbSelectionDataModel).where(
                UserGermanVerbSelectionDataModel.user_id == user_id,
                UserGermanVerbSelectionDataModel.german_verb_id == german_verb_id,
            )
        )
        return result.rowcount > 0

    @staticmethod
    def _to_domain(row: UserProfileDataModel) -> UserProfileModel:
        learning_ids = [ll.language_id for ll in row.learning_languages]
        return UserProfileModel(
            id=row.id,
            user_id=row.user_id,
            native_language_id=row.native_language_id,
            learning_language_ids=learning_ids,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )
