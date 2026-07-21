# -*- coding: utf-8 -*-
"""GATE: pending disposition (P3) -- deferred is DATA, never silence, never policy.

The BOM x BYTE_EXACT_TOKEN cell was examined and deliberately left at MEDIUM/queue. If the
registry simply carried no row, a reader could not tell "examined and deliberately left"
from "never looked at" -- and absence would read as "checked, clean". P3 records the cell
as PENDING_PREDICATE with BOTH honest readings, the gap that blocks a rule, and the
evidence that would unblock it.

The load-bearing invariant: a PENDING row is DOCUMENTATION, not policy. It must never be
consulted by evaluate() and must never move a level. This gate pins that.

  A the pending registry lints (two readings, gap, evidence, provenance, no duplicates)
  B PENDING NEVER ESCALATES -- evaluate() ignores it even with O1 enabled
  C the report carries the disposition for the token cell, with provenance
  D verdict-neutral -- verdicts identical whether or not the disposition is produced
Basis: AUTHOR_DECISION_20260721_D-O1-TOKEN-CELL (P3).
"""
import contextlib
import io
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_BASE = os.path.dirname(_HERE)
os.environ["MSL_MIP_HERMETIC_TLD"] = "1"
for _p in ("core", "single_sign", "sequence"):
    sys.path.insert(0, os.path.join(_BASE, _p))
sys.path.insert(0, _BASE)

import msl_mip_runtime as rt
import o1_policy_engine as o1
import sequence_engine as se
from sign_core_card import RiskLevel
from load_card import load_card
se._force_tld_state_for_test(frozenset({"com", "org", "net", "ru", "io", "dev", "xn--p1ai"}), False)

_C = os.path.join(_BASE, "cards")
MASK = load_card(os.path.join(_C, "SIGN_CORE_CARD_FULLWIDTH_SOLIDUS_UFF0F_GEN3_v0_3_RU.md"))
BOM_CARD = load_card(os.path.join(_C, "SIGN_CORE_CARD_BYTE_ORDER_MARK_UFEFF_GEN3_v0_1_RU.md"))
CARDS = [BOM_CARD, MASK]
B = "﻿"
TOKEN_CASE = "bad" + B + "word"

fails = []


def _analyze(text):
    with contextlib.redirect_stdout(io.StringIO()):
        return rt.analyze(text, CARDS)


def _verdicts(rep):
    return tuple((v.get("visible_form"), v.get("at_offset"), v.get("detected_context"),
                  v.get("risk_level"), v.get("runtime_role"))
                 for v in rep["sequence_output"].relation_verdicts) + \
           (rep.get("semantic_action"), rep.get("effective_action"))


# ------------------------------------------------------------------------- A lint
if o1.lint_pending_registry() != []:
    fails.append("A pending registry does not lint clean: %s" % o1.lint_pending_registry())
if not o1.PENDING_PREDICATE_REGISTRY:
    fails.append("A pending registry is empty (the token cell must be documented)")

PR = o1.PendingRow
bad_pending = [
    ("one-reading", PR(0xFEFF, "X", ("only one",), "gap", "evidence", "prov")),
    ("no-gap",      PR(0xFEFF, "X", ("a", "b"), "", "evidence", "prov")),
    ("no-evidence", PR(0xFEFF, "X", ("a", "b"), "gap", "", "prov")),
    ("no-provenance", PR(0xFEFF, "X", ("a", "b"), "gap", "evidence", "")),
    ("empty-context", PR(0xFEFF, "", ("a", "b"), "gap", "evidence", "prov")),
]
for name, row in bad_pending:
    if o1.lint_pending_registry([row]) == []:
        fails.append("A malformed pending row NOT rejected: " + name)

# --------------------------------------------------- B PENDING NEVER ESCALATES
# The documented cell is exactly (U+FEFF, BYTE_EXACT_TOKEN). With O1 ENABLED and the
# active registry empty, evaluating that very cell must still return the base level.
os.environ["MSL_MIP_O1_ENABLED"] = "1"
final, dec = o1.final_level(RiskLevel.MEDIUM, 0xFEFF, "BYTE_EXACT_TOKEN")
os.environ["MSL_MIP_O1_ENABLED"] = "0"
if final != RiskLevel.MEDIUM or dec.matched:
    fails.append("B a PENDING cell ESCALATED -- documentation leaked into policy")
if dec.reason != "NO_ACTIVE_RULE":
    fails.append("B pending cell reason %r (want NO_ACTIVE_RULE)" % dec.reason)

# ------------------------------------------------------------------- C the report
rep = _analyze(TOKEN_CASE)
disp = rep.get("pending_disposition")
if not disp:
    fails.append("C report carries no pending_disposition for the token cell")
else:
    e = disp[0]
    if e.get("status") != "PENDING_PREDICATE":
        fails.append("C status %r (want PENDING_PREDICATE)" % e.get("status"))
    if e.get("context") != "BYTE_EXACT_TOKEN" or e.get("codepoint") != "U+FEFF":
        fails.append("C disposition points at the wrong cell: %r" % e)
    if len(e.get("consistent_with") or []) < 2:
        fails.append("C disposition must name BOTH readings, got %r" % e.get("consistent_with"))
    for field in ("blocking_gap", "required_evidence", "provenance"):
        if not e.get(field):
            fails.append("C disposition missing %s" % field)
    if "at_offset" not in e:
        fails.append("C disposition missing at_offset")

# a cell with no pending record must produce no disposition
host = _analyze("pay" + B + "pal.com")
if host.get("pending_disposition"):
    fails.append("C disposition emitted for a NON-pending cell (mid-host)")

# ------------------------------------------------------------- D verdict-neutral
base_v = _verdicts(rep)
saved = o1.PENDING_PREDICATE_REGISTRY
try:
    o1.PENDING_PREDICATE_REGISTRY = ()          # no documentation at all
    empty_rep = _analyze(TOKEN_CASE)
    if empty_rep.get("pending_disposition"):
        fails.append("D disposition produced from an EMPTY pending registry")
    if _verdicts(empty_rep) != base_v:
        fails.append("D verdicts changed when the pending registry was emptied")
finally:
    o1.PENDING_PREDICATE_REGISTRY = saved

print("=" * 66)
print("GATE: pending disposition (P3) -- deferred is data, not silence")
print("=" * 66)
if fails:
    for f in fails:
        print("  FAIL: " + f)
    print("\nTOTAL: FAIL")
    sys.exit(1)
print("A pending registry lints; %d malformed rows rejected" % len(bad_pending))
print("B a PENDING cell NEVER escalates -- documentation cannot leak into policy")
print("C the report names both readings + gap + evidence + provenance for the token cell")
print("D verdict-neutral: emptying the pending registry changes no verdict")
print("\nTOTAL: CLEAN -- 'not applied' is recorded as data, and stays powerless over levels")
sys.exit(0)
