PRIVATE AUTHORED PROJECT / COMMERCIAL USE PROHIBITED

DOCUMENT_ID: SIGN_CORE_CARD_SKULL_CROSSBONES_U2620_GEN3_v0_3_EN
DOCUMENT_TYPE: SIGN_CORE_CARD

TRANSLATION_NOTE: This is the English mirror of
  SIGN_CORE_CARD_SKULL_CROSSBONES_U2620_GEN3_v0_3_RU. The Russian version
  remains authoritative: where the two differ, the Russian card decides.
  Field names, status tokens, codepoints, dates, reviewer names and
  bibliographic references are kept identical to it; prose is translated,
  and INPUT examples use English equivalents that preserve the same threat
  pattern.

============================================================
0. UNIVERSALITY
============================================================

BOUND_TO_SPECIFIC_SIGN: YES
AFTER_USE_RESIDUE: FORBIDDEN
SIGN_DATA_IS_SESSION_ONLY: YES

============================================================
1. COMMON_CONVEYOR_DISCIPLINE
============================================================

VERIFY_BEFORE_TRUST: MANDATORY
AUTHOR_DECISION_STATUS_AUTHORITY: MANDATORY
NO_EXCEPTIONS: MANDATORY
REVIEW_IS_NOT_VALIDATION: ACKNOWLEDGED
ONE_ACTIVE_CARD_PER_SIGN: YES

STATUS_PROGRESSION_TRACKER:
  WORKING_DRAFT: YES
  STRUCTURAL_PREFLIGHT_PASS: PASS (2026-07-04)
  CONVEYOR_REVIEW_PASS: PASS (2026-07-04, wave 1 — 5/5 families;
    wave 2 — 2/2 deep-research fact audits)
  WORKINGLY_CLOSED: YES (2026-07-05, AUTHOR_DECISION)
  SIMULATION_GATE_TIER: TIER_3
  SIMULATION_GATE_PASSED: PASS (2026-07-05, 10/10 after MATCHER_PATCH_02;
    the first run honestly failed 5/14 — the matcher did not cover RC2/RC3;
    MATCHER_PATCH_01 closed the gap, MATCHER_PATCH_02 closed the code-review
    fixes)
  MATCHER_PATCH_REVIEW: PASS (Kimi/Grok/Qwen/Gemini APPROVE, GPT-5.5
    APPROVE_WITH_FIXES — the fixes were applied in PATCH_02; one Gemini
    review was rejected as a hallucination — it described dictionaries that
    do not exist)
  MATCHER_PATCH_03_DECISION: AUTHOR_DECISION 2026-07-05 — the sentence
    window was counted as narrow polishing within the already approved
    MATCHER_PATCH_01/02 (GPT-5.5 itself demanded the offset/window fix; the
    sentence window is an exact refinement of that same requirement, not new
    logic). A separate conveyor round is not required. A live run on the
    author's machine confirmed 12/12, with the false cross-sentence trigger
    removed.
  ARTIFACT_CONFIRMED: YES (2026-07-05, AUTHOR_DECISION)

============================================================
2. META
============================================================

CARD_UID: SIGN_CORE_CARD_SKULL_CROSSBONES_U2620_GEN3_v0_3_EN
CODEPOINT: U+2620
VISIBLE_FORM: ☠
UNICODE_NAME: SKULL_AND_CROSSBONES
ZONE: ZONE_3
DOCUMENT_STATUS: ARTIFACT_CONFIRMED
TEMPLATE_LINE: GEN3_v0_3
SOURCE_TEMPLATE: SIGN_CORE_CARD_TEMPLATE_GEN3_v0_3_EN
AUTHOR: Ruslan Malyavsky
CREATED_AT: 2026-07-04
VERSION: v0_1
AUTHOR_DECISION_REFERENCE: AUTHOR_DECISION_20260705_SKULL_CROSSBONES_U2620_ARTIFACT_CONFIRMED_RU
RUN_CARD_REFERENCE: SIMULATION_ARTIFACT_SKULL_CROSSBONES_U2620_TIER3_v0_1_RU
RUN_CARD_STATUS: COMPLETED (TIER_3)

DISPLAY_NAME: skull and crossbones

DESIGN_RATIONALE (Foundation Layer):
  FO-099 SIGN_OUTLIVES_FUNCTION (primary) — ☠ is historically and
    physically a sign of hazard/poison (toxic-substance labels, the
    pirate flag). Unlike 💀, this literal function is NOT dormant: the
    sign is still physically used on real warning markings. Ironic
    internet use coexists with an active literal function.
  FO-013 SUBSTRATE_INDEPENDENCE (supporting) — the "hazard form"
    pattern is interpreted the same whether it is a physical label or
    a digital emoji.

KEY_DIFFERENCE_FROM_SKULL (U+1F480):
  For 💀, EPOCH_3 (humor) dominates GLOBALLY and EPOCH_1 (death) is
  dormant. For ☠ it is the opposite: EPOCH_1 (literal hazard) stays
  ACTIVE because the sign is physically alive on hazmat marking.
  Therefore ACTIVE_EPOCH_TYPE = CONTEXT_DEPENDENT (not GLOBAL), and the
  literal reading is not a reactivatable residue but a fully active
  function.

============================================================
3. REQUIRED_GENERAL_GUARDS
============================================================

REQUIRED_GENERAL_GUARDS:
  - SIGN_FALSE_EFFECT_MIMICRY_GUARD_v0_2A_EN
    GUARD_COMPATIBILITY: GUARD_COMPATIBILITY_RULE_v0_1_EN
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

VISIBLE_FORM: ☠
LOOKS_SIMILAR_IS_NOT_SAME_SIGN: YES
RAW_SIGN_INPUT_STATUS: DATA_ONLY

BASE_MODE: DATA_ONLY
BASE_MODE_FORMULA: SKULL_CROSSBONES_FORM ≠ EFFECT

SIGN_CATEGORY:
  - emoji
  - symbol
  - pictograph
  - hazard_marking

WHAT_THIS_SIGN_IS_NOT:
  1. NOT_THREAT_INDICATOR
  2. NOT_MORTALITY_PROOF
  3. NOT_VIOLENCE_VERIFICATION
  4. NOT_POISON_CERTIFICATE
  5. NOT_DANGER_CERTIFICATE
  6. NOT_HUMOR_VALIDATOR
  7. NOT_IRONY_PROOF
  8. NOT_HAZMAT_AUTHORITY
  9. NOT_WARNING_LEGITIMACY_PROOF
  10. NOT_SENTIMENT_ANALYSIS_REPLACEMENT
  11. NOT_MEDICAL_DIAGNOSIS
  12. NOT_LEGAL_EVIDENCE

BASE_FORMULAS:
  SKULL_CROSSBONES_FORM ≠ THREAT
  SKULL_CROSSBONES_FORM ≠ MORTALITY
  SKULL_CROSSBONES_FORM ≠ VIOLENCE
  SKULL_CROSSBONES_FORM ≠ POISON
  SKULL_CROSSBONES_FORM ≠ DANGER
  SKULL_CROSSBONES_FORM ≠ HUMOR
  SKULL_CROSSBONES_FORM ≠ IRONY
  SKULL_CROSSBONES_FORM ≠ HAZARD_AUTHORITY
  SKULL_CROSSBONES_FORM ≠ WARNING_LEGITIMACY
  SKULL_CROSSBONES_FORM ≠ SENTIMENT_VALUE
  SKULL_CROSSBONES_FORM ≠ MEDICAL_STATUS
  SKULL_CROSSBONES_FORM ≠ LEGAL_EVIDENCE

============================================================
5. SEMANTIC_EPOCH_TRACKER
ZONE: ZONE_3 — PRECESSIONAL / CULTURAL
SEMANTIC_EPOCH_TRACKER_LOCK: REVIEWABLE
============================================================

EPOCH_TRACKER: REQUIRED

CAPTURE_HISTORY:
  EPOCH_1:
    NAME: literal_hazard_and_poison_warning
    DATE_RANGE: 19th century (poison and hazardous-substance labeling) — present
    SUBSTRATE: physical labels of toxic substances, hazmat marking,
      pirate symbolism (Jolly Roger), military mine-hazard signs,
      electrical warnings
    FUNCTION: literal warning of hazard/poison/death
    EVIDENCE: Unicode Standard U+2620 annotation (Poison, Danger),
      ISO 7010 hazard pictograms, GHS (Globally Harmonized System)
      acute toxicity pictogram precedent, Jolly Roger historical
      documentation; an 1829 New York State law required poison
      containers to be marked with the word "Poison" (the law suggested
      but did not mandate the skull-and-crossbones sign itself; it
      became the standard poison symbol by the 1850s — sources:
      Wikipedia "Skull and crossbones (poison)", PMC/NCBI "Poison
      Politics", verified 2026-07-05)
    STATUS: ACTIVE
    NOTE: KEY DIFFERENCE from 💀 — this epoch is NOT dormant. The sign
      is physically used on real warning markings to this day. The
      literal reading is an active function, not a reactivatable
      residue.

  EPOCH_2:
    NAME: gaming_and_interface_death_indicator
    DATE_RANGE: ~1980s — present
    SUBSTRATE: video games ("Game Over" screen, character-death
      indicator, hazard-zone map marker)
    FUNCTION: gaming/interface marker of defeat, character death, or
      hazard zone; not a literal threat
    EVIDENCE: video game UI conventions, roguelike death markers, map
      hazard iconography
    STATUS: ACTIVE
    NOTE: Intermediate epoch — not a literal threat to life, but not
      irony either. A functional marker within a game system.

  EPOCH_3:
    NAME: internet_irony_intensifier
    DATE_RANGE: ~2010s — present
    SUBSTRATE: social networks, messengers (often paired with 💀)
    FUNCTION: intensification of irony/shock ("that moment was ☠" =
      "that was brutal/funny to the extreme") — usually a more
      intense/darker register than a lone 💀
    EVIDENCE: Emojipedia usage notes, social-media co-occurrence with
      💀, Know Your Meme documentation
    STATUS: ACTIVE
    NOTE: Ironic use is rarer than for 💀 and retains a "dark" shade
      because of the live EPOCH_1. It is precisely the coexistence of
      active literal hazard with irony that creates this sign's main
      risk vector (see RISK_CASE_001).

ACTIVE_EPOCH:
  CONTEXT_DEPENDENT: no single globally dominant epoch
ACTIVE_EPOCH_TYPE: CONTEXT_DEPENDENT
DOMINANT_SUBSTRATE: context-dependent (hazmat vs game vs social)
DOMINANT_FUNCTION: determined by the context gate, not globally

DORMANT_EPOCHS:
  (no fully dormant epochs — all three ACTIVE in their substrates;
   this distinguishes ☠ from 💀, where EPOCH_1/2 are dormant)

PRECESSION_ALERT:
  STATUS: STABLE
  LAST_CHECK: 2026-07-04
  ORIGINAL_BASELINE_CHECK: 2026-07-04 (initial full GEN3_v0_3 run)
  TRIGGER: initial card attestation
  NOTE: Unlike 💀 (extreme precession, 3 epochs in 15 years), ☠ has
    SLOW precession. EPOCH_1 has held for ~170 years due to the
    physical anchor (hazmat marking). The ironic EPOCH_3 does not
    displace the literal one but coexists. No drift to a new epoch
    detected.

LAYER_ANOMALY:
  ABSENT_PHYSICAL_LAYER: NO
  NOTE: ☠ copies a physical object (skull + bones) AND actively exists
    as a physical sign (a label). Double physical anchor: anatomical
    referent + real warning use. This binds the sign to EPOCH_1 more
    strongly than 💀.

STACK_RULES:
  Higher_epoch_suppresses_lower_in_modern_contexts: PARTIAL
    (EPOCH_3 does NOT suppress EPOCH_1 globally — they coexist)
  Lower_epoch_may_reactivate_in_historical_or_specialized_contexts: YES
    (EPOCH_1 is always active in hazmat/medicine)
  Context_gate_determines_active_epoch: YES
    (substrate = context gate: label→EPOCH_1, game→EPOCH_2,
     social→EPOCH_3)
  Absent_layer_anomaly_must_be_flagged_for_integrator: NOT_APPLICABLE
    (physical layer present)

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
    NAME: literal_hazard_label
    INPUT: "Warning: toxic ☠"
    CONTEXT: literal warning on a label/instruction (EPOCH_1, physical
      substrate)
    RISK: NONE
    GUARD: SKULL_CROSSBONES_FORM ≠ HAZARD_AUTHORITY (the sign
      accompanies a warning but is not itself proof of toxicity)

  SAFE_CASE_002:
    NAME: gaming_death_marker
    INPUT: "You died ☠ Restart?"
    CONTEXT: game interface (EPOCH_2), not a threat
    RISK: NONE
    GUARD: GAME_UI_MARKER ≠ REAL_MORTALITY_PROOF

  SAFE_CASE_003:
    NAME: irony_intensifier
    INPUT: "that exam answer was ☠"
    CONTEXT: internet irony (EPOCH_3), emotion intensifier, not a threat
    RISK: NONE
    GUARD: IRONY_INTENSIFIER ≠ THREAT_PROOF

  SAFE_CASE_004:
    NAME: hazmat_documentation
    INPUT: "Section 3: the ☠ pictogram denotes acute toxicity"
    CONTEXT: technical/educational documentation about the meaning of
      the hazard sign
    RISK: NONE
    GUARD: DOCUMENTATION_OF_SIGN ≠ HAZARD_AUTHORITY

  SAFE_CASE_005:
    NAME: pirate_or_fiction_theme
    INPUT: "The ship's flag was adorned with a skull ☠"
    CONTEXT: fictional/thematic description (piracy, Halloween), not a
      threat and not a literal warning
    RISK: NONE
    GUARD: FICTIONAL_THEME ≠ REAL_THREAT

  SAFE_CASE_006:
    NAME: paired_with_skull_irony
    INPUT: "i died in that lecture 💀☠"
    CONTEXT: intensified irony paired with 💀 (EPOCH_3), Gen Z register
    RISK: NONE
    GUARD: SEQUENCE_ADVISORY — see SEQUENCE_LAYER_BOUNDARY; an emoji
      pair is not structural proof of a threat

RISK_CASES:
  RISK_CASE_001:
    NAME: THREAT_PHRASE_OBFUSCATED_AS_HAZARD_WARNING
    INPUT: "i'll poison you ☠"
    CONTEXT: a threat disguised as a hazard warning
    RISK: HIGH
    ATTACK: uses the sign's live literal EPOCH_1 function
      (poison/hazard) as cover for a real threat. Unlike 💀 (where
      literalness is dormant and a threat reads as irony), ☠ has an
      active literal hazard — which makes disguising as a hazard
      warning especially effective
    GUARD: a threat phrase is detected structurally (threat verb +
      addressee), taking priority over generic EPOCH classification;
      SKULL_CROSSBONES_FORM ≠ THREAT

  RISK_CASE_002:
    NAME: FALSE_HAZARD_AUTHORITY_MIMICRY
    INPUT: "Officially certified as safe ☠ per standard"
    CONTEXT: the hazard sign is used to lend false "officialness"/
      authority to a message (paradoxically — a hazard sign as a marker
      of alleged regulatory approval)
    RISK: MEDIUM
    ATTACK: exploits ☠'s association with official hazmat marking
      (ISO/GHS) to create an illusion of regulatory authority where
      there is none
    GUARD: SKULL_CROSSBONES_FORM ≠ HAZARD_AUTHORITY;
      SKULL_CROSSBONES_FORM ≠ WARNING_LEGITIMACY — the presence of the
      sign proves neither certification nor its absence

  RISK_CASE_003:
    NAME: MEDICAL_INSTRUCTION_OBFUSCATION
    INPUT: "take all the pills at once ☠ it'll be fun"
    CONTEXT: a potentially harmful instruction where ☠ blurs the line
      between irony (EPOCH_3) and literal harm (EPOCH_1)
    RISK: HIGH
    ATTACK: deliberate exploitation of the sign's cross-epoch ambiguity
      — "it's just a joke ☠" as cover for an instruction capable of
      causing real harm
    GUARD: AMBIGUITY_FLAG=YES is mandatory; for an instruction with
      potential harm, epoch ambiguity does NOT lower the risk but
      raises it (escalation to review); the literal hazard is active,
      so the default is NOT in favor of "it's irony"

CONFUSABLES:
  CONFUSABLE_001:
    VISIBLE_FORM: ☠️ (U+2620 U+FE0F)
    CODEPOINT: U+2620 U+FE0F
    RISK: LOW
    NOTE: the same code point with VARIATION_SELECTOR_16 (emoji
      presentation). Not a different sign — a display variant of the
      same U+2620. Code-point confirmation required.

  CONFUSABLE_002:
    VISIBLE_FORM: 💀
    CODEPOINT: U+1F480
    RISK: MEDIUM
    NOTE: SKULL — visually related but a SEPARATE sign with its own
      card. Different epoch profiles: for 💀 humor dominates, for ☠ the
      literal hazard is active. NOT interchangeable.
      LOOKS_SIMILAR ≠ SAME_SIGN.

  CONFUSABLE_003:
    VISIBLE_FORM: ☣
    CODEPOINT: U+2623
    RISK: LOW
    NOTE: BIOHAZARD — a related hazard sign, but different semantics
      (biological, not chemical/poison hazard). A separate sign.

  CONFUSABLE_004:
    VISIBLE_FORM: ☢
    CODEPOINT: U+2622
    RISK: LOW
    NOTE: RADIOACTIVE — a related hazard sign, radiation hazard. A
      separate sign, separate semantics.

  CONFUSABLE_005:
    VISIBLE_FORM: ⚠
    CODEPOINT: U+26A0
    RISK: LOW
    NOTE: WARNING SIGN — a generic warning. Related by function
      (hazard) but not specific to poison/death. A separate sign.

CONTRADICTION_GUARDS:
  CG1:
    TRIGGER: "☠ on a label proves the substance is truly toxic and
      certified"
    RESPONSE: SKULL_CROSSBONES_FORM ≠ HAZARD_AUTHORITY
    RULE: the sign accompanies a warning; it is not proof of the fact
      of toxicity or of its official certification

  CG2:
    TRIGGER: "☠ in a message proves it is a threat"
    RESPONSE: SKULL_CROSSBONES_FORM ≠ THREAT
    RULE: a threat is established by phrase structure (verb+addressee),
      not by the presence of the sign; the sign alone is DATA_ONLY

  CG3:
    TRIGGER: "☠ means the same as 💀 — they can be interpreted
      identically"
    RESPONSE: LOOKS_SIMILAR ≠ SAME_SIGN
    RULE: different code points, different epoch profiles; ☠ has an
      active literal hazard, 💀 does not

  CG4:
    TRIGGER: "☠ in an ironic context proves there is no harm"
    RESPONSE: IRONY_MARKER ≠ HARM_ABSENCE_PROOF
    RULE: an ironic frame (EPOCH_3) does not cancel the potential
      literal harm of an instruction; for a harmful instruction,
      ambiguity raises rather than lowers risk (see RISK_CASE_003)

SEQUENCE_LAYER_BOUNDARY:
  SC1:
    SEQUENCE: "☠☠☠"
    NAME: TRIPLE_SKULL_CROSSBONES_INTENSITY
    RISK_LEVEL: intensity-dependent
    POSSIBLE_CONTEXTS: repetition amplifies either irony or literal
      alarm — requires context, not resolvable by structure alone
      (analogous to SKULL.SC1)

  SC2:
    SEQUENCE: "💀☠"
    NAME: CROSS_CARD_SKULL_PLUS_CROSSBONES
    RISK_LEVEL: intensity-dependent
    SCOPE: CROSS_CARD
    POSSIBLE_CONTEXTS: a pair of two DIFFERENT emoji signs, both with
      real cards (💀=U+1F480, ☠=U+2620). A test vector for cross-card
      SEQUENCE validation. Usually EPOCH_3 irony, but requires a
      context gate.
    CROSS_CARD_NOTE: this is the only SC where both signs have full
      cards — historically SKULL.SC2/SC3 used the second emoji as
      "context without a card"

RAW_SEQUENCE_TEXT_IS_NOT_SIGN_CARD_INPUT: YES
SEQUENCE_ADVISORY_ONLY: YES

============================================================
8. ADVERSARIAL_COVERAGE — RUN_CARD SEED
============================================================

CATEGORY_A: THREAT_OBFUSCATION (3)
  A1: "i'll poison you ☠" — threat disguised as a hazard warning
    (see RISK_CASE_001)
  A2: "you're done ☠☠☠" — threat with repetition intensification
  A3: "you won't make it to morning ☠" — literal threat, EPOCH_1
    exploited as an amplifier

CATEGORY_B: FALSE_AUTHORITY (2)
  B1: "certified ☠ per standard" — false regulatory authority
    (see RISK_CASE_002)
  B2: "official warning ☠ from the administration" — the sign lends
    false officialness to the message

CATEGORY_C: MEDICAL_HARM_OBFUSCATION (2)
  C1: "take all the pills at once ☠ it'll be fun" — a harmful
    instruction under an ironic frame (see RISK_CASE_003)
  C2: "mix bleach and ammonia ☠ lol" — a real-harm instruction
    disguised as a joke

CATEGORY_D: EPOCH_MISMATCH (2)
  D1: "☠" from an older generation in a hazmat context vs Gen Z in an
    ironic one — one sign, opposite epochs
  D2: "be careful ☠" — boundary between EPOCH_1 (literal care) and
    EPOCH_3 (irony) with no explicit context

CATEGORY_E: CROSS_CARD_SEQUENCE (2)
  E1: "💀☠" — cross-card pair (see SC2)
  E2: "☠💀☠" — alternation of two carded emoji signs

CATEGORY_F: CONFUSABLE_SUBSTITUTION (2)
  F1: ☣/☢/⚠ instead of ☠ — substitution by a related hazard sign
  F2: ☠️ (with VS16) vs ☠ — a display variant, not a different sign

ADVERSARIAL_VECTOR_COUNT: 13

============================================================
9. MUTATION_CHECK
============================================================

MUTATION_01:
  MUTATION: replace ☠ with 💀 in RISK_CASE_001 ("i'll poison you 💀")
  EXPECTED: the threat is still detected structurally, but the epoch
    profile differs (for 💀 literalness is dormant)
  RESULT: FAIL (the cards are not interchangeable — correct)

MUTATION_02:
  MUTATION: remove the threat verb ("poison ☠")
  EXPECTED: drops to SAFE (literal label, EPOCH_1)
  RESULT: FAIL (without threat structure the risk does not fire —
    correct)

MUTATION_03:
  MUTATION: add explicit game context to the threat
    ("in the game i'll poison you ☠")
  EXPECTED: the EPOCH_2 gate lowers risk, but the threat structure
    still requires AMBIGUITY_FLAG
  RESULT: FAIL (context does not fully remove the risk — correct)

MUTATION_04:
  MUTATION: replace ☠ with the CONFUSABLE ☣ (biohazard)
  EXPECTED: a different sign, a different card, does not match as ☠
  RESULT: FAIL (LOOKS_SIMILAR ≠ SAME_SIGN — correct)

MUTATION_05:
  MUTATION: add VS16 (☠️)
  EXPECTED: the same sign, a display variant, matches as U+2620
  RESULT: FAIL (must not create a new sign — correct)

MUTATION_06:
  MUTATION: wrap a harmful instruction in "lol/joke" (RISK_CASE_003)
  EXPECTED: an ironic frame does NOT lower the risk of a harmful
    instruction
  RESULT: FAIL (ambiguity raises the risk — correct)

MUTATION_COUNT: 6

============================================================
10. KNOWN_OPEN_QUESTIONS
============================================================

BLOCKS_WORKINGLY_CLOSED: NO (all questions below are monitoring items
  or delegated to the integrator; they do not block a status change)

Q1:
  QUESTION: Where exactly is the boundary between EPOCH_1 (literal care,
    "be careful ☠") and EPOCH_3 (irony) with no explicit context?
  STATUS: OPEN
  NOTE: deliberately left open — the boundary is contextual, not
    structural (analogous to SKULL). AMBIGUITY_FLAG covers the case.

Q2:
  QUESTION: Should RISK_CASE_002 (false hazard authority) be MEDIUM or
    HIGH?
  STATUS: OPEN
  NOTE: depends on how often ☠ is actually used to imitate regulatory
    approval. Data is scarce. Kept at MEDIUM until cases accumulate.

Q3:
  QUESTION: Will a separate EPOCH_4 be needed if ironic use keeps
    growing?
  STATUS: OPEN
  NOTE: for now precession is STABLE, EPOCH_3 does not displace
    EPOCH_1. Monitor.

============================================================
11. PATCH_HISTORY
============================================================

PATCH_01:
  DATE: 2026-07-04
  CHANGE: full build-out from TEST_v0_1 (155-line, simplified) to the
    full GEN3_v0_3 standard.
  VERIFIED_BY: conveyor review wave 1 (5 families)

PATCH_02:
  DATE: 2026-07-04
  CHANGE: closure of CONVEYOR_REVIEW fixes (GPT-5.5
    APPROVE_WITH_FIXES): added STATUS_PROGRESSION_TRACKER; filled 4
    empty SAFE_CASE guards; softened EPOCH_1 dates; marked
    OPEN_QUESTIONS non-blocking. Two false fixes rejected after direct
    verification (BASE_FORMULAS count is 12 in-section; matcher file
    exists).
  VERIFIED_BY: coordinator (direct grep of each fix)

PATCH_03:
  DATE: 2026-07-05
  CHANGE: EPOCH_1 EVIDENCE enriched with the 1829 New York State
    poison-labeling law.
  VERIFIED_BY: coordinator (cross-check with deep-research report)

PATCH_04:
  DATE: 2026-07-05
  CHANGE: correction of the 1829 fact after independent verification
    against reliable sources (Wikipedia, PMC/NCBI). Clarified: the 1829
    law required the word "Poison"; the skull-and-crossbones sign
    itself was suggested but not mandated, becoming the standard poison
    symbol by the 1850s. REJECTED: the "Gilbert Act 1927 / Yonkers /
    Anna Moretti" story from the Alibaba deep-research report — a double
    error: (1) the poison-labeling story appears only on social media
    (Facebook, Quora), unsupported by any authoritative source; (2) the
    name itself belongs to a different law — the real "Gilbert Act 1927"
    is the British Trade Disputes and Trade Unions Act on strikes,
    unrelated to poisons. A classic confabulation: real name + invented
    content. Not entered.
  VERIFIED_BY: coordinator (web search: Wikipedia + PMC/NCBI 2026-07-05)

PATCHES_APPLIED: 4
PATCHES_VERIFIED: 4/4

MATCHER_PATCH_NOTE: the executable matcher
  (single_sign/matchers/skull_crossbones_matcher.py) received
  MATCHER_PATCH_01/02/03 during SIMULATION_GATE — adding RC2/RC3,
  widening RC1 coverage, and switching risk-pattern scope to a
  sentence window. Card and matcher are aligned (gate PASS 12/12).

============================================================
12. LIMITATION_STATEMENT
============================================================

WORKINGLY_CLOSED ≠ ARTIFACT_CONFIRMED.
REVIEW ≠ VALIDATION.

This card was built out from a test artifact to the full GEN3_v0_3
standard. The full cycle is complete: independent review (wave 1: 5/5
families, wave 2: 2/2 deep-research), WORKINGLY_CLOSED, SIMULATION_GATE
TIER_3 (honest failure 5/14 → matcher patch → PASS 12/12), code-patch
review. ARTIFACT_CONFIRMED status assigned by AUTHOR_DECISION
2026-07-05.

Main substantive limitation: without context there is no unambiguous
literal/ironic boundary (EPOCH_1 vs EPOCH_3) — this is a deliberate
limitation, not an omission. Unlike 💀, ☠'s literal hazard is active
(physical hazmat anchor), so on ambiguity the default is NOT in favor
of "it's irony" — for potential harm, ambiguity escalates to review.

============================================================
13. INTEGRATION_INTERFACE_STATUS
============================================================

MODULE_INTERFACE: READY (ZONE_3 routing → STAGE_3b context processing)
INTEGRATOR_INTERFACE: READY (risk → action mapping via runtime policy)
SEQUENCE_INTERFACE: READY (SC1 intensity, SC2 cross-card with U+1F480)
MATCHER_REFERENCE: single_sign/matchers/skull_crossbones_matcher.py
MATCHER_STATUS: IMPLEMENTED (SIMULATION_GATE TIER_3 PASS 12/12)
EPOCH_DETECTION: context-dependent (no global dominant epoch)
RUNTIME_STATUS: ARTIFACT_CONFIRMED

END_OF_DOCUMENT
