# -*- coding: utf-8 -*-
"""GATE: O1 increment-0 -- zero-delta + engine self-test.

Two parts, both must pass:

PART A (engine self-test, in-process): the empty registry lints clean; every kind of
  malformed row is REJECTED by the linter (so the linter is real, not decorative); the
  seam is inert with an empty registry; and -- crucially -- the engine is LIVE (a row
  injected for the test DOES raise + audit), so the zero-delta below is because the
  registry is EMPTY, not because the seam is a dead stub.

PART B (zero-delta, subprocess): the two verified batteries (sim_bycode_v2 = ZWSP 21/21,
  zwj_bom_battery = ZWJ/BOM 11/11 + mutations) are run with O1 OFF and O1 ON. Both must
  PASS (frozen expectations preserved) AND produce BIT-IDENTICAL stdout OFF vs ON (the
  seam alone changes exactly nothing). Any stdout difference = the seam is not inert.

This gate is scoped to INCREMENT-0. Once a behavioral rule is added, O1-ON output will
(intentionally) differ from O1-OFF and this exact-identity check is superseded by the
delta-census gate. Basis: AUTHOR_DECISION_20260721_D-O1-IMPL-SCOPE.
"""
import os
import subprocess
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_BASE = os.path.dirname(_HERE)
for _p in ("core", "single_sign", "sequence"):
    sys.path.insert(0, os.path.join(_BASE, _p))
sys.path.insert(0, _BASE)

import o1_policy_engine as o1
from sign_core_card import RiskLevel

fails = []
PR = o1.PolicyRow
BOM_CP = 0xFEFF

# ------------------------------------------------------------------ PART A
# A1: the increment-0 empty registry lints clean.
if o1.lint_registry(()) != []:
    fails.append("A1 empty registry did not lint clean")

# A2: every malformed row must be rejected (linter is real).
bad_rows = [
    ("zwsp-key",     PR(0x200B, "BYTE_EXACT_TOKEN", None, RiskLevel.HIGH, "r", "p")),
    ("wildcard-ctx", PR(BOM_CP, "ANY",              None, RiskLevel.HIGH, "r", "p")),
    ("critical",     PR(BOM_CP, "HOST",             None, RiskLevel.CRITICAL, "r", "p")),
    ("none-target",  PR(BOM_CP, "HOST",             None, RiskLevel.NONE, "r", "p")),
    ("no-provenance",PR(BOM_CP, "HOST",             None, RiskLevel.HIGH, "r", "")),
    ("no-rule-id",   PR(BOM_CP, "HOST",             None, RiskLevel.HIGH, "", "p")),
    ("target-not-enum", PR(BOM_CP, "HOST",          None, "HIGH", "r", "p")),
]
for name, row in bad_rows:
    if o1.lint_registry([row]) == []:
        fails.append("A2 malformed row NOT rejected: " + name)

# A3: a well-formed row lints clean.
good = PR(BOM_CP, "BYTE_EXACT_TOKEN", None, RiskLevel.HIGH, "R1", "RECONCILE_B3+AD")
if o1.lint_registry([good]) != []:
    fails.append("A3 well-formed row wrongly rejected")

# A4: with the empty registry the seam is inert even when O1 is enabled.
os.environ["MSL_MIP_O1_ENABLED"] = "1"
fr, dec = o1.final_level(RiskLevel.MEDIUM, BOM_CP, "BYTE_EXACT_TOKEN")
if fr != RiskLevel.MEDIUM or dec.matched or o1.audit_field(dec) is not None:
    fails.append("A4 empty-registry seam not inert when enabled")

# A5: the engine is LIVE (not a dead stub) -- inject a row, it must raise + audit,
#     and it must be RAISE-ONLY (a base already at/above the target is not lowered).
saved = o1.ACTIVE_POLICY_REGISTRY
try:
    o1.ACTIVE_POLICY_REGISTRY = (good,)
    fr, dec = o1.final_level(RiskLevel.MEDIUM, BOM_CP, "BYTE_EXACT_TOKEN")
    if fr != RiskLevel.HIGH or not dec.matched:
        fails.append("A5 engine did not raise on a matching row")
    af = o1.audit_field(dec)
    if not af or af.get("final_level") != "HIGH" or af.get("base_level") != "MEDIUM" \
            or af.get("seam") != o1.SEAM_ID:
        fails.append("A5 audit field wrong on a fired row")
    # raise-only: base HIGH, target HIGH -> stays HIGH, no spurious change, not matched.
    fr2, dec2 = o1.final_level(RiskLevel.HIGH, BOM_CP, "BYTE_EXACT_TOKEN")
    if fr2 != RiskLevel.HIGH or dec2.matched:
        fails.append("A5 raise-only broken (base at target should be a no-op)")
    # a non-matching key must not fire.
    fr3, dec3 = o1.final_level(RiskLevel.MEDIUM, BOM_CP, "EMAIL")
    if fr3 != RiskLevel.MEDIUM or dec3.matched:
        fails.append("A5 non-matching key fired")
finally:
    o1.ACTIVE_POLICY_REGISTRY = saved
    os.environ["MSL_MIP_O1_ENABLED"] = "0"

# ------------------------------------------------------------------ PART B
def run_battery(script, enabled):
    env = dict(os.environ, PYTHONIOENCODING="utf-8",
               MSL_MIP_O1_ENABLED=("1" if enabled else "0"))
    p = subprocess.run([sys.executable, os.path.join(_HERE, script)], cwd=_BASE,
                       env=env, capture_output=True, text=True, encoding="utf-8",
                       timeout=300)
    return p.returncode, p.stdout

for script in ("sim_bycode_v2.py", "zwj_bom_battery.py"):
    rc_off, out_off = run_battery(script, False)
    rc_on, out_on = run_battery(script, True)
    if rc_off != 0:
        fails.append("B %s did NOT pass with O1 OFF (rc=%s)" % (script, rc_off))
    if rc_on != 0:
        fails.append("B %s did NOT pass with O1 ON (rc=%s)" % (script, rc_on))
    if out_off != out_on:
        fails.append("B %s stdout DIFFERS OFF vs ON -> seam not inert" % script)

# ------------------------------------------------------------------ report
print("=" * 66)
print("GATE: O1 increment-0 -- zero-delta + engine self-test")
print("=" * 66)
if fails:
    for f in fails:
        print("  FAIL: " + f)
    print("\nTOTAL: FAIL")
    sys.exit(1)
print("engine: empty registry clean; linter rejects %d/%d malformed rows; engine live + raise-only"
      % (len(bad_rows), len(bad_rows)))
print("zero-delta: sim_bycode_v2 (ZWSP) + zwj_bom_battery (ZWJ/BOM) bit-identical OFF vs ON, both pass")
print("\nTOTAL: CLEAN -- seam RELATION_PATH_O1_HOOK_v0_1 changes exactly nothing")
sys.exit(0)
