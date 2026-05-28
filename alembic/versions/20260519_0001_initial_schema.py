"""Initial schema: german nouns+verbs, profiles, exercises + seed

Revision ID: 0001_deutsch
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER, DATETIME2
import uuid
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from seed_data.german_nouns_catalog import GERMAN_NOUNS_CATALOG
from seed_data.german_verbs_catalog import GERMAN_VERBS, all_conjugation_rows

revision = "0001_deutsch"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "languages",
        sa.Column("id", UNIQUEIDENTIFIER(as_uuid=True), primary_key=True),
        sa.Column("code", sa.String(10), nullable=False, unique=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("is_target_language", sa.Boolean, nullable=False, server_default=sa.text("0")),
        sa.Column("is_native_language", sa.Boolean, nullable=False, server_default=sa.text("0")),
    )

    op.create_table(
        "german_nouns",
        sa.Column("id", UNIQUEIDENTIFIER(as_uuid=True), primary_key=True),
        sa.Column("singular", sa.String(100), nullable=False),
        sa.Column("plural", sa.String(100), nullable=True),
        sa.Column("article_singular", sa.String(10), nullable=False),
        sa.Column("article_plural", sa.String(10), nullable=True),
        sa.Column("definition", sa.String(500), nullable=False),
        sa.Column("is_catalog", sa.Boolean, nullable=False, server_default=sa.text("1")),
        sa.Column("created_by_user_id", UNIQUEIDENTIFIER(as_uuid=True), nullable=True),
        sa.Column("created_at", DATETIME2(precision=6), server_default=sa.text("SYSUTCDATETIME()"), nullable=False),
        sa.UniqueConstraint("singular", "created_by_user_id", name="uq_german_noun_user"),
    )

    op.create_table(
        "german_verbs",
        sa.Column("id", UNIQUEIDENTIFIER(as_uuid=True), primary_key=True),
        sa.Column("infinitive", sa.String(100), nullable=False),
        sa.Column("definition", sa.String(500), nullable=False),
        sa.Column("is_catalog", sa.Boolean, nullable=False, server_default=sa.text("1")),
        sa.Column("created_by_user_id", UNIQUEIDENTIFIER(as_uuid=True), nullable=True),
        sa.Column("created_at", DATETIME2(precision=6), server_default=sa.text("SYSUTCDATETIME()"), nullable=False),
        sa.UniqueConstraint("infinitive", "created_by_user_id", name="uq_german_verb_user"),
    )

    op.create_table(
        "german_verb_conjugations",
        sa.Column("id", UNIQUEIDENTIFIER(as_uuid=True), primary_key=True),
        sa.Column("verb_id", UNIQUEIDENTIFIER(as_uuid=True), sa.ForeignKey("german_verbs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("tense", sa.String(20), nullable=False),
        sa.Column("person", sa.String(10), nullable=False),
        sa.Column("conjugated_form", sa.String(100), nullable=False),
        sa.UniqueConstraint("verb_id", "tense", "person", name="uq_verb_tense_person"),
    )

    op.create_table(
        "user_profiles",
        sa.Column("id", UNIQUEIDENTIFIER(as_uuid=True), primary_key=True),
        sa.Column("user_id", UNIQUEIDENTIFIER(as_uuid=True), nullable=False, unique=True),
        sa.Column("native_language_id", UNIQUEIDENTIFIER(as_uuid=True), sa.ForeignKey("languages.id"), nullable=False),
        sa.Column("created_at", DATETIME2(precision=6), server_default=sa.text("SYSUTCDATETIME()"), nullable=False),
        sa.Column("updated_at", DATETIME2(precision=6), server_default=sa.text("SYSUTCDATETIME()"), nullable=False),
    )

    op.create_table(
        "user_learning_languages",
        sa.Column("id", UNIQUEIDENTIFIER(as_uuid=True), primary_key=True),
        sa.Column("user_id", UNIQUEIDENTIFIER(as_uuid=True), sa.ForeignKey("user_profiles.user_id"), nullable=False),
        sa.Column("language_id", UNIQUEIDENTIFIER(as_uuid=True), sa.ForeignKey("languages.id"), nullable=False),
        sa.UniqueConstraint("user_id", "language_id", name="uq_user_learning_language"),
    )

    op.create_table(
        "user_german_noun_selections",
        sa.Column("id", UNIQUEIDENTIFIER(as_uuid=True), primary_key=True),
        sa.Column("user_id", UNIQUEIDENTIFIER(as_uuid=True), sa.ForeignKey("user_profiles.user_id"), nullable=False),
        sa.Column("german_noun_id", UNIQUEIDENTIFIER(as_uuid=True), sa.ForeignKey("german_nouns.id"), nullable=False),
        sa.Column("added_at", DATETIME2(precision=6), server_default=sa.text("SYSUTCDATETIME()"), nullable=False),
        sa.UniqueConstraint("user_id", "german_noun_id", name="uq_user_german_noun"),
    )

    op.create_table(
        "user_german_verb_selections",
        sa.Column("id", UNIQUEIDENTIFIER(as_uuid=True), primary_key=True),
        sa.Column("user_id", UNIQUEIDENTIFIER(as_uuid=True), sa.ForeignKey("user_profiles.user_id"), nullable=False),
        sa.Column("german_verb_id", UNIQUEIDENTIFIER(as_uuid=True), sa.ForeignKey("german_verbs.id"), nullable=False),
        sa.Column("added_at", DATETIME2(precision=6), server_default=sa.text("SYSUTCDATETIME()"), nullable=False),
        sa.UniqueConstraint("user_id", "german_verb_id", name="uq_user_german_verb"),
    )

    op.create_table(
        "noun_exercise_results",
        sa.Column("id", UNIQUEIDENTIFIER(as_uuid=True), primary_key=True),
        sa.Column("user_id", UNIQUEIDENTIFIER(as_uuid=True), nullable=False, index=True),
        sa.Column("german_noun_id", UNIQUEIDENTIFIER(as_uuid=True), sa.ForeignKey("german_nouns.id"), nullable=False),
        sa.Column("exercise_type", sa.String(50), nullable=False),
        sa.Column("target_language_code", sa.String(10), nullable=False),
        sa.Column("exercise_mode", sa.String(30), nullable=False, server_default="singular"),
        sa.Column("scenario_native", sa.Text, nullable=False),
        sa.Column("prompt_native", sa.Text, nullable=False),
        sa.Column("expected_answer", sa.Text, nullable=False),
        sa.Column("user_answer", sa.Text, nullable=False),
        sa.Column("is_correct", sa.Boolean, nullable=False),
        sa.Column("feedback", sa.Text, nullable=False),
        sa.Column("created_at", DATETIME2(precision=6), server_default=sa.text("SYSUTCDATETIME()"), nullable=False),
    )

    op.create_table(
        "verb_exercise_results",
        sa.Column("id", UNIQUEIDENTIFIER(as_uuid=True), primary_key=True),
        sa.Column("user_id", UNIQUEIDENTIFIER(as_uuid=True), nullable=False, index=True),
        sa.Column("german_verb_id", UNIQUEIDENTIFIER(as_uuid=True), sa.ForeignKey("german_verbs.id"), nullable=False),
        sa.Column("exercise_type", sa.String(50), nullable=False),
        sa.Column("target_language_code", sa.String(10), nullable=False),
        sa.Column("tense", sa.String(20), nullable=False),
        sa.Column("person", sa.String(10), nullable=False),
        sa.Column("scenario_native", sa.Text, nullable=False),
        sa.Column("prompt_native", sa.Text, nullable=False),
        sa.Column("expected_answer", sa.Text, nullable=False),
        sa.Column("user_answer", sa.Text, nullable=False),
        sa.Column("is_correct", sa.Boolean, nullable=False),
        sa.Column("feedback", sa.Text, nullable=False),
        sa.Column("created_at", DATETIME2(precision=6), server_default=sa.text("SYSUTCDATETIME()"), nullable=False),
    )

    _seed_languages()
    _seed_german_nouns()
    _seed_german_verbs()


def downgrade() -> None:
    op.drop_table("verb_exercise_results")
    op.drop_table("noun_exercise_results")
    op.drop_table("user_german_verb_selections")
    op.drop_table("user_german_noun_selections")
    op.drop_table("user_learning_languages")
    op.drop_table("user_profiles")
    op.drop_table("german_verb_conjugations")
    op.drop_table("german_verbs")
    op.drop_table("german_nouns")
    op.drop_table("languages")


def _seed_languages() -> None:
    languages_table = sa.table(
        "languages",
        sa.column("id", UNIQUEIDENTIFIER),
        sa.column("code", sa.String),
        sa.column("name", sa.String),
        sa.column("is_target_language", sa.Boolean),
        sa.column("is_native_language", sa.Boolean),
    )
    rows = [
        {"id": uuid.UUID("a0000003-0000-0000-0000-000000000001"), "code": "en", "name": "English",
         "is_target_language": False, "is_native_language": True},
        {"id": uuid.UUID("a0000003-0000-0000-0000-000000000002"), "code": "de", "name": "German",
         "is_target_language": True, "is_native_language": True},
        {"id": uuid.UUID("a0000003-0000-0000-0000-000000000003"), "code": "es", "name": "Spanish",
         "is_target_language": False, "is_native_language": True},
    ]
    op.bulk_insert(languages_table, rows)


def _seed_german_nouns() -> None:
    t = sa.table(
        "german_nouns",
        sa.column("id", UNIQUEIDENTIFIER),
        sa.column("singular", sa.String),
        sa.column("plural", sa.String),
        sa.column("article_singular", sa.String),
        sa.column("article_plural", sa.String),
        sa.column("definition", sa.String),
        sa.column("is_catalog", sa.Boolean),
        sa.column("created_by_user_id", UNIQUEIDENTIFIER),
    )
    rows = []
    for i, (sg, pl, art_sg, art_pl, defn) in enumerate(GERMAN_NOUNS_CATALOG, start=1):
        plural_val = None if pl == "—" else pl
        art_pl_val = None if art_pl == "—" else art_pl
        rows.append({
            "id": uuid.UUID(f"d0000001-0000-0000-0000-{i:012d}"),
            "singular": sg,
            "plural": plural_val,
            "article_singular": art_sg,
            "article_plural": art_pl_val,
            "definition": defn,
            "is_catalog": True,
            "created_by_user_id": None,
        })
    op.bulk_insert(t, rows)


def _seed_german_verbs() -> None:
    verbs_table = sa.table(
        "german_verbs",
        sa.column("id", UNIQUEIDENTIFIER),
        sa.column("infinitive", sa.String),
        sa.column("definition", sa.String),
        sa.column("is_catalog", sa.Boolean),
        sa.column("created_by_user_id", UNIQUEIDENTIFIER),
    )
    conj_table = sa.table(
        "german_verb_conjugations",
        sa.column("id", UNIQUEIDENTIFIER),
        sa.column("verb_id", UNIQUEIDENTIFIER),
        sa.column("tense", sa.String),
        sa.column("person", sa.String),
        sa.column("conjugated_form", sa.String),
    )
    verb_rows = []
    conj_rows = []
    for i, (inf, defn) in enumerate(GERMAN_VERBS[:100], start=1):
        vid = uuid.UUID(f"e0000001-0000-0000-0000-{i:012d}")
        verb_rows.append({
            "id": vid,
            "infinitive": inf,
            "definition": defn,
            "is_catalog": True,
            "created_by_user_id": None,
        })
        for j, (tense, person, form) in enumerate(all_conjugation_rows(inf), start=1):
            conj_rows.append({
                "id": uuid.UUID(f"e0000002-0000-0000-{i:04d}-{j:012d}"),
                "verb_id": vid,
                "tense": tense,
                "person": person,
                "conjugated_form": form,
            })
    op.bulk_insert(verbs_table, verb_rows)
    op.bulk_insert(conj_table, conj_rows)
