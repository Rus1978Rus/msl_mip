PRIVATE AUTHORED PROJECT / COMMERCIAL USE PROHIBITED

DOCUMENT_ID: SIGN_CORE_CARD_AT_U0040_GEN3_v0_3_EN
DOCUMENT_TYPE: SIGN_CORE_CARD

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

GUIDED_TRAVERSAL_RISK_CHECK: MANDATORY
  # Guide (from FO-100 TRAVERSAL_NOT_EQUAL_STRUCTURE): when handling a
  # reviewer's finding, always check whether it refers to STRUCTURE
  # (a verifiable fact in the file/code) or to TRAVERSAL (the reviewer's
  # interpretation / another report). Do not mistake TRAVERSAL for
  # STRUCTURE. Practice: grep / run the actual artifact BEFORE accepting
  # a finding. When reviewers disagree on a fact, resolve by primary
  # source, not majority vote. Convergence is not proof.

STATUS_PROGRESSION_TRACKER:
  WORKING_DRAFT: YES
  STRUCTURAL_PREFLIGHT_PASS: PASS (2026-07-05)
  CONVEYOR_REVIEW_PASS: WAVE_1 PASS (5/5) + WAVE_2 (2 deep-research
    fact audits + GPT finding)
  WORKINGLY_CLOSED: YES (2026-07-06, AUTHOR_DECISION)
  SIMULATION_GATE_TIER: TIER_2
  SIMULATION_GATE_PASSED: PASS (2026-07-06, first run clean; confirmed
    on live machine)
  ARTIFACT_CONFIRMED: YES (2026-07-06, AUTHOR_DECISION after
    translation-review: Gemini APPROVE + Grok APPROVE, both with
    FINDING_STATUS, coordinator-verified by grep — counts/formulas/
    tokens/mechanic/differentiator identical to RU, 0 untranslated
    Cyrillic)

============================================================
2. META
============================================================

CARD_UID: SIGN_CORE_CARD_AT_U0040_GEN3_v0_3_EN
CODEPOINT: U+0040
VISIBLE_FORM: @
UNICODE_NAME: COMMERCIAL AT
ZONE: ZONE_2
DOCUMENT_STATUS: ARTIFACT_CONFIRMED
TEMPLATE_LINE: GEN3_v0_3
SOURCE_TEMPLATE: SIGN_CORE_CARD_TEMPLATE_GEN3_v0_3_EN
AUTHOR: Ruslan Malyavsky
CREATED_AT: 2026-07-05
VERSION: v0_1
AUTHOR_DECISION_REFERENCE: AUTHOR_DECISION_20260706_AT_U0040_ARTIFACT_CONFIRMED_RU
RUN_CARD_REFERENCE: SIMULATION_ARTIFACT_AT_U0040_TIER2_v0_1_RU
RUN_CARD_STATUS: COMPLETED (TIER_2)

DISPLAY_NAME: commercial at

TRANSLATION_NOTE: This is the English translation of
  SIGN_CORE_CARD_AT_U0040_GEN3_v0_3_RU (the authoritative RU card is
  ARTIFACT_CONFIRMED). Machine tokens identical to RU; only prose and
  INPUT examples localized. AWAITING TRANSLATION_REVIEW before EN can
  reach ARTIFACT_CONFIRMED (per DOT/SKULL_CROSSBONES precedent).

TIER_1_CONTEXT: first TIER 1 sign. Class PH (phishing/social
  engineering). Priority CRITICAL. Vector: URL userinfo spoofing.

DESIGN_RATIONALE:
  @ is a structural sign (ZONE_2, context-dependent separator), not
  cultural (not ZONE_3; epoch tracker minimal). The main risk vector is
  structural: in a URL WITH AN EXPLICIT SCHEME (http://, https://),
  everything BEFORE @ is treated by the browser as userinfo (username)
  and ignored for host determination; the real host is what comes AFTER
  @. Hence phishing http://paypal.com@evil.ru → the browser goes to
  evil.ru while the human sees paypal.com. IMPORTANT (clarified by Qwen
  fact audit 2026-07-06): this userinfo mechanic is deterministic ONLY
  when a scheme is present. WITHOUT a scheme, paypal.com@evil.ru is
  parsed differently by the WHATWG parser (protocol='paypal.com:',
  evil.ru goes to path, host empty) — the host is NOT evil.ru. So the
  card's RISK cases use examples WITH a scheme, and disambiguation
  without a scheme is a contextual ambiguity (see Q1).

  Difference from the dot: the dot creates a fake DOMAIN
  (paypal.com.evil.ru), @ creates a fake USERINFO
  (paypal.com@evil.ru). Different mechanisms, both PH.

  KEY CHALLENGE: @ is highly polysemous and mostly LEGITIMATE — email
  (user@domain.com), social mention (@username), code decorator
  (@property), federated handle (@user@instance). The card MUST
  separate the dangerous context (userinfo position in a URL-like
  string) from the mass of safe ones. Default is NOT "@ = threat".

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

VISIBLE_FORM: @
LOOKS_SIMILAR_IS_NOT_SAME_SIGN: YES
RAW_SIGN_INPUT_STATUS: DATA_ONLY

BASE_MODE: DATA_ONLY
BASE_MODE_FORMULA: AT_FORM ≠ EFFECT

SIGN_CATEGORY:
  - punctuation
  - separator
  - addressing_symbol

WHAT_THIS_SIGN_IS_NOT:
  1. NOT_VERIFIED_ACCOUNT_PROOF
  2. NOT_DOMAIN_AUTHORITY
  3. NOT_HOST_IDENTITY_PROOF
  4. NOT_EMAIL_VALIDITY_PROOF
  5. NOT_MENTION_LEGITIMACY_PROOF
  6. NOT_EXECUTION_DIRECTIVE
  7. NOT_TRUST_MARKER
  8. NOT_AFFILIATION_PROOF
  9. NOT_OWNERSHIP_PROOF
  10. NOT_ROUTING_GUARANTEE

BASE_FORMULAS:
  AT_FORM ≠ VERIFIED_ACCOUNT
  AT_FORM ≠ DOMAIN_AUTHORITY
  AT_FORM ≠ HOST_IDENTITY
  AT_FORM ≠ EMAIL_VALIDITY
  AT_FORM ≠ MENTION_LEGITIMACY
  AT_FORM ≠ EXECUTION_DIRECTIVE
  AT_FORM ≠ TRUST_MARKER
  AT_FORM ≠ AFFILIATION
  AT_FORM ≠ OWNERSHIP
  AT_FORM ≠ ROUTING_GUARANTEE

============================================================
5. SEMANTIC_EPOCH_TRACKER
ZONE: ZONE_2 — CONTEXTUAL / STRUCTURAL
SEMANTIC_EPOCH_TRACKER_LOCK: REVIEWABLE
============================================================

EPOCH_TRACKER: MINIMAL (structural sign — cultural-meaning precession
  is weak; functional roles are tracked, not cultural epochs)

CAPTURE_HISTORY:
  ROLE_1:
    NAME: commercial_at_accounting
    DATE_RANGE: medieval / 16th c. — present (earliest attested
      commercial "at the rate of": Francesco Lapi letter, 1536)
    SUBSTRATE: trade accounts ("at the rate of" — per unit price)
    FUNCTION: "at the rate of" (7 widgets @ $2 = 7 widgets at $2 each)
    STATUS: ACTIVE (niche — accounting, price tags)
    EVIDENCE: Unicode name "COMMERCIAL AT"; history of trade notation

  ROLE_2:
    NAME: email_address_separator
    DATE_RANGE: 1971 (Ray Tomlinson) — present
    SUBSTRATE: email (user@host)
    FUNCTION: separator "user @ host"
    STATUS: ACTIVE (dominant function)
    EVIDENCE: ARPANET, Ray Tomlinson 1971 — chose @ as the separator
      between local part and host

  ROLE_3:
    NAME: social_mention_handle
    DATE_RANGE: @-addressing earlier (IRC), popularized by Twitter
      ~2006 (first @reply Nov 2006) — present
    SUBSTRATE: social networks (@username), federation (@user@instance)
    FUNCTION: addressing/mentioning a user
    STATUS: ACTIVE

  ROLE_4:
    NAME: code_decorator_annotation
    DATE_RANGE: ~2004-2005 (Python decorators PEP 318 / Python 2.4,
      Java annotations JSR 175) — present
    SUBSTRATE: source code (@property, @Override)
    FUNCTION: annotation/decorator
    STATUS: ACTIVE (niche — programming)

ACTIVE_EPOCH:
  CONTEXT_DEPENDENT: ROLE_2 (email) dominates, but ROLE_3 (mention) is
    massive on social networks; the role is determined by substrate
ACTIVE_EPOCH_TYPE: CONTEXT_DEPENDENT
DOMINANT_FUNCTION: email separator (globally), but context decides

PRECESSION_ALERT:
  STATUS: STABLE
  LAST_CHECK: 2026-07-05
  NOTE: @'s functional roles accumulate (accounting→email→mention→
    decorator) but do NOT displace one another — they coexist by
    substrate. Precession is structural (new roles), not cultural drama.

STACK_RULES:
  Context_gate_determines_active_role: YES
    (@ in URL userinfo position → RISK context; @ between a word and a
     domain with a dot → email; @ before a word at the start → mention;
     @ before an identifier in code → decorator)

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
    NAME: legitimate_email
    INPUT: "write to me at ivan@example.com"
    CONTEXT: ordinary email address (ROLE_2): local part @ host, where
      the host is a single domain, no userinfo
    RISK: NONE
    GUARD: AT_FORM ≠ EMAIL_VALIDITY (the sign does not prove the
      address works — but is not a threat either)

  SAFE_CASE_002:
    NAME: social_mention
    INPUT: "thanks @username for the help"
    CONTEXT: social-network mention (ROLE_3): @ before a handle, not in
      a URL context
    RISK: NONE
    GUARD: AT_FORM ≠ MENTION_LEGITIMACY

  SAFE_CASE_003:
    NAME: code_decorator
    INPUT: "@property def name(self): ..."
    CONTEXT: decorator/annotation in code (ROLE_4)
    RISK: NONE
    GUARD: AT_FORM ≠ EXECUTION_DIRECTIVE

  SAFE_CASE_004:
    NAME: commercial_pricing
    INPUT: "10 units @ $5 = $50"
    CONTEXT: commercial "at the rate of" (ROLE_1)
    RISK: NONE
    GUARD: COMMERCIAL_AT_PRICING ≠ ROUTING_GUARANTEE

  SAFE_CASE_005:
    NAME: email_in_mailto
    INPUT: "mailto:support@paypal.com"
    CONTEXT: mailto scheme — @ separates the local part and host in an
      email, NOT userinfo in an http(s) URL. Here paypal.com is the
      legitimate mail host, not a spoof victim
    RISK: NONE
    GUARD: MAILTO_AT ≠ URL_USERINFO_AT (different schemes, different
      meaning of @)

  SAFE_CASE_006:
    NAME: handle_list
    INPUT: "team: @anna @boris @vika"
    CONTEXT: list of mentions (ROLE_3), not a URL
    RISK: NONE
    GUARD: MULTIPLE_MENTION_HANDLES ≠ URL_USERINFO_CHAIN

  SAFE_CASE_007:
    NAME: federated_handle
    INPUT: "follow @user@mastodon.social"
    CONTEXT: federated handle (ActivityPub/Fediverse, ROLE_3):
      @name@instance — a legitimate format with TWO @, not a
      URL-userinfo chain. The second @ separates the user from the
      instance domain — a federation address, not a host spoof
    RISK: NONE
    GUARD: FEDERATED_HANDLE ≠ URL_USERINFO_CHAIN — the pattern
      @user@domain in a NON-URL context (no scheme, no path) is a
      federation address, not RC3 obfuscation. Differentiator: RC3
      requires a URL context (scheme/path), a federated handle is free
      text without a scheme

RISK_CASES:
  RISK_CASE_001:
    NAME: URL_USERINFO_SPOOFING
    INPUT: "log in: http://paypal.com@evil.ru/login"
    CONTEXT: @ in an http(s) URL makes everything before it userinfo
      (ignored by the browser for host determination); the real host is
      evil.ru AFTER @. The human sees "paypal.com", lands on evil.ru
    RISK: HIGH
    ATTACK: classic phishing — a familiar brand placed in the userinfo
      position to visually mask the real malicious host
    GUARD: AT_FORM ≠ HOST_IDENTITY; structurally: in a URL-like string
      the host is what follows the LAST @, not what precedes it; a brand
      in userinfo position = a mimicry signal

  RISK_CASE_002:
    NAME: USERINFO_BRAND_IN_NON_FINAL_POSITION
    INPUT: "https://secure-paypal.com@192.168.1.5/verify"
    CONTEXT: a brand-like string in userinfo + a numeric/foreign host
      after @ (including an IP address as host)
    RISK: HIGH
    ATTACK: amplification of RC1 — an IP host or unexpected domain after
      @, brand in userinfo for masking
    GUARD: AT_FORM ≠ HOST_IDENTITY; the host after @ (domain OR IP) is
      the true destination; a brand before @ does not change it

  RISK_CASE_003:
    NAME: MULTIPLE_AT_OBFUSCATION
    INPUT: "http://paypal.com@trusted.org@evil.ru/"
    CONTEXT: multiple @ — per the parsing rules of the browser (WHATWG
      URL parser) the host is determined after the LAST @; everything
      before is userinfo. The trick confuses both humans and naive
      parsers
    RISK: HIGH
    ATTACK: multiple @ mask the real host (evil.ru) behind a chain of
      trusted names in userinfo
    GUARD: AT_FORM ≠ HOST_IDENTITY; host = the segment after the LAST @;
      multiple @ in a URL string is a strong obfuscation signal

  RISK_CASE_004:
    NAME: FALSE_VERIFIED_ACCOUNT_MIMICRY (PHAGO, HYPOTHESIS)
    INPUT: "write to the official @PayPal_Support for a refund"
    CONTEXT: @ + a brand handle creates the impression of a verified
      official account that may not exist
    RISK: MEDIUM
    ATTACK: PHAGO vector — userinfo/handle implies a verified entity;
      abuse of trust in @-addressing
    GUARD: AT_FORM ≠ VERIFIED_ACCOUNT — the @ before a name confirms
      neither the existence nor the officialness of an account.
      STATUS: HYPOTHESIS (PHAGO dimension, TIER 1) — needs case
      accumulation; do not escalate as HIGH until confirmed

CONFUSABLES:
  CONFUSABLE_001:
    VISIBLE_FORM: ＠
    CODEPOINT: U+FF20
    RISK: HIGH
    NOTE: FULLWIDTH COMMERCIAL AT — visually near-identical to @, a
      different codepoint. May bypass naive filters that look only for
      U+0040. Requires normalization before analysis.

  CONFUSABLE_002:
    VISIBLE_FORM: ﹫
    CODEPOINT: U+FE6B
    RISK: MEDIUM
    NOTE: SMALL COMMERCIAL AT — a compatibility variant, a separate
      codepoint. LOOKS_SIMILAR ≠ SAME_SIGN.

ADJACENT_RISK_NOTE:
  Homoglyphs in the part BEFORE/AFTER @ (e.g. аpple.com with a Cyrillic
  а, U+0430) are NOT a confusable of @ itself but an adjacent vector
  tracked by separate cards (U+0430 etc., TIER 2). Moved out of
  CONFUSABLES to avoid mixing @'s own confusables with homoglyphs of
  its surroundings.

CONTRADICTION_GUARDS:
  CG1:
    TRIGGER: "@ before paypal.com proves this is PayPal"
    RESPONSE: AT_FORM ≠ HOST_IDENTITY
    RULE: in a URL the host is determined by what follows @, not what
      precedes it; a brand before @ is userinfo, not host

  CG2:
    TRIGGER: "@Official_Brand proves a verified account"
    RESPONSE: AT_FORM ≠ VERIFIED_ACCOUNT
    RULE: @ before a handle is addressing syntax, not confirmation of
      existence or officialness (PHAGO, hypothesis)

  CG3:
    TRIGGER: "any @ in text is suspicious"
    RESPONSE: CONTEXT_GATE_REQUIRED
    RULE: the vast majority of @ are legitimate (email, mention,
      decorator). RISK only in a URL-userinfo context. Default is NOT
      "@ = threat"

  CG4:
    TRIGGER: "@ in an email is as dangerous as @ in a URL"
    RESPONSE: EMAIL_AT ≠ URL_USERINFO_AT
    RULE: in email @ separates user and host (legitimate); in an
      http(s) URL @ introduces userinfo before the host (the spoofing
      vector). The scheme context decides

SEQUENCE_LAYER_BOUNDARY:
  SC1:
    SEQUENCE: "@ near . (a dot) in a URL"
    NAME: AT_PLUS_DOT_URL_CONTEXT
    RISK_LEVEL: context-dependent
    SCOPE: CROSS_CARD (@ U+0040 + . U+002E)
    POSSIBLE_CONTEXTS: the combination of @ and a dot in a URL
      strengthens host analysis (the domain after @ contains dots). A
      test vector for the cross-card sequence @ + DOT

RAW_SEQUENCE_TEXT_IS_NOT_SIGN_CARD_INPUT: YES
SEQUENCE_ADVISORY_ONLY: YES

============================================================
8. ADVERSARIAL_COVERAGE — RUN_CARD SEED
============================================================

CATEGORY_A: URL_USERINFO_SPOOFING (5)
  A1: "http://paypal.com@evil.ru/login" — basic userinfo-spoof (RC1)
  A2: "https://secure-paypal.com@192.168.1.5/" — brand + IP host (RC2)
  A3: "http://paypal.com@trusted.org@evil.ru/" — multiple @ (RC3)
  A4: "http://аpple.com@evil.ru" — userinfo-spoof + homoglyph in brand
  A5: "http://paypal.com%40evil.ru/" — %40 (URL-encoded @) as a bypass
    of naive filters that look for a literal @; after decoding =
    userinfo-spoof

CATEGORY_B: FALSE_VERIFIED_ACCOUNT (2)
  B1: "write to @PayPal_Support" — fake official handle (RC4)
  B2: "DM @official_bank_help" — PHAGO handle mimicry

CATEGORY_C: LEGITIMATE_CONTEXT (SAFE negatives, must NOT fire) (4)
  C1: "ivan@example.com" — ordinary email
  C2: "@property" — decorator
  C3: "thanks @username" — mention
  C4: "mailto:support@paypal.com" — mailto (email, not URL-userinfo)

CATEGORY_D: CONFUSABLE_SUBSTITUTION (2)
  D1: "paypal.com＠evil.ru" — fullwidth @ (U+FF20) instead of U+0040
  D2: "user﹫host" — small @ (U+FE6B)

ADVERSARIAL_VECTOR_COUNT: 13

============================================================
9. MUTATION_CHECK
============================================================

MUTATION_01:
  MUTATION: remove the URL context ("paypal.com@evil.ru" without http://)
  EXPECTED: still suspicious (domain@domain pattern), but weaker — could
    be an email with an unusual domain; AMBIGUITY_FLAG
  RESULT: FAIL (without an explicit URL scheme the risk is not
    automatically HIGH — correct, an email looks the same)

MUTATION_02:
  MUTATION: replace @ with a dot ("paypal.com.evil.ru")
  EXPECTED: this is already the DOT card's vector (domain mimicry), not @
  RESULT: FAIL (different signs, different cards — correct)

MUTATION_03:
  MUTATION: a single @ in a mention with no URL ("@user")
  EXPECTED: SAFE (ROLE_3)
  RESULT: FAIL (risk must not fire — correct)

MUTATION_04:
  MUTATION: fullwidth ＠ (U+FF20) in a URL-spoof
  EXPECTED: caught after normalization as an equivalent of @; without
    normalization — a bypass (CONFUSABLE_001)
  RESULT: FAIL (requires normalization — documented)

MUTATION_05:
  MUTATION: email with a subdomain (user@mail.paypal.com)
  EXPECTED: SAFE — a legitimate email, host mail.paypal.com
  RESULT: FAIL (must not fire — correct)

MUTATION_06:
  MUTATION: a decorator with an argument (@app.route("/"))
  EXPECTED: SAFE (ROLE_4, code)
  RESULT: FAIL (does not fire — correct)

MUTATION_07:
  MUTATION: a federated handle @user@mastodon.social with no URL scheme
  EXPECTED: SAFE (a federation address, ROLE_3) — NOT RC3, since there
    is no URL context (scheme/path)
  RESULT: FAIL (must not fire as multiple-@ obfuscation — the
    differentiator is that RC3 requires a URL context)

MUTATION_COUNT: 7

============================================================
10. KNOWN_OPEN_QUESTIONS
============================================================

BLOCKS_WORKINGLY_CLOSED: NO (monitoring items / delegated to the
  integrator)

Q1:
  QUESTION: How to reliably distinguish "paypal.com@evil.ru" (URL-spoof)
    from a legitimate email with an unusual domain without an explicit
    http scheme?
  STATUS: OPEN (confirmed as structurally undecidable — Qwen fact audit
    2026-07-06 against RFC 3986 + WHATWG URL Standard)
  NOTE: without a scheme it is a contextual ambiguity, FUNDAMENTAL not
    temporary. The fact audit confirmed by primary sources: neither RFC
    3986 nor WHATWG treats an email as a form of URL; a string without a
    scheme is either an invalid URI (RFC 3986) or a URL object with an
    invalid scheme (WHATWG) — but NEVER an email. There is no structural
    differentiator without a scheme. WITH a scheme (http/https/mailto)
    it is deterministic (the scheme is the semantic key). The heuristic
    (domain-with-TLD in userinfo + domain-with-TLD after @) remains for
    the matcher/integrator as a PROBABILISTIC signal, not a structural
    rule.

Q2:
  QUESTION: RC4 (fake verified account) — MEDIUM or higher?
  STATUS: OPEN
  NOTE: PHAGO vector, HYPOTHESIS. Data is scarce. Kept at MEDIUM until
    cases accumulate.

Q3:
  QUESTION: Is mandatory Unicode normalization (@/＠/﹫) needed at
    runtime input for all signs, not just @?
  STATUS: OPEN
  NOTE: intersects with future invisible signs (U+FE0F, U+200D) — a
    general input-normalization question. Delegated to the runtime level.

============================================================
11. PATCH_HISTORY
============================================================

PATCH_01:
  DATE: 2026-07-05
  CHANGE: card @ built from scratch to the GEN3_v0_3 standard (first
    TIER 1 sign). ZONE_2, 10 BASE_FORMULAS, 6 SAFE, 4 RISK, 3
    CONFUSABLES, 4 CG, 12 ADVERSARIAL, 6 MUTATION. GUIDED_TRAVERSAL_RISK
    guide inherited from template.
  VERIFIED_BY: STRUCTURAL_PREFLIGHT PASS + conveyor wave 1

PATCH_02:
  DATE: 2026-07-05
  CHANGE: conveyor wave-1 fixes (GPT-5.5 APPROVE_WITH_FIXES, all
    findings FINDING_STATUS=VERIFIED, grep-checked): (1) filled 2 empty
    GUARDs (SAFE_004 pricing, SAFE_006 handle list); (2) RC3 "per spec"
    → "per the URL parsing rules of the browser (WHATWG URL parser)";
    (3) CONFUSABLE_003 homoglyph moved out of CONFUSABLES into
    ADJACENT_RISK_NOTE; (4) added ADVERSARIAL A5 (%40 URL-encoded @) →
    count 12→13; (5) role dates refined; (6) TIER 1 (sign priority) vs
    TIER_2 (simulation tier) clarified.
  VERIFIED_BY: coordinator (grep of each fix)

PATCH_03:
  DATE: 2026-07-06
  CHANGE: clarifications from the Qwen fact audit (deep research, wave
    2). (1) DESIGN_RATIONALE: the userinfo mechanic "host after @" is
    deterministic ONLY with a URL scheme; without a scheme WHATWG parses
    differently (host empty). RISK cases use scheme examples — remain
    correct. (2) Q1 reinforced by primary sources (RFC 3986 + WHATWG):
    structurally distinguishing phishing-URL vs email without a scheme
    is FUNDAMENTALLY undecidable.
  FACT_AUDIT: Qwen/Alibaba (Q1, mechanics), Copilot (7/7 B.1-B.7:
    Tomlinson 1971, PEP 318, JSR 175, @-reply 2006, Lapi 1536, U+FF20/
    U+FE6B, %40 RFC 3986). Cross-review Qwen↔Copilot on B.1 resolved by
    primary source (both correct for different cases — the difference is
    scheme presence). 0 confabulations.
  VERIFIED_BY: coordinator (source cross-check)

PATCH_04:
  DATE: 2026-07-06
  CHANGE: added SAFE_CASE_007 (federated handle @user@mastodon.social,
    ActivityPub/Fediverse) + MUTATION_07 — closing a real gap: a
    legitimate two-@ format could falsely fire as RC3 (multiple @). The
    differentiator: RC3 requires a URL context (scheme/path), a
    federated handle is free text.
  SOURCE: the single VERIFIED finding from GPT's deep-research
    meta-audit (its other recommendations REJECTED as already done in
    PATCH_02, or UNVERIFIABLE as out of the @ fact-audit scope).
  VERIFIED_BY: coordinator (grep: federated handle was absent)

PATCHES_APPLIED: 4
PATCHES_VERIFIED: 3/4

MATCHER_NOTE: the executable matcher
  (single_sign/matchers/at_matcher.py) was implemented after
  WORKINGLY_CLOSED and passed SIMULATION_GATE TIER_2 (first run clean:
  RISK only in a URL context with scheme; the federated-handle vs
  URL-multiple-@ differentiator works by scheme presence; no false
  positives on legitimate @). Card and matcher are aligned.

============================================================
12. LIMITATION_STATEMENT
============================================================

WORKINGLY_CLOSED ≠ ARTIFACT_CONFIRMED.
REVIEW ≠ VALIDATION.

The card @ was built from scratch and completed the full
CONVEYOR_DISCIPLINE: STRUCTURAL_PREFLIGHT, independent review (wave 1
5/5, wave 2 two deep-research fact audits + a GPT finding),
WORKINGLY_CLOSED, SIMULATION_GATE TIER_2 (first run clean, confirmed on
live machine). ARTIFACT_CONFIRMED status assigned by AUTHOR_DECISION
2026-07-06.

Main substantive limitation: @ is highly polysemous, and reliably
separating URL-userinfo-spoofing from legitimate contexts (email,
mention, decorator, federated handle) without an explicit URL scheme is
contextual, not purely structural (see Q1). This is a deliberate
limitation: the card prefers NOT to over-catch the mass of legitimate
@, escalating only a clear URL-userinfo pattern with a scheme. The
PHAGO vector (RC4) is a HYPOTHESIS, not confirmed.

============================================================
13. INTEGRATION_INTERFACE_STATUS
============================================================

MODULE_INTERFACE: READY (ZONE_2 routing)
INTEGRATOR_INTERFACE: READY (risk → action mapping via runtime policy)
SEQUENCE_INTERFACE: READY (SC1 cross-card @ + DOT)
MATCHER_REFERENCE: single_sign/matchers/at_matcher.py
MATCHER_STATUS: IMPLEMENTED (SIMULATION_GATE TIER_2 PASS, first run
  clean 9/9 + mutations + adversarial C with no false positives)
NORMALIZATION_NOTE: Unicode normalization of @/＠/﹫ is required before
  analysis (see CONFUSABLES, Q3)
RUNTIME_STATUS: ARTIFACT_CONFIRMED

END_OF_DOCUMENT
