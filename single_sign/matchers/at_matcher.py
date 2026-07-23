# -*- coding: utf-8 -*-
"""
Matcher for the @ sign (U+0040, COMMERCIAL AT). ZONE_2, class PH.

Matches SIGN_CORE_CARD_AT_U0040_GEN3_v0_3 (WORKINGLY_CLOSED).
Returns a 3-tuple (safe_ids, risk_ids, interpretation) — like
dot/solidus (a structural sign without cultural epochs).

MAIN PRINCIPLE (from the card): @ is overwhelmingly LEGITIMATE
(email, mention, decorator, price tag, federated handle). RISK ONLY
in the URL-userinfo context. The default is NOT "@ = threat" (CG3).

RISK mechanics are deterministic ONLY with a URL scheme (PATCH_03,
Alibaba/Copilot fact audit per WHATWG + RFC 3986): in http(s)://...@host
host = the segment after the LAST @, everything before is userinfo.
Without a scheme, paypal.com@evil.ru does NOT give host=evil.ru
(WHATWG: protocol='paypal.com:', host empty) — so without a scheme
it is contextual ambiguity (Q1), not automatic RISK.

MATCHER_PATCH_HISTORY:
  created 2026-07-06 for the @ card (after a 5/5 conveyor + 2 fact audits).
"""
from __future__ import annotations
import re

# URL scheme before @ — marker of URL context (RISK determinism only here)
_URL_SCHEME_RE = re.compile(r'(https?|ftp)://', re.IGNORECASE)
# mailto — email context, @ is legitimate (SAFE, not URL-userinfo)
_MAILTO_RE = re.compile(r'mailto:', re.IGNORECASE)

# a domain with a TLD (to recognise a brand in userinfo position)
_DOMAIN_RE = re.compile(r'[\w-]+\.[A-Za-z]{2,}')
# an IP address as host (RC2)
_IP_RE = re.compile(r'\d{1,3}(?:\.\d{1,3}){3}')

# a code decorator: @ at line start/after indent before an identifier
_DECORATOR_RE = re.compile(r'(^|\n)\s*@[A-Za-z_]\w*')

INTERPRETATION = {
    "SAFE_CASE_001": "email_separator",
    "SAFE_CASE_002": "social_mention",
    "SAFE_CASE_003": "code_decorator",
    "SAFE_CASE_004": "commercial_pricing",
    "SAFE_CASE_005": "mailto_email",
    "SAFE_CASE_006": "handle_list",
    "SAFE_CASE_007": "federated_handle",
    "RISK_CASE_001": "url_userinfo_spoofing",
    "RISK_CASE_002": "userinfo_brand_non_final",
    "RISK_CASE_003": "multiple_at_obfuscation",
    "RISK_CASE_004": "false_verified_account",
}


def _ends_in_valid_tld(label: str) -> bool:
    """True iff the last dot-label of `label` is a registered TLD. Distinguishes a real
    brand domain (paypal.com -> 'com') from a dotted email local part (john.doe -> 'doe').
    Uses the runtime TLD registry lazily (imported at call time so there is no import-order
    or layering coupling); on any failure returns False (fail-closed -> stays a legit email,
    never a false spoof alarm)."""
    try:
        from sequence_engine import _tlds
        tld_set, _degraded = _tlds()
        last = label.rstrip(".").rsplit(".", 1)[-1].lower()
        return bool(last) and last in tld_set
    except Exception:
        return False


def _url_context_around(text: str, offset: int):
    """Extracts the URL-like token containing @ at the offset.
    Token = the contiguous whitespace-free run around the offset."""
    start = offset
    while start > 0 and not text[start - 1].isspace():
        start -= 1
    end = offset
    while end < len(text) and not text[end].isspace():
        end += 1
    return text[start:end], start


def match(text: str, offset: int):
    """Returns (safe_ids, risk_ids, interpretation).
    @ at the offset. RISK only in the URL-userinfo context."""
    safe, risk = [], []

    # Check: the offset really holds @ (or a fullwidth equivalent already
    # normalised to @ at runtime input — see NORMALIZATION_NOTE)
    if offset < 0 or offset >= len(text) or text[offset] != "@":
        return [], [], None

    token, tok_start = _url_context_around(text, offset)
    tok_lower = token.lower()

    has_scheme = bool(_URL_SCHEME_RE.search(token))
    is_mailto = bool(_MAILTO_RE.search(token))

    # --- SAFE: mailto (email in the mailto scheme, not URL-userinfo) ---
    if is_mailto:
        safe.append("SAFE_CASE_005")
        return safe, risk, INTERPRETATION["SAFE_CASE_005"]

    # --- RISK branch: ONLY with a URL scheme (PATCH_03 determinism) ---
    if has_scheme:
        # the token part after the scheme
        after_scheme = _URL_SCHEME_RE.sub("", token)
        at_count = after_scheme.count("@")
        # host = after the LAST @ (WHATWG)
        last_at = after_scheme.rfind("@")
        userinfo = after_scheme[:last_at]
        host_part = after_scheme[last_at + 1:]

        # RC3: multiple @ in a URL — obfuscation
        if at_count >= 2:
            risk.append("RISK_CASE_003")
            return safe, risk, INTERPRETATION["RISK_CASE_003"]

        # a brand domain in userinfo (before @) — an imitation signal
        brand_in_userinfo = bool(_DOMAIN_RE.search(userinfo))
        host_is_ip = bool(_IP_RE.match(host_part))
        host_is_domain = bool(_DOMAIN_RE.match(host_part))

        if brand_in_userinfo and host_is_ip:
            # RC2: brand in userinfo + IP host
            risk.append("RISK_CASE_002")
            return safe, risk, INTERPRETATION["RISK_CASE_002"]
        if brand_in_userinfo and host_is_domain:
            # RC1: basic userinfo spoofing (brand.tld @ other-domain.tld)
            risk.append("RISK_CASE_001")
            return safe, risk, INTERPRETATION["RISK_CASE_001"]
        # @ in a URL but userinfo without a brand domain — legitimate
        # userinfo (e.g. user@host) — not spoofing
        safe.append("SAFE_CASE_001")
        return safe, risk, INTERPRETATION["SAFE_CASE_001"]

    # --- NO scheme: contextual ambiguity (Q1) -> SAFE branching ---
    # a code decorator
    if _DECORATOR_RE.search(text[max(0, offset - 40):offset + 40]):
        safe.append("SAFE_CASE_003")
        return safe, risk, INTERPRETATION["SAFE_CASE_003"]

    # federated handle @user@domain (SAFE_CASE_007): two @ with NO scheme
    if token.count("@") >= 2 and _DOMAIN_RE.search(token):
        safe.append("SAFE_CASE_007")
        return safe, risk, INTERPRETATION["SAFE_CASE_007"]

    # email OR schemeless userinfo spoofing: word@domain.tld, single @
    if token.count("@") == 1 and _DOMAIN_RE.search(token[token.find("@"):]):
        before = token[:token.find("@")]
        # brand.tld@other-domain.tld with NO scheme is the classic display spoof: to the
        # EYE (the witness-frame target, not the URL parser) it reads as a plain email
        # anchored on the brand BEFORE the @, while the resolvable domain is AFTER it.
        # Previously gated on has_scheme and so passed silently (measured 2026-07, agent #9).
        # The tell must be a REAL brand domain: the label before the @ must end in a valid
        # TLD. A dotted email local part (john.doe) ends in a non-TLD and stays a legit
        # email -- that guard removes the false positive the shape-only check produced.
        if _DOMAIN_RE.search(before) and _ends_in_valid_tld(before):
            risk.append("RISK_CASE_001")
            return safe, risk, INTERPRETATION["RISK_CASE_001"]
        safe.append("SAFE_CASE_001")
        return safe, risk, INTERPRETATION["SAFE_CASE_001"]

    # price tag: @ next to digits/currency ("10 pcs @ 5$")
    around = text[max(0, offset - 10):offset + 10]
    if re.search(r'\d', around) and re.search(r'[$€£\d]', text[offset:offset + 10]):
        safe.append("SAFE_CASE_004")
        return safe, risk, INTERPRETATION["SAFE_CASE_004"]

    # mention: @ before a handle word
    if offset + 1 < len(text) and (text[offset + 1].isalnum() or text[offset + 1] == "_"):
        safe.append("SAFE_CASE_002")
        return safe, risk, INTERPRETATION["SAFE_CASE_002"]

    # default: a lone @ with no context — DATA_ONLY, safe
    safe.append("SAFE_CASE_002")
    return safe, risk, INTERPRETATION["SAFE_CASE_002"]
