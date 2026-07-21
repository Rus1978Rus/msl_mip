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

# Outcome of one occurrence's O1 evaluation.
#   reason: DISABLED | NO_ACTIVE_RULE | NO_OP | APPLIED
PolicyDecision = namedtuple(
    "PolicyDecision", "base_level final_level matched rule_id provenance reason")

_FORBIDDEN_TARGETS = frozenset({RiskLevel.CRITICAL})  # witness frame: no auto-escalation
_ZWSP_CP = 0x200B                                     # verified path -- never an O1 key
_WILDCARD_CONTEXTS = frozenset({"*", "ANY", None})


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


def lint_registry(registry=None) -> list:
    """Structural linter for the policy registry. Returns a list of (rule_id, reason)
    failures; an empty list is clean. The increment-0 empty registry passes trivially,
    but the linter is real and self-tested (a bad row must be rejected).

    Rejects: ZWSP key (verified path); wildcard / class-default key; a target that is
    not a RiskLevel; a CRITICAL/escalate target (witness frame); a NONE target (a no-op
    that can never raise); a missing rule_id or provenance.
    NOTE: the 'no-op vs the context base' check (a target <= the base risk of that
    context) needs the _SCOPE_RISK base map and is wired in increment-1 when rules exist.
    """
    if registry is None:
        registry = ACTIVE_POLICY_REGISTRY
    fails = []
    for row in registry:
        rid = row.rule_id or "<no-id>"
        if row.sign_cp == _ZWSP_CP:
            fails.append((rid, "ZWSP key forbidden (verified path)"))
        if row.sign_cp is None or row.sign_cp == "*" or row.context in _WILDCARD_CONTEXTS \
                or row.occurrence_role == "*":
            fails.append((rid, "wildcard / class-default key forbidden"))
        if not isinstance(row.target, RiskLevel):
            fails.append((rid, "target is not a RiskLevel"))
        elif row.target in _FORBIDDEN_TARGETS:
            fails.append((rid, "CRITICAL/escalate target forbidden (witness frame)"))
        elif row.target == RiskLevel.NONE:
            fails.append((rid, "NONE target is a no-op (cannot raise)"))
        if not row.rule_id:
            fails.append((rid, "missing rule_id"))
        if not row.provenance:
            fails.append((rid, "missing provenance"))
    return fails
