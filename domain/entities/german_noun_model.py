from dataclasses import dataclass
from uuid import UUID


@dataclass
class GermanNounModel:
    id: UUID | None
    singular: str
    plural: str | None
    article_singular: str
    article_plural: str | None
    definition: str
    is_catalog: bool = True
    created_by_user_id: UUID | None = None
