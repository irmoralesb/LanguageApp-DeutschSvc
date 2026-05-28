from uuid import UUID
from pydantic import BaseModel, Field


class GermanNounCreate(BaseModel):
    singular: str = Field(..., max_length=100)
    plural: str | None = Field(default=None, max_length=100)
    article_singular: str = Field(..., pattern="^(der|die|das)$")
    article_plural: str | None = Field(default=None, pattern="^(die)$")
    definition: str = Field(..., max_length=500)


class GermanNounUpdate(BaseModel):
    singular: str | None = Field(default=None, max_length=100)
    plural: str | None = Field(default=None, max_length=100)
    article_singular: str | None = Field(default=None, pattern="^(der|die|das)$")
    article_plural: str | None = None
    definition: str | None = Field(default=None, max_length=500)


class GermanNounResponse(BaseModel):
    id: UUID
    singular: str
    plural: str | None
    article_singular: str
    article_plural: str | None
    definition: str
    is_catalog: bool
