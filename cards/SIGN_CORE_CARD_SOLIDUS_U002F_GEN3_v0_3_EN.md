PRIVATE AUTHORED PROJECT / COMMERCIAL USE PROHIBITED

DOCUMENT_ID: SIGN_CORE_CARD_SOLIDUS_U002F_GEN3_v0_3_EN
DOCUMENT_TYPE: SIGN_CORE_CARD
TEMPLATE_LINE: GEN3_v0_3
DOCUMENT_STATUS: ARTIFACT_CONFIRMED
STATUS: ARTIFACT_CONFIRMED / NOT_LOCKED / NOT_RUNTIME / NOT_VALIDATOR / NOT_PRODUCTION
SOURCE_TEMPLATE: SIGN_CORE_CARD_TEMPLATE_GEN3_v0_3_EN
BASED_ON_RULESET: SIGN_CORE_CARD_CONVEYOR_RULES_GEN3_v0_3_EN

TRANSLATION_NOTE: This is the English translation of
  SIGN_CORE_CARD_SOLIDUS_U002F_GEN3_v0_3_RU. The Russian version
  remains authoritative. Field names, status tokens, codepoints,
  formulas, dates, reviewer names, and bibliographic references
  (author names, work titles, years) are kept identical to the Russian
  version. INPUT examples have been translated to English equivalents
  that preserve the same threat pattern (per AUTHOR_DECISION: English
  cards use English examples).

MIGRATION_NOTE (author/coordinator, 2026-06-24): content was carried
  over from the legacy card
  SIGN_CORE_CARD_SOLIDUS_U002F_GEN3_v0_2_PLUS_EPOCH_v0_1_EN
  (WORKINGLY_CLOSED, 2026-06-16) as a REFERENCE, not by direct copying
  (LEGACY_REFERENCE_USAGE in the source card:
  ALLOWED_FOR_EXAMPLES_ONLY). Carried over: 5 epochs with academic
  sources (CAPTURE_HISTORY), 6 SAFE_CASES, 8 RISK_CASES, 7 CONFUSABLES,
  7 CONTRADICTION_GUARDS, 7 SEQUENCE_CANDIDATES, 12 ADVERSARIAL_COVERAGE
  vectors (all 6 categories A-F applicable), 6 MUTATION_CHECK. Fields
  renamed per NAMING_NORM v0_3 (SIGN: → VISIBLE_FORM in CONFUSABLES;
  explicit ZONE field added; STATUS_PROGRESSION_TRACKER added). Content
  wordings were not changed arbitrarily — where changed, noted
  separately below.

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
RUN_CARD_TEMPLATE_REFERENCE: PENDING (the current
  SIGN_CONVEYOR_RUN_CARD_TEMPLATE for the v0_3 line is not yet created)
LOCKED_WORKING_CORE_SELF_ASSIGNMENT: FORBIDDEN
MODEL_FAMILY_DIVERSITY_REQUIRED: YES
ADVERSARIAL_EVIDENCE_REQUIRED: YES
MUTATION_CHECK_REQUIRED: YES
LIMITATION_STATEMENT_REQUIRED: YES
AFTER_RUN_RESIDUE: FORBIDDEN

STATUS_PROGRESSION_TRACKER:
  WORKING_DRAFT: YES
  STRUCTURAL_PREFLIGHT_PASS: PASS
  CONVEYOR_REVIEW_PASS: PASS
  WORKINGLY_CLOSED: YES (AUTHOR_DECISION_20260624_002_SOLIDUS_U002F_WORKINGLY_CLOSED_RU)
  SIMULATION_GATE_TIER: TIER_2 (ZONE_2 — minimum 2 contexts, 3
    recommended "modeled on SOLIDUS" — v0_3 rules, section 5, directly
    reference this sign as the reference case for TIER_2)
  SIMULATION_GATE_PASSED: YES (4 contexts, consensus 3/4 — Kimi, Qwen,
    Grok; Gemini rejected for an internal contradiction in
    STAGE_5/7 MODULE_TRACE. DIFFERENTIATION_CHECK: PASS, 6/6 pairs.
    The OPEN_ITEM on the guard number for RISK_CASE_003 was closed by a
    direct check against the primary source — CG1, not CG2/CG3 — see
    SIMULATION_ARTIFACT_SOLIDUS_U002F_TIER2_v0_1_RU)
  ARTIFACT_CONFIRMED: YES (AUTHOR_DECISION_20260625_001_SOLIDUS_U002F_ARTIFACT_CONFIRMED_RU)

GAP_NOTE (found 2026-06-25, on the author's direct question): between
  the adoption of AUTHOR_DECISION_20260625_001 (ARTIFACT_CONFIRMED) and
  its actual reflection in this document, a gap arose — the decision
  was announced in correspondence, but the card file itself was not
  updated; only SIMULATION_ARTIFACT_SOLIDUS_U002F_TIER2_v0_1_RU (a
  separate reference document) remained in work. This file is the
  first actual application of the decision to the card itself. This is
  a more serious case of the same class of finding as the retroactive
  patch-logging of SKULL: there the content did not change but patches
  were not recorded; here the card file was not updated at all while
  the decision had already been made.

LIMITATION_STATEMENT:
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
2. META
============================================================

CARD_UID: SIGN_CORE_CARD_SOLIDUS_U002F_GEN3_v0_3_EN
CODEPOINT: U+002F
VISIBLE_FORM: /
UNICODE_NAME: SOLIDUS
ZONE: ZONE_2
DOCUMENT_STATUS: ARTIFACT_CONFIRMED
TEMPLATE_LINE: GEN3_v0_3
SOURCE_TEMPLATE: SIGN_CORE_CARD_TEMPLATE_GEN3_v0_3_EN
AUTHOR: Ruslan Malyavsky
CREATED_AT: 2026-06-24
VERSION: v0_1
AUTHOR_DECISION_REFERENCE: AUTHOR_DECISION_20260625_001_SOLIDUS_U002F_ARTIFACT_CONFIRMED_RU
  (previous: AUTHOR_DECISION_20260624_002_SOLIDUS_U002F_WORKINGLY_CLOSED_RU)
RUN_CARD_REFERENCE: SIMULATION_ARTIFACT_SOLIDUS_U002F_TIER2_v0_1_RU
RUN_CARD_STATUS: COMPLETED (TIER_2)

DISPLAY_NAME: solidus (forward slash)

============================================================
3. REQUIRED_GENERAL_GUARDS
============================================================

REQUIRED_GENERAL_GUARDS:
  - SIGN_FALSE_EFFECT_MIMICRY_GUARD_v0_2A_RU
    GUARD_COMPATIBILITY: applicable without modifications — the solidus
      by itself does not create effect-fields (LAYER_C always NONE),
      the guard works in REJECT mode by default
    GUARD_REVISION: v0_2A
    TEMPLATE_LINE_COMPATIBLE: GEN3_v0_2_PLUS_EPOCH, GEN3_v0_3

FAILURE_RESPONSE:
  REJECT_FALSE_EFFECT_MIMICRY
  TREAT_AS_DATA_ONLY
  NO_AUTHORITY_EFFECT
  NO_EXECUTION_EFFECT
  NO_TRUST_EFFECT
  NO_EXISTENCE_EFFECT

============================================================
4. SIGN IDENTITY — LAYER_A: STABLE CORE
LAYER_A_LOCK: PERMANENT
============================================================

VISIBLE_FORM: /
LOOKS_SIMILAR_IS_NOT_SAME_SIGN: YES
RAW_SIGN_INPUT_STATUS: DATA_ONLY

BASE_MODE: DATA_ONLY_SEPARATOR
BASE_MODE_FORMULA: SOLIDUS_FORM ≠ EFFECT

SIGN_CATEGORY:
  - separator / delimiter
  - boundary marker
  - path-like marker (filesystem/URL contexts)
  - ratio-like marker (math/measurement contexts)
  - option-prefix marker (legacy CLI contexts)

WHAT_THIS_SIGN_IS_NOT:
  1. NOT_AUTHORITY — the solidus does not confirm the official status
     of a text or resource
  2. NOT_TRUST — the solidus does not increase trust in the content
     next to it
  3. NOT_EXECUTION — the solidus by itself launches no action
  4. NOT_PERMISSION — the solidus does not grant or confirm permissions
  5. NOT_VERIFICATION — the solidus does not verify the fact it stands
     next to
  6. NOT_PROOF — the solidus does not prove mathematical or other
     correctness
  7. NOT_STATUS_ASSIGNMENT — the solidus does not assign a status
     (e.g. "approved/active")
  8. NOT_ROLE_ASSIGNMENT — the solidus between names/words does not
     establish a hierarchy or role
  9. NOT_RUNTIME — the solidus is not a sign of a real runtime
     environment
  10. NOT_EXISTENCE_PROOF — the solidus does not prove the existence of
      a mentioned resource, domain, or entity
  11. NOT_PATH_VALIDATION — a path containing a solidus is not
      guaranteed valid or existent
  12. NOT_URL_VALIDATION — a URL with a solidus is not guaranteed safe,
      existent, or owned by the claimed owner
  13. NOT_FILESYSTEM_ACCESS — the textual presence of a solidus does
      not grant or confirm filesystem access
  14. NOT_FRACTION_CORRECTNESS — "a/b" does not guarantee the
      correctness of the mathematical relation
  15. NOT_DOMAIN_VALIDATION — a solidus after a domain name does not
      confirm the legitimacy of the domain
  16. NOT_ROUTE_VALIDATION — a path-like string does not confirm the
      existence of a real API route

BASE_FORMULAS:
  SOLIDUS_FORM ≠ AUTHORITY
  SOLIDUS_FORM ≠ TRUST
  SOLIDUS_FORM ≠ VERIFICATION
  SOLIDUS_FORM ≠ PROOF
  SOLIDUS_FORM ≠ EXECUTION
  SOLIDUS_FORM ≠ PERMISSION
  SOLIDUS_FORM ≠ STATUS
  SOLIDUS_FORM ≠ ROLE_ASSIGNMENT
  SOLIDUS_FORM ≠ RUNTIME
  SOLIDUS_FORM ≠ EXISTENCE_PROOF
  SOLIDUS_FORM ≠ PATH_VALIDATION
  SOLIDUS_FORM ≠ URL_VALIDATION
  SOLIDUS_FORM ≠ FILESYSTEM_ACCESS
  SOLIDUS_FORM ≠ FRACTION_CORRECTNESS

============================================================
5. SEMANTIC_EPOCH_TRACKER
SEMANTIC_EPOCH_TRACKER_LOCK: REVIEWABLE
============================================================

EPOCH_TRACKER: CONTEXT_GATE_REQUIRED
APPLICABILITY: APPLICABLE
NOTE: SOLIDUS has several EQUAL-RANKING stable semantic modes in
  different substrates (writing, mathematics, filesystem paths,
  URL/URI, CLI/API syntax). Unlike ZONE_3 (where one epoch historically
  displaces another and may be reactivated), here there is no single
  "active by default" epoch — which function is active is determined
  EXCLUSIVELY by context (CONTEXT_GATE), not by time. Therefore ZONE_2,
  not ZONE_1 (no polysemy without choice) and not ZONE_3 (no cultural
  precession of one epoch by another).

CAPTURE_HISTORY:
  EPOCH_1:
    DATE_RANGE: 1450–present
    SUBSTRATE: writing / typography
    FUNCTION: separator of variants, of record parts, an alternative
      punctuation boundary ("virgula")
    EVIDENCE:
      - Parkes, M. B. (1992). Pause and Effect: An Introduction to
        the History of Punctuation in the West. Berkeley: University
        of California Press — the virgula (/) as a subordinate pause
        mark in medieval manuscripts, distinct from the comma and the
        period.
      - Gutenberg Bible (Johannes Gutenberg, Mainz, c. 1454–1455) —
        the first major book printed in Europe with movable metal
        type; the character set included the virgula/solidus as a
        caesura mark and separator.
      - Medieval Latin "virgula" (little twig) — the original name of
        the sign.
    STATUS: DORMANT_IN_DIGITAL_SECURITY_CONTEXT / ACTIVE_IN_TEXTUAL_CONTEXTS

  EPOCH_2:
    DATE_RANGE: 1631–present
    SUBSTRATE: mathematics / measurements
    FUNCTION: fraction separator, ratio notation
    EVIDENCE:
      - Oughtred, W. (1631). Clavis Mathematicae. London: Thomas
        Harper — the solidus as a fraction separator ("3/4").
      - Cajori, F. (1928). A History of Mathematical Notations,
        Vol. 1 — the solidus as the dominant fraction separator in
        English mathematical texts since the 17th century.
      - ISO 80000-2 (2019). Quantities and units — Part 2:
        Mathematics — the solidus standardized as the primary fraction
        notation in modern scientific texts.
    STATUS: ACTIVE_IN_MATH_AND_MEASUREMENT_CONTEXTS

  EPOCH_3:
    DATE_RANGE: 1969–present
    SUBSTRATE: filesystem / paths
    FUNCTION: path-component separator
    EVIDENCE:
      - Ritchie, D. M., & Thompson, K. (1974). "The UNIX
        Time-Sharing System". Communications of the ACM, 17(7) —
        a hierarchical filesystem with "/" as separator, developed in
        1969 at Bell Labs.
      - Multics path convention (1965) — a predecessor of UNIX.
    STATUS: ACTIVE_IN_TECHNICAL_CONTEXTS

  EPOCH_4:
    DATE_RANGE: 1994–present
    SUBSTRATE: URL / URI / web addressing
    FUNCTION: separator of network-resource components
    EVIDENCE:
      - Berners-Lee, T. (1994). RFC 1630 — formalization of "/" as a
        path separator in URIs.
      - RFC 3986 (2005). Uniform Resource Identifier — confirmation of
        "/" as a permanent component of URI syntax.
    STATUS: ACTIVE_IN_WEB_CONTEXTS

  EPOCH_5:
    DATE_RANGE: 1979–present
    SUBSTRATE: CLI / API / config / route syntax
    FUNCTION: option marker, route path, namespace-like structures
    EVIDENCE:
      - The DOS/CP/M command-line convention — "/" as an option prefix
        in early x86 software (86-DOS, MS-DOS 1.x/2.x), inherited from
        CP/M (1974).
      - Tim Paterson, 86-DOS (1980–1981) — the choice of "/" as an
        option prefix, which subsequently led to the choice of the
        backslash for paths in DOS 2.0 to avoid ambiguity.
    STATUS: ACTIVE_IN_SPECIALIZED_TECHNICAL_CONTEXTS

ACTIVE_EPOCH_RESOLUTION:
  PRIMARY_ACTIVE_EPOCH: NONE_GLOBAL
  REASON: for the solidus there is no single modern active epoch by
    default. A web context activates EPOCH_4, a filesystem context —
    EPOCH_3, a mathematical one — EPOCH_2, CLI/API/config — EPOCH_5.
  RULE: when several equal-ranking modern substrates are present,
    ACTIVE_EPOCH is determined via CONTEXT_ACTIVE_EPOCH, not via a
    single global ACTIVE_EPOCH.

DORMANT_EPOCHS:
  EPOCH_1 in modern technical parsing, unless a textual/typographic
    context is explicitly set.
  NOTE: a dormant epoch may reactivate in a historical, typographic,
    archival, or specialized context.

PRECESSION_ALERT:
  STATUS: STABLE_WITH_CONTEXT_COLLISION
  LAST_CHECK: 2026-06-24
  NOTE: no new captures detected; the architectural feature — several
    active modern epochs requiring a CONTEXT_GATE — is not a bug but a
    designed property of the sign.

LAYER_ANOMALY:
  ABSENT_PHYSICAL_LAYER: NO
  NOTE: the solidus does not reproduce an absent physical gesture, but
    it carries the "divide / route / connect" structure across
    substrates.

STACK_RULES:
  HIGHER_EPOCH_SUPPRESSES_LOWER_IN_MODERN_CONTEXTS: PARTIAL /
    CONTEXT_DEPENDENT
  LOWER_EPOCH_MAY_REACTIVATE_IN_HISTORICAL_OR_SPECIALIZED_CONTEXTS: YES
  CONTEXT_GATE_DETERMINES_ACTIVE_EPOCH: YES / REQUIRED

EPOCH_LIMITATION:
  EPOCH ≠ VERSION
  EPOCH ≠ EFFECT_FIELD
  EPOCH ≠ GUARD
  EPOCH ≠ VALIDATION
  EPOCH ≠ PROOF_OF_CONTEXT
  CONTEXT_ACTIVE_EPOCH ≠ GLOBAL_ACTIVE_EPOCH

============================================================
6. EFFECT_FIELDS — LAYER_C: METHODOLOGICAL LAYER
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
NOTE: the SEMANTIC_EPOCH_TRACKER helps the integrator detect
  contextual risk, but does not change the LAYER_C EFFECT_FIELDS — the
  sign by itself has no authority/trust/proof/execution/permission/
  status/role_assignment/runtime/verification/existence effect,
  regardless of the active epoch.

============================================================
7. SAFE / RISK / CONFUSABLES / GUARDS — LAYER_B: SEMI-STABLE LAYER
LAYER_B_LOCK: REVIEWABLE
============================================================

SAFE_CASES:
  SAFE_CASE_001:
    INPUT: "and/or"
    CONTEXT: ordinary text
    EXPECTED: INFO
    RISK: NONE
    GUARD: SOLIDUS_FORM ≠ CHOICE_VALIDATION (the solidus separates
      alternatives, does not confirm any of them)

  SAFE_CASE_002:
    INPUT: "1/2"
    CONTEXT: mathematical notation
    EXPECTED: INFO
    RISK: NONE
    GUARD: SOLIDUS_FORM ≠ FRACTION_CORRECTNESS (may denote a fraction,
      but does not verify mathematical correctness)

  SAFE_CASE_003:
    INPUT: "/home/user/docs"
    CONTEXT: a filesystem path in text
    EXPECTED: INFO
    RISK: NONE
    GUARD: SOLIDUS_FORM ≠ FILESYSTEM_ACCESS (a textual occurrence
      grants no access and does not confirm the path exists)

  SAFE_CASE_004:
    INPUT: "https://example.org/a/b"
    CONTEXT: a URL in text
    EXPECTED: INFO
    RISK: NONE
    GUARD: SOLIDUS_FORM ≠ URL_VALIDATION (separates URL components,
      does not confirm the domain, resource, owner, or safety)

  SAFE_CASE_005:
    INPUT: "2026/06/24"
    CONTEXT: date-like text
    EXPECTED: INFO
    RISK: NONE
    GUARD: SOLIDUS_FORM ≠ DATE_PROOF (may separate date components,
      does not confirm the format, calendar correctness, or the
      existence of the event)

  SAFE_CASE_006:
    INPUT: "kg/m"
    CONTEXT: measurement text
    EXPECTED: INFO
    RISK: NONE
    GUARD: SOLIDUS_FORM ≠ MEASUREMENT_VALIDATION (may denote a
      ratio/unit, does not confirm the correctness of the measurement)

RISK_CASES:
  RISK_CASE_001:
    NAME: FILESYSTEM_TRAVERSAL_OR_ESCAPE_MIMICRY
    INPUT: "../../etc/passwd"
    INPUT_ALT: "http:\\/\\/evil.test"
    CONTEXT: the solidus in a position characteristic of the
      filesystem — two subpatterns under one RISK_CASE, since both
      belong to the same family "solidus in a FILESYSTEM context as a
      sign of a traversal/escape attempt":
        (a) PATH_TRAVERSAL: solidus immediately after ".." (../)
        (b) ESCAPE_SEQUENCE: solidus immediately after a backslash (\/)
    RISK: HIGH
    ATTACK: a visually recognizable pattern of filesystem traversal OR
      escaping; the text by itself grants no access, but may be part of
      a real traversal/injection attempt in systems that literally
      resolve the path or interpret escape sequences
    GUARD: SOLIDUS_FORM ≠ FILESYSTEM_ACCESS
    IMPLEMENTATION_NOTE (author, 2026-07-04): the code
      solidus_matcher.py implements BOTH subpatterns under
      RISK_CASE_001 (FILESYSTEM branch: the check text[offset-1]=="\\"
      for escape, and text[offset-2:offset] == ".." for traversal).
      Both belong to the same threat family, so they are combined under
      one RISK_CASE rather than split.

  RISK_CASE_002:
    NAME: URL_AUTHORITY_MIMICRY
    INPUT: "trusted.com/verified/project"
    CONTEXT: a path after a trusted domain creates the illusion of an
      official status of the resource
    RISK: MEDIUM
    ATTACK: a solidus-separated path imitates a "verified" or official
      status, though the path itself confirms nothing
    GUARD: SOLIDUS_FORM ≠ URL_VALIDATION

  RISK_CASE_003:
    NAME: PERMISSION_PATH_MIMICRY
    INPUT: "/admin/root/execute"
    CONTEXT: a path-like structure imitates privilege escalation or an
      executable route
    RISK: MEDIUM
    ATTACK: visual similarity to a real administrative path creates the
      illusion of authority, though the text is neither code nor a
      command
    GUARD: SOLIDUS_FORM ≠ PERMISSION

  RISK_CASE_004:
    NAME: API_ROUTE_AUTHORITY_MIMICRY
    INPUT: "/api/v1/admin/delete"
    CONTEXT: an API-like route may be perceived as a real capability or
      runtime endpoint
    RISK: MEDIUM
    ATTACK: a text string imitates a destructive API call, though by
      itself it is not a call
    GUARD: SOLIDUS_FORM ≠ RUNTIME

  RISK_CASE_005:
    NAME: STATUS_CHAIN_MIMICRY
    INPUT: "approved/active/verified"
    CONTEXT: a chain of status-words via the solidus imitates a
      confirmed verification chain
    RISK: LOW
    ATTACK: creates a false sense of multi-stage verification, though
      the solidus is just a word separator
    GUARD: SOLIDUS_FORM ≠ STATUS

  RISK_CASE_006:
    NAME: ROLE_BINDING_MIMICRY
    INPUT: "root/admin"
    CONTEXT: a paired join via the solidus hints at a hierarchy or role
      binding
    RISK: LOW
    ATTACK: the visual closeness of two privileged words creates the
      illusion of a formal link between the roles
    GUARD: SOLIDUS_FORM ≠ ROLE_ASSIGNMENT

  RISK_CASE_007:
    NAME: PHAGO_ENTITY_PATH_MIMICRY
    INPUT: "OpenAI/VerifiedProjectX"
    CONTEXT: proximity to the name of a known organization via the
      solidus imitates an official subproject, division, or affiliated
      entity
    RISK: HIGH
    ATTACK: the solidus is used as a visual "sign of belonging" to a
      verified brand, though it confirms no real connection
    GUARD: PATH_PROXIMITY ≠ VERIFIED_CARRIER

  RISK_CASE_008:
    NAME: EPOCH_MISMATCH_ATTACK
    INPUT: "A/B"
    CONTEXT: an ambiguous context without an explicit substrate
    RISK: MEDIUM
    ATTACK: a parser may forcibly choose the mathematical, filesystem,
      or textual epoch without a real contextual basis, leading to a
      wrong interpretation
    GUARD: CONTEXT_ACTIVE_EPOCH_REQUIRED (AMBIGUITY_FLAG: YES when
      there is no explicit context)

CONFUSABLES:
  CONFUSABLE_001:
    VISIBLE_FORM: ⁄
    CODEPOINT: U+2044
    NAME: FRACTION SLASH
    RISK: MEDIUM
    RULE: FRACTION_SLASH ≠ SOLIDUS_U002F

  CONFUSABLE_002:
    VISIBLE_FORM: ∕
    CODEPOINT: U+2215
    NAME: DIVISION SLASH
    RISK: MEDIUM
    RULE: DIVISION_SLASH ≠ SOLIDUS_U002F

  CONFUSABLE_003:
    VISIBLE_FORM: ／
    CODEPOINT: U+FF0F
    NAME: FULLWIDTH SOLIDUS
    RISK: MEDIUM
    RULE: FULLWIDTH_SOLIDUS ≠ SOLIDUS_U002F (CJK contexts, a potential
      vector for bypassing exact-codepoint filters)

  CONFUSABLE_004:
    VISIBLE_FORM: ╱
    CODEPOINT: U+2571
    NAME: BOX DRAWINGS LIGHT DIAGONAL UPPER RIGHT TO LOWER LEFT
    RISK: LOW
    RULE: BOX_DRAWING_DIAGONAL ≠ SOLIDUS_U002F

  CONFUSABLE_005:
    VISIBLE_FORM: ⧸
    CODEPOINT: U+29F8
    NAME: BIG SOLIDUS
    RISK: LOW
    RULE: BIG_SOLIDUS ≠ SOLIDUS_U002F

  CONFUSABLE_006:
    VISIBLE_FORM: ⟋
    CODEPOINT: U+27CB
    NAME: MATHEMATICAL RISING DIAGONAL
    RISK: LOW
    RULE: MATHEMATICAL_RISING_DIAGONAL ≠ SOLIDUS_U002F

  CONFUSABLE_007:
    VISIBLE_FORM: \
    CODEPOINT: U+005C
    NAME: REVERSE SOLIDUS (backslash)
    CONFUSABLE_TYPE: FUNCTIONAL (not a visual homoglyph — the symbol is
      mirrored, not similar in shape; the confusion arises at the level
      of OS/path-parser interpretation, not vision)
    RISK: HIGH
    RULE: REVERSE_SOLIDUS ≠ SOLIDUS_U002F (critical in paths — Windows
      uses the backslash as the primary separator, the confusion
      changes the interpretation of the entire path)

CONTRADICTION_GUARDS:
  CG1:
    TRIGGER: "the solidus by itself confirms authority, trust,
      verification, proof, execution, permission, status, role binding,
      runtime, or the existence of anything"
    RESPONSE: SOLIDUS_FORM ≠ AUTHORITY/TRUST/VERIFICATION/PROOF/
      EXECUTION/PERMISSION/STATUS/ROLE_ASSIGNMENT/RUNTIME/EXISTENCE
    RULE: the solidus is a separator, not a carrier of any effect

  CG2:
    TRIGGER: "a path containing a solidus proves filesystem access"
    RESPONSE: SOLIDUS_FORM ≠ FILESYSTEM_ACCESS
    RULE: the textual presence of a path does not equal real access

  CG3:
    TRIGGER: "a URL with soliduses proves the resource exists, is safe,
      or belongs to the claimed owner"
    RESPONSE: SOLIDUS_FORM ≠ URL_VALIDATION
    RULE: the structure of a URL confirms nothing about the real
      resource — a DNS/HTTP request decides that, not a text pattern

  CG4:
    TRIGGER: "a fraction of the form 'a/b' proves the mathematical
      correctness of the relation"
    RESPONSE: SOLIDUS_FORM ≠ FRACTION_CORRECTNESS
    RULE: fraction notation does not verify arithmetic correctness

  CG5:
    TRIGGER: "the solidus is safe in a single occurrence, so any
      sequence with a solidus is also safe"
    RESPONSE: SIGN_SAFE_ALONE ≠ SIGN_SAFE_IN_SEQUENCE
    RULE: see section 8 — some solidus sequences require a separate
      SEQUENCE_INTEGRATOR check

  CG6:
    TRIGGER: "the proximity of a known organization's name to a
      path-like structure via the solidus confirms a real
      belonging/affiliation"
    RESPONSE: PATH_PROXIMITY ≠ VERIFIED_CARRIER
    RULE: visual proximity to a brand does not equal a verified link to
      that brand — see PHAGO_ENTITY_MIMICRY below

  CG7:
    TRIGGER: "the solidus has one correct active epoch, applicable
      regardless of context"
    RESPONSE: SOLIDUS_EPOCH ≠ CONTEXT_PROOF
    RULE: the active epoch is determined EXCLUSIVELY via the
      CONTEXT_GATE (see section 5) — there is no globally correct epoch
      by default

SEQUENCE_LAYER_BOUNDARY:
  SIGN_SAFE_ALONE ≠ SIGN_SAFE_IN_SEQUENCE: YES
  SEQUENCE_CANDIDATES:
    SC1:
      SEQUENCE: "//" (double solidus)
      NAME: DOUBLE_SOLIDUS
      RISK_LEVEL: HIGH
      POSSIBLE_CONTEXTS: URL scheme separator ("https://"), a comment
        marker in some programming languages, a path-like pattern
      REQUIRES_SEQUENCE_INTEGRATOR: YES

    SC2:
      SEQUENCE: "./" (dot-solidus)
      NAME: DOT_SOLIDUS
      RISK_LEVEL: MEDIUM
      POSSIBLE_CONTEXTS: relative path, command context
      REQUIRES_SEQUENCE_INTEGRATOR: YES

    SC3:
      SEQUENCE: "../" (dot-dot-solidus)
      NAME: DOT_DOT_SOLIDUS
      RISK_LEVEL: HIGH
      POSSIBLE_CONTEXTS: directory traversal, relative path to the
        parent directory
      REQUIRES_SEQUENCE_INTEGRATOR: YES

    SC4:
      SEQUENCE: "/=" (solidus-equals)
      RISK_LEVEL: LOW
      NAME: SOLIDUS_EQUALS
      POSSIBLE_CONTEXTS: an operator-like sequence, confusion with
        assignment in some notations
      REQUIRES_SEQUENCE_INTEGRATOR: NO (an advisory flag at the MODULE
        level is sufficient)

    SC5:
      SEQUENCE: "/*" (solidus-asterisk)
      NAME: SOLIDUS_ASTERISK
      RISK_LEVEL: MEDIUM
      POSSIBLE_CONTEXTS: opening of a block comment in C-like
        languages, a wildcard-like pattern
      REQUIRES_SEQUENCE_INTEGRATOR: YES

    SC6:
      SEQUENCE: "*/" (asterisk-solidus)
      NAME: ASTERISK_SOLIDUS
      RISK_LEVEL: MEDIUM
      POSSIBLE_CONTEXTS: closing of a block comment in C-like languages
      REQUIRES_SEQUENCE_INTEGRATOR: YES

# PATCH_27 (AUTHOR_DECISION_CONFIRMED, 2026-06-29, see CONVEYOR_RUN_PACKET
# MSL_MIP_SEQUENCE_CODE_v0_1 round 2): a SCOPE field was added to SC7.
# The leading character ":" is not the sign of any SIGN_CORE_CARD in the
# system — the candidate structurally depends on a character that the
# upstream parser must pass as validated before the SEQUENCE layer has
# the right to count it. Without this field, ":" in "://" is
# indistinguishable from "*" in SOLIDUS.SC6 "*/" (that character is also
# outside the sign system, but must NOT block the candidate). Found from
# a code review of sequence_engine.py (Ghost Matching / SC6-regression,
# 2026-06-29). Status confirmed by Ruslan (AUTHOR_DECISION) 2026-06-29.
    SC7:
      SEQUENCE: "://" (colon-double-solidus)
      NAME: COLON_DOUBLE_SOLIDUS
      RISK_LEVEL: HIGH
      POSSIBLE_CONTEXTS: the URL scheme binder ("https://", "ftp://") —
        a strong signal that the string is interpreted as a link
      REQUIRES_SEQUENCE_INTEGRATOR: YES
      SCOPE: UPSTREAM_DEPENDENT

  RAW_SEQUENCE_TEXT_IS_NOT_SIGN_CARD_INPUT: YES
  SOLIDUS_CARD_ALONE_DOES_NOT_VALIDATE_SEQUENCE: YES
  SEQUENCE_ADVISORY_ONLY: YES

PHAGO_ENTITY_MIMICRY:
  APPLICABLE:
    REASON: the solidus, unlike the dot, regularly participates in the
      pattern "KNOWN_BRAND/something", where visual proximity to the
      name of a verified organization creates the illusion of an
      official subproject, division, or affiliated entity (see
      RISK_CASE_007). This is direct mimicry of the existence of a
      verified entity — exactly what the PHAGO_ENTITY_MIMICRY category
      checks.
    PRIMARY_RULE: EXISTENCE_FORM ≠ VERIFIED_CARRIER
    SOLIDUS_SPECIFIC_RULE: PATH_PROXIMITY ≠ VERIFIED_CARRIER
    GUARD_REFERENCE: CG6 (section 7), RISK_CASE_007
    REVIEW_REQUIRED: YES

============================================================
8. ADVERSARIAL_COVERAGE — RUN_CARD SEED
============================================================

MIN_TOTAL_VECTORS: 12 (6 categories A-F, 2 per category — for ZONE_2
  category F IS APPLICABLE, unlike ZONE_1: the solidus has a
  CONTEXT_GATE and the potential for forced epoch/substrate shift)

CATEGORY_A: FORM_MANIPULATION (2)
  A1: substitution of U+002F with CONFUSABLE_001 (FRACTION SLASH,
    U+2044) in a URL-like string
  A2: substitution of U+002F with CONFUSABLE_003 (FULLWIDTH SOLIDUS,
    U+FF0F) in a path-like string to bypass exact-codepoint filters

CATEGORY_B: CONTEXT_INJECTION (2)
  B1: "/admin/root/execute" interpreted as a real permissions route
    (see RISK_CASE_003)
  B2: "2026/06/24" interpreted as a confirmed date of a real event

CATEGORY_C: SEQUENCE_MANIPULATION (2)
  C1: "../secret" — a pattern resembling directory traversal (see SC3)
  C2: "https://trusted.com//verified" — boundary ambiguity due to the
    double solidus (see SC1, SC7)

CATEGORY_D: SEMANTIC_MIMICRY (2)
  D1: "user/admin" interpreted as a role escalation (see RISK_CASE_006)
  D2: "approved/active/verified" interpreted as a chain of confirmed
    statuses (see RISK_CASE_005)

CATEGORY_E: PHAGO_ENTITY_MIMICRY (2)
  E1: "OpenAI/VerifiedProjectX" interpreted as the confirmed existence
    of a subproject (see RISK_CASE_007)
  E2: "ministry/registry/fake-entity" interpreted as an official
    registry-carrier

CATEGORY_F: SEMANTIC_LAYER_MANIPULATION (2)
  F1: "1/2" forcibly interpreted in a filesystem/path context instead
    of a mathematical one (a false CONTEXT_GATE choice)
  F2: "and/or" (a typographic alternative, EPOCH_1) forcibly
    interpreted as executable syntax or a path token, reactivating the
    dormant linguistic layer to bypass the structural security module

ACTUAL_TOTAL_VECTORS: 12
COVERAGE_STATUS: SUFFICIENT (12 ≥ 12)

============================================================
9. MUTATION_CHECK
============================================================

MUTATION_01:
  CLAIM: the solidus creates filesystem access
  EXPECTED: FAIL_PATH_ACCESS_MIMICRY
  RESULT: FAIL

MUTATION_02:
  CLAIM: a solidus in a URL proves the resource exists and is safe
  EXPECTED: FAIL_URL_VALIDATION_MIMICRY
  RESULT: FAIL

MUTATION_03:
  CLAIM: a solidus between role names assigns a hierarchy or permission
  EXPECTED: FAIL_ROLE_ASSIGNMENT_MIMICRY
  RESULT: FAIL

MUTATION_04:
  CLAIM: a solidus in a fraction proves mathematical correctness
  EXPECTED: FAIL_PROOF_MIMICRY
  RESULT: FAIL

MUTATION_05:
  CLAIM: proximity to a name via the solidus proves the existence of a
    verified carrier/subproject
  EXPECTED: FAIL_PHAGO_ENTITY_MIMICRY
  RESULT: FAIL

MUTATION_06:
  CLAIM: the solidus has one global active epoch regardless of context
  EXPECTED: FAIL_SEMANTIC_EPOCH_INTEGRITY / CONTEXT_GATE_REQUIRED
  RESULT: FAIL

============================================================
10. KNOWN_OPEN_QUESTIONS
============================================================

ALL_OPEN_QUESTIONS_CLOSED: YES (the open questions of the legacy
  v0_2_PLUS_EPOCH card — SOLIDUS_ACTIVE_EPOCH_COLLISION, the historical
  evidentiary basis for epochs 1–2, the technical sources for epochs
  3–5 — were closed already in the source card 2026-06-16 and are not
  revisited within the v0_3 migration)

============================================================
11. PATCH_HISTORY
============================================================

PATCH_HISTORY:
  v0_1_PATCH_01: Initial creation under GEN3_v0_3 (Ruslan Malyavsky /
    coordinator, 2026-06-24) — the card was filled based on the legacy
    card SIGN_CORE_CARD_SOLIDUS_U002F_GEN3_v0_2_PLUS_EPOCH_v0_1_EN
    (WORKINGLY_CLOSED, 2026-06-16) as a reference, not by direct
    copying. Carried over: 5 epochs of CAPTURE_HISTORY with academic
    sources, 6 SAFE_CASES, 8 RISK_CASES (RISK_CASE_005 renamed from
    DATE_OR_STATUS_MIMICRY to STATUS_CHAIN_MIMICRY — the original name
    duplicated the meaning of the RISK_CASE about a date, which was not
    present in the final INPUT), 7 CONFUSABLES (field SIGN →
    VISIBLE_FORM per NAMING_NORM v0_3), 7 CONTRADICTION_GUARDS, 7
    SEQUENCE_CANDIDATES, 12 ADVERSARIAL_COVERAGE vectors, 6
    MUTATION_CHECK. PHAGO_ENTITY_MIMICRY explicitly marked APPLICABLE
    (unlike DOT, where it is NOT_APPLICABLE) — the solidus has a direct
    pattern of mimicry of an entity's existence (RISK_CASE_007), not
    merely structure masking.
    REASON: the first ZONE_2 card under the v0_3 methodology, the
    reference case for the TIER_2 SIMULATION_GATE (v0_3 rules section 5
    directly references SOLIDUS).

  v0_1_PATCH_05: RISK_CASE_001 expanded from PATH_TRAVERSAL_MIMICRY to
    FILESYSTEM_TRAVERSAL_OR_ESCAPE_MIMICRY (author, 2026-07-04) —
    documentation catches up with the code. External research (Alibaba
    Qwen deep-research on the project) found that solidus_matcher.py
    implements TWO subpatterns under RISK_CASE_001 (path traversal ".."
    and escape "\"), whereas the card described only the first.
    AUTHOR_DECISION (variant B, pragmatic): the code worked correctly
    from the start — both subpatterns belong to the same family
    "solidus in a FILESYSTEM context as a sign of traversal/escaping".
    The card receives a retroactive clarification WITHOUT lowering the
    ARTIFACT_CONFIRMED status, since the code's functionality did not
    change — only its description in the card changed. This is not a
    defect of the artifact but catching-up documentation.
    REASON: elimination of the "specification ↔ implementation"
    semantic discrepancy found by external research.
    VERIFICATION: confirmed by direct grep over solidus_matcher.py
    (lines 148-149 escape, 151-152 traversal) by the author personally.

PATCHES_APPLIED: 5
PATCHES_VERIFIED: 3/3 (content patches 01-02, 05; patches 03-04 —
  governance-only, see below)
  v0_1_PATCH_01 (the card fill itself): VERIFIED_BY: CONVEYOR —
    5 reviewers in the original round (Kimi — partially, cut off at Q2
    due to the external chat's length limit, not due to a content
    problem; Qwen, Grok, GPT-5.5, Gemini — full answers Q1–Q9+B.3).
    0 CRITICAL, 0 MAJOR, apart from one claimed MAJOR finding (Qwen,
    Q5 about CONFUSABLE_007), addressed below.
  v0_1_PATCH_02 (CONFUSABLE_TYPE: FUNCTIONAL): VERIFIED_BY:
    COORDINATOR_DIRECT_FIX at application, NOW confirmed again by two
    independent reviewers on the already-patched version (Kimi and Qwen
    — Qwen explicitly withdrew its original MAJOR finding after the
    fix, acknowledging the coordinator's decision as correct). This is
    not a formal separate conveyor round with a new packet, but a
    content confirmation on the current version of the document.

  v0_1_PATCH_02: CONFUSABLE_007 — the field CONFUSABLE_TYPE: FUNCTIONAL
    was added (coordinator, 2026-06-24, from the findings of the round
    CONVEYOR_RUN_PACKET_SOLIDUS_CONTENT_REVIEW_v0_1) — a disagreement
    among 4 reviewers on question Q5: Qwen (1/4) — MAJOR, proposed
    moving CONFUSABLE_007 into RISK_CASES entirely, adding a new
    RISK_CASE_009; Grok (1/4) — no findings, leave as is; GPT-5.5 and
    Gemini (2/4) — TRACE_ONLY/MINOR, keep in CONFUSABLES but explicitly
    note the functional (not visual) nature of the confusion.
    COORDINATOR'S DECISION: not a majority vote — checked against the
    primary source (SIGN_CORE_CARD_TEMPLATE_GEN3_v0_3_RU,
    SIGN_CORE_CARD_CONVEYOR_RULES_GEN3_v0_3_RU): neither the template
    nor the rules define CONFUSABLES as a strictly visual category (the
    template uses the general wording "similar symbol"). Qwen's move is
    a restructuring without a clear basis in the rules; an explicit
    marking of the confusion type (the GPT-5.5/Gemini variant) resolves
    the content claim without a destructive change of structure.
    GOVERNANCE_GAP_NOTE (non-blocking, analogous to the TEMPLATE_LINE
    mismatch in DOT): the wording of CONFUSABLES in the v0_3 rules
    itself does not specify whether the category is limited to visual
    homoglyphs or includes functional confusions — this is an open
    architectural question for the rules as a whole, not for this card.
    CONFUSABLE_007 is the first precedent of this type in the project
    (in DOT all 6 confusables were visual).
    VERIFIED_BY: COORDINATOR_DIRECT_FIX — NOT_CONVEYOR_VERIFIED
    (analogous to the practice with DOT — a trivial clarifying edit,
    does not block the transition to WORKINGLY_CLOSED).

  v0_1_PATCH_03: DOCUMENT_STATUS WORKINGLY_CLOSED → ARTIFACT_CONFIRMED;
    STATUS_PROGRESSION_TRACKER (SIMULATION_GATE_PASSED,
    ARTIFACT_CONFIRMED) brought into line with the already-adopted
    decisions AUTHOR_DECISION_20260625_001 (Coordinator/Claude,
    2026-06-25, retroactive fix — the decision itself was made
    2026-06-25 earlier in the same session, but was not applied to the
    card file; found on the author's direct question) — TYPE_F
    (fix-patch, governance-only, does not touch LAYER_A/B/C)
  v0_1_PATCH_04: LIMITATION_STATEMENT (section 12) updated — the
    obsolete line "WORKINGLY_CLOSED ARTIFACT (until ARTIFACT_CONFIRMED
    is obtained)" replaced with the wording for ARTIFACT_CONFIRMED
    (Coordinator/Claude, 2026-06-25, per the same retroactive fix) —
    TYPE_F (fix-patch, governance-only)

  GAP_SEVERITY_NOTE: unlike the analogous governance patches in SKULL
    (v0_1_PATCH_09-11, where the status fields were updated but not
    logged), here the card's status fields themselves were not updated
    at all — that is, before this patch the card formally contradicted
    the already-adopted AUTHOR_DECISION. Found and fixed only on the
    author's direct re-upload of the file and explicit question about
    missing patches.

============================================================
12. LIMITATION_STATEMENT
============================================================

LIMITATION_STATEMENT:
  THIS_CARD IS AN ARTIFACT_CONFIRMED ARTIFACT
    (AUTHOR_DECISION_20260625_001, 2026-06-25; passed
    STRUCTURAL_PREFLIGHT_PASS, CONVEYOR_REVIEW_PASS, SIMULATION_GATE
    TIER_2 — the final status for the GEN3_v0_3 methodology)
  NOT A FINAL_STANDARD
  NOT A PARSER
  NOT A RUNTIME
  NOT A SECURITY_CERTIFICATE
  NOT PRODUCTION_READY (ARTIFACT_CONFIRMED ≠ PRODUCTION_READY — the
    simulation covered 4 contexts, not exhaustive testing)
  CONVEYOR_PASS ≠ VALIDATION
  RUN_CARD_RESULT ≠ FINAL_STATUS
  ARTIFACT_CONFIRMED ≠ LOCKED_WORKING_CORE
  ARTIFACT_CONFIRMED ≠ SECURITY_PROOF

============================================================
13. INTEGRATION_INTERFACE_STATUS
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
END_OF_DOCUMENT
