# ARCH_DECISION: NORMALIZATION/CONFUSABLES — SEPARATE LAYER

**Status:** AUTHOR_DECISION (accepted)
**Date:** 2026-07-07
**Decision author:** Ruslan Malyavsky (AUTHOR_DECISION_STATUS_AUTHORITY)
**Type:** project-level architecture decision

---

## DECISION

Homoglyph handling and normalization (NFKC + skeleton UTS#39 over
confusables.txt) is extracted into a **SEPARATE LAYER** of the system,
NOT kept as a property of individual sign cards.

## RATIONALE (market-critical, not cosmetic)

Current model: each sign card carries its own `confusables` list
(fields `confusable_id`, `confusables` exist in core/sign_core_card.py
and core/load_card.py; filled manually).

Scaling problem: with an alphabet of N signs, the "confusables in
cards" model gives QUADRATIC complexity growth — up to N×N homoglyph
pairs maintained by hand, going stale with each Unicode release.
- 10 signs — tolerable.
- 1000 signs — up to ~10^6 pairs by hand = UNMAINTAINABLE.

Author's conclusion (2026-07-07): "if the alphabet eventually consists
of thousands of signs, confusables-in-cards will knock it out of the
market." A competitor with automatic normalization updates with one
button; manual confusables mean a thousand edits.

A separate layer gives:
- LINEAR complexity: N signs, ONE normalization layer.
- Auto-updatability via the already-built
  tools/unicode_sources_update.py (confusables.txt is already committed
  to sources/17.0.0/, card fields already exist — infrastructure is
  half-ready).
- A new sign is protected from homoglyphs automatically (normalization
  BEFORE the sign is searched), without hand-maintaining pairs.

## WHAT THIS DECISION DOES NOT YET RESOLVE (sent to conveyor)

Recognizing the layer as needed ≠ finished architecture. Open design
questions, going through a separate design conveyor:
1. **Offsets (CRITICAL):** the whole system is built on character
   positions (text.find, sign_offset_start/end, validated_offsets,
   text[offset]). NFKC CHANGES text length → naive normalization will
   shift all offsets and break the single-sign ↔ sequence link. How to
   reconcile normalization with the offset model is the main question.
2. **Fate of the old confusables field in cards:** migrate to layer /
   keep as override / delete?
3. **Layer insertion point:** before scan_signs? separate pass? how not
   to break sequence matching (_find_literal_matches)?
4. **flag vs transform:** does the layer CANONICALIZE text (mutate) or
   only FLAG (like invisible-guard, not strip)? — align with the
   accepted flag-only discipline.

## RELATION TO OTHER DECISIONS

This layer is the common root that BOTH scope conveyors hit:
- invisible signs → homoglyphs/bidi go here;
- digits → non-ASCII Nd (٠١, ０１ fullwidth) go here.
Decisions D1 (invisible=OPTION_2) and D8 (digits ASCII-only + Nd into
this layer) DEPEND on this layer existing. Hence it is decided FIRST.

## SOURCES (versioned)

sources/17.0.0/ (Unicode 17.0.0, DI=4174, fixed 2026-07-07,
via www.unicode.org):
- DerivedCoreProperties.txt (sha 24c7fed1195c482f)
- UnicodeData.txt (sha 2e1efc1dcb59c575)
- confusables.txt (sha 091c7f82fc39ef20)
