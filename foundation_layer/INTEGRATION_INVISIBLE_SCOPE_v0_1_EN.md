════════════════════════════════════════════════════════════════════
CONVEYOR INTEGRATION — INVISIBLE SIGNS SCOPE
Packet: INVISIBLE_SIGNS_SCOPE_DESIGN_REVIEW_v0_1 | Date: 2026-07-07
Reviewers: 6 | Type: DESIGN_DECISION_REVIEW
Status: prepared for AUTHOR_DECISION (final call is Ruslan's)
════════════════════════════════════════════════════════════════════

──────────────────────────────────────────────────────────────────
1. VERDICT SUMMARY
──────────────────────────────────────────────────────────────────
Reviewer           VERDICT      CONFIDENCE
R1                 OPTION_2      HIGH
R2                 OPTION_2      HIGH
R3                 OPTION_2      HIGH
R4                 OPTION_2      HIGH
R5 (Grok?)         OPTION_2      HIGH
R6 (Gemini?)       OPTION_2      HIGH

RESULT: 6/6 OPTION_2, 6/6 HIGH. UNANIMOUS.
None chose 1 (separate project) or 3 (pause).
Matches the digits run pattern (7/7 narrow option).

──────────────────────────────────────────────────────────────────
2. CORE AGREEMENT (why narrow, not a project)
──────────────────────────────────────────────────────────────────
- TOPOLOGY (VERIFIED, checked against code earlier): the set of
  "unknown" = the logical complement of the card registry. Uncarded is
  defined ONLY relative to MSL/MIP. A separate project = either a
  duplicate registry or hard version sync = a cycle.
- RESOURCE (VERIFIED): one operator, 6+ entities. A new repo now
  scatters focus.
- HOT CONTEXT (VERIFIED): 3 review rounds, noise criterion checked
  (0 flags), simulation ~90%. A pause devalues the invested context.
- PRECEDENT (VERIFIED): AI Conveyor Workbench — "register as a value,
  return later" — worked without loss.

──────────────────────────────────────────────────────────────────
3. MAIN UNANIMOUS RISK: "STUB FOREVER"
──────────────────────────────────────────────────────────────────
Nearly all 6 named one thing: a MODULE_CANDIDATE in the backlog risks
never returning → the backlog becomes a graveyard, the system stays
blind to VISIBLE homoglyphs and bidi attacks (having closed only the
invisible ones).

KEY MITIGATION (R5, strongest): an EXPLICIT RETURN TRIGGER is needed.
Without a trigger, registration = a delayed failure. Trigger candidates
from reviewers:
  - "return upon reaching N MSL/MIP cards" (e.g. 10);
  - "return upon the first invisible prompt injection incident";
  - "return upon the appearance of a second operator";
  - "return when INTEGRITY_WITNESS is formalized."

──────────────────────────────────────────────────────────────────
4. PRIOR_ANALYSIS CRITIQUES (what review corrected in Claude)
──────────────────────────────────────────────────────────────────
PA1 "uncarded cannot live alone" — PARTIALLY refuted (R1, R2, R4, R6):
  true UNDER current resource conditions, but NOT absolute. Redefined
  BROADER — "Unicode text hygiene / input-integrity analyzer" — a
  separate project is possible. That is a different scope, not an
  "else-branch." Soften wording: not "impossible" but "premature as a
  first step."

PA5 "uncarded MERGES with INTEGRITY_WITNESS" — refuted as overstated
  (R5 explicitly, R2 partly): this is HYPOTHESIS, not VERIFIED. They
  COMPLEMENT each other at DIFFERENT levels:
    uncarded = passport of an unknown symbol (flag-only, no risk);
    INTEGRITY_WITNESS = context-hijack detector (active canary).
  A merge is POSSIBLE, but it is a separate arch decision, not a given.
  PA5 closed it prematurely. IMPORTANT: this changes the registration
  wording — link, but do NOT equate.

PA5 "Trojan Source / IDN closed" — soften (R2): not CLOSED but
  LOWER_DIFFERENTIATION (more mature, less unique to the project).

PA6 "a bare scanner is not new" — true, but incomplete (R5): it omits
  the key point — the DISCIPLINE is defensible (passport without risk,
  REVIEW ≠ VALIDATION, versioned sources), which prior art LACKS.

──────────────────────────────────────────────────────────────────
5. NEW STRONG QUESTION (not in the options): OPERATIONAL DEBT
──────────────────────────────────────────────────────────────────
R5 raised what neither Claude nor the other options saw —
and it can change the verdict:

  Is the author willing to take on OPERATIONAL MAINTENANCE of versioned
  Unicode sources (DerivedCoreProperties.txt, UTS#39 skeleton,
  confusables) for the WHOLE lifecycle — updating on every major Unicode
  release + validating the noise criterion on a MULTILINGUAL corpus?

  IF YES → OPTION_2 is sustainable.
  IF NO  → OPTION_2 = a delayed failure, and OPTION_3 WITH AN EXPLICIT
           TRIGGER is wiser (pause until the resource appears).

NOTE (2026-07-07): this debt was PARTIALLY CLOSED in-session by the
tool tools/unicode_sources_update.py (fetch + version pinning +
fallback guard). The mechanical part of R5's objection is addressed;
the corpus-validation part remains manual.

Adjacent (R5): the noise criterion R4 was checked on "ordinary text,"
but what is "ordinary" for 4000 DI codepoints? A representative
multilingual corpus is needed (Arabic, Hebrew, CJK — where bidi/
script-mixing are LEGITIMATE). Sourcing it is a resource question that
can block final validation.

──────────────────────────────────────────────────────────────────
6. STUB OUTPUT CONTRACT (R2, R4 — even a stub needs a schema)
──────────────────────────────────────────────────────────────────
UNCARDED_CLASSIFICATION, even unimplemented, must declare a format:
  codepoint, name, category, bidi, script, DICP (Default_Ignorable),
  NFKC_delta, skeleton_hit, risk_assigned: NO
+ explicit line: "this layer is NOT a sanitizer, it makes a PASSPORT,
  it does not clean."
+ Unicode version pinning (pin the UCD/UTS#39 version).

──────────────────────────────────────────────────────────────────
7. ONE_QUESTION SUMMARY (what reviewers want from the author)
──────────────────────────────────────────────────────────────────
Q1 (R5, strongest): will you take on operational maintenance of Unicode
   sources? — determines OPTION_2 vs OPTION_3 sustainability.
Q2 (R1, R3): what TRIGGER moves the stub into an active component?
Q3 (R2): fix UNCARDED_TEXT_INTEGRITY_LAYER as a separate MODULE_CANDIDATE
   WITHOUT code right now — yes?
Q4 (R6): will future INTEGRITY_WITNESS import MSL/MIP as a code
   dependency, or integrate via serialized logs/reports?

──────────────────────────────────────────────────────────────────
8. WHAT REQUIRES AUTHOR_DECISION
──────────────────────────────────────────────────────────────────
D1. Accept OPTION_2 as the scope decision? (6/6 for, status is yours)
D2. Q1 — Unicode-source operational debt: take it on OR OPTION_2 turns
    into OPTION_3 with a trigger? (NOTE: mechanical part addressed by
    the in-session tool)
D3. Q2 — name an explicit RETURN TRIGGER (so the backlog is not a
    graveyard). My advice: "first invisible injection incident OR
    formalization of INTEGRITY_WITNESS, whichever comes first."
D4. Registration: link uncarded to INTEGRITY_WITNESS but do NOT equate
    (PA5 correction). MODULE_CANDIDATE wording.
D5. Stub output contract + Unicode version pinning — fix?

──────────────────────────────────────────────────────────────────
9. CLAUDE'S RECOMMENDATION (OPINION, not a decision)
──────────────────────────────────────────────────────────────────
- D1: yes, OPTION_2. Unanimous + topology VERIFIED against code.
- D2: this WAS the session's main question; now partly resolved by the
  in-session source-update tool. Corpus validation remains manual — if
  you are not ready to hold THAT, R5's caution partly stands, but the
  mechanical debt is closed.
- D3: definitely name a trigger. Without it D1 is meaningless.
- D4: important to accept the PA5 correction. My earlier analysis
  equated uncarded and INTEGRITY_WITNESS — review showed they are
  different levels. Link by address, do not merge.
- D5: yes.

──────────────────────────────────────────────────────────────────
10. LINK OF THE TWO RUNS (invisible + digits)
──────────────────────────────────────────────────────────────────
Both runs (7/7 digits, 6/6 invisible) converged on the NARROW option
AND on ONE shared missing layer: normalization / confusables / Unicode
sources. Digits sent Nd-outside-ASCII there; invisible sent visible
homoglyphs/bidi there; both need Unicode source version pinning; both
hit one operational debt (R5).

STRUCTURAL CONCLUSION: the real next module is probably NOT VS16 and NOT
digits separately, but the SHARED Unicode-normalization/confusables layer
+ a decision on operationally maintaining its sources. That is the root
both branches hit. Perhaps it should go to AUTHOR_DECISION first — before
individual signs.
════════════════════════════════════════════════════════════════════
