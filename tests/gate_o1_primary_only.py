# -*- coding: utf-8 -*-
"""GATE: the O1 overlay may raise ONLY a PRIMARY edge (Level 2 runtime_role contract).

Finding W3 (Kimi methodological audit 2026-07-26, reproduced by measurement): the O1 seam
in _assess_relation_risk applied final_level to EVERY edge regardless of runtime_role. With
a consumer target list, pay<BOM>pal produced THREE HIGH verdicts on one offset -- the
legitimate PRIMARY (BOUNDARY_DISRUPTOR) plus a TAXONOMY_ONLY and a SUPPORTING_FACET edge
that Level 2 says must NOT emit an independent risk. That revived the Z1 duplicate-verdict
Level 2 removed, and hung the o1_policy audit on edges documented as non-driving. The final
action was unchanged (max still HIGH from PRIMARY), so this gate asserts the CONTRACT, not
the action: the non-PRIMARY edges stay at their base risk and carry no O1 audit.

  A PRIMARY still raised -- BOUNDARY_DISRUPTOR reaches HIGH (the C6 impersonation is caught).
  B non-PRIMARY NOT raised -- INVISIBLE_CLASS_COLLISION (TAXONOMY_ONLY) and ABSENCE_CONFUSABLE
    (SUPPORTING_FACET) stay NONE and carry no o1_policy audit field.
  C action preserved -- effective_action is still hold_pending_review (from the PRIMARY edge),
    proving the fix restores the contract WITHOUT weakening the verdict.
Basis: finding W3; AUTHOR_DECISION Level 2 (S-03) runtime_role contract; D-O1-C6-NARROW.
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
import sequence_engine as se
from load_card import load_card
se._force_tld_state_for_test(frozenset({"com", "org", "net", "ru"}), False)

_C = os.path.join(_BASE, "cards")
MASK = load_card(os.path.join(_C, "SIGN_CORE_CARD_FULLWIDTH_SOLIDUS_UFF0F_GEN3_v0_3_RU.md"))
BOM_CARD = load_card(os.path.join(_C, "SIGN_CORE_CARD_BYTE_ORDER_MARK_UFEFF_GEN3_v0_1_RU.md"))
CARDS = [BOM_CARD, MASK]
B = "﻿"
GHOST = "pay" + B + "pal"
TARGETS = {"paypal"}

fails = []


def _run(text, targets=None):
    with contextlib.redirect_stdout(io.StringIO()):
        return rt.analyze(text, CARDS, protected_targets=targets)


rep = _run(GHOST, TARGETS)
by_role = {}
for v in rep["sequence_output"].relation_verdicts:
    if v["visible_form"] == B:
        by_role[v.get("runtime_role")] = v

# ----------------------------------------------------------------- A PRIMARY still raised
prim = by_role.get("PRIMARY")
if not prim:
    fails.append("A no PRIMARY (BOUNDARY_DISRUPTOR) edge at all")
elif prim.get("risk_level") != "HIGH":
    fails.append("A PRIMARY edge not raised to HIGH: %r" % prim.get("risk_level"))

# ------------------------------------------------------------- B non-PRIMARY NOT raised
for role in ("TAXONOMY_ONLY", "SUPPORTING_FACET"):
    edge = by_role.get(role)
    if not edge:
        # absence is acceptable, but if present it must not be raised
        continue
    if edge.get("risk_level") != "NONE":
        fails.append("B %s edge was raised by O1: %r (contract: non-PRIMARY drives no risk)"
                     % (role, edge.get("risk_level")))
    if edge.get("o1_policy") is not None:
        fails.append("B %s edge carries an o1_policy audit (O1 ran on a non-PRIMARY edge)"
                     % role)

# --------------------------------------------------------------------- C action preserved
if rep.get("effective_action") != "hold_pending_review":
    fails.append("C the verdict weakened: effective=%r (expected hold_pending_review "
                 "from the PRIMARY edge)" % rep.get("effective_action"))

print("=" * 68)
print("GATE: O1 overlay raises PRIMARY edges only (runtime_role contract)")
print("=" * 68)
if fails:
    for f in fails:
        print("  FAIL: " + f)
    print("\nTOTAL: FAIL")
    sys.exit(1)
print("A PRIMARY (BOUNDARY_DISRUPTOR) still reaches HIGH -- impersonation caught")
print("B TAXONOMY_ONLY + SUPPORTING_FACET stay NONE, no O1 audit -- contract held")
print("C effective_action still hold_pending_review -- verdict not weakened")
print("\nTOTAL: CLEAN -- O1 no longer double-verdicts on non-PRIMARY edges")
sys.exit(0)
