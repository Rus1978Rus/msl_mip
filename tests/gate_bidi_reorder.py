# -*- coding: utf-8 -*-
"""GATE: bidi reordering axis, phase 1 (D-BIDI-REORDER D1-D9, spec B1-B8).

  A TARGET DELTAS: the measured spoof in both forms -- unbalanced AND BALANCED (the
    balanced one is the point of the front: it reorders identically, so a balance
    trigger would miss the careful attacker) -- plus the LRO analogue -> queue.
  B FP GUARDS (the front's price; all already pass today, so these watch for
    REGRESSION): the panel's three guards, Hebrew/Arabic marks x1..x20, balanced
    isolates. Marks and isolates must never open the valve.
  C NO-OP AND STRUCTURE traps: empty scope, scope of exactly 1 char, embedding,
    unmatched isolate (closed by end of paragraph), orphan PDF -> no signal.
  D ATTRIBUTION (D8, mechanises the S1 trap): the Trojan-Source pair. WITH the RLO the
    bidi finding must exist independently; WITHOUT it the finding must disappear while
    the verdict stays queue from SOLIDUS. Counting someone else's escalation as a bidi
    catch is the failure this cell exists to prevent.
  E ANTI-RETRANSMISSION (spec B3): the printed report contains ZERO of the 12 control
    codepoints -- otherwise the report itself becomes a carrier of the reordering.
  F ADDITIVE: host stays queue via D-INV-GEN with bidi attributed alongside; carded
    ZWSP still holds; raw text preserved; other axes unchanged.
All non-ASCII literals via chr() (english-only gate).
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
import bidi_axis as ba
_CARDS = rt.load_all_cards()
se._force_tld_state_for_test(
    frozenset({"com", "org", "net", "ru", "xn--p1ai"}), False)

RLO, LRO, PDF = chr(0x202E), chr(0x202D), chr(0x202C)
RLE, RLM, LRM = chr(0x202B), chr(0x200F), chr(0x200E)
RLI, PDI = chr(0x2067), chr(0x2069)
Z = chr(0x200B)
QUEUE = "queue_for_review"
HEB = "".join(chr(c) for c in (0x5E9, 0x5DC, 0x5D5, 0x5DD))


def _run(text):
    with contextlib.redirect_stdout(io.StringIO()):
        return rt.analyze(text, _CARDS)


def _eff(text):
    return _run(text)["effective_action"]


fails = []

# A. Target deltas -- all three were measured as pass before this axis.
for name, t in [
        ("unbalanced spoof", "invoice" + RLO + "gpj.exe"),
        ("spoof inside a phrase", "open invoice" + RLO + "gpj.exe now"),
        ("BALANCED spoof (the point of the front)",
         "invoice" + RLO + "gpj" + PDF + ".exe"),
        ("unbalanced override in prose", "text " + RLO + "reversed"),
        ("LRO analogue", "file" + LRO + "txt.exe"),
        ("override then paragraph break", "x" + RLO + "ab\nclean line")]:
    r = _run(t)
    if r["effective_action"] != QUEUE:
        fails.append("A %s: eff=%s want=queue" % (name, r["effective_action"]))
    if not r["bidi_axis"]["contributed"]:
        fails.append("A %s: axis did not attribute its own contribution" % name)
    if not any(f["finding"] == "REORDERING_CAPABLE"
               for f in r["bidi_axis"]["findings"]):
        fails.append("A %s: no REORDERING_CAPABLE finding" % name)

# B. FP guards -- the price of the front. Must stay pass, and the axis must be silent.
for name, t in [
        ("panel guard: isolate protecting a range",
         "cost " + RLI + HEB + PDI + " - 123"),
        ("panel guard: RLM joining a number range", HEB + " 123" + RLM + "-456"),
        ("panel guard: email then RLM then Hebrew",
         "user@example.com" + RLM + " " + HEB),
        ("Hebrew + RLM x1", HEB + " " + RLM + " " + HEB),
        ("Hebrew + RLM x5", (HEB + RLM + " ") * 5),
        ("marks x20 mixed document", (RLM + HEB + " " + LRM + "abc ") * 10),
        ("balanced isolates", "name " + RLI + "value" + PDI + " end"),
        ("plain prose", "no bidi here")]:
    r = _run(t)
    if r["effective_action"] != "pass":
        fails.append("B %s: eff=%s want=pass" % (name, r["effective_action"]))
    if r["bidi_axis"]["contributed"]:
        fails.append("B %s: axis wrongly contributed" % name)

# Marks must be collapsed in the axis field (D7), not one entry per control.
r = _run((RLM + HEB + " " + LRM + "abc ") * 10)
ms = r["bidi_axis"]["marks_summary"]
if not ms.get("collapsed") or ms.get("count") != 20:
    fails.append("B marks not collapsed correctly: %s" % ms)
if r["bidi_axis"]["findings"]:
    fails.append("B marks produced findings")

# C. No-op and structural traps.
for name, t in [
        ("empty scope", "a" + RLO + PDF + "b"),
        ("scope of exactly one char", "x" + RLO + "y" + PDF + "z"),
        ("embedding over Latin", "abc" + RLE + "xyz" + PDF + "def"),
        ("unmatched isolate (closed by paragraph end)", "name " + RLI + "value end"),
        ("orphan PDF", "a" + PDF + "b"),
        ("orphan PDI", "a" + PDI + "b")]:
    r = _run(t)
    if r["effective_action"] != "pass" or r["bidi_axis"]["contributed"]:
        fails.append("C %s: eff=%s contributed=%s want pass/False"
                     % (name, r["effective_action"], r["bidi_axis"]["contributed"]))

# D. Attribution pair -- the S1 trap, mechanised.
with_rlo = "if (admin) { /* " + RLO + " } else { */ grant(); }"
without = "if (admin) { /*   } else { */ grant(); }"
ra, rb = _run(with_rlo), _run(without)
if ra["effective_action"] != QUEUE or rb["effective_action"] != QUEUE:
    fails.append("D both Trojan-Source variants should stay queue (SOLIDUS)")
if not ra["bidi_axis"]["contributed"]:
    fails.append("D with RLO: bidi must contribute independently")
if rb["bidi_axis"]["contributed"]:
    fails.append("D without RLO: bidi must NOT contribute (would steal SOLIDUS's catch)")

# E. Anti-retransmission: the printed report must carry none of the 12 controls.
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    rt.print_report(_run("invoice" + RLO + "gpj" + PDF + ".exe"))
printed = buf.getvalue()
leaked = sorted({"U+%04X" % ord(c) for c in printed if ord(c) in ba.ALL_CONTROLS})
if leaked:
    fails.append("E report leaked bidi controls: %s" % leaked)
if "REORDERING_CAPABLE" not in printed or "NOT computed" not in printed:
    fails.append("E report must state the finding and the phase-1 limit")

# F. Additive.
r = _run("goog" + RLO + "le.com")
if r["effective_action"] != QUEUE:
    fails.append("F host case changed level")
if not r["bidi_axis"]["contributed"]:
    fails.append("F host case: bidi should be attributed alongside D-INV-GEN")
if _eff("paypal" + Z + ".com") != "hold_pending_review":
    fails.append("F carded ZWSP host verdict changed")
raw = "invoice" + RLO + "gpj.exe"
if _run(raw).get("text") != raw:
    fails.append("F raw input not preserved")

print("=" * 66)
print("GATE: bidi reordering axis, phase 1 (override scope, marks silent)")
print("=" * 66)
if fails:
    for f in fails:
        print("  FAIL: " + f)
    print("\nTOTAL: FAIL")
    sys.exit(1)
print("A target deltas: unbalanced AND balanced spoof + LRO + paragraph end -> queue")
print("B FP guards: panel's three + marks x1/x5/x20 + isolates -> pass, marks collapsed")
print("C no-op traps: empty scope, scope=1, embedding, unmatched isolate, orphans -> pass")
print("D attribution: with RLO bidi contributes; without RLO it does not (SOLIDUS keeps")
print("  its catch) -- the S1 trap mechanised")
print("E anti-retransmission: zero of the 12 controls in the printed report")
print("F additive: host unchanged with bidi attributed, carded ZWSP holds, raw kept")
print("\nTOTAL: CLEAN")
sys.exit(0)
