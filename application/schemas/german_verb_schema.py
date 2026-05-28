from uuid import UUID
from pydantic import BaseModel, Field

from domain.entities.german_verb_model import GermanVerbConjugationModel


class GermanVerbConjugationResponse(BaseModel):
    id: UUID
    tense: str
    person: str
    conjugated_form: str


class GermanVerbResponse(BaseModel):
    id: UUID
    infinitive: str
    definition: str
    is_catalog: bool
    conjugations: list[GermanVerbConjugationResponse] = Field(default_factory=list)


class GermanVerbCreate(BaseModel):
    infinitive: str = Field(..., max_length=100)
    definition: str = Field(..., max_length=500)
