# -*- coding: utf-8 -*-
"""GATE: W4/VS-AXIS (D-W4-VS-AXIS) — variation-selector handling.

VS are category Mn (outside class-138). This axis:
  A SILENCES a legit single selector on a valid base (anti-flood, F-NEW-3): no
    witness, pass — benign emoji must not raise WITNESS_PRESENT.
  B ESCALATES a CHAIN (>=2 adjacent selectors = data carrier) or ORPHAN (selector
    with no valid base) to queue_for_review, with the witness kept.
  C CHAIN = ADJACENCY: two separate emoji each carrying one VS16 are two singles,
    NOT a chain -> silenced.
  D host VS-break (selector on a non-emoji host char) -> ORPHAN -> queue (D9).
  E ADDITIVE: input with no variation selector is unchanged (no new escalation).
Basis: AUTHOR_DECISION_20260726_D-W4-VS-AXIS.
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
se._force_tld_state_for_test(frozenset({"com", "org", "net", "ru"}), False)
_CARDS = rt.load_all_cards()

V = "️"      # VS16 U+FE0F
V15 = "︎"    # VS15 U+FE0E
SUP = "󠄀"   # U+E0100 supplement
HEART = "❤"
PLANE = "✈"

fails = []


def _run(text):
    with contextlib.redirect_stdout(io.StringIO()):
        return rt.analyze(text, _CARDS)


def _wit(r):
    return len(r.get("uncarded_invisibles") or []), r.get("attention_status"), r["effective_action"]


# A. legit single-on-base -> silenced (no witness, pass)
for name, t in [("heart+VS16", "hi " + HEART + V + " there"),
                ("VS15 text-pres", "x " + HEART + V15)]:
    n, a, e = _wit(_run(t))
    if n != 0 or a != "NONE" or e != "pass":
        fails.append("A single-on-base not silenced (%s): uncarded=%d attn=%s eff=%s" % (name, n, a, e))

# C. two separate emoji, each one VS16 -> two singles, NOT a chain -> silenced
n, a, e = _wit(_run(HEART + V + " " + PLANE + V))
if n != 0 or e != "pass":
    fails.append("C multi-emoji wrongly flagged as chain: uncarded=%d eff=%s" % (n, e))

# B. chain / orphan -> witness + queue
for name, t in [("chain VS16x5", "data" + V * 5),
                ("orphan on letter", "pass" + V + "word"),
                ("orphan leading", V + "hi"),
                ("supplement chain", "doc" + SUP * 3)]:
    n, a, e = _wit(_run(t))
    if n == 0 or a != "WITNESS_PRESENT":
        fails.append("B carrier not witnessed (%s): uncarded=%d attn=%s" % (name, n, a))
    if e != "queue_for_review":
        fails.append("B carrier not escalated to queue (%s): eff=%s" % (name, e))

# D. host VS-break -> ORPHAN -> queue
n, a, e = _wit(_run("goog" + V + "le.com"))
if e != "queue_for_review":
    fails.append("D host VS-break not escalated: eff=%s" % e)

# E. additive: no VS -> no new escalation (plain text passes; a real ZWSP host still holds)
if _run("just plain text here")["effective_action"] != "pass":
    fails.append("E plain text no longer passes")
if _run("paypal" + "​" + ".com")["effective_action"] != "hold_pending_review":
    fails.append("E carded ZWSP host verdict changed (should stay hold)")

print("=" * 66)
print("GATE: W4/VS-AXIS — variation selectors (silence legit, escalate carrier)")
print("=" * 66)
if fails:
    for f in fails:
        print("  FAIL: " + f)
    print("\nTOTAL: FAIL")
    sys.exit(1)
print("A legit single-on-base silenced (no witness, pass) — flood fixed")
print("B chain/orphan -> witness + queue; C multi-emoji != chain; D host-break -> queue")
print("E additive: non-VS inputs unchanged")
print("\nTOTAL: CLEAN")
sys.exit(0)
