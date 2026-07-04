PRIVATE AUTHORED PROJECT / COMMERCIAL USE PROHIBITED

DOCUMENT_ID: SIGN_CORE_CARD_DOT_U002E_GEN3_v0_3_EN
DOCUMENT_TYPE: SIGN_CORE_CARD
TEMPLATE_LINE: GEN3_v0_3
DOCUMENT_STATUS: ARTIFACT_CONFIRMED
STATUS: ARTIFACT_CONFIRMED / NOT_LOCKED / NOT_RUNTIME / NOT_VALIDATOR / NOT_PRODUCTION
SOURCE_TEMPLATE: SIGN_CORE_CARD_TEMPLATE_GEN3_v0_3_EN
BASED_ON_RULESET: SIGN_CORE_CARD_CONVEYOR_RULES_GEN3_v0_3_EN

TRANSLATION_NOTE: This is the English translation of
  SIGN_CORE_CARD_DOT_U002E_GEN3_v0_3_RU. The Russian version remains
  authoritative. Field names, status tokens, codepoints, and formulas
  are kept identical to the Russian version. INPUT examples have been
  translated to English equivalents that preserve the same threat
  pattern (per AUTHOR_DECISION: English cards use English examples).

PATCH_NOTE_v0_1_PATCH_02 (author, 2026-06-23): in section 7
  (CONFUSABLES) the field SIGN was renamed to VISIBLE_FORM in all
  five entries (CONFUSABLE_001..005), synchronously with the patch to
  SIGN_CORE_CARD_TEMPLATE_GEN3_v0_3 (PATCH_NOTE_TEMPLATE_v0_3_P1). The
  card used a field name forbidden by NAMING_NORM
  (SIGN_CORE_CARD_CONVEYOR_RULES_GEN3_v0_3, section 3) because that
  name was in the template itself at fill time. Found during
  STRUCTURAL_PREFLIGHT_PASS. Field values unchanged, only the name.

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
  WORKINGLY_CLOSED: YES (AUTHOR_DECISION_20260623_001_DOT_U002E_WORKINGLY_CLOSED_RU)
  SIMULATION_GATE_TIER: TIER_1
  SIMULATION_GATE_PASSED: YES (see SIMULATION_NOTE below)
  ARTIFACT_CONFIRMED: YES (AUTHOR_DECISION_20260624_001_DOT_U002E_ARTIFACT_CONFIRMED_RU)

SIMULATION_NOTE (2026-06-23/24, coordinator, not a separate conveyor
  packet — TIER_1/ZONE_1 permits execution by the author/coordinator
  alone, v0_3 rules section 5):
  The end-to-end run through MODULE_TEMPLATE_SINGLE_SIGN →
  INTEGRATOR_TEMPLATE was performed TWICE on the same two contexts:
    CONTEXT_1: "Version 3.14 released." (two dot occurrences —
      decimal separator + sentence terminator) → expected pass in
      both rounds, unchanged.
    CONTEXT_2: "paypal.com.security-check.ru" (RISK_CASE_002, HIGH) →
      BEFORE v0_1_PATCH_22 in MODULE_TEMPLATE: pass (bug — RISK_CASES
      were not checked for ZONE_1, see below).
      AFTER v0_1_PATCH_22: hold_pending_review (correct).
  During the first round, an ARCHITECTURE_BUG was found and documented
    in MODULE_TEMPLATE_SINGLE_SIGN_GEN3_v0_2_PLUS_EPOCH_v0_1 (not in
    this card) — ZONE_1_ALGORITHM did not check RISK_CASES, fixed by
    patch v0_1_PATCH_22 (EN+RU versions of the document, conveyor-
    verified: CONVEYOR_RUN_PACKET_MODULE_TEMPLATE_PATCH22_VERIFICATION_
    v0_1, 4 reviewers, ACCEPT 4/4).
  The second round (after the patch) confirmed the fix on the same
    inputs without divergence.
  OPEN, NON-BLOCKING: the card's TEMPLATE_LINE (GEN3_v0_3) does not
    match the MODULE_TEMPLATE's TEMPLATE_LINE (GEN3_v0_2_PLUS_EPOCH) —
    a governance mismatch, not a functional gap (structurally all
    required fields are present, the run passed without difficulty).
  THIS IS NOT a formal CONVEYOR_RUN_PACKET of type SIMULATION and not
    a multi-model check — the trace was performed by a single
    coordinator. SIMULATION_GATE_PASSED: YES reflects this with full
    transparency, not masking the absence of multi-model verification
    of this specific step (unlike CONTENT_REVIEW and
    PATCH_03_04_VERIFICATION, which passed the full multi-model
    conveyor).

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

CARD_UID: SIGN_CORE_CARD_DOT_U002E_GEN3_v0_3_EN
CODEPOINT: U+002E
VISIBLE_FORM: .
UNICODE_NAME: FULL STOP
ZONE: ZONE_1
DOCUMENT_STATUS: ARTIFACT_CONFIRMED
TEMPLATE_LINE: GEN3_v0_3
SOURCE_TEMPLATE: SIGN_CORE_CARD_TEMPLATE_GEN3_v0_3_EN
AUTHOR: Ruslan Malyavsky
CREATED_AT: 2026-06-23
VERSION: v0_1
AUTHOR_DECISION_REFERENCE: AUTHOR_DECISION_20260624_001_DOT_U002E_ARTIFACT_CONFIRMED_RU
  (previous: AUTHOR_DECISION_20260623_001_DOT_U002E_WORKINGLY_CLOSED_RU)
RUN_CARD_REFERENCE: SIMULATION_ARTIFACT_DOT_U002E_TIER1_v0_1_RU
RUN_CARD_STATUS: COMPLETED (TIER_1, see SIMULATION_NOTE above and the
  SIMULATION_ARTIFACT as a separate document)

DISPLAY_NAME: dot

============================================================
3. REQUIRED_GENERAL_GUARDS
============================================================

REQUIRED_GENERAL_GUARDS:
  - SIGN_FALSE_EFFECT_MIMICRY_GUARD_v0_2A_RU
    GUARD_COMPATIBILITY: applicable without modifications — the dot
      does not create effect-fields, the guard works in REJECT mode
      by default
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

VISIBLE_FORM: .
LOOKS_SIMILAR_IS_NOT_SAME_SIGN: YES
RAW_SIGN_INPUT_STATUS: DATA_ONLY

BASE_MODE: DATA_ONLY_SEPARATOR
BASE_MODE_FORMULA: DOT_FORM ≠ EFFECT

SIGN_CATEGORY:
  - punctuation
  - sentence_terminator
  - decimal_separator (locale-dependent)
  - abbreviation_marker
  - path_component_separator (filesystem/domain contexts)

WHAT_THIS_SIGN_IS_NOT:
  1. NOT_AUTHORITY — the dot does not confirm the official status of a text
  2. NOT_EXISTENCE_PROOF — the dot does not prove the existence of a
     mentioned object
  3. NOT_VERIFICATION — the dot does not verify the fact it stands next to
  4. NOT_COMPLETION_PROOF — a dot after a line does not guarantee that
     the thought is actually complete (may be a cut-off)
  5. NOT_SENTENCE_BOUNDARY_GUARANTEE — a dot does not always mean the
     end of a sentence (abbreviations, initials, software versions, IPs)
  6. NOT_DECIMAL_GUARANTEE — the dot is not always a decimal separator
     (locale-dependent — in some systems the separator is a comma)
  7. NOT_FILE_EXTENSION_GUARANTEE — a dot before letters does not
     guarantee it is a file extension
  8. NOT_DOMAIN_VALIDATION — the dot in "example.com" does not confirm
     the domain is real or safe
  9. NOT_EXECUTION_TRIGGER — the dot by itself launches no action
  10. NOT_TRUST_SIGNAL — an abundance of dots (e.g. "...") does not
     increase trust in the content

BASE_FORMULAS:
  DOT_FORM ≠ SENTENCE_END_PROOF
  DOT_FORM ≠ DECIMAL_SEPARATOR_PROOF
  DOT_FORM ≠ FILE_EXTENSION_PROOF
  DOT_FORM ≠ DOMAIN_VALIDITY_PROOF
  DOT_FORM ≠ ABBREVIATION_PROOF
  DOT_FORM ≠ COMPLETION_PROOF
  DOT_FORM ≠ AUTHORITY
  DOT_FORM ≠ EXECUTION_TRIGGER
  DOT_FORM ≠ TRUST_SIGNAL
  DOT_FORM ≠ VERSION_VALIDITY_PROOF

============================================================
5. SEMANTIC_EPOCH_TRACKER
SEMANTIC_EPOCH_TRACKER_LOCK: REVIEWABLE
============================================================

EPOCH_TRACKER: NOT_APPLICABLE
NOTE: DOT (ZONE_1) has several parallel functions (sentence
  terminator, decimal separator, abbreviation marker, path/domain
  component separator), but these functions exist SIMULTANEOUSLY in
  modern usage, without cultural precession of one function by another
  over time. This is polysemy of a single stable sign, not epoch
  change — therefore SEMANTIC_EPOCH_TRACKER does not apply.

LAYER_ANOMALY:
  ABSENT_PHYSICAL_LAYER: YES, level L1 (physical gesture)
  NOTE: the dot as a written sign has no physical gestural predecessor
    (unlike, for example, signs derived from manual gestures) — it
    arose directly as a written punctuation convention in ancient
    writing for marking up text.

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

============================================================
7. SAFE / RISK / CONFUSABLES / GUARDS — LAYER_B: SEMI-STABLE LAYER
LAYER_B_LOCK: REVIEWABLE
============================================================

SAFE_CASES:
  SAFE_CASE_001:
    INPUT: "End of sentence."
    CONTEXT: completion of an ordinary sentence
    EXPECTED: INFO
    RISK: NONE
    GUARD: DOT_FORM ≠ SENTENCE_END_PROOF (advisory only)

  SAFE_CASE_002:
    INPUT: "3.14"
    CONTEXT: decimal fraction in mathematical/numeric text
    EXPECTED: INFO
    RISK: NONE
    GUARD: DOT_FORM ≠ DECIMAL_SEPARATOR_PROOF

  SAFE_CASE_003:
    INPUT: "Mr. Smith"
    CONTEXT: abbreviation (after "Mr")
    EXPECTED: INFO
    RISK: NONE
    GUARD: DOT_FORM ≠ ABBREVIATION_PROOF

  SAFE_CASE_004:
    INPUT: "document.pdf"
    CONTEXT: separator between file name and extension
    EXPECTED: INFO
    RISK: NONE
    GUARD: DOT_FORM ≠ FILE_EXTENSION_PROOF

  SAFE_CASE_005:
    INPUT: "version 2.5.1"
    CONTEXT: separator of version-number components
    EXPECTED: INFO
    RISK: NONE
    GUARD: DOT_FORM ≠ VERSION_VALIDITY_PROOF

  SAFE_CASE_006:
    INPUT: "Please wait..."
    CONTEXT: ellipsis (triple dot) as an indicator of
      continuation/incompleteness of a thought
    EXPECTED: INFO
    RISK: NONE
    GUARD: DOT_FORM ≠ COMPLETION_PROOF

RISK_CASES:
  RISK_CASE_001:
    NAME: FAKE_OFFICIAL_NOTATION
    INPUT: "Notice No.A.1.7-OFFICIAL from management."
    CONTEXT: imitation of a formal/bureaucratic style through an
      abundance of dots in numbers and abbreviations
    RISK: LOW
    ATTACK: dots in pseudo-indices create the illusion of official
      document circulation, though the dot itself does not confirm the
      legitimacy of the source
    GUARD: DOT_FORM ≠ AUTHORITY

  RISK_CASE_002:
    NAME: DOMAIN_LOOKALIKE_VIA_DOT_PLACEMENT
    INPUT: "paypal.com.security-check.ru"
    CONTEXT: a phishing URL where dots create the illusion of a
      subdomain of a legitimate service
    RISK: HIGH
    ATTACK: placing dots so that the real domain ("security-check.ru")
      is visually hidden behind a subdomain that looks legitimate
    GUARD: DOT_FORM ≠ DOMAIN_VALIDITY_PROOF

  RISK_CASE_003:
    NAME: VERSION_NUMBER_TRUST_INFLATION
    INPUT: "Tested in version 99.9.9.9 — absolutely safe"
    CONTEXT: use of a long, "technical-looking" dotted version to
      create the illusion of thorough verification
    RISK: LOW
    ATTACK: the number of dots/digits in a version number does not
      correlate with the real reliability of the claim
    GUARD: DOT_FORM ≠ VERSION_VALIDITY_PROOF

  RISK_CASE_004:
    NAME: ABBREVIATION_AUTHORITY_MIMICRY
    INPUT: "Per the conclusion of Ph.D. and Sc.D. holders, the product
      is certified"
    CONTEXT: use of dotted academic-degree abbreviations without
      verifying that the degree is real
    RISK: MEDIUM
    ATTACK: a dotted abbreviation looks like formal confirmation of
      qualification, though the dot itself verifies neither the
      existence of the degree nor the identity
    GUARD: DOT_FORM ≠ AUTHORITY

  RISK_CASE_005:
    NAME: ELLIPSIS_AS_FALSE_CONTINUATION_SIGNAL
    INPUT: "We guarantee results... details on request"
    CONTEXT: the ellipsis is used to hint at the existence of hidden,
      fuller information that may not actually exist
    RISK: LOW
    ATTACK: creates a false sense that there is a weighty continuation
      of the argument, though the ellipsis is just a punctuation device
    GUARD: DOT_FORM ≠ COMPLETION_PROOF

  RISK_CASE_006:
    NAME: NUMERIC_OBFUSCATION_VIA_DOT_INSERTION
    INPUT: "1.92.168.1.1" (instead of the correct "192.168.1.1")
    CONTEXT: adding an extra dot to an IP-like string to bypass simple
      pattern validation or confuse an automatic parser
    RISK: MEDIUM
    ATTACK: non-standard dot placement can fool regex validators that
      blindly trust the presence of dots as a sign of a valid IP address
    GUARD: DOT_FORM ≠ DECIMAL_SEPARATOR_PROOF (as applied to network
      addresses — a separate advisory format check)

CONFUSABLES:
  CONFUSABLE_001:
    VISIBLE_FORM: ‧
    CODEPOINT: U+2027
    NAME: HYPHENATION POINT
    RISK: LOW
    RULE: HYPHENATION_POINT ≠ FULL_STOP

  CONFUSABLE_002:
    VISIBLE_FORM: ·
    CODEPOINT: U+00B7
    NAME: MIDDLE DOT
    RISK: MEDIUM
    RULE: MIDDLE_DOT ≠ FULL_STOP

  CONFUSABLE_003:
    VISIBLE_FORM: 。
    CODEPOINT: U+3002
    NAME: IDEOGRAPHIC FULL STOP
    RISK: MEDIUM
    RULE: IDEOGRAPHIC_FULL_STOP ≠ FULL_STOP (visually similar, used in
      CJK texts, may mask domains/strings when mixed with the standard dot)

  CONFUSABLE_004:
    VISIBLE_FORM: ٠
    CODEPOINT: U+0660
    NAME: ARABIC-INDIC DIGIT ZERO
    RISK: LOW
    RULE: ARABIC_INDIC_ZERO ≠ FULL_STOP (risk of confusion in mixed
      RTL/LTR numeric strings)

  CONFUSABLE_005:
    VISIBLE_FORM: ｡
    CODEPOINT: U+FF61
    NAME: HALFWIDTH IDEOGRAPHIC FULL STOP
    RISK: MEDIUM
    RULE: HALFWIDTH_IDEOGRAPHIC_FULL_STOP ≠ FULL_STOP (used in
      Japanese/Korean texts, a potential vector for bypassing filters
      that look only for the standard dot U+002E)

  CONFUSABLE_006:
    VISIBLE_FORM: ․
    CODEPOINT: U+2024
    NAME: ONE DOT LEADER
    RISK: MEDIUM
    RULE: ONE_DOT_LEADER ≠ FULL_STOP (a direct typographic twin of the
      dot, visually almost indistinguishable from U+002E in most fonts
      — the most precise visual confusable of all those listed)

CONTRADICTION_GUARDS:
  CG1:
    TRIGGER: "a dot at the end of a text confirms that the thought is
      fully complete"
    RESPONSE: DOT_FORM ≠ COMPLETION_PROOF
    RULE: the dot is a punctuation marker, not a guarantee of semantic
      completeness

  CG2:
    TRIGGER: "a dot as a decimal separator means the number is correct
      across all locales"
    RESPONSE: DOT_FORM ≠ DECIMAL_SEPARATOR_PROOF
    RULE: interpreting the dot as a decimal separator is locale-
      dependent; in some systems that role belongs to the comma

  CG3:
    TRIGGER: "a domain with dots like paypal.com.xyz.ru is a subdomain
      of paypal.com"
    RESPONSE: DOT_FORM ≠ DOMAIN_VALIDITY_PROOF
    RULE: the visual presence of dots does not determine the real
      domain hierarchy — DNS decides that, not a text pattern

  CG4:
    TRIGGER: "an abbreviation with a dot (e.g. 'Ph.D.') confirms the
      reality of an academic degree or position"
    RESPONSE: DOT_FORM ≠ AUTHORITY
    RULE: a dot in an abbreviation is a spelling convention, not a
      mechanism for verifying qualification

  CG5:
    TRIGGER: "a long version number with many dots ('9.9.9.9') means
      more thorough testing or product reliability"
    RESPONSE: DOT_FORM ≠ VERSION_VALIDITY_PROOF
    RULE: the number of version-number components does not correlate
      with quality or safety

  CG6:
    TRIGGER: "a dot after a file ('document.pdf') guarantees the file
      is really a PDF and is safe"
    RESPONSE: DOT_FORM ≠ FILE_EXTENSION_PROOF
    RULE: the extension after the dot is a declared, not
      cryptographically confirmed, file type; the real format may
      differ (e.g. an executable renamed with a .pdf extension)

SEQUENCE_LAYER_BOUNDARY:
  SIGN_SAFE_ALONE ≠ SIGN_SAFE_IN_SEQUENCE: YES
  SEQUENCE_CANDIDATES:
    SC1:
      SEQUENCE: ".." (two dots in a row)
      NAME: DOUBLE_DOT
      RISK_LEVEL: MEDIUM
      POSSIBLE_CONTEXTS: filesystem "parent directory" path (../),
        potential directory traversal in paths, typo
      REQUIRES_SEQUENCE_INTEGRATOR: YES

    SC2:
      SEQUENCE: "..." (three dots, ellipsis)
      NAME: ELLIPSIS_SEQUENCE
      RISK_LEVEL: LOW
      POSSIBLE_CONTEXTS: rhetorical device of incompleteness,
        manipulative creation of a false sense of "continuation"
        (see RISK_CASE_005)
      REQUIRES_SEQUENCE_INTEGRATOR: NO (an advisory flag at the level
        of a single MODULE is sufficient)

    SC3:
      SEQUENCE: "../../../" (multiple double dots with path separators)
      NAME: PATH_TRAVERSAL_PATTERN
      RISK_LEVEL: HIGH
      POSSIBLE_CONTEXTS: the classic directory-traversal attack
        pattern for escaping the permitted directory
      REQUIRES_SEQUENCE_INTEGRATOR: YES

  IF NOT_APPLICABLE: not applicable — the sequences above are real and
    significant.

PHAGO_ENTITY_MIMICRY:
  NOT_APPLICABLE:
    REASON: the dot by itself does not imitate the existence of a
      verified entity (organization, account, product) — unlike, for
      example, the @ sign (mimicry of a verified account) or # (mimicry
      of an official tag/category). The dot's risks (see RISK_CASES
      above) relate to masking domains and creating a false sense of
      formality, but not to the direct imitation of a specific verified
      entity.
    REVIEW_REQUIRED: YES

============================================================
8. ADVERSARIAL_COVERAGE — RUN_CARD SEED
============================================================

MIN_TOTAL_VECTORS: 10 (5 categories A-E, 2 per category;
  CATEGORY_F = NOT_APPLICABLE for ZONE_1, see below)

CATEGORY_A: FORM_MANIPULATION (3)
  A1: substitution of U+002E with CONFUSABLE_002 (MIDDLE DOT, U+00B7)
    in a domain name for visual deception
  A2: substitution of U+002E with CONFUSABLE_003 (IDEOGRAPHIC FULL
    STOP, U+3002) in mixed CJK/Latin text
  A3: substitution of U+002E with CONFUSABLE_006 (ONE DOT LEADER,
    U+2024) in Latin text — the most precise visual twin of all the
    confusables, the least noticeable substitution for a human

CATEGORY_B: CONTEXT_INJECTION (2)
  B1: inserting a dot into a number to imitate a decimal fraction where
    an integer is expected (e.g. the price "100.00" instead of "10000"
    to visually reduce the amount)
  B2: using a dot as a separator in a pseudo-official document number
    to imitate bureaucratic numbering (see RISK_CASE_001)

CATEGORY_C: SEQUENCE_MANIPULATION (2)
  C1: a ".." chain in a path for directory traversal (see SC1, SC3)
  C2: multiple dots "....." as a visual separator masking the end of
    one semantic unit and the start of another in phishing text

CATEGORY_D: SEMANTIC_MIMICRY (2 minimum)
  D1: imitation of a software version with a long dotted number to
    create the illusion of "verified" status (see RISK_CASE_003)
  D2: imitation of an academic abbreviation with dots to create the
    illusion of expert confirmation (see RISK_CASE_004)

CATEGORY_E: PHAGO_ENTITY_MIMICRY (2)
  E1: the dot in "paypal.com.fake-domain.ru" as part of a pattern
    masking the real domain as a legitimate service (see RISK_CASE_002)
  E2: the dot as a separator in a file name, masking the real
    extension (e.g. "invoice.pdf.exe" — the dot before "exe" is
    visually less noticeable after the already-familiar ".pdf")

CATEGORY_F: SEMANTIC_LAYER_MANIPULATION
  NOT_APPLICABLE
  REASON: ZONE_1, the dot has no dormant/active epochs (see section 5,
    SEMANTIC_EPOCH_TRACKER: NOT_APPLICABLE) — category F tests the
    reactivation of an obsolete epoch of a sign, which is inapplicable
    to a sign without epochs.

ACTUAL_TOTAL_VECTORS: 11
COVERAGE_STATUS: SUFFICIENT (11 ≥ 10)

============================================================
9. MUTATION_CHECK
============================================================

MUTATION_01:
  CLAIM: a dot at the end of a phrase proves the author finished the thought
  EXPECTED: FAIL_COMPLETION_MIMICRY
  RESULT: FAIL

MUTATION_02:
  CLAIM: a dot as a decimal separator behaves identically across all
    locales and number systems
  EXPECTED: FAIL_LOCALE_ASSUMPTION_MIMICRY
  RESULT: FAIL

MUTATION_03:
  CLAIM: a domain with dots in any placement forms a legitimate
    subdomain structure of a known brand
  EXPECTED: FAIL_DOMAIN_AUTHORITY_MIMICRY
  RESULT: FAIL

MUTATION_04:
  CLAIM: a dotted academic-degree abbreviation confirms the reality of
    the named person's qualification
  EXPECTED: FAIL_AUTHORITY_MIMICRY
  RESULT: FAIL

MUTATION_05:
  CLAIM: a file extension after a dot guarantees the real format and
    safety of the file
  EXPECTED: FAIL_FILE_TYPE_TRUST_MIMICRY
  RESULT: FAIL

MUTATION_06:
  CLAIM: a ".." sequence in a path is always safe for runtime because
    it looks like ordinary punctuation
  EXPECTED: FAIL_SEQUENCE_SAFETY_MIMICRY
  RESULT: FAIL

============================================================
10. KNOWN_OPEN_QUESTIONS
============================================================

ALL_OPEN_QUESTIONS_CLOSED: YES (no open questions identified at fill time)

============================================================
11. PATCH_HISTORY
============================================================

PATCH_HISTORY:
  v0_1_PATCH_01: Initial creation (Ruslan Malyavsky, 2026-06-23) — the
    first card filled from the SIGN_CORE_CARD_TEMPLATE GEN3_v0_3
    template; the first practical test of the new template.
  v0_1_PATCH_02: SIGN → VISIBLE_FORM in CONFUSABLES (author,
    2026-06-23) — renaming of the NAMING_NORM-forbidden field in all
    five CONFUSABLE_00X, synchronously with the template patch
    (PATCH_NOTE_TEMPLATE_v0_3_P1).
    REASON: STRUCTURAL_PREFLIGHT_PASS finding — PROHIBITED_FIELD_USED

  v0_1_PATCH_03: CONFUSABLE_006 added — U+2024 ONE DOT LEADER (conveyor
    review CONVEYOR_RUN_PACKET_DOT_CONTENT_REVIEW_v0_1, 2026-06-23) — a
    sixth confusable was added that was not in the original card.
    REASON: convergent finding by three reviewers from different model
    families (Kimi, Gemini, GPT-5.5), independently pointing to this
    codepoint as a missed direct typographic twin of the dot.
    REJECTED_FINDINGS_FROM_THIS_REVIEW_ROUND (checked by the
      coordinator personally against the primary source, per the
      VERIFY_BEFORE_TRUST_MANDATORY rule, and rejected):
      - Qwen m2/m3/m4 (MUTATION_03/05/06 EXPECTED does not match the
        BASE_FORMULA name) — the template defines EXPECTED as a free
        description FAIL_<substitution_type>; there is no requirement
        of a literal match with the BASE_FORMULA name in either the
        template or the ruleset.
      - GPT-5.5 (U+FF0E "was in the card, then disappeared") —
        incorrect as a fact: U+FF0E does not appear in any version of
        the card.
      - GPT-5.5 (clarify the GUARD wording in RISK_CASE_006 for the IP
        context) — the clarification "(as applied to network addresses
        — a separate advisory format check)" is already present in the card.
      - Qwen m1 (replace U+0660 with U+2024) — the replacement was
        rejected, U+0660 retained: a confusable is defined by visual
        similarity of shape, not by symbol category; U+2024 was added
        separately, not as a replacement.

  v0_1_PATCH_04: ADVERSARIAL_COVERAGE CATEGORY_A vector A3 added —
    reference to CONFUSABLE_006 (Kimi, repeat round after patch_03,
    2026-06-23) — vector A3 added (substitution of U+002E with
    CONFUSABLE_006 in Latin text), ACTUAL_TOTAL_VECTORS updated 10→11.
    REASON: Kimi's finding — A1/A2 did not mention CONFUSABLE_006, the
    most precise visual twin of the dot of all confusables, confirmed
    by the coordinator via direct check of the file.

PATCHES_APPLIED: 5
PATCHES_VERIFIED: 2/5
  (v0_1_PATCH_03 and v0_1_PATCH_04 are now CONVEYOR_VERIFIED — this was
  the purpose of the separate PATCH_03_04_VERIFICATION round (5
  reviewers: Kimi, Gemini, GPT-5.5, Qwen, Grok), which directly checked
  their content against questions Q1/Q2 and confirmed them
  independently. v0_1_PATCH_05 (fix to the CATEGORY_A header) is a
  finding from the SAME round, but the fix itself was applied by the
  coordinator after the round and was not re-checked by the conveyor;
  v0_1_PATCH_01/02 are not conveyor checks by definition (author
  creation / mechanical self-check))
  v0_1_PATCH_01: VERIFIED_BY: AUTHOR (initial creation, not a conveyor
    check by definition)
  v0_1_PATCH_02: VERIFIED_BY: COORDINATOR (STRUCTURAL_PREFLIGHT_PASS, a
    mechanical check, not the conveyor)
  v0_1_PATCH_03: ORIGINALLY VERIFIED_BY: COORDINATOR_ARBITRATION_ONLY,
    NOW: CONVEYOR_VERIFIED (see PATCH_03_04_VERIFICATION_ROUND_RESULT
    below). At the time of application (2026-06-23, earlier the same
    day) the patch was the result of the coordinator's arbitration of
    discrepancies, not a repeat conveyor run — no external model had
    seen it. After that, a separate packet
    CONVEYOR_RUN_PACKET_DOT_PATCH_03_04_VERIFICATION_v0_1 was prepared,
    and 5 reviewers (Kimi, Gemini, GPT-5.5, Qwen, Grok — this is the
    full and exact list of participants; the mention of "Copilot" as a
    participant in one earlier draft was erroneous, Copilot did not
    participate in any round of this project) confirmed the content of
    patch_03 independently (question Q1 of the verification packet).
  v0_1_PATCH_04: ORIGINALLY VERIFIED_BY: COORDINATOR (Kimi's finding
    about CATEGORY_A, confirmed by the coordinator via direct check of
    the file), NOW: CONVEYOR_VERIFIED — the same
    PATCH_03_04_VERIFICATION round confirmed vector A3 and recomputed
    ACTUAL_TOTAL_VECTORS=11 independently (question Q2 of the
    verification packet), by all 5 reviewers.
  NOTE_ON_PATCHES_APPLIED_VS_VERIFIED_RATIO: the formal rule
    "PATCHES_APPLIED = PATCHES_VERIFIED — mandatory equality" exists in
    SPEC_MSL_MIP_FOUNDATION (CONVEYOR_PASS_CRITERIA for the
    v0_2_PLUS_EPOCH discipline), but is NOT fixed as mandatory in
    SIGN_CORE_CARD_CONVEYOR_RULES_GEN3_v0_3 (section 4 of v0_3
    describes only the patch-record format, without requiring end-to-
    end equality). This card follows CONVEYOR_DISCIPLINE_VERSION: v0_3,
    so the current 2/5 ratio is not a violation of the fixed rule — it
    is a transparently documented asymmetry, not a blocker.
    (Reviewer Qwen in the second round referred to this rule as
    "section 4 of the v0_3 rules" — this is an incorrect attribution,
    checked by the coordinator personally via grep over both documents,
    and confirmed independently by the 5 reviewers of the
    PATCH_03_04_VERIFICATION round, question Q5.)
  COORDINATOR_ARBITRATION ≠ CONVEYOR_REVIEW
  CONVEYOR_REVIEW_PASS refers to the content of the card at the time of
    submission to the packet (v0_1_PATCH_02), not to a patch added
    after it

  v0_1_PATCH_05: CATEGORY_A header "(2)" → "(3)" (Qwen,
    PATCH_03_04_VERIFICATION round, 2026-06-23) — the CATEGORY_A:
    FORM_MANIPULATION header was not updated after vector A3 was added
    by patch_04 and continued to show (2) with three actual vectors
    (A1, A2, A3). Checked by the coordinator directly against the file.
    VERIFIED_BY: COORDINATOR (Qwen's finding from the verification
      round, but the header fix itself was applied by the coordinator
      after the round and was not re-checked by the conveyor —
      analogous to the original status of patches 03/04 before their
      own verification)

  PATCH_03_04_VERIFICATION_ROUND_RESULT (a separate conveyor round, 5
    reviewers — Kimi, Gemini, GPT-5.5, Qwen, Grok, 2026-06-23):
    ARBITRATION_CONFIRMED: YES on all four points (Q3–Q6) — all
      previous coordinator rejections (EXPECTED/BASE_FORMULA mismatch,
      the "disappeared" U+FF0E, the PATCHES_APPLIED=PATCHES_VERIFIED
      rule attribution, the U+0660 replacement) confirmed 4/4
      independently.
    Q1/Q2 (content of patches 03/04): confirmed 5/5 — this is the basis
      for marking these two patches as CONVEYOR_VERIFIED above.
    The only new finding — the CATEGORY_A header "(2)" instead of "(3)"
      (Qwen) — patch_05 above.
    VERDICT: ACCEPT (Kimi, Gemini, GPT-5.5, Grok) /
      ACCEPT_WITH_PATCHES (Qwen, the only MINOR finding)

============================================================
12. LIMITATION_STATEMENT
============================================================

LIMITATION_STATEMENT:
  THIS_CARD IS AN ARTIFACT_CONFIRMED ARTIFACT (passed
    STRUCTURAL_PREFLIGHT_PASS, CONVEYOR_REVIEW_PASS, SIMULATION_GATE
    TIER_1 — the final status for the GEN3_v0_3 methodology)
  NOT A FINAL_STANDARD
  NOT A PARSER
  NOT A RUNTIME
  NOT A SECURITY_CERTIFICATE
  NOT PRODUCTION_READY (ARTIFACT_CONFIRMED ≠ PRODUCTION_READY — the
    simulation covered 2 contexts, not exhaustive testing)
  CONVEYOR_PASS ≠ VALIDATION
  RUN_CARD_RESULT ≠ FINAL_STATUS
  WORKINGLY_CLOSED ≠ ARTIFACT_CONFIRMED (passed, both statuses obtained
    in sequence)
  WORKINGLY_CLOSED ≠ LOCKED_WORKING_CORE
  ARTIFACT_CONFIRMED ≠ LOCKED_WORKING_CORE
  MODEL_CONSENSUS ≠ TRUTH

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
