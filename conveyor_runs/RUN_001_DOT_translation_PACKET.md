PRIVATE AUTHORED PROJECT / COMMERCIAL USE PROHIBITED

RULE_REMINDER: VERIFY_BEFORE_TRUST_MANDATORY
RULE_REMINDER: TRANSLATION REVIEW — both EN and RU provided.

DOCUMENT_ID: CONVEYOR_RUN_PACKET_MSL_MIP_DOT_CARD_TRANSLATION_v0_1
PACKET_TYPE: REVIEW
PACKET_SUBTYPE: CARD_TRANSLATION_REVIEW

CONTEXT: First of the sign-card translations for international
publication: DOT (U+002E), an ARTIFACT_CONFIRMED card. AUTHOR_DECISION:
English cards use English INPUT examples (not transliteration) that
preserve the same threat pattern. Russian remains authoritative.

PART A — MATERIALS
- SIGN_CORE_CARD_DOT_U002E_GEN3_v0_3_EN.md (translation)
- SIGN_CORE_CARD_DOT_U002E_GEN3_v0_3_RU__2_.md (authoritative)

PART B — WHAT TO CHECK
B.1. FIELD/TOKEN INTEGRITY: every field name, status token, codepoint
  (U+XXXX), and formula (DOT_FORM ≠ ...) identical between EN and RU.
  Diff the 11 BASE_FORMULAS and the 10 EFFECT_FIELDS.
B.2. SECTION STRUCTURE: sections 0-13 present, same order, same
  numbering. All 6 SAFE_CASES, 6 RISK_CASES, 6 CONFUSABLES, 6
  CONTRADICTION_GUARDS, 6 MUTATIONS present.
B.3. CODEPOINT INTEGRITY of confusables: U+2027, U+00B7, U+3002,
  U+0660, U+FF61, U+2024 — all six identical, with identical RISK
  levels and RULE names.
B.4. EXAMPLE EQUIVALENCE: the translated INPUT examples must preserve
  the SAME threat pattern as the Russian. Check specifically:
    - RISK_CASE_001: RU pseudo-official notice → EN "Notice
      No.A.1.7-OFFICIAL" — same "dots create false officialdom" pattern?
    - RISK_CASE_004: RU academic degrees (к.т.н./д.э.н.) → EN Ph.D./Sc.D.
      — same "dotted degree abbreviation = false authority" pattern?
    - SAFE_CASE_003: RU "г-н Иванов" → EN "Mr. Smith" — same
      abbreviation pattern?
  The examples need NOT be literal translations, but MUST demonstrate
  the identical vulnerability.
B.5. FACTUAL DATA preserved: dates, reviewer names (Kimi/Gemini/
  GPT-5.5/Qwen/Grok), patch numbers, AUTHOR_DECISION references,
  ACTUAL_TOTAL_VECTORS=11, PATCHES 5/2 verified — all unchanged.

PART C — FIND ERRORS
C.1. Any English example that FAILS to show the same threat as its
  Russian original (meaning drift in a security-relevant way)?
C.2. Any status/token accidentally translated that should have stayed
  fixed?
C.3. SOURCE_TEMPLATE and BASED_ON_RULESET correctly point to _EN
  versions? (CARD_UID and DOCUMENT_ID correctly _EN?)

PART D — DELIVERABLE
REVIEW_RESULT:
  REVIEWER: <name>
  B.1-B.5, C.1-C.3: <answers>
  TOKEN_MISMATCHES: <list>
  EXAMPLE_PATTERN_DRIFT: <any example that lost its threat pattern>
  VERDICT: APPROVE / APPROVE_WITH_FIXES / REJECT

END_OF_PACKET
