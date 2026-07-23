# -*- coding: utf-8 -*-
"""GATE: schemeless userinfo spoofing brand.tld@other-domain.tld.

MEASURED silent pass (agent #9): "paypal.com@evil.ru" with NO URL scheme passed (effective
pass). The at_matcher gated the userinfo-spoof risk on has_scheme, citing the WHATWG parse
(schemeless -> host is not evil.ru). But the witness-frame target is the HUMAN eye, which
anchors on the brand domain BEFORE the @; the display spoof works regardless of what a URL
parser does. So it is now surfaced when the label before the @ is a REAL brand domain (last
label a registered TLD). A dotted email local part (john.doe) ends in a NON-TLD and stays a
legitimate email -- that TLD guard removes the false positive a shape-only check produced.

  A SPOOF FLAGGED   -- brand.tld@other-domain.tld (with or without a scheme) -> not pass.
  B LEGIT SAFE      -- ordinary emails, incl. dotted local parts, stay pass (no false alarm).
Basis: measured 2026-07; fix in at_matcher (_ends_in_valid_tld). NOTE the LEVEL (hold vs
queue) and the reversal of the WHATWG "not automatic RISK" call are left for the conveyor.
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

fails = []


def eff(text):
    with contextlib.redirect_stdout(io.StringIO()):
        return rt.analyze(text, CARDS)["effective_action"]


# ------------------------------------------------------------- A SPOOF FLAGGED
spoof = [
    "paypal.com@evil.ru",
    "paypal.com@secure-login.ru",
    "http://paypal.com@evil.ru",           # scheme'd case must keep working too
    "google.com@attacker.net",
]
for t in spoof:
    if eff(t) == "pass":
        fails.append("A spoof passed silently: %s" % t)

# --------------------------------------------------------------- B LEGIT SAFE
legit = [
    "john@gmail.com",
    "john.doe@gmail.com",          # dotted local part -- the former false positive
    "first.last@company.org",
    "support@paypal.com",
    "a.b.c@example.com",
    "user_name@example.net",
]
for t in legit:
    got = eff(t)
    if got != "pass":
        fails.append("B legit email did NOT stay pass: %s -> %s" % (t, got))

print("=" * 62)
print("GATE: schemeless userinfo spoofing")
print("=" * 62)
if fails:
    for f in fails:
        print("  FAIL: " + f)
    print("\nTOTAL: FAIL")
    sys.exit(1)
print("A spoof flagged: brand.tld@other.tld (scheme'd and schemeless) no longer passes")
print("B legit safe: plain and dotted-local-part emails stay pass (no false alarm)")
print("\nTOTAL: CLEAN -- the display spoof is surfaced, real emails are not")
sys.exit(0)
