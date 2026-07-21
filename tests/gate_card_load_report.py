# -*- coding: utf-8 -*-
"""GATE: structured card-load report.

A card that fails to load drops a DETECTOR -- a silent-pass risk (a threat becomes
invisible to that subsystem). load_cards_report() must surface that in a STRUCTURED
form (not only a stdout warning), so a programmatic caller can refuse to run degraded.

Checks:
  1. Healthy load: degraded is False, loaded == expected == len(CARD_FILENAMES) > 0,
     no warnings, and the card list matches load_all_cards().
  2. MISSING card: a bogus filename is reported {status: MISSING}, degraded True, and the
     real cards still load.
  3. FAILED card: a card whose loader raises is reported {status: FAILED}, degraded True.
Basis: full-project audit finding (card load was warning-only / stdout).
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_BASE = os.path.dirname(_HERE)
for _p in ("core", "single_sign", "sequence"):
    sys.path.insert(0, os.path.join(_BASE, _p))
sys.path.insert(0, _BASE)

import msl_mip_runtime as rt

fails = []

# 1. Healthy load.
rep = rt.load_cards_report()
expected = len(rt.CARD_FILENAMES)
if rep["degraded"]:
    fails.append("1 healthy load reported degraded=True: %s" % rep["load_warnings"])
if rep["loaded"] != expected or rep["expected"] != expected or expected == 0:
    fails.append("1 loaded=%s expected=%s (CARD_FILENAMES=%d)" % (rep["loaded"], rep["expected"], expected))
if rep["load_warnings"]:
    fails.append("1 healthy load had warnings: %s" % rep["load_warnings"])
if len(rep["cards"]) != len(rt.load_all_cards()):
    fails.append("1 load_cards_report cards != load_all_cards cards")

# 2. MISSING card -> structured warning, not a silent drop.
saved = list(rt.CARD_FILENAMES)
try:
    rt.CARD_FILENAMES.append("SIGN_CORE_CARD_DOES_NOT_EXIST_UZZZZ.md")
    rep2 = rt.load_cards_report()
    if not rep2["degraded"]:
        fails.append("2 missing card did not set degraded=True")
    miss = [w for w in rep2["load_warnings"] if w["status"] == "MISSING"
            and "DOES_NOT_EXIST" in w["card"]]
    if not miss:
        fails.append("2 missing card not reported as {status: MISSING}")
    if rep2["loaded"] != expected:  # the real cards still loaded
        fails.append("2 real cards did not still load (loaded=%s, want %s)" % (rep2["loaded"], expected))
finally:
    rt.CARD_FILENAMES[:] = saved

# 3. FAILED card -> the loader raises; must be reported as {status: FAILED}, not crash.
_real_load = rt.load_card
_calls = {"n": 0}
def _failing_load(path):
    _calls["n"] += 1
    if _calls["n"] == 1:
        raise ValueError("simulated malformed card")
    return _real_load(path)
rt.load_card = _failing_load
try:
    rep3 = rt.load_cards_report()
    if not rep3["degraded"]:
        fails.append("3 failed card did not set degraded=True")
    failed = [w for w in rep3["load_warnings"] if w["status"] == "FAILED"]
    if not failed:
        fails.append("3 failed card not reported as {status: FAILED}")
    if rep3["loaded"] != expected - 1:
        fails.append("3 expected exactly one card to drop (loaded=%s, want %s)" % (rep3["loaded"], expected - 1))
finally:
    rt.load_card = _real_load

print("=" * 60)
print("GATE: structured card-load report")
print("=" * 60)
if fails:
    for f in fails:
        print("  FAIL: " + f)
    print("\nTOTAL: FAIL")
    sys.exit(1)
print("healthy load clean (%d/%d cards); MISSING and FAILED cards surface as structured, degraded=True"
      % (expected, expected))
print("\nTOTAL: CLEAN -- a dropped detector is visible, not a silent stdout-only warning")
sys.exit(0)
