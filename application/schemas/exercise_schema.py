from uuid import UUID
from pydantic import BaseModel, Field


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
