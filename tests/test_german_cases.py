"""Tests for German case declension helpers."""

import pytest

from domain.german_cases import (
    article_for_case,
    article_options_for_noun,
    build_case_sentence,
    is_valid_case,
    normalize_case,
)


def test_normalize_case() -> None:
    assert normalize_case("Akkusativ") == "akkusativ"


def test_article_for_case_masculine() -> None:
    assert article_for_case("der", "akkusativ") == "den"
    assert article_for_case("der", "dativ") == "dem"


def test_article_for_case_feminine() -> None:
    assert article_for_case("die", "dativ") == "der"


def test_article_for_case_neuter() -> None:
    assert article_for_case("das", "akkusativ") == "das"


def test_build_case_sentence_replaces_noun() -> None:
    sentence = build_case_sentence("akkusativ", "Mann")
    assert "Mann" in sentence
    assert "___" in sentence


def test_article_options_includes_practice_cases() -> None:
    options = article_options_for_noun("der", ["nominativ", "akkusativ"])
    assert "der" in options
    assert "den" in options


def test_is_valid_case() -> None:
    assert is_valid_case("dativ")
    assert not is_valid_case("instrumental")


def test_article_for_case_rejects_unknown_article() -> None:
    with pytest.raises(ValueError):
        article_for_case("ein", "akkusativ")
