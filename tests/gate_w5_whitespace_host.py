# -*- coding: utf-8 -*-
"""GATE: W5/WHITESPACE-HOST (D-W5-WHITESPACE-HOST) — whitespace-lookalike host-break.

A non-ASCII whitespace (NBSP/NNBSP/...) that breaks a host label is category Zs/Zl/Zp,
outside class-138, so D-INV-GEN misses it. This additive seam escalates it to queue,
reusing the existing whitespace witness-family + _reconstructed_context (ASCII-boundary
removal probe). Host-only; witness kept; carded verdicts unchanged.
  A AUTHORITATIVE: host-break whitespace -> queue (incl dot-adjacent + IDN).
  B LEGIT: prose NBSP / french NNBSP-before-punctuation -> pass (not a domain).
  C DEGRADED policy (D5): under a degraded registry, do NOT escalate (the alphabetic-TLD
    fallback would false-escalate a prose 'Title.<NBSP>Name'); witness kept, verdict unchanged.
  D ADDITIVE: carded ZWSP host still holds; plain text passes.
Basis: AUTHOR_DECISION_20260726_D-W5-WHITESPACE-HOST. All non-ASCII test literals via chr()
(english-only gate).
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
_CARDS = rt.load_all_cards()

NB = chr(0x00A0)      # NBSP
NN = chr(0x202F)      # NARROW NBSP
Z = chr(0x200B)       # ZWSP (carded)
# cyrillic IDN via chr(): "pey<NBSP>pal.rf" in Cyrillic + Cyrillic TLD
IDN = "".join(chr(c) for c in (0x43F, 0x44D, 0x439)) + NB + \
      "".join(chr(c) for c in (0x43F, 0x430, 0x43B)) + "." + chr(0x440) + chr(0x444)
MR = "Mr." + NB + "Smith"
FRENCH = "mot" + NN + ": suite"

fails = []


def _eff(text):
    with contextlib.redirect_stdout(io.StringIO()):
        return rt.analyze(text, _CARDS)["effective_action"]


# A + B: authoritative registry
se._force_tld_state_for_test(frozenset({"com", "org", "net", "ru", "xn--p1ai"}), False)
for name, t, want in [
        ("paypal<NBSP>.com", "paypal" + NB + ".com", "queue_for_review"),
        ("goog<NBSP>le.com", "goog" + NB + "le.com", "queue_for_review"),
        ("IDN cyrillic host", IDN, "queue_for_review"),
        ("Mr.<NBSP>Smith prose", MR, "pass"),
        ("french NNBSP", FRENCH, "pass"),
        ("carded ZWSP host", "paypal" + Z + ".com", "hold_pending_review"),
        ("plain text", "just some words here", "pass")]:
    got = _eff(t)
    if got != want:
        fails.append("A/B authoritative %s: eff=%s want=%s" % (name, got, want))

# C: degraded registry -> no whitespace-host escalation (prose FP avoided)
se._force_tld_state_for_test(frozenset(), True)
for name, t in [("paypal<NBSP>.com degraded", "paypal" + NB + ".com"),
                ("Mr.<NBSP>Smith degraded", MR)]:
    got = _eff(t)
    if got != "pass":
        fails.append("C degraded should not escalate %s: eff=%s" % (name, got))
if _eff("paypal" + Z + ".com") != "hold_pending_review":
    fails.append("C carded ZWSP host verdict changed under degraded")

print("=" * 66)
print("GATE: W5/WHITESPACE-HOST — non-ASCII whitespace host-break")
print("=" * 66)
if fails:
    for f in fails:
        print("  FAIL: " + f)
    print("\nTOTAL: FAIL")
    sys.exit(1)
print("A authoritative host-break (dot-adjacent + IDN) -> queue")
print("B prose NBSP / french NNBSP -> pass")
print("C degraded registry -> no escalation (prose FP avoided); carded ZWSP still holds")
print("\nTOTAL: CLEAN")
sys.exit(0)
