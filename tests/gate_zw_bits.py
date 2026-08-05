# -*- coding: utf-8 -*-
"""GATE: zero-width bit-channel axis, phase 1 (D-ZW-BITS D1-D11).

  A ATTACKS: block, spread across 400 visible chars, diluted under 800 chars of cover,
    SHAPED bits (two switches -- the case that walks past any alternation threshold),
    the WJ/SHY pair (no positional oracle exists for either), a payload inside PERSIAN
    cover on nonfunctional positions (the author's question), and third-symbol noise
    (a third carrier must not cancel a dominant pair).
  B LEGIT: Persian, Hindi, single WJ, single SHY, German anti-ligature, mixed-script
    document, plain prose. The axis must stay silent -- these characters are mandatory
    orthography, and waking on them would repeat the emoji flood W4 was built to kill.
  C RESIDUAL R4 (the author's question, measured): sloppy Persian with 3/10/25 wrong
    ZWNJ must NOT fire, because segmentation keeps each typo in its own segment.
    Pinned as an expectation so a future change to segmentation cannot silently
    reintroduce the false positive.
  D ADJACENCY (D4 -- found by prototyping, not by the round): without it the block
    payload supplies its own context and escapes. Verified directly on the classifier.
  E DISCLOSURE (D9): A/B is a reporting convention, no byte decode is claimed, the
    printed report carries ZERO raw carriers, and a segment sha256 is present.
  F ADDITIVE: carded ZWSP host still holds; other axes unchanged; attribution honest --
    where the Input-Guard escalates on its own, this axis must report contributed=False.
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
import zw_bits as zw
_CARDS = rt.load_all_cards()
se._force_tld_state_for_test(
    frozenset({"com", "org", "net", "ru", "xn--p1ai"}), False)

ZWSP, ZWNJ, ZWJ = chr(0x200B), chr(0x200C), chr(0x200D)
WJ, SHY = chr(0x2060), chr(0x00AD)
QUEUE = "queue_for_review"
MIM, YEH, KAF, NOON, BEH, ALEF = (chr(c) for c in
                                  (0x645, 0x6CC, 0x6A9, 0x646, 0x628, 0x627))
PERSIAN_OK = MIM + YEH + ZWNJ + KAF + NOON + BEH        # ZWNJ between joining letters
PERSIAN_TYPO = ALEF + ZWNJ + BEH                        # after right-joining ALEF
HINDI = chr(0x915) + chr(0x94D) + ZWNJ + chr(0x937)     # virama conjunct
FAMILY = chr(0x1F468) + ZWJ + chr(0x1F469) + ZWJ + chr(0x1F467)
BITS = "".join(format(c, "08b") for c in b"exfiltrate")


def _run(text):
    with contextlib.redirect_stdout(io.StringIO()):
        return rt.analyze(text, _CARDS)


def _enc(payload, zero, one):
    return "".join(zero if b == "0" else one
                   for ch in payload for b in format(ch, "08b"))


def _spread(cover, zero, one):
    out, bi = [], 0
    for ch in cover:
        out.append(ch)
        if bi < len(BITS):
            out.append(zero if BITS[bi] == "0" else one)
            bi += 1
    return "".join(out)


fails = []

# A. Attacks -- each must raise AND be attributed to this axis.
for name, t in [
        ("block payload", "x" + _enc(b"exf", ZWNJ, WJ) + "y"),
        ("spread over 400 visible", _spread("a" * 400, ZWNJ, WJ)),
        ("diluted under 800 cover", "x" * 800 + " " + _enc(b"exfilt", ZWNJ, WJ)),
        ("SHAPED bits, two switches", "x" + ZWNJ * 40 + WJ * 40 + "y"),
        ("pair WJ/SHY (no positional oracle)", "w" + _enc(b"exf", WJ, SHY) + "z"),
        ("payload in PERSIAN cover, nonfunctional positions",
         "".join(ALEF + (ZWNJ if b == "0" else WJ) + BEH for b in BITS[:24])),
        ("third-symbol noise", "x" + _enc(b"exf", ZWNJ, WJ).replace(WJ, WJ + ZWSP, 3)
         + "y")]:
    r = _run(t)
    if r["effective_action"] != QUEUE:
        fails.append("A %s: eff=%s want=queue" % (name, r["effective_action"]))
    if not r["zw_bits"]["contributed"]:
        fails.append("A %s: axis did not attribute its own contribution" % name)

# B. Legit -- the axis must be silent (its verdict, not the final one).
for name, t in [
        ("Persian x30", " ".join([PERSIAN_OK] * 30)),
        ("Hindi virama x30", " ".join([HINDI] * 30)),
        ("single WJ", "no" + WJ + "break"),
        ("single SHY", "Sil" + SHY + "ben"),
        ("German anti-ligature", "Auf" + ZWNJ + "lage und Schilf" + ZWNJ + "insel"),
        ("mixed-script document",
         " ".join([PERSIAN_OK] * 5) + " " + FAMILY + " hello world "
         + " ".join([PERSIAN_OK] * 5)),
        ("plain prose", "just some words here")]:
    r = _run(t)
    if r["zw_bits"]["contributed"] or r["zw_bits"]["findings"]:
        fails.append("B %s: axis wrongly fired" % name)
    if name != "mixed-script document" and r["effective_action"] != "pass":
        fails.append("B %s: eff=%s want=pass" % (name, r["effective_action"]))

# C. Residual R4 -- the author's question, pinned by measurement.
for typos in (3, 10, 25):
    t = " ".join([PERSIAN_OK] * max(0, 30 - typos) + [PERSIAN_TYPO] * typos)
    r = _run(t)
    if r["zw_bits"]["contributed"]:
        fails.append("C sloppy Persian with %d typos must not fire (segmentation)"
                     % typos)

# D. Adjacency rule, checked on the classifier itself.
block = "x" + ZWNJ + WJ + ZWNJ + ZWNJ + "y"
if zw.function_status(block, 1) != "NONFUNCTIONAL":
    fails.append("D adjacency rule missing: stacked carriers must be NONFUNCTIONAL")
if zw.function_status(PERSIAN_OK, PERSIAN_OK.index(ZWNJ)) != "PROVEN_FUNCTIONAL":
    fails.append("D Persian joining context must be PROVEN_FUNCTIONAL")
if zw.function_status(HINDI, HINDI.index(ZWNJ)) != "PROVEN_FUNCTIONAL":
    fails.append("D virama conjunct must be PROVEN_FUNCTIONAL")
if zw.function_status(FAMILY, 1) != "PROVEN_FUNCTIONAL":
    fails.append("D emoji ZWJ must be PROVEN_FUNCTIONAL")
if zw.function_status(PERSIAN_TYPO, 1) != "NONFUNCTIONAL":
    fails.append("D ZWNJ after right-joining ALEF must be NONFUNCTIONAL")
if zw.get_joining_types()["status"] != "OK":
    fails.append("D pinned Joining_Type table not verified")
# spec B3: the @missing default must be applied -- ZWNJ is absent from the file.
if zw._jt(0x200C) != "U":
    fails.append("D @missing default not applied: jt(ZWNJ) should default to U")

# E. Disclosure contract.
r = _run("x" + _enc(b"exfilt", ZWNJ, WJ) + "y")
f = r["zw_bits"]["findings"][0]
if set(f["symbol_stream"]) - set("AB"):
    fails.append("E stream must be A/B reporting convention only")
for banned in ("decoded", "payload_bytes", "hex", "utf8"):
    if banned in f:
        fails.append("E guessed decode leaked into disclosure: %s" % banned)
if not f.get("segment_sha256"):
    fails.append("E segment sha256 missing")
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    rt.print_report(r)
printed = buf.getvalue()
leaked = sorted({"U+%04X" % ord(c) for c in printed if ord(c) in zw.CARRIERS})
if leaked:
    fails.append("E report leaked raw carriers: %s" % leaked)
if "scheme NOT established" not in printed:
    fails.append("E report must state that the scheme is not established")

# F. Additive + honest attribution.
if _run("paypal" + ZWSP + ".com")["effective_action"] != "hold_pending_review":
    fails.append("F carded ZWSP host verdict changed")
r = _run(" ".join([FAMILY] * 30))
if r["zw_bits"]["contributed"]:
    fails.append("F emoji document: this axis must NOT claim another axis's escalation")

print("=" * 66)
print("GATE: zero-width bit-channel axis, phase 1")
print("=" * 66)
if fails:
    for f in fails:
        print("  FAIL: " + f)
    print("\nTOTAL: FAIL")
    sys.exit(1)
print("A 7 attacks -> queue, attributed: block, spread, diluted, SHAPED (2 switches),")
print("  WJ/SHY pair, payload in Persian cover on nonfunctional positions, 3rd-symbol noise")
print("B 7 legit controls silent (Persian, Hindi, WJ, SHY, German ligature, mixed, plain)")
print("C residual R4 pinned: sloppy Persian 3/10/25 typos does not fire (segmentation)")
print("D adjacency rule + four-state oracle + @missing default verified on the classifier")
print("E disclosure: A/B convention only, no decode, zero raw carriers in the report")
print("F additive: carded ZWSP holds; another axis's escalation is not claimed")
print("\nTOTAL: CLEAN")
sys.exit(0)
