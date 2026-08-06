PRIVATE AUTHORED PROJECT / COMMERCIAL USE PROHIBITED

DOCUMENT_ID: AUTHOR_AMENDMENT_20260708_CARD_FORM_v0_4_SINGLE_TEMPLATE_EN
DOCUMENT_TYPE: AUTHOR_AMENDMENT
AMENDS: ARCH_DECISION_CARD_FORM_v0_4 (D2, partially; implementation plan, step 2)
AUTHOR: Ruslan Malyavsky
DATE: 2026-07-08
STATUS: ACCEPTED BY AUTHOR (in session; AUTHOR_DECISION_STATUS_AUTHORITY)
SUPERSEDED_PARTIALLY_BY: AUTHOR_DECISION_20260708_HOMOGLYPH_AS_RELATION
  (2026-07-08, later the same day):
  - item 2 (CARD_TYPE: FULL/HOMOGLYPH) — REVOKED: homoglyphness =
    a relation, not a type; the axis is replaced by SIGN_RELATIONS;
  - item 3 (HOMOGLYPH_FILL_RULE) — status OPEN, resolved at
    implementation step 0;
  - item 1 (the single card template) — IN FORCE.

============================================================
SUBSTANCE OF THE AMENDMENT
============================================================

1. THERE IS ONE SIGN CARD TEMPLATE. A separate "thin card"
   type/template (THIN_HOMOGLYPH_CARD) is NOT introduced.
   Author's wording: "we have an approved sign card template,
   there will be no other; if a sign does not perform some action
   described in the template, that field gets a dash or stays
   empty."

2. Sign type is distinguished by the META.CARD_TYPE field with
   values:
     FULL      — a sign with its own function/life;
     HOMOGLYPH — a lookalike sign that exists as a mask of
                 another sign.
   Absence of the field = FULL (legacy v0_3, compatible with D1).

3. For CARD_TYPE: HOMOGLYPH, fields that have no content for a
   mask-sign are filled with NOT_APPLICABLE / a dash; template
   minimums do not apply to such fields (HOMOGLYPH_FILL_RULE in
   the v0_4 template). A dash is knowledge too: "this sign has no
   life of its own, only someone else's form."

============================================================
WHAT REMAINS IN FORCE (the core of D2 untouched)
============================================================

- A homoglyph enters the runtime ONLY through ITS OWN card
  (ARCH_DECISION_HOMOGLYPH_VIA_CARD_ONLY; resolved by code:
  scan_signs builds the registry from card visible_form;
  CONFUSABLES entries do not enter the registry).
- A CONFUSABLE entry in the canon card = relation/provenance,
  NOT a runtime entry point.
- Required for a homoglyph: CANONICAL_TARGET (a sequence, D6),
  a reference to the canon card, VERIFICATION_SNAPSHOT.

============================================================
REASON
============================================================

The term "thin card" arose in the previous session's conveyor and
made it into the decision text, but was not introduced or
recognized by the author as a separate entity. One template = one
parser, one runtime path, one standard for the future library;
"not applicable" is legitimate field content, not a reason for a
second template.

============================================================
CONSEQUENCES FOR THE IMPLEMENTATION PLAN (migration packet, "six steps")
============================================================

- Step 2 (separate THIN_HOMOGLYPH_CARD template) — CANCELLED.
  Instead: edits to the v0_4 template (CARD_TYPE: FULL/HOMOGLYPH,
  HOMOGLYPH_FILL_RULE, CANONICAL_TARGET/CANON_CARD_REF fields for
  homoglyphs).
- Step 3 (parser): no second dataclass; CARD_TYPE and homoglyph
  fields are read. The EXECUTION mechanics of HOMOGLYPH cards in
  module_engine (a lookalike has no personal matcher) — to be
  refined during implementation, as D2 already noted.
- Scale (thousands of lookalikes) is handled NOT by cards but by
  the normalization layer (DECISION 1); HOMOGLYPH cards are
  selective, attack-driven (entry discipline as in the FO
  registry); drafts are automatically derivable from the pinned
  Unicode sources.
