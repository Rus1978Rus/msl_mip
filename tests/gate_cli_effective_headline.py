# -*- coding: utf-8 -*-
"""GATE: the CLI FINAL VERDICT headline reflects the EFFECTIVE (actionable) action.

Finding W2 (Kimi methodological audit 2026-07-26, reproduced by measurement): print_report
printed only semantic_action on the FINAL VERDICT line whenever integrity_status was OK. An
independent safeguard (e.g. D-INV-GEN) can raise effective ABOVE semantic WITHOUT an
integrity VIOLATION (status stays OK) -- so an uncarded host-break invisible showed
"FINAL VERDICT: PASS" while the effective action was queue/hold. The human reads that line;
it must show the actionable verdict.

  A DIVERGENT case -- goog<U+2062>le.com: semantic=pass but effective=queue_for_review.
    The headline must read the EFFECTIVE action, and must NOT read "FINAL VERDICT: PASS".
    The un-raised main path is named underneath so nothing is hidden.
  B AGREEING case -- a clean string: headline shows the (single) action and prints NO
    "main path" note, because there is no divergence to disclose.
Basis: finding W2; AUTHOR_DECISION_20260722_D-INV-GEN; witness-frame (effective is the
  actionable field the human must see).
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
CARDS = rt.load_all_cards()

fails = []


def _report_lines(text):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rep = rt.analyze(text, CARDS)
        rt.print_report(rep)
    return rep, buf.getvalue().splitlines()


def _headline(lines):
    for ln in lines:
        if ln.startswith("FINAL VERDICT:"):
            return ln
    return None


# --------------------------------------------------------------------- A DIVERGENT case
rep, lines = _report_lines("goog" + "⁢" + "le.com")
if rep.get("semantic_action") != "pass" or rep.get("effective_action") != "queue_for_review":
    fails.append("A precondition changed: semantic=%r effective=%r (expected pass / "
                 "queue_for_review) -- re-measure before trusting the headline check"
                 % (rep.get("semantic_action"), rep.get("effective_action")))
else:
    head = _headline(lines)
    if head is None:
        fails.append("A no FINAL VERDICT line in the report")
    else:
        if "QUEUE_FOR_REVIEW" not in head:
            fails.append("A headline does not show the effective action: %r" % head)
        if "PASS" in head:
            fails.append("A headline still shows the un-raised semantic PASS: %r" % head)
    if not any("main path" in ln and "PASS" in ln for ln in lines):
        fails.append("A the un-raised main path (PASS) is not disclosed underneath")

# ---------------------------------------------------------------------- B AGREEING case
rep2, lines2 = _report_lines("hello world")
if rep2.get("semantic_action") != rep2.get("effective_action"):
    fails.append("B precondition changed: a clean string diverged "
                 "(semantic=%r effective=%r)" % (rep2.get("semantic_action"),
                                                  rep2.get("effective_action")))
else:
    head2 = _headline(lines2)
    if head2 is None:
        fails.append("B no FINAL VERDICT line for the clean string")
    elif rep2["effective_action"].upper() not in head2:
        fails.append("B headline does not show the action for an agreeing case: %r" % head2)
    if any("main path" in ln for ln in lines2):
        fails.append("B a 'main path' note printed although there was no divergence")

print("=" * 68)
print("GATE: CLI FINAL VERDICT headline shows the effective (actionable) action")
print("=" * 68)
if fails:
    for f in fails:
        print("  FAIL: " + f)
    print("\nTOTAL: FAIL")
    sys.exit(1)
print("A divergent (goog<U+2062>le.com): headline QUEUE_FOR_REVIEW, not PASS; main path disclosed")
print("B agreeing (clean string): headline shows the single action, no 'main path' note")
print("\nTOTAL: CLEAN -- the human reads the actionable verdict, no hidden escalation")
sys.exit(0)
