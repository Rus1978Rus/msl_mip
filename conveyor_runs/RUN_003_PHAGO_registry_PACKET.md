PRIVATE AUTHORED PROJECT / COMMERCIAL USE PROHIBITED

RULE_REMINDER: VERIFY_BEFORE_TRUST_MANDATORY
  Verify PHAGO flags against the actual card content, not from memory.
  Card facts: SOLIDUS has PHAGO_ENTITY_MIMICRY: APPLICABLE (RISK_CASE_007,
  OpenAI/VerifiedProjectX). DOT has PHAGO_ENTITY_MIMICRY: NOT_APPLICABLE.
  SKULL has PE_001/PE_002 marked SEMANTIC_AMBIGUITY (not classic PHAGO,
  adapted for emoji domain).

DOCUMENT_ID: CONVEYOR_RUN_PACKET_MSL_MIP_PHAGO_REGISTRY_v0_1
PACKET_TYPE: REVIEW
PACKET_SUBTYPE: REGISTRY_DIMENSION_REVIEW

CONTEXT: The SIGN_PRIORITY_REGISTRY previously ranked signs only by
PH/INJ/LLM category. A gap was found: PHAGO_ENTITY_MIMICRY (mimicry of
a verified entity's existence, not just structure masking) was proven
real at the card level (SOLIDUS) but was not surfaced as a dimension in
the registry. This patch adds PHAGO as an explicit orthogonal
dimension, plus a summary table separating CONFIRMED (card-verified)
from HYPOTHESIS (flagged for future per-card review).

PART A — MATERIALS
- SIGN_PRIORITY_REGISTRY_v0_1_DRAFT.md (patched)

PART B — WHAT TO CHECK
B.1. ORTHOGONALITY: Is PHAGO correctly defined as a SEPARATE dimension
  from PH/INJ/LLM (not a fourth category, but a cross-cutting flag)? Is
  the distinction "entity-existence mimicry vs structure masking" clear
  and correct?
B.2. CONFIRMED FLAGS: Do the three CONFIRMED flags match the actual
  cards?
    - `/` U+002F = ● (strong) — matches SOLIDUS APPLICABLE / RISK_CASE_007?
    - 💀 U+1F480 = ○ (partial) — matches SKULL PE_001/002 SEMANTIC_AMBIGUITY?
    - `.` U+002E = — (none) — matches DOT NOT_APPLICABLE?
B.3. HYPOTHESIS CANDIDATES: Are the HYPOTHESIS flags reasonable, and
  correctly labeled as NOT-yet-confirmed?
    - `@` = ● (userinfo implies verified account) — sound?
    - `-` = ● (fake compound brand implies affiliated entity) — sound?
    - homoglyphs `а`/`ο` = ● (mimic the brand NAME itself) — sound?
    - `_` = ○ (fake subdomains) — sound, or overstated?
B.4. Is the CONFIRMED vs HYPOTHESIS separation honest — i.e. nothing
  presented as fact that is only a hypothesis?

PART C — FIND ERRORS
C.1. Any sign that should carry a PHAGO flag but is missing from the
  summary table?
C.2. Any HYPOTHESIS flag that is actually a category error (not real
  entity mimicry)?
C.3. Does the bilingual (EN/RU) text stay consistent?

PART D — DELIVERABLE
REVIEW_RESULT:
  REVIEWER: <name>
  B.1-B.4, C.1-C.3: <answers with direct check against card facts>
  MISSING_PHAGO_SIGNS: <list>
  OVERSTATED_FLAGS: <list>
  VERDICT: APPROVE / APPROVE_WITH_FIXES / REJECT

END_OF_PACKET
