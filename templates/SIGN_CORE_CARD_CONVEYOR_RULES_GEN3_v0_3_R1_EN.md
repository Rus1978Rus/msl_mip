PRIVATE AUTHORED PROJECT / COMMERCIAL USE PROHIBITED

DOCUMENT_ID: SIGN_CORE_CARD_CONVEYOR_RULES_GEN3_v0_3_R1_EN
DOCUMENT_TYPE: CONVEYOR_DISCIPLINE_RULESET
TEMPLATE_LINE: GEN3_v0_3
DOCUMENT_STATUS: WORKINGLY_CLOSED
STATUS: WORKINGLY_CLOSED / NOT_LOCKED / NOT_RUNTIME / NOT_VALIDATOR / NOT_PRODUCTION
AUTHOR_DECISION_REFERENCE: AUTHOR_DECISION_20260621_001_SIGN_CORE_CARD_CONVEYOR_RULES_v0_3_WORKINGLY_CLOSED_RU
AUTHOR: Ruslan Malyavsky
CREATED_AT: 2026-06-21
SUPERSEDES: SIGN_CORE_CARD_TEMPLATE_GEN3_CONVEYOR_v0_2_PLUS_EPOCH (the conveyor rules,
  not the template itself — the template is created as a separate document
  SIGN_CORE_CARD_TEMPLATE_GEN3_v0_3)

TRANSLATION_NOTE: This is the English translation of
  SIGN_CORE_CARD_CONVEYOR_RULES_GEN3_v0_3_RU. The Russian version
  remains authoritative. Field names, status tokens, and rule IDs are
  kept identical to the Russian version — only human-facing prose is
  translated.

============================================================
0. WHY THIS DOCUMENT WAS CREATED
============================================================

Five sign cards (DOT, AT, HASH, SKULL, SOLIDUS) that passed the
v0_2_PLUS_EPOCH conveyor and reached WORKINGLY_CLOSED showed
structural gaps under a line-by-line end-to-end audit.

SOURCE_AUDIT_TABLE (line-by-line check, performed by the document's
  author personally via direct grep over the primary sources,
  AUDIT_DATE: 2026-06-20/21, re-verified during external conveyor
  review of this document):

  CARD: DOT
    CARD_UID_PRESENT: NO
    ZONE_PRESENT: YES (ZONE_1)
    BASE_MODE_PRESENT: YES
    CODEPOINT_FIELD_NAME_USED: UNICODE
    GLYPH_FIELD_NAME_USED: GLYPH

  CARD: AT
    CARD_UID_PRESENT: NO
    ZONE_PRESENT: YES (ZONE_3)
    BASE_MODE_PRESENT: NO
    CODEPOINT_FIELD_NAME_USED: SIGN_UNICODE
    GLYPH_FIELD_NAME_USED: SIGN_GLYPH

  CARD: HASH
    CARD_UID_PRESENT: YES
    ZONE_PRESENT: YES (ZONE_3)
    BASE_MODE_PRESENT: YES
    CODEPOINT_FIELD_NAME_USED: SIGN
    GLYPH_FIELD_NAME_USED: VISIBLE_FORM

  CARD: SKULL
    CARD_UID_PRESENT: YES
    ZONE_PRESENT: YES (ZONE_3)
    BASE_MODE_PRESENT: YES
    CODEPOINT_FIELD_NAME_USED: SIGN
    GLYPH_FIELD_NAME_USED: VISIBLE_FORM

  CARD: SOLIDUS
    CARD_UID_PRESENT: YES
    ZONE_PRESENT: NO (at the time of the original audit; patched
      afterwards in both languages — ZONE_2 added)
    BASE_MODE_PRESENT: YES
    CODEPOINT_FIELD_NAME_USED: SIGN
    GLYPH_FIELD_NAME_USED: VISIBLE_FORM

SUMMARY_FROM_TABLE:
  CARD_UID missing: 2 of 5 (DOT, AT)
  ZONE was missing: 1 of 5 (SOLIDUS, fixed by patch)
  BASE_MODE missing: 1 of 5 (AT)
  Codepoint field names: 3 different variants (UNICODE / SIGN_UNICODE / SIGN)
  Glyph field names: 3 different variants (GLYPH / SIGN_GLYPH / VISIBLE_FORM)

VERIFICATION_NOTE: during external conveyor review of this document,
  one reviewer (Qwen) proposed the refinement "3 of 5 cards without
  CARD_UID, including SKULL" — this refinement was checked by the
  document's author personally via direct grep over the SKULL file
  and REJECTED as inaccurate: SKULL contains CARD_UID (confirmed
  line by line). This episode is kept here as a live illustration of
  rule 8 itself (see section 8) — even an explicit verification
  attempt can contain an error, and the formal act of "refining" does
  not automatically make the second statement more reliable than the
  first without independent checking against the primary source.

ROOT CAUSE (from the table above): the v0_2_PLUS_EPOCH conveyor
checked the QUALITY of card content (MUTATION_CHECK,
ADVERSARIAL_EVIDENCE, MODEL_FAMILY_DIVERSITY), but did NOT check the
COMPLETENESS and UNIFORMITY of structure relative to the template and
relative to other already-closed cards.

SECOND ROOT CAUSE: WORKINGLY_CLOSED was assigned based on isolated
review of the card text. No card underwent real end-to-end execution
through MODULE_TEMPLATE before receiving this status. Structural holes
(a missing ZONE) were discovered only when trying to actually run the
card through the pipeline — that is, after the status had already been
assigned.

============================================================
1. PRINCIPLE: WORKINGLY_CLOSED ≠ READY FOR USE
============================================================

FORMULA:
  TEXT_REVIEW_PASS ≠ EXECUTABLE
  WORKINGLY_CLOSED (old meaning) ≠ SIMULATION_CONFIRMED
  STRUCTURAL_COMPLETENESS ≠ CONTENT_QUALITY
  (a card can be high-quality in content and still incomplete in
   structure — these are two different dimensions of checking)

NEW RULE:
  A sign card receives the final status ARTIFACT_CONFIRMED only after
  passing the SIMULATION_GATE (see section 5). WORKINGLY_CLOSED
  becomes an intermediate status, not final.

STATUS_PROGRESSION (new chain):
  WORKING_DRAFT
    → STRUCTURAL_PREFLIGHT_PASS (new step — check for the presence of
        all REQUIRED_FIELDS from section 2, BEFORE the textual conveyor
        review; a mechanical/fast check, does not require a full round
        of models)
    → CONVEYOR_REVIEW_PASS (textual review of content quality, as
        before — MUTATION_CHECK, ADVERSARIAL_EVIDENCE,
        MODEL_FAMILY_DIVERSITY)
    → WORKINGLY_CLOSED (as before, but not final)
    → SIMULATION_GATE_PASSED (new step, see section 5, graded by
        TIER depending on ZONE)
    → ARTIFACT_CONFIRMED (new final status)

  Any failure at any step → return to WORKING_DRAFT with an open list
  of findings, not silent accumulation of holes.

  PATCH_NOTE: the original version of the document placed
  STRUCTURAL_COMPLETENESS_VERIFIED after CONVEYOR_REVIEW_PASS — this
  created the risk of spending a full round of textual review on a
  card whose structural gaps could be found instantly. Fixed following
  external conveyor review (GPT-5.5): the structural check now precedes
  the content check.

============================================================
2. REQUIRED CARD FIELDS (REQUIRED_FIELDS)
============================================================

Unlike v0_2_PLUS_EPOCH, where field requirements were inferred from
the filled-in example of the template (implicitly), v0_3 fixes an
explicit list. A card CANNOT receive CONVEYOR_REVIEW_PASS without all
fields from this list.

REQUIRED_FIELDS_META:
  CARD_UID                  (unique card identifier;
                              REQUIRED — was missing in DOT, AT)
  CODEPOINT                  (Unicode codepoint, format U+XXXX —
                              the single canonical name for this
                              value; the SIGN field is forbidden as
                              a duplicate, see PATCH_NOTE_v0_3_P1)
  VISIBLE_FORM               (visible glyph of the sign)
  UNICODE_NAME               (official Unicode name)
  ZONE                       (ZONE_1 / ZONE_2 / ZONE_3 —
                              REQUIRED — was missing in SOLIDUS)
  DOCUMENT_STATUS
  TEMPLATE_LINE
  SOURCE_TEMPLATE
  AUTHOR                     (REQUIRED — was missing in the original
                              v0_3 version, added following external
                              conveyor review)
  CREATED_AT                 (REQUIRED)
  VERSION                    (REQUIRED)
  AUTHOR_DECISION_REFERENCE  (REQUIRED)
  RUN_CARD_REFERENCE         (REQUIRED)
  RUN_CARD_STATUS            (REQUIRED)

REQUIRED_FIELDS_META_OPTIONAL (added following the third round of
  external review — Kimi/Grok):
  RUN_CARD_DATE   (optional; required only if RUN_CARD_STATUS holds a
                    dated result of a conveyor run; occurs in HASH)
  PATCHED_AT      (optional; required only if the card was patched
                    after CREATED_AT; occurs in HASH)
  DISPLAY_NAME    (optional; human-readable name of the sign besides
                    the official UNICODE_NAME — e.g. "dot" for FULL
                    STOP; see also LEGACY_FIELD_MAPPING in section 3,
                    where SIGN_NAME from old cards maps here)

PATCH_NOTE_v0_3_P1: the original version of the document required both
  SIGN (in META) and CODEPOINT (in LAYER_A) for the same codepoint
  value — an internal contradiction, found by external review
  (GPT-5.5), confirmed by the document's author via line-by-line
  check. Fixed: the single canonical name is CODEPOINT, in all
  sections of the document.

REQUIRED_FIELDS_LAYER_A:
  VISIBLE_FORM
  BASE_MODE                  (categorical value, e.g. DATA_ONLY,
                              DATA_ONLY_SEPARATOR — REQUIRED — was
                              missing in AT. NOT replaced by
                              BASE_MODE_FORMULA — these are different
                              fields: BASE_MODE = category,
                              BASE_MODE_FORMULA = formula)
  BASE_MODE_FORMULA
  SIGN_CATEGORY
  WHAT_THIS_SIGN_IS_NOT       (minimum 10 items)
  BASE_FORMULAS                (minimum 10 formulas)

REQUIRED_FIELDS_LAYER_B:
  SAFE_CASES                 (minimum 6)
  RISK_CASES                  (minimum 6)
  CONFUSABLES                 (minimum 5)
  CONTRADICTION_GUARDS        (minimum 6)
  SEQUENCE_LAYER_BOUNDARY     (may be NOT_APPLICABLE with explicit
                              justification, but the field must be
                              present)
  PHAGO_ENTITY_MIMICRY        (may be empty with an explicit NOTE,
                              but the field must be present)

REQUIRED_FIELDS_LAYER_C:
  EFFECT_FIELDS (all 10 fields: authority/trust/verification/
    proof/execution/permission/status/role_assignment/runtime/
    existence)
  EFFECT_FIELDS_ALL_NONE
  CLOSED_SCHEMA

OPTIONAL_FIELDS_RELATION (relation axis, AUTHOR_DECISION_20260708;
  added in revision R1 after the axis was implemented in code):

  SIGN_RELATIONS — an OPTIONAL block. Declared ONLY when the sign is a
  mask (homoglyph) of another sign, i.e. can visually impersonate a
  canon in a specific context. Ordinary signs do NOT have the block
  (absence = no active relations, the sign acts standalone; legacy
  v0_3 cards do NOT migrate the block — D1).

  WHEN TO DECLARE AN EDGE: the sign resembles another (the canon)
  enough to impersonate it in a specific context (URL, domain, path...).
  Similarity itself is NOT a threat (RELATION_FOUND != THREAT); the
  edge only records the link, risk is decided by the runtime from
  context. Do NOT declare edges "just in case" — extra edges produce
  false positives.

  EDGE FIELDS (RELATION_NNN):
    RELATION_TYPE      — CONFUSABLE_OF (visually confused) /
                         NFKC_MAPS_TO (normalises into the canon) /
                         VISUAL_MIMIC_OF (visual mimicry)
    TARGET             — the canon: codepoint or sequence (e.g. U+002F)
    CONTEXT_SCOPE      — where the link is active (one or more,
                         comma-separated): URL / HOST / PORT / PATH /
                         EMAIL / IDENTIFIER / IDN / CODE / FREE_TEXT /
                         ANY. HOST = the domain part (the main
                         substitution case). ANY = "everywhere" — use
                         WITH CARE (high false-positive risk); only for
                         context-independent links. An edge WITHOUT
                         scope matches nowhere (except ANY) — the
                         validator emits RELATION_WITHOUT_SCOPE.
    VERIFICATION_STATUS — VERIFIED / CANDIDATE / MANUAL_OVERRIDE.
                         CANDIDATE downgrades the final risk one step.
    RUNTIME_EFFECT     — ALWAYS RELATION_ONLY (hard invariant: the
                         edge states similarity, NOT risk).
    IS_ACTIVE          — optional; TRUE by default. FALSE/NO/0/OFF
                         disables the edge without deletion. If ALL
                         edges are disabled the validator emits
                         ALL_RELATIONS_INACTIVE (audit trace, not error).

  BOUNDARY: mask risk is decided by the SEQUENCE layer (edge +
  protected context + neighbours), NOT by the card and NOT by
  single-sign. The card only DECLARES the link. Provenance of similar
  signs stays in CONFUSABLES (human-readable list); the runtime takes
  edges ONLY from SIGN_RELATIONS and does NOT read CONFUSABLES as edges.

  EXAMPLE (fullwidth solidus mask ／ U+FF0F):
    SIGN_RELATIONS:
      RELATION_001:
        RELATION_TYPE: CONFUSABLE_OF
        TARGET: U+002F
        CONTEXT_SCOPE: URL, HOST, PATH
        VERIFICATION_STATUS: VERIFIED
        RUNTIME_EFFECT: RELATION_ONLY
    -> runtime: ／ in http://gоog／le.com (host) -> HIGH;
       in http://ok.com/a／b (path) -> MEDIUM; in free text -> NONE.

REQUIRED_FIELDS_SEMANTIC_EPOCH_TRACKER:
  For ZONE_1: EPOCH_TRACKER: NOT_APPLICABLE with an explicit NOTE
    why (polysemy without precession)
  For ZONE_2: EPOCH_TRACKER: CONTEXT_GATE_REQUIRED with explicit
    APPLICABILITY and CAPTURE_HISTORY (if applicable)
  For ZONE_3: EPOCH_TRACKER: REQUIRED with full CAPTURE_HISTORY,
    ACTIVE_EPOCH, DORMANT_EPOCHS, PRECESSION_ALERT

  RULE: regardless of ZONE, the SEMANTIC_EPOCH_TRACKER section MUST be
  present with an explicit EPOCH_TRACKER value. Never leave it implied.

REQUIRED_FIELDS_DOCUMENT_LEVEL:
  ADVERSARIAL_COVERAGE (with MIN_TOTAL_VECTORS, ACTUAL_TOTAL_VECTORS,
    COVERAGE_STATUS — all three fields required, not only MIN)
  MUTATION_CHECK (minimum 6 mutations, each with CLAIM/EXPECTED/RESULT)
  KNOWN_OPEN_QUESTIONS (may be an empty list with an explicit
    ALL_OPEN_QUESTIONS_CLOSED: YES)
  PATCH_HISTORY (format fixed in section 4)
  LIMITATION_STATEMENT
  INTEGRATION_INTERFACE_STATUS

============================================================
3. UNIFORM FIELD NAMING FORMAT (NAMING_NORM)
============================================================

PROBLEM FOUND: the same concept was named differently in different
cards:
  Sign name:    SIGN_NAME (DOT, AT) vs no separate field (HASH/SKULL/SOLIDUS)
  Codepoint:    UNICODE (DOT) vs SIGN_UNICODE (AT) vs SIGN (HASH/SKULL/SOLIDUS)
  Glyph:        GLYPH (DOT) vs SIGN_GLYPH (AT) vs VISIBLE_FORM (HASH/SKULL/SOLIDUS)

CANONICAL DECISION (mandatory for all new cards):
  Codepoint     → CODEPOINT: U+XXXX
  Glyph         → VISIBLE_FORM: <symbol>
  Unicode name  → UNICODE_NAME: <official name>

  The fields SIGN_NAME / SIGN_UNICODE / SIGN_GLYPH / UNICODE / GLYPH /
  SIGN are FORBIDDEN in new cards. If a human-readable name of the
  sign is needed besides UNICODE_NAME — use the DISPLAY_NAME field as
  an addition, not a replacement.

REASON_FOR_CHOICE: the CODEPOINT/VISIBLE_FORM/UNICODE_NAME canon was
  chosen because:
  1. The terminology is closer to the official Unicode Consortium
     nomenclature
  2. It is used in 3 of 5 existing cards (HASH, SKULL, SOLIDUS) — a
     later and more structurally mature generation of cards
  3. Separate names (CODEPOINT vs VISIBLE_FORM) unambiguously
     distinguish "what it is technically" from "how it looks", unlike
     the merged variants SIGN_UNICODE/SIGN_GLYPH

LEGACY_FIELD_MAPPING (read-only, for compatibility when reading
  existing cards, NOT for creating new ones):
  SIGN_NAME       → DISPLAY_NAME (optional)
  UNICODE         → CODEPOINT
  SIGN_UNICODE    → CODEPOINT
  SIGN            → CODEPOINT
  GLYPH           → VISIBLE_FORM
  SIGN_GLYPH      → VISIBLE_FORM

  This is a mapping for reading, not a requirement to rename fields in
  legacy cards. Any future parser/validator must support both name
  sets through this mapping, until the moment (if a separate decision
  is made) when legacy cards are re-created under v0_3.

LOCK FIELDS (CANONICAL DECISION):
  The separate approach is used (modeled on HASH/SKULL/SOLIDUS,
  not DOT/AT):
    LAYER_A_LOCK: PERMANENT
    LAYER_B_LOCK: REVIEWABLE
    LAYER_C_LOCK: SESSION
    SEMANTIC_EPOCH_TRACKER_LOCK: REVIEWABLE

  A single SCHEMA_LOCK block (as in DOT/AT) is FORBIDDEN in new
  cards — separate LOCKs more precisely reflect the different nature
  of mutability of each LAYER.

TRANSLATION_NOTE_POLICY (project-wide, added following external review
  — GPT-5.5, across all three template translations):
  TRANSLATION_NOTE_ALLOWED_IN_TRANSLATED_TEMPLATES: YES
  PARSER_MUST_IGNORE_TRANSLATION_NOTE: YES
  A translated template (an _EN duplicate of a _RU authoritative
  document) may carry a top-level TRANSLATION_NOTE field explaining
  that the other-language version is authoritative. This field is
  metadata for human readers; any parser/validator must ignore it and
  must NOT treat its presence as a structural mismatch between the RU
  and EN versions.

============================================================
4. UNIFORM PATCH_HISTORY FORMAT
============================================================

CANONICAL FORMAT (mandatory for all new cards):

  v0_X_PATCH_NN: <short_patch_name> (<review_source>,
    <date>) — <description of what changed and why>
    REASON: <if the patch fixes a finding from a previous review>
    PATCHES_APPLIED: N
    PATCHES_VERIFIED: N/N

  FORBIDDEN: gaps in numbering without explicit explanation
  (the HASH.PATCHES_MISSING: P12 precedent — allowed only with an
  explanation; unmotivated gaps are a finding).

============================================================
5. SIMULATION_GATE — MANDATORY STEP BEFORE ARTIFACT_CONFIRMED
============================================================

NEW REQUIREMENT, absent in v0_2_PLUS_EPOCH:

After receiving WORKINGLY_CLOSED (textual review passed, structure
complete per REQUIRED_FIELDS) the card MUST pass at least one
end-to-end simulation run:

  SIGN_CORE_CARD → MODULE_TEMPLATE → INTEGRATOR_TEMPLATE →
  RUNTIME_ACTION_REQUEST

  Minimum 2 different contexts for ZONE_2/ZONE_3 signs
  (the DIFFERENTIATION_CHECK_MANDATORY check — see the rule
  established in SIMULATION_ARTIFACT_FIRST_PIPELINE_DOT_U002E_ZONE1).

  Minimum 1 context for ZONE_1 signs (DIFFERENTIATION_CHECK does not
  apply — ZONE_1 by definition does not distinguish contexts).

SIMULATION_GATE_EXIT_CONDITIONS:
  ARCHITECTURE_BUG found → return to WORKING_DRAFT, patch the card OR
    patch the template (depends on the nature of the finding), re-run
    from the start
  CARD_DATA_GAP found (a field is required by the pipeline but absent
    from the card) → return to WORKING_DRAFT
  All checks passed, 0 ARCHITECTURE_BUG → ARTIFACT_CONFIRMED

SIMULATION_GATE_TIERS (graded by sign complexity, added following
  external conveyor review — a single threshold for all signs creates
  a bottleneck risk when scaling to dozens of cards):

  TIER_1 (ZONE_1 — stable signs without contextual variability):
    Minimum 1 context
    DIFFERENTIATION_CHECK does not apply (ZONE_1 by definition does
      not distinguish contexts)
    May be performed by the author alone, without a mandatory external
      model conveyor
    Documented as a simplified SIMULATION_ARTIFACT

  TIER_2 (ZONE_2 — context-dependent signs):
    Minimum 2 contexts (3 recommended, modeled on SOLIDUS)
    DIFFERENTIATION_CHECK_MANDATORY is required
    Minimum 1 independent external reviewer (not the author)

  TIER_3 (ZONE_3 — signs with cultural epoch precession):
    Minimum 3 contexts, including at least 2 different epochs
      (DORMANT/ACTIVE) to test EPOCH_CONTEXT_INJECTION
    DIFFERENTIATION_CHECK_MANDATORY is required
    Minimum 2 independent external reviewers
    Full SIMULATION_ARTIFACT document (RU+EN if needed)

  The final status ARTIFACT_CONFIRMED is assigned only after passing
  the TIER corresponding to this card's ZONE.

SIMULATION PROTOCOL REQUIREMENT:
  The result of the SIMULATION_GATE is recorded as a separate document
  SIMULATION_ARTIFACT_<SIGN_NAME>_<CODEPOINT>, by analogy with
  SIMULATION_ARTIFACT_FIRST_PIPELINE_DOT_U002E_ZONE1. This document is
  part of the card package, not an optional appendix.

============================================================
6. RULE OF ISOLATED CONVEYOR PACKET DELIVERY
============================================================

(Carried over from the previous simulation round, formalized here as
part of the conveyor rules, not only as a lesson from one case.)

RULE_ID: ISOLATED_PACKET_DELIVERY_MANDATORY

When delivering a card or a simulation packet to any reviewing model —
the model must receive ONLY the isolated file, not the conversation
history. Before each conveyor round, the coordinating party confirms
this explicitly.

============================================================
7. RULE OF MANDATORY DIFFERENTIATION
============================================================

(Carried over from the previous round, formalized here.)

RULE_ID: DIFFERENTIATION_CHECK_MANDATORY

IF one sign is tested in N different contexts AND INTERPRETATION is
identical in all N contexts THEN automatically ARCHITECTURE_BUG. This
finding cannot be downgraded at the discretion of an individual
reviewer.

============================================================
8. RULE OF SELF-CHECK BEFORE TRUSTING ANOTHER'S ANALYSIS
============================================================

(New rule, established following this round of audit.)

RULE_ID: VERIFY_BEFORE_TRUST_MANDATORY

If one conveyor participant (a model) provides a table of
discrepancies, a diagnosis, or a finding about the state of files —
another participant, before acting on that analysis (patching,
creating new documents, changing architecture), must independently
verify at least part of the claimed facts against the primary source.

RATIONALE: during this audit, three cases were found and fixed where
the provided analysis was inaccurate (a factual error about
HASH.BASE_MODE; the expectation that DOT.LAYER_A_LOCK exists turned
out to be incorrect, since DOT uses the old SCHEMA_LOCK scheme of the
same template epoch, not the separate LAYER_*_LOCK — this is an
example that one must check not only the presence of a specific field,
but also which generational document scheme the card belongs to,
before treating the absence of a field as a finding;
"running ahead" on the status of the SOLIDUS.RU.ZONE patch, which had
not actually happened yet). A chain of models compounding theories
("STRUCTURAL_DRIFT" → "TEMPLATE_TO_TEMPLATE_INTERFACE_GAP" →
"CROSS_ARTIFACT_AUDIT_TEMPLATE") on the basis of unverified analysis
is the same class of risk as REVIEWED ≠ VALIDATED.

PATCH_NOTE_v0_3_P2 (third round of external review — Kimi, Grok):
the original wording of the DOT.LAYER_A_LOCK example was itself
inaccurate ("a claim about structure, not confirmed by personal
check") — this masked the real nature of the error (the expectation
of a field that does not exist in this generational template scheme,
not an unreliable "claim"). The wording is fixed above. Kept here as
another live example that even the wording of the illustration for
rule 8 itself went through more than one round of refinement before
becoming accurate.

============================================================
LIMITATIONS
============================================================

THIS_DOCUMENT ≠ FINAL_TEMPLATE (these are the conveyor rules;
  the canonical SIGN_CORE_CARD_TEMPLATE_GEN3_v0_3 itself is created as
  a separate document based on these rules)
RULESET_CREATED ≠ RULESET_VALIDATED (the rules themselves must pass
  conveyor review before being applied)
WORKING_DRAFT ≠ WORKINGLY_CLOSED
EXISTING_CARDS_NOT_RETROACTIVELY_INVALIDATED: old cards
  (DOT, AT, HASH, SKULL, SOLIDUS under v0_2_PLUS_EPOCH) keep their
  current status as LEGACY_PRE_v0_3; the decision to re-create them
  from scratch under v0_3 is made by the author separately for each
  card, not automatically by this document

============================================================
END_OF_DOCUMENT
