# ARCH_DECISION: HOMOGLYPH ENTERS ONLY VIA A CARD (discipline)

**Status:** AUTHOR_DECISION (accepted)
**Date:** 2026-07-07
**Decision author:** Ruslan Malyavsky (AUTHOR_DECISION_STATUS_AUTHORITY)
**Type:** disciplinary principle (not implementation mechanics)

---

## PRINCIPLE

A sign — including a homoglyph (a look-alike sign: ／ instead of /,
Cyrillic instead of Latin, fullwidth, etc.) — has NO right to appear in
a module next to a genuine sign while bypassing:
1. a sign card,
2. Unicode verification (NFKC / UTS#39 skeleton),
3. the conveyor,
4. AUTHOR_DECISION.

**No signs "on the fly." No back door into validated_offsets via code.**

## WHAT THIS RESOLVES (the reviewers' split on the norm layer)

The NORMALIZATION_LAYER_DESIGN run produced a split:
- CAMP 1: `if ch in cards OR NFKC(ch) in cards` right in scan_signs —
  the homoglyph is added to validated_offsets by code, on the fly.
  → REJECTED. Violates discipline: admits an UNVERIFIED sign into the
    core (validated_offsets) bypassing the card and the conveyor. This
    is exactly the FALSE_TRUST the whole project stands against.
- CAMP 2: a separate confusable_flags structure, not in
  validated_offsets → does not violate discipline, but sequence never
  sees combinations of homoglyphs (devalues the sequence layer, which
  was BUILT to read combinations — confirmed by the sequence_engine.py
  docstring: "catch cross-card idioms ../, ://").
- AUTHOR'S DECISION (a third path, absent from the reviewers): the
  homoglyph travels the SAME path as any sign — card + verification +
  conveyor. Then it LEGALLY reaches sequence (because it has become a
  verified sign), and discipline stays intact.

## ROLE OF THE NORM LAYER (consequence)

The norm layer at runtime does NOT create signs. It only READS what has
already been verified and stored in cards. A homoglyph becomes a sign
by the ONLY legal means — through a card.

Author's analogy: sign cards are a future LIBRARY/reference (SQL-database
style). The norm layer = a CONSUMER of the library (query "whose
homoglyph is this"), not an on-the-fly sign generator. Populating the
library happens through templates and the conveyor (in perspective — by
the community following the author's standard), not via hardcode.

## WHAT IS DELIBERATELY NOT DECIDED HERE (derivative, later)

These are mechanics, decided later, WITHOUT breaking the principle above:
- homoglyph = a separate card TYPE or a FIELD in a sign card;
- a "thin" homoglyph card (inherits risk from its canonical sign +
  adds only verification), so the conveyor over it is fast;
- offset mechanics when a homoglyph reaches sequence
  (NFKC-expansion ﬁ→fi etc. — see CONVEYOR_PACKET_NORMALIZATION);
- design of the homoglyph field in the standard card template.

## FIXED UNANIMOUSLY BY REVIEW (6/6, still in force)

- FLAG_ONLY: the layer flags, does not mutate text (analyzer ≠ sanitizer).
- confusables in a card = manual OVERRIDE over the auto UTS#39 base.
- offsets are the foundation; direct text transformation is forbidden.

## RELATION

Builds on ARCH_DECISION_NORMALIZATION_LAYER.md (layer needed,
market-critical). This document refines the DISCIPLINE of a sign's entry
into that layer. Both are part of the Foundation Layer.
