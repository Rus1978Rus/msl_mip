# -*- coding: utf-8 -*-
"""O1 CONTEXTUAL SEVERITY POLICY LAYER -- increment-0 (empty engine).

Seam id: RELATION_PATH_O1_HOOK_v0_1.

An additive, per-occurrence severity overlay that sits ABOVE the base risk computed
in sequence_engine._assess_relation_risk. Increment-0 ships the SEAM and the
infrastructure ONLY: the active registry is EMPTY, so the overlay never fires and the
final level always equals the base level. A zero-delta gate
(tests/gate_o1_increment0_zero_delta.py) proves the seam alone changes nothing on the
verified ZWSP / ZWJ / BOM batteries.

Design basis: AUTHOR_DECISION_20260721_D-O1-IMPL-SCOPE, AUTHOR_DECISION_20260721_D-O1-DESIGN.
  - additive, monotonic: final = max(base, overlay); absence = identity; RAISE-ONLY.
  - sparse exact-match registry keyed by CODEPOINT sign_id (not name / visible_form).
  - severity lives ONLY in the registry; the card owns the occurrence-role vocabulary.
  - REAL = HIGH -> hold; CRITICAL / escalate are forbidden by the linter (witness frame).
  - reads ready verdict fields only; NEVER calls the _detect_context_at hotspot.
  - the audit field is written ONLY when a row fires (final > base); in increment-0 it
    never fires, so no field is added and the batteries stay bit-identical.
  - the seam is named, not universal: it covers the relation-verdict path only. A future
    sign whose risk flows via another path is blocked by the row-liveness precondition
    (a row must fire on its reconcile input) before it can be activated.
"""
from __future__ import annotations

import os
from collections import namedtuple

from sign_core_card import RiskLevel

SEAM_ID = "RELATION_PATH_O1_HOOK_v0_1"

# A policy row (used from increment-1 onward). Increment-0 registry is EMPTY.
#   sign_cp         -- CODEPOINT of the sign (int), never a name / visible_form.
#   context         -- measured detected_context (e.g. "BYTE_EXACT_TOKEN"), never a class/wildcard.
#   occurrence_role -- role vocabulary owned by the card, or None.
#   target          -- RiskLevel to escalate to (raise-only; NONE/CRITICAL forbidden).
#   rule_id         -- stable id, required.
#   provenance      -- reconcile + author-decision id, required.
PolicyRow = namedtuple("PolicyRow", "sign_cp context occurrence_role target rule_id provenance")

# INCREMENT-0: NO active rules. Rows are added, one at a time with provenance, only
# after their own author decision + row-liveness proof (never wholesale).
ACTIVE_POLICY_REGISTRY: tuple = ()

# --- PENDING disposition (P3 of AUTHOR_DECISION_20260721_D-O1-TOKEN-CELL) -------------
# A cell that was EXAMINED and deliberately left un-escalated must not read as silence.
# "No rule" and "rule applied, did not fire" are different facts, and a reader of the
# registry deserves to see WHY a known divergence carries no row: what gap blocks it and
# what evidence would unblock it. These rows are DOCUMENTATION: they are NEVER consulted
# by evaluate() and can never change a level (the gate pins this).
PendingRow = namedtuple(
    "PendingRow", "sign_cp context hypotheses blocking_gap required_evidence provenance")

PENDING_PREDICATE_REGISTRY: tuple = (
    PendingRow(
        sign_cp=0xFEFF,
        context="BYTE_EXACT_TOKEN",
        # Both readings are honest and, at this seam, indistinguishable. Saying so beats
        # a level that pretends to a precision the runtime does not have.
        hypotheses=("ghost-token attack (exact-match / allowlist evasion)",
                    "transport artifact (export, paste, file concatenation)"),
        blocking_gap="no predicate at this seam separates the two readings; a direct rule "
                     "measured 67% benign escalations",
        required_evidence="collapse-form predicate: the token's collapse matches the "
                          "CONSUMER's protected allowlist (measured benign FP 0% / ghost "
                          "TP 100%); needs collapse wiring, allowlist config and its own "
                          "author decision",
        provenance="RECONCILE_BYSPEC_ZWJ_BOM B3 + FP-measurement 2026-07-21 + "
                   "AUTHOR_DECISION_20260721_D-O1-TOKEN-CELL",
    ),
)

# Outcome of one occurrence's O1 evaluation.
#   reason: DISABLED | NO_ACTIVE_RULE | NO_OP | APPLIED
PolicyDecision = namedtuple(
    "PolicyDecision", "base_level final_level matched rule_id provenance reason")

# Witness scale for O1 targets: an overlay escalates to queue (MEDIUM) or hold (HIGH).
# NONE (no-op), LOW (below the scale), and CRITICAL/escalate (out of the witness frame,
# = auto-intervention) are all forbidden as targets.
_ALLOWED_TARGETS = frozenset({RiskLevel.MEDIUM, RiskLevel.HIGH})
_ZWSP_CP = 0x200B                                     # verified path -- never an O1 key
_WILDCARD_CONTEXTS = frozenset({"*", "ANY", "ALL", None})
_WILDCARD_ROLES = frozenset({"*", "ANY", "ALL", ""})


def o1_enabled() -> bool:
    """Read the flag at CALL time (so a test can toggle OFF/ON within one process).
    Default OFF: the seam returns the base level unchanged until O1 is switched on."""
    return os.environ.get("MSL_MIP_O1_ENABLED", "0") == "1"


def _lookup(sign_cp, context, occurrence_role):
    for row in ACTIVE_POLICY_REGISTRY:
        if (row.sign_cp, row.context, row.occurrence_role) == (sign_cp, context, occurrence_role):
            return row
    return None


def evaluate(base_level: RiskLevel, sign_cp, context: str,
             occurrence_role=None) -> PolicyDecision:
    """The O1 decision for one occurrence. Increment-0: registry empty -> always
    NO_ACTIVE_RULE -> final == base. RAISE-ONLY, absence = identity."""
    if not o1_enabled():
        return PolicyDecision(base_level, base_level, False, None, None, "DISABLED")
    row = _lookup(sign_cp, context, occurrence_role)
    if row is None:
        return PolicyDecision(base_level, base_level, False, None, None, "NO_ACTIVE_RULE")
    final = RiskLevel.max(base_level, row.target)  # monotonic combine
    # INTEGRITY invariant (conservation of severity): O1 may only RAISE, never lower.
    # final == max(base, target) is raise-only by construction; this re-checks the
    # returned value against base independently, so a future change to the combine
    # that lowered risk would fail loudly here rather than silently under-escalate.
    if RiskLevel.max(base_level, final) != final:
        raise AssertionError(
            "O1 integrity violated: final %s is below base %s (rule %s)"
            % (final, base_level, row.rule_id))
    matched = final != base_level
    return PolicyDecision(base_level, final, matched, row.rule_id, row.provenance,
                          "APPLIED" if matched else "NO_OP")


def final_level(base_level: RiskLevel, sign_cp, context: str,
                occurrence_role=None):
    """Seam entry point. Returns (final RiskLevel, PolicyDecision).
    In increment-0 final_level is ALWAYS base_level."""
    d = evaluate(base_level, sign_cp, context, occurrence_role)
    return d.final_level, d


def audit_field(decision: PolicyDecision):
    """The audit dict for a FIRED row, or None. Written IFF the row raised the level
    (decision.matched) -- never a second decision channel, and absent when no row
    fired, so increment-0 output carries no new field."""
    if not decision.matched:
        return None
    return {
        "base_level": decision.base_level.value,
        "final_level": decision.final_level.value,
        "rule_id": decision.rule_id,
        "provenance": decision.provenance,
        "seam": SEAM_ID,
    }


def pending_for(sign_cp, context):
    """The PENDING disposition record for a cell, or None. Pure lookup over DOCUMENTATION
    rows -- callers may only report it. It is NOT consulted by evaluate() and cannot
    change a level."""
    for row in PENDING_PREDICATE_REGISTRY:
        if (row.sign_cp, row.context) == (sign_cp, context):
            return {
                "codepoint": "U+%04X" % row.sign_cp,
                "context": row.context,
                "status": "PENDING_PREDICATE",
                "consistent_with": list(row.hypotheses),
                "blocking_gap": row.blocking_gap,
                "required_evidence": row.required_evidence,
                "provenance": row.provenance,
            }
    return None


def lint_pending_registry(registry=None) -> list:
    """Form check for the PENDING rows. They never affect a verdict, but a documentation
    row with no gap, no evidence or no provenance is worthless -- it would re-create the
    silence it exists to remove. Returns (context, reason) failures; empty list is clean."""
    if registry is None:
        registry = PENDING_PREDICATE_REGISTRY
    fails = []
    seen = set()
    for row in registry:
        cid = "%s/%s" % (row.sign_cp, row.context)
        if not isinstance(row.sign_cp, int) or isinstance(row.sign_cp, bool):
            fails.append((cid, "sign_cp must be an int codepoint"))
        if not isinstance(row.context, str) or not row.context:
            fails.append((cid, "context must be a concrete non-empty string"))
        if not row.hypotheses or len(row.hypotheses) < 2:
            fails.append((cid, "a pending cell must name at least TWO readings (it is "
                               "pending precisely because they are indistinguishable)"))
        if not row.blocking_gap:
            fails.append((cid, "missing blocking_gap (what stops a rule)"))
        if not row.required_evidence:
            fails.append((cid, "missing required_evidence (what would unblock it)"))
        if not row.provenance:
            fails.append((cid, "missing provenance"))
        if cid in seen:
            fails.append((cid, "duplicate pending cell"))
        seen.add(cid)
    return fails


def lint_registry(registry=None) -> list:
    """Structural linter for the policy registry. Returns a list of (rule_id, reason)
    failures; an empty list is clean. The increment-0 empty registry passes trivially,
    but the linter is real and self-tested (each malformed row must be rejected).

    Rejects, per row:
      - sign_cp not an int codepoint (a string like "U+FEFF" is a DEAD row: the seam
        keys by ord(vf):int, so a string key never matches -- caught here, not at runtime);
      - ZWSP codepoint as a key (verified path);
      - context that is empty / not a concrete string / a wildcard / class-default;
      - occurrence_role that is a wildcard string (None is allowed);
      - target that is not a RiskLevel, or not in {MEDIUM, HIGH} (NONE/LOW/CRITICAL out);
      - missing rule_id or provenance;
      - a duplicate (sign_cp, context, occurrence_role) key (_lookup would silently
        shadow the second row).
    NOTE: the 'no-op vs the context base' check (target <= the base risk of that context)
    needs the _SCOPE_RISK base map and is wired in increment-1 when rules exist.
    """
    if registry is None:
        registry = ACTIVE_POLICY_REGISTRY
    fails = []
    seen = {}
    for row in registry:
        rid = row.rule_id or "<no-id>"
        # sign_cp: an int codepoint, never a name/string/None/bool.
        if not isinstance(row.sign_cp, int) or isinstance(row.sign_cp, bool):
            fails.append((rid, "sign_cp must be an int codepoint (not a name/string/None)"))
        elif row.sign_cp == _ZWSP_CP:
            fails.append((rid, "ZWSP key forbidden (verified path)"))
        # context: a concrete non-empty string, never a class/wildcard.
        if not isinstance(row.context, str) or row.context == "" \
                or row.context in _WILDCARD_CONTEXTS:
            fails.append((rid, "context must be a concrete non-empty string (no wildcard/class-default)"))
        # occurrence_role: None is allowed; a wildcard string is not.
        if row.occurrence_role is not None and (
                not isinstance(row.occurrence_role, str)
                or row.occurrence_role in _WILDCARD_ROLES):
            fails.append((rid, "occurrence_role must be None or a concrete role (no wildcard)"))
        # target: raise-only escalation to a witness level (MEDIUM=queue / HIGH=hold).
        if not isinstance(row.target, RiskLevel):
            fails.append((rid, "target is not a RiskLevel"))
        elif row.target not in _ALLOWED_TARGETS:
            fails.append((rid, "target must be MEDIUM or HIGH (no NONE/LOW/CRITICAL)"))
        # provenance + rule_id required.
        if not row.rule_id:
            fails.append((rid, "missing rule_id"))
        if not row.provenance:
            fails.append((rid, "missing provenance"))
        # duplicate exact key -> _lookup silently takes the first; forbid it.
        key = (row.sign_cp, row.context, row.occurrence_role)
        if key in seen:
            fails.append((rid, "duplicate key %r (shadows rule %s)" % (key, seen[key])))
        else:
            seen[key] = rid
    return fails
