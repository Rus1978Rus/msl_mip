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

from sign_core_card import SignCoreCard, RiskLevel
from sequence_output import SequenceMatch, SequenceOutput


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


def _detect_context_at(text: str, offset: int) -> str:
    """Rough context detector around the mask position (step 4, D2).
    First pass: URL / HOST / PATH. Returns a scope name or FREE_TEXT.
    HOST = between 'scheme://' and the next '/' (main gοοgle.com case).
    Cheap, string-based; full URL parsing is a separate pass."""
    before = text[:offset]
    scheme_pos = before.rfind("://")
    if scheme_pos != -1:
        after_scheme = text[scheme_pos + 3:]
        rel = offset - (scheme_pos + 3)  # mask position inside after_scheme
        next_slash = after_scheme.find("/")
        # host separators: '/', '?', '#' — end of the host part
        host_end = len(after_scheme)
        for sep in ("/", "?", "#"):
            p = after_scheme.find(sep)
            if p != -1:
                host_end = min(host_end, p)
        if 0 <= rel < host_end:
            return "HOST"
        if next_slash != -1 and rel >= next_slash:
            return "PATH"
        return "URL"
    # no scheme: is there a url-like structure a.b/c nearby
    window = text[max(0, offset - 20):offset + 20]
    if "/" in window and "." in window:
        return "URL"
    return "FREE_TEXT"


_SCOPE_RISK = {
    "HOST": RiskLevel.HIGH,     # host substitution — the main case
    "URL": RiskLevel.MEDIUM,
    "PATH": RiskLevel.MEDIUM,
    "FREE_TEXT": RiskLevel.NONE,
}


def _downgrade(level: RiskLevel) -> RiskLevel:
    """A CANDIDATE edge downgrades risk by one step (D1): an
    unverified relation must not hit as hard as VERIFIED."""
    order = [RiskLevel.NONE, RiskLevel.LOW, RiskLevel.MEDIUM,
             RiskLevel.HIGH, RiskLevel.CRITICAL]
    i = order.index(level)
    return order[max(0, i - 1)]


def _assess_relation_risk(text: str, sign_statuses: list) -> list:
    """STAGE_6b: verdict per active mask (D-REL-4/6).
    Barrier N3: read ONLY active_relation_candidates."""
    verdicts = []
    for st in sign_statuses:
        for cand in getattr(st, "active_relation_candidates", []):
            offset = cand.get("at_offset", 0)
            scope_of_edge = set(cand.get("context_scope", []))
            ctx = _detect_context_at(text, offset)

            # PROTECTED_CONTEXT: the real context is in the edge scope
            # (or the edge is ANY). Otherwise the mask is out of scope.
            protected = ("ANY" in scope_of_edge) or (ctx in scope_of_edge)
            if protected and ctx != "FREE_TEXT":
                risk = _SCOPE_RISK.get(ctx, RiskLevel.MEDIUM)
                # OBFUSCATION (D-REL-6): substituting a canon with a
                # mask in protected context — already in the risk level.
            else:
                risk = RiskLevel.NONE  # RELATION_FOUND != THREAT

            # verification_status of the edge as a modifier (D1)
            if cand.get("verification_status", "").upper() == "CANDIDATE" \
                    and risk != RiskLevel.NONE:
                risk = _downgrade(risk)

            verdicts.append({
                "visible_form": cand.get("visible_form", ""),
                "target": cand.get("target", ""),
                "at_offset": offset,
                "detected_context": ctx,
                "protected": protected,
                "risk_level": risk.value,
                "canon_hypothesis": None,  # probe deferred (D3)
                "relation_id": cand.get("relation_id", ""),
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

    # --- STAGE_2a: CANDIDATE_POOL (PATCH_26) ---
    pool = _build_candidate_pool(cards)
    if not pool:
        return SequenceOutput(card_set=card_set, check_unavailable=True,
                              warnings=["EMPTY_CANDIDATE_POOL"],
                              relation_verdicts=relation_verdicts)

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
    )
