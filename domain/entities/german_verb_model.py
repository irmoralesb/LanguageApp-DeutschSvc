from dataclasses import dataclass, field
from uuid import UUID

TENSES = ("present", "past", "future")
PERSONS = ("1sg", "2sg", "3sg", "1pl", "2pl", "3pl")


@dataclass
class GermanVerbConjugationModel:
    id: UUID | None
    verb_id: UUID | None
    tense: str
    person: str
    conjugated_form: str


@dataclass
class GermanVerbModel:
    id: UUID | None
    infinitive: str
    definition: str
    conjugations: list[GermanVerbConjugationModel] = field(default_factory=list)
    is_catalog: bool = True
    created_by_user_id: UUID | None = None

    def get_conjugation(self, tense: str, person: str) -> GermanVerbConjugationModel | None:
        for conjugation in self.conjugations:
            if conjugation.tense == tense and conjugation.person == person:
                return conjugation
        return None
