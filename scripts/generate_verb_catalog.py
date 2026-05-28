"""One-off script to generate alembic/seed_data/german_verbs_catalog.py."""
from pathlib import Path

TENSES = ("present", "past", "future")
PERSONS = ("1sg", "2sg", "3sg", "1pl", "2pl", "3pl")
FUTURE_AUX = {
    "1sg": "werde", "2sg": "wirst", "3sg": "wird",
    "1pl": "werden", "2pl": "werdet", "3pl": "werden",
}


def future_forms(infinitive: str) -> dict[str, str]:
    return {p: f"{FUTURE_AUX[p]} {infinitive}" for p in PERSONS}


def regular_present(infinitive: str) -> dict[str, str]:
    stem = infinitive[:-2] if infinitive.endswith(("eln", "ern", "en")) else infinitive
    endings = {"1sg": "e", "2sg": "st", "3sg": "t", "1pl": "en", "2pl": "t", "3pl": "en"}
    return {p: stem + endings[p] for p in PERSONS}


def regular_past(infinitive: str) -> dict[str, str]:
    stem = infinitive[:-2] if infinitive.endswith(("eln", "en")) else infinitive
    endings = {"1sg": "te", "2sg": "test", "3sg": "te", "1pl": "ten", "2pl": "tet", "3pl": "ten"}
    return {p: stem + endings[p] for p in PERSONS}


def full_regular(infinitive: str) -> dict[str, dict[str, str]]:
    return {
        "present": regular_present(infinitive),
        "past": regular_past(infinitive),
        "future": future_forms(infinitive),
    }


IRREGULAR: dict[str, tuple[str, dict[str, dict[str, str]]]] = {
    "sein": (
        "existieren; sich befinden",
        {
            "present": {"1sg": "bin", "2sg": "bist", "3sg": "ist", "1pl": "sind", "2pl": "seid", "3pl": "sind"},
            "past": {"1sg": "war", "2sg": "warst", "3sg": "war", "1pl": "waren", "2pl": "wart", "3pl": "waren"},
            "future": future_forms("sein"),
        },
    ),
    "haben": (
        "besitzen",
        {
            "present": {"1sg": "habe", "2sg": "hast", "3sg": "hat", "1pl": "haben", "2pl": "habt", "3pl": "haben"},
            "past": {"1sg": "hatte", "2sg": "hattest", "3sg": "hatte", "1pl": "hatten", "2pl": "hattet", "3pl": "hatten"},
            "future": future_forms("haben"),
        },
    ),
    "werden": (
        "zu etwas werden",
        {
            "present": {"1sg": "werde", "2sg": "wirst", "3sg": "wird", "1pl": "werden", "2pl": "werdet", "3pl": "werden"},
            "past": {"1sg": "wurde", "2sg": "wurdest", "3sg": "wurde", "1pl": "wurden", "2pl": "wurdet", "3pl": "wurden"},
            "future": future_forms("werden"),
        },
    ),
    "können": (
        "in der Lage sein",
        {
            "present": {"1sg": "kann", "2sg": "kannst", "3sg": "kann", "1pl": "können", "2pl": "könnt", "3pl": "können"},
            "past": {"1sg": "konnte", "2sg": "konntest", "3sg": "konnte", "1pl": "konnten", "2pl": "konntet", "3pl": "konnten"},
            "future": future_forms("können"),
        },
    ),
    "müssen": (
        "verpflichtet sein",
        {
            "present": {"1sg": "muss", "2sg": "musst", "3sg": "muss", "1pl": "müssen", "2pl": "müsst", "3pl": "müssen"},
            "past": {"1sg": "musste", "2sg": "musstest", "3sg": "musste", "1pl": "mussten", "2pl": "musstet", "3pl": "mussten"},
            "future": future_forms("müssen"),
        },
    ),
    "sollen": (
        "empfohlen werden",
        {
            "present": {"1sg": "soll", "2sg": "sollst", "3sg": "soll", "1pl": "sollen", "2pl": "sollt", "3pl": "sollen"},
            "past": {"1sg": "sollte", "2sg": "solltest", "3sg": "sollte", "1pl": "sollten", "2pl": "solltet", "3pl": "sollten"},
            "future": future_forms("sollen"),
        },
    ),
    "wollen": (
        "wünschen",
        {
            "present": {"1sg": "will", "2sg": "willst", "3sg": "will", "1pl": "wollen", "2pl": "wollt", "3pl": "wollen"},
            "past": {"1sg": "wollte", "2sg": "wolltest", "3sg": "wollte", "1pl": "wollten", "2pl": "wolltet", "3pl": "wollten"},
            "future": future_forms("wollen"),
        },
    ),
    "dürfen": (
        "erlaubt sein",
        {
            "present": {"1sg": "darf", "2sg": "darfst", "3sg": "darf", "1pl": "dürfen", "2pl": "dürft", "3pl": "dürfen"},
            "past": {"1sg": "durfte", "2sg": "durftest", "3sg": "durfte", "1pl": "durften", "2pl": "durftet", "3pl": "durften"},
            "future": future_forms("dürfen"),
        },
    ),
    "mögen": (
        "gern haben",
        {
            "present": {"1sg": "mag", "2sg": "magst", "3sg": "mag", "1pl": "mögen", "2pl": "mögt", "3pl": "mögen"},
            "past": {"1sg": "mochte", "2sg": "mochtest", "3sg": "mochte", "1pl": "mochten", "2pl": "mochtet", "3pl": "mochten"},
            "future": future_forms("mögen"),
        },
    ),
    "gehen": (
        "sich zu Fuß bewegen",
        {
            "present": {"1sg": "gehe", "2sg": "gehst", "3sg": "geht", "1pl": "gehen", "2pl": "geht", "3pl": "gehen"},
            "past": {"1sg": "ging", "2sg": "gingst", "3sg": "ging", "1pl": "gingen", "2pl": "gingt", "3pl": "gingen"},
            "future": future_forms("gehen"),
        },
    ),
    "kommen": (
        "sich nähern; ankommen",
        {
            "present": {"1sg": "komme", "2sg": "kommst", "3sg": "kommt", "1pl": "kommen", "2pl": "kommt", "3pl": "kommen"},
            "past": {"1sg": "kam", "2sg": "kamst", "3sg": "kam", "1pl": "kamen", "2pl": "kamt", "3pl": "kamen"},
            "future": future_forms("kommen"),
        },
    ),
    "sehen": (
        "mit den Augen wahrnehmen",
        {
            "present": {"1sg": "sehe", "2sg": "siehst", "3sg": "sieht", "1pl": "sehen", "2pl": "seht", "3pl": "sehen"},
            "past": {"1sg": "sah", "2sg": "sahst", "3sg": "sah", "1pl": "sahen", "2pl": "saht", "3pl": "sahen"},
            "future": future_forms("sehen"),
        },
    ),
    "geben": (
        "übergeben",
        {
            "present": {"1sg": "gebe", "2sg": "gibst", "3sg": "gibt", "1pl": "geben", "2pl": "gebt", "3pl": "geben"},
            "past": {"1sg": "gab", "2sg": "gabst", "3sg": "gab", "1pl": "gaben", "2pl": "gabt", "3pl": "gaben"},
            "future": future_forms("geben"),
        },
    ),
    "nehmen": (
        "ergreifen; konsumieren",
        {
            "present": {"1sg": "nehme", "2sg": "nimmst", "3sg": "nimmt", "1pl": "nehmen", "2pl": "nehmt", "3pl": "nehmen"},
            "past": {"1sg": "nahm", "2sg": "nahmst", "3sg": "nahm", "1pl": "nahmen", "2pl": "nahmt", "3pl": "nahmen"},
            "future": future_forms("nehmen"),
        },
    ),
    "sprechen": (
        "reden",
        {
            "present": {"1sg": "spreche", "2sg": "sprichst", "3sg": "spricht", "1pl": "sprechen", "2pl": "sprecht", "3pl": "sprechen"},
            "past": {"1sg": "sprach", "2sg": "sprachst", "3sg": "sprach", "1pl": "sprachen", "2pl": "spracht", "3pl": "sprachen"},
            "future": future_forms("sprechen"),
        },
    ),
    "essen": (
        "Nahrung zu sich nehmen",
        {
            "present": {"1sg": "esse", "2sg": "isst", "3sg": "isst", "1pl": "essen", "2pl": "esst", "3pl": "essen"},
            "past": {"1sg": "aß", "2sg": "aßest", "3sg": "aß", "1pl": "aßen", "2pl": "aßt", "3pl": "aßen"},
            "future": future_forms("essen"),
        },
    ),
    "fahren": (
        "sich mit einem Fahrzeug bewegen",
        {
            "present": {"1sg": "fahre", "2sg": "fährst", "3sg": "fährt", "1pl": "fahren", "2pl": "fahrt", "3pl": "fahren"},
            "past": {"1sg": "fuhr", "2sg": "fuhrst", "3sg": "fuhr", "1pl": "fuhren", "2pl": "fuhrt", "3pl": "fuhren"},
            "future": future_forms("fahren"),
        },
    ),
    "schlafen": (
        "ruhen mit geschlossenen Augen",
        {
            "present": {"1sg": "schlafe", "2sg": "schläfst", "3sg": "schläft", "1pl": "schlafen", "2pl": "schlaft", "3pl": "schlafen"},
            "past": {"1sg": "schlief", "2sg": "schliefst", "3sg": "schlief", "1pl": "schliefen", "2pl": "schlieft", "3pl": "schliefen"},
            "future": future_forms("schlafen"),
        },
    ),
    "lesen": (
        "geschriebene Worte verstehen",
        {
            "present": {"1sg": "lese", "2sg": "liest", "3sg": "liest", "1pl": "lesen", "2pl": "lest", "3pl": "lesen"},
            "past": {"1sg": "las", "2sg": "last", "3sg": "las", "1pl": "lasen", "2pl": "last", "3pl": "lasen"},
            "future": future_forms("lesen"),
        },
    ),
    "schreiben": (
        "mit Schriftzeichen festhalten",
        {
            "present": {"1sg": "schreibe", "2sg": "schreibst", "3sg": "schreibt", "1pl": "schreiben", "2pl": "schreibt", "3pl": "schreiben"},
            "past": {"1sg": "schrieb", "2sg": "schriebst", "3sg": "schrieb", "1pl": "schrieben", "2pl": "schriebt", "3pl": "schrieben"},
            "future": future_forms("schreiben"),
        },
    ),
    "helfen": (
        "unterstützen",
        {
            "present": {"1sg": "helfe", "2sg": "hilfst", "3sg": "hilft", "1pl": "helfen", "2pl": "helft", "3pl": "helfen"},
            "past": {"1sg": "half", "2sg": "halfst", "3sg": "half", "1pl": "halfen", "2pl": "halft", "3pl": "halfen"},
            "future": future_forms("helfen"),
        },
    ),
    "wissen": (
        "Kenntnis haben",
        {
            "present": {"1sg": "weiß", "2sg": "weißt", "3sg": "weiß", "1pl": "wissen", "2pl": "wisst", "3pl": "wissen"},
            "past": {"1sg": "wusste", "2sg": "wusstest", "3sg": "wusste", "1pl": "wussten", "2pl": "wusstet", "3pl": "wussten"},
            "future": future_forms("wissen"),
        },
    ),
    "finden": (
        "entdecken",
        {
            "present": {"1sg": "finde", "2sg": "findest", "3sg": "findet", "1pl": "finden", "2pl": "findet", "3pl": "finden"},
            "past": {"1sg": "fand", "2sg": "fandst", "3sg": "fand", "1pl": "fanden", "2pl": "fandt", "3pl": "fanden"},
            "future": future_forms("finden"),
        },
    ),
    "bleiben": (
        "an einem Ort verweilen",
        {
            "present": {"1sg": "bleibe", "2sg": "bleibst", "3sg": "bleibt", "1pl": "bleiben", "2pl": "bleibt", "3pl": "bleiben"},
            "past": {"1sg": "blieb", "2sg": "bliebst", "3sg": "blieb", "1pl": "blieben", "2pl": "bliebt", "3pl": "blieben"},
            "future": future_forms("bleiben"),
        },
    ),
    "stehen": (
        "aufrecht sein",
        {
            "present": {"1sg": "stehe", "2sg": "stehst", "3sg": "steht", "1pl": "stehen", "2pl": "steht", "3pl": "stehen"},
            "past": {"1sg": "stand", "2sg": "standst", "3sg": "stand", "1pl": "standen", "2pl": "standt", "3pl": "standen"},
            "future": future_forms("stehen"),
        },
    ),
    "liegen": (
        "horizontal ruhen",
        {
            "present": {"1sg": "liege", "2sg": "liegst", "3sg": "liegt", "1pl": "liegen", "2pl": "liegt", "3pl": "liegen"},
            "past": {"1sg": "lag", "2sg": "lagst", "3sg": "lag", "1pl": "lagen", "2pl": "lagt", "3pl": "lagen"},
            "future": future_forms("liegen"),
        },
    ),
    "heißen": (
        "einen Namen tragen",
        {
            "present": {"1sg": "heiße", "2sg": "heißt", "3sg": "heißt", "1pl": "heißen", "2pl": "heißt", "3pl": "heißen"},
            "past": {"1sg": "hieß", "2sg": "hießest", "3sg": "hieß", "1pl": "hießen", "2pl": "hießt", "3pl": "hießen"},
            "future": future_forms("heißen"),
        },
    ),
    "denken": (
        "nachdenken",
        {
            "present": {"1sg": "denke", "2sg": "denkst", "3sg": "denkt", "1pl": "denken", "2pl": "denkt", "3pl": "denken"},
            "past": {"1sg": "dachte", "2sg": "dachtest", "3sg": "dachte", "1pl": "dachten", "2pl": "dachtet", "3pl": "dachten"},
            "future": future_forms("denken"),
        },
    ),
    "tun": (
        "handeln; ausführen",
        {
            "present": {"1sg": "tue", "2sg": "tust", "3sg": "tut", "1pl": "tun", "2pl": "tut", "3pl": "tun"},
            "past": {"1sg": "tat", "2sg": "tatst", "3sg": "tat", "1pl": "taten", "2pl": "tatet", "3pl": "taten"},
            "future": future_forms("tun"),
        },
    ),
    "lassen": (
        "erlauben; zulassen",
        {
            "present": {"1sg": "lasse", "2sg": "lässt", "3sg": "lässt", "1pl": "lassen", "2pl": "lasst", "3pl": "lassen"},
            "past": {"1sg": "ließ", "2sg": "ließest", "3sg": "ließ", "1pl": "ließen", "2pl": "ließt", "3pl": "ließen"},
            "future": future_forms("lassen"),
        },
    ),
}

REGULAR_DEFS = [
    ("sagen", "etwas mitteilen"),
    ("machen", "etwas herstellen oder tun"),
    ("zeigen", "sichtbar machen"),
    ("führen", "leiten"),
    ("bringen", "etwas transportieren"),
    ("leben", "existieren"),
    ("meinen", "der Ansicht sein"),
    ("fragen", "eine Frage stellen"),
    ("kennen", "wissen über jemanden"),
    ("gelten", "als wahr angesehen werden"),
    ("arbeiten", "beruflich tätig sein"),
    ("brauchen", "benötigen"),
    ("folgen", "hinter jemandem gehen"),
    ("lernen", "Wissen erwerben"),
    ("spielen", "ein Spiel ausüben"),
    ("tragen", "etwas auf dem Körper halten"),
    ("gewinnen", "siegreich sein"),
    ("beginnen", "anfangen"),
    ("erklären", "verständlich machen"),
    ("setzen", "an einen Ort stellen"),
    ("erreichen", "ein Ziel erlangen"),
    ("schaffen", "etwas zustande bringen"),
    ("erhalten", "bekommen"),
    ("versuchen", "es probieren"),
    ("bedeuten", "symbolisieren"),
    ("verstehen", "begreifen"),
    ("treffen", "zusammenkommen mit"),
    ("warten", "Zeit vergehen lassen"),
    ("legen", "horizontal platzieren"),
    ("verkaufen", "gegen Geld abgeben"),
    ("passieren", "geschehen"),
    ("bekommen", "erhalten"),
    ("entstehen", "zustande kommen"),
    ("sitzen", "auf etwas ruhen"),
    ("ziehen", "bewegen"),
    ("bestehen", "existieren"),
    ("hoffen", "eine Hoffnung haben"),
    ("bezahlen", "Geld geben"),
    ("holen", "besorgen"),
    ("reisen", "eine Reise machen"),
    ("tanzen", "Rhythmus bewegen"),
    ("kochen", "Essen zubereiten"),
    ("kaufen", "erwerben gegen Geld"),
    ("öffnen", "zugänglich machen"),
    ("schließen", "nicht mehr offen sein"),
    ("antworten", "auf eine Frage reagieren"),
    ("wünschen", "sich etwas erhoffen"),
    ("hören", "Geräusche wahrnehmen"),
    ("schauen", "mit den Augen betrachten"),
    ("suchen", "etwas finden wollen"),
    ("laufen", "schnell gehen"),
    ("fliegen", "durch die Luft bewegen"),
    ("schwimmen", "im Wasser bewegen"),
    ("singen", "Musik mit der Stimme machen"),
    ("trinken", "Flüssigkeit zu sich nehmen"),
    ("fühlen", "empfinden"),
    ("riechen", "Gerüche wahrnehmen"),
    ("lügen", "die Unwahrheit sagen"),
    ("sterben", "das Leben verlieren"),
    ("verlieren", "nicht mehr haben"),
    ("empfehlen", "raten"),
    ("stehlen", "ohne Erlaubnis nehmen"),
    ("glauben", "für wahr halten"),
    ("halten", "festhalten"),
    ("reden", "sprechen"),
    ("erzählen", "eine Geschichte mitteilen"),
    ("bauen", "etwas errichten"),
    ("planen", "vorausdenken"),
    ("ändern", "modifizieren"),
    ("verbessern", "besser machen"),
    ("prüfen", "kontrollieren"),
    ("studieren", "an einer Hochschule lernen"),
    ("üben", "trainieren"),
    ("malen", "ein Bild erstellen"),
    ("zeichnen", "Linien auf Papier machen"),
    ("fotografieren", "Bilder mit der Kamera machen"),
    ("feiern", "ein Fest haben"),
    ("gratulieren", "Glückwünsche aussprechen"),
    ("besuchen", "jemanden aufsuchen"),
    ("einladen", "zum Kommen auffordern"),
    ("küssen", "mit den Lippen berühren"),
    ("lieben", "Zuneigung empfinden"),
    ("hassen", "ablehnen"),
    ("lachen", "Freude zeigen"),
    ("weinen", "Tränen vergießen"),
    ("schreien", "laut rufen"),
    ("flüstern", "leise sprechen"),
    ("rufen", "laut sprechen"),
    ("sammeln", "zusammentragen"),
    ("ordnen", "sortieren"),
    ("packen", "in eine Tasche legen"),
    ("waschen", "reinigen mit Wasser"),
    ("putzen", "sauber machen"),
    ("kämmen", "Haare ordnen"),
    ("rasieren", "Haare entfernen"),
    ("anziehen", "Kleidung tragen"),
    ("ausziehen", "Kleidung ablegen"),
    ("duschen", "sich waschen unter Wasser"),
    ("danken", "Dank aussprechen"),
    ("entschuldigen", "um Verzeihung bitten"),
    ("verzeihen", "nicht mehr böse sein"),
    ("vergessen", "nicht mehr wissen"),
    ("erinnern", "sich erinnern"),
    ("merken", "bemerken"),
    ("behalten", "nicht weggeben"),
    ("teilen", "in Teile aufteilen"),
    ("schenken", "gratis geben"),
    ("leihen", "temporär geben"),
    ("borgen", "temporär nehmen"),
    ("sparen", "Geld zurücklegen"),
    ("ausgeben", "Geld verwenden"),
    ("verdienen", "Geld für Arbeit bekommen"),
    ("kosten", "einen Preis haben"),
    ("mieten", "gegen Geld nutzen"),
    ("vermieten", "gegen Geld verleihen"),
    ("nutzen", "verwenden"),
    ("benutzen", "gebrauchen"),
    ("verwenden", "anwenden"),
    ("probieren", "testen"),
    ("testen", "prüfen"),
    ("wählen", "auswählen"),
    ("stimmen", "korrekt sein"),
    ("passen", "zueinander passen"),
    ("gehören", "Eigentum sein"),
    ("scheinen", "Licht ausstrahlen"),
    ("regnen", "Regen fallen"),
    ("schneien", "Schnee fallen"),
    ("blühen", "Blumen haben"),
    ("wachsen", "größer werden"),
    ("fallen", "nach unten gehen"),
    ("steigen", "nach oben gehen"),
    ("springen", "mit den Füßen abstoßen"),
    ("rennen", "schnell laufen"),
]


def main() -> None:
    verbs: list[tuple[str, str, dict[str, dict[str, str]]]] = []
    seen: set[str] = set()

    def add(inf: str, defn: str, conj: dict[str, dict[str, str]] | None = None) -> None:
        if inf in seen:
            return
        seen.add(inf)
        verbs.append((inf, defn, conj or full_regular(inf)))

    for inf, (defn, conj) in IRREGULAR.items():
        add(inf, defn, conj)
    for inf, defn in REGULAR_DEFS:
        if len(verbs) >= 100:
            break
        add(inf, defn)

    assert len(verbs) == 100, f"expected 100 verbs, got {len(verbs)}"

    lines = [
        '"""Catalog of 100 popular German verbs with full conjugations for seed migration."""',
        "",
        "from __future__ import annotations",
        "",
        'TENSES = ("present", "past", "future")',
        'PERSONS = ("1sg", "2sg", "3sg", "1pl", "2pl", "3pl")',
        "",
        "# Each entry: (infinitive, definition, {tense: {person: form}})",
        "GERMAN_VERBS_CATALOG: list[tuple[str, str, dict[str, dict[str, str]]]]] = [",
    ]
    for inf, defn, conj in verbs:
        lines.append("    (")
        lines.append(f"        {inf!r},")
        lines.append(f"        {defn!r},")
        lines.append("        {")
        for tense in TENSES:
            lines.append(f"            {tense!r}: {{")
            for person in PERSONS:
                lines.append(f"                {person!r}: {conj[tense][person]!r},")
            lines.append("            },")
        lines.append("        },")
        lines.append("    ),")
    lines.append("]")

    out = Path(__file__).resolve().parents[1] / "alembic" / "seed_data" / "german_verbs_catalog.py"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out} ({len(verbs)} verbs)")


if __name__ == "__main__":
    main()
