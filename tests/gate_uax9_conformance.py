# -*- coding: utf-8 -*-
"""GATE: UAX#9 conformance (D-BIDI-REORDER phase 2, spec B7).

The round forbade a hand-rolled "strip and compare": an implementation that is not
conformant drifts between versions and between implementations, so its output could not
honestly be shown to a human as "the reference order". This gate is what makes the claim
checkable -- it runs the OFFICIAL Unicode test files for the pinned 16.0.0:

  BidiTest.txt           class sequences x up to 3 paragraph directions = 770241 cases
  BidiCharacterTest.txt  real codepoints incl. bracket pairs (rule N0)  =  91707 cases

Both are pinned by sha256 alongside the runtime tables; a mismatch is fail-visible, not a
silent skip. Levels, the paragraph level, X9-removed positions and the L2 reordering are
all compared, so a regression in any rule surfaces here rather than in a verdict.
"""
import hashlib
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_BASE = os.path.dirname(_HERE)
sys.path.insert(0, os.path.join(_BASE, "core"))

import uax9

_DATA = os.path.join(_BASE, "data", "unicode", "conformance")
PINNED = {
    "BidiTest.txt":
        "93e5eb9d88ca89dcf895f5576486a3363762ad2aa8f2db2fa56fe60cb82b9520",
    "BidiCharacterTest.txt":
        "d04a51a90052dcd71c4e91ee5b3a9d973ee35c12406b5a99875ac8163c8f2804",
}

fails = []


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


for name, want in PINNED.items():
    path = os.path.join(_DATA, name)
    if not os.path.isfile(path):
        fails.append("missing conformance artifact %s" % name)
    elif _sha256(path) != want:
        fails.append("sha256 mismatch for %s" % name)

char_total = char_fail = 0
if not fails:
    with open(os.path.join(_DATA, "BidiCharacterTest.txt"), encoding="utf-8") as f:
        for line in f:
            line = line.split("#", 1)[0].strip()
            if not line:
                continue
            cps, direction, plevel, levels, order = line.split(";")
            text = "".join(chr(int(c, 16)) for c in cps.split())
            d = int(direction)
            char_total += 1
            lv, _ty, got_pl, removed = uax9.resolve_levels(
                uax9.classes_of(text), None if d == 2 else d, text)
            ok = got_pl == int(plevel)
            if ok:
                for i, e in enumerate(levels.split()):
                    if e == "x":
                        if not removed[i]:
                            ok = False
                            break
                    elif removed[i] or lv[i] != int(e):
                        ok = False
                        break
            if ok:
                want_order = [int(x) for x in order.split()] if order.strip() else []
                ok = uax9.reorder(lv, removed) == want_order
            if not ok:
                char_fail += 1
                if char_fail <= 3:
                    fails.append("BidiCharacterTest: %s" % line[:90])

bt_total = bt_fail = 0
if not fails or char_fail:
    levels = order = None
    with open(os.path.join(_DATA, "BidiTest.txt"), encoding="utf-8") as f:
        for line in f:
            line = line.split("#", 1)[0].strip()
            if not line:
                continue
            if line.startswith("@Levels:"):
                levels = line[8:].split()
                continue
            if line.startswith("@Reorder:"):
                order = [int(x) for x in line[9:].split()]
                continue
            types_str, bitset = line.split(";")
            types = types_str.split()
            bits = int(bitset.strip(), 16) if bitset.strip().lower().startswith("0x") \
                else int(bitset.strip())
            for bit, pl in ((1, None), (2, 0), (4, 1)):
                if not bits & bit:
                    continue
                bt_total += 1
                lv, _ty, _pl, removed = uax9.resolve_levels(types, pl, None)
                ok = True
                for i, e in enumerate(levels):
                    if e == "x":
                        if not removed[i]:
                            ok = False
                            break
                    elif removed[i] or lv[i] != int(e):
                        ok = False
                        break
                if ok and uax9.reorder(lv, removed) != order:
                    ok = False
                if not ok:
                    bt_fail += 1
                    if bt_fail <= 3:
                        fails.append("BidiTest: %s ; para=%s" % (types_str.strip(), pl))

print("=" * 66)
print("GATE: UAX#9 conformance (revision 50, Unicode 16.0.0)")
print("=" * 66)
if fails:
    for f in fails[:8]:
        print("  FAIL: " + f)
    print("\nTOTAL: FAIL")
    sys.exit(1)
print("BidiCharacterTest.txt: %d cases, %d failed (brackets/N0 included)"
      % (char_total, char_fail))
print("BidiTest.txt:          %d cases, %d failed" % (bt_total, bt_fail))
print("levels + paragraph level + X9-removed positions + L2 reordering all compared")
print("artifacts sha256-pinned; mismatch is fail-visible")
print("\nTOTAL: CLEAN")
sys.exit(0)
