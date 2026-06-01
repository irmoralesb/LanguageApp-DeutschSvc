"""German grammatical cases: declension tables and A1/A2 sentence templates."""

import random as rand_mod
from typing import Literal

GermanGrammaticalCase = Literal["nominativ", "akkusativ", "dativ", "genitiv"]

GERMAN_CASES: tuple[GermanGrammaticalCase, ...] = (
    "nominativ",
    "akkusativ",
    "dativ",
    "genitiv",
)

CASE_LABELS_DE: dict[str, str] = {
    "nominativ": "Nominativ",
    "akkusativ": "Akkusativ",
    "dativ": "Dativ",
    "genitiv": "Genitiv",
}

NOMINATIVE_ARTICLES = ("der", "die", "das")

DECLENSION_BY_NOMINATIVE: dict[str, dict[str, str]] = {
    "der": {
        "nominativ": "der",
        "akkusativ": "den",
        "dativ": "dem",
        "genitiv": "des",
    },
    "die": {
        "nominativ": "die",
        "akkusativ": "die",
        "dativ": "der",
        "genitiv": "der",
    },
    "das": {
        "nominativ": "das",
        "akkusativ": "das",
        "dativ": "dem",
        "genitiv": "des",
    },
}

# Simple A1/A2 sentences; ___ marks the article blank.
CASE_SENTENCE_TEMPLATES: dict[str, list[str]] = {
    "nominativ": [
        "___ {noun} ist hier.",
        "___ {noun} ist neu.",
    ],
    "akkusativ": [
        "Ich sehe ___ {noun}.",
        "Ich habe ___ {noun}.",
        "Ich kaufe ___ {noun}.",
    ],
    "dativ": [
        "Ich gebe ___ {noun} ein Buch.",
        "Ich helfe ___ {noun}.",
        "Das Buch gehört ___ {noun}.",
    ],
    "genitiv": [
        "Die Farbe ___ {noun} ist blau.",
        "Das ist die Tasche ___ {noun}.",
    ],
}

CASE_HINTS_EN: dict[str, str] = {
    "nominativ": "Pick the subject article (Nominativ).",
    "akkusativ": "Pick the direct-object article (Akkusativ).",
    "dativ": "Pick the indirect-object article (Dativ).",
    "genitiv": "Pick the possessive article (Genitiv).",
}


def normalize_case(value: str) -> str:
    return value.strip().lower()


def is_valid_case(value: str) -> bool:
    return normalize_case(value) in GERMAN_CASES


def article_for_case(nominative_article: str, grammatical_case: str) -> str:
    nom_art = nominative_article.lower().strip()
    case = normalize_case(grammatical_case)
    if nom_art not in DECLENSION_BY_NOMINATIVE:
        raise ValueError(f"Unsupported nominative article: {nominative_article}")
    if case not in DECLENSION_BY_NOMINATIVE[nom_art]:
        raise ValueError(f"Unsupported grammatical case: {grammatical_case}")
    return DECLENSION_BY_NOMINATIVE[nom_art][case]


def article_options_for_noun(nominative_article: str, practice_cases: list[str]) -> list[str]:
    """Articles that commonly confuse learners for this noun gender."""
    nom_art = nominative_article.lower().strip()
    decl = DECLENSION_BY_NOMINATIVE.get(nom_art)
    if decl is None:
        return list(NOMINATIVE_ARTICLES)

    options: set[str] = set()
    for case in practice_cases:
        normalized = normalize_case(case)
        if normalized in decl:
            options.add(decl[normalized])
    for case in GERMAN_CASES:
        if case in decl:
            options.add(decl[case])

    ordered = ["der", "die", "das", "den", "dem", "des"]
    return [art for art in ordered if art in options]


def build_case_sentence(
    grammatical_case: str,
    singular: str,
    *,
    rng: rand_mod.Random | None = None,
) -> str:
    case = normalize_case(grammatical_case)
    templates = CASE_SENTENCE_TEMPLATES.get(case)
    if not templates:
        raise ValueError(f"No templates for case: {grammatical_case}")
    picker = rng or rand_mod
    template = picker.choice(templates)
    return template.format(noun=singular)


def case_hint_native(grammatical_case: str, native_language: str) -> str:
    case = normalize_case(grammatical_case)
    if native_language.lower().startswith("en"):
        return CASE_HINTS_EN.get(case, f"Choose the correct article ({CASE_LABELS_DE.get(case, case)}).")
    label = CASE_LABELS_DE.get(case, case)
    return f"Wähle den richtigen Artikel ({label})."
