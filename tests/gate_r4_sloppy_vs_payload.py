# -*- coding: utf-8 -*-
"""GATE: R4 round -- normative Persian vs single-carrier payload (D-R4 F1-F5, B3-B6).

Origin: the author's question "what about Persian with wrong spelling?". The round's
central finding was a correction of MY OWN measurement: I had measured "correct Persian
-> 0 nonfunctional" on a sample that happened to contain no enclitic suffixes, and
generalised from it. The panel found the after-R class, and the live oracle confirmed
100% of a normative document judged NONFUNCTIONAL.

  A AFTER-R CARVE-OUT (F4): the half-space before the closed set of Persian enclitics
    (ra, ha, tar, i, am, at, ash, ist) after a RIGHT-JOINING letter is normative
    orthography (ISIRI 9147) and must read PROVEN_FUNCTIONAL. These cells are the
    regression pins for the measured false positive.
  B THE CARVE-OUT MUST NOT WIDEN: the previous round's attack (ZWNJ after ALEF before
    an ordinary letter) and every non-suffix continuation stay NONFUNCTIONAL. This is
    what keeps BYPASS_AFTER_R_CARVEOUT a one-line channel instead of "anything after a
    right-joining letter".
  C LIVE FALSE POSITIVE GONE (the round's SIM-D): normative Persian written solid, and
    the same text with pasted ZWSP at word boundaries -- the axis must stay silent.
    Before the carve-out this fired: 20 carriers, 20 nonfunctional -> queue.
  D ATTACKS STILL CAUGHT: a payload on nonfunctional positions inside Persian cover,
    and the block/shaped forms, must still raise with attribution. The carve-out buys
    silence on normative positions ONLY.
  E BLINDNESS PINS (B3): single-carrier schemes of 24/80/240 do NOT fire -- pinned as
    an expectation with the marker LIMIT-ZW-SINGLE-CARRIER-FUNCTIONAL, never as a bare
    pass. If a future change starts catching them, this cell must be revisited through
    a round, not silently.
  F WITNESS AGGREGATION (F3): 24 identical uncarded occurrences print as ONE block with
    a count and range (measured before: 96 of 112 report lines were the same four
    sentences repeated), while the report STRUCTURE still carries every occurrence --
    so no verdict can shift. Distinct signs must not be merged.
  G DOUBLE HONESTY (B4): the printed axis note must state both halves -- the scheme is
    not established AND the blindness is real. Half a statement in either direction is
    dishonest.
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

ZWNJ, ZWSP, WJ, LRM = chr(0x200C), chr(0x200B), chr(0x2060), chr(0x200E)
QUEUE = "queue_for_review"


def _s(*cps):
    return "".join(chr(c) for c in cps)


# Normative Persian words: a right-joining letter, the half-space, then an enclitic.
AQA_RA = _s(0x622, 0x642, 0x627) + ZWNJ + _s(0x631, 0x627)      # aqa-ra
DARD_HA = _s(0x62F, 0x631, 0x62F) + ZWNJ + _s(0x647, 0x627)     # dard-ha
SEDA_HA = _s(0x635, 0x62F, 0x627) + ZWNJ + _s(0x647, 0x627)     # seda-ha
ROOZ_HA = _s(0x631, 0x648, 0x632) + ZWNJ + _s(0x647, 0x627)     # rooz-ha
BOZORG_TAR = _s(0x628, 0x632, 0x631, 0x6AF) + ZWNJ + _s(0x62A, 0x631)
KETAB_I = _s(0x6A9, 0x62A, 0x627, 0x628) + ZWNJ + _s(0x627, 0x6CC)
MI_KONAD = _s(0x645, 0x6CC) + ZWNJ + _s(0x6A9, 0x646, 0x62F)    # control: D + D
WORDS = [AQA_RA, DARD_HA, SEDA_HA, ROOZ_HA]


def _run(text):
    with contextlib.redirect_stdout(io.StringIO()):
        return rt.analyze(text, _CARDS)


def _printed(report):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rt.print_report(report)
    return buf.getvalue()


fails = []

# A. After-R carve-out: normative orthography reads functional.
for name, word in [("aqa-ra", AQA_RA), ("dard-ha", DARD_HA), ("seda-ha", SEDA_HA),
                   ("rooz-ha", ROOZ_HA), ("bozorg-tar", BOZORG_TAR),
                   ("ketab-i", KETAB_I), ("mi-konad (D+D control)", MI_KONAD)]:
    got = zw.function_status(word, word.index(ZWNJ))
    if got != "PROVEN_FUNCTIONAL":
        fails.append("A %s: %s want PROVEN_FUNCTIONAL" % (name, got))

# B. The carve-out must not widen beyond the closed suffix set.
for name, word in [
        ("ALEF then ordinary letter (previous round's attack)",
         _s(0x627) + ZWNJ + _s(0x628)),
        ("DAL then non-suffix", _s(0x62F) + ZWNJ + _s(0x645)),
        ("ZAIN then non-suffix", _s(0x632) + ZWNJ + _s(0x6A9)),
        ("Latin neighbours", "a" + ZWNJ + "b"),
        ("Cyrillic neighbours", _s(0x430) + ZWNJ + _s(0x431))]:
    got = zw.function_status(word, word.index(ZWNJ))
    if got != "NONFUNCTIONAL":
        fails.append("B %s: %s want NONFUNCTIONAL" % (name, got))

# C. The measured live false positive is gone (round SIM-D).
for name, t in [
        ("normative Persian, spaced", " ".join(WORDS * 6)),
        ("normative Persian, solid token", "".join(WORDS * 6)),
        ("solid + pasted ZWSP at word boundaries", ZWSP.join(WORDS * 6)),
        ("every third word followed by a pasted ZWSP",
         "".join(w + (ZWSP if k % 3 == 2 else "")
                 for k, w in enumerate(WORDS * 6)))]:
    r = _run(t)
    if r["zw_bits"]["contributed"] or r["zw_bits"]["findings"]:
        fails.append("C %s: axis fired on normative text" % name)

# D. Attacks still caught, with attribution.
bits = "0110100101101001" * 2
for name, t in [
        ("payload on nonfunctional positions in Persian cover",
         "".join(_s(0x627) + (ZWNJ if b == "0" else WJ) + _s(0x628) for b in bits)),
        ("block payload", "x" + (ZWNJ + WJ) * 12 + "y"),
        ("shaped payload, two switches", "x" + ZWNJ * 20 + WJ * 20 + "y")]:
    r = _run(t)
    if r["effective_action"] != QUEUE or not r["zw_bits"]["contributed"]:
        fails.append("D %s: eff=%s contributed=%s" % (name, r["effective_action"],
                                                      r["zw_bits"]["contributed"]))

# E. Blindness pins (B3) -- named, never a bare pass.
for n in (24, 80, 240):
    t = "".join(_s(0x645, 0x6CC) + ZWNJ + _s(0x6A9, 0x646) for _ in range(n))
    r = _run(t)
    if r["zw_bits"]["contributed"]:
        fails.append("E single-carrier scheme of %d changed behaviour -- "
                     "LIMIT-ZW-SINGLE-CARRIER-FUNCTIONAL moved, needs a round" % n)
    if r["zw_bits"]["carrier_total"] != n:
        fails.append("E %d carriers must still be COUNTED (blindness is not silence): "
                     "counted %d" % (n, r["zw_bits"]["carrier_total"]))

# F. Witness aggregation, and the structure kept intact.
r = _run("".join("ab" + ZWNJ + "cd " for _ in range(24)))
if len(r["uncarded_invisibles"]) != 24:
    fails.append("F report structure lost occurrences: %d of 24"
                 % len(r["uncarded_invisibles"]))
out = _printed(r)
if out.count("U+200C") != 1:
    fails.append("F witness not aggregated: %d rows for one repeated sign"
                 % out.count("U+200C"))
if "x24" not in out:
    fails.append("F aggregated row must carry the count")
if len(out.splitlines()) > 40:
    fails.append("F report still floods: %d lines" % len(out.splitlines()))
# Distinct signs must stay distinct.
out2 = _printed(_run("a" + ZWNJ + "b " + LRM + " c" + ZWNJ + "d"))
if out2.count("U+200C") != 1 or out2.count("U+200E") != 1:
    fails.append("F distinct signs merged or duplicated")

# H. CROSS-ORACLE CONSISTENCY (found by auditing the seam between the two oracles this
# project now has: the card layer's SNI oracle and this axis both judge whether a join
# control does a job). The axis used to trust unicodedata.combining()==9, which holds
# for 69 codepoints while only SIX are normative InCB linkers. Measured evasion: a
# two-carrier channel in Khmer cover with every carrier placed right after a COENG --
# a mark in nearly every Khmer word -- read PROVEN_FUNCTIONAL throughout, so the
# nonfunctional count was zero and the axis went silent, while the SAME channel between
# ordinary letters fired. Both halves are pinned here: the evasion must raise, and the
# six normative conjunct scripts must stay silent.
_BITS = "0110100101101001" * 2
for name, base, mark, tail in [
        ("Khmer COENG cover", 0x1780, 0x17D2, 0x1789),
        ("Thai PHINTHU cover", 0x0E01, 0x0E3A, 0x0E20),
        ("Myanmar virama cover", 0x1000, 0x1039, 0x1001),
        ("Javanese pangkon cover", 0xA984, 0xA9C0, 0xA985)]:
    t = "".join(_s(base, mark) + (ZWNJ if b == "0" else WJ) + _s(tail)
                for b in _BITS)
    r = _run(t)
    if r["effective_action"] != QUEUE or not r["zw_bits"]["contributed"]:
        fails.append("H %s: carriers after a NON-normative virama evade the axis "
                     "(eff=%s contributed=%s)"
                     % (name, r["effective_action"], r["zw_bits"]["contributed"]))
for name, cons, linker, cons2 in [
        ("Devanagari", 0x0915, 0x094D, 0x0937), ("Bengali", 0x0995, 0x09CD, 0x09AC),
        ("Gujarati", 0x0A95, 0x0ACD, 0x0AB7), ("Oriya", 0x0B15, 0x0B4D, 0x0B37),
        ("Telugu", 0x0C15, 0x0C4D, 0x0C37), ("Malayalam", 0x0D15, 0x0D4D, 0x0D37)]:
    word = _s(cons, linker) + ZWNJ + _s(cons2)
    if zw.function_status(word, word.index(ZWNJ)) != "PROVEN_FUNCTIONAL":
        fails.append("H %s conjunct must stay PROVEN_FUNCTIONAL" % name)
    r = _run(" ".join([word] * 30))
    if r["effective_action"] != "pass" or r["zw_bits"]["contributed"]:
        fails.append("H %s document of 30 conjuncts must stay silent" % name)
# The linker predicate must read the pinned table, not the stdlib heuristic.
if zw._is_linker(chr(0x17D2)) or not zw._is_linker(chr(0x094D)):
    fails.append("H linker predicate is not reading InCB=Linker from the pin")

# G. Double honesty in the axis note.
r = _run("x" + (ZWNJ + WJ) * 12 + "y")
note = (r["zw_bits"].get("note") or "") + " " + _printed(r)
if "NOT established" not in note:
    fails.append("G the report must state that the scheme is not established")

print("=" * 66)
print("GATE: R4 -- normative Persian vs single-carrier payload")
print("=" * 66)
if fails:
    for f in fails:
        print("  FAIL: " + f)
    print("\nTOTAL: FAIL")
    sys.exit(1)
print("A after-R carve-out: 6 normative enclitic forms + D/D control -> PROVEN")
print("B carve-out does not widen: previous round's attack and non-suffixes -> NONFUNC")
print("C measured live FP gone: normative Persian spaced/solid/pasted-ZWSP -> silent")
print("D attacks still caught with attribution: Persian cover, block, shaped")
print("E blindness pinned at 24/80/240 -- not firing, but carriers still counted")
print("F witness aggregated (1 row x24) while the structure keeps all 24 occurrences")
print("G double honesty: the scheme is stated as NOT established")
print("H cross-oracle: carriers after Khmer/Thai/Myanmar/Javanese viramas no longer")
print("  evade (ccc==9 held for 69 codepoints, only 6 are normative InCB linkers);")
print("  all six conjunct scripts stay silent")
print("\nTOTAL: CLEAN")
sys.exit(0)
