"""
Matcher for DOT (U+002E, ZONE_1).

IMPORTANT CAVEAT (do not hide): SAFE_CASES/RISK_CASES in the card are
textual illustrations for humans/reviewers (SIMULATION_GATE), not
formal patterns. Some of them (RISK_CASE_001 FAKE_OFFICIAL_
NOTATION, RISK_CASE_003 VERSION_NUMBER_TRUST_INFLATION, RISK_CASE_004
ABBREVIATION_AUTHORITY_MIMICRY, RISK_CASE_005 ELLIPSIS_AS_FALSE_
CONTINUATION_SIGNAL) describe RHETORICAL patterns — "the text creates
a false impression of X" — requiring semantic understanding, not
reducible to a deterministic character check. This matcher does NOT
detect them and does not fake detection with bogus rules (see the
dot_module.py lesson — exactly such faking false-positived on "readme.txt.bak").
Only structurally checkable cases are implemented: decimal/sentence/
abbreviation/file_extension/ellipsis (SAFE) and DOMAIN_LOOKALIKE/
NUMERIC_OBFUSCATION (RISK, both with a clear structural signal).
"""

import re
from public_suffix import load_compound_suffixes, load_single_tlds

_GENERIC_TLDS = {"com", "org", "net", "info", "biz", "gov", "edu", "io", "app", "dev"}

_compound_suffixes_cache = None
_compound_suffixes_source = None
_single_tlds_cache = None
_single_tlds_source = None


def _get_compound_suffixes():
    """Lazy load of compound domain suffixes (once per process
    lifetime) — three protection levels, see public_suffix.py."""
    global _compound_suffixes_cache, _compound_suffixes_source
    if _compound_suffixes_cache is None:
        _compound_suffixes_cache, _compound_suffixes_source = load_compound_suffixes()
    return _compound_suffixes_cache, _compound_suffixes_source


def _get_single_tlds():
    """Lazy load of single TLDs (IANA registry) — the same
    three-level discipline. FIXED (2026-06-29, GPT-5.5):
    a tiny hand-made _TLDS (20 entries) was used before, so real
    TLDs like .shop/.xyz/.site produced false negatives on
    domain_mimicry_risk."""
    global _single_tlds_cache, _single_tlds_source
    if _single_tlds_cache is None:
        _single_tlds_cache, _single_tlds_source = load_single_tlds()
    return _single_tlds_cache, _single_tlds_source


def get_compound_suffix_source() -> str:
    """Public entry for the calling runtime (msl_mip_runtime.py):
    which protection level fired for the compound suffix list —
    'LIVE_FETCH' / 'CACHE_FROM_<date>' / 'EMBEDDED_FALLBACK'.
    Call ONCE at program start, not on every match."""
    _, source = _get_compound_suffixes()
    return source


def get_single_tld_source() -> str:
    """FIXED (MAJOR, found by GPT-5.5, 2026-06-29): the single-TLD
    source (IANA registry) used to load but was never surfaced to
    the caller — the user saw the honest warning about compound
    suffixes but not about single TLDs. Same discipline: call ONCE
    at start."""
    _, source = _get_single_tlds()
    return source

# FIXED (2026-06-29): _TLDS (a tiny hand list of 20 entries)
# removed — replaced by _get_single_tlds() (IANA registry, three
# protection levels). See public_suffix.py.
_EXTS = {
    "md", "txt", "py", "js", "json", "xml", "html", "css", "pdf",
    "doc", "docx", "xls", "png", "jpg", "jpeg", "gif", "zip", "tar",
    "exe", "dll",
}


def _word_at(text: str, start: int, direction: int) -> str:
    """Extracts a word (alphanumeric) from start in direction +1/-1."""
    out = []
    i = start
    while 0 <= i < len(text) and text[i].isalnum():
        out.append(text[i])
        i += direction
    if direction < 0:
        out.reverse()
    return "".join(out)


def _is_ipv4_like(s: str) -> bool:
    parts = s.split(".")
    if len(parts) != 4:
        return False
    return all(p.isdigit() and 0 <= int(p) <= 255 for p in parts)


_INTERPRETATION_NAMES = {
    "SAFE_CASE_001": "sentence_terminator",
    "SAFE_CASE_002": "decimal_separator",
    "SAFE_CASE_003": "abbreviation",
    "SAFE_CASE_004": "file_extension",
    "SAFE_CASE_004_DOMAIN": "domain_separator",
    "SAFE_CASE_006_ELLIPSIS": "ellipsis",
    "LEADING_DOT": "leading_dot_token",
}


def match(text: str, offset: int):
    """Returns (safe_ids, risk_ids, interpretation) for the dot at
    the offset. FIXED after the conveyor code review
    (CONVEYOR_RUN_PACKET_MSL_MIP_CODE_SINGLE_SIGN_v0_1, 2026-06-28):
    - interpretation is now returned explicitly by the matcher (the
      engine used to take it from card.context — leaking card prose
      outside as a "machine" value, found by GPT-5.5);
    - abbreviation no longer hijacks any single-letter word before
      the dot (broke "x.py", "a.com" — found by GPT-5.5/
      Copilot/Qwen) — it now requires either space+capital after the
      dot ("A. Smith") or a chain of other single-letter words
      ("k.t.n.");
    - leading-dot handling added (".env") — found by Grok/
      Copilot/Qwen/GPT-5.5 as an unhandled edge."""
    safe, risk = [], []
    if offset < 0 or offset >= len(text) or text[offset] != ".":
        return safe, risk, "unknown"

    left = text[offset - 1] if offset > 0 else ""
    right = text[offset + 1] if offset + 1 < len(text) else ""

    # SAFE_CASE_002: decimal_separator
    if left.isdigit() and right.isdigit():
        safe.append("SAFE_CASE_002")
        chain_start = offset
        while chain_start > 0 and (text[chain_start - 1].isdigit() or text[chain_start - 1] == "."):
            chain_start -= 1
        chain_end = offset
        while chain_end < len(text) - 1 and (text[chain_end + 1].isdigit() or text[chain_end + 1] == "."):
            chain_end += 1
        chain = text[chain_start:chain_end + 1]
        if "." in chain and not _is_ipv4_like(chain) and all(
            p.isdigit() for p in chain.split(".")
        ) and len(chain.split(".")) >= 4:
            risk.append("RISK_CASE_006")
        elif len(chain.split(".")) >= 3:
            # SAFE_CASE_005: version_number — 3+ segments, not looking
            # like IP obfuscation (found in code review: the real card
            # contains this SAFE_CASE, previously not flagged separately
            # from decimal_separator)
            safe.append("SAFE_CASE_005")
        return safe, risk, _INTERPRETATION_NAMES["SAFE_CASE_002"]

    # FIXED: abbreviation — only when it REALLY looks like an
    # abbreviation (space+capital after the dot: "A. Smith"), OR
    # a chain of single-letter dot-separated words ("k.t.n."). A bare
    # "single letter before the dot" is no longer enough (broke x.py,
    # a.com — INTERPRETATION would get 'abbreviation' although it is
    # clearly a filename/domain).
    left_word = _word_at(text, offset - 1, -1)
    if len(left_word) == 1 and left_word.isalpha():
        right_word = _word_at(text, offset + 1, +1)
        space_then_upper = (
            offset + 2 < len(text) and text[offset + 1] == " " and text[offset + 2].isupper()
        )
        chain_abbreviation = len(right_word) == 1 and right_word.isalpha()
        if space_then_upper or chain_abbreviation:
            safe.append("SAFE_CASE_003")
            return safe, risk, _INTERPRETATION_NAMES["SAFE_CASE_003"]
        # otherwise — a single-letter word not looking like an abbreviation
        # (x.py, a.com) — fall through to the normal word.word logic

    # ellipsis
    if text[offset:offset + 3] == "..." or text[max(0, offset - 2):offset + 1] == "...":
        safe.append("SAFE_CASE_006_ELLIPSIS")
        return safe, risk, _INTERPRETATION_NAMES["SAFE_CASE_006_ELLIPSIS"]

    # sentence_terminator
    if (offset == len(text) - 1 or not right.isalnum()) and left.isalpha():
        safe.append("SAFE_CASE_001")
        return safe, risk, _INTERPRETATION_NAMES["SAFE_CASE_001"]

    # FIXED: a dot at text start (no left context at all) — used to
    # yield a silent unknown, now an explicit case
    if left == "" and right != "":
        safe.append("LEADING_DOT")
        return safe, risk, _INTERPRETATION_NAMES["LEADING_DOT"]

    if not (left.isalnum() and right.isalnum()):
        return safe, risk, "unknown"

    # FIXED (found in code review, 2026-06-28): the decision
    # "1 dot vs 2+ dots" used dot_count = text.count(".") — over the
    # WHOLE TEXT. So "example.com." (a domain + a sentence-final dot
    # AFTER the domain) was falsely treated as a "2+ dot domain" and
    # got RISK_CASE_002/HIGH, although the domain itself has only one
    # dot — the second belongs to an unrelated sentence further in
    # the text. Dots are now counted only inside the FOUND local
    # chain (the one containing the offset).
    local_chain = None
    for m in re.finditer(r"[\w-]+(?:\.[\w-]+)+", text):
        if m.start() <= offset < m.end():
            local_chain = m.group(0)
            break
    right_word = _word_at(text, offset + 1, +1)

    if local_chain is None:
        # a lone dot with no extendable chain on either side — should
        # not happen here in practice (left/right are already alnum),
        # a defensive fallback
        local_chain = _word_at(text, offset - 1, -1) + "." + right_word

    local_dot_count = local_chain.count(".")
    single_tlds, _ = _get_single_tlds()
    compound_suffixes, _ = _get_compound_suffixes()

    if local_dot_count == 1:
        # FIXED (MINOR, found by GPT-5.5, 2026-06-29): for short
        # chains like "gov.scot" (a single dot) right_word ("scot")
        # alone is neither in single_tlds nor helpful — the WHOLE
        # chain must be checked against known compound suffixes.
        
        if right_word.lower() in single_tlds or local_chain.lower() in compound_suffixes:
            safe.append("SAFE_CASE_004_DOMAIN")
            return safe, risk, _INTERPRETATION_NAMES["SAFE_CASE_004_DOMAIN"]
        safe.append("SAFE_CASE_004")
        return safe, risk, _INTERPRETATION_NAMES["SAFE_CASE_004"]

    last_segment = local_chain.rsplit(".", 1)[-1].lower()
    is_domain_like = last_segment in single_tlds
    # FIXED (MINOR_01, found by GPT-5.5, 2026-06-29): compound
    # suffixes (gov.scot, com.au) are not in _TLDS as a single
    # segment, so they used to yield a correct NONE risk but a
    # wrong file_extension label instead of domain_separator. The
    # last 2-3 segments are checked against real compound
    # suffixes.
    if not is_domain_like:
        segments_for_suffix_check = local_chain.split(".")
        for k in (2, 3):
            if len(segments_for_suffix_check) >= k:
                candidate_suffix = ".".join(segments_for_suffix_check[-k:]).lower()
                if candidate_suffix in compound_suffixes:
                    is_domain_like = True
                    break

    # FIXED (found INDEPENDENTLY during self-check before sending
    # the conveyor packet, 2026-06-29): domain_mimicry_risk was
    # computed UNCONDITIONALLY, regardless of is_domain_like. So
    # "example.com.bak" (clearly a file, not a domain — the last
    # segment "bak" is no TLD nor compound suffix) still got
    # RISK_CASE_002 because "com" is not last. Semantically
    # incoherent: SAFE_CASE_004 (file) + RISK_CASE_002 (DOMAIN
    # imitation) at once. The imitation check now runs ONLY inside
    # the "looks like a domain" branch — if the last segment is no
    # TLD nor compound suffix, domain-imitation risk simply does
    # not apply, whatever generic TLD sits inside the chain.
    if is_domain_like:
        safe.append("SAFE_CASE_004_DOMAIN")
        segments = local_chain.split(".")
        domain_mimicry_risk = False
        for i, seg in enumerate(segments[:-1]):
            if seg.lower() in _GENERIC_TLDS:
                remaining = ".".join(segments[i:]).lower()
                if remaining not in compound_suffixes:
                    domain_mimicry_risk = True
                    break
        if domain_mimicry_risk:
            risk.append("RISK_CASE_002")
        return safe, risk, _INTERPRETATION_NAMES["SAFE_CASE_004_DOMAIN"]
    safe.append("SAFE_CASE_004")
    return safe, risk, _INTERPRETATION_NAMES["SAFE_CASE_004"]
