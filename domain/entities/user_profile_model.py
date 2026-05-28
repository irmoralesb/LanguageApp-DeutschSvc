from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class UserProfileModel:
    id: UUID | None
    user_id: UUID
    native_language_id: UUID
    learning_language_ids: list[UUID]
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class UserGermanNounSelectionModel:
    id: UUID | None
    user_id: UUID
    german_noun_id: UUID
    added_at: datetime | None = None


@dataclass
class UserGermanVerbSelectionModel:
    id: UUID | None
    user_id: UUID
    german_verb_id: UUID
    added_at: datetime | None = None
