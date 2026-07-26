# -*- coding: utf-8 -*-
"""GATE: the O(n^2)-fix fast context detector is ZERO-DELTA vs the reference.

D-ONSQ-FIX invariant: _detect_context_at (fast, per-token facts cache) MUST return
EXACTLY what _detect_context_at_reference (the original per-offset oracle) returns,
for every input and every offset. This gate is the correctness proof for the fix.

Two layers:
  A UNIT DIFFERENTIAL — for a broad corpus x several mask alphabets x EVERY offset,
    assert fast(text, off, mask) == reference(text, off, mask). This is the tight
    loop that catches a sweep mistake at the exact offset it happens.
  B FULL-ANALYZE — a handful of end-to-end analyze() runs compared fast vs
    reference (MSL_MIP_ONSQ_REFERENCE=1) on the serialized report, so any
    downstream effect of a context delta is caught too.

Basis: AUTHOR_DECISION_20260726_D-ONSQ-FIX; CONVEYOR_PACKET_ONSQ_FIX_2026-07-26.
"""
import io
import contextlib
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_BASE = os.path.dirname(_HERE)
os.environ["MSL_MIP_HERMETIC_TLD"] = "1"
for _p in ("core", "single_sign", "sequence"):
    sys.path.insert(0, os.path.join(_BASE, _p))
sys.path.insert(0, _BASE)

import sequence_engine as se
se._force_tld_state_for_test(frozenset({"com", "org", "net", "ru", "io", "co", "xn--p1ai"}), False)

Z = "​"   # ZWSP
J = "‍"   # ZWJ
B = "﻿"   # BOM
S = "／"   # fullwidth solidus
V = "️"   # VS16 (Mn, residual invisible)
FWDOT = "．"

# ---- corpus: exercise every branch of the reference ----
_CORPUS = [
    # bare host, in-label / dot-adjacent / leading / trailing masks
    "goog{m}le.com", "paypal{m}.com", "{m}paypal.com", "paypal.com{m}",
    "pay{m}pal.com{m}.evil.com", "www.example.com{m}.evil.com",
    # scheme / URL components
    "http://goog{m}le.com/path", "http://user{m}@host.com", "https://a.com/pa{m}th",
    "http://a.com/p?q{m}=1", "http://a.com/p#fr{m}ag", "http://user{m}name@paypal{m}.com/x",
    "ftp://x.com{m}?a", "http://a.com{m}", "scheme://{m}",
    # email
    "us{m}er@example.com", "john.doe{m}@company.com", "a@b{m}.com",
    # path / free-text / byte-exact
    "readme.md{m}x", "#goog{m}le.com", "bad{m}word", "user{m}name", "hello {m}world",
    "just some {m}prose here", "{m}", "a{m}b",
    # fullwidth / ideographic dots + fullwidth solidus mask
    "goog{m}le{fw}com", "paypal{m}。com", "a{m}b｡com",
    # IDN / punycode / degraded-ish (Cyrillic via chr() to keep this file EN-only)
    chr(0x43F) + chr(0x430) + "{m}" + chr(0x440) + "." + chr(0x440) + chr(0x444),
    "xn--80a{m}k.xn--p1ai",
    # multi-mask floods (small — the gate checks correctness, not speed)
    "a{m}a{m}a{m}a{m}.com", ("x{m}" * 8) + "y", ("{m}" * 5) + "paypal.com",
    # combining marks + residual invisibles interleaved
    "goog{m}lé.com", "pay{m}️pal.com", "a{m}‍b.com",
    # wrappers, structural stops, labels near 63/64
    "(paypal{m}.com)", "*goog{m}le.com*", "\"a{m}.com\"", "/goog{m}le.com",
    "@goog{m}le.com", ("a" * 60) + "{m}b.com", ("a" * 63) + "{m}.com",
    # long-ish label + dots sequence
    "a.b.c{m}.d.com", "x{m}...com", "..{m}..", "a{m}.", ".{m}a",
]

_MASKS = [Z, J, B, S]


def _mask_variants(tmpl):
    """Expand {m}/{fw} with each mask; return (text, mask_alphabet) pairs."""
    out = []
    for m in _MASKS:
        if "{m}" not in tmpl:
            continue
        text = tmpl.replace("{m}", m).replace("{fw}", FWDOT)
        out.append((text, frozenset({m})))
        # also a multi-mask alphabet run so _demask strips several kinds
        out.append((tmpl.replace("{m}", m).replace("{fw}", FWDOT), frozenset({Z, J, B, S})))
    return out


fails = []
checks = 0
for tmpl in _CORPUS:
    for text, alphabet in _mask_variants(tmpl):
        for off in range(len(text)):
            ref = se._detect_context_at_reference(text, off, alphabet)
            fast = se._detect_context_at(text, off, alphabet)
            checks += 1
            if ref != fast:
                fails.append("A off=%d ref=%s fast=%s text=%r mask=%r"
                             % (off, ref, fast, text, "".join(sorted(alphabet))))
                if len(fails) > 40:
                    break
        if len(fails) > 40:
            break
    if len(fails) > 40:
        break

# ---- B: full-analyze differential (fast vs reference via env) ----
import msl_mip_runtime as rt
_CARDS = rt.load_all_cards()


def _report(text):
    with contextlib.redirect_stdout(io.StringIO()):
        rep = rt.analyze(text, _CARDS)
    # serialize the decision-bearing surface deterministically
    so = rep.get("sequence_output")
    rv = getattr(so, "relation_verdicts", []) if so else []
    return (rep.get("semantic_action"), rep.get("effective_action"),
            rep.get("attention_status"),
            tuple((v.get("relation_type"), v.get("runtime_role"), v.get("at_offset"),
                   v.get("detected_context"), v.get("risk_level")) for v in rv),
            tuple(sorted((u.get("codepoint"), u.get("at_offset"))
                         for u in (rep.get("uncarded_invisibles") or []))))


_FULL = ["goog" + Z + "le.com", "http://user" + Z + "@paypal" + Z + ".com/x",
         "john.doe" + Z + "@company.com", "pay" + B + "pal.com" + B + ".evil.com",
         ("a" + Z) * 12, "readme.md" + Z + "x", "*goog" + S + "le.com*",
         chr(0x43F) + chr(0x430) + Z + chr(0x440) + "." + chr(0x440) + chr(0x444)]
for text in _FULL:
    os.environ["MSL_MIP_ONSQ_REFERENCE"] = "1"
    ref = _report(text)
    os.environ["MSL_MIP_ONSQ_REFERENCE"] = "0"
    fast = _report(text)
    checks += 1
    if ref != fast:
        fails.append("B analyze delta text=%r\n   ref =%r\n   fast=%r" % (text, ref, fast))
os.environ.pop("MSL_MIP_ONSQ_REFERENCE", None)

print("=" * 70)
print("GATE: O(n^2)-fix fast context detector == reference (ZERO-DELTA)")
print("=" * 70)
print("  checks run: %d" % checks)
if fails:
    for f in fails[:40]:
        print("  FAIL: " + f)
    print("\nTOTAL: FAIL (%d mismatches)" % len(fails))
    sys.exit(1)
print("  A unit differential: fast == reference for every corpus offset")
print("  B full-analyze: report identical fast vs reference")
print("\nTOTAL: CLEAN -- zero-delta proven; fast path safe to ship")
sys.exit(0)
