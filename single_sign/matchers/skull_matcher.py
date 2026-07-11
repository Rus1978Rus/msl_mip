"""
Matcher for SKULL (U+1F480, ZONE_3).

Keywords for detect_epoch are taken from the card's real FUNCTION
fields (EPOCH_1: "marker of death, poison, danger, Halloween";
EPOCH_2: "i am tired/dead inside/burnout/defeat";
EPOCH_3: LOL/LMAO/ROFL replacement — hysterical laughter/absurdist
humour) — NOT separately invented categories (see the lesson of the
previous runtime, which invented EPOCH_HALLOWEEN/EPOCH_GAMING
that do not exist in the real card: Halloween is part of FUNCTION
EPOCH_1, not a separate epoch).

HONESTLY PARTIALLY METADATA-DEPENDENT: RISK_CASE_003
(GENERATIONAL_MISINTERPRETATION), RISK_CASE_006 (MEDICAL_MISREAD),
RISK_CASE_008 (CROSS_PLATFORM_EPOCH_MISMATCH) fundamentally require
INPUT_METADATA (SENDER_COHORT/DOMAIN/PLATFORM) — not a text
pattern; explicitly provided for by the MODULE_TEMPLATE architecture
(the INPUT_METADATA section). Without metadata these cases are not
detected — not an implementation gap but an honest reflection that
searching the text for what is not there would be the same error
class caught before.
RISK_CASE_001 (ALGORITHMIC_FALSE_POSITIVE_BAN), RISK_CASE_005
(SECOND_HAND_EMBARRASSMENT_DRIFT) — not implemented: the first
describes EXTERNAL moderation behaviour (meta-level, not a text
property), the second a fuzzy cultural drift with no clear signal.
RISK_CASE_007 (EMOJI_SEQUENCE_INJECTION) belongs to SEQUENCE_MODULE
(several skulls in a row), not to a single sign; handled by
sequence_engine.py, not here.
"""

import re


def _contains_word(text_lower: str, phrase: str) -> bool:
    """WHOLE word/phrase search by word boundaries, not substring.
    FIXED after code review (Gemini, 2026-06-28): a plain
    `phrase in text` caught 'kill' inside 'skill', 'die' inside
    'diet' — false EPOCH_1 hits on innocent words."""
    pattern = r"\b" + re.escape(phrase) + r"\b"
    return re.search(pattern, text_lower) is not None


EPOCH_1_KEYWORDS = (
    "смерть", "смерти", "умер", "умереть", "убить", "убийство",
    "опасность", "опасно", "гибель", "яд", "ядовито", "хэллоуин",
    "halloween", "death", "dead", "die", "died", "kill", "killed",
    "poison", "toxic", "danger", "dangerous",
)

EPOCH_2_KEYWORDS = (
    "устал", "устала", "выгорел", "не могу", "сдался", "поражение",
    "проиграл", "tired", "exhausted", "burnout", "defeat", "defeated",
    "give up", "failed", "failure",
)

EPOCH_3_KEYWORDS = (
    "lol", "lmao", "rofl", "хаха", "ахах", "смешно", "ржака", "мем",
    "funny", "hilarious", "laugh", "joke", "cringe", "lit", "based",
)

# RISK_CASE_002: REAL_THREAT_OBFUSCATION — an explicit threat phrase nearby
_THREAT_PHRASES = (
    "найду тебя", "i will find you", "убью", "kill you", "i'll kill",
)

# RISK_CASE_004: CANCEL_CULTURE_OSTRACISM — a social "erasure" phrase
_CANCEL_PHRASES = (
    "мёртв для нас", "dead to us", "he is dead to us",
)


def detect_epoch(text: str) -> str:
    """ACTIVE_EPOCH (GLOBAL) — EPOCH_3 dominates but EPOCH_1/EPOCH_2
    reactivate on an explicit textual signal (DORMANT_EPOCHS
    reactivation, see the card). Uses word-boundary search
    (see _contains_word) — substring search caught 'kill' in 'skill'."""
    t = text.lower()
    if any(_contains_word(t, kw) for kw in EPOCH_1_KEYWORDS):
        return "EPOCH_1"
    if any(_contains_word(t, kw) for kw in EPOCH_2_KEYWORDS):
        return "EPOCH_2"
    if any(_contains_word(t, kw) for kw in EPOCH_3_KEYWORDS):
        return "EPOCH_3"
    return "EPOCH_3"  # default ACTIVE_EPOCH (GLOBAL, dominant for Gen Z)


_EPOCH_INTERPRETATION = {
    "EPOCH_1": "literal_death",
    "EPOCH_2": "ironic_exhaustion",
    "EPOCH_3": "humor_marker",
}


_HALLOWEEN_KEYWORDS = ("halloween", "хэллоуин", "🎃")
_MEDICAL_KEYWORDS = ("анатоми", "медицин", "лекция", "слайде")


def _safe_case_for_epoch(text_lower: str, epoch: str) -> list:
    """FIXED after code review (2026-06-28, a finding of independent
    card analysis): the old code blindly assigned SAFE_CASE_003 to any
    non-EPOCH_3 case. Per the real card SAFE_CASE_003 is
    SPECIFICALLY Halloween (holiday greetings, seasonal decoration),
    not "tiredness" nor "death in general". Matching is now exact:
      SAFE_CASE_001 = EPOCH_3 humor (Gen Z social media)
      SAFE_CASE_002 = EPOCH_2 exhaustion (student messaging)
      SAFE_CASE_003 = explicit Halloween context (any epoch)
      SAFE_CASE_006 = explicit medical/academic context
    If EPOCH_1 without Halloween/medical context — honestly left
    without a SAFE_CASE (the card has no exact match for generic
    "death/danger without context refinement"); no approximate
    label substitution."""
    if any(kw in text_lower for kw in _HALLOWEEN_KEYWORDS):
        return ["SAFE_CASE_003"]
    if any(kw in text_lower for kw in _MEDICAL_KEYWORDS):
        return ["SAFE_CASE_006"]
    if epoch == "EPOCH_3":
        return ["SAFE_CASE_001"]
    if epoch == "EPOCH_2":
        return ["SAFE_CASE_002"]
    return []


def match(text: str, offset: int, metadata: dict = None):
    """Returns (safe_ids, risk_ids, active_epoch, interpretation).

    FIXED after code review (CONVEYOR_RUN_PACKET_MSL_MIP_CODE_
    SINGLE_SIGN_v0_1, 2026-06-28): "He is dead to us 💀" used to give
    interpretation="literal_death" SIMULTANEOUSLY with risk=RISK_CASE_004
    (CANCEL_CULTURE_OSTRACISM) — most reviewers (Kimi, Grok,
    GPT-5.5, Qwen) deemed it a real label conflict, not just
    "signal overlap" (minority: Gemini/Copilot saw acceptable
    synergy). Majority decision adopted: when a risk phrase
    (cancel/threat) fires, its interpretation REPLACES the
    epoch-based one, not coexists — the downstream INTERPRETATION
    consumer must not receive "literal_death" for text that is
    actually about social erasure rather than literal death."""
    
    safe, risk = [], []
    metadata = metadata or {}
    t = text.lower()

    # Risk phrases are checked FIRST — they override the epoch-based
    # interpretation when fired (see docstring)
    if any(_contains_word(t, p) for p in _THREAT_PHRASES):
        risk.append("RISK_CASE_002")
        epoch = detect_epoch(text)  # the epoch is still computed for audit
        interp = "threat_obfuscated_as_humor"
    elif any(_contains_word(t, p) for p in _CANCEL_PHRASES):
        risk.append("RISK_CASE_004")
        epoch = detect_epoch(text)
        interp = "social_ostracism_marker"
    else:
        epoch = detect_epoch(text)
        interp = _EPOCH_INTERPRETATION[epoch]
        safe.extend(_safe_case_for_epoch(t, epoch))

    # Metadata-dependent cases — detected ONLY when metadata is
    # actually provided (never guessed from text)
    sender_cohort = metadata.get("SENDER_COHORT")
    if sender_cohort in ("Boomer", "Millennial") and epoch == "EPOCH_3":
        risk.append("RISK_CASE_003")  # GENERATIONAL_MISINTERPRETATION

    domain = metadata.get("DOMAIN")
    if domain == "medical":
        risk.append("RISK_CASE_006")  # MEDICAL_MISREAD

    platform_history = metadata.get("PLATFORM_ORIGIN")
    platform_current = metadata.get("PLATFORM")
    if platform_history and platform_current and platform_history != platform_current:
        risk.append("RISK_CASE_008")  # CROSS_PLATFORM_EPOCH_MISMATCH

    return safe, risk, epoch, interp
