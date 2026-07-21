# -*- coding: utf-8 -*-
"""GATE: witness frame -- no auto-escalation.

The machine is a WITNESS, not a judge: the last word is always the human's. No runtime
action map may route a risk to an automatic intervention (escalate_to_human). The most
severe action a verdict may drive is hold_pending_review (a loud recommendation to look).

This pins CRITICAL -> hold_pending_review across ALL THREE action maps (single-sign
integrator, sequence integrator, relation axis), reconciling a demo artifact where the
single-sign / sequence integrators mapped CRITICAL -> escalate_to_human while the relation
axis already mapped it to hold (found in audit_silent_paths_2026-07-12 and re-found by an
external audit). CRITICAL is currently unreachable (no card emits it), so this closes a
LATENT auto-judge path with zero change to current behavior. Basis: witness frame,
three-level signal (escalate is OUTSIDE the CLEAN/POSSIBLE/REAL scale), D-O1-DESIGN D6.
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_BASE = os.path.dirname(_HERE)
for _p in ("core", "single_sign", "sequence"):
    sys.path.insert(0, os.path.join(_BASE, _p))
sys.path.insert(0, _BASE)

from sign_core_card import RiskLevel
import integrator_engine as single_sign_integrator
import sequence_integrator_engine as sequence_integrator
import msl_mip_runtime as rt

fails = []
HOLD = "hold_pending_review"
ESCALATE = "escalate_to_human"

# The three runtime action maps. Two are keyed by the RiskLevel enum, the relation
# axis map (_REL_ACTION) is keyed by the enum's string value.
enum_maps = {
    "single_sign.DEFAULT_ACTION_MAP": single_sign_integrator.DEFAULT_ACTION_MAP,
    "sequence.DEFAULT_ACTION_MAP": sequence_integrator.DEFAULT_ACTION_MAP,
}
for name, amap in enum_maps.items():
    got = amap.get(RiskLevel.CRITICAL)
    if got == ESCALATE:
        fails.append("%s maps CRITICAL -> escalate_to_human (auto-judge forbidden)" % name)
    elif got != HOLD:
        fails.append("%s maps CRITICAL -> %r (expected hold_pending_review)" % (name, got))
    # Defensive: no other level may route to escalate either.
    for lvl, act in amap.items():
        if act == ESCALATE:
            fails.append("%s maps %s -> escalate_to_human (auto-judge forbidden)" % (name, lvl))

rel = rt._REL_ACTION
if rel.get("CRITICAL") == ESCALATE:
    fails.append("relation _REL_ACTION maps CRITICAL -> escalate_to_human")
elif rel.get("CRITICAL") != HOLD:
    fails.append("relation _REL_ACTION maps CRITICAL -> %r (expected hold)" % rel.get("CRITICAL"))
for k, act in rel.items():
    if act == ESCALATE:
        fails.append("relation _REL_ACTION maps %s -> escalate_to_human" % k)

print("=" * 60)
print("GATE: witness frame -- no auto-escalation")
print("=" * 60)
if fails:
    for f in fails:
        print("  FAIL: " + f)
    print("\nTOTAL: FAIL")
    sys.exit(1)
print("all 3 action maps (single-sign, sequence, relation) map CRITICAL -> hold_pending_review")
print("no runtime action map routes any level to escalate_to_human")
print("\nTOTAL: CLEAN -- machine stays a witness, not a judge")
sys.exit(0)
