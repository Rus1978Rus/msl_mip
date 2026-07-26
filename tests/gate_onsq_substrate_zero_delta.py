# -*- coding: utf-8 -*-
"""GATE: the detect_substrate O(m^2)-fix (round 4, D-ONSQ-SUBSTRATE-FIX) is ZERO-DELTA.

Two token-level facts replace per-offset O(n) work: text.count("/") once, and an
O(1) domain-before-slash test from a precomputed ASCII-letter-run array (equivalent
to `_DOMAIN_BEFORE_SLASH_RE.search(text[:offset])`, including the $-before-trailing-\\n
edge). MSL_MIP_ONSQ3_REFERENCE=1 forces the original regex/count oracle.

Layers:
  A DIRECT: _dom_before_slash_fast(text,off,letrun) == bool(regex.search(text[:off]))
    for every offset of a broad corpus + fuzz (the tightest check on the risky part).
  B SUBSTRATE: detect_substrate fast == reference for every offset.
  C END-TO-END: full analyze() report identical fast vs reference.

Basis: AUTHOR_DECISION_20260726_D-ONSQ-CLAIMED-FIX (round 4 = OPEN); Kimi review 2026-07-26.
"""
import contextlib
import io
import os
import random
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_BASE = os.path.dirname(_HERE)
os.environ["MSL_MIP_HERMETIC_TLD"] = "1"
for _p in ("core", "single_sign", "sequence", os.path.join("single_sign", "matchers")):
    sys.path.insert(0, os.path.join(_BASE, _p))
sys.path.insert(0, _BASE)

import solidus_matcher as sm
import msl_mip_runtime as rt
import sequence_engine as se
se._force_tld_state_for_test(frozenset({"com", "org", "net", "ru", "io"}), False)
_CARDS = rt.load_all_cards()

fails = []
checks = 0

_CORPUS = [
    "", "/", "//", "///", "/" * 50, "a.com/x", "trusted.com/verified",
    "sub.domain.org/path/to", "x.co/", ".com/", "1.co/", "-.com/", "a.c/",
    "http://a.com/p", "a.com\n/x", "site.com\n", "C:/Users/doc", "../../e/p",
    "a.b.cd/", "word.NET/x", "пример.com/a", "домен.рф/",  # unicode \w before dot
    "12.34/56", "2026/01/02", "path/to/file", "a/b/c/d", "!.com/",
    "_priv.com/", "a-b.com/x", "x.abcdefghij/", "no dot here/x/y",
    ("a.com/" * 30), ("/" * 100), "café.com/x",
]


def _both_substrate_all_offsets(text):
    global checks
    for off in range(len(text) + 1):
        os.environ["MSL_MIP_ONSQ3_REFERENCE"] = "1"
        ref = sm.detect_substrate(text, off)
        os.environ["MSL_MIP_ONSQ3_REFERENCE"] = "0"
        sm._SUB_CACHE.clear()
        fast = sm.detect_substrate(text, off)
        checks += 1
        if ref != fast:
            fails.append("B off=%d ref=%s fast=%s text=%r" % (off, ref, fast, text))


def _direct_all_offsets(text):
    global checks
    sm._SUB_CACHE.clear()
    _, letrun = sm._sub_facts(text)
    for off in range(len(text) + 1):
        ref = bool(sm._DOMAIN_BEFORE_SLASH_RE.search(text[:off]))
        fast = sm._dom_before_slash_fast(text, off, letrun)
        checks += 1
        if ref != fast:
            fails.append("A off=%d ref=%s fast=%s text=%r" % (off, ref, fast, text))


for t in _CORPUS:
    _direct_all_offsets(t)
    _both_substrate_all_offsets(t)

# fuzz
random.seed(9090)
alpha = "abcXY.-_/\\:0129 \n" + "рф" + "é"
for i in range(1500):
    t = "".join(random.choice(alpha) for _ in range(random.randint(1, 40)))
    _direct_all_offsets(t)
    if i < 400:
        _both_substrate_all_offsets(t)

os.environ.pop("MSL_MIP_ONSQ3_REFERENCE", None)


# C end-to-end
def _surface(text):
    with contextlib.redirect_stdout(io.StringIO()):
        r = rt.analyze(text, _CARDS)
    so = r.get("sequence_output"); ms = getattr(so, "matches", None) or []
    return (r.get("semantic_action"), r.get("effective_action"), r.get("attention_status"),
            tuple((m.sc_id, m.match_start, m.match_end, m.risk_level) for m in ms))


for t in ["a.com/x/y", "trusted.com/verified", "http://x.com//a", "C:/Users/f",
          "path/to/f", "/" * 30, "a.com\n/z", "домен.рф/a"]:
    os.environ["MSL_MIP_ONSQ3_REFERENCE"] = "1"; sm._SUB_CACHE.clear(); ref = _surface(t)
    os.environ["MSL_MIP_ONSQ3_REFERENCE"] = "0"; sm._SUB_CACHE.clear(); fast = _surface(t)
    checks += 1
    if ref != fast:
        fails.append("C analyze delta text=%r ref=%r fast=%r" % (t, ref, fast))
os.environ.pop("MSL_MIP_ONSQ3_REFERENCE", None)

print("=" * 68)
print("GATE: detect_substrate O(m^2)-fix == reference (ZERO-DELTA)")
print("=" * 68)
print("  checks run: %d" % checks)
if fails:
    for f in fails[:30]:
        print("  FAIL: " + f)
    print("\nTOTAL: FAIL (%d)" % len(fails))
    sys.exit(1)
print("  A domain-before-slash fast == regex for every offset (+ trailing-\\n edge)")
print("  B detect_substrate fast == reference; C full analyze identical")
print("\nTOTAL: CLEAN -- zero-delta proven; fast substrate safe to ship")
sys.exit(0)
