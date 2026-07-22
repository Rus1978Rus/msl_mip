# -*- coding: utf-8 -*-
"""GATE: a combining mark must not silence a carded invisible host-break.

MEASURED hole: a single combining mark (accent) anywhere in a host cut the positive domain
scan -> the context fell to FREE_TEXT -> a CARDED invisible host-break (ZWSP/ZWJ/BOM) was
gated to NONE and, being carded, never reached the uncarded witness either -> a reliable
HOLD became a TRUE silent pass. The composition is realistic: accents are valid in IDN
domains, so an attacker's phishing host can legitimately carry one.

Fix: combining marks (Mn/Mc/Me) are stripped for the RECONSTRUCTION shape checks (mirroring
_strip_label_invisibles) -- the base letters + TLD still form the domain, so the carded
invisible is seen as an in-host break. The text is never mutated and it is a no-op when no
mark is present (the verified batteries stay bit-identical).

  A ATTACK CLOSED -- each carded invisible + a combining mark in the host -> hold.
  B NO REGRESSION -- baseline host-break still hold; a legit accented domain with NO
    invisible still passes (nothing to flag); token / leading-padding cases unchanged.
Basis: measured 2026-07 composition attack; fix in sequence_engine._strip_combining_marks.
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
se._force_tld_state_for_test(frozenset({"com", "org", "net", "ru", "io", "dev", "xn--p1ai"}), False)
CARDS = rt.load_all_cards()

ZWSP = "​"
ZWJ = "‍"
BOM = "﻿"
ACUTE = "́"        # combining acute (Mn)
DEVA_AA = "ा"      # Devanagari vowel sign AA (Mc, spacing combining mark)

fails = []


def eff(text):
    with contextlib.redirect_stdout(io.StringIO()):
        return rt.analyze(text, CARDS)["effective_action"]


# ------------------------------------------------------- A ATTACK CLOSED
for name, inv in (("ZWSP", ZWSP), ("ZWJ", ZWJ), ("BOM", BOM)):
    # a real in-host break of the carded invisible, with an accent elsewhere in the host
    got = eff("goog" + inv + "le" + ACUTE + ".com")
    if got != "hold_pending_review":
        fails.append("A %s + accent-after in host -> %s (want hold)" % (name, got))
    got2 = eff("goo" + ACUTE + "g" + inv + "le.com")   # accent BEFORE the invisible
    if got2 != "hold_pending_review":
        fails.append("A %s with accent-before -> %s (want hold)" % (name, got2))
# a spacing combining mark (Mc) must be handled the same as a nonspacing one (Mn)
if eff("goog" + ZWSP + "le" + DEVA_AA + ".com") != "hold_pending_review":
    fails.append("A a spacing combining mark (Mc) still demotes the host-break")

# --------------------------------------------------- B NO REGRESSION
regression = [
    ("baseline host-break stays hold", "goog" + ZWSP + "le.com", "hold_pending_review"),
    ("legit accented domain, NO invisible -> pass", "caf" + ACUTE + "e.com", "pass"),
    ("plain domain -> pass", "google.com", "pass"),
    ("ZWSP in a token stays queue", "bad" + ZWSP + "word", "queue_for_review"),
    ("ZWSP leading padding stays queue", ZWSP + "paypal.com", "queue_for_review"),
    ("ZWSP in email stays queue", "us" + ZWSP + "er@example.com", "queue_for_review"),
    ("clean text passes", "the quick brown fox", "pass"),
]
for label, text, want in regression:
    got = eff(text)
    if got != want:
        fails.append("B REGRESSION [%s]: %s (want %s)" % (label, got, want))

print("=" * 66)
print("GATE: combining mark must not silence a carded invisible host-break")
print("=" * 66)
if fails:
    for f in fails:
        print("  FAIL: " + f)
    print("\nTOTAL: FAIL")
    sys.exit(1)
print("A attack closed: ZWSP/ZWJ/BOM + a combining mark (Mn and Mc) in the host -> hold")
print("B no regression: baseline hold; legit accented domain (no invisible) passes; token/pad/email/clean unchanged")
print("\nTOTAL: CLEAN -- one accent no longer turns a host-break into a silent pass")
sys.exit(0)
