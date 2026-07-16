PRIVATE AUTHORED PROJECT / COMMERCIAL USE PROHIBITED

CARD_UID: SIGN_CORE_CARD_ZERO_WIDTH_SPACE_U200B_GEN3_v0_3_EN
CODEPOINT: U+200B
VISIBLE_FORM: ​
INSPECTION_LABEL: ⟦ZWSP U+200B⟧
  [human-readable marker field: VISIBLE_FORM above contains the LITERAL invisible
   U+200B (runtime scans text for it). A human cannot read VISIBLE_FORM —
   INSPECTION_LABEL closes the inspection crack.]
UNICODE_NAME: ZERO WIDTH SPACE
ZONE: ZONE_2
DOCUMENT_STATUS: WORKINGLY_CLOSED
LIFECYCLE_STATUS: WORKINGLY_CLOSED_PENDING_CLASS_GUARD
  [REAL lifecycle position (AUTHOR_DECISION D-ZWSP-WORKINGLY-CLOSED 2026-07-15;
   raised from VALIDATED_BY_TOOL/PENDING_CONVEYOR_REVIEW per D-ZWSP-STATUS
   2026-07-13 — step 2 of PATH_TO_ARTIFACT closed).
   DOCUMENT_STATUS above was raised WORKING_DRAFT → WORKINGLY_CLOSED — this is a
   MACHINE-GATE field (module_engine._VALID_STATUSES). Basis for the flip: the code
   defines _VALID_STATUSES as "passed STRUCTURAL_PREFLIGHT_PASS + CONVEYOR_REVIEW_PASS
   (several independent reviewers) + AUTHOR_DECISION" — ALL THREE conditions are met
   (preflight 35/0/1; external conveyor 8/8 ACCEPT; this decision). Keeping WORKING_DRAFT
   is no longer possible: the warning CARD_NOT_CONVEYOR_REVIEWED ("did not pass preflight/
   conveyor") would become FALSE — claim≠reality in the opposite direction. The runtime
   CORRECTLY stops warning. The _PENDING_CLASS_GUARD qualifier lives here, in
   LIFECYCLE_STATUS (the code does not know that string — in DOCUMENT_STATUS it would be
   CARD_INVALID); the class guard per D-ZWSP-STATUS Q2 is a CLASS dependency, NOT a blocker.
   Code is UNtouched — only a card field changes. ARTIFACT_CONFIRMED stays PENDING until the
   guard is built — see PATH_TO_ARTIFACT below.]
VALIDATION_METHOD: TWO_LEGGED_SIMULATION + MUTATION_ADEQUACY_5/5 + RECONCILE_BY_TUPLE
CLASS_ROLE: METHOD_REFERENCE_SPECIMEN
  [first invisible sign of the class run through the strict instrument — a method reference]
TEMPLATE_LINE: GEN3_v0_3
SOURCE_TEMPLATE: SIGN_CORE_CARD_TEMPLATE_GEN3_v0_3_R1_RU
AUTHOR: Руслан Малявский
CREATED_AT: 2026-07-12
VERSION: v0_1

TRANSLATION_NOTE: This is the English MEANING-MIRROR of
  SIGN_CORE_CARD_ZERO_WIDTH_SPACE_U200B_GEN3_v0_3_RU (per rule
  RULE_CARD_EN_ON_CLOSE_v0_1: EN is a mirror of meaning, not a literal
  word-for-word translation). The Russian version remains AUTHORITATIVE by
  meaning. Field names, status tokens, codepoints, hashes, numbers and formulas
  are kept IDENTICAL to the Russian version. Coined terms are mirrored as
  CONCEPTS with fixed English equivalents: поднадзорный класс = supervised class;
  образцы = samples (exemplars); свидетель, не судья = witness, not judge;
  реестратор = registrar; обещания=реальность = claims = reality. INPUT examples
  keep the same threat pattern (homoglyph + invisible break); Russian prose words
  inside examples are rendered in English, the attack itself is unchanged.

AUTHOR_DECISION_REFERENCE: foundation_layer/AUTHOR_DECISION_20260712_INVISIBLE_SIGNS_D-INV-1_2_3.md
AUTHOR_DECISION_REFERENCE_STATUS: foundation_layer/AUTHOR_DECISION_20260713_D-ZWSP-STATUS.md; foundation_layer/AUTHOR_DECISION_20260715_D-ZWSP-WORKINGLY-CLOSED.md
RUN_CARD_REFERENCE: conveyor_runs/SIMULATION_ARTIFACT_ZERO_WIDTH_SPACE_U200B_TIER2_BY_CODE_v0_3_RU.md
  (passing BY_CODE artifact from the real run of 2026-07-15, ENGINE_COMMIT 9963a68,
   RAW+hashes inside; v0_2 = SUPERSEDED pre-patch snapshot HONEST_FAIL 6/21)
RUN_CARD_STATUS: SIMULATION_DONE (BATTERY_RESULT: 21/21; BY_CODE, mutation-adequacy 5/5; U1/D2 closed by F-NEW-4/5)
BY_SPEC_STATUS: NOT_AVAILABLE (no BY_SPEC leg; two-legged/reconcile NOT claimed —
  the run's independent anchor is the machine oracle tests/zwsp_oracle_manifest.py)
PATH_TO_ARTIFACT:
  1. STRUCTURAL_PREFLIGHT_PASS + CONVEYOR_REVIEW_PASS — PASSED (preflight 35/0/1;
     external conveyor 8/8 ACCEPT, PASS_WITH_PATCHES). Canonical order restored.
  2. → WORKINGLY_CLOSED_PENDING_CLASS_GUARD — REACHED (AUTHOR_DECISION
     D-ZWSP-WORKINGLY-CLOSED, 2026-07-15; DOCUMENT_STATUS=WORKINGLY_CLOSED).
  3. build INVISIBLE_DEFAULT_IGNORABLE_GUARD (from >=3 different invisibles) + re-validation
       ← NEXT STEP (CLASS_FRONT, not a blocker — per D-ZWSP-STATUS Q2)
  4. → ARTIFACT_CONFIRMED
DISPLAY_NAME: zero width space (invisible zero-advance-width space)

============================================================
1. UNIVERSALITY / CONVEYOR_DISCIPLINE
============================================================
BOUND_TO_SPECIFIC_SIGN: YES
AFTER_USE_RESIDUE: FORBIDDEN
SIGN_DATA_IS_SESSION_ONLY: YES
STATUS_PROGRESSION_TRACKER:
  WORKING_DRAFT: NO (superseded — DOCUMENT_STATUS raised to WORKINGLY_CLOSED, D-ZWSP-WORKINGLY-CLOSED 2026-07-15)
  STRUCTURAL_PREFLIGHT_PASS: PASS (self-check 2026-07-13: 35 PASS / 0 FAIL / 1 PRECEDENT — CONFUSABLES arbitration)
  CONVEYOR_REVIEW_PASS: PASS_WITH_PATCHES (2026-07-14, 8/8 ACCEPT; BY_CODE recheck + doc-sync applied)
  WORKINGLY_CLOSED: DONE (WORKINGLY_CLOSED_PENDING_CLASS_GUARD — AUTHOR_DECISION D-ZWSP-WORKINGLY-CLOSED 2026-07-15; DOCUMENT_STATUS=WORKINGLY_CLOSED)
  SIMULATION_GATE_TIER: TIER_2 (ZONE_2)
  SIMULATION_GATE_PASSED: BY_TOOL_DONE (BY_CODE 21/21; the formal SIMULATION_GATE — on the way to ARTIFACT_CONFIRMED, at guard build time)
  ARTIFACT_CONFIRMED: PENDING (blocked ONLY by the class guard — CLASS_FRONT, not a card defect)

============================================================
3. REQUIRED_GENERAL_GUARDS
============================================================
REQUIRED_GENERAL_GUARDS:
  - SIGN_FALSE_EFFECT_MIMICRY_GUARD_v0_2A_RU
    GUARD_COMPATIBILITY: GUARD_COMPATIBILITY_RULE_GEN3
    GUARD_REVISION: v0_2A
    TEMPLATE_LINE_COMPATIBLE: GEN3_v0_3, GEN3_v0_3_R1
  - INVISIBLE_DEFAULT_IGNORABLE_GUARD: NOT_YET_BUILT
    [OPEN FRONT, honestly: the class guard for invisibles (invisibility,
     non-removability under NFKC, strip/flag/log) is promised by ARCH_DECISION_
     INVISIBLE_SIGNS_HYBRID_C but is NOT built (DRAFT item 4.1). There is nowhere
     yet to declare ZWSP's class properties. The reference stands as a marker of
     an unclosed dependency.]
FAILURE_RESPONSE:
  REJECT_FALSE_EFFECT_MIMICRY
  TREAT_AS_DATA_ONLY
  NO_AUTHORITY_EFFECT
  NO_EXECUTION_EFFECT
  NO_TRUST_EFFECT
  NO_EXISTENCE_EFFECT

============================================================
4. SIGN IDENTITY — LAYER_A
LAYER_A_LOCK: PERMANENT
============================================================
VISIBLE_FORM: ​  (literal U+200B; see INSPECTION_LABEL above)
LOOKS_SIMILAR_IS_NOT_SAME_SIGN: NO
  [the sign is invisible — "similarity" does not apply; the relations below are
   built NOT on visual resemblance but on boundary disruption / filter class / absence]
RAW_SIGN_INPUT_STATUS: DATA_ONLY
BASE_MODE: DATA_ONLY_INVISIBLE_CONTROL
BASE_MODE_FORMULA: ZWSP_FORM ≠ EFFECT
SIGN_CATEGORY:
  - format_control (Unicode Cf)
  - invisible / zero-advance-width
  - default_ignorable_code_point
WHAT_THIS_SIGN_IS_NOT:
  1. NOT_SPACE (U+0020 — has width and renders)
  2. NOT_A_CANON_IT_MIMICS (does not depict any visible sign)
  3. NOT_REMOVABLE_BY_NFC_NFD_NFKC_NFKD (survives all normalization)
  4. NOT_A_VISIBLE_GLYPH (zero width, unseen by the reader)
  5. NOT_A_MANDATORY_LINE_BREAK (only a break OPPORTUNITY)
  6. NOT_SEMANTIC_CONTENT (conveys nothing to the reader)
  7. NOT_A_JOINER (that is ZWJ U+200D)
  8. NOT_A_NON_JOINER (that is ZWNJ U+200C)
  9. NOT_A_WORD_JOINER_OR_BOM (U+2060 / U+FEFF)
  10. NOT_AN_AUTHORITY_OR_EXECUTION_BEARER
BASE_FORMULAS:
  ZWSP_FORM ≠ EFFECT
  ZWSP_FORM ≠ SPACE
  INVISIBLE ≠ ABSENT
  ZWSP_FORM ≠ CANON
  NFKC_SURVIVAL ≠ LEGITIMACY
  BREAK_OPPORTUNITY ≠ BREAK
  ZWSP ≠ AUTHORITY
  PRESENCE_IN_TOKEN ≠ TOKEN_STRUCTURE
  ZWSP_FORM ≠ VISUAL_MIMICRY
  ZWSP_PRESENCE ≠ WORD_BOUNDARY_MEANING

============================================================
5. SEMANTIC_EPOCH_TRACKER  (ZONE_2)
SEMANTIC_EPOCH_TRACKER_LOCK: REVIEWABLE
============================================================
EPOCH_TRACKER: CONTEXT_GATE_REQUIRED
APPLICABILITY: APPLICABLE
REASON: the sign has two stable substrates: typographic (line breaking) and
  machine (byte-exact-match sabotage).
CAPTURE_HISTORY:
  EPOCH_1:
    DATE_RANGE: ~1991 (Unicode 1.0) — present
    SUBSTRATE: typography / text layout
    FUNCTION: an invisible LINE-BREAK POINT without a visible space
      (long URLs, word segmentation in Thai/CJK without spaces)
    EVIDENCE: Unicode Standard, UAX#14 (line breaking)
    STATUS: ACTIVE_IN_TYPOGRAPHY
  EPOCH_2:
    DATE_RANGE: ~2000s — present (the filter-evasion era)
    SUBSTRATE: Latin machine strings (domains, identifiers, code)
    FUNCTION: an invisible SABOTAGE of exact matching — breaking a token/
      domain/keyword to bypass byte-exact filters
    EVIDENCE: phishing / filter-evasion practice; detector probe 2026-07-12
    STATUS: ACTIVE_ATTACK
ACTIVE_EPOCH:
  STATUS: CONTEXT_GATE_REQUIRED
  PRIMARY_ACTIVE_EPOCH: NONE_GLOBAL
LAYER_ANOMALY:
  ABSENT_PHYSICAL_LAYER: YES (digital genesis; a control character; there NEVER
    was a glyph — neither written nor gestural)
  NOTE: a pure digital control with no physical substrate
STACK_RULES:
  Higher_epoch_suppresses_lower_in_modern_contexts: PARTIAL
  Lower_epoch_may_reactivate_in_historical_or_specialized_contexts: YES
  Context_gate_determines_active_epoch: REQUIRED
  Absent_layer_anomaly_must_be_flagged_for_integrator: YES

============================================================
6. EFFECT_FIELDS — LAYER_C
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
7. LAYER_B
LAYER_B_LOCK: REVIEWABLE
============================================================
SAFE_CASES:
  SAFE_CASE_001:
    INPUT: a long URL with ZWSP as a line-break point in layout
    CONTEXT: typography
    EXPECTED: INFO
    RISK: NONE
    GUARD: BREAK_OPPORTUNITY ≠ BREAK
  SAFE_CASE_002:
    INPUT: Thai/CJK text with ZWSP as a word segmenter
    CONTEXT: typography of non-spacing scripts
    EXPECTED: INFO
    RISK: NONE
    GUARD: ZWSP_PRESENCE ≠ WORD_BOUNDARY_MEANING
    SEMANTIC_STATUS: LEGITIMATE_USE
      [U+200B is line-break class ZW (UAX#14); in CJK/Thai it is a legitimate word
       segmenter, semantically safe]
    IMPLEMENTATION_STATUS: NOT_RECOGNIZED_WITHOUT_EXTERNAL_TYPOGRAPHY_CONTEXT
      [the detector does NOT tell typography from a machine string without an
       external typography context; this cannot be fixed in code — a heuristic
       "CJK=safe" would open a mask miss in a CJK DOMAIN (gоog<ZWSP>le.中国).
       Card honesty, not a heuristic — conveyor decision 5/5.]
    CURRENT_RUNTIME_EXPECTATION: MAY_QUEUE
      [a CJK token with ZWSP collapses into BYTE_EXACT_TOKEN → the detector MAY give
       MEDIUM/QUEUE. The card does NOT promise an automatic PASS the code does not
       deliver (claim=evidence). NOT a bug — an honest boundary until a typography
       context exists (v0.5). See T1 in the oracle manifest, OQ on typography context.]
  SAFE_CASE_003:
    INPUT: "the sign ZWSP has codepoint U+200B" (mention of the sign)
    CONTEXT: educational / quotation
    EXPECTED: INFO
    RISK: NONE
    GUARD: mention ≠ use
  SAFE_CASE_004:
    INPUT: an intentional ZWSP in a code string literal (test fixture)
    CONTEXT: source code with explicit intent
    EXPECTED: INFO
    RISK: NONE
    GUARD: ZWSP_FORM ≠ EFFECT
  SAFE_CASE_005:
    INPUT: a single ZWSP in free text with no structure
    CONTEXT: free text
    EXPECTED: INFO
    RISK: NONE
    GUARD: INVISIBLE ≠ ABSENT (but outside a protected context — not a threat)
  SAFE_CASE_006:
    INPUT: ZWSP in HTML markup as a soft-wrap hint
    CONTEXT: web layout
    EXPECTED: INFO
    RISK: NONE
    GUARD: BREAK_OPPORTUNITY ≠ BREAK
RISK_CASES:
  [RISK_CASE_RUNTIME_STATUS (claims=reality): VERIFIED — the case ACTUALLY fires on
   a run (probe 2026-07-12); PENDING — the system does NOT currently produce this
   case (context yields NONE, or a TAXONOMY_ONLY/SUPPORTING_FACET type emits no
   risk). The RISK level below = what the detector EMITS, not what is "wished for".
   The detector distinguishes contexts HOST/EMAIL/PATH/BYTE_EXACT_TOKEN/FREE_TEXT;
   it does NOT separately distinguish CODE and IDENTIFIER — see KNOWN_OPEN OQ4.]
  RISK_CASE_001:
    NAME: DOMAIN_LABEL_BREAK_EVASION
    INPUT: gоog​le.com (invisible label break)
    CONTEXT: HOST
    RISK: HIGH
    RUNTIME_STATUS: VERIFIED
    ATTACK: an invisible break of exact matching — a byte-exact blocklist misses the domain
    GUARD: the "relation" axis, edge BOUNDARY_DISRUPTOR, scope HOST
  RISK_CASE_002:
    NAME: KEYWORD_SPLIT_EVASION
    INPUT: bad​word (keyword split)
    CONTEXT: BYTE_EXACT_TOKEN
    RISK: MEDIUM
    RUNTIME_STATUS: VERIFIED
      [REALITY: the detector does not distinguish CODE/IDENTIFIER/policy — all
       collapse into BYTE_EXACT_TOKEN → MEDIUM (not HIGH). The card previously
       promised HIGH+CODE, which the system does not produce; brought to fact.
       Finer distinction — KNOWN_OPEN OQ4.]
    ATTACK: a keyword split bypasses an exact-match policy filter
    GUARD: edge BOUNDARY_DISRUPTOR, scope BYTE_EXACT_TOKEN
  RISK_CASE_003:
    NAME: ZWSP_PLUS_MASK_DOMAIN_BREAK
    INPUT: gоog​／le.com (ZWSP + mask break the domain together)
    CONTEXT: HOST
    RISK: HIGH
    RUNTIME_STATUS: VERIFIED
    ATTACK: a combination of invisible break and fullwidth mask —
      PROVEN by run (probe 2026-07-12, a known open hole)
    GUARD: BOUNDARY_DISRUPTOR + demask reconstructs the domain → HOST
  RISK_CASE_004:
    NAME: INVISIBLE_PADDING_HIDDEN_TEXT
    INPUT: invisible padding between characters to hide/inflate
    CONTEXT: FREE_TEXT
    RISK: NONE
    RUNTIME_STATUS: PENDING
      [HONESTLY: in FREE_TEXT the detector yields NONE, and ABSENCE_CONFUSABLE is now
       SUPPORTING_FACET (emits no standalone risk). The system does NOT currently
       raise this case — we do not pass it off as firing. Awaits a separate pass
       (detecting padding/inflation outside a protected context).]
    ATTACK: hidden text / invisible length inflation
    GUARD: edge ABSENCE_CONFUSABLE (evidence, not a standalone verdict)
  RISK_CASE_005:
    NAME: IDENTIFIER_TOKEN_SPLIT
    INPUT: user​name as a "different" identifier
    CONTEXT: BYTE_EXACT_TOKEN
    RISK: MEDIUM
    RUNTIME_STATUS: VERIFIED
      [REALITY: the detector's context is BYTE_EXACT_TOKEN (it has no IDENTIFIER/
       CODE); MEDIUM matched the run.]
    ATTACK: an identifier split bypasses name comparison
    GUARD: BOUNDARY_DISRUPTOR, scope BYTE_EXACT_TOKEN
  RISK_CASE_006:
    NAME: INVISIBLE_CLASS_FILTER_BYPASS
    INPUT: ZWSP where a crude filter "allows zero-width" expecting ZWJ
    CONTEXT: BYTE_EXACT_TOKEN
    RISK: NONE
    RUNTIME_STATUS: PENDING
      [HONESTLY: edge INVISIBLE_CLASS_COLLISION — TAXONOMY_ONLY: the behavior of the
       EXTERNAL crude filter is not observable from the input string, there is no
       runtime check, it emits no risk. The type is described but not passed off as a
       working contract. Awaits a separate pass on the cases.]
    ATTACK: an invisible passes via the allowance for ANOTHER invisible in a crude
      classifier (class, not Unicode function)
    GUARD: edge INVISIBLE_CLASS_COLLISION (TARGET_KIND: CLASS)
CONFUSABLES:
  NOT_APPLICABLE:
    REASON: an invisible sign has NO visual look-alikes — you cannot "confuse BY
      SIGHT" what is not seen. The classic CONFUSABLES mechanism (visual mimicry)
      does not apply to ZWSP. The runtime reads only SIGN_RELATIONS below.
    REVIEW_REQUIRED: YES
  FUNCTIONAL_NEIGHBORS:
    [TERM UPDATED 2026-07-16: the five signs below are SAMPLES (exemplars of the
     SUPERVISED CLASS of invisibles), NOT "all neighbors". "Neighbor/NEIGHBOR" is
     LEGACY (glossary: foundation_layer/CLASS_FRONT_INVISIBLE_SIGNS.md). The
     supervised class = Cf∧Default_Ignorable = 138 (D-NEIGHBORS-BORDER-138); these
     5 ⊂ 138. The field name FUNCTIONAL_NEIGHBORS and the NEIGHBOR_00N keys are
     KEPT as STRUCTURAL (template/preflight) — renaming the field is a separate pass.
     NOT confusion BY SIGHT (not CONFUSABLES, a difference of FUNCTION, not look);
     a reference block for the human; the runtime computes no risk over them — there
     are no CONFUSABLE_ keys here, the parser does not load them, and this is DELIBERATE.]
    NEIGHBOR_001:
      CODEPOINT: U+200C
      NAME: ZERO WIDTH NON-JOINER (ZWNJ)
      FUNCTION_DIFF: ZWNJ suppresses joining (Persian orthography);
        carries meaning — blind deletion would distort
    NEIGHBOR_002:
      CODEPOINT: U+200D
      NAME: ZERO WIDTH JOINER (ZWJ)
      FUNCTION_DIFF: ZWJ joins (emoji sequences); Join_Control=YES
        (ZWSP has NO); carries meaning
    NEIGHBOR_003:
      CODEPOINT: U+2060
      NAME: WORD JOINER (WJ)
      FUNCTION_DIFF: WJ FORBIDS a break — the direct opposite of ZWSP
    NEIGHBOR_004:
      CODEPOINT: U+FEFF
      NAME: ZERO WIDTH NO-BREAK SPACE / BOM
      FUNCTION_DIFF: BOM — byte-order marker / no-break
    NEIGHBOR_005:
      CODEPOINT: U+00AD
      NAME: SOFT HYPHEN (SHY)
      FUNCTION_DIFF: SHY — a conditional break with a VISIBLE hyphen on wrap

SIGN_RELATIONS:
  [SOURCE OF TRUTH FOR THE RUNTIME. Three edges per D-INV-1 (minimum of types).
   Honestly: without a codepoint canon — TARGET_KIND: EMPTY_SEQUENCE (D-INV-3),
   with no invented TARGET and no false VISUAL_MIMIC_OF.
   RELATION_TYPE_RUNTIME_STATUS (Level 2, finding S-03) — the type is a CONTRACT,
   not a label; the field states what the type REALLY does at runtime, not just what
   it describes. It matches the _RELATION_RUNTIME_ROLE map in sequence_engine.]
  RELATION_001:
    RELATION_TYPE: BOUNDARY_DISRUPTOR
    RELATION_TYPE_RUNTIME_STATUS: PRIMARY
      [breaks the exact-match boundary; the ONLY standalone verdict of ZWSP — a real
       contract, VERIFIED by run on gоog<ZWSP>／le.com]
    TARGET_KIND: EMPTY_SEQUENCE
    CONTEXT_SCOPE: HOST, EMAIL, BYTE_EXACT_TOKEN, PATH, HIDDEN_BOUNDARY_PADDING, QUERY_VALUE, FRAGMENT, USERINFO
    VERIFICATION_STATUS: VERIFIED
    RUNTIME_EFFECT: RELATION_ONLY
  RELATION_002:
    RELATION_TYPE: INVISIBLE_CLASS_COLLISION
    RELATION_TYPE_RUNTIME_STATUS: TAXONOMY_ONLY
      [passes via the allowance for another invisible in a CRUDE external filter;
       that filter's behavior is NOT observable from the input string → there is NO
       runtime check yet. The type is described honestly but NOT passed off as a
       working contract: it emits no risk. Awaits a separate pass on the cases.]
    TARGET_KIND: CLASS
    TARGET: zero-width-allowed (a crude classifier, NOT a Unicode function)
    CONTEXT_SCOPE: BYTE_EXACT_TOKEN
    VERIFICATION_STATUS: CANDIDATE
    RUNTIME_EFFECT: RELATION_ONLY
  RELATION_003:
    RELATION_TYPE: ABSENCE_CONFUSABLE
    RELATION_TYPE_RUNTIME_STATUS: SUPPORTING_FACET
      [indistinguishable from the sign's absence; EVIDENCE at the primary verdict, NOT
       a standalone second HIGH on the same sign in the same context (Z1, three
       reviewers — the duplicate was removed). Emits no risk.]
    TARGET_KIND: EMPTY_SEQUENCE
    CONTEXT_SCOPE: HOST, EMAIL, BYTE_EXACT_TOKEN
    VERIFICATION_STATUS: VERIFIED
    RUNTIME_EFFECT: RELATION_ONLY

CONTRADICTION_GUARDS:
  CG1:
    TRIGGER: "ZWSP is invisible, therefore it is not there"
    RESPONSE: INVISIBLE ≠ ABSENT
    RULE: invisibility is not absence; the sign is present in the byte stream
  CG2:
    TRIGGER: "ZWSP is a space"
    RESPONSE: ZWSP_FORM ≠ SPACE
    RULE: zero width, not a word separator, a different codepoint
  CG3:
    TRIGGER: "normalization will remove ZWSP"
    RESPONSE: NFKC_SURVIVAL ≠ LEGITIMACY
    RULE: invisibles survive NFC/NFD/NFKC/NFKD — they stay in the string
  CG4:
    TRIGGER: "RELATION_FOUND means a threat"
    RESPONSE: RELATION_FOUND ≠ THREAT
    RULE: the edge = "disrupts the boundary in scope"; the sequence layer decides risk
  CG5:
    TRIGGER: "all invisibles can be blindly deleted"
    RESPONSE: DEFAULT_IGNORABLE ≠ SAFE_TO_DELETE
    RULE: ZWNJ/ZWJ carry meaning (orthography/emoji); deletion would distort
  CG6:
    TRIGGER: "no visible canon — no relation"
    RESPONSE: NO_CODEPOINT_CANON ≠ NO_RELATION
    RULE: a relation to boundary/class/emptiness exists without a visual canon

SEQUENCE_LAYER_BOUNDARY:
  SIGN_SAFE_ALONE ≠ SIGN_SAFE_IN_SEQUENCE: YES
  SEQUENCE_CANDIDATES: NOT_APPLICABLE
    [ZWSP has no literal SEQUENCE_CANDIDATES of its own; inter-sign behavior (ZWSP
     between domain labels) is assessed through the "relation" axis
     (active_relation_candidates + _assess_relation_risk), as with the mask ／,
     not through a literal sequence candidate]

PHAGO_ENTITY_MIMICRY:
  NOT_APPLICABLE
  PHAGO_REVIEW: VERIFIED (conveyor 9 reviewers 8:1 + author decision 2026-07-13)
  PHAGO_BASIS: ZWSP BY ITS FUNCTION (token break) does NOT create false belonging
    to an entity. Mimicry involving ZWSP is emergent at the SEQUENCE level (paired
    with a homoglyph/domain) → it belongs to the SEQUENCE/RELATION layer, not a
    property of the single sign. Consistent with the criterion's anchors:
    / U+002F APPLICABLE (the separator function ITSELF spawns a false brand
    hierarchy), . U+002E NOT_APPLICABLE (does not itself spawn) — ZWSP is like the dot.
    Test: remove ZWSP — the target entity (administrator, paypal) exists without it.
  PHAGO_ROBUST: NOT_APPLICABLE holds under ANY reading of phago — the verdict does NOT
    depend on the open node PHAGO_NATURE. ZWSP: (1) does NOT create false BELONGING to
    an entity; (2) does NOT ABSORB another identity (the phagocytosis-hypothesis test);
    (3) is not itself an entity-signal (an invisible break, not a face/brand/authority).
    → NOT_APPLICABLE under all three readings.
    See foundation_layer/OPEN_NODE_PHAGO_NATURE.md.
  PHAGO_INTERACTION_ROLE: ENABLER_ONLY
    [participates in mimicry at the SEQUENCE level, NOT a PHAGO actor at the sign
     level. The PAST boundary ("own face" / "serves" / "invisible") is ROLLED BACK as
     wrong — it conflicted with / U+002F (APPLICABLE). The correct criterion is in
     foundation_layer/RULE_PHAGO_APPLICABILITY_v0_1.md.]
  PHAGO_APPLICABILITY_RULE: the canonical source is
    foundation_layer/RULE_PHAGO_APPLICABILITY_v0_1.md (NOT duplicated here to avoid drift).

============================================================
8. ADVERSARIAL_COVERAGE — RUN_CARD SEED
============================================================
MIN_TOTAL_VECTORS: 12
CATEGORY_A: FORM_MANIPULATION
  A1: ZWSP between every pair of domain characters
  A2: several ZWSP in a row to inflate length
CATEGORY_B: CONTEXT_INJECTION
  B1: ZWSP in the host part of a schemeless URL
  B2: ZWSP in an email local part
CATEGORY_C: SEQUENCE_MANIPULATION
  C1: ZWSP + fullwidth mask ／ together (RISK_CASE_003)
  C2: ZWSP between label and TLD (gоogle​.com)
CATEGORY_D: SEMANTIC_MIMICRY
  [SOFT FRICTION: ZWSP does not IMITATE; the vectors are framed as SABOTAGE]
  D1: ZWSP passes where a filter "allows zero-width" expecting ZWJ
  D2: ZWSP imitates ABSENCE (ABSENCE_CONFUSABLE) — padding "as if clean"
CATEGORY_E: PHAGO_ENTITY_MIMICRY — N/A_ACTIVELY_VERIFIED (run 2026-07-13)
  [PHAGO=NOT_APPLICABLE, but the rule "N/A on phago is checked SEPARATELY" → this is
   not a dismissive "NOT_APPLICABLE" but 2 ACTIVE vectors: attempts to make ZWSP create
   false belonging to an entity, which FAIL on the engine, confirming N/A. RESULT = the
   detector's output, not a guess.]
  E1: attempt to use ZWSP as a ROLE entity-signal — "admin<ZWSP>istrator"
    OBSERVED: detector → BYTE_EXACT_TOKEN / MEDIUM (token break), NOT entity mimicry
    RESULT: N/A CONFIRMED — the role "administrator" is carried by the VISIBLE LETTERS
      (remove ZWSP → "administrator" is intact); ZWSP by its function creates no false belonging
  E2: attempt to make ZWSP create belonging to a BRAND — "paypal<ZWSP>.com"
    OBSERVED: detector → HOST / HIGH (domain break)
    RESULT: N/A CONFIRMED — the brand resemblance "paypal.com" is emergent from the STRING
      (visible letters), intact without ZWSP; mimicry (if it arises) is at the SEQUENCE
      level, not the single sign (consistent with PHAGO_BASIS, section 7)
CATEGORY_F: SEMANTIC_LAYER_MANIPULATION
  F1: switch the active epoch via the context gate (typography → machine)
  F2: feed ZWSP in a typographic frame to hide a machine-level risk
ACTUAL_TOTAL_VECTORS: 12
COVERAGE_STATUS: SUFFICIENT_FOR_CURRENT_CARD_SCOPE
COVERAGE_SUFFICIENCY: SUFFICIENT_FOR_CURRENT_CARD_SCOPE
  [RUN: BY_CODE battery 21/21 (two-legged BY_SPEC+BY_CODE, reconcile by tuple,
   mutation-adequacy 5/5). NOT a bare SUFFICIENT: it covers exactly the contexts the
   detector REALLY produces (HOST/EMAIL/PATH/BYTE_EXACT_TOKEN/QUERY_VALUE/FRAGMENT/
   USERINFO/HIDDEN_BOUNDARY_PADDING). Beyond this card's scope (density DoS at ingest,
   file input) are separate fronts, not covered and honestly marked so.]

============================================================
9. MUTATION_CHECK
============================================================
MUTATION_01:
  CLAIM: ZWSP yields authority_effect
  EXPECTED: FAIL_FALSE_AUTHORITY
  RESULT: FAIL
MUTATION_02:
  CLAIM: ZWSP executes/launches
  EXPECTED: FAIL_FALSE_EXECUTION
  RESULT: FAIL
MUTATION_03:
  CLAIM: ZWSP is proof/verification
  EXPECTED: FAIL_FALSE_VERIFICATION
  RESULT: FAIL
MUTATION_04:
  CLAIM: ZWSP is equivalent to the space U+0020
  EXPECTED: FAIL_FALSE_EQUIVALENCE
  RESULT: FAIL
MUTATION_05:
  CLAIM: ZWSP is always safe to delete
  EXPECTED: FAIL_FALSE_SAFE_DELETE (ZWNJ/ZWJ carry meaning)
  RESULT: FAIL
MUTATION_06:
  CLAIM: invisibility = absence from the stream
  EXPECTED: FAIL_FALSE_ABSENCE
  RESULT: FAIL

MUTATION_CHECK_RUNTIME (engine-verified, run of msl_mip_runtime 2026-07-13 —
  REAL mutations of codepoint/context/scope/type/target_kind; RESULT = the DETECTOR's
  output on the run, not an assumption; MUTATION_01-06 above are semantic, about
  EFFECT_FIELDS; these are runtime, about detector behavior):
  MR_01_CODEPOINT_BINDING:
    CLAIM: any invisible in a domain fires as ZWSP
    METHOD: goog<U+2062>le.com (U+2062 instead of U+200B)
    OBSERVED: the ZWSP edge did NOT fire; U+2062 → witness (UNVERIFIABLE); verdict pass
    RESULT: FAIL (the map is bound to U+200B; a foreign invisible → witness, not a ZWSP verdict)
  MR_02_CONTEXT_GATING:
    CLAIM: ZWSP gives a fixed risk regardless of context
    METHOD: goog<ZWSP>le.com / bad<ZWSP>word / "just <ZWSP> text"
    OBSERVED: HOST=HIGH, BYTE_EXACT_TOKEN=MEDIUM, FREE_TEXT=NONE
    RESULT: FAIL (risk is context-dependent — gated by _detect_context_at)
  MR_03_SCOPE_PROTECTION:
    CLAIM: risk does not depend on the edge's CONTEXT_SCOPE
    METHOD: temp map without HOST in the BOUNDARY_DISRUPTOR scope; goog<ZWSP>le.com
    OBSERVED: ctx=HOST, but protected=False → risk NONE, verdict pass
    RESULT: FAIL (scope gates risk; HOST outside scope → NONE)
  MR_04_UNKNOWN_TYPE_SAFETY:
    CLAIM: an unknown RELATION_TYPE emits risk as PRIMARY
    METHOD: temp map RELATION_TYPE=FOOBAR_UNKNOWN_TYPE; goog<ZWSP>le.com
    OBSERVED: INVALID_EDGE_NOT_ACTIVATED (1 edge), excluded, emits no risk
    RESULT: FAIL (an unknown type → INVALID_EDGE, not a PRIMARY default)
  MR_05_FACET_ROLE_GATING:
    CLAIM: ABSENCE_CONFUSABLE emits no risk under any type
    METHOD: temp map ABSENCE_CONFUSABLE→BOUNDARY_DISRUPTOR; goog<ZWSP>le.com
    OBSERVED: as SUPPORTING_FACET → NONE; changing the type to PRIMARY → HOST/HIGH
    RESULT: FAIL (emission is gated by ROLE/type, not fixed — the dedup is real)
  MR_06_TARGET_KIND_ENFORCEMENT:
    CLAIM: TARGET_KIND CODEPOINT without a TARGET activates silently
    METHOD: temp map TARGET_KIND EMPTY_SEQUENCE→CODEPOINT (no TARGET added)
    OBSERVED: INVALID_EDGE_NOT_ACTIVATED (1 edge), surfaced, not activated
    RESULT: FAIL (CODEPOINT requires a TARGET; contract violation → INVALID_EDGE)
  MUTATION_CHECK_RUNTIME_TOTAL: 6 (all FAIL = the engine holds the invariant under mutation)

============================================================
10. KNOWN_OPEN_QUESTIONS
============================================================
OQ1:
  QUESTION: the class INVISIBLE_DEFAULT_IGNORABLE_GUARD is not built — there is
    nowhere to declare ZWSP's class properties
  STATUS: RECLASSIFIED (AUTHOR_DECISION D-ZWSP-STATUS 2026-07-13)
  BLOCKS_WORKINGLY_CLOSED: NO  (was YES)
  RECLASSIFIED_AS: CLASS_FRONT_DEPENDENCY
    [the guard is a CLASS dependency, NOT a defect of this card. Building it on N=1 =
     overfitting (violates "do not generalize from one", risks breaking legitimate
     ZWJ/ZWNJ — DEFAULT_IGNORABLE ≠ SAFE_TO_DELETE). Moved to the class-front
     register: foundation_layer/CLASS_FRONT_INVISIBLE_SIGNS.md. The registrar
     (witness) PARTIALLY covers the sub-promise "the unknown does not stay silent" →
     it lowers urgency but does NOT replace it (witness ≠ policy: goog<U+2063>le.com →
     PASS+witness, not HOST/HIGH). The guard is needed later, from >=3 signs.]
  NOTE: ZWSP's class properties are declared inline (SIGN_CATEGORY +
    WHAT_THIS_SIGN_IS_NOT); their common home is the future class-level guard.
OQ2:
  QUESTION: D-GUARD-2 is blind to a warned edge with a nonzero verdict
    (candidate D-GUARD-5)
  STATUS: OPEN
  BLOCKS_WORKINGLY_CLOSED: NO
  NOTE: DRAFT item 4.2; the guard's boundary, not the card's
OQ3:
  QUESTION: the detector's _demask must NOT blindly delete ZWNJ/ZWJ (it would break
    Persian orthography / emoji) — this is a DETECTOR boundary, not the card's
  STATUS: OPEN
  BLOCKS_WORKINGLY_CLOSED: NO
  NOTE: DEFAULT_IGNORABLE ≠ SAFE_TO_DELETE; for ZWSP demask is correct
    (ZWSP in a machine domain is a break; deletion reconstructs the canon),
    but for ZWNJ/ZWJ demask-deletion would distort meaning
OQ4:
  QUESTION: the detector does NOT distinguish CODE vs IDENTIFIER vs policy-filter — all
    collapse into one context BYTE_EXACT_TOKEN (MEDIUM). The finer distinction
    (a policy keyword → HIGH vs an ordinary identifier → MEDIUM) is not invented:
    the detector cannot do it yet
  STATUS: OPEN
  BLOCKS_WORKINGLY_CLOSED: NO
  NOTE: RISK_CASE_002/005/006 brought to the real BYTE_EXACT_TOKEN; the card no
    longer promises a context the system does not produce
OQ5:
  QUESTION: a FALSE ALARM in the GENERAL detector (R8): a schemeless domain with a
    mask in the PATH is falsely classified as HOST/HIGH instead of PATH/MEDIUM.
    Example: docs.example.com/guide/very-long<ZWSP>-section → HOST/HIGH/HOLD, though
    ZWSP sits in the PATH, not the host. The same input WITH a scheme handles correctly
    (PATH/MEDIUM). Root: the "mask inside domain" branch (_domain_prefix tolerates a
    trailing path); the distinguishing signal — the pre-mask token piece already
    contains / ? #.
  STATUS: RESOLVED (F-NEW-2 patch, 2026-07-13)
  BLOCKS_WORKINGLY_CLOSED: NO (was YES)
  SEVERITY: HIGH
    [this is an ALERTING SYSTEM: a false alarm is critical — it undermines a human's
     trust in HOLD. Not cosmetics — fix it, do not defer indefinitely.]
  SCOPE: the GENERAL detector — affects the mask ／ (U+FF0F) too, and all 55
    bare-domain cases. The fix requires a full re-gate of 55 + regression on ／, so
    a separate package, not inside this invisibles commit.
  RESOLUTION: CLOSED by F-NEW-2 root 2B — HOST fires only if the mask index is
    INSIDE the host span (len(left_part) < host_end of the reconstruction);
    past the host -> PATH. NB: the ORIGINAL hypothesis above (pre-mask token
    already contains / ? #) proved INSUFFICIENT — it missed P5-style deep paths;
    the host-span check replaced it. docs.example.com/guide/very-long<ZWSP>-
    section now reads PATH/MEDIUM.
OQ-HBP:
  QUESTION: HIDDEN_BOUNDARY_PADDING — a NEW context (F-NEW-2 root 2A) for a
    leading/trailing invisible on a WHOLE domain (<ZWSP>paypal.com,
    paypal.com<ZWSP>): not a label break (not HOST/HIGH), but not a silent PASS
    either → MEDIUM/QUEUE as a fallback from pass.
  STATUS: OPEN
  BLOCKS_WORKINGLY_CLOSED: NO
  NEEDS: a conveyor decision — is this the right separate context-entity, is the
    MEDIUM risk correct, does it spawn contexts needlessly (is it not a subtype of
    BYTE_EXACT_TOKEN). Goes to conveyor with the F-NEW-3 batch.
  DIRECTION: at a SCHEMA REVISION, refactor into a POSITION_ROLE, not a top-level
    context — in essence this is a POSITIONAL role of the sign (start/end/inside), not
    a separate kind of context alongside HOST/PATH. For now do NOT break what works: it
    lives as a context until the schema revision (v0.5+).
OQ-SOLIDUS-DRIFT:
  QUESTION: the ／ (SOLIDUS, ARTIFACT_CONFIRMED) detector now reads
    example.com,／test and gоogle.com*／path as PATH, not HOST. The ZWSP card patch
    touched a FINISHED artifact's zone — the FIRST confirmed DRIFT.
  STATUS: OPEN
  BLOCKS_WORKINGLY_CLOSED: NO
  SEVERITY: MEDIUM
    [positionally PATH is more correct than the old HOST over-read (the solidus gate
     itself called this a quirk); but a behavior change in an ARTIFACT_CONFIRMED
     detector must go through re-validation, not silently.]
  NEEDS: re-validation of the SOLIDUS card with today's instrument (BY_CODE), as for
    ZWSP. Link: ARTIFACT_CONFIRMED is bound to the instrument VERSION — the instrument
    changed → the solidus status must be re-confirmed. To conveyor with the F-NEW-3 batch.
OQ-SHARED-DETECTOR-BOUNDARY:
  QUESTION: in the TIER_2 battery two cases stay "failing" — U1
    (?q=bad<ZWSP>word → context PATH instead of QUERY_VALUE) and D2
    (paypal.com<ZWSP>@evil.com → no userinfo parsing, host not extracted).
  STATUS: RESOLVED (F-NEW-4 + F-NEW-5, 2026-07-13)
    [they were NOT ZWSP failures: QUERY_VALUE and userinfo parsing are properties of
     the GENERAL detector. Closed by general-detector patches to _detect_context_at:
     F-NEW-4 — URL component parsing (authority/path/QUERY_VALUE/FRAGMENT);
     F-NEW-5 — userinfo (host after the LAST @ inside authority, EMAIL not broken —
     separated by presence of scheme://). U1 → QUERY_VALUE/MEDIUM,
     D2 → USERINFO/MEDIUM. ZWSP battery 19/21 → 21/21.]
  BLOCKS_WORKINGLY_CLOSED: NO (for ZWSP)
  NEEDS: — (closed; the general detector was fixed as a separate front, as planned).
ALL_OPEN_QUESTIONS_CLOSED: NO

============================================================
11. PATCH_HISTORY
============================================================
PATCH_HISTORY:
  v0_1_PATCH_01: initial creation (template probe on ZWSP 2026-07-12 +
    AUTHOR_DECISION D-INV-1/2/3) — the first invisible-sign card;
    the "relation" axis extended with types BOUNDARY_DISRUPTOR /
    INVISIBLE_CLASS_COLLISION / ABSENCE_CONFUSABLE, TARGET_KIND enum.
  v0_1_PATCH_02: FIX_FIRST after the first round (2026-07-12) — claims=reality.
    RISK_CASE contexts/levels/RUNTIME_STATUS brought to what the detector REALLY
    produces (BYTE_EXACT_TOKEN/MEDIUM instead of invented CODE/HIGH;
    004/006 honestly PENDING). RELATION_TYPE_RUNTIME_STATUS (Level 2): PRIMARY/
    TAXONOMY_ONLY/SUPPORTING_FACET — the duplicate HIGH removed. CONFUSABLES →
    NOT_APPLICABLE + FUNCTIONAL_NEIGHBORS. COVERAGE → UNVERIFIED. OQ4
    (CODE/IDENTIFIER not distinguished). RUNTIME_REALITY in LIMITATION.
    The registrar for uncarded invisibles is in the runtime, not the card. The found
    false alarm R8 (schemeless path → falsely HOST) filed as OQ5 NEXT_SESSION_FIX
    (general detector, fixed in a separate pass with a re-gate of 55).
  v0_1_PATCH_03: F-NEW-3 + T1-honesty + D-ZWSP-STATUS (2026-07-13). SAFE_CASE_002
    (CJK) → CURRENT_RUNTIME_EXPECTATION: MAY_QUEUE (do not promise an auto-PASS the
    code does not deliver). Status block: LIFECYCLE_STATUS / VALIDATION_METHOD / CLASS_ROLE.
    OQ1 → CLASS_FRONT_DEPENDENCY (BLOCKS_WORKINGLY_CLOSED: NO). PHAGO: NOT_APPLICABLE
    VERIFIED + PHAGO_ROBUST + ENABLER_ONLY (rule — RULE_PHAGO_APPLICABILITY, node
    PHAGO_NATURE). Solidus → REVALIDATION_REQUIRED (principle Q7).
  v0_1_PATCH_04: F-NEW-4/5 (2026-07-13). CONTEXT_SCOPE of the BOUNDARY_DISRUPTOR edge +=
    QUERY_VALUE, FRAGMENT, USERINFO (the detector learned to parse URLs into components
    + userinfo by the last @). OQ-SHARED-DETECTOR-BOUNDARY → RESOLVED. U1/D2
    closed → battery 19/21 → 21/21.
  v0_1_PATCH_05: preflight-pass (2026-07-13). MUTATION_CHECK_RUNTIME — 6 REAL
    engine-verified mutations (RESULT = the engine's run). CATEGORY_E → N/A_ACTIVELY_
    VERIFIED (2 active vectors prove phago-N/A). OPEN_NODE CONVEYOR_REVIEW_FORMAT.
  v0_1_PATCH_06: doc-sync (2026-07-14). Upper layers brought to the lower (correct) ones:
    21/21 everywhere; RUNTIME_REALITY — the full list of contexts = the edge's scope; COVERAGE
    → SUFFICIENT_FOR_CURRENT_CARD_SCOPE; RUN_CARD_STATUS/SIMULATION_GATE → 21/21;
    STRUCTURAL_PREFLIGHT → PASS; CONVEYOR_REVIEW_PASS → PASS_WITH_PATCHES (8/8 ACCEPT).
    OPEN_NODE CARD_SINGLE_SOURCE_OF_TRUTH. Trigger: the BY_CODE recheck exposed an internal
    card desync (not card↔code).
PATCHES_APPLIED: 6
PATCHES_VERIFIED: 6/6 (BY_CODE battery 21/21 + preflight 35/0/1 + BY_CODE recheck 2026-07-14)

============================================================
12. LIMITATION_STATEMENT
============================================================
LIMITATION_STATEMENT:
  THIS_CARD IS A WORKING_DRAFT ARTIFACT (until ARTIFACT_CONFIRMED)
  NOT A FINAL_STANDARD
  NOT A PARSER
  NOT A RUNTIME
  NOT A SECURITY_CERTIFICATE
  CONVEYOR_PASS ≠ VALIDATION
  RUN_CARD_RESULT ≠ FINAL_STATUS
  WORKINGLY_CLOSED ≠ ARTIFACT_CONFIRMED
  WORKINGLY_CLOSED ≠ LOCKED_WORKING_CORE
  DETECTOR_BOUNDARY_NOTE: DEFAULT_IGNORABLE ≠ SAFE_TO_DELETE — the detector's
    _demask must NOT blindly delete all invisibles: deleting ZWNJ/ZWJ would
    distort meaning (Persian orthography, emoji-ZWJ sequences), not clean it. For
    ZWSP in a machine context (domain/identifier) demask is correct — this is a
    DETECTOR boundary, recorded here as a limitation but implemented in the detector,
    not the card.
  RUNTIME_REALITY (claims=reality): the system CURRENTLY REALLY produces for
    ZWSP: HOST→HIGH; EMAIL→MEDIUM; PATH→MEDIUM; BYTE_EXACT_TOKEN→MEDIUM;
    QUERY_VALUE→MEDIUM; FRAGMENT→MEDIUM; USERINFO→MEDIUM;
    HIDDEN_BOUNDARY_PADDING→MEDIUM; FREE_TEXT→NONE. (QUERY_VALUE/FRAGMENT/
    USERINFO — from F-NEW-4/5 URL component parsing; HIDDEN_BOUNDARY_PADDING —
    from F-NEW-2; this list is EXACTLY = the CONTEXT_SCOPE of the BOUNDARY_DISRUPTOR
    edge, verified BY_CODE 2026-07-14.) The only standalone verdict comes from the
    BOUNDARY_DISRUPTOR edge (PRIMARY); INVISIBLE_CLASS_COLLISION (TAXONOMY_ONLY) and
    ABSENCE_CONFUSABLE (SUPPORTING_FACET) emit NO risk — they give no second
    independent HIGH on the same sign. PATH is deliberately MEDIUM, not HIGH: from
    the string one cannot tell a soft wrap of a displayed URL from a machine path.
    This is NOT an antivirus: the verdict (PASS/QUEUE/HOLD) is a RECOMMENDATION to a
    human, not a command; nothing is cut or deleted, the sign is only brought into
    view. An invisible WITHOUT a card is not assessed at all — it is separately
    SURFACED by the registrar INVISIBLE_UNCARDED_REGISTRAR with status
    UNVERIFIABLE (not "dangerous", not "safe" — "cannot verify").

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

END_OF_CARD
