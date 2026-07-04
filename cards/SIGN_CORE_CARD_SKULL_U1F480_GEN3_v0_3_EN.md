PRIVATE AUTHORED PROJECT / COMMERCIAL USE PROHIBITED

DOCUMENT_ID: SIGN_CORE_CARD_SKULL_U1F480_GEN3_v0_3_EN
DOCUMENT_TYPE: SIGN_CORE_CARD
TEMPLATE_LINE: GEN3_v0_3
DOCUMENT_STATUS: ARTIFACT_CONFIRMED
STATUS: ARTIFACT_CONFIRMED / NOT_LOCKED / NOT_RUNTIME / NOT_VALIDATOR / NOT_PRODUCTION
SOURCE_TEMPLATE: SIGN_CORE_CARD_TEMPLATE_GEN3_v0_3_EN
AUTHOR: Ruslan Malyavsky
CREATED_AT: 2026-06-18
PATCHED_AT: 2026-06-25
VERSION: v0_1
AUTHOR_DECISION_REFERENCE: AUTHOR_DECISION_20260625_003_SKULL_U1F480_ARTIFACT_CONFIRMED_RU
RUN_CARD_REFERENCE: SIMULATION_ARTIFACT_SKULL_U1F480_TIER3_v0_1_RU
RUN_CARD_STATUS: COMPLETED (TIER_3)

TRANSLATION_NOTE: This is the English translation of
  SIGN_CORE_CARD_SKULL_U1F480_GEN3_v0_3_RU. The Russian version remains
  authoritative. Field names, status tokens, codepoints, formulas,
  dates, reviewer names, epoch names, and English-language INPUT
  examples (Gen Z slang, already in English in the original) are kept
  identical. Russian-language INPUT examples and NOTE prose are
  translated to English (per AUTHOR_DECISION: English cards use English
  examples).

CONTENT_PROVENANCE_NOTE: the content base (EPOCH_TRACKER, RISK_CASES,
  CONTRADICTION_GUARDS, ADVERSARIAL_COVERAGE, MUTATION_CHECK,
  KNOWN_OPEN_QUESTIONS) was carried over from
  SIGN_CORE_CARD_SKULL_U1F480_GEN3_v0_2_PLUS_EPOCH_v0_1_RU
  (DOCUMENT_STATUS: WORKINGLY_CLOSED, AUTHOR_DECISION_REFERENCE:
  AUTHOR_DECISION_20260618_004_SKULL_WORKINGLY_CLOSED_RU). That legacy
  document is NOT modified and remains a separate historical artifact.
  The current document is a new v0_3 artifact line with its own
  STATUS_PROGRESSION_TRACKER and its own PATCH_HISTORY starting from
  v0_1 (per the DOT/SOLIDUS migration precedent — the WORKINGLY_CLOSED
  status is not inherited automatically, STRUCTURAL_PREFLIGHT_PASS and
  CONVEYOR_REVIEW_PASS must be passed anew).

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
RUN_CARD_TEMPLATE_REFERENCE: SIGN_CONVEYOR_RUN_CARD_TEMPLATE_GEN3_v0_3
LOCKED_WORKING_CORE_SELF_ASSIGNMENT: FORBIDDEN
MODEL_FAMILY_DIVERSITY_REQUIRED: YES
ADVERSARIAL_EVIDENCE_REQUIRED: YES
MUTATION_CHECK_REQUIRED: YES
LIMITATION_STATEMENT_REQUIRED: YES
AFTER_RUN_RESIDUE: FORBIDDEN

STATUS_PROGRESSION_TRACKER:
  WORKING_DRAFT: YES
  STRUCTURAL_PREFLIGHT_PASS: PASS (5/5 runs, 2026-06-25)
  CONVEYOR_REVIEW_PASS: PASS (5/5 runs ACCEPT/ACCEPT_WITH_PATCHES, the
    single MINOR closed by PATCH_08, 2026-06-25)
  WORKINGLY_CLOSED: YES (AUTHOR_DECISION_20260625_002, 2026-06-25)
  SIMULATION_GATE_TIER: TIER_3
  SIMULATION_GATE_PASSED: YES (TIER_3, 2026-06-25; see
    TIER3_ARBITRATION_NOTE below)
  ARTIFACT_CONFIRMED: YES (AUTHOR_DECISION_20260625_003, 2026-06-25)

TIER3_ARBITRATION_NOTE: the TIER_3 run (5/5 reviewers: Kimi, Gemini,
  GPT-5.5, Qwen, Grok) gave a unanimous DIFFERENTIATION_CHECK: PASS and
  0 ARCHITECTURE_BUG. The only divergence — the RISK_LEVEL for
  CONTEXT_3 ("I have 3 exams tomorrow 💀", mixed cohort): 4/5 (Gemini,
  GPT-5.5, Qwen, Grok) gave MEDIUM by the literal application of the
  STAGE_5 MODULE_TEMPLATE rule ("AMBIGUITY_FLAG=YES → RISK_LEVEL ≥
  MEDIUM"). Kimi alone gave LOW, justifying it by an informal "priority
  of an explicit SAFE_CASE over a heuristic" — a rule that is not in
  the text of MODULE_TEMPLATE.
  ARBITRATION (author, 2026-06-25): MEDIUM is the correct value.
  SAFE_CASE_002 describes the general case without specifying a cohort;
  the mixed cohort in CONTEXT_3 is a narrower, separate scenario for
  which the AMBIGUITY_LOGIC must fire literally, without exceptions not
  described in the template itself. Kimi's divergence is recorded as
  its own interpretation error (inventing a nonexistent rule), not as
  grounds for a MODULE_TEMPLATE patch. RATIONALE: a discrepancy between
  the documented rule and the code's behavior creates a greater risk
  (hidden specification drift) than the cost of a false MEDIUM (a light
  review label, queue_for_review, not a block).

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

CARD_UID: SIGN_CORE_CARD_SKULL_U1F480_GEN3_v0_3_EN
CODEPOINT: U+1F480
VISIBLE_FORM: 💀
UNICODE_NAME: SKULL
ZONE: ZONE_3
DOCUMENT_STATUS: ARTIFACT_CONFIRMED
TEMPLATE_LINE: GEN3_v0_3
SOURCE_TEMPLATE: SIGN_CORE_CARD_TEMPLATE_GEN3_v0_3_EN
AUTHOR: Ruslan Malyavsky
CREATED_AT: 2026-06-18
VERSION: v0_1
AUTHOR_DECISION_REFERENCE: AUTHOR_DECISION_20260625_003_SKULL_U1F480_ARTIFACT_CONFIRMED_RU
RUN_CARD_REFERENCE: SIMULATION_ARTIFACT_SKULL_U1F480_TIER3_v0_1_RU
RUN_CARD_STATUS: COMPLETED (TIER_3)

DISPLAY_NAME: skull

============================================================
3. REQUIRED_GENERAL_GUARDS
============================================================

REQUIRED_GENERAL_GUARDS:
  - SIGN_FALSE_EFFECT_MIMICRY_GUARD_v0_2A_RU
    GUARD_COMPATIBILITY: GUARD_COMPATIBILITY_RULE_v0_1_RU
    GUARD_REVISION: v0_2A
    TEMPLATE_LINE_COMPATIBLE: v0_2, v0_2A, v0_2B, v0_2_PLUS, v0_2_PLUS_EPOCH, v0_3

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

VISIBLE_FORM: 💀
LOOKS_SIMILAR_IS_NOT_SAME_SIGN: YES
RAW_SIGN_INPUT_STATUS: DATA_ONLY

BASE_MODE: DATA_ONLY
BASE_MODE_FORMULA: SKULL_FORM ≠ EFFECT

SIGN_CATEGORY:
  - emoji
  - symbol
  - pictograph

WHAT_THIS_SIGN_IS_NOT:
  1. NOT_THREAT_INDICATOR
  2. NOT_MORTALITY_PROOF
  3. NOT_VIOLENCE_VERIFICATION
  4. NOT_SUICIDE_MARKER
  5. NOT_DANGER_CERTIFICATE
  6. NOT_HUMOR_VALIDATOR
  7. NOT_IRONY_PROOF
  8. NOT_SARCASM_DETECTOR
  9. NOT_GEN_Z_TRANSLATOR
  10. NOT_SENTIMENT_ANALYSIS_REPLACEMENT
  11. NOT_MEDICAL_DIAGNOSIS
  12. NOT_LEGAL_EVIDENCE

BASE_FORMULAS:
  SKULL_FORM ≠ THREAT
  SKULL_FORM ≠ MORTALITY
  SKULL_FORM ≠ VIOLENCE
  SKULL_FORM ≠ SUICIDE
  SKULL_FORM ≠ DANGER
  SKULL_FORM ≠ HUMOR
  SKULL_FORM ≠ IRONY
  SKULL_FORM ≠ SARCASM
  SKULL_FORM ≠ GENERATIONAL_CODE
  SKULL_FORM ≠ SENTIMENT_VALUE
  SKULL_FORM ≠ MEDICAL_STATUS
  SKULL_FORM ≠ LEGAL_EVIDENCE

============================================================
5. SEMANTIC_EPOCH_TRACKER
ZONE: ZONE_3 — PRECESSIONAL / CULTURAL
SEMANTIC_EPOCH_TRACKER_LOCK: REVIEWABLE
============================================================

EPOCH_TRACKER: REQUIRED

CAPTURE_HISTORY:
  EPOCH_1:
    NAME: literal_death_and_danger
    DATE_RANGE: 2010–2017
    SUBSTRATE: early mobile communication, literal translation
    FUNCTION: marker of death, poison, danger, Halloween
    EVIDENCE: Unicode Standard U+1F480 annotation (Poison, Skull),
      toxicology symbols, Jolly Roger historical precedent
    STATUS: DORMANT_IN_GENERAL_DIGITAL_CONTEXT
    NOTE: The direct "death/danger" meaning is practically displaced in
      everyday digital communication. It persists in medical, chemical,
      and military contexts.

  EPOCH_2:
    NAME: ironic_exhaustion_and_defeat
    DATE_RANGE: 2015–2019
    SUBSTRATE: millennial social media (Tumblr, early Twitter)
    FUNCTION: "I'm tired", "I'm dead inside", "burnout", "defeat"
      ("I'm dead", "ded", "kill me now")
    EVIDENCE: Know Your Meme, Urban Dictionary entries 2015-2017,
      Tumblr culture documentation
    STATUS: DORMANT_IN_MAINSTREAM_GEN_Z
    NOTE: The "millennial burnout" epoch partially overlaps with
      EPOCH_3, but differs in tone: EPOCH_2 = tragicomic exhaustion,
      EPOCH_3 = absurdist laughter.

  EPOCH_3:
    NAME: hysterical_laughter_and_absurdist_humor
    DATE_RANGE: 2019–ongoing
    SUBSTRATE: Gen Z social media (TikTok, Twitter/X, Discord)
    FUNCTION: replacement for "LOL", "LMAO", "ROFL" — hysterical
      laughter, absurdist humor, a reaction to cringe
    EVIDENCE: Emojipedia trend analysis 2019-2024, TikTok linguistic
      studies, Discord server culture documentation
    STATUS: ACTIVE
    NOTE: The dominant function in Gen Z and Alpha. When used by
      millennials or older generations it may activate EPOCH_1 (the
      literal meaning), creating intergenerational ambiguity.

ACTIVE_EPOCH:
  EPOCH_3: hysterical_laughter_and_absurdist_humor
ACTIVE_EPOCH_TYPE: GLOBAL
DOMINANT_SUBSTRATE: Gen Z social media
DOMINANT_FUNCTION: "hysterical laughter / absurdist humor"

DORMANT_EPOCHS:
  EPOCH_1: DORMANT_IN_GENERAL_DIGITAL_CONTEXT — reactivates in medical,
    chemical, military, Halloween contexts
  EPOCH_2: DORMANT_IN_MAINSTREAM_GEN_Z — reactivates in millennial
    contexts, burnout memes

PRECESSION_ALERT:
  STATUS: DRIFTING
  LAST_CHECK: 2026-06-25
  ORIGINAL_BASELINE_CHECK: 2026-06-18 (legacy run v0_1,
    GEN3_v0_2_PLUS_EPOCH)
  TRIGGER: re-attestation on migration to GEN3_v0_3 — the trend toward
    EPOCH_4 confirmed as current at the time of re-attestation, a
    separate epoch not yet fixed
  NOTE: Extreme precession speed: 3 epochs in 15 years. Sentiment
    analyzers lag behind reality. A trend toward EPOCH_4 has been
    detected: "💀 as a marker of second-hand embarrassment" (cringe on
    behalf of another). Not fixed as a separate epoch — requires
    observation.

LAYER_ANOMALY:
  ABSENT_PHYSICAL_LAYER: NO
  NOTE: 💀 copies a physical object — the human skull. This is a rare
    case for a digital sign: the physical layer is present (the
    anatomical skull), but the semantics are completely detached from
    the physical referent (laughter ≠ skull).

STACK_RULES:
  Higher_epoch_suppresses_lower_in_modern_contexts: YES
    (EPOCH_3 dominates in Gen Z)
  Lower_epoch_may_reactivate_in_historical_or_specialized_contexts: YES
    (EPOCH_1 in medicine, EPOCH_2 among millennials)
  Context_gate_determines_active_epoch: PARTIAL
    (age cohort = context gate)
  Absent_layer_anomaly_must_be_flagged_for_integrator: NOT_APPLICABLE
    (the physical layer is present)

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
    INPUT: "That joke was so funny 💀"
    CONTEXT: Gen Z social media, messaging
    EXPECTED: INFO (humor marker)
    RISK: NONE
    GUARD: SKULL_FORM ≠ THREAT
    NOTE: EPOCH_3 active. The context is clearly humorous.

  SAFE_CASE_002:
    INPUT: "I have 3 exams tomorrow 💀"
    CONTEXT: student messaging, social media
    EXPECTED: INFO (exhaustion marker)
    RISK: NONE
    GUARD: SKULL_FORM ≠ MORTALITY
    NOTE: The EPOCH_2→EPOCH_3 transition zone. Not a threat, not death.

  SAFE_CASE_003:
    INPUT: "Happy Halloween! 💀🎃"
    CONTEXT: holiday greetings, seasonal decoration
    EXPECTED: INFO (festive symbol)
    RISK: NONE
    GUARD: SKULL_FORM ≠ DANGER
    NOTE: EPOCH_1 reactivated in a culturally permitted context
      (Halloween).

  SAFE_CASE_004:
    INPUT: "Warning: Poison 💀"
    CONTEXT: informal warning / pictographic danger marker
    EXPECTED: INFO
    RISK: LOW / CONTEXT_DEPENDENT
    GUARD: SKULL_FORM ≠ DANGER
    NOTE: Formal hazard marking may require ☠️ / a standardized sign;
      💀 by itself is not a danger certificate.

  SAFE_CASE_005:
    INPUT: "Game over 💀 — you died, try again!"
    CONTEXT: video game UI / game-over screen
    EXPECTED: INFO (game UI marker for end of attempt)
    RISK: NONE
    GUARD: SKULL_FORM ≠ MORTALITY
    NOTE: A stable gaming convention: 💀 as a visual marker of "end of
      attempt" uses the literal image (skull = character's death), but
      does not activate EPOCH_1 as a threat to a real person and does
      not require a clinical/legal interpretation. A separate example
      that a literal visual referent can be safely "put in quotes" by a
      genre convention, independently of the dominant EPOCH_3.

  SAFE_CASE_006:
    INPUT: "Anatomy lecture: the slide shows 💀 to illustrate the
      structure of the skull."
    CONTEXT: educational / academic context (anatomy)
    EXPECTED: INFO (illustrative symbol)
    RISK: NONE
    GUARD: SKULL_FORM ≠ MEDICAL_STATUS
    NOTE: An academic illustration of anatomical structure — not the
      medical status of a specific person and not a reactivation of
      EPOCH_1 as a threat. A third independent "safe" substrate besides
      humor (EPOCH_3) and the culturally-permitted Halloween
      (EPOCH_1-reactivation) — showing that the sign has at least three
      structurally different channels yielding RISK: NONE.

RISK_CASES:

  RISK_CASE_001:
    NAME: ALGORITHMIC_FALSE_POSITIVE_BAN
    INPUT: "I'm dead 💀" (in social media post)
    CONTEXT: automated moderation (NLP / Sentiment Analysis)
    RISK: HIGH
    ATTACK: sentiment_misinterpretation — the algorithm sees 💀 and
      flags the text as "threat of violence/suicide", ignoring the
      EPOCH_3 slang context
    GUARD: epoch_context_required, generational_cohort_analysis,
      slang_dictionary_integration
    AFFECTED_SYSTEMS: Twitter/X moderation, Instagram filters,
      TikTok algorithm, Discord Trust & Safety
    REAL_CASE: Automatic bans for "I'm dead 💀" on TikTok (2022-2023)

  RISK_CASE_002:
    NAME: REAL_THREAT_OBFUSCATION
    INPUT: "I will find you 💀" (in DM)
    CONTEXT: cyberbullying, harassment, stalking
    RISK: HIGH
    ATTACK: intent_obfuscation — a real threat is masked as a "joke",
      using the sign's polysemy. The recipient may interpret it as
      EPOCH_3 (laughter), the sender means EPOCH_1 (death/threat)
    GUARD: behavioral_context_analysis, conversation_history_required,
      human_review_required
    NOTE: The classic "sarcasm as defense" problem — the sender can
      claim "it was just a meme"

  RISK_CASE_003:
    NAME: GENERATIONAL_MISINTERPRETATION
    INPUT: "💀" (from Gen Z to Boomer)
    CONTEXT: intergenerational communication (workplace, family)
    RISK: MEDIUM
    ATTACK: cohort_mismatch — the older generation activates EPOCH_1
      (death/danger), the younger sends EPOCH_3 (laughter). Creates
      panic, misunderstanding, HR incidents
    GUARD: generational_cohort_flag, age_context_analysis,
      explicit_clarification_prompt
    REAL_CASE: Parents report "suicidal moods" of a child to the school
      after receiving a "💀" in a message

  RISK_CASE_004:
    NAME: CANCEL_CULTURE_OSTRACISM
    INPUT: "He is dead to us 💀"
    CONTEXT: social media harassment, cancel culture
    RISK: MEDIUM
    ATTACK: social_ostracism_marker — the sign is used to coordinate
      collective bullying and the "cancellation" of a person. Formally
      EPOCH_3 (irony), functionally EPOCH_1 (social death)
    GUARD: toxicity_proximity_check, collective_behavior_analysis,
      target_vulnerability_assessment
    NOTE: A transition from metaphor to real harm: "social death" can
      lead to real trauma

  RISK_CASE_005:
    NAME: SECOND_HAND_EMBARRASSMENT_DRIFT
    INPUT: "Watching this fail 💀"
    CONTEXT: TikTok, reaction videos, cringe content
    RISK: LOW
    ATTACK: precession_drift — the new meaning "cringe at another's
      failure" is not yet fixed as EPOCH_4, but is actively used.
      Creates uncertainty for parsers
    GUARD: precession_alert_monitoring, DRIFTING_flag,
      context_collection_required
    NOTE: A potential EPOCH_4 — requires documentation after 6-12
      months of observation

  RISK_CASE_006:
    NAME: MEDICAL_MISREAD
    INPUT: "💀" in patient message to doctor
    CONTEXT: telemedicine, mental health apps
    RISK: HIGH
    ATTACK: professional_context_mismatch — in a medical context
      EPOCH_1 (death) is activated automatically, but the patient may
      use EPOCH_3 (humor). Creates a false alarm
    GUARD: professional_domain_flag, patient_history_required,
      explicit_intent_clarification
    AFFECTED_SYSTEMS: BetterHelp, Talkspace, NHS digital services

  RISK_CASE_007:
    NAME: EMOJI_SEQUENCE_INJECTION
    INPUT: "💀💀💀" (triple skull)
    CONTEXT: any digital text
    RISK: LOW
    ATTACK: intensity_escalation — multiple emoji may be interpreted as
      an intensification of a threat (EPOCH_1) instead of an
      intensification of laughter (EPOCH_3)
    GUARD: sequence_context_analysis, repetition_pattern_recognition
    NOTE: "💀💀💀" = "very funny" (EPOCH_3), but an algorithm may read
      it as a "triple threat"

  RISK_CASE_008:
    NAME: CROSS_PLATFORM_EPOCH_MISMATCH
    INPUT: "💀" (sent from Discord to LinkedIn)
    CONTEXT: cross-platform communication
    RISK: MEDIUM
    ATTACK: platform_context_mismatch — platforms have different norms.
      Discord: EPOCH_3 is the norm. LinkedIn: EPOCH_1 may provoke an HR
      reaction
    GUARD: platform_norm_analysis, professional_context_gate,
      tone_transfer_warning

CONFUSABLES:

  CONFUSABLE_001:
    VISIBLE_FORM: ☠️
    CODEPOINT: U+2620
    NAME: SKULL AND CROSSBONES
    RISK: MEDIUM
    RULE: SKULL_AND_CROSSBONES ≠ SKULL_U1F480
    NOTE: ☠️ more often retains EPOCH_1 (danger/poison), whereas 💀 has
      migrated to EPOCH_3. The visual similarity creates a risk of the
      wrong epoch.

  CONFUSABLE_002:
    VISIBLE_FORM: 💀︎ / 💀️
    CODEPOINT: U+1F480 + U+FE0E / U+FE0F
    NAME: SKULL WITH VARIATION SELECTOR
    RISK: LOW
    RULE: TEXT_STYLE_SKULL ≠ EMOJI_STYLE_SKULL
    NOTE: U+FE0E (text style) / U+FE0F (emoji style) — different
      rendering on different platforms, but semantically identical.

  CONFUSABLE_003:
    VISIBLE_FORM: 🦴
    CODEPOINT: U+1F9B4
    NAME: BONE
    RISK: LOW
    RULE: BONE ≠ SKULL
    NOTE: An anatomical link, but different semantics. 🦴 =
      bone/dog/archaeology, 💀 = death/laughter.

  CONFUSABLE_004:
    VISIBLE_FORM: 🎃
    CODEPOINT: U+1F383
    NAME: JACK-O-LANTERN
    RISK: LOW
    RULE: HALLOWEEN_PUMPKIN ≠ SKULL
    NOTE: A contextual partner (often occurs together), but does not
      replace 💀.

  CONFUSABLE_005:
    VISIBLE_FORM: 😵
    CODEPOINT: U+1F635
    NAME: DIZZY FACE
    RISK: LOW
    RULE: DIZZY_FACE ≠ SKULL
    NOTE: Semantic proximity ("dead from laughter"), but 😵 = a face,
      💀 = a skull. Different visual and emotional register.

  CONFUSABLE_006:
    VISIBLE_FORM: 🤡
    CODEPOINT: U+1F921
    NAME: CLOWN FACE
    RISK: LOW
    RULE: CLOWN ≠ SKULL
    NOTE: A contextual replacement in some Gen Z memes ("clown world"),
      but the semantics differ.

CONTRADICTION_GUARDS:

  CG1:
    TRIGGER: "💀 = threat of violence"
    RESPONSE: SKULL_FORM ≠ THREAT
    RULE: 💀 by itself is not proof of a threat. Analysis of the
      context, the sender's cohort, and conversation history is
      required.

  CG2:
    TRIGGER: "💀 = physical death"
    RESPONSE: SKULL_FORM ≠ MORTALITY_PROOF
    RULE: 💀 is not verification of the fact of death. A medical
      context requires additional data.

  CG3:
    TRIGGER: "💀 = safe joke"
    RESPONSE: SKULL_FORM ≠ JOKE_VALIDATION
    RULE: 💀 does not make threatening text a safe joke. Context and
      intent determine the status, not the emoji.

  CG4:
    TRIGGER: "💀 = Gen Z humor"
    RESPONSE: SKULL_FORM ≠ GENERATIONAL_CODE
    RULE: 💀 is not an exclusive marker of a generation. Use by other
      cohorts is possible, but creates ambiguity.

  CG5:
    TRIGGER: "💀💀💀 = triple threat"
    RESPONSE: SKULL_REPETITION ≠ INTENSITY_ESCALATION
    RULE: Multiple 💀 usually mean an intensification of laughter, not
      of a threat. Contextual analysis is required.

  CG6:
    TRIGGER: "☠️ = 💀"
    RESPONSE: SKULL_AND_CROSSBONES ≠ SKULL
    RULE: ☠️ and 💀 have a different semantic history. ☠️ retains
      EPOCH_1, 💀 is active in EPOCH_3. Not interchangeable.

  CG7:
    TRIGGER: "💀 in medical context = patient danger"
    RESPONSE: SKULL_FORM ≠ MEDICAL_STATUS
    RULE: 💀 in a patient's message is not an automatic marker of
      suicide. A clinical, not algorithmic, assessment is required.

  CG8:
    TRIGGER: "💀 from child to parent = suicidal ideation"
    RESPONSE: SKULL_FORM ≠ PARENTAL_ALARM
    RULE: 💀 from a child to a parent more often activates EPOCH_3
      (laughter), not EPOCH_1 (death). Parental alarm may be false.

SEQUENCE_LAYER_BOUNDARY:
  SIGN_SAFE_ALONE ≠ SIGN_SAFE_IN_SEQUENCE: YES

  SC1 (legacy: SEQ_001):
    SEQUENCE: "💀💀💀"
    NAME: TRIPLE_SKULL
    RISK_LEVEL: intensity-dependent
    RULE: TRIPLE_SKULL ≠ TRIPLE_THREAT (usually means strong laughter)

  SC2 (legacy: SEQ_002):
    SEQUENCE: "💀😭"
    NAME: SKULL_PLUS_CRYING
    RISK_LEVEL: combined idiom
    RULE: SKULL_PLUS_CRYING = HYSTERICAL_LAUGHTER (not crying + death)

# PATCH_28 (AUTHOR_DECISION_CONFIRMED, 2026-06-29, found while testing
# the cross-card SC3 with the new SKULL_CROSSBONES_U2620 card): the
# original SEQUENCE contained "💀☠️" — 3 codepoints (skull + crossbones
# + VARIATION_SELECTOR_16 U+FE0F). The SKULL_CROSSBONES_U2620 card uses
# the base VISIBLE_FORM (1 codepoint, no selector) for consistency with
# the "1 sign = 1 position" architecture. The base form "💀☠" (2
# codepoints) occurs as a substring BOTH in text with the selector AND
# without it — without loss of coverage. Status confirmed by Ruslan
# (AUTHOR_DECISION) 2026-06-29.
  SC3 (legacy: SEQ_003):
    SEQUENCE: "💀☠"
    NAME: SKULL_PLUS_SKULL_AND_CROSSBONES
    RISK_LEVEL: epoch_mismatch
    RULE: EPOCH_3 + EPOCH_1 = CONTEXTUAL_CONFLICT. Ambiguity resolution
      is required.

  SC4 (legacy: SEQ_004):
    SEQUENCE: "💀🎃"
    NAME: SKULL_PLUS_PUMPKIN
    RISK_LEVEL: seasonal_context
    RULE: HALLOWEEN_PAIR = EPOCH_1_REACTIVATION (culturally permitted)

  SC5 (legacy: SEQ_005):
    SEQUENCE: "💀💀💀💀💀"
    NAME: MASS_SKULL
    RISK_LEVEL: spam-like
    RULE: MASS_REPETITION ≠ MASS_THREAT (usually = frenzied laughter)

PHAGO_ENTITY_MIMICRY:

  PE_001:
    INPUT: "Verified killer 💀"
    TYPE: SEMANTIC_AMBIGUITY (not PHAGO)
    NOTE: 💀 creates contextual "edginess", but does not imitate an
      authorized carrier. In emoji, PHAGO_ENTITY is rare.

  PE_002:
    INPUT: "💀 as a marker of false popularity"
    TYPE: SEMANTIC_AMBIGUITY (not PHAGO)
    NOTE: 💀 in comments "💀💀💀" creates the illusion of a mass
      reaction, but does not claim a verified status.

============================================================
8. ADVERSARIAL_COVERAGE — RUN_CARD SEED
============================================================

MIN_TOTAL_VECTORS: 12 (6 categories A-F, 2 per category,
  CATEGORY_F = APPLICABLE)

CATEGORY_A: FORM_MANIPULATION (2)
  A1: U+1F480 + U+FE0E (text style) — renders as a black-and-white
    symbol, masking the emoji nature
  A2: U+1F480 + U+FE0F (emoji style) — the standard color render,
    different platforms show a different skull

CATEGORY_B: CONTEXT_INJECTION (2)
  B1: "I'm dead 💀" in a medical chat — the doctor activates EPOCH_1
    (death), the patient meant EPOCH_3 (laughter)
  B2: "💀" in a court document — the lawyer interprets it as a threat
    (EPOCH_1), the defendant as a meme (EPOCH_3)

CATEGORY_C: SEQUENCE_MANIPULATION (2)
  C1: "💀💀💀" — the algorithm reads it as an intensification of a
    threat (EPOCH_1×3), when it is actually frenzied laughter
    (EPOCH_3×3)
  C2: "💀☠️" — an epoch conflict: EPOCH_3 (laughter) + EPOCH_1 (danger)
    = ambiguity for the parser

CATEGORY_D: SEMANTIC_MIMICRY (3)
  D1: "I'm dead 💀" — literal (EPOCH_1: suicidal threat) vs ironic
    (EPOCH_3: laughter) — contextual analysis required
  D2: "💀" from Gen Z to a Boomer — sender: laughter, recipient:
    panic/HR incident (cohort_mismatch)
  D3: "💀" in TikTok comments — creates the illusion of a mass reaction
    (popularity mimicry), not PHAGO

CATEGORY_E: PHAGO_ENTITY_MIMICRY (2)
  NOTE: CATEGORY_E for emoji describes PHAGO-like attacks (astroturfing,
    quasi-entity edginess), but not the classic PHAGO_ENTITY_MIMICRY
    from FO-097. This is an adaptation of the category for the emoji
    domain.
  E1: "💀💀💀" under a viral post — bots imitate an organic mass
    reaction (astroturfing)
  E2: "Verified account 💀" — a quasi-entity uses 💀 to create an
    "edginess" effect, masking commercial interest

CATEGORY_F: SEMANTIC_LAYER_MANIPULATION (3)
  F1: EPOCH_1 reactivation: "💀" in news of a celebrity's death — Gen Z
    comments in EPOCH_3 (laughter), the recipient reads EPOCH_1
    (mourning)
  F2: EPOCH_3 dominance: "💀" in a medical report — the doctor expects
    EPOCH_1 (death), the patient uses EPOCH_3 (irony)
  F3: EPOCH_2 reactivation: "💀" in a millennial context — burnout
    (EPOCH_2) vs laughter (EPOCH_3) — tonal ambiguity

ACTUAL_TOTAL_VECTORS: 14
COVERAGE_STATUS: SUFFICIENT (14 ≥ 12)

============================================================
9. MUTATION_CHECK
============================================================

MUTATION_01:
  CLAIM: 💀 in text proves physical threat
  EXPECTED: FAIL_THREAT_MIMICRY
  RESULT: FAIL

MUTATION_02:
  CLAIM: 💀 makes any toxic text a joke
  EXPECTED: FAIL_HUMOR_MIMICRY
  RESULT: FAIL

MUTATION_03:
  CLAIM: 💀 from child = suicidal ideation
  EXPECTED: FAIL_MEDICAL_MISREAD
  RESULT: FAIL

MUTATION_04:
  CLAIM: 💀💀💀 = triple threat
  EXPECTED: FAIL_INTENSITY_MISREAD
  RESULT: FAIL

MUTATION_05:
  CLAIM: ☠️ = 💀 (interchangeable)
  EXPECTED: FAIL_CONFUSABLE_MISREAD
  RESULT: FAIL

MUTATION_06:
  CLAIM: 💀 in work email = professional humor
  EXPECTED: FAIL_PROFESSIONAL_CONTEXT_MISMATCH
  RESULT: FAIL

============================================================
10. KNOWN_OPEN_QUESTIONS
============================================================

OQ1:
  QUESTION: Will 💀 evolve into EPOCH_4 (second-hand embarrassment /
    cringe marker)?
  STATUS: CLOSED_AS_MONITORING_ITEM
  BLOCKS_WORKINGLY_CLOSED: NO
  NOTE: The DRIFTING status records the trend. If EPOCH_4 is confirmed
    in 12 months — a card patch will be required.

OQ2:
  QUESTION: How should the NLP integrator resolve the collision between
    a real threat (EPOCH_1) and laughter (EPOCH_3) without false
    positives?
  STATUS: CLOSED_AS_DELEGATED_TO_INTEGRATOR
  BLOCKS_WORKINGLY_CLOSED: NO
  NOTE: Collision resolution is the task of the NLP integrator (MODULE
    / SEQUENCE_INTEGRATOR), not the SIGN_CORE_CARD. The card records the
    existence of the collision through CG1-CG4 and RISK_CASE_001/002.
    The concrete resolution algorithm is determined by the integrator.

OQ3:
  QUESTION: Will 💀 be displaced by a new emoji (e.g. 🪦 headstone) as
    a death marker, freeing 💀 for a complete semantic migration into
    humor?
  STATUS: CLOSED_AS_MONITORING_ITEM
  BLOCKS_WORKINGLY_CLOSED: NO
  NOTE: A monitoring question. Does not block the current status. If 🪦
    begins to displace 💀 as a death marker — a card patch will be
    required after 12 months of observation.

ALL_OPEN_QUESTIONS_CLOSED: YES

============================================================
11. PATCH_HISTORY
============================================================

PATCH_HISTORY:
  v0_1: initial WORKING_DRAFT for the migration of 💀 U+1F480 to
    GEN3_v0_3. The content base was carried over from
    SIGN_CORE_CARD_SKULL_U1F480_GEN3_v0_2_PLUS_EPOCH_v0_1_RU without
    substantive changes (EPOCH_TRACKER, RISK_CASES,
    CONTRADICTION_GUARDS, SEQUENCE_LAYER_BOUNDARY, PHAGO_ENTITY_MIMICRY,
    ADVERSARIAL_COVERAGE, MUTATION_CHECK, KNOWN_OPEN_QUESTIONS).
  v0_1_PATCH_01: ZONE: ZONE_3 added as an explicit field in META
    (Coordinator/Claude, 2026-06-25, from a STRUCTURAL_PREFLIGHT AUDIT
    finding) — TYPE_F (fix-patch)
  v0_1_PATCH_02: STATUS_PROGRESSION_TRACKER added to section 1 (a new
    v0_3 section, absent in the legacy document) (Coordinator/Claude,
    2026-06-25) — TYPE_F (fix-patch)
  v0_1_PATCH_03: LIMITATION_STATEMENT — the line "WORKINGLY_CLOSED ≠
    ARTIFACT_CONFIRMED" was added (the status did not exist at the time
    the legacy document was created) (Coordinator/Claude, 2026-06-25) —
    TYPE_F (fix-patch)
  v0_1_PATCH_04: CARD_UID / DOCUMENT_ID / TEMPLATE_LINE renamed from
    GEN3_v0_2_PLUS_EPOCH to GEN3_v0_3 (Coordinator/Claude, 2026-06-25) —
    TYPE_F (fix-patch)
  v0_1_PATCH_05: CONFUSABLES (6 entries) — the field SIGN: renamed to
    VISIBLE_FORM: (a legacy field name forbidden by NAMING_NORM, the
    same class of finding as PATCH_NOTE_TEMPLATE_v0_3_P1 on DOT)
    (Coordinator/Claude, 2026-06-25) — TYPE_F (fix-patch)
  v0_1_PATCH_06: AUTHOR_DECISION_REFERENCE / RUN_CARD_REFERENCE /
    RUN_CARD_STATUS reset to PENDING / PENDING / NOT_STARTED — the new
    v0_3 artifact line does not inherit the legacy WORKINGLY_CLOSED
    status automatically, STRUCTURAL_PREFLIGHT_PASS and
    CONVEYOR_REVIEW_PASS must be passed anew (Coordinator/Claude,
    2026-06-25) — TYPE_F (fix-patch)
  v0_1_PATCH_07: SAFE_CASES expanded from 4 to 6 (added SAFE_CASE_005 —
    game UI context, SAFE_CASE_006 — academic/anatomical context), to
    meet MIN=6 per the v0_3 rules (Coordinator/Claude, 2026-06-25,
    content proposed, requires review) — TYPE_P (content-patch)
  v0_1_PATCH_08: PRECESSION_ALERT.LAST_CHECK updated from the obsolete
    legacy date (2026-06-18) to the re-attestation date (2026-06-25);
    the original date preserved as ORIGINAL_BASELINE_CHECK for
    traceability; TRIGGER reformulated as "re-attestation on migration
    to GEN3_v0_3" (the finding was unanimously confirmed by 5
    independent runs — coordinator-draft, Gemini, GPT-5.5, Qwen, Grok;
    all classified it as MINOR, no divergence) — TYPE_F (fix-patch)

PATCHES_APPLIED: 11
PATCHES_VERIFIED: 8/8 (content patches 01-08, covered by
  STRUCTURAL_PREFLIGHT_PASS / CONVEYOR_REVIEW_PASS / TIER_3
  SIMULATION_GATE — all three rounds confirmed exactly this version of
  the content)
PATCHES_09_11_NOTE: patches 09-11 (below) — NOT substantive, they touch
  only governance fields (DOCUMENT_STATUS, AUTHOR_DECISION_REFERENCE,
  STATUS_PROGRESSION_TRACKER, LIMITATION_STATEMENT), not part of the set
  of fields consumed by MODULE_TEMPLATE at STAGE_3c (CAPTURE_HISTORY,
  SAFE_CASES, RISK_CASES, CONTRADICTION_GUARDS, BASE_FORMULAS, etc. —
  all 16 substantive fields were unchanged since the TIER_3 run).
  Verified by an explicit comparison 2026-06-25: a repeat
  SIMULATION_GATE is not required. These patches are logged here
  retroactively — they were initially made without a record in
  PATCH_HISTORY, which is itself a finding (a failure to observe the
  project's own discipline), fixed on the author's direct question.
  v0_1_PATCH_09: AUTHOR_DECISION_REFERENCE updated to
    AUTHOR_DECISION_20260625_002 (WORKINGLY_CLOSED), DOCUMENT_STATUS
    WORKING_DRAFT → WORKINGLY_CLOSED, STATUS_PROGRESSION_TRACKER brought
    into line (Coordinator/Claude, 2026-06-25, execution of a
    previously confirmed AUTHOR_DECISION) — TYPE_F (fix-patch,
    governance-only)
  v0_1_PATCH_10: TIER3_ARBITRATION_NOTE added to section 1;
    SIMULATION_GATE_PASSED: YES recorded after the author's arbitration
    on CONTEXT_3 (Coordinator/Claude, 2026-06-25) — TYPE_P
    (content-patch, governance-only — does not change LAYER_A/B/C)
  v0_1_PATCH_11: DOCUMENT_STATUS WORKINGLY_CLOSED → ARTIFACT_CONFIRMED,
    AUTHOR_DECISION_REFERENCE updated to AUTHOR_DECISION_20260625_003;
    LIMITATION_STATEMENT (section 12) updated — the obsolete line
    "WORKING_DRAFT ARTIFACT (until ARTIFACT_CONFIRMED is obtained)"
    replaced with the wording for ARTIFACT_CONFIRMED, added
    ARTIFACT_CONFIRMED ≠ LOCKED_WORKING_CORE / PRODUCTION_READY /
    SECURITY_PROOF (finding: Gemini, execution: Coordinator/Claude,
    2026-06-25) — TYPE_F (fix-patch, governance-only)

============================================================
12. LIMITATION_STATEMENT
============================================================

LIMITATION_STATEMENT:
  THIS_CARD IS AN ARTIFACT_CONFIRMED ARTIFACT
    (AUTHOR_DECISION_20260625_003, 2026-06-25)
  NOT A FINAL_STANDARD
  NOT A PARSER
  NOT A RUNTIME
  NOT A SECURITY_CERTIFICATE
  CONVEYOR_PASS ≠ VALIDATION
  RUN_CARD_RESULT ≠ FINAL_STATUS
  ARTIFACT_CONFIRMED ≠ LOCKED_WORKING_CORE
  ARTIFACT_CONFIRMED ≠ PRODUCTION_READY
  ARTIFACT_CONFIRMED ≠ SECURITY_PROOF (see the LIMITATION_STATEMENT of
    section 1 — CONVEYOR_PASS/MODEL_CONSENSUS/GUARDS_HOLD are not
    equivalent to validation or a proof of security)

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
