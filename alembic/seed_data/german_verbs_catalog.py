"""100 popular German verbs with conjugation generation for seed migration."""

from __future__ import annotations

PERSONS = ("1sg", "2sg", "3sg", "1pl", "2pl", "3pl")
TENSES = ("present", "past", "future")

# (infinitive, definition_de)
GERMAN_VERBS: list[tuple[str, str]] = [
    ("sein", "Existieren oder sich befinden."),
    ("haben", "Besitzen oder halten."),
    ("werden", "In einen Zustand übergehen."),
    ("können", "Fähigkeit oder Möglichkeit ausdrücken."),
    ("müssen", "Notwendigkeit ausdrücken."),
    ("sagen", "Mit Worten mitteilen."),
    ("machen", "Etwas herstellen oder tun."),
    ("geben", "Jemandem etwas überreichen."),
    ("kommen", "Sich nähern oder ankommen."),
    ("gehen", "Zu Fuß sich bewegen."),
    ("wissen", "Information besitzen."),
    ("sehen", "Mit den Augen wahrnehmen."),
    ("lassen", "Erlauben oder zulassen."),
    ("stehen", "Aufrecht auf den Füßen sein."),
    ("finden", "Entdecken oder suchen und finden."),
    ("bleiben", "Nicht weggehen."),
    ("liegen", "Horizontal ruhen."),
    ("heißen", "Einen Namen tragen."),
    ("denken", "Im Kopf überlegen."),
    ("nehmen", "Etwas mit der Hand greifen."),
    ("tun", "Eine Handlung ausführen."),
    ("dürfen", "Erlaubnis haben."),
    ("glauben", "Für wahr halten."),
    ("halten", "Festhalten oder stoppen."),
    ("nennen", "Einen Namen geben."),
    ("mögen", "Gern haben."),
    ("zeigen", "Sichtbar machen."),
    ("führen", "Leiten oder begleiten."),
    ("sprechen", "Mit der Sprache kommunizieren."),
    ("bringen", "Etwas zu einem Ort tragen."),
    ("leben", "Existieren als Lebewesen."),
    ("fahren", "Mit einem Fahrzeug reisen."),
    ("meinen", "Eine Meinung haben."),
    ("fragen", "Um Information bitten."),
    ("kennen", "Jemanden oder etwas kennen."),
    ("gelten", "Als gültig gelten."),
    ("stellen", "Etwas aufstellen."),
    ("spielen", "Ein Spiel ausüben."),
    ("arbeiten", "Beruflich tätig sein."),
    ("brauchen", "Benötigen."),
    ("folgen", "Hinter jemandem hergehen."),
    ("lernen", "Wissen erwerben."),
    ("verstehen", "Begreifen."),
    ("setzen", "Etwas platzieren."),
    ("bekommen", "Etwas erhalten."),
    ("beginnen", "Anfangen."),
    ("erzählen", "Eine Geschichte berichten."),
    ("tragen", "Auf dem Körper tragen."),
    ("schreiben", "Mit Schrift festhalten."),
    ("lesen", "Geschriebenes verstehen."),
    ("verlieren", "Nicht mehr haben."),
    ("kennenlernen", "Zum ersten Mal kennen."),
    ("entscheiden", "Eine Wahl treffen."),
    ("entwickeln", "Sich weiterentwickeln."),
    ("erklären", "Etwas deutlich machen."),
    ("erreichen", "Ein Ziel schaffen."),
    ("fehlen", "Nicht da sein."),
    ("gefallen", "Angenehm sein."),
    ("gehören", "Im Besitz sein."),
    ("geschehen", "Passieren."),
    ("gewinnen", "Einen Wettbewerb gewinnen."),
    ("helfen", "Unterstützung leisten."),
    ("hoffen", "Eine Erwartung haben."),
    ("hören", "Geräusche wahrnehmen."),
    ("kaufen", "Gegen Geld erwerben."),
    ("kochen", "Essen zubereiten."),
    ("laufen", "Schnell gehen."),
    ("lieben", "Starke Zuneigung empfinden."),
    ("öffnen", "Zugänglich machen."),
    ("schließen", "Nicht mehr offen sein."),
    ("schlafen", "Ruhen mit geschlossenen Augen."),
    ("schwimmen", "Im Wasser fortbewegen."),
    ("singen", "Musikalische Töne erzeugen."),
    ("sitzen", "Auf einem Sitz sein."),
    ("sterben", "Das Leben verlieren."),
    ("studieren", "An einer Hochschule lernen."),
    ("suchen", "Etwas finden wollen."),
    ("tanzen", "Rhythmisch sich bewegen."),
    ("trinken", "Flüssigkeit zu sich nehmen."),
    ("vergessen", "Nicht mehr im Gedächtnis haben."),
    ("verkaufen", "Gegen Geld abgeben."),
    ("warten", "Auf etwas warten."),
    ("waschen", "Reinigen mit Wasser."),
    ("wünschen", "Sich etwas erhoffen."),
    ("ziehen", "Ziehen oder umziehen."),
    ("antworten", "Auf eine Frage reagieren."),
    ("bedeuten", "Eine Bedeutung haben."),
    ("bieten", "Anbieten."),
    ("bitten", "Höflich um etwas bitten."),
    ("danken", "Dank aussprechen."),
    ("dienen", "Einem Zweck dienen."),
    ("enden", "Zu Ende gehen."),
    ("fallen", "Nach unten fallen."),
    ("feiern", "Ein Fest begehen."),
    ("füllen", "Voll machen."),
    ("grüßen", "Einen Gruß aussprechen."),
    ("hängen", "An etwas befestigt sein."),
    ("holen", "Holen oder abholen."),
    ("kosten", "Einen Preis haben."),
    ("lachen", "Freude laut äußern."),
    ("legen", "Horizontal platzieren."),
    ("liefern", "Bringen oder zustellen."),
    ("merken", "Bemerken oder sich erinnern."),
    ("passen", "Zueinander passen."),
    ("planen", "Voraus planen."),
    ("rechnen", "Mathematisch berechnen."),
    ("reden", "Sprechen oder plaudern."),
    ("reisen", "Eine Reise unternehmen."),
    ("riechen", "Einen Geruch wahrnehmen."),
    ("scheinen", "Licht ausstrahlen."),
    ("schicken", "Versenden."),
    ("schneiden", "Mit einem Messer teilen."),
    ("springen", "Vom Boden abheben."),
    ("steigen", "Nach oben gehen."),
    ("stimmen", "Richtig oder übereinstimmend sein."),
    ("träumen", "Im Schlaf erleben."),
    ("üben", "Wiederholt trainieren."),
    ("verlassen", "Einen Ort verlassen."),
    ("versuchen", "Etwas probieren."),
    ("wachsen", "Größer werden."),
    ("weinen", "Tränen vergießen."),
    ("wiederholen", "Noch einmal tun."),
    ("wohnen", "An einem Ort leben."),
    ("wundern", "Überrascht sein."),
    ("ändern", "Verändern."),
    ("ankommen", "An einem Ziel ankommen."),
    ("aufstehen", "Vom Liegen aufstehen."),
    ("aussehen", "Ein bestimmtes Aussehen haben."),
    ("bezahlen", "Geld geben."),
    ("einladen", "Zu einem Ereignis einladen."),
]

# Irregular conjugations: infinitive -> {tense: {person: form}}
IRREGULAR: dict[str, dict[str, dict[str, str]]] = {
    "sein": {
        "present": {"1sg": "bin", "2sg": "bist", "3sg": "ist", "1pl": "sind", "2pl": "seid", "3pl": "sind"},
        "past": {"1sg": "war", "2sg": "warst", "3sg": "war", "1pl": "waren", "2pl": "wart", "3pl": "waren"},
        "future": {"1sg": "werde sein", "2sg": "wirst sein", "3sg": "wird sein", "1pl": "werden sein", "2pl": "werdet sein", "3pl": "werden sein"},
    },
    "haben": {
        "present": {"1sg": "habe", "2sg": "hast", "3sg": "hat", "1pl": "haben", "2pl": "habt", "3pl": "haben"},
        "past": {"1sg": "hatte", "2sg": "hattest", "3sg": "hatte", "1pl": "hatten", "2pl": "hattet", "3pl": "hatten"},
        "future": {"1sg": "werde haben", "2sg": "wirst haben", "3sg": "wird haben", "1pl": "werden haben", "2pl": "werdet haben", "3pl": "werden haben"},
    },
    "werden": {
        "present": {"1sg": "werde", "2sg": "wirst", "3sg": "wird", "1pl": "werden", "2pl": "werdet", "3pl": "werden"},
        "past": {"1sg": "wurde", "2sg": "wurdest", "3sg": "wurde", "1pl": "wurden", "2pl": "wurdet", "3pl": "wurden"},
        "future": {"1sg": "werde werden", "2sg": "wirst werden", "3sg": "wird werden", "1pl": "werden werden", "2pl": "werdet werden", "3pl": "werden werden"},
    },
    "können": {
        "present": {"1sg": "kann", "2sg": "kannst", "3sg": "kann", "1pl": "können", "2pl": "könnt", "3pl": "können"},
        "past": {"1sg": "konnte", "2sg": "konntest", "3sg": "konnte", "1pl": "konnten", "2pl": "konntet", "3pl": "konnten"},
        "future": {"1sg": "werde können", "2sg": "wirst können", "3sg": "wird können", "1pl": "werden können", "2pl": "werdet können", "3pl": "werden können"},
    },
    "müssen": {
        "present": {"1sg": "muss", "2sg": "musst", "3sg": "muss", "1pl": "müssen", "2pl": "müsst", "3pl": "müssen"},
        "past": {"1sg": "musste", "2sg": "musstest", "3sg": "musste", "1pl": "mussten", "2pl": "musstet", "3pl": "mussten"},
        "future": {"1sg": "werde müssen", "2sg": "wirst müssen", "3sg": "wird müssen", "1pl": "werden müssen", "2pl": "werdet müssen", "3pl": "werden müssen"},
    },
    "gehen": {
        "present": {"1sg": "gehe", "2sg": "gehst", "3sg": "geht", "1pl": "gehen", "2pl": "geht", "3pl": "gehen"},
        "past": {"1sg": "ging", "2sg": "gingst", "3sg": "ging", "1pl": "gingen", "2pl": "gingt", "3pl": "gingen"},
        "future": {"1sg": "werde gehen", "2sg": "wirst gehen", "3sg": "wird gehen", "1pl": "werden gehen", "2pl": "werdet gehen", "3pl": "werden gehen"},
    },
    "kommen": {
        "present": {"1sg": "komme", "2sg": "kommst", "3sg": "kommt", "1pl": "kommen", "2pl": "kommt", "3pl": "kommen"},
        "past": {"1sg": "kam", "2sg": "kamst", "3sg": "kam", "1pl": "kamen", "2pl": "kamt", "3pl": "kamen"},
        "future": {"1sg": "werde kommen", "2sg": "wirst kommen", "3sg": "wird kommen", "1pl": "werden kommen", "2pl": "werdet kommen", "3pl": "werden kommen"},
    },
    "sehen": {
        "present": {"1sg": "sehe", "2sg": "siehst", "3sg": "sieht", "1pl": "sehen", "2pl": "seht", "3pl": "sehen"},
        "past": {"1sg": "sah", "2sg": "sahst", "3sg": "sah", "1pl": "sahen", "2pl": "saht", "3pl": "sahen"},
        "future": {"1sg": "werde sehen", "2sg": "wirst sehen", "3sg": "wird sehen", "1pl": "werden sehen", "2pl": "werdet sehen", "3pl": "werden sehen"},
    },
    "geben": {
        "present": {"1sg": "gebe", "2sg": "gibst", "3sg": "gibt", "1pl": "geben", "2pl": "gebt", "3pl": "geben"},
        "past": {"1sg": "gab", "2sg": "gabst", "3sg": "gab", "1pl": "gaben", "2pl": "gabt", "3pl": "gaben"},
        "future": {"1sg": "werde geben", "2sg": "wirst geben", "3sg": "wird geben", "1pl": "werden geben", "2pl": "werdet geben", "3pl": "werden geben"},
    },
    "nehmen": {
        "present": {"1sg": "nehme", "2sg": "nimmst", "3sg": "nimmt", "1pl": "nehmen", "2pl": "nehmt", "3pl": "nehmen"},
        "past": {"1sg": "nahm", "2sg": "nahmst", "3sg": "nahm", "1pl": "nahmen", "2pl": "nahmt", "3pl": "nahmen"},
        "future": {"1sg": "werde nehmen", "2sg": "wirst nehmen", "3sg": "wird nehmen", "1pl": "werden nehmen", "2pl": "werdet nehmen", "3pl": "werden nehmen"},
    },
}


def _stem(infinitive: str) -> str:
    if infinitive.endswith("en"):
        return infinitive[:-2]
    if infinitive.endswith("n"):
        return infinitive[:-1]
    return infinitive


def _regular_conjugations(infinitive: str) -> dict[str, dict[str, str]]:
    stem = _stem(infinitive)
    present = {
        "1sg": f"{stem}e",
        "2sg": f"{stem}st",
        "3sg": f"{stem}t",
        "1pl": f"{stem}en",
        "2pl": f"{stem}t",
        "3pl": f"{stem}en",
    }
    past = {
        "1sg": f"{stem}te",
        "2sg": f"{stem}test",
        "3sg": f"{stem}te",
        "1pl": f"{stem}ten",
        "2pl": f"{stem}tet",
        "3pl": f"{stem}ten",
    }
    future = {
        "1sg": f"werde {infinitive}",
        "2sg": f"wirst {infinitive}",
        "3sg": f"wird {infinitive}",
        "1pl": f"werden {infinitive}",
        "2pl": f"werdet {infinitive}",
        "3pl": f"werden {infinitive}",
    }
    return {"present": present, "past": past, "future": future}


def conjugations_for(infinitive: str) -> dict[str, dict[str, str]]:
    if infinitive in IRREGULAR:
        return IRREGULAR[infinitive]
    return _regular_conjugations(infinitive)


def all_conjugation_rows(infinitive: str) -> list[tuple[str, str, str]]:
    """Returns list of (tense, person, form)."""
    conj = conjugations_for(infinitive)
    rows: list[tuple[str, str, str]] = []
    for tense in TENSES:
        for person in PERSONS:
            rows.append((tense, person, conj[tense][person]))
    return rows
