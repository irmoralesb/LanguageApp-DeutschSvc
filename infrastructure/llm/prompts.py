from domain.entities.german_noun_model import GermanNounModel
from domain.entities.german_verb_model import GermanVerbModel

PERSON_LABELS = {
    "1sg": "ich (1st person singular)",
    "2sg": "du (2nd person singular)",
    "3sg": "er/sie/es (3rd person singular)",
    "1pl": "wir (1st person plural)",
    "2pl": "ihr (2nd person plural)",
    "3pl": "sie/Sie (3rd person plural)",
}

TENSE_LABELS = {
    "present": "Präsens (present)",
    "past": "Präteritum (simple past)",
    "future": "Futur I (future)",
}

EXERCISE_GENERATION_SYSTEM = (
    "You are a German language teaching assistant. Create exercises where the learner "
    "writes German nouns with correct articles/plural forms or German verb conjugations. "
    "Respond with valid JSON only."
)

EXERCISE_EVALUATION_SYSTEM = (
    "You are a German language teaching assistant. Evaluate noun answers for article and plural/singular "
    "correctness, and verb answers for tense/person correctness and spelling. Respond with valid JSON only."
)


def _format_noun_expected(noun: GermanNounModel, mode: str) -> str:
    if mode == "plural":
        pl = noun.plural or noun.singular
        art = noun.article_plural or "die"
        return f"{art} {pl}"
    return f"{noun.article_singular} {noun.singular}"


def _format_verb_expected(verb: GermanVerbModel, tense: str, person: str) -> str:
    conj = verb.get_conjugation(tense, person)
    return conj.conjugated_form if conj else verb.infinitive


def build_noun_exercise_prompt(
    noun: GermanNounModel,
    native_language: str,
    exercise_mode: str,
    situation: str | None = None,
) -> str:
    expected = _format_noun_expected(noun, exercise_mode)
    situation_line = (
        f"Optional context: {situation}."
        if situation
        else "Use a clear everyday context."
    )
    mode_desc = "plural form with article" if exercise_mode == "plural" else "singular form with article"
    return f"""\
Create a German noun exercise.

Noun (singular): {noun.singular}
Plural: {noun.plural or 'N/A'}
Singular article: {noun.article_singular}
Plural article: {noun.article_plural or 'die'}
Definition (German): {noun.definition}
Learner native language: {native_language}
Exercise mode: {mode_desc} (expected answer format: "{expected}")
{situation_line}

Return JSON with exactly these keys:
{{
  "scenario_native": "<1-2 sentences in {native_language} describing a situation>",
  "prompt_native": "<One sentence in {native_language} asking the learner to write the German {mode_desc} for this noun>",
  "expected_answer": "{expected}"
}}
"""


def build_noun_evaluation_prompt(
    noun: GermanNounModel,
    exercise_mode: str,
    prompt_native: str,
    expected_answer: str,
    user_answer: str,
) -> str:
    return f"""\
Evaluate the learner's German noun answer.

Noun: {noun.singular} (definition: {noun.definition})
Exercise mode: {exercise_mode}
Prompt: {prompt_native}
Expected answer: {expected_answer}
Student answer: {user_answer}

Check: correct article (der/die/das), correct spelling, correct singular/plural per mode.
Minor capitalization differences are acceptable.

Return JSON:
{{
  "is_correct": <true or false>,
  "feedback": "<Short feedback in German>",
  "correct_example": "<Correct form if wrong; null if correct>"
}}
"""


def build_verb_exercise_prompt(
    verb: GermanVerbModel,
    native_language: str,
    tense: str,
    person: str,
    situation: str | None = None,
) -> str:
    expected = _format_verb_expected(verb, tense, person)
    situation_line = (
        f"Optional context: {situation}."
        if situation
        else "Use a clear everyday context."
    )
    return f"""\
Create a German verb conjugation exercise.

Verb (infinitive): {verb.infinitive}
Definition (German): {verb.definition}
Tense: {TENSE_LABELS.get(tense, tense)}
Person: {PERSON_LABELS.get(person, person)}
Learner native language: {native_language}
Expected conjugated form: "{expected}"
{situation_line}

Return JSON with exactly these keys:
{{
  "scenario_native": "<1-2 sentences in {native_language} describing a situation>",
  "prompt_native": "<One sentence in {native_language} asking the learner to write the German conjugated form>",
  "expected_answer": "{expected}"
}}
"""


def build_verb_evaluation_prompt(
    verb: GermanVerbModel,
    tense: str,
    person: str,
    prompt_native: str,
    expected_answer: str,
    user_answer: str,
) -> str:
    return f"""\
Evaluate the learner's German verb conjugation answer.

Verb: {verb.infinitive} (definition: {verb.definition})
Tense: {TENSE_LABELS.get(tense, tense)}
Person: {PERSON_LABELS.get(person, person)}
Prompt: {prompt_native}
Expected answer: {expected_answer}
Student answer: {user_answer}

Check: correct tense and person, correct spelling. Minor capitalization differences are acceptable.

Return JSON:
{{
  "is_correct": <true or false>,
  "feedback": "<Short feedback in German>",
  "correct_example": "<Correct form if wrong; null if correct>"
}}
"""

