from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class NounExercisePrompt:
    german_noun_id: UUID | None
    target_language_code: str
    exercise_mode: str
    scenario_native: str
    prompt_native: str
    expected_answer: str


@dataclass
class NounGenderExerciseItem:
    german_noun_id: UUID
    singular: str
    definition: str
    incorrect_attempts: int
    correct_attempts: int


@dataclass
class NounCaseExercisePrompt:
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


@dataclass
class VerbExercisePrompt:
    german_verb_id: UUID | None
    target_language_code: str
    tense: str
    person: str
    scenario_native: str
    prompt_native: str
    expected_answer: str


@dataclass
class VerbConjugationExercisePrompt:
    german_verb_id: UUID
    infinitive: str
    definition: str
    tense: str
    person: str
    person_label: str
    prompt_native: str
    options: list[str]
    incorrect_attempts: int
    correct_attempts: int


@dataclass
class NounPluralExercisePrompt:
    german_noun_id: UUID
    singular: str
    definition: str
    article_singular: str
    prompt_native: str
    options: list[str]
    incorrect_attempts: int
    correct_attempts: int


@dataclass
class ExerciseEvaluation:
    is_correct: bool
    feedback: str
    correct_example: str | None = None


@dataclass
class NounExerciseHistoryRecord:
    id: UUID | None
    user_id: UUID
    german_noun_id: UUID
    exercise_type: str
    target_language_code: str
    exercise_mode: str
    scenario_native: str
    prompt_native: str
    expected_answer: str
    user_answer: str
    is_correct: bool
    feedback: str
    created_at: datetime | None = None


@dataclass
class VerbExerciseHistoryRecord:
    id: UUID | None
    user_id: UUID
    german_verb_id: UUID
    exercise_type: str
    target_language_code: str
    tense: str
    person: str
    scenario_native: str
    prompt_native: str
    expected_answer: str
    user_answer: str
    is_correct: bool
    feedback: str
    created_at: datetime | None = None


@dataclass
class GermanNounStats:
    german_noun_id: UUID
    total_attempts: int
    correct_attempts: int


@dataclass
class GermanVerbStats:
    german_verb_id: UUID
    total_attempts: int
    correct_attempts: int

