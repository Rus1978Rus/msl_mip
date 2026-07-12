PRIVATE AUTHORED PROJECT / COMMERCIAL USE PROHIBITED

DOCUMENT_ID: CONVEYOR_RUN_PACKET_TEMPLATE_v0_1_EN
DOCUMENT_TYPE: CONVEYOR_RUN_PACKET_TEMPLATE
TEMPLATE_LINE: GEN3_v0_3
DOCUMENT_STATUS: WORKINGLY_CLOSED
STATUS: WORKINGLY_CLOSED / NOT_LOCKED / NOT_RUNTIME / NOT_VALIDATOR / NOT_PRODUCTION
AUTHOR_DECISION_REFERENCE: AUTHOR_DECISION_20260621_003_CONVEYOR_RUN_PACKET_TEMPLATE_v0_1_WORKINGLY_CLOSED_RU
AUTHOR: Ruslan Malyavsky
CREATED_AT: 2026-06-21
REVISION_NOTE_20260712: FINDING_STATUS/FINDING_BASIS raised from Part C
  (FINDING_STATUS_RULE) into section 0 as RULE_REMINDER:
  PER_FINDING_STATUS_AND_BASIS_MANDATORY — mandatory for ANY packet, not
  only in the deliverable format. Reason — the 2026-07-12 round (narrow
  circle on _domain_prefix): one reviewer passed a guess off as
  verification, another reviewed non-existent code for the second round
  running; both are caught by the section-0 BASIS requirement. Machinery
  source — ACK_GAP_TRIVALENT_v0_2.

TRANSLATION_NOTE: This is the English translation of
  CONVEYOR_RUN_PACKET_TEMPLATE_v0_1_RU. The Russian version remains
  authoritative. Field names, status tokens, rule IDs, and
  machine-readable values are kept identical to the Russian version —
  only human-facing prose is translated.

============================================================
HOW TO USE THIS TEMPLATE
============================================================

This is a FORM for creating a conveyor packet — a document sent to
external reviewer models to organize one round of review. It fits the
three round types found in the project's practice:

  TYPE_1: REVIEW — review of a text document (rules, template,
    specification) against quality/traceability criteria
  TYPE_2: SIMULATION — end-to-end pipeline execution (sign card →
    MODULE_TEMPLATE → INTEGRATOR_TEMPLATE → result)
  TYPE_3: AUDIT — comparative check of several artifacts against each
    other (e.g. structural cross-check of cards)

Choose the appropriate type at the start of filling — this determines
which blocks from B.1–B.9 (the TASK section) you need and which can be
removed as irrelevant.

Every field in angle brackets <...> is filled with the specifics of
the current round.

============================================================
0. MANDATORY RULES IN EFFECT FOR ANY PACKET
============================================================

These rules are established from previous project rounds.
ISOLATED_PACKET_DELIVERY_MANDATORY and VERIFY_BEFORE_TRUST_MANDATORY
are mandatory for every packet without exception.
AUTHOR_DECISION_STATUS_AUTHORITY applies to any packet where a
reviewer formulates a verdict or a status conclusion (that is, almost
always). DIFFERENTIATION_CHECK_MANDATORY is added only if applicable
(SIMULATION rounds with several test cases).

RULE_REMINDER: ISOLATED_PACKET_DELIVERY_MANDATORY
  This packet must be delivered to the reviewing model as an ISOLATED
  FILE, not as part of a conversation history. Evaluate only the
  contents of the packet itself and the attached files; do not draw
  conclusions from earlier messages about other tasks.

RULE_REMINDER: VERIFY_BEFORE_TRUST_MANDATORY
  If you refer to the contents of other project documents (sign cards,
  rules, templates) in your review — verify this directly against the
  attached files, not from memory and not from someone else's
  retelling. The formal act of "refining" does not automatically make
  the second statement more reliable without independent checking
  against the primary source.

[ADD IF APPLICABLE]
RULE_REMINDER: DIFFERENTIATION_CHECK_MANDATORY
  If one sign/element is tested in N different contexts AND the result
  is identical in all N contexts THEN automatically ARCHITECTURE_BUG —
  this finding cannot be downgraded at the discretion of an individual
  reviewer. (Apply for SIMULATION-type rounds with several test cases.)

RULE_REMINDER: AUTHOR_DECISION_STATUS_AUTHORITY
  A reviewer's verdict ≠ the project's final status. Any statement of
  WORKINGLY_CLOSED / ARTIFACT_CONFIRMED / READY_FOR_USE is a
  recommendation, not a fact, until explicitly accepted through
  AUTHOR_DECISION by the coordinating party (the project author). This
  rule applies to EVERY reviewer, including one who is formally the
  "MASTER-ORCHESTRATOR" or session coordinator — such a role does not
  grant authority to assign final status. Found across three project
  rounds where this rule was violated as part of a reminder for the
  coordinator; raised to a formal section-0 rule following external
  review (GPT-5.5, Copilot).

RULE_REMINDER: PER_FINDING_STATUS_AND_BASIS_MANDATORY
  For EVERY finding by any reviewer, two fields are mandatory:
    FINDING_STATUS: VERIFIED | REJECTED | UNVERIFIABLE
    FINDING_BASIS:  what it rests on — a code trace with the EXACT input
                    and the EXACT line/branch, OR a direct quote from the
                    packet with a locator, OR an honest "could not verify".
  A verdict without BASIS is NOT accepted for arbitration. An assertion is
  not a proof. UNVERIFIABLE is a legitimate answer; a guess dressed as
  verification is not. A bare "VERIFIED"/"checked"/"obvious" without
  METHOD+TARGET+OBSERVED = no FINDING_STATUS (a decorative field). The full
  machinery (trivalence, BASIS_MINIMUM, the elision ban
  UNVERIFIABLE→VERIFIED and the guillotine ban UNVERIFIABLE→REJECTED,
  FINDING_STATUS≠ISSUE_SEVERITY, UNIVERSAL_SCOPE) lives in Part C,
  FINDING_STATUS_RULE; it is raised here into section 0 so it binds ANY
  packet from the moment the task is posed, not only in the deliverable
  format. Found in the 2026-07-12 round (narrow circle on _domain_prefix):
  one live reviewer wrote "Devanagari → HOST ✅" without checking (took a
  bare base letter without its vowel sign; a real Devanagari IDN carries a
  combining mark — DEVANAGARI VOWEL SIGN AA, U+093E, isalnum()=False — on
  which the positive scan halts: a guess passed off as verification);
  another voice reviewed non-existent code for the second round running.
  Both are caught by the single BASIS requirement.
  SOURCE: ACK_GAP_TRIVALENT_v0_2 (AUTHOR_DECISION 2026-07-05).

============================================================
DOCUMENT_ID: CONVEYOR_RUN_PACKET_<SHORT_ROUND_NAME>
VERSION: v0_1
DATE: <YYYY-MM-DD>
STATUS: ACTIVE_PACKET
PROJECT: MSL/MIP — Malyavsky Syntax Language / Malyavsky Invariant Protocol
PACKET_TYPE: <REVIEW / SIMULATION / AUDIT>
PACKET_SUBTYPE: <RULESET_REVIEW / TEMPLATE_REVIEW /
  FILLED_CARD_PREFLIGHT_REVIEW / CROSS_ARTIFACT_SCHEMA_AUDIT /
  TIER_1_SIMULATION_GATE / TIER_2_SIMULATION_GATE /
  TIER_3_SIMULATION_GATE / OTHER>

NOTE_ON_PACKET_SUBTYPE: refines the specific scenario within
  PACKET_TYPE without needing to introduce a new top-level
  PACKET_TYPE for each new scenario. For example, "check a filled card
  before STRUCTURAL_PREFLIGHT_PASS" is PACKET_TYPE: REVIEW,
  PACKET_SUBTYPE: FILLED_CARD_PREFLIGHT_REVIEW, not a separate type.
  Added following external review (GPT-5.5); format refined (placeholder
  separated from explanation) following a repeat review (GPT-5.5).

[FILL IF THIS IS A REPEAT ROUND AFTER A PREVIOUS ONE]
PREVIOUS_RUN_REFERENCE: <ID of the previous packet in this same series>
PREVIOUS_RUN_RESULT: <CONFIRMED_PASS / ACCEPT_WITH_PATCHES / REJECTED>
PATCHES_APPLIED_FROM_PREVIOUS_RUN: <list>

============================================================
PART A — REQUIRED MATERIALS
============================================================

REQUIRED_FILES:
  1. <file name>
     ROLE: <TARGET_DOCUMENT / SOURCE_OF_TRUTH / SOURCE_CARD etc.>
     STATUS_EXPECTED: <expected document status>
  [repeat for each required file]

OPTIONAL_FOR_CONTEXT:
  <files not strictly required, but useful for completeness of
  understanding — e.g. old versions for comparison>

NOT_REQUIRED_FOR_THIS_RUN:
  <explicitly exclude documents that may seem relevant but are not
  needed in this round — saves the reviewer's time and reduces the
  risk that they audit something other than what was asked>

============================================================
PART B — TASK FOR THE CONVEYOR
============================================================

TARGET: <one sentence stating the goal of this round>

REQUIRED_REVIEWERS: 3 (minimum)
MINIMUM_REVIEWER_FAMILIES: 3

------------------------------------------------------------
B.0 WHAT IS NEW / WHAT CHANGED SINCE THE LAST ROUND
[delete this block if the round is the first]
------------------------------------------------------------

<context: what was checked before, what was added in this round, why
exactly this needs to be tested now>

------------------------------------------------------------
FOR PACKETS OF TYPE REVIEW / AUDIT — USE THIS STRUCTURE:
------------------------------------------------------------

B.1 WHAT IS BEING CHECKED
  <description of the target document and what it is checked against —
  e.g. "against the requirements of SIGN_CORE_CARD_CONVEYOR_RULES">

B.2 QUESTIONS / CHECKS FOR EACH REVIEWER
  Q1. <a specific, verifiable question — not a general one ("is the
      document good?"), but a specific one ("is field X present in
      section Y, and does it match the rules' requirement?")>
  Q2. <next question>
  [continue as needed — for traceability checks use line-by-line
  tables "rule field → document field → status", not general
  impressions]

B.3 PRACTICAL APPLICABILITY CHECK
  [for AUDIT/REVIEW of templates and rules — ask the reviewer to try,
  mentally or in writing, to apply the document to a specific test
  case, to catch non-obvious problems not visible in a purely
  mechanical check]

PRINCIPLE_NOTE (for filled sign cards specifically):
  Checking a filled card against the template/rules
  (PACKET_TYPE: REVIEW, PACKET_SUBTYPE: FILLED_CARD_PREFLIGHT_REVIEW)
  and end-to-end simulation through MODULE_TEMPLATE/INTEGRATOR_TEMPLATE
  (PACKET_TYPE: SIMULATION, PACKET_SUBTYPE: TIER_N_SIMULATION_GATE)
  are TWO DIFFERENT PACKETS, not one hybrid. This is a direct
  consequence of the fact that in
  SIGN_CORE_CARD_CONVEYOR_RULES_GEN3_v0_3_RU the
  STRUCTURAL_PREFLIGHT_PASS/CONVEYOR_REVIEW_PASS and
  SIMULATION_GATE_PASSED are different, sequential stages of the card
  lifecycle (rules section 1). Mixing them in one packet masks the
  fact that one stage (the mechanical/textual check) must finish and
  give a result BEFORE the other begins (the substantive pipeline
  run). The decision was made following an external review with
  diverging opinions (GPT-5.5 and Copilot proposed two packets; Grok
  and one of the GPT-5.5 runs proposed a hybrid) — separation was
  chosen, as it accurately reflects the architecture of the v0_3 rules.

------------------------------------------------------------
FOR PACKETS OF TYPE SIMULATION — USE THIS STRUCTURE:
------------------------------------------------------------

B.1 SIMULATION STATUS
  SIMULATION_ID: <unique identifier>
  SIMULATION_STATUS: DEMO / TRACE_RUN / NOT_RUNTIME / NOT_VALIDATOR /
    NOT_PRODUCTION
  FORMULAS: <mandatory limiting formulas — e.g.
    SIMULATION_RUN ≠ VALIDATION, TRACE_RUN ≠ RUNTIME_IMPLEMENTATION>

B.2 INPUT DATA
  <the sign/element under test, the contexts under test — if more than
  one context, see RULE_REMINDER: DIFFERENTIATION_CHECK_MANDATORY in
  section 0>
  PARSER_SCOPE: <explicitly state the boundaries — what the simulation
  parses, and what is taken as given in advance>

B.3 MATERIALS USED
  <explicit statement — use the FULL source files, not a reconstruction
  from memory; see the experience of the first DOT round, where a
  minimal snapshot gave distorted results>

B.4 RUNTIME_POLICY_INSTANCE / DEMO ARTIFACTS
  <if the simulation needs a demonstration policy or other auxiliary
  artifacts — explicitly mark them with the status
  DEMO / NOT_PART_OF_CORE_SPEC>

B.5 PIPELINE — STAGE ONE
  <run all stages of the first template in the chain, record
  INPUT/ACTION/OUTPUT at each stage>

B.6 PIPELINE — STAGE TWO
  <same for the next template in the chain>

[continue B.7, B.8... for additional pipeline stages, if there are
more than two]

------------------------------------------------------------
COMMON TO ALL PACKET TYPES:
------------------------------------------------------------

B.<N> FINDINGS CLASSIFICATION

  For REVIEW/AUDIT packets:
    CRITICAL_ISSUE: the document contains a forbidden construct, or
      omits a mandatory requirement without which the document cannot
      perform its function
    MAJOR_ISSUE: the wording is ambiguous enough that different users
      of the document will understand/fill it in fundamentally
      differently
    MINOR_ISSUE: an inaccuracy that does not create a divergence risk
      but requires clarification
    TRACE_ONLY_NOTE: an observation requiring no changes

  For SIMULATION packets:
    ARCHITECTURE_BUG: the pipeline cannot be passed even with correct
      input; the OUTPUT of one stage does not match the INPUT of the
      next; a mandatory check cannot be performed
    CARD_DATA_GAP: the artifact used (a card) does not contain a field
      required by the pipeline
    TEMPLATE_TO_TEMPLATE_INTERFACE_GAP: a downstream template (e.g.
      MODULE_TEMPLATE) expects a field or structure that the upstream
      document (the sign card) does not formally guarantee — differs
      from CARD_DATA_GAP in that this is not a gap in one specific
      card, but a lack of coordination between two different project
      documents. Found from the SOLIDUS round experience (a missing
      explicit ZONE field), added following external review (GPT-5.5).
    PIPELINE_INTERFACE_GAP: a more general class — the OUTPUT of one
      pipeline stage does not formally match the INPUT of the next
      stage, even if a human can restore the meaning manually. Differs
      from TEMPLATE_TO_TEMPLATE_INTERFACE_GAP in that it applies not
      only to the "card → MODULE_TEMPLATE" pair, but to any pair of
      pipeline stages (e.g. OUTPUT of MODULE_TEMPLATE vs INPUT of
      INTEGRATOR_TEMPLATE). Added following a repeat external review
      (GPT-5.5).
    POLICY_GAP: the demo policy does not cover the needed case
    SIMULATION_INPUT_GAP: the input does not contain data not declared
      as part of the simulation
    TRACE_ONLY_NOTE: a note that does not block the pipeline

B.<N+1> WHAT IS NOT PART OF THIS ROUND
  <explicitly list adjacent topics/tasks that do NOT need to be solved
  within this review — prevents scope creep and wasting the reviewer's
  effort on the irrelevant>

============================================================
PART C — DELIVERABLE_FORMAT
============================================================

[FOR REVIEW PACKETS:]

REVIEW_RESULT:
  REVIEWER: <model name>
  REVIEW_TARGET: <target document>
  ANSWERS_TO_QUESTIONS: <answer to each Q from B.2, with a finding
    classification or a confirmation "no findings">
  CRITICAL_ISSUES: <count + list>
  MAJOR_ISSUES: <count + list>
  MINOR_ISSUES: <count + list>
  TRACE_ONLY_NOTES: <list>
  VERDICT: <ACCEPT / ACCEPT_WITH_PATCHES / REJECT>
  READY_FOR_<NEXT_STEP>: <YES / NO / YES_AFTER_PATCHES>

FINDING_STATUS_RULE (mandatory for every finding in the issues above):
  Each reviewer finding carries a trivalent verification status:
    VERIFIED     — finding confirmed by a concrete check
                   (grep/diff/run/quote-with-locator — state WHAT)
    REJECTED     — finding refuted by a check (state WHAT)
    UNVERIFIABLE — structure intact, but content correspondence is not
                   machine-checkable → AUTHOR_DECISION required
  PROHIBITIONS (symmetric):
    - UNVERIFIABLE → VERIFIED without arbitration = FORBIDDEN (elision:
      "we don't know" passed off as "we know")
    - UNVERIFIABLE → REJECTED without arbitration = FORBIDDEN (guillotine:
      "we don't know" passed off as "refuted")
  DERIVED RULES:
    1. REVIEWER_CLAIM without FINDING_STATUS = NOT ADMITTED TO ARBITRATION
    2. FINDING_STATUS without a BASIS = ABSENCE OF FINDING_STATUS
       (a bare "VERIFIED" with no check shown is the same elision;
       the field is filled decoratively)
  LINK: operationalizes VERIFY_BEFORE_TRUST and GUIDED_TRAVERSAL_RISK —
    the coordinator checks the BASIS of every finding before accepting.
    An unauthorized UNVERIFIABLE→VERIFIED transition violates
    AUTHOR_DECISION_STATUS_AUTHORITY and is recorded in the packet.
  SOURCE: ACK_GAP_TRIVALENT_v0_2, Block A (AUTHOR_DECISION 2026-07-05).
  CONVEYOR_STATUS: WORKINGLY_CLOSED (2026-07-05) — passed conveyor:
    6 reviewers, unanimous ACCEPT; 3 patches applied (BASIS_MINIMUM,
    UNIVERSAL_SCOPE, FINDING_STATUS≠ISSUE_SEVERITY); AUTHOR_DECISION
    by Ruslan Malyavsky.

  BASIS_MINIMUM (patch after 6-reviewer conveyor 2026-07-05):
    A valid BASIS must name:
      METHOD   — how it was checked (grep / diff / run / quote / compare)
      TARGET   — where (file / section / line / field)
      OBSERVED — what was actually found
    EXPECTED and LOCATOR (line / path / command / test id) are strongly
    recommended; for VERIFIED and REJECTED a LOCATOR or reproducible
    command is mandatory where possible. For UNVERIFIABLE the basis
    must explain WHY the check cannot be completed mechanically.
  DECORATIVE_BASIS_GUARD:
    Bare "checked" / "obvious" / "reviewed" without METHOD+TARGET+
    OBSERVED is not a basis. Such a finding = absence of FINDING_STATUS.
  FINDING_STATUS ≠ ISSUE_SEVERITY:
    Verification status (VERIFIED/REJECTED/UNVERIFIABLE) is orthogonal
    to severity (CRITICAL/MAJOR/MINOR). A finding can be VERIFIED and
    MINOR; or UNVERIFIABLE and critically important (→ AUTHOR_DECISION).
  UNIVERSAL_SCOPE:
    FINDING_STATUS_RULE applies to EVERY finding in ALL deliverable
    formats (REVIEW_RESULT, AUDIT_RESULT, SIMULATION_RESULT) unless a
    packet explicitly declares otherwise.

[FOR AUDIT PACKETS — a separate format, not REVIEW_RESULT: comparing
  several artifacts is better expressed by a discrepancy matrix, not
  by answers to individual questions. Added following a repeat external
  review (GPT-5.5).]

AUDIT_RESULT:
  REVIEWER: <model name>
  AUDIT_TARGETS: <list of compared documents>
  COMPARISON_MATRIX: <table of discrepancies — field/aspect → value in
    each of the compared documents → match status>
  NORMALIZATION_FINDINGS: <list of systematic discrepancies requiring
    unification>
  CRITICAL_ISSUES: <count + list>
  MAJOR_ISSUES: <count + list>
  MINOR_ISSUES: <count + list>
  TRACE_ONLY_NOTES: <list>
  VERDICT: <ACCEPT / ACCEPT_WITH_PATCHES / REJECT>

[FOR SIMULATION PACKETS:]

SIMULATION_RESULT:
  REVIEWER: <model name>
  SIMULATION_TARGET: <simulation ID>
  SOURCE_CARD_USED: <exact reference to the loaded file, not a snapshot>
  <STAGE>_TRACE: <all steps with INPUT/ACTION/OUTPUT>
  [repeat for each pipeline stage]
  FINAL_RESULT: <the actual outcome of the simulation>
  MATCHES_EXPECTED: <YES/NO>
  [if several test cases:]
  DIFFERENTIATION_CHECK: <YES/NO — do the results differ between cases
    where they should differ>
  FINDINGS: <list with classification>
  VERDICT: <PASS / PASS_WITH_FINDINGS / ARCHITECTURE_BUG_FOUND>

============================================================
CONVEYOR_EXIT_CONDITION
============================================================

[FOR REVIEW/AUDIT PACKETS:]
ALL_REVIEWERS_ACCEPT → STATUS: READY_FOR_<NEXT_STEP>
ANY_CRITICAL_ISSUE → STATUS: REJECTED, patch cycle before re-review
ACCEPT_WITH_PATCHES (majority) → apply patches, if needed — a repeat
  round
DISAGREEMENT_BETWEEN_REVIEWERS → REQUIRES_ARBITRATION

[FOR SIMULATION PACKETS:]
ALL_REVIEWERS_PASS → SIMULATION_STATUS: CONFIRMED_PASS
ALL_REVIEWERS_PASS_WITH_FINDINGS_AND_NO_ARCHITECTURE_BUG →
  SIMULATION_STATUS: CONFIRMED_PASS_WITH_FINDINGS,
  REQUIRES_AUTHOR_ARBITRATION_FOR_NEXT_STEP (the findings by themselves
  do not block the transition, but the author must explicitly decide
  whether to patch them before the next step or record them as a known
  limitation). Added following a repeat external review (GPT-5.5) —
  closes the asymmetry: the PASS_WITH_FINDINGS verdict was already
  allowed in Part C (SIMULATION_RESULT), but had no corresponding path
  in the exit condition.
ANY_ARCHITECTURE_BUG_FOUND → STATUS: ESCALATE_TO_AUTHOR, suspend the
  transition to the next step
[IF APPLICABLE:]
DIFFERENTIATION_NOT_ACHIEVED → automatically ARCHITECTURE_BUG,
  regardless of how an individual reviewer classified it
DISAGREEMENT_BETWEEN_REVIEWERS → REQUIRES_ARBITRATION

NEXT_STEP_AFTER_SUCCESS: <what happens after the successful completion
  of this round — the next document, the next card, the transition to
  the next TIER, etc.>

============================================================
IMPORTANT REMINDER WHEN CHECKING OTHERS' REVIEWS (for the
coordinator, not for the reviewer)
============================================================

When several reviewers return results on one packet:

1. Do NOT sum the findings mechanically as "the majority is right".
   For each disputed point — personally verify the fact against the
   primary source (grep over the file, not a retelling), before
   deciding who is right.

2. Any message claiming the final status of a document
   ("WORKINGLY_CLOSED", "ARTIFACT_CONFIRMED", etc.) on behalf of a
   reviewer model is NOT a valid action. The final status is assigned
   only through AUTHOR_DECISION by the coordinating party (the project
   author), not by a unilateral statement of a conveyor participant.

3. A finding marked by one reviewer as CRITICAL/MAJOR is not
   automatically correct just because it is stricter than the others.
   Check the wording of the primary source (rules/specification) —
   is the literal requirement actually violated, or is this a
   suggestion for improvement that should be classified as an optional
   extension rather than a blocking finding.

============================================================
END_OF_TEMPLATE
