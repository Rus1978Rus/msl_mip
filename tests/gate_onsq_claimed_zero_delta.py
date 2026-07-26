# -*- coding: utf-8 -*-
"""GATE: the literal-matcher O(m^2)-fix (D-ONSQ-CLAIMED-FIX) is ZERO-DELTA.

Two changes, both proven identical to their reference oracle (forced by env
MSL_MIP_ONSQ2_REFERENCE=1):
  - _find_literal_matches: prefix-max (Fenwick) containment replaces the O(m^2)
    `any(claimed)` scan;
  - _attach_source_offsets: sorted-offsets bisect replaces the O(m*s) nested loop.

The gate compares the FULL decision surface (verdict/effective/attention/relation
verdicts + every SequenceMatch incl. source_sign_offsets/ordering) fast vs
reference over a targeted corpus + a fuzz, plus containment counterexamples.

Basis: AUTHOR_DECISION_20260726_D-ONSQ-CLAIMED-FIX; CONVEYOR_PACKET_ONSQ_CLAIMED_2026-07-26.
"""
import contextlib
import io
import os
import random
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_BASE = os.path.dirname(_HERE)
os.environ["MSL_MIP_HERMETIC_TLD"] = "1"
for _p in ("core", "single_sign", "sequence"):
    sys.path.insert(0, os.path.join(_BASE, _p))
sys.path.insert(0, _BASE)

import msl_mip_runtime as rt
import sequence_engine as se
se._force_tld_state_for_test(frozenset({"com", "org", "net", "ru", "io"}), False)
_CARDS = rt.load_all_cards()

Z = "​"; J = "‍"; B = "﻿"; S = "／"


def _surface(text):
    with contextlib.redirect_stdout(io.StringIO()):
        r = rt.analyze(text, _CARDS)
    so = r.get("sequence_output")
    ms = getattr(so, "matches", None) or []
    rv = getattr(so, "relation_verdicts", []) if so else []
    return (
        r.get("semantic_action"), r.get("effective_action"), r.get("attention_status"),
        tuple((m.sc_id, m.sequence, m.match_start, m.match_end, m.risk_level,
               getattr(m, "scheme_neutralized", None), getattr(m, "url_context_flag", None),
               tuple(m.source_sign_offsets)) for m in ms),
        tuple((v.get("relation_type"), v.get("at_offset"), v.get("detected_context"),
               v.get("risk_level")) for v in rv),
    )


def _both(text):
    os.environ["MSL_MIP_ONSQ2_REFERENCE"] = "1"
    ref = _surface(text)
    os.environ["MSL_MIP_ONSQ2_REFERENCE"] = "0"
    fast = _surface(text)
    return ref, fast


_CORPUS = [
    "", "/", "//", "///", "/" * 50, "//" * 40, "/.//./" * 10,
    "http://example.com/a/b/c", "https://a.com//b", "a.com/x/y/z",
    "../../../etc/passwd", "..\\..\\x", "path/to/file", "://", "a://b//c",
    "goog" + Z + "le.com", "pay" + B + "pal.com" + B + ".evil.com",
    "user" + Z + "name@example.com", "*goog" + S + "le.com*",
    ("a" + Z) * 20, ("/" ) * 200, "read" + Z + "me.md/x",
    "x/" * 30, "." * 40, ".../.../" * 8, "a/b" + Z + "c/d.com",
    "text with / slashes / here", "one://two://three", "http://u@h.com/p?q#f",
]

fails = []
checks = 0
for t in _CORPUS:
    ref, fast = _both(t)
    checks += 1
    if ref != fast:
        fails.append("CORPUS delta text=%r\n   ref =%r\n   fast=%r" % (t, ref, fast))

# fuzz over slash/dot/colon/mask alphabets
random.seed(4242)
alpha = "ab/.:@-" + Z + J + B + S + "com "
for i in range(2000):
    t = "".join(random.choice(alpha) for _ in range(random.randint(1, 60)))
    ref, fast = _both(t)
    checks += 1
    if ref != fast:
        fails.append("FUZZ delta text=%r\n   ref =%r\n   fast=%r" % (t, ref, fast))
        if len(fails) > 20:
            break
os.environ.pop("MSL_MIP_ONSQ2_REFERENCE", None)

# direct containment counterexamples on the Fenwick structure
pm = se._PrefixMax(20)
for s, e in [(0, 5), (4, 10)]:
    pm.update(s, e)
if pm.query(2) >= 8:          # union trap: {(0,5),(4,10)} must NOT cover (2,8)
    fails.append("UNION-TRAP: prefix-max wrongly reports (2,8) covered")
pm2 = se._PrefixMax(20)
for s, e in [(0, 4), (3, 7), (6, 10)]:
    pm2.update(s, e)
if pm2.query(2) >= 9:         # bridge trap: none contains (2,9)
    fails.append("BRIDGE-TRAP: prefix-max wrongly reports (2,9) covered")
pm3 = se._PrefixMax(20)
pm3.update(3, 8)
if not (pm3.query(3) >= 8):   # exact containment must hold at start==idx
    fails.append("EXACT: (3,8) should cover (3,8)")

print("=" * 70)
print("GATE: literal-matcher O(m^2)-fix == reference (ZERO-DELTA)")
print("=" * 70)
print("  checks run: %d" % checks)
if fails:
    for f in fails[:20]:
        print("  FAIL: " + f)
    print("\nTOTAL: FAIL (%d)" % len(fails))
    sys.exit(1)
print("  corpus + 2000 fuzz: full report identical fast vs reference")
print("  containment counterexamples (union / bridge / exact): correct")
print("\nTOTAL: CLEAN -- zero-delta proven; fast literal-matcher safe to ship")
sys.exit(0)
