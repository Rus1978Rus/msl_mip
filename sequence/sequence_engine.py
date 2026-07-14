"""
SEQUENCE_MODULE_TEMPLATE engine — STAGE_1-7.

Implements SEQUENCE_MODULE_TEMPLATE_GEN3_v0_2_PLUS_EPOCH_v0_1 with
PATCH_24/25/26. The layer works ON TOP of single-sign results
(module_engine): takes the source text + the list of OutputStatus of
every processed sign, and searches the known SEQUENCE_CANDIDATES of
all involved cards for matches that are contiguous in the text.

KEY adjacency PRINCIPLE: a candidate only fires when its literal
sequence is actually present in the text AS A CONTIGUOUS
substring. This protects against false "gluing" of signs standing
in different parts of the text (e.g. two dots in "end. Start." do
not form SEQUENCE '..' because other characters sit between them).


CROSS-CARD (PATCH_26): CANDIDATE_POOL is the union of the
SEQUENCE_CANDIDATES of ALL CARD_SET cards, not one. This catches
cross-card idioms like '../' (dot+dot+solidus — both DOT and
SOLIDUS), '://' (SOLIDUS.SC7).
"""

from __future__ import annotations

import unicodedata

from sign_core_card import SignCoreCard, RiskLevel
from sequence_output import SequenceMatch, SequenceOutput
from public_suffix import load_single_tlds


def _build_candidate_pool(cards: list) -> list:
    """STAGE_2/2a (PATCH_26): CANDIDATE_POOL = the union of all
    cards' SEQUENCE_CANDIDATES. Each element is (candidate, card)."""
    pool = []
    for card in cards:
        for sc in card.sequence_candidates:
            pool.append((sc, card))
    # sort by decreasing sequence length — longer (more specific)
    # candidates are checked first so that '../../../' takes
    # priority over '..' at the same spot
    pool.sort(key=lambda pair: len(pair[0].sequence), reverse=True)
    return pool


def _valid_scheme_before(text: str, colon_idx: int) -> bool:
    """SOLIDUS_SCHEME_PATCH (CODE_REVIEW Q1 fix, 2026-07-07): checks
    that a VALID URL scheme precedes the colon at colon_idx per
    RFC 3986 §3.1: scheme = ALPHA *( ALPHA / DIGIT / "+" / "-" / "." ).
    I.e. the sequence starts with a letter and consists of
    letters/digits/+/-/. Cuts the false "//" downgrade in pseudo-schemes
    ("::/", no letter before ":") — found by 6 code reviewers.
    The "://" discriminator fires only for real schemes."""
    i = colon_idx - 1
    end = colon_idx
    while i >= 0 and (text[i].isalnum() or text[i] in "+-."):
        i -= 1
    scheme = text[i + 1:end]
    return len(scheme) >= 1 and scheme[0].isalpha()


def _find_literal_matches(text: str, pool: list,
                          validated_offsets: set = None,
                          card_signs: set = None,
                          strict: bool = False,
                          known_signs: set = None) -> list:
    """STAGE_3-4: finds contiguous literal matches of every candidate
    in the text. Adjacency is guaranteed because str.find looks for
    a CONTIGUOUS substring.

    FIXED (round 2, 2026-06-29): the old "anchor rule" (the leading
    character MUST be a set sign) was disproved by the SOLIDUS.SC6
    "*/" counter-example — the leading "*" is outside the sign set,
    yet the candidate is legitimate if "/" is validated. New rule:

      (a) ALL candidate characters that are signs from CARD_SET OR
          from known_signs (the full system sign registry, see below)
          must be validated;
      (b) at least ONE candidate character must be a CARD_SET sign
          (protection against fully "empty" Ghost matches);
      (c) candidate characters absent from both CARD_SET and
          known_signs (true context — 🎃/😭/☠️ for SKULL, "*" in "*/",
          which have no SIGN_CORE_CARD in the system at all)
          need no validation.

    FIXED (round 3, 2026-06-29, CARD_SET_COMPLETENESS, found in code
    review): card_signs is built only from the cards PASSED to the
    specific call. If the caller forgot to pass DOT while the
    SOLIDUS.SC3 candidate "../" contains dots — the dots used to
    count as "external context" (like the asterisk) although the DOT
    card REALLY exists in the system, just was not passed to THIS
    call. That produced Ghost-Matching via caller inattention, not
    deliberate design. known_signs is a separate optional parameter:
    the FULL registry of signs known to the system (not only the
    current CARD_SET). When passed, a known_signs character ALWAYS
    requires validation even if its card is not in this call's
    card_signs. known_signs=None (default) keeps the old behaviour
    (no registry, for isolated single-card unit tests).
    

    UPSTREAM_DEPENDENT (sc.scope) is checked separately and
    unconditionally blocks the candidate in strict mode — SOLIDUS.SC7 "://".

    strict=False: validated_offsets not passed -> text mode."""
    matches = []
    claimed = []
    card_signs = card_signs or set()
    registry = known_signs if known_signs is not None else card_signs

    def _candidate_validated(sc, idx: int, end: int) -> bool:
        if validated_offsets is None:
            return not strict
        if sc.scope == "UPSTREAM_DEPENDENT":
            # an explicit card mark: the candidate structurally depends
            # on a character outside the sign system — unreachable in
            # strict mode until such a character gets its own card
            return False
        has_card_sign = False
        for pos in range(idx, end):
            ch = text[pos]
            if ch in card_signs:
                has_card_sign = True
            if ch in registry:
                # a sign from CARD_SET OR the full system registry —
                # must be validated in both cases
                if pos not in validated_offsets:
                    return False
        return has_card_sign

    for sc, card in pool:
        seq = sc.sequence
        if not seq:
            continue
        start = 0
        while True:
            idx = text.find(seq, start)
            if idx < 0:
                break
            end = idx + len(seq)
            covered = any(c_start <= idx and end <= c_end for c_start, c_end in claimed)
            if not covered and _candidate_validated(sc, idx, end):
                # ── SOLIDUS_SCHEME_PATCH (variant "b", AUTHOR_DECISION 2026-07-07) ──
                # If "//" immediately follows ":" it is the scheme link
                # of a URL ("://"), legitimate. CLARIFICATION_2: only "://" (with
                # the colon) is neutralised; "//" without ":" stays under analysis
                # with the card risk. CLARIFICATION_1: the scheme sets
                # url_context_flag, which downstream may use ONLY to raise
                # scrutiny, never to lower risk.
                eff_risk = sc.risk_level
                url_ctx = False
                scheme_neut = False
                if seq == "//" and idx >= 2 and text[idx - 1] == ":" \
                        and _valid_scheme_before(text, idx - 1):
                    eff_risk = RiskLevel.NONE  # an enum, NOT the string "NONE" —
                    # RiskLevel.max()/order.index() requires an enum member;
                    # a string would crash with ValueError when aggregating
                    # several sequence matches (CODE_REVIEW Q4, found by 6 reviewers)
                    url_ctx = True             # marks URL mode for @/dot
                    scheme_neut = True
                matches.append(SequenceMatch(
                    sc_id=sc.sc_id,
                    sequence=seq,
                    name=("url_scheme_authority_separator" if scheme_neut else sc.name),
                    risk_level=eff_risk,
                    candidate_source_card=card.codepoint,
                    match_start=idx,
                    match_end=end,
                    url_context_flag=url_ctx,
                    scheme_neutralized=scheme_neut,
                ))
                claimed.append((idx, end))
            start = idx + 1
    matches.sort(key=lambda m: (m.match_start, -(m.match_end - m.match_start)))
    return matches


def _attach_source_offsets(matches: list, sign_statuses: list) -> None:
    """PATCH_25: per match — which single signs (by their
    SIGN_OFFSET) fell into [match_start, match_end).
    Fills source_sign_offsets with real data (SOURCE_SIGN_LIST),
    made possible by PATCH_23 (offset in OutputStatus)."""
    for m in matches:
        for st in sign_statuses:
            if m.match_start <= st.sign_offset_start < m.match_end:
                m.source_sign_offsets.append(st.sign_offset_start)
        m.source_sign_offsets.sort()


# ─────────────────────────────────────────────────────────────────────
# BARE-DOMAIN DETECTOR (boundary G1) — reconstructed 2026-07-12 from FIX_VERIFICATION
# reviews (six runs) used AS A REQUIREMENTS SPEC. Status: NEW_ARTIFACT,
# NOT_REVIEWED — the reviews are input, not sign-off. Two author decisions
# are fixed here in code and in foundation_layer/
# AUTHOR_DECISION_20260712_BARE_DOMAIN_DETECTOR_D-DET-1_2.md:
#
#   D-DET-1  Two or more masks in one token: remove ALL masks before the
#            domain check (not just the current one — the P6 double-mask
#            miss caught by DeepSeek-R1 and Qwen). If the remainder looks
#            like a domain → HOST.
#   D-DET-2  TLD registry unavailable: a domain-shaped token with a mask
#            raises an alarm, NOT silence; the whole run is marked DEGRADED
#            (fail-closed by BEHAVIOUR, not only by flag — the V3 concern
#            raised by 5 of 6 reviewers).
#
# ARCHITECTURAL CONSTRAINT (ARCH_DECISION_HOMOGLYPH_VIA_CARD_ONLY): the set
# of mask characters is taken from the cards (SIGN_RELATIONS -> visible_form),
# never hardcoded. See run_mask_chars in _assess_relation_risk.
#
# FIX_FIRST round 1 (2026-07-12): _domain_prefix rewritten from a block-list
# (_STRIP_OUTER, a fixed punctuation set) to a positive character allow-list.
# Three reviewers found the block-list bypass — see _domain_prefix's own
# docstring and foundation_layer/AUTHOR_DECISION_20260712_BARE_DOMAIN_
# DETECTOR_FIX_FIRST_ROUND1.md, including AUTHOR_DECISION D-DET-3
# (concatenation false positives documented, not fixed) and two v0.5 tails.
#
# FIX_FIRST round 2 (2026-07-12): the narrow-circle review of round 1 found
# that the positive scan skipped a LEADING structural separator as if it
# were a wrapper (@example.com, /example.com mis-read as bare domains).
# AUTHOR_DECISION D-DET-4: leading / \\ ? # : @ are a HARD_STOP. Same round
# corrected the "any script" docstring wording (combining marks fail
# isalnum() — a pre-existing limitation) and added the mask-after-domain
# concatenation FP as a D-DET-3 addendum. See FIX_FIRST_ROUND2.md.
# ─────────────────────────────────────────────────────────────────────

# TLD registry state (lazy, once per process). Health check mirrors the
# reviews: a set with >= _TLD_MIN_HEALTHY entries is trusted; anything
# smaller/broken is DEGRADED (D-DET-2). load_single_tlds() itself already
# has a three-level fallback (live -> cache -> embedded ~200 entries), so
# DEGRADED only fires on a genuinely empty/corrupt registry.
_TLD_SET = None
_TLD_SOURCE_DEGRADED = False
_TLD_MIN_HEALTHY = 100


def _tlds():
    """Returns (frozenset_of_tlds, degraded_bool). Cached for the process
    lifetime — the caller must not fetch on every mask."""
    global _TLD_SET, _TLD_SOURCE_DEGRADED
    if _TLD_SET is None:
        try:
            entries, _source = load_single_tlds()
        except Exception:
            entries = frozenset()
        if not isinstance(entries, (set, frozenset)) or len(entries) < _TLD_MIN_HEALTHY:
            _TLD_SET = frozenset(entries) if isinstance(entries, (set, frozenset)) else frozenset()
            _TLD_SOURCE_DEGRADED = True
        else:
            _TLD_SET = frozenset(entries)
            _TLD_SOURCE_DEGRADED = False
    return _TLD_SET, _TLD_SOURCE_DEGRADED


def _force_tld_state_for_test(tld_set, degraded: bool) -> None:
    """Test hook only: pin the TLD registry state so a gate can exercise
    the DEGRADED path (D-DET-2) without touching the network."""
    global _TLD_SET, _TLD_SOURCE_DEGRADED
    _TLD_SET = frozenset(tld_set)
    _TLD_SOURCE_DEGRADED = bool(degraded)


def _reset_tld_state_for_test() -> None:
    """Test hook only: drop the cache so the next _tlds() reloads live."""
    global _TLD_SET, _TLD_SOURCE_DEGRADED
    _TLD_SET = None
    _TLD_SOURCE_DEGRADED = False


def _demask(s: str, mask_chars) -> str:
    """D-DET-1: remove EVERY mask character from s (all occurrences, all
    declared masks — not only the current one). mask_chars comes from the
    cards, never hardcoded.

    NOTE (documented boundary, not silently narrowed): the only masks in
    the system today are structural separators (fullwidth solidus U+FF0F),
    which a real domain string cannot contain — deleting them reconstructs
    the domain. Should a LETTER-homoglyph mask ever be carded (e.g. a
    Cyrillic letter masquerading as Latin 'o'), blanket deletion would
    corrupt the label and D-DET-1 would need a follow-up AUTHOR_DECISION
    (delete vs. canon substitution). Flagged in the foundation doc as an
    open item."""
    if not mask_chars:
        return s
    return "".join(ch for ch in s if ch not in mask_chars)


# F-NEW-1 (P0, 2026-07-13): a SECOND, NON-carded invisible next to the carded
# mask (goog<ZWSP><ZWJ>le.com) used to survive _demask — which strips only
# CARDED masks — and then trip _looks_like_domain on the residual invisible, so
# the label read as "not a domain" -> FREE_TEXT -> a SILENTLY MISSED phishing
# host. The trivial bypass: append any second invisible after the ZWSP.
#
# The trap (yesterday's finding): DEFAULT_IGNORABLE != SAFE_TO_DELETE. We must
# NOT blindly delete all invisibles — a blanket strip would corrupt legitimate
# Persian ZWNJ orthography and ZWJ emoji sequences. So the rule is narrow:
#   - an invisible INSIDE a reconstructed domain label is anomalous by its mere
#     PRESENCE (whatever it is, carded or not) -> strip it ONLY to SEE the real
#     domain for the "is this a host?" test;
#   - we NEVER delete it from the text; the uncarded ones are still surfaced as
#     witnesses by the registrar (msl_mip_runtime);
#   - this predicate runs ONLY inside _detect_context_at, which is reached ONLY
#     for a carded-mask relation candidate (a ZWSP/mask is already present).
#     Emoji/Persian text with NO carded mask never enters this path -> untouched.
_BIDI_CONTROL_CLASSES = {"LRE", "RLE", "LRO", "RLO", "PDF",
                         "LRI", "RLI", "FSI", "PDI"}
# Non-Cf Default_Ignorable ranges that can still hide in a label (stable set;
# Cf is handled by the category check). Matches the registrar's approximation.
_DI_EXTRA_RANGES = ((0x034F, 0x034F), (0x115F, 0x1160), (0x17B4, 0x17B5),
                    (0x180B, 0x180F), (0x3164, 0x3164), (0xFE00, 0xFE0F),
                    (0xFFA0, 0xFFA0), (0xE0100, 0xE01EF))


def _is_domain_label_invisible(ch: str) -> bool:
    """True if ch is an invisible / zero-advance code point that can hide
    INSIDE a domain label (F-NEW-1). Ordinary whitespace is EXCLUDED on
    purpose: it already splits tokens and U+0020 must never be treated as a
    hidden mask (the N1 witness-flood guard). Extended predicate = Cf +
    bidi-control + Default_Ignorable-extra + braille-blank; deliberately WIDER
    than the current registrar witness predicate so a not-yet-carded gap (e.g.
    braille U+2800) cannot re-open the missed-attack hole while F-NEW-3 is
    still pending."""
    if ch.isspace():
        return False
    if unicodedata.category(ch) == "Cf":
        return True
    if unicodedata.bidirectional(ch) in _BIDI_CONTROL_CLASSES:
        return True
    if ch == "⠀":   # BRAILLE PATTERN BLANK (So) — renders empty
        return True
    cp = ord(ch)
    return any(lo <= cp <= hi for lo, hi in _DI_EXTRA_RANGES)


def _strip_label_invisibles(s: str) -> str:
    """Strip domain-label invisibles for RECONSTRUCTION ONLY (see the predicate
    note above). Never used to mutate the source text."""
    return "".join(ch for ch in s if not _is_domain_label_invisible(ch))


def _has_alnum(s: str) -> bool:
    """A side of the mask is 'content-bearing' iff it has at least one
    alphanumeric char (F-NEW-2 root 2A). Deliberately NOT '== a full domain':
    a real in-label mask (goog<mask>le.com) has halves ('goog', 'le.com') where
    neither half is a domain on its own, yet the concat IS one."""
    return any(ch.isalnum() for ch in s)


# D-DET-4 (FIX_FIRST round 2, 2026-07-12): a LEADING structural separator
# is not a wrapper. The positive scan below skips leading non-domain
# characters to see past wrappers ((, ", *, …); but /, \, ?, #, :, @ carry
# structural meaning (path, query, fragment, port, authority/email), and
# silently skipping them made "@example.com", "/example.com" etc. mis-read
# as bare domains (FREE_TEXT -> PATH). These are a HARD_STOP: hit one before
# the domain block starts and the token has no bare-domain prefix at all.
# This is NOT a return to the block-list — punctuation is unbounded, but the
# set of structural separators is closed and already meaningful in the spec.
_LEADING_STRUCTURAL_STOPS = frozenset("/\\?#:@")


def _domain_prefix(token: str) -> str:
    """POSITIVE extraction (FIX_FIRST 2026-07-12, blocker — three reviewers
    found the bypass in the first conveyor round): return the first maximal
    run of domain-shaped characters in the token — a character for which
    str.isalnum() is True (any Unicode letter or digit, so IDN labels such
    as a Cyrillic homoglyph attack still match — this is the thing we WANT
    to catch, not exclude), plus '-' and '.' — and discard everything
    outside that run.

    PRECISION (a reviewer caught the docstring lying): "isalnum() is True"
    is NOT the same as "any letter of any script". Unicode COMBINING MARKS
    (categories Mn/Mc) return isalnum()=False — e.g. U+093E DEVANAGARI VOWEL
    SIGN AA, Arabic diacritics, Hebrew niqqud, NFD-decomposed Latin. So an
    IDN label carrying such a mark (भारत.भारत, …) has its run cut at the
    mark and is dropped -> FREE_TEXT. This is a PRE-EXISTING limitation, not
    a regression (the old block-list left the mark in the string but the
    per-label isalnum-or-hyphen check then rejected it just the same);
    documented, deferred (see the gate case and FIX_FIRST_ROUND1). Closing
    it needs proper IDNA/NFC canonicalisation of the whole candidate, out of
    this rough detector's scope.

    Replaces the old block-list approach (strip a fixed punctuation set,
    _STRIP_OUTER, off the token's outer edges). A block list only ever
    covers the punctuation someone thought to enumerate: markdown '*', an
    em dash, a tilde, a pipe, a fullwidth quotation mark and any other
    wrapping character NOT in that specific list stuck to the domain,
    made a label fail the isalnum-or-hyphen check in _looks_like_domain,
    and silently downgraded a real HOST mask to FREE_TEXT (a fullwidth-
    solidus mask domain wrapped in asterisks bypassed detection this way
    — the asterisks were never in _STRIP_OUTER; see the gate for the
    literal example). A positive allow-list closes the whole class at
    once instead of chasing individual punctuation marks.

    D-DET-4 (round 2) originally HARD-STOPPED here (returned "" on a leading
    / \\ ? # : @) so '@example.com/x' would not read as a bare domain. FIX_
    FIRST round 3 (blocker 1) MOVED that logic up into _detect_context_at:
    the hard-stop-to-"" also silenced a domain-WITH-mask after the prefix
    ('#goog<mask>le.com' -> FREE_TEXT, a real bypass). _domain_prefix is back to
    pure positive extraction (leading non-domain chars, structural or not,
    are skipped); _detect_context_at now remembers whether a LEADING
    structural separator was present and uses it ONLY to demote the mask-
    after-domain PATH case to FREE_TEXT — never to suppress a HOST.

    This also subsumes the old separate 'cut at the first /, ?, #, :,
    space' step (P5): none of those characters are in the allow-list, so
    the scan stops there on its own — no separate pass needed.

    Deliberately NOT trimmed here (known, deferred — see AUTHOR_DECISION
    D-DET-3 / FIX_FIRST_ROUND1 in foundation_layer): a leading/trailing
    hyphen on the extracted run (RFC-invalid but not rejected — v0.5
    tail), and the concatenation false positives this positive scan can
    itself produce when two unrelated fragments glue into a domain-shaped
    string once the mask is removed."""
    token = token.strip()
    n = len(token)
    i = 0
    while i < n and not (token[i].isalnum() or token[i] in ".-"):
        i += 1
    j = i
    while j < n and (token[j].isalnum() or token[j] in ".-"):
        j += 1
    return token[i:j]


def _is_tld(label: str, tld_set, degraded: bool) -> bool:
    """P2 (IDN): a label is a TLD if it is in the registry directly OR its
    punycode A-label is (an IDN ccTLD label -> its A-label, e.g. xn--p1ai).
    D-DET-2: when the registry is
    DEGRADED, accept a TLD-SHAPED label (alphabetic, 2..63) rather than go
    silent — alarm, not miss."""
    label = label.lower()
    if label in tld_set:
        return True
    try:
        alabel = label.encode("idna").decode("ascii").lower()
        if alabel in tld_set:
            return True
    except Exception:
        pass
    if degraded:
        return label.isalpha() and 2 <= len(label) <= 63
    return False


# Blocker 2 (FIX_FIRST round 3): fullwidth / ideographic domain-separator
# dots canonicalised to ASCII '.' before label analysis. The masked target
# is itself a fullwidth character (／ = U+FF0F), so an attacker naturally
# pairs it with a fullwidth full stop (．U+FF0E), an ideographic full stop
# (。U+3002) or its halfwidth form (｡U+FF61). NFKC maps all three to '.';
# without this the positive scan stops at the fullwidth dot and the domain
# is dropped -> FREE_TEXT. Applied to the candidate BEFORE the '.' split.
_DOMAIN_DOT_CANON = {"。": ".", "．": ".", "｡": "."}


def _canon_domain_seps(s: str) -> str:
    for k, v in _DOMAIN_DOT_CANON.items():
        if k in s:
            s = s.replace(k, v)
    return s


def _looks_like_domain(raw: str, tld_set, degraded: bool) -> bool:
    """A string looks like a bare domain: >= 2 labels, each a valid DNS
    label (alnum or '-', non-empty, <= 63 chars), last label a TLD. The
    tail (path/port/query) is trimmed by _domain_prefix first (P5).
    Fullwidth/ideographic dots are canonicalised to '.' first (Blocker 2)."""
    raw = _canon_domain_seps(raw)
    s = _domain_prefix(raw)
    if not s:
        return False
    labels = s.strip(".").split(".")
    if len(labels) < 2:
        return False
    for lbl in labels:
        if not lbl or len(lbl) > 63:
            return False
        if not all(ch.isalnum() or ch == "-" for ch in lbl):
            return False
    return _is_tld(labels[-1], tld_set, degraded)


def _is_byte_exact_token(s: str) -> bool:
    """Level 1: a no-space word that would go to an EXACT (byte-for-byte)
    comparison — an identifier, a keyword, a handle. An invisible/mask break
    inside it silently defeats that comparison. Requirements: length >= 2,
    only [alnum / '-' / '_'], NO dot (a dotted thing is a domain, handled
    above), and at least one LETTER (a pure-digit run like a CJK date
    '20260711' is not a token going to exact compare -> stays FREE_TEXT)."""
    if len(s) < 2 or "." in s:
        return False
    if not all(ch.isalnum() or ch in "-_" for ch in s):
        return False
    return any(ch.isalpha() for ch in s)


def _detect_context_at(text: str, offset: int, mask_chars=frozenset()) -> str:
    """Context detector around the mask position (step 4, D2): URL / HOST /
    EMAIL / PATH / BYTE_EXACT_TOKEN / FREE_TEXT.

    Two passes:
      1. SCHEME (P4): a 'scheme://' is honoured ONLY inside the mask's own
         whitespace-delimited token, before the mask — a 'http://' earlier
         in the sentence (a different token) must not lower a later bare
         mask.
      2. BARE DOMAIN (boundary G1): no scheme in the token — reconstruct
         the domain by removing ALL masks (D-DET-1) and test the mask's sides.

    mask_chars — the mask alphabet for this run, sourced from the cards
    (SIGN_RELATIONS visible_form), never hardcoded."""
    # token = the whitespace-delimited unit that contains the mask
    left_bound = offset
    while left_bound > 0 and not text[left_bound - 1].isspace():
        left_bound -= 1
    right_bound = offset
    while right_bound < len(text) and not text[right_bound].isspace():
        right_bound += 1
    token = text[left_bound:right_bound]
    rel = offset - left_bound  # mask index inside the token

    # --- Pass 1: SCHEME_SCOPE (P4) — scheme only inside THIS token ---
    # Structure FIRST (F-NEW-4), then userinfo ON the structure (F-NEW-5).
    scheme_at = token.rfind("://", 0, rel)
    if scheme_at != -1:
        after = token[scheme_at + 3:]
        rel_s = rel - (scheme_at + 3)
        # F-NEW-4 — split the URL into components:
        #   scheme://authority/path?query#fragment
        # The AUTHORITY ends at the FIRST of / ? # (RFC 3986). '@' is NOT a
        # component delimiter here — it lives INSIDE the authority (userinfo@host).
        host_end = len(after)
        for sep in ("/", "?", "#"):
            p = after.find(sep)
            if p != -1:
                host_end = min(host_end, p)
        if 0 <= rel_s < host_end:
            # Mask is in the AUTHORITY. F-NEW-5 — userinfo@host: per RFC 3986 the
            # host is after the LAST '@' in the authority; a mask BEFORE the last
            # '@' sits in the USERINFO (identity region), not the host. The '@' is
            # scoped to authority[:host_end] ONLY — a '@' in path/query is a
            # different '@' (already separated by the component split). Schemeless
            # user@domain is EMAIL (Pass 2) and never reaches this branch.
            authority = after[:host_end]
            at = authority.rfind("@")
            if at != -1 and rel_s <= at:
                return "USERINFO"
            return "HOST"
        # Past the authority — which component holds the mask? A fragment '#'
        # outranks a query '?' (a '?' AFTER the first '#' is part of the fragment).
        frag_at = after.find("#")
        q_at = after.find("?")
        if frag_at != -1 and q_at > frag_at:
            q_at = -1
        if frag_at != -1 and rel_s > frag_at:
            return "FRAGMENT"
        if q_at != -1 and rel_s > q_at:
            return "QUERY_VALUE"
        return "PATH"

    # --- Pass 2: BARE DOMAIN (boundary G1), no scheme in the token ---
    tld_set, degraded = _tlds()

    # Blocker 1 (FIX_FIRST round 3): a LEADING structural separator
    # (/ \ ? # : @) is not part of a bare domain, but it must NOT blank the
    # whole token — a domain-WITH-mask AFTER the prefix is still the attack
    # (#goog<mask>le.com -> HOST). Strip a leading non-domain prefix, remember
    # whether it contained a structural separator, and use that ONLY to
    # demote the mask-after-domain PATH case to FREE_TEXT (D-DET-4's
    # conservative call for '#example.com／x') — never to suppress a HOST.
    had_leading_structural = False
    lead = 0
    while lead < rel and not (token[lead].isalnum() or token[lead] in ".-"):
        if token[lead] in _LEADING_STRUCTURAL_STOPS:
            had_leading_structural = True
        lead += 1

    left_part = _demask(token[lead:rel], mask_chars)   # D-DET-1: strip ALL masks,
    right_part = _demask(token[rel + 1:], mask_chars)  # not only the current one
    whole = _demask(token[lead:], mask_chars)          # the token with ALL masks gone

    # F-NEW-1 (P0): after removing carded masks, ALSO strip any residual
    # label-invisible for the RECONSTRUCTION checks below, so a second hidden
    # char (ZWJ / U+2062 / braille) cannot silently defeat host/email/token
    # detection. No-op when nothing residual survives (single-mask cases keep
    # their exact prior behaviour); the chars are NOT removed from the text.
    left_part = _strip_label_invisibles(left_part)
    right_part = _strip_label_invisibles(right_part)
    whole = _strip_label_invisibles(whole)

    # host substitution — a domain on BOTH sides of the mask
    # (a.com<mask>evil.com, incl. tails via _domain_prefix in _looks_like_domain)
    if _looks_like_domain(left_part, tld_set, degraded) \
            and _looks_like_domain(right_part, tld_set, degraded):
        return "HOST"
    # F-NEW-2 root 2A (P1 leading / P2 trailing): a hidden zero-width at the
    # very START or END of a domain-shaped token is PADDING (defeats a
    # byte-exact match of the domain), NOT a label break -> not HOST/HIGH. But
    # removing the false HIGH must NOT open a silent PASS (the padding would slip
    # through) -> a MEDIUM fallback, never pass. The padding tell: the whole
    # reconstructs to a domain, yet one side of the mask is empty/blank (no
    # alnum). A genuine in-label mask (goog<ZWSP>le.com) has alnum on BOTH
    # sides, so it is NOT caught here.
    if _looks_like_domain(whole, tld_set, degraded) \
            and not (_has_alnum(left_part) and _has_alnum(right_part)):
        return "HIDDEN_BOUNDARY_PADDING"
    # mask inserted INSIDE one domain (goog<mask>le.com -> google.com). D-DET-1
    # makes the double-mask goog<mask>le.<mask>com collapse to google.com too.
    # F-NEW-2 root 2B (P4 after-domain / P5 deep-path): DOMAIN_PREFIX_FOUND !=
    # SIGN_IS_INSIDE_DOMAIN. A leading domain prefix in the reconstruction does
    # NOT mean the mask broke the host — the mask may sit in the path. Bind it
    # to POSITION: the mask lands at index len(left_part) in the reconstruction
    # (the mask char itself is removed); fire HOST only if that index is INSIDE
    # the host label span [.. host_end). At/after host_end the mask is in the
    # path/tail -> fall through to PATH. This (the "host-span" form) also keeps
    # the multi-label case honest: www.example.com<mask>.evil.com reconstructs
    # to ONE longer host, the mask is inside it -> still HOST (a simpler
    # "left is not itself a domain" test would wrongly drop that one). Both
    # sides must be content-bearing (2A handles an empty side above).
    if _has_alnum(left_part) and _has_alnum(right_part):
        recon = left_part + right_part
        if _looks_like_domain(recon, tld_set, degraded):
            host = _domain_prefix(recon)
            host_end = recon.find(host) + len(host)
            if len(left_part) < host_end:
                return "HOST"
    # EMAIL (Level 1): local@domain with the mask anywhere -> the mask breaks
    # exact matching of an identity token (user<mask>name@example.com).
    if "@" in whole:
        at = whole.rfind("@")
        local, dom = whole[:at], whole[at + 1:]
        if local and _looks_like_domain(dom, tld_set, degraded):
            return "EMAIL"
    # a domain then the mask opens a tail -> path segment (readme.md<mask>x);
    # a LEADING structural separator demotes this PATH to FREE_TEXT (D-DET-4).
    if _looks_like_domain(left_part, tld_set, degraded):
        return "FREE_TEXT" if had_leading_structural else "PATH"
    # BYTE_EXACT_TOKEN (Level 1): a no-space word that goes to an exact compare
    # (bad<mask>word, user<mask>name). The mask silently breaks the match. We
    # cannot tell a keyword from an identifier from a bare string (that finer
    # CODE/IDENTIFIER split is deferred — see the card KNOWN_OPEN), so we name
    # the honest generic and surface it.
    if _is_byte_exact_token(whole):
        return "BYTE_EXACT_TOKEN"
    return "FREE_TEXT"


# FRAMING: this is a WITNESS, not a judge. Every level here maps to a
# RECOMMENDATION surfaced to the human (HIGH -> "hold, look"; MEDIUM ->
# "queue, look"), never to an automatic block. HOST (a domain break) is the
# one unambiguous case -> HIGH. EMAIL / BYTE_EXACT_TOKEN / PATH are contexts
# where an invisible break DEFEATS exact matching but we cannot be sure it is
# malicious (an identifier, a keyword, a soft-wrapped displayed URL) -> we
# SURFACE them at MEDIUM rather than assert HIGH. PATH specifically: ZWSP in a
# DISPLAYED url (soft-wrap) is legitimate, in a MACHINE path it is suspect;
# we cannot tell display from machine from the string, so PATH stays MEDIUM.
_SCOPE_RISK = {
    "HOST": RiskLevel.HIGH,             # host / domain break — the unambiguous case
    "EMAIL": RiskLevel.MEDIUM,          # identity token exact-match; surfaced, not judged
    "BYTE_EXACT_TOKEN": RiskLevel.MEDIUM,  # no-space word going to exact compare; can't tell keyword vs identifier -> surface
    "URL": RiskLevel.MEDIUM,
    "PATH": RiskLevel.MEDIUM,           # display (soft-wrap) vs machine ambiguity -> not HIGH (Z4-05)
    # F-NEW-4/5 URL components: an invisible break in a query/fragment/userinfo
    # defeats exact matching of that value but is not a host-label break -> MEDIUM,
    # never a silent pass (URL alone used to fall out of scope -> NONE).
    "QUERY_VALUE": RiskLevel.MEDIUM,
    "FRAGMENT": RiskLevel.MEDIUM,
    "USERINFO": RiskLevel.MEDIUM,
    # F-NEW-2 root 2A: a hidden zero-width padding a whole domain at its edge —
    # not a label break (not HIGH), but a real evasion of byte-exact matching
    # that must be surfaced, never a silent pass -> MEDIUM.
    "HIDDEN_BOUNDARY_PADDING": RiskLevel.MEDIUM,
    "FREE_TEXT": RiskLevel.NONE,
}


def _downgrade(level: RiskLevel) -> RiskLevel:
    """A CANDIDATE edge downgrades risk by one step (D1): an
    unverified relation must not hit as hard as VERIFIED."""
    order = [RiskLevel.NONE, RiskLevel.LOW, RiskLevel.MEDIUM,
             RiskLevel.HIGH, RiskLevel.CRITICAL]
    i = order.index(level)
    return order[max(0, i - 1)]


# Level 2 (finding S-03): a RELATION_TYPE must be a CONTRACT, not a label.
# runtime_role says what a type actually DOES at runtime, honestly:
#   PRIMARY          — emits an INDEPENDENT risk verdict (context-driven).
#   SUPPORTING_FACET — evidence attached to a primary; does NOT emit a second
#                      independent risk on the same sign+context (removes the
#                      Z1 duplicate: ABSENCE_CONFUSABLE no longer double-HIGHs).
#   TAXONOMY_ONLY    — the type is a described distinction whose runtime check
#                      does NOT yet exist (e.g. INVISIBLE_CLASS_COLLISION: a
#                      COARSE external filter's "zero-width allowed" behaviour
#                      is NOT observable from the input string). Carried and
#                      surfaced, but does not drive risk — not passed off as a
#                      working contract.
# Legacy mimicry types (the ／ mask edge) are PRIMARY -> unchanged behaviour.
_RELATION_RUNTIME_ROLE = {
    "BOUNDARY_DISRUPTOR": "PRIMARY",
    "ABSENCE_CONFUSABLE": "SUPPORTING_FACET",
    "INVISIBLE_CLASS_COLLISION": "TAXONOMY_ONLY",
    "CONFUSABLE_OF": "PRIMARY",
    "NFKC_MAPS_TO": "PRIMARY",
    "VISUAL_MIMIC_OF": "PRIMARY",
    "": "PRIMARY",   # no declared type (legacy) -> primary
}


def _assess_relation_risk(text: str, sign_statuses: list) -> list:
    """STAGE_6b: verdict per active mask (D-REL-4/6).
    Barrier N3: read ONLY active_relation_candidates."""
    verdicts = []
    # ARCH constraint: the mask alphabet for this run is taken from the
    # cards (SIGN_RELATIONS -> visible_form), never hardcoded. D-DET-1
    # strips exactly these characters when reconstructing a bare domain.
    run_mask_chars = frozenset(
        c.get("visible_form", "")
        for st in sign_statuses
        for c in getattr(st, "active_relation_candidates", [])
        if c.get("visible_form")
    )
    _, tld_degraded = _tlds()  # D-DET-2: run-level DEGRADED signal
    for st in sign_statuses:
        for cand in getattr(st, "active_relation_candidates", []):
            offset = cand.get("at_offset", 0)
            scope_of_edge = set(cand.get("context_scope", []))
            rtype = cand.get("relation_type", "")
            # M4-precondition: an UNKNOWN relation_type must NOT default to
            # PRIMARY (the old dangerous default — an unrecognised type would
            # then emit an INDEPENDENT risk verdict). It maps to INVALID_EDGE:
            # no independent risk, surfaced as an integrity concern. (In
            # practice load_card already marks unknown types invalid and they
            # are filtered upstream; this is defence-in-depth at the seam.)
            role = _RELATION_RUNTIME_ROLE.get(rtype, "INVALID_EDGE")
            ctx = _detect_context_at(text, offset, run_mask_chars)

            # PROTECTED_CONTEXT: the real context is in the edge scope
            # (or the edge is ANY). Otherwise the mask is out of scope.
            protected = ("ANY" in scope_of_edge) or (ctx in scope_of_edge)
            # Level 2: ONLY a PRIMARY type emits an independent risk. A
            # SUPPORTING_FACET or a TAXONOMY_ONLY type is recorded (its
            # context/protected are computed for provenance) but does NOT add
            # a second verdict-driving risk on the same sign.
            if role == "PRIMARY" and protected and ctx != "FREE_TEXT":
                risk = _SCOPE_RISK.get(ctx, RiskLevel.MEDIUM)
            else:
                risk = RiskLevel.NONE  # RELATION_FOUND != THREAT

            # verification_status of the edge as a modifier (D1)
            if cand.get("verification_status", "").upper() == "CANDIDATE" \
                    and risk != RiskLevel.NONE:
                risk = _downgrade(risk)

            verdicts.append({
                "visible_form": cand.get("visible_form", ""),
                "target": cand.get("target", ""),
                # Level 3 (Z3-02): NO silent "CODEPOINT" fallback at this seam.
                # module_engine always carries target_kind; an empty value here
                # is surfaced as-is, never quietly migrated to CODEPOINT.
                "target_kind": cand.get("target_kind", ""),
                "relation_type": rtype,       # honest type visible (D-INV-1)
                "runtime_role": role,         # Level 2: PRIMARY/SUPPORTING_FACET/TAXONOMY_ONLY
                "at_offset": offset,
                "detected_context": ctx,
                "protected": protected,
                "risk_level": risk.value,
                "canon_hypothesis": None,  # probe deferred (D3)
                "relation_id": cand.get("relation_id", ""),
                "tld_source_degraded": tld_degraded,  # D-DET-2
            })
    return verdicts


def process_sequence(text: str, cards: list,
                     sign_statuses: list = None,
                     known_signs: set = None) -> SequenceOutput:
    """The full STAGE_1-7 of the sequence layer.

    text          — the source text (same as fed to module_engine)
    cards          — the SignCoreCards actually involved
                     (CARD_SET, PATCH_26); usually the cards whose signs
                     are present in the text
    sign_statuses  — the OutputStatus list from module_engine (for
                     SOURCE_SIGN_LIST); optional
    known_signs    — the FULL registry of visible_forms of all
                     SIGN_CORE_CARDs known to the system (not just cards).
                     Closes the CARD_SET_COMPLETENESS gap (found in
                     code review, 2026-06-29): without this parameter,
                     if the caller passed an incomplete CARD_SET
                     (e.g. forgot DOT), the dots in SOLIDUS.SC3 "../"
                     were wrongly treated as "external context" and
                     matched without validation. In the production
                     runtime (msl_mip_runtime.py) pass the registry
                     of ALL loaded system cards here, not only this
                     call's cards.
                     Default None — for isolated single-card unit
                     tests, keeps the old behaviour.
    """
    sign_statuses = sign_statuses or []

    # --- STAGE_1: INPUT_VALIDATION ---
    if not text:
        return SequenceOutput(check_unavailable=True,
                              warnings=["EMPTY_TEXT"])
    if not cards:
        return SequenceOutput(check_unavailable=True,
                              warnings=["NO_CARDS_IN_SET"])

    # --- STAGE_2: CARD_SET_DETERMINATION (PATCH_26) ---
    card_set = [c.codepoint for c in cards]

    # FIXED (found in code review, 2026-06-29, Grok): the
    # sequence layer used not to check card document_status in
    # CARD_SET at all — a WORKING_DRAFT card silently participated
    # in sequence search with no signal that its result is
    # unreliable (unlike module_engine, where such a warning is
    # mandatory). The sequence layer now warns honestly too,
    # without blocking.
    _CONFIRMED_STATUSES = {"WORKINGLY_CLOSED", "ARTIFACT_CONFIRMED"}
    draft_cards = [
        c for c in cards
        if c.document_status not in _CONFIRMED_STATUSES and c.visible_form in text
    ]
    draft_warnings = [
        f"CARD_NOT_CONVEYOR_REVIEWED: {c.card_uid or c.codepoint} "
        f"(status={c.document_status}) actually occurs in the text — "
        f"sequence results involving this sign are unreliable"
        for c in draft_cards
    ]

    # --- STAGE_6b: RELATION_RISK (step 4, D-REL-4/6) — BEFORE the pool ---
    # The mask verdict does not depend on the normal candidate pool: a
    # mask is itself a reason to analyse. Barrier N3: only active ones.
    relation_verdicts = _assess_relation_risk(text, sign_statuses)

    # D-DET-2: mark the whole run DEGRADED when a bare-domain mask verdict
    # was computed against an unavailable TLD registry (fail-closed by
    # behaviour, not only by flag). The warning is honest, non-blocking.
    degraded = any(v.get("tld_source_degraded") for v in relation_verdicts)
    if degraded:
        draft_warnings.append(
            "TLD_SOURCE_DEGRADED: the single-TLD registry is unavailable; "
            "bare-domain mask verdicts were computed fail-closed (TLD-shaped "
            "labels accepted UNVERIFIED — alarm, not silence). Treat HOST/PATH "
            "verdicts on bare domains as provisional (D-DET-2)."
        )

    # --- STAGE_2a: CANDIDATE_POOL (PATCH_26) ---
    pool = _build_candidate_pool(cards)
    if not pool:
        return SequenceOutput(card_set=card_set, check_unavailable=True,
                              warnings=["EMPTY_CANDIDATE_POOL"] + draft_warnings,
                              relation_verdicts=relation_verdicts,
                              degraded=degraded)

    # The set of positions that actually passed single-sign validation.
    # Each OutputStatus covers [sign_offset_start, sign_offset_end).
    # When statuses are provided, strict match validation is on
    # (Ghost Matching fix): a candidate is accepted only when all its
    # positions are validated. No statuses -> text mode.
    validated_offsets = None
    strict = False
    if sign_statuses:
        validated_offsets = set()
        for st in sign_statuses:
            for pos in range(st.sign_offset_start, st.sign_offset_end):
                validated_offsets.add(pos)
        strict = True

    # --- STAGE_3-4: MATCHING + adjacency + validation ---
    card_signs = {c.visible_form for c in cards}
    matches = _find_literal_matches(text, pool, validated_offsets, card_signs,
                                    strict, known_signs)

    # --- STAGE_5: SOURCE_SIGN_LIST / SOURCE_OCCURRENCE_LIST (PATCH_25) ---
    _attach_source_offsets(matches, sign_statuses)
    source_sign_list = sorted({st.sign_offset_start for st in sign_statuses})

    # --- STAGE_6: MULTIPLE_MATCHES (PATCH_26) ---
    multiple = len(matches) > 1

    # FIXED (found in code review, 2026-06-29, GPT-5.5): the
    # "card visible_form in text" check misses a rare but real
    # case — a WORKING_DRAFT card declares a SEQUENCE_CANDIDATE
    # that does NOT contain that card's visible_form (e.g. a
    # hypothetical card declares the "://" candidate without its
    # own sign inside). Such a match will really fire, but the
    # "visible_form in text" warning will not appear. A second,
    # independent check: if the match came from an unreviewed
    # card, the warning must appear regardless of the first
    # check.
    draft_codepoints = {c.codepoint for c in cards
                        if c.document_status not in _CONFIRMED_STATUSES}
    matched_draft = {m.candidate_source_card for m in matches
                     if m.candidate_source_card in draft_codepoints}
    already_warned = {c.codepoint for c in draft_cards}
    for cp in matched_draft - already_warned:
        draft_warnings.append(
            f"CARD_NOT_CONVEYOR_REVIEWED_MATCHED_SEQUENCE_SOURCE: "
            f"{cp} — an unreviewed card became a match source "
            f"in SEQUENCE although its visible_form is not directly in the text"
        )

    # --- STAGE_7: OUTPUT_ASSEMBLY ---
    # relation_verdicts computed above (STAGE_6b, before the pool).
    return SequenceOutput(
        card_set=card_set,
        matches=matches,
        multiple_matches=multiple,
        source_sign_list=source_sign_list,
        source_occurrence_list="NOT_AVAILABLE",  # honest stub (PATCH_25)
        check_unavailable=False,
        warnings=draft_warnings,
        relation_verdicts=relation_verdicts,
        degraded=degraded,
    )
