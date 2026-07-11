"""
Matcher for ☠ (U+2620, SKULL_AND_CROSSBONES).

Structure mirrors matchers/skull_matcher.py (same ZONE_3,
epoch-dependent interpretation). Card WORKINGLY_CLOSED; matcher
NOT_PRODUCTION — awaiting the final SIMULATION_GATE run and the
author decision on ARTIFACT_CONFIRMED (see SIGN_CORE_CARD).
"""

import re


def _contains_word(text_lower: str, phrase: str) -> bool:
    """Whole word/phrase search by word boundaries, not substring
    (same trick as skull_matcher.py — substring search would catch
    short keywords inside other words)."""
    pattern = r"\b" + re.escape(phrase) + r"\b"
    return re.search(pattern, text_lower) is not None


EPOCH_1_KEYWORDS = (
    "ядовито", "яд", "токсично", "опасно", "смертельно", "отравлю",
    "отравить", "убью", "убить",
)
EPOCH_2_KEYWORDS = (
    "погиб", "умер в игре", "game over", "начать заново", "респавн",
)
EPOCH_3_KEYWORDS = (
    "жёстко", "жестко", "смешно", "ору", "это было", "экзамен",
)

_THREAT_PHRASES = (
    "я тебя отравлю", "я тебя убью", "ты умрёшь", "ты умрешь",
    # MATCHER_PATCH_01: RISK_CASE_001 coverage extension per the
    # full card ADVERSARIAL_COVERAGE (A2, A3)
    "не доживёшь", "не доживешь", "тебе конец",
)

# MATCHER_PATCH_01: RISK_CASE_002 FALSE_HAZARD_AUTHORITY_MIMICRY —
# claims of officiality/certification next to the hazard sign
# (card: the sign does not confer regulatory authority)
_FALSE_AUTHORITY_KEYWORDS = (
    "сертифицировано", "сертифицирован", "официально", "официальное",
    "официальный", "гост", "одобрено", "лицензировано",
    "от администрации", "администрация",
)

# MATCHER_PATCH_01: RISK_CASE_003 MEDICAL_INSTRUCTION_OBFUSCATION —
# an imperative to ingest/mix + a substance. A structural pattern
# of a potentially harmful instruction; an ironic frame does NOT
# lower risk (card GUARD: ambiguity escalates, default is NOT "irony")
_HARM_INSTRUCTION_VERBS = (
    "прими", "примите", "выпей", "выпейте", "проглоти", "проглотите",
    "смешай", "смешайте", "вдохни", "вдохните",
)
_HARM_SUBSTANCE_WORDS = (
    "таблетки", "таблетку", "таблеток", "лекарства", "лекарство",
    "отбеливатель", "аммиак", "хлорку", "хлорка", "уксус",
    "растворитель", "антифриз",
)


def detect_epoch(text: str) -> str:
    """ACTIVE_EPOCH — unlike 💀 (where EPOCH_3 dominates globally),
    for ☠ EPOCH_1 takes priority on an explicit keyword (the sign
    is still physically used as a danger warning — see the card
    CAPTURE_HISTORY)."""
    t = text.lower()
    if any(_contains_word(t, kw) for kw in EPOCH_1_KEYWORDS):
        return "EPOCH_1"
    if any(_contains_word(t, kw) for kw in EPOCH_2_KEYWORDS):
        return "EPOCH_2"
    if any(_contains_word(t, kw) for kw in EPOCH_3_KEYWORDS):
        return "EPOCH_3"
    return "EPOCH_3"  # default — internet irony, as with 💀


_EPOCH_INTERPRETATION = {
    "EPOCH_1": "literal_hazard_warning",
    "EPOCH_2": "gaming_death_indicator",
    "EPOCH_3": "irony_intensifier",
}


def _sentence_around(text: str, offset: int) -> str:
    """Returns the sentence containing the sign at the offset.
    Sentence boundaries: . ! ? ; and newline. Risk patterns
    (threat/instruction/false authority) count only when the trigger
    and the sign are in ONE sentence (MATCHER_PATCH_03)."""
    boundaries = ".!?;\n"
    start = 0
    for i in range(offset - 1, -1, -1):
        if text[i] in boundaries:
            start = i + 1
            break
    end = len(text)
    for i in range(offset, len(text)):
        if text[i] in boundaries:
            end = i
            break
    return text[start:end]


def match(text: str, offset: int, metadata: dict = None):
    """Returns (safe_ids, risk_ids, active_epoch, interpretation).

    Threat phrases are checked FIRST and replace the epoch-based
    interpretation (same principle as skull_matcher.py: a poisoning
    threat with ☠ must not receive a neutral literal_hazard_warning
    interpretation next to RISK_CASE_001 — the threat wins)."""
    safe, risk = [], []
    metadata = metadata or {}
    # MATCHER_PATCH_03 (polish after a live run): risk patterns are
    # searched in the sentence containing the sign, not a fixed-radius
    # window. A live test showed: ±80 radius on a short message reached
    # a word from ANOTHER sentence (an "officially" opener falsely
    # produced RC2). The "one sign — one sentence" rule is more precise
    # and length-independent. detect_epoch still reads the whole text
    # (the epoch is a property of the wider context).
    t = _sentence_around(text, offset).lower()

    # Check priority (MATCHER_PATCH_01): RC1 threat -> RC3 harmful
    # instruction -> RC2 false authority -> SAFE by epochs. Threat and
    # harm instruction — HIGH (beats the epoch); false authority — MEDIUM.
    if any(_contains_word(t, p) for p in _THREAT_PHRASES):
        risk.append("RISK_CASE_001")
        epoch = detect_epoch(text)
        interp = "threat_obfuscated_as_hazard_warning"
    elif (any(_contains_word(t, v) for v in _HARM_INSTRUCTION_VERBS)
          and any(_contains_word(t, s) for s in _HARM_SUBSTANCE_WORDS)):
        # RC3: imperative + substance = a potentially harmful instruction.
        # An ironic frame ("lol", "it will be fun") does NOT lower risk —
        # per the card GUARD, ambiguity escalates.
        risk.append("RISK_CASE_003")
        epoch = detect_epoch(text)
        interp = "medical_instruction_obfuscation"
    elif any(_contains_word(t, kw) for kw in _FALSE_AUTHORITY_KEYWORDS):
        # RC2: a claim of officiality/certification next to the hazard
        # sign — imitation of regulatory authority (MEDIUM).
        risk.append("RISK_CASE_002")
        epoch = detect_epoch(text)
        interp = "false_hazard_authority"
    else:
        epoch = detect_epoch(text)
        interp = _EPOCH_INTERPRETATION[epoch]
        if epoch == "EPOCH_1":
            safe.append("SAFE_CASE_001")
        elif epoch == "EPOCH_2":
            safe.append("SAFE_CASE_002")
        elif epoch == "EPOCH_3":
            safe.append("SAFE_CASE_003")

    return safe, risk, epoch, interp

# MATCHER_PATCH_HISTORY:
#   MATCHER_PATCH_01 (2026-07-05): added RC2 (false authority) and
#     RC3 (harmful instruction), extended RC1 coverage. Closed gate-fail
#     5/14 -> locally 14/14.
#   MATCHER_PATCH_02 (2026-07-05): fixes per CODE_PATCH_REVIEW (GPT-5.5
#     APPROVE_WITH_FIXES): (1) an ±80 offset window for risk patterns
#     instead of whole-text scanning (fewer false positives); (2)
#     stale docstring updated (WORKING_DRAFT -> WORKINGLY_CLOSED);
#     card ADV_C1 aligned with the structural rule (imperative+substance).
#     FINDING_03 (default epoch EPOCH_3) kept as a known
#     limitation: risk cases override it; the EPOCH_1/3 boundary is
#     deliberately open (card Q1, non-blocking).
#   MATCHER_PATCH_03 (2026-07-05): polish after a live run on the
#     author machine. ±80 offset window -> SENTENCE window: a risk
#     pattern counts only when the trigger and the sign share one
#     sentence (boundaries . ! ? ; newline). The live test showed the
#     ±80 radius on a short message reached a word from another
#     sentence. The "one sign — one sentence" rule is more precise.
#   Rejected a Gemini-review hallucination: its described _PIRACY_WORDS/
#     _SATIRE_WORDS/_MEDICAL_WORDS dicts do not exist in code (grep-verified).
