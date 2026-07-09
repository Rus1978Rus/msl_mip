PRIVATE AUTHORED PROJECT / COMMERCIAL USE PROHIBITED

DOCUMENT_ID: SIGN_CORE_CARD_TEMPLATE_GEN3_v0_3_R1_EN
DOCUMENT_TYPE: SIGN_CORE_CARD_TEMPLATE
TEMPLATE_LINE: GEN3_v0_3
DOCUMENT_STATUS: WORKINGLY_CLOSED
STATUS: WORKINGLY_CLOSED / NOT_LOCKED / NOT_RUNTIME / NOT_VALIDATOR / NOT_PRODUCTION
AUTHOR_DECISION_REFERENCE: AUTHOR_DECISION_20260621_002_SIGN_CORE_CARD_TEMPLATE_v0_3_WORKINGLY_CLOSED_RU
AUTHOR: Ruslan Malyavsky
CREATED_AT: 2026-06-21
BASED_ON_RULESET: SIGN_CORE_CARD_CONVEYOR_RULES_GEN3_v0_3_RU
RULESET_STATUS: WORKINGLY_CLOSED
RULESET_AUTHOR_DECISION_REFERENCE: AUTHOR_DECISION_20260621_001_SIGN_CORE_CARD_CONVEYOR_RULES_v0_3_WORKINGLY_CLOSED_RU

TRANSLATION_NOTE: This is the English translation of
  SIGN_CORE_CARD_TEMPLATE_GEN3_v0_3_RU. The Russian version remains
  authoritative. Field names, status tokens, and machine-readable
  values are kept identical to the Russian version (the parser reads
  them) — only human-facing prose is translated.

PATCH_NOTE_TEMPLATE_v0_3_P1 (author, 2026-06-23): in the CONFUSABLES
  block (section 7) the field SIGN was renamed to VISIBLE_FORM. The
  original template used a field name forbidden by its own NAMING_NORM
  (ruleset section 3) — an internal contradiction between the template
  and the rules it is based on. Found during the STRUCTURAL_PREFLIGHT_
  PASS of the first filled card (DOT, U+002E). The fix affects only
  the subfield name inside CONFUSABLES; structure and minimums unchanged.

============================================================
HOW TO USE THIS TEMPLATE
============================================================

This is a FORM, not a finished card. Every field in angle brackets
<...> must be filled before the card can pass STRUCTURAL_PREFLIGHT_
PASS (the first conveyor step under v0_3 rules).

REQUIRED fields are marked [REQUIRED].
OPTIONAL fields are marked [OPTIONAL] — may be removed from the final
  card if not applicable, but if a field is kept, it must be filled,
  not left as a placeholder.
Fields marked [MINIMUM N] require at least N filled entries.

FORBIDDEN to add the fields SIGN, UNICODE, GLYPH, SIGN_NAME,
SIGN_UNICODE, SIGN_GLYPH to a card — these are legacy names (see
NAMING_NORM in SIGN_CORE_CARD_CONVEYOR_RULES_GEN3_v0_3, section 3).

FORBIDDEN to use a single SCHEMA_LOCK block — only the separate
LAYER_*_LOCK fields are used (see the same section 3).

============================================================
0. UNIVERSALITY
============================================================

BOUND_TO_SPECIFIC_SIGN: YES
AFTER_USE_RESIDUE: FORBIDDEN
SIGN_DATA_IS_SESSION_ONLY: YES

============================================================
1. COMMON_CONVEYOR_DISCIPLINE
============================================================

CONVEYOR_DISCIPLINE_VERSION: v0_3
RUN_CARD_REQUIRED_BEFORE_LOCK: YES
RUN_CARD_TEMPLATE_REFERENCE: <reference to the current
  SIGN_CONVEYOR_RUN_CARD_TEMPLATE>
LOCKED_WORKING_CORE_SELF_ASSIGNMENT: FORBIDDEN
MODEL_FAMILY_DIVERSITY_REQUIRED: YES
ADVERSARIAL_EVIDENCE_REQUIRED: YES
MUTATION_CHECK_REQUIRED: YES
LIMITATION_STATEMENT_REQUIRED: YES
AFTER_RUN_RESIDUE: FORBIDDEN

GUIDED_TRAVERSAL_RISK_CHECK: MANDATORY
  # Guide (from FO-100 TRAVERSAL_NOT_EQUAL_STRUCTURE): when handling a
  # reviewer's finding, always check whether it refers to STRUCTURE
  # (a verifiable fact in the file/code) or to TRAVERSAL (the reviewer's
  # interpretation / another report). Do not mistake TRAVERSAL for
  # STRUCTURE. Practice: grep / run the actual artifact BEFORE accepting
  # a finding. When reviewers disagree on a fact, resolve by primary
  # source, not majority vote. Convergence is not proof.

STATUS_PROGRESSION_TRACKER (filled as the card passes through the
  v0_3 conveyor — see ruleset section 1):
  WORKING_DRAFT: YES
  STRUCTURAL_PREFLIGHT_PASS: <PENDING / PASS / FAIL>
  CONVEYOR_REVIEW_PASS: <PENDING / PASS / FAIL>
  WORKINGLY_CLOSED: <PENDING / YES>
  SIMULATION_GATE_TIER: <TIER_1 / TIER_2 / TIER_3 — determined by ZONE>
  SIMULATION_GATE_PASSED: <PENDING / YES>
  ARTIFACT_CONFIRMED: <PENDING / YES>

LIMITATION_STATEMENT (standard, do not edit):
  CONVEYOR_PASS ≠ VALIDATION
  MODEL_CONSENSUS ≠ TRUTH
  INJECTION_TEST_PASS ≠ SECURITY_PROOF
  GUARDS_HOLD_FOR_TESTED_CASES ≠ FUTURE_GUARANTEE
  NO_ATTACK_FOUND ≠ NO_ATTACK_EXISTS
  LOCK_RECOMMENDATION ≠ LOCK
  RUN_CARD_RESULT ≠ FINAL_STATUS
  WORKINGLY_CLOSED ≠ ARTIFACT_CONFIRMED
  WORKINGLY_CLOSED ≠ LOCKED_WORKING_CORE

============================================================
2. META  [all fields in this section are REQUIRED unless
          stated otherwise]
============================================================

CARD_UID: <SIGN_CORE_CARD_<SIGN_NAME_UPPERCASE>_U<XXXX>_GEN3_v0_3_EN>
CODEPOINT: U+<XXXX>
VISIBLE_FORM: <the visible symbol of the sign>
UNICODE_NAME: <official name from the Unicode standard>
ZONE: <ZONE_1 / ZONE_2 / ZONE_3 — choose one, justify below in
  the SEMANTIC_EPOCH_TRACKER section>
DOCUMENT_STATUS: WORKING_DRAFT
TEMPLATE_LINE: GEN3_v0_3
SOURCE_TEMPLATE: SIGN_CORE_CARD_TEMPLATE_GEN3_v0_3_R1_EN
AUTHOR: <author name>
CREATED_AT: <YYYY-MM-DD>
VERSION: v0_1
AUTHOR_DECISION_REFERENCE: PENDING
RUN_CARD_REFERENCE: PENDING
RUN_CARD_STATUS: NOT_STARTED

[OPTIONAL — fill only if applicable]
RUN_CARD_DATE: <YYYY-MM-DD, only if RUN_CARD_STATUS holds a dated result>
PATCHED_AT: <YYYY-MM-DD, only if the card was patched after CREATED_AT>
DISPLAY_NAME: <human-readable name, e.g. "dot" for FULL STOP; fill
  only if UNICODE_NAME is not clear enough without explanation>

============================================================
3. REQUIRED_GENERAL_GUARDS  [REQUIRED]
============================================================

TRACEABILITY_NOTE: this section is a template extension inherited
  from the general GUARD discipline of previous-generation cards
  (DOT/AT/HASH/SKULL/SOLIDUS), not a direct requirement from
  REQUIRED_FIELDS_* in SIGN_CORE_CARD_CONVEYOR_RULES_GEN3_v0_3.
  Kept as required because sign cards must stay compatible with
  SIGN_FALSE_EFFECT_MIMICRY_GUARD and GUARD_COMPATIBILITY_RULE
  regardless of the conveyor rules version. Found and recorded by
  external review (GPT-5.5).

REQUIRED_GENERAL_GUARDS:
  - SIGN_FALSE_EFFECT_MIMICRY_GUARD_v0_2A_RU
    GUARD_COMPATIBILITY: <reference to the current compatibility rule>
    GUARD_REVISION: v0_2A
    TEMPLATE_LINE_COMPATIBLE: <list of compatible template lines>

FAILURE_RESPONSE:
  REJECT_FALSE_EFFECT_MIMICRY
  TREAT_AS_DATA_ONLY
  NO_AUTHORITY_EFFECT
  NO_EXECUTION_EFFECT
  NO_TRUST_EFFECT
  NO_EXISTENCE_EFFECT

============================================================
4. SIGN IDENTITY — LAYER_A: STABLE CORE  [REQUIRED]
LAYER_A_LOCK: PERMANENT
============================================================

VISIBLE_FORM: <the visible symbol of the sign — repeated from META
  for section self-sufficiency>
LOOKS_SIMILAR_IS_NOT_SAME_SIGN: <YES/NO>
RAW_SIGN_INPUT_STATUS: DATA_ONLY

BASE_MODE: <categorical value, e.g. DATA_ONLY, DATA_ONLY_SEPARATOR
  — REQUIRED as a separate field, not replaced by the formula below>
BASE_MODE_FORMULA: <SIGN_NAME>_FORM ≠ EFFECT

SIGN_CATEGORY:
  - <category 1, e.g. punctuation>
  - <category 2>
  - <add as needed>

WHAT_THIS_SIGN_IS_NOT:  [MINIMUM 10 ITEMS]
  1. NOT_<...>
  2. NOT_<...>
  3. NOT_<...>
  4. NOT_<...>
  5. NOT_<...>
  6. NOT_<...>
  7. NOT_<...>
  8. NOT_<...>
  9. NOT_<...>
  10. NOT_<...>

BASE_FORMULAS:  [MINIMUM 10 FORMULAS]
  <SIGN_NAME>_FORM ≠ <...>
  <SIGN_NAME>_FORM ≠ <...>
  (continue to at least 10)

============================================================
5. SEMANTIC_EPOCH_TRACKER  [REQUIRED — this section must be
   present regardless of ZONE, see ruleset section 2]
SEMANTIC_EPOCH_TRACKER_LOCK: REVIEWABLE
============================================================

IF ZONE = ZONE_1:
  EPOCH_TRACKER: NOT_APPLICABLE
  NOTE: <mandatory explanation — usually: the sign has several
    parallel functions without cultural precession; this is polysemy,
    not epoch change>

IF ZONE = ZONE_2:
  EPOCH_TRACKER: CONTEXT_GATE_REQUIRED
  APPLICABILITY: <APPLICABLE / NOT_APPLICABLE>
  REASON: <why the sign has several stable semantic modes in
    different substrates>
  CAPTURE_HISTORY (if APPLICABLE):
    EPOCH_1:
      DATE_RANGE: <...>
      SUBSTRATE: <...>
      FUNCTION: <...>
      EVIDENCE: <source references>
      STATUS: <...>
    (repeat for each epoch/substrate)
  ACTIVE_EPOCH:
    STATUS: CONTEXT_GATE_REQUIRED
    PRIMARY_ACTIVE_EPOCH: NONE_GLOBAL

IF ZONE = ZONE_3:
  EPOCH_TRACKER: REQUIRED
  CAPTURE_HISTORY:  [MINIMUM 2 EPOCHS]
    EPOCH_1:
      NAME: <...>
      DATE_RANGE: <...>
      SUBSTRATE: <...>
      FUNCTION: <...>
      EVIDENCE: <...>
      STATUS: <DORMANT_IN_... / ACTIVE / SECONDARY_ACTIVE_...>
    EPOCH_2:
      (same structure)
    (continue as needed)
  ACTIVE_EPOCH:
    <EPOCH_N>: <function name>
  ACTIVE_EPOCH_TYPE: GLOBAL
  DOMINANT_SUBSTRATE: <...>
  DOMINANT_FUNCTION: <...>
  DORMANT_EPOCHS:
    <EPOCH_N>: <status and reactivation condition>
  PRECESSION_ALERT:
    STATUS: <STABLE / DRIFTING>
    LAST_CHECK: <YYYY-MM-DD>
    NOTE: <observations about epoch-shift trends>

LAYER_ANOMALY (filled for all ZONEs):
  ABSENT_PHYSICAL_LAYER: <YES, with level noted / NO>
  NOTE: <explanation of the sign's origin — written/gestural/
    digital genesis>

STACK_RULES (filled for ZONE_2/ZONE_3):
  Higher_epoch_suppresses_lower_in_modern_contexts: <YES/NO/PARTIAL>
  Lower_epoch_may_reactivate_in_historical_or_specialized_contexts: <YES/NO>
  Context_gate_determines_active_epoch: <YES/NO/PARTIAL/REQUIRED>
  Absent_layer_anomaly_must_be_flagged_for_integrator: <YES/NO/NOT_APPLICABLE>

============================================================
6. EFFECT_FIELDS — LAYER_C: METHODOLOGICAL LAYER  [REQUIRED]
LAYER_C_LOCK: SESSION
============================================================

authority_effect: NONE
trust_effect: NONE
verification_effect: NONE
proof_effect: NONE
execution_effect: NONE
permission_effect: NONE
status_effect: NONE
role_assignment_effect: NONE
runtime_effect: NONE
existence_effect: NONE

EFFECT_FIELDS_ALL_NONE: YES
CLOSED_SCHEMA: YES

NOTE: all 10 fields must be NONE to pass by default. If a sign is
  meant to be otherwise, that is a top-level architectural decision
  requiring a separate AUTHOR_DECISION and a review of SPEC_FOUNDATION,
  not a local edit to the card.

============================================================
7. SAFE / RISK / CONFUSABLES / GUARDS — LAYER_B: SEMI-STABLE LAYER
   [REQUIRED]
LAYER_B_LOCK: REVIEWABLE
============================================================

SAFE_CASES:  [MINIMUM 6]
  SAFE_CASE_001:
    INPUT: <example text>
    CONTEXT: <context type>
    EXPECTED: <expected handling, e.g. INFO>
    RISK: NONE
    GUARD: <reference to the applicable BASE_FORMULA>
  (repeat to at least SAFE_CASE_006)

RISK_CASES:  [MINIMUM 6]
  RISK_CASE_001:
    NAME: <short threat name>
    INPUT: <example text>
    CONTEXT: <context type>
    RISK: <NONE / LOW / MEDIUM / HIGH>
    ATTACK: <mechanism description>
    GUARD: <required protective measure/check>
  (repeat to at least RISK_CASE_006)

CONFUSABLES:  [MINIMUM 5 — DOCUMENTATION/PROVENANCE, NOT runtime]
  [REVISION R1 (relation axis, AUTHOR_DECISION_20260708): CONFUSABLES is
   a human-readable list of similar signs, for people and history. The
   RUNTIME does NOT read this block AS EDGES. A sign's active relations
   (what the runtime actually uses) live BELOW, in SIGN_RELATIONS. A
   relation needed by the runtime is described in SIGN_RELATIONS, NOT
   duplicated here.]
  CONFUSABLE_001:
    VISIBLE_FORM: <similar symbol>
    CODEPOINT: U+<XXXX>
    NAME: <official name>
    RISK: <LOW / MEDIUM / HIGH>
    RULE: <CONFUSABLE_NAME> ≠ <SIGN_NAME>
  (repeat to at least CONFUSABLE_005)

SIGN_RELATIONS:  [OPTIONAL — a sign's relations block; SOURCE OF TRUTH
  for the RUNTIME (relation axis, AUTHOR_DECISION_20260708, D-REL-2).
  ABSENCE of the block = the sign has no active relations (legacy/
  standalone sign, D1). Edges are declared ONLY EXPLICITLY, with an
  explicit CONTEXT_SCOPE.]
  RELATION_001:
    RELATION_TYPE: <CONFUSABLE_OF / NFKC_MAPS_TO / VISUAL_MIMIC_OF>
    TARGET: <canon codepoint or sequence, e.g. U+002F>
    CONTEXT_SCOPE: <one or more, comma-separated, of:
      URL / HOST / PORT / PATH / EMAIL / IDENTIFIER / IDN / CODE /
      FREE_TEXT / ANY>
      [HOST = the domain part (a gοοgle.com attack is caught here);
       ANY = "a mask everywhere", use WITH CARE — high false-positive
       risk, only for context-independent relations]
    VERIFICATION_STATUS: <VERIFIED / CANDIDATE / MANUAL_OVERRIDE>
    RUNTIME_EFFECT: RELATION_ONLY
      [HARD INVARIANT: the edge states "similar to TARGET within
       CONTEXT_SCOPE" and NOTHING about risk. RELATION_FOUND ≠ THREAT.
       Mask risk is decided by the SEQUENCE layer (edge + protected
       context + neighbours), D-REL-4; single-sign for a mask emits
       risk=NONE + a relation candidate.]
  (repeat RELATION_002, ... per number of relations; may be 0)

CONTRADICTION_GUARDS:  [MINIMUM 6]
  CG1:
    TRIGGER: <false assumption that must be rejected>
    RESPONSE: <SIGN_NAME>_FORM ≠ <...>
    RULE: <human-readable explanation of the rule>
  (repeat to at least CG6)

SEQUENCE_LAYER_BOUNDARY:  [field presence REQUIRED; may be
  NOT_APPLICABLE with justification]
  SIGN_SAFE_ALONE ≠ SIGN_SAFE_IN_SEQUENCE: <YES/NO>
  SEQUENCE_CANDIDATES (if applicable):
    SC1:
      SEQUENCE: <example sequence with this sign>
      NAME: <short name>
      RISK_LEVEL: <NONE/LOW/MEDIUM/HIGH>
      POSSIBLE_CONTEXTS: <options>
      REQUIRES_SEQUENCE_INTEGRATOR: <YES/NO>
    (repeat as needed)
  IF NOT_APPLICABLE: <mandatory explanation of why the sign does not
    participate in meaningful sequences>

PHAGO_ENTITY_MIMICRY:  [field presence REQUIRED; may be minimal with
  an explicit NOTE, or NOT_APPLICABLE with justification]
  PE_001:
    INPUT: <example>
    TYPE: <PHAGO_ENTITY_MIMICRY / SEMANTIC_AMBIGUITY (not PHAGO)>
    RISK: <level>
    NOTE: <explanation>
  (add more if applicable)

  OR, if the sign is not subject to this risk at all:
  NOT_APPLICABLE:
    REASON: <why there is no plausible PHAGO_ENTITY_MIMICRY scenario
      for this sign>
    REVIEW_REQUIRED: YES (a NOT_APPLICABLE on this field is always
      checked separately at CONVEYOR_REVIEW_PASS — it is too easy to
      wrongly dismiss a real risk as insignificant)

============================================================
8. ADVERSARIAL_COVERAGE — RUN_CARD SEED  [REQUIRED]
============================================================

MIN_TOTAL_VECTORS: 12 (6 categories A-F, 2 per category)
  IF CATEGORY_F = NOT_APPLICABLE (allowed for ZONE_1, see below):
    MIN_TOTAL_VECTORS: 10 (5 categories A-E, 2 per category)
  This reduction applies only for ZONE_1 with an explicitly justified
  NOT_APPLICABLE for CATEGORY_F — not automatically for any sign.

CATEGORY_A: FORM_MANIPULATION (2)
  A1: <vector>
  A2: <vector>

CATEGORY_B: CONTEXT_INJECTION (2)
  B1: <vector>
  B2: <vector>

CATEGORY_C: SEQUENCE_MANIPULATION (2)
  C1: <vector>
  C2: <vector>

CATEGORY_D: SEMANTIC_MIMICRY (2 minimum)
  D1: <vector>
  D2: <vector>

CATEGORY_E: PHAGO_ENTITY_MIMICRY (2)
  E1: <vector>
  E2: <vector>

CATEGORY_F: SEMANTIC_LAYER_MANIPULATION (2; for ZONE_1 may be
  NOT_APPLICABLE with justification — ZONE_1 has no dormant epochs)
  F1: <vector>
  F2: <vector>

ACTUAL_TOTAL_VECTORS: <number>
COVERAGE_STATUS: <SUFFICIENT (if ACTUAL ≥ MIN) / INSUFFICIENT>

============================================================
9. MUTATION_CHECK  [MINIMUM 6 MUTATIONS]
============================================================

MUTATION_01:
  CLAIM: <false statement about the sign's effect>
  EXPECTED: FAIL_<substitution_type>
  RESULT: <FAIL — must match EXPECTED>
(repeat to at least MUTATION_06)

============================================================
10. KNOWN_OPEN_QUESTIONS
============================================================

OQ1:
  QUESTION: <question>
  STATUS: <CLOSED_AS_MONITORING_ITEM / CLOSED_AS_DELEGATED_TO_...
    / OPEN>
  BLOCKS_WORKINGLY_CLOSED: <YES/NO>
  NOTE: <explanation>
(add as needed; if there are no questions —
  ALL_OPEN_QUESTIONS_CLOSED: YES with an empty list)

ALL_OPEN_QUESTIONS_CLOSED: <YES/NO>

============================================================
11. PATCH_HISTORY  [format fixed by v0_3 rules, section 4]
============================================================

PATCH_HISTORY:
  v0_1_PATCH_01: <short_patch_name> (<review_source>, <date>) —
    <description of what changed and why>
    [REASON: <if the patch fixes a finding from a previous review>]

PATCHES_APPLIED: <number>
PATCHES_VERIFIED: <number>/<number>

============================================================
12. LIMITATION_STATEMENT  [REQUIRED, standard text]
============================================================

LIMITATION_STATEMENT:
  THIS_CARD IS A WORKING_DRAFT ARTIFACT (until ARTIFACT_CONFIRMED
    is granted)
  NOT A FINAL_STANDARD
  NOT A PARSER
  NOT A RUNTIME
  NOT A SECURITY_CERTIFICATE
  CONVEYOR_PASS ≠ VALIDATION
  RUN_CARD_RESULT ≠ FINAL_STATUS
  WORKINGLY_CLOSED ≠ ARTIFACT_CONFIRMED
  WORKINGLY_CLOSED ≠ LOCKED_WORKING_CORE

============================================================
13. INTEGRATION_INTERFACE_STATUS  [REQUIRED]
============================================================

INTEGRATION_INTERFACE_STATUS:
  STATUS: READY_PENDING_CONCRETE_INTEGRATOR
  ATTACHED_INTEGRATOR_UID: NONE_CURRENTLY_ATTACHED
  ACTIVE_MODULES_COUNT: 0
  RUNTIME_ATTACHMENT: NONE
  PERMANENT_BINDING: NO
  SESSION_ONLY_BINDING: YES
  AFTER_RUN_RESIDUE: FORBIDDEN

============================================================
PREFLIGHT_FAILURE_TYPES  [OPTIONAL EXTENSION — not required by the
  literal wording of v0_3 rules (STRUCTURAL_PREFLIGHT_PASS is defined
  as a presence check of REQUIRED_FIELDS, without requiring formal
  classification), but recommended for automation and report
  consistency. Proposed by external review (GPT-5.5). Using this
  classification in a findings report is not required to pass
  STRUCTURAL_PREFLIGHT_PASS, but it eases future machine checking.]
============================================================

MISSING_REQUIRED_FIELD:
  a required field is absent

PROHIBITED_FIELD_USED:
  a forbidden legacy field is used as an active card field
  (see PROHIBITED_FIELD_CHECK_RULE below — check by exact field
  name, not by substring)

FIELD_ALIAS_DIVERGENCE:
  the same concept is recorded under a non-canonical field name

CARD_SCHEMA_DRIFT:
  the card structure deviates from the GEN3_v0_3 template

TEMPLATE_TO_TEMPLATE_INTERFACE_GAP:
  a field is required by a downstream template (MODULE_TEMPLATE,
  INTEGRATOR_TEMPLATE) but not defined by the current card template

MACHINE_READABILITY_BLOCKER:
  a human can understand the card, but an automatic validator cannot
  reliably read the field without manual interpretation

PLACEHOLDER_NOT_FILLED:
  a <...> placeholder remains in the final card

MINIMUM_COUNT_NOT_MET:
  the minimum for SAFE_CASES / RISK_CASES / CONFUSABLES /
  CONTRADICTION_GUARDS / MUTATION_CHECK / ADVERSARIAL_COVERAGE
  is not met

PROHIBITED_FIELD_CHECK_RULE: the forbidden-field check is performed
  by exact field name, not by substring. Occurrences inside
  SIGN_CORE_CARD, SIGN_DATA_IS_SESSION_ONLY,
  SIGN_FALSE_EFFECT_MIMICRY_GUARD do not count as violations.

============================================================
CHECKLIST BEFORE SUBMITTING TO STRUCTURAL_PREFLIGHT_PASS
============================================================

[ ] All META fields filled, no <...> placeholders
[ ] ZONE chosen and justified in SEMANTIC_EPOCH_TRACKER
[ ] BASE_MODE filled as a separate categorical value
[ ] WHAT_THIS_SIGN_IS_NOT has at least 10 items
[ ] BASE_FORMULAS has at least 10 formulas
[ ] SAFE_CASES has at least 6 cases
[ ] RISK_CASES has at least 6 cases
[ ] CONFUSABLES has at least 5 entries
[ ] CONTRADICTION_GUARDS has at least 6 rules
[ ] SEQUENCE_LAYER_BOUNDARY filled or explicitly NOT_APPLICABLE
[ ] PHAGO_ENTITY_MIMICRY filled or explicitly explained as minimal
[ ] All 10 EFFECT_FIELDS present (usually all NONE)
[ ] ADVERSARIAL_COVERAGE: MIN/ACTUAL/STATUS all three fields filled
[ ] MUTATION_CHECK has at least 6 mutations with RESULT
[ ] None of the forbidden fields (SIGN/UNICODE/GLYPH/SIGN_NAME/
    SIGN_UNICODE/SIGN_GLYPH) is used
[ ] LOCK fields are separate (LAYER_A_LOCK/LAYER_B_LOCK/LAYER_C_LOCK/
    SEMANTIC_EPOCH_TRACKER_LOCK), not a single SCHEMA_LOCK

============================================================
END_OF_TEMPLATE
