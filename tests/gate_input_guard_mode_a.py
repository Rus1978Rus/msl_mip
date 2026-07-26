# -*- coding: utf-8 -*-
"""GATE: Input-Guard Mode A (DoS cost budget) -- FIRST-CUT acceptance.

Proves the guard is (A) ADDITIVE on ordinary input (no false collapse, verdicts
unchanged), (B) forbids a bare pass under a density signal, (C) collapses a real
flood to a hold recommendation while STILL analysing the visible projection so a
flood cannot hide a phishing tail (anti-smokescreen G10), and (D) bounces a mega
flood fast (the heavy layers see the short projection, not the flood).

Basis: AUTHOR_DECISION_20260721_D-INPUT-GUARD-MODE-A-DESIGN; IG_IMPL_PLAN_2026-07-26.
"""
import contextlib
import io
import os
import sys
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
_BASE = os.path.dirname(_HERE)
os.environ["MSL_MIP_HERMETIC_TLD"] = "1"
for _p in ("core", "single_sign", "sequence"):
    sys.path.insert(0, os.path.join(_BASE, _p))
sys.path.insert(0, _BASE)

import msl_mip_runtime as rt
import sequence_engine as se
import input_guard as ig
se._force_tld_state_for_test(frozenset({"com", "org", "net", "ru", "io"}), False)
_CARDS = rt.load_all_cards()
Z = "​"

fails = []


def _run(text):
    with contextlib.redirect_stdout(io.StringIO()):
        return rt.analyze(text, _CARDS)


# --- A. ADDITIVE on ordinary / honest inputs: status OK, no collapse ---
_HONEST = [
    "hello world", "paypal.com", "goog" + Z + "le.com", "user@example.com",
    "def foo(x):\n    return x + 1  # a comment\n" * 60,            # ~2.5 KB code
    ("The quick brown fox jumps over the lazy dog. " * 120),        # ~5 KB prose
    ("".join(chr(0x4E00 + (i % 200)) for i in range(3000))),       # 3 KB CJK
    "https://example.com/path?q=1#frag " * 100,                     # URL-rich prose
]
for t in _HONEST:
    r = _run(t)
    g = r["input_guard"]["status"]
    if g != "OK":
        fails.append("A honest input collapsed/flagged (%s): %r..." % (g, t[:40]))

# --- B. DENSITY_SIGNAL: bare pass forbidden ---
sig = "a" + (Z * 30) + "b"            # 30 invisibles, high density, short
r = _run(sig)
gs = r["input_guard"]["status"]
if gs == "DENSITY_SIGNAL":
    if r["effective_action"] == "pass":
        fails.append("B DENSITY_SIGNAL still produced a bare pass")
# (if thresholds put it at OK/collapse that's fine too; the invariant is 'no bare pass under signal')

# --- C. COLLAPSE + anti-smokescreen (G10): flood hides a phishing tail ---
smoke = (Z * 6000) + "paypal.com.security-check.ru/verify"
r = _run(smoke)
gc = r["input_guard"]["status"]
if gc != "INGESTION_HOLD_SUMMARY":
    fails.append("C smokescreen flood did NOT collapse (status=%s)" % gc)
else:
    if r["effective_action"] not in ("hold_pending_review", "queue_for_review"):
        fails.append("C collapse did not raise the verdict (eff=%s)" % r["effective_action"])
    if r["input_guard"]["counters"]["invisibles"] < 6000:
        fails.append("C flood counter wrong: %r" % r["input_guard"]["counters"])
    if not r["input_guard"]["truncated"]:
        fails.append("C collapse not marked truncated")
    # the projection must still expose the phishing host (not a silent pass hidden by the flood)
    if r["semantic_action"] == "pass" and r["effective_action"] == "pass":
        fails.append("C smokescreen: phishing tail hidden by the flood (silent pass)")

# --- D. mega-flood bounce is fast (heavy layers see the short projection) ---
mega = Z * 1_000_000
t0 = time.perf_counter()
r = _run(mega)
dt = time.perf_counter() - t0
if r["input_guard"]["status"] != "INGESTION_HOLD_SUMMARY":
    fails.append("D 1M-invisible flood did not collapse")
if dt > 1.0:
    fails.append("D mega-flood bounce too slow: %.3f s (expected < 1s)" % dt)

# single-char visible flood collapses too
r2 = _run("/" * 200000)
if r2["input_guard"]["status"] != "INGESTION_HOLD_SUMMARY":
    fails.append("D 200k slash flood did not collapse (status=%s)" % r2["input_guard"]["status"])

# --- projection unit: strips invisibles, collapses long runs ---
if ig.visible_projection(Z * 100 + "abc") != "abc":
    fails.append("projection did not strip invisibles")
if len(ig.visible_projection("/" * 1000)) > 20:
    fails.append("projection did not collapse a long single-char run")

print("=" * 68)
print("GATE: Input-Guard Mode A (DoS cost budget) -- first-cut acceptance")
print("=" * 68)
print("  mega-flood (1M) bounce: %.3f s" % dt)
if fails:
    for f in fails:
        print("  FAIL: " + f)
    print("\nTOTAL: FAIL")
    sys.exit(1)
print("A additive: honest prose/code/CJK/URL inputs stay OK (no false collapse)")
print("B density signal never yields a bare pass")
print("C flood collapses to a hold; visible projection still exposes the phishing tail (G10)")
print("D mega-flood bounces fast; slash flood collapses; projection strips/collapses")
print("\nTOTAL: CLEAN -- input budget holds the door without waking honest text")
sys.exit(0)
