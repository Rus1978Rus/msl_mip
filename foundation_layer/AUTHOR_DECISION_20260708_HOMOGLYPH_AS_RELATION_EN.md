PRIVATE AUTHORED PROJECT / COMMERCIAL USE PROHIBITED

DOCUMENT_ID: AUTHOR_DECISION_20260708_HOMOGLYPH_AS_RELATION_EN
DOCUMENT_TYPE: AUTHOR_DECISION
STATUS: ACCEPTED BY AUTHOR (AUTHOR_DECISION_STATUS_AUTHORITY)
IMPLEMENTATION_STATUS: DECISION_ACCEPTED / CODE_PENDING
  (repository is on GEN3_v0_3; the "relation" axis is NOT implemented;
  the v0_4 CARD_TYPE code is revoked and does NOT go to the repository)
AUTHOR: Ruslan Malyavsky
DATE: 2026-07-08
SUPERSEDES_PARTIALLY: AUTHOR_AMENDMENT_20260708_CARD_FORM_v0_4_SINGLE_TEMPLATE
  (the CARD_TYPE: FULL/HOMOGLYPH axis is revoked; the single template stays)

BASIS: four design conveyors (2026-07-08), 5-6 reviewers each:
  1. Situational sign reading — RICH, unanimous: a sign's behaviour is
     situational, lives on ZONE_2 + SEQUENCE, not in mere presence.
  2. Homoglyphness: type or relation — FUNDAMENTAL_ERROR_CONFIRMED,
     UNANIMOUS (6/6): CARD_TYPE as a sign type is a core error.
  3. Replacement construction — CONVERGENT: a minimal RELATIONS block
     with context, not a single ref, not a full graph.
  4. Risk verdict locus — CONVERGENT (6/6, incl. the former delegation
     camp): mask risk is decided in the SEQUENCE layer; delegation to
     the canon is allowed only as a PROBE/HELPER.

════════════════════════════════════════════════════════════════
DECISION
════════════════════════════════════════════════════════════════

D-REL-1. THE "TYPE" AXIS IS WRONG. The CARD_TYPE: FULL/HOMOGLYPH field
  is removed from the core (template, parser, module_engine).
  Homoglyphness is NOT a property of a sign but a RELATION between
  signs, activated by context. Every sign is just a sign, one card.

D-REL-2. MODEL — A RELATIONS BLOCK. Instead of a type, a SIGN_RELATIONS
  block (minimal form): an edge with RELATION_TYPE (CONFUSABLE_OF /
  NFKC_MAPS_TO / VISUAL_MIMIC_OF), TARGET (canon codepoint/sequence),
  CONTEXT_SCOPE (URL / PATH / EMAIL / IDENTIFIER / CODE / FREE_TEXT /
  ANY), VERIFICATION_STATUS. Edge RUNTIME_EFFECT = RELATION_ONLY (an
  edge by itself is NOT risk). Existing CANON_CARD_REF /
  CANONICAL_TARGET / CONFUSABLES.HOMOGLYPH_CARD_REF become compatible
  representations/aliases of the same relation (lossless migration).

D-REL-3. THE ＠ CASE (dual role). One codepoint may be a canon in its
  own script and a mask in another context. Expressed via the edge's
  CONTEXT_SCOPE, WITHOUT a duplicate card ("one sign — one card"
  preserved): outside scope the sign acts as standalone, inside scope
  the relation activates.

D-REL-4. RISK LOCUS — SEQUENCE. The final verdict on mask risk is made
  in the SEQUENCE layer (edge + protected context + neighbours), NOT in
  single-sign. Invariants:
    RELATION_FOUND ≠ THREAT
    CANON_MATCHER_RESULT ≠ FINAL_RISK
    RISK = RELATION + PROTECTED_CONTEXT + SEQUENCE_PATTERN

D-REL-5. CANON DELEGATION — PROBE ONLY. module_engine may call the
  canon matcher in PROJECTION/PROBE mode to get a hypothesis "what the
  canon would mean at this position". The result is DATA (a hypothesis)
  attached to the status, NOT a final risk. Single-sign for a mask
  emits risk = NONE/DATA_ONLY + a relation candidate.

D-REL-6. OBFUSCATION STEP — IN SEQUENCE. The obfuscation penalty
  (substituting a canon with a mask in a protected context) is applied
  in the SEQUENCE layer, not by the canon matcher (which doesn't know
  about the mask) and not by single-sign. Obfuscation is a property of
  the combination, not a single sign.

════════════════════════════════════════════════════════════════
WHAT IS PRESERVED (not redone)
════════════════════════════════════════════════════════════════
- The single sign card template (the 2026-07-08 amendment stays in this
  part; ONLY the CARD_TYPE field is revoked).
- Form v0_4: UNICODE_VERSION, VERIFICATION_SNAPSHOT, CONFUSABLES with
  provenance (SOURCE/BASIS/VERIFICATION_STATUS), D4 minimum 0 — all stay.
- scan_signs detection by visible_form — type-independent, unchanged.
- INVARIANT D1 (DUAL): the five v0_3 cards (DOT, SOLIDUS, SKULL,
  SKULL_CROSSBONES, AT) do NOT break — they have no CARD_TYPE and no
  SIGN_RELATIONS; they work as standalone signs. Regression mandatory
  (gate + 60/60 legacy).

════════════════════════════════════════════════════════════════
OPEN IMPLEMENTATION QUESTIONS (resolved in CODE via gate, NOT conveyor)
════════════════════════════════════════════════════════════════
- Typing of canon_hypothesis: enum of contexts or free tags.
- Reverse index: the edge is declared in the mask card, the canon does
  not duplicate — the runtime builds a reverse index (candidate, leaning YES).
- Sequence Bloat: matching in sequence by token property
  [is_homoglyph_of_X], not a separate SC per attack vector.
- A "called as mask" flag when probing the canon.
These are implementation questions, going via CODE → code-review → gate
→ PC, not a new design conveyor (design is settled).

════════════════════════════════════════════════════════════════
ROLLOUT ORDER (per prior unanimous decisions)
════════════════════════════════════════════════════════════════
Containers (brackets) first as the situational-reading pilot (a v0_2
probe exists, REPORTED), then the homoglyph as a regression case.
Implementation of the "relation" axis — next session, via CODE+gate.
