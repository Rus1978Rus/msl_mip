"""
Matcher for SOLIDUS (U+002F, ZONE_2).

CONTEXT_GATE: the solidus has no single active epoch — which
SUBSTRATE is active is decided by context (see the card:
ACTIVE_EPOCH_RESOLUTION.PRIMARY_ACTIVE_EPOCH = NONE_GLOBAL).

HONESTLY NOT IMPLEMENTED (semantic, not structural patterns,
see the dot_matcher.py docstring for the same class of caveat):
  RISK_CASE_005 STATUS_CHAIN_MIMICRY, RISK_CASE_006 ROLE_BINDING_
  MIMICRY, RISK_CASE_007 PHAGO_ENTITY_PATH_MIMICRY — they require
  recognising "looks like a known brand/organisation" or
  "looks like a status chain", which is not a structural feature.
"""


import re


def _word_at(text: str, start: int, direction: int) -> str:
    out = []
    i = start
    allowed = lambda c: c.isalnum() or c in "-_"
    while 0 <= i < len(text) and allowed(text[i]):
        out.append(text[i])
        i += direction
    if direction < 0:
        out.reverse()
    return "".join(out)


_ADMIN_WORDS = {"admin", "root", "execute", "permission", "sudo", "superuser"}
_API_WORDS = {"api", "v1", "v2", "v3"}

# FIXED after code review (CONVEYOR_RUN_PACKET_MSL_MIP_CODE_
# SINGLE_SIGN_v0_1, 2026-06-28, found by ALL 7 reviewers): a domain-
# like segment before the solidus ("trusted.com/verified") must be
# detected by an explicit regex over the text BEFORE the offset, not
# via _word_at (which stops at "." and therefore never sees the
# dot — the root of the bug).
_DOMAIN_BEFORE_SLASH_RE = re.compile(r"[\w-]+\.[A-Za-z]{2,}$")

_INTERPRETATION_NAMES = {
    "SAFE_CASE_001": "path_or_choice_separator",
    "SAFE_CASE_002": "fraction_separator",
    "SAFE_CASE_003": "filesystem_path",
    "SAFE_CASE_004": "url_separator",
    "SAFE_CASE_004_AUTHORITY": "url_authority_separator",
    "SAFE_CASE_005": "date_separator",
}


def detect_substrate(text: str, offset: int) -> str:
    """CONTEXT_GATE: decides the active substrate for a specific
    solidus occurrence. Returns one of:
    MATH / FILESYSTEM / URL / URL_AUTHORITY / DATE / AMBIGUOUS."""

    left = text[offset - 1] if offset > 0 else ""
    right = text[offset + 1] if offset + 1 < len(text) else ""

    if left.isdigit() and right.isdigit():
        window_start = offset
        while window_start > 0 and (text[window_start - 1].isdigit() or text[window_start - 1] == "/"):
            window_start -= 1
        window_end = offset
        while window_end < len(text) - 1 and (text[window_end + 1].isdigit() or text[window_end + 1] == "/"):
            window_end += 1
        chain = text[window_start:window_end + 1]
        parts = chain.split("/")
        if len(parts) == 3 and len(parts[0]) == 4:
            return "DATE"
        return "MATH"

    if text[max(0, offset - 1):offset + 2] == "://" or "://" in text[max(0, offset - 8):offset + 8]:
        return "URL"

    # FIXED (BUG_B, GPT-5.5, 2026-06-28): a Windows path like
    # "C:/Users" with a SINGLE slash was caught by no FILESYSTEM
    # rule (2+ slashes or a leading "./"/".." were required),
    # staying AMBIGUOUS. Explicit pattern "<letter>:/" — a Windows drive.
    if offset >= 2 and text[offset - 2].isalpha() and text[offset - 1] == ":":
        return "FILESYSTEM"

    # FIXED: a backslash before the solidus signals an escape
    # sequence (RISK_CASE_001); without it the FILESYSTEM branch
    # would never be reached for such inputs, and the RISK_CASE_001
    # check in match() would be dead code
    if offset > 0 and text[offset - 1] == "\\":
        return "FILESYSTEM"

    # FIXED: a domain-like segment right before "/"
    # (with no "://" required) — e.g. "trusted.com/verified"
    if _DOMAIN_BEFORE_SLASH_RE.search(text[:offset]):
        return "URL_AUTHORITY"

    if left in "./" or text[max(0, offset - 2):offset] == "..":
        return "FILESYSTEM"
    if text.count("/") >= 2:
        return "FILESYSTEM"

    return "AMBIGUOUS"


def match(text: str, offset: int):
    safe, risk = [], []
    if offset < 0 or offset >= len(text) or text[offset] != "/":
        return safe, risk, "unknown"

    substrate = detect_substrate(text, offset)
    left_word = _word_at(text, offset - 1, -1)
    right_word = _word_at(text, offset + 1, +1)

    if substrate == "MATH":
        safe.append("SAFE_CASE_002")
        return safe, risk, _INTERPRETATION_NAMES["SAFE_CASE_002"]

    if substrate == "DATE":
        safe.append("SAFE_CASE_005")
        return safe, risk, _INTERPRETATION_NAMES["SAFE_CASE_005"]

    if substrate == "URL":
        safe.append("SAFE_CASE_004")
        if "." in left_word and "/" not in left_word:
            risk.append("RISK_CASE_002")
        return safe, risk, _INTERPRETATION_NAMES["SAFE_CASE_004"]

    if substrate == "URL_AUTHORITY":
        # FIXED (AUTHOR_DECISION, 2026-06-29): URL_AUTHORITY used to
        # unconditionally add RISK_CASE_002, making ANY link with a
        # domain a QUEUE_FOR_REVIEW source. Architecturally wrong:
        # the DOT layer already scores domain quality (imitation,
        # subdomains etc.). If DOT found risk — the final verdict is
        # already raised via DOT. If not — the domain is clean and
        # SOLIDUS must not punish it again merely for having a path
        # after it. SOLIDUS records the FACT (a URL path boundary)
        # but adds no risk of its own.
        # Confirmed by a direct run: paypal.com.security-check.ru
        # yields HOLD_PENDING_REVIEW via DOT even without this risk.
        safe.append("SAFE_CASE_004")
        return safe, risk, _INTERPRETATION_NAMES["SAFE_CASE_004_AUTHORITY"]

    if substrate == "FILESYSTEM":
        safe.append("SAFE_CASE_003")

        # RISK_CASE_001: ESCAPE_SEQUENCE — a solidus right after a
        # backslash (found in code review: the real card contains
        # this RISK_CASE, previously unimplemented)
        if offset > 0 and text[offset - 1] == "\\":
            risk.append("RISK_CASE_001")

        if text[max(0, offset - 2):offset] == "..":
            risk.append("RISK_CASE_001")

        if left_word.lower() in _ADMIN_WORDS or right_word.lower() in _ADMIN_WORDS:
            risk.append("RISK_CASE_003")

        if left_word.lower() in _API_WORDS or right_word.lower() in _API_WORDS:
            risk.append("RISK_CASE_004")

        return safe, risk, _INTERPRETATION_NAMES["SAFE_CASE_003"]

    safe.append("SAFE_CASE_001")
    risk.append("RISK_CASE_008")
    return safe, risk, _INTERPRETATION_NAMES["SAFE_CASE_001"]
