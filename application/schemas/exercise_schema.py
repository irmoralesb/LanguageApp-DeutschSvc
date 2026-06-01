from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from domain.german_cases import is_valid_case, normalize_case


class NounGenderExerciseGenerateRequest(BaseModel):
    target_score: int = Field(default=10, ge=1, le=50)
    count: int = Field(default=9, ge=3, le=30)


class NounGenderExerciseItemResponse(BaseModel):
    german_noun_id: UUID
    singular: str
    definition: str
    incorrect_attempts: int
    correct_attempts: int


class NounGenderExerciseGenerateResponse(BaseModel):
    target_score: int
    nouns: list[NounGenderExerciseItemResponse]


class NounGenderExerciseEvaluateRequest(BaseModel):
    german_noun_id: UUID
    selected_article: str = Field(pattern="^(der|die|das)$")


class NounGenderExerciseEvaluateResponse(BaseModel):
    is_correct: bool
    correct_article: str
    feedback: str


_CASE_PATTERN = "^(nominativ|akkusativ|dativ|genitiv)$"
_CASE_ARTICLE_PATTERN = "^(der|die|das|den|dem|des)$"


class NounCaseExerciseGenerateRequest(BaseModel):
    cases: list[str] = Field(min_length=1)

    @field_validator("cases")
    @classmethod
    def validate_cases(cls, cases: list[str]) -> list[str]:
        normalized = [normalize_case(c) for c in cases]
        invalid = [c for c in normalized if not is_valid_case(c)]
        if invalid:
            raise ValueError(f"Invalid grammatical cases: {', '.join(invalid)}")
        unique = list(dict.fromkeys(normalized))
        if not unique:
            raise ValueError("At least one grammatical case is required.")
        return unique


class NounCaseExerciseGenerateResponse(BaseModel):
    german_noun_id: UUID
    singular: str
    definition: str
    grammatical_case: str
    case_label: str
    sentence_with_blank: str
    scenario_native: str
    article_options: list[str]
    incorrect_attempts: int
    correct_attempts: int


class NounCaseExerciseEvaluateRequest(BaseModel):
    german_noun_id: UUID
    grammatical_case: str = Field(pattern=_CASE_PATTERN)
    selected_article: str = Field(pattern=_CASE_ARTICLE_PATTERN)
    sentence_with_blank: str = Field(min_length=1)


class NounCaseExerciseEvaluateResponse(BaseModel):
    is_correct: bool
    correct_article: str
    feedback: str
    correct_phrase: str


class NounExerciseGenerateRequest(BaseModel):
    german_noun_id: UUID | None = None
    exercise_mode: str = Field(default="singular", pattern="^(singular|plural)$")
    situation: str | None = None


class NounExerciseGenerateResponse(BaseModel):
    german_noun_id: UUID
    target_language_code: str
    exercise_mode: str
    scenario_native: str
    prompt_native: str
    expected_answer: str


class NounExerciseEvaluateRequest(BaseModel):
    german_noun_id: UUID
    exercise_mode: str = Field(default="singular", pattern="^(singular|plural)$")
    scenario_native: str
    prompt_native: str
    expected_answer: str
    user_answer: str


class NounExerciseEvaluateResponse(BaseModel):
    is_correct: bool
    feedback: str
    correct_example: str | None = None


class VerbExerciseGenerateRequest(BaseModel):
    german_verb_id: UUID | None = None
    tense: str = Field(default="present", pattern="^(present|past|future)$")
    person: str = Field(default="3sg", pattern="^(1sg|2sg|3sg|1pl|2pl|3pl)$")
    situation: str | None = None


class VerbExerciseGenerateResponse(BaseModel):
    german_verb_id: UUID
    target_language_code: str
    tense: str
    person: str
    scenario_native: str
    prompt_native: str
    expected_answer: str


class VerbExerciseEvaluateRequest(BaseModel):
    german_verb_id: UUID
    tense: str
    person: str
    scenario_native: str
    prompt_native: str
    expected_answer: str
    user_answer: str


class VerbExerciseEvaluateResponse(BaseModel):
    is_correct: bool
    feedback: str
    correct_example: str | None = None
