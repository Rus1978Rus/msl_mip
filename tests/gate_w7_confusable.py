# -*- coding: utf-8 -*-
"""GATE: W7 visible-confusable axis (D-W7-CONFUSABLE D1-D8, SPEC B5 battery).

  A TIER 1 (generic mixed-script/lookalike confusable in a host label) -> queue.
  B SEPARATOR axis (fullwidth/ideographic/halfwidth dots) -> queue; hold on
    protected-label collision (event before canonicalisation, S4.1).
  C LEGIT controls -> pass (IDN, CJK, hyphenated Latin, science prose, plain prose,
    email local-part, plain ASCII brands).
  D MARKER cells (pinned expectations): mono-script pseudo-brand -> tier-1 silent
    (R1); palochka+target -> STILL no hold (R1b, measured UTS#39 divergence
    U+04CF -> 'i'); 4 deferred mappings -> silent (R2); tier-2 collision works on
    a measured-colliding pair (coco); exact ASCII target -> no hold.
  E DEGRADED registry -> witness kept, verdict never raised (W5 parity).
  F ADDITIVE: carded ZWSP host still holds; report field present with status OK.
Basis: AUTHOR_DECISION_20260804_D-W7-CONFUSABLE + SPEC_20260804_W7_BLOCKERS_B1-B8.
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
_CARDS = rt.load_all_cards()


def _run(text, targets=None):
    with contextlib.redirect_stdout(io.StringIO()):
        return rt.analyze(text, _CARDS, protected_targets=targets)


def _eff(text, targets=None):
    return _run(text, targets)["effective_action"]


def _cyr(*cps):
    return "".join(chr(c) for c in cps)


CYR_A, CYR_O, CYR_R, CYR_S, CYR_E, CYR_B = (chr(c) for c in
                                            (0x430, 0x43E, 0x440, 0x441, 0x435, 0x431))
GRK_A, GRK_O = chr(0x3B1), chr(0x3BF)
ARM_O = chr(0x585)
ROMAN_C = chr(0x216D)
PALOCHKA = chr(0x4CF)
FW_DOT, IDEO_DOT, HW_DOT = chr(0xFF0E), chr(0x3002), chr(0xFF61)
Z = chr(0x200B)
APPLE_SPOOF = _cyr(0x430, 0x440, 0x440, 0x4CF, 0x435)       # a r r palochka e
COCO_SPOOF = CYR_S + CYR_O + CYR_S + CYR_O                   # skeleton == 'coco'
JAPANESE = _cyr(0x6771, 0x4EAC, 0x30BF, 0x30EF, 0x30FC)     # Tokyo tower, Han+Kana
KOREAN = _cyr(0xD55C, 0xAD6D, 0xC0AC, 0xC774, 0xD2B8)       # Hangul
RU_PROSE = _cyr(0x43F, 0x440, 0x43E, 0x441, 0x442, 0x43E) + " " + \
    _cyr(0x442, 0x435, 0x43A, 0x441, 0x442)

fails = []
se._force_tld_state_for_test(
    frozenset({"com", "org", "net", "ru", "xn--p1ai"}), False)

# A. Tier 1 positives -> queue.
for name, t in [
        ("cyr-a paypal", "p" + CYR_A + "ypal.com"),
        ("cyr-o google", "g" + CYR_O + "ogle.com"),
        ("greek-o google", "g" + GRK_O + "ogle.com"),
        ("armenian-o google", "g" + ARM_O + "ogle.com"),
        ("roman-numeral coinbase", ROMAN_C + "oinbase.com"),
        ("mixed-case spoof", "P" + CYR_A + "YPAL.com"),
        ("punycode decoded", "xn--pypal-4ve.com"),
        ("userinfo bait", "p" + CYR_A + "ypal.com@evil.com"),
        ("cyr label + one latin", CYR_S + CYR_B + CYR_E + CYR_R + "a.com"),
        ("science host (pinned residual R3)", GRK_A + "-testing.com")]:
    got = _eff(t)
    if got != "queue_for_review":
        fails.append("A %s: eff=%s want=queue_for_review" % (name, got))

# B. Separator axis.
for name, t in [("fullwidth dot", "paypal" + FW_DOT + "com"),
                ("ideographic dot", "paypal" + IDEO_DOT + "com"),
                ("halfwidth dot", "paypal" + HW_DOT + "com")]:
    got = _eff(t)
    if got != "queue_for_review":
        fails.append("B %s: eff=%s want=queue_for_review" % (name, got))
got = _eff("paypal" + FW_DOT + "com", {"paypal"})
if got != "hold_pending_review":
    fails.append("B fullwidth+target: eff=%s want=hold" % got)

# C. Legit controls -> pass.
for name, t in [
        ("ascii paypal", "paypal.com"),
        ("ascii PayPal", "PayPal.com"),
        ("pure cyrillic IDN", "sber." + CYR_R + chr(0x444)),
        ("japanese Han+Kana", JAPANESE + ".com"),
        ("korean Hangul", KOREAN + ".com"),
        ("hyphen latin x-men", "x-men.com"),
        ("hyphen latin e-shop", "e-shop.ru"),
        ("science prose", GRK_A + "-testing is fine"),
        ("beta-cell prose", chr(0x3B2) + "-cell study"),
        ("russian prose", RU_PROSE),
        ("email greek local", GRK_A + "-user@lab.org")]:
    got = _eff(t)
    if got != "pass":
        fails.append("C %s: eff=%s want=pass" % (name, got))

# D. Marker cells (pinned).
if _eff(APPLE_SPOOF + ".com") != "pass":
    fails.append("D R1 mono-script tier-1 should be silent")
if _eff(APPLE_SPOOF + ".com", {"apple"}) != "pass":
    fails.append("D R1b palochka+target must NOT hold (U+04CF->'i' measured)")
for name, t in [("deferred omega", chr(0x461) + "eb.com"),
                ("deferred eta", chr(0x3B7) + "ews.com"),
                ("deferred armenian ayb", chr(0x561) + "eb.com"),
                ("deferred armenian seh", chr(0x57D) + "ber.com")]:
    got = _eff(t)
    if got != "pass":
        fails.append("D R2 %s should be silent: eff=%s" % (name, got))
if _eff(COCO_SPOOF + ".com", {"coco"}) != "hold_pending_review":
    fails.append("D tier-2 collision (coco) should hold")
if _eff(COCO_SPOOF + ".com") != "pass":
    fails.append("D whole-script coco without target should pass (R1)")
if _eff("paypal.com", {"paypal"}) != "pass":
    fails.append("D exact ASCII target must not hold")
if _eff("p" + CYR_A + "ypal.com", {"paypal"}) != "hold_pending_review":
    fails.append("D tier-2 mixed-script paypal should hold")
if _eff("xn--pypal-4ve.com", {"paypal"}) != "hold_pending_review":
    fails.append("D tier-2 punycode paypal should hold")

# E. Degraded registry: witness kept, verdict not raised.
se._force_tld_state_for_test(frozenset(), True)
r = _run("p" + CYR_A + "ypal.com")
if r["effective_action"] != "pass":
    fails.append("E degraded must not escalate: eff=%s" % r["effective_action"])
if not r["confusable_axis"]["records"]:
    fails.append("E degraded must keep witness records")
se._force_tld_state_for_test(
    frozenset({"com", "org", "net", "ru", "xn--p1ai"}), False)

# F. Additive: carded path untouched; report field structured.
if _eff("paypal" + Z + ".com") != "hold_pending_review":
    fails.append("F carded ZWSP host verdict changed")
r = _run("p" + CYR_A + "ypal.com")
cf = r.get("confusable_axis")
if not cf or cf.get("status") != "OK" or not cf.get("witness"):
    fails.append("F confusable_axis field missing/empty: %s" % (cf,))
if r.get("text") != "p" + CYR_A + "ypal.com":
    fails.append("F raw input not preserved in report")

print("=" * 66)
print("GATE: W7 visible-confusable axis (tier1/tier2/separator/markers)")
print("=" * 66)
if fails:
    for f in fails:
        print("  FAIL: " + f)
    print("\nTOTAL: FAIL")
    sys.exit(1)
print("A tier-1 mixed-script/lookalike in host label -> queue (10 cells)")
print("B separator lookalikes -> queue; protected collision -> hold")
print("C legit controls -> pass (11 cells incl CJK/IDN/science/prose)")
print("D markers: R1 mono-script silent, R1b palochka no-hold (measured),")
print("   R2 deferred silent, tier-2 collision holds, exact target no-hold")
print("E degraded registry: witness kept, no escalation")
print("F additive: carded ZWSP unchanged, raw text preserved, field structured")
print("\nTOTAL: CLEAN")
sys.exit(0)
