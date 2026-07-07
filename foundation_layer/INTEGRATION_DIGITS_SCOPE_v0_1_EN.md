════════════════════════════════════════════════════════════════════
CONVEYOR INTEGRATION — DIGIT SIGNS SCOPE
Packet: DIGITS_SCOPE_DESIGN_REVIEW_v0_1 | Date: 2026-07-07
Reviewers: 7 | Type: DESIGN_DECISION_REVIEW
Status: prepared for AUTHOR_DECISION (final call is Ruslan's)
════════════════════════════════════════════════════════════════════

──────────────────────────────────────────────────────────────────
1. VERDICT SUMMARY
──────────────────────────────────────────────────────────────────
Reviewer         VERDICT     CONFIDENCE
R1 (GPT?)        OPTION_B     HIGH
R2 Kimi K2.6     OPTION_B     HIGH
R3 (Gemini?)     OPTION_B     HIGH
R4 (Unicode-ref) OPTION_B     HIGH
R5 (Grok?)       OPTION_B     HIGH
R6 (Claude?)     OPTION_B     HIGH
R7 (GPT-o?)      OPTION_B     HIGH

RESULT: 7/7 OPTION_B, 7/7 HIGH. UNANIMOUS.
None chose A (full cards) or C (digits out of scope).

──────────────────────────────────────────────────────────────────
2. PA2 CRITIQUES VERIFIED AGAINST CODE (VERIFY_BEFORE_TRUST)
──────────────────────────────────────────────────────────────────
Unanimity does not cancel verification. Two reviewers attacked PA2 —
checked by directly reading sequence_engine.py.

CRITIQUE-1 (R5): "a character enters sequence ONLY via a card; without
  a stub the digit is dropped at scan_signs."
  CHECK: _find_literal_matches, rule (b): "among the candidate's
  characters there must be at least ONE sign from CARD_SET." A candidate
  of pure digits with no digit card will NOT match.
  STATUS: VERIFIED. PA2 "no else-branch needed, architecture ready to
  accept" is INACCURATE. Digit stub cards are MANDATORY as the entry
  into sequence. Independently noted by R6, R7.

CRITIQUE-2 (R3): "01 ≠ // : the engine searches LITERAL strings
  (str.find), while 01 is a CLASS (0 + any digit)."
  CHECK: function _find_literal_matches, internally str.find — exact
  substrings. "//" is a fixed string; a leading zero is a class-pattern.
  STATUS: VERIFIED. The current engine will NOT catch a class without
  matching-logic rework. PA2 underestimated implementation cost of B.

PA2 CONCLUSION: verdict B held, BUT my PA2 was partially refuted by
code. Implementing B is costlier than I wrote: (1) digit stub cards
needed, (2) matching must be reworked for classes, not only literals.
The conveyor worked — it caught what the author-analysis missed.

──────────────────────────────────────────────────────────────────
3. BOUNDARY_DEFINITION CONVERGENCE (the run's main value)
──────────────────────────────────────────────────────────────────
All 7 converged on ONE criterion, in different words:

  DIGIT = DATA (risk NONE) BY DEFAULT.
  DIGIT = SIGN ⟺ it participates in a DECLARED structural sequence
  pattern that changes interpretation/routing (IP octet, leading zero
  in a known field, version), with a DOCUMENTED risk (not derived
  on the fly).

Checkable test (R2, clearest):
  "Is the digit part of a documented SC-pattern?"
    YES → analyze as sign (sequence layer)
    NO  → data (risk NONE)

Formula (R4): DIGIT_ALONE ≠ STRUCTURAL_RISK ;
              NUMERIC_VALUE ≠ SIGN_EFFECT ;
              DIGIT_SEQUENCE + DECLARED_CONTEXT → ANALYZABLE_PATTERN

──────────────────────────────────────────────────────────────────
4. MAIN RISK OF OPTION B (named by 5 of 7 independently)
──────────────────────────────────────────────────────────────────
SEQUENCE_BLOAT / DRIFT TOWARD OPTION A: over time more and more digit
sequence rules accumulate, the boundary blurs, and the system de facto
slides into semantic evaluation of numbers (the very thing A fears).

MITIGATIONS (collected from reviewers):
- R1: a digit sequence rule is added ONLY on a proven structural effect
  (as with ://). Discipline, not a list.
- R6: a strict DIGIT-card template with fixed risk=NONE, RISK_CASES
  FORBIDDEN, explicit note "stub for the sequence layer, does not
  evaluate the number's semantics."
- R2: context-specific rules (version_pattern vs id_pattern) with
  different risk, so "01 in a version" ≠ "01 in an ID."

──────────────────────────────────────────────────────────────────
5. UNANIMOUS MISSED_CONSIDERATION: NON-ASCII UNICODE Nd
──────────────────────────────────────────────────────────────────
All 7 raised the same: digits are not limited to ASCII 0-9.
- Arabic-Indic ٠١٢ (U+0660-0669), Eastern ۰۱۲ (U+06F0-06F9)
- Fullwidth ０１ (U+FF10-FF19)
- Roman Ⅳ (U+2160+), circled ① (U+2460+), Devanagari, etc.
- The whole Unicode Nd class is wider than ASCII 0-9.

Attack vector: fullwidth/homoglyph digits bypass structural checks
(paypa1.com with fullwidth 1; ０１ normalizes to 01).

REVIEWER CONSENSUS: this is NOT a job for digit cards but for an
ADJACENT layer — confusables/NFKC normalization. And this is THE SAME
layer discussed in the INVISIBLE packet (uncarded/confusables, noise
criterion with NFKC ∪ skeleton UTS#39). Two runs converged on one
layer — a strong signal the uncarded/normalization layer is real and
needed by both.

──────────────────────────────────────────────────────────────────
6. CONSOLIDATED ONE_QUESTION_TO_AUTHOR (6 of 7 — one question)
──────────────────────────────────────────────────────────────────
Q-MAIN (R2, R4, R5, R7, partly R6): what is the FIRST concrete digit
  sequence rule you declare? The answer determines:
  - a concrete rule exists (IP octet / leading zero / version)
    → Option B is READY to implement;
  - no concrete rule → B needs a research phase, and temporarily it is
    safer NOT to touch digits (soft C until a rule appears).

Q-SECOND (R2, R4, R5, R6, R7): ASCII 0-9 or the whole Unicode Nd?
  - ASCII only → 10 stub cards, Nd into a separate layer;
  - whole Nd → either hundreds of stubs, or mandatory NFKC
    normalization at input BEFORE single-sign (Nd→ASCII mapping).

──────────────────────────────────────────────────────────────────
7. WHAT REQUIRES AUTHOR_DECISION (nothing assigned automatically)
──────────────────────────────────────────────────────────────────
D1. Accept OPTION_B as the digit policy? (7/7 for, status is yours)
D2. PA3 "digit = data by default": R2 and R6 propose reclassifying
    HYPOTHESIS→VERIFIED (for a structural analyzer this is definitional).
    Agree?
D3. Q-MAIN: name the first sequence rule OR acknowledge there is none
    yet → then fix B-as-policy + freeze implementation until a rule
    appears (soft C in time).
D4. Q-SECOND: ASCII-only now, Nd into the confusables/normalization
    layer (reviewers' advice) — confirm?
D5. SEQUENCE_BLOAT mitigation: accept the rule "a digit sequence rule
    only on a PROVEN structural effect" + a strict DIGIT template
    forbidding RISK_CASES?

──────────────────────────────────────────────────────────────────
8. CLAUDE'S RECOMMENDATION (OPINION, not a decision)
──────────────────────────────────────────────────────────────────
- D1: yes, B. Unanimous + held under code verification.
- D2: yes, VERIFIED — for a structural analyzer it is by definition;
  R2/R6 are right.
- D3: you have NO proven digit sequence rule yet. The honest
  anti-overclaim move: fix B AS POLICY now, but freeze implementation
  until the first proven rule (candidate #1 — IP octet with leading
  zero, 0177.0.0.1 octal bypass, has a documented CVE class). Do not
  breed stubs for non-existent rules.
- D4: ASCII-only, Nd into the shared normalization/confusables layer —
  the same one that surfaced in the invisible packet. Don't duplicate.
- D5: yes, both mitigations. Especially the strict template forbidding
  RISK_CASES — direct protection against FALSE_EFFECT at the entry.

MAIN STRUCTURAL CONCLUSION OF BOTH RUNS: both invisible and digits hit
ONE missing layer — normalization/confusables/uncarded. This is not two
decisions but one layer needed by two branches. Perhaps THAT is the real
next module, not VS16 or digits separately.
════════════════════════════════════════════════════════════════════
