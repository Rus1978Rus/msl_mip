# -*- coding: utf-8 -*-
"""GATE: SNI card-layer functional-position exemption (D-SNI, svod 2026-08-06).

  A TARGETS (the round's measured defect): normal prose in scripts whose orthography
    REQUIRES the carded invisisibles -- Khmer/Thai/Lao/Myanmar ZWSP word boundaries,
    Devanagari virama+ZWJ conjuncts, Malayalam chillu (virama+ZWJ word-final) -- moves
    queue -> pass with ONE collapsed witness aggregate. 40 boundaries = 1 entry, not 40
    (MUT-SN-10).
  B GUARDS (each buried an amnesty variant by measurement): host/machine fields never
    soften even in native script (MUT-SN-02); the Cf-tolerant host path stays hold;
    Latin ZWSP stays queue (MUT-SN-05); the mixed-script boundary KH|ZWSP|latin gets no
    exemption (MUT-SN-03 -- BOTH significant neighbours must be SA, the attacker owns
    both sides); Devanagari ZWJ WITHOUT the virama stays queue (script equality alone
    proves nothing -- only InCB=Linker separates conjunct from anomaly); a dominant
    native script cannot amnesty a Latin token elsewhere in the document (MUT-SN-A-dom,
    measured 55/55 with zero tax); the two-carrier bit channel under Khmer cover is
    still caught -- by ZW-BITS independently, with honest attribution (MUT-SN-07).
  C CONTROLS FROZEN: emoji path untouched (it passes via context, not via this seam --
    MUT-SN-11); Persian ZWNJ untouched; plain Latin/Cyrillic prose untouched; the
    Khmer COENG+ZWJ (a real TUS 16.4 function outside InCB) stays queue as the NAMED
    residual SNI-FP-KHMER-COENG-ZWJ -- a carve-out needs the SNI-M4 corpus measure and
    its own author decision; BOM gets no script exemption anywhere (MUT-SN-06).
  D FAIL-CLOSED (MUT-SN-09): a missing or hash-mismatched pinned table means
    SNI_UNVERIFIABLE and the exemption grants NOTHING -- unknown is not amnesty. The
    oracle itself is probed directly on both failure paths.
  E REGRESSION PIN (REGRESSION_CARD_ZWSP_NATIVE, fail-visible): the single-carrier
    ZWSP channel inside SA cover now passes the card -- BY DESIGN, because catching it
    meant queueing 100% of the writing system (zero specificity). This cell pins the
    blindness with its witness trail: eff=pass is asserted TOGETHER with the aggregate
    (a bare pass with no trail is the banned formulation), and ZW-BITS staying silent
    is asserted so a future change that starts claiming this catch must come through
    a round, not slip in.
All non-ASCII literals via chr() (english-only gate).
"""
import contextlib
import io
import os
import shutil
import sys
import tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))
_BASE = os.path.dirname(_HERE)
os.environ["MSL_MIP_HERMETIC_TLD"] = "1"
for _p in ("core", "single_sign", "sequence"):
    sys.path.insert(0, os.path.join(_BASE, _p))
sys.path.insert(0, _BASE)

import msl_mip_runtime as rt
import sequence_engine as se
import sni_oracle as sni
_CARDS = rt.load_all_cards()
se._force_tld_state_for_test(
    frozenset({"com", "org", "net", "ru", "xn--p1ai"}), False)

ZWSP, ZWNJ, ZWJ, WJ = chr(0x200B), chr(0x200C), chr(0x200D), chr(0x2060)
BOM = chr(0xFEFF)
QUEUE = "queue_for_review"
HOLD = "hold_pending_review"


def _s(*cps):
    return "".join(chr(c) for c in cps)


KH = _s(0x1781, 0x17D2, 0x1789)          # Khmer word (with a COENG mark inside)
TH = _s(0x0E20, 0x0E32)                  # Thai
LAO = _s(0x0EA5, 0x0EB2)                 # Lao
MY = _s(0x1000, 0x102C)                  # Myanmar
DEV_V = _s(0x0939, 0x093F, 0x0928, 0x094D)   # Devanagari ...consonant+virama
DEV_N = _s(0x0939, 0x093F, 0x0928)           # same word WITHOUT the virama
DEV_2 = _s(0x0926, 0x0940)
ML = _s(0x0D2E, 0x0D15)                  # Malayalam letters
ML_CH = _s(0x0D28, 0x0D4D)               # Malayalam NA + virama (chillu = +ZWJ)
COENG_ZWJ = _s(0x1780, 0x17D2) + ZWJ + _s(0x179A)   # Khmer COENG+ZWJ (TUS 16.4)
FAMILY = chr(0x1F468) + ZWJ + chr(0x1F469) + ZWJ + chr(0x1F467)
PERSIAN = _s(0x0645, 0x06CC) + ZWNJ + _s(0x06A9, 0x0646)


def _run(text):
    with contextlib.redirect_stdout(io.StringIO()):
        return rt.analyze(text, _CARDS)


fails = []

# A. Targets: normative native text leaves the queue, with ONE collapsed aggregate.
for name, t, want_sni in [
        ("Khmer 10 words", (KH + ZWSP) * 10 + KH, 10),
        ("Khmer 20 words", (KH + ZWSP) * 20 + KH, 20),
        ("Khmer 40 words", (KH + ZWSP) * 40 + KH, 40),
        ("Thai prose", TH + ZWSP + TH + " " + TH + ZWSP + TH, 2),
        ("Lao prose", LAO + ZWSP + LAO, 1),
        ("Myanmar prose", MY + ZWSP + MY, 1),
        ("Devanagari virama+ZWJ conjunct", DEV_V + ZWJ + DEV_2, 1),
        ("Malayalam chillu in prose", ML + ML_CH + ZWJ + " " + ML, 1)]:
    r = _run(t)
    if r["effective_action"] != "pass":
        fails.append("A %s: eff=%s want=pass" % (name, r["effective_action"]))
    agg = r.get("sni_card")
    if not agg or agg["exempted_total"] != want_sni:
        fails.append("A %s: aggregate=%s want %d exempted"
                     % (name, agg and agg["exempted_total"], want_sni))
    # MUT-SN-10: collapsed -- entries grow by (sign, basis), never per occurrence.
    if agg and len(agg["by_sign_basis"]) > 2:
        fails.append("A %s: witness not collapsed (%d entries)"
                     % (name, len(agg["by_sign_basis"])))

# B. Guards -- every measured amnesty variant must still be dead.
for name, t, want in [
        ("ZWSP in host", "paypal" + ZWSP + ".com", HOLD),
        ("Cf-tolerant host", "exa" + ZWSP + "mple.com", HOLD),
        ("Khmer-script domain", KH + ZWSP + KH + " evil" + ZWSP + ".com", HOLD),
        ("Latin ZWSP token", "ab" + ZWSP + "cd ok", QUEUE),
        ("mixed boundary KH|ZWSP|latin", KH + ZWSP + "ab", QUEUE),
        ("mixed boundary latin|ZWSP|KH", "ab" + ZWSP + KH, QUEUE),
        ("Devanagari ZWJ without virama", DEV_N + ZWJ + DEV_2, QUEUE),
        ("dominant script cannot amnesty a Latin token",
         (KH + ZWSP) * 10 + KH + " ab" + ZWSP + "cd", QUEUE)]:
    r = _run(t)
    if r["effective_action"] != want:
        fails.append("B %s: eff=%s want=%s" % (name, r["effective_action"], want))

# B2. Two-carrier channel under Khmer cover: caught, and attributed to ZW-BITS --
# the card exemption must not suppress the independent axis (MUT-SN-07).
bits = "".join(KH + (ZWNJ if b == "0" else WJ) for b in "0110100101101001")
r = _run(KH + " " + bits + " " + KH)
if r["effective_action"] != QUEUE:
    fails.append("B2 two-carrier cover: eff=%s want=queue" % r["effective_action"])
if not r["zw_bits"]["contributed"]:
    fails.append("B2 two-carrier cover: ZW-BITS must contribute independently")

# C. Frozen controls.
for name, t, want in [
        ("emoji family in prose", "look " + FAMILY + " here", "pass"),
        ("Persian ZWNJ prose", " ".join([PERSIAN] * 5), "pass"),
        ("plain prose", "just some words here", "pass"),
        ("COENG+ZWJ named residual", COENG_ZWJ + " " + COENG_ZWJ, QUEUE)]:
    r = _run(t)
    if r["effective_action"] != want:
        fails.append("C %s: eff=%s want=%s" % (name, r["effective_action"], want))
    if name != "COENG+ZWJ named residual" and r.get("sni_card"):
        fails.append("C %s: sni_card present on a control (must be absent)" % name)
# MUT-SN-06: BOM never earns a script exemption -- the oracle answers None even
# with SA neighbours on both sides, so whatever the card does today stands.
if sni.functional_position(KH + BOM + KH, len(KH)) is not None:
    fails.append("C BOM: oracle granted a script exemption to BOM")
base = _run(KH + " " + KH)          # no carded sign at all
if base.get("sni_card"):
    fails.append("C clean native text: sni_card must be absent (bit-identical)")

# D. Fail-closed oracle (MUT-SN-09): missing table and tampered table both grant
# nothing; the status is UNVERIFIABLE, never a silent default.
tmp = tempfile.mkdtemp(prefix="sni_gate_")
try:
    t1 = sni.load_sni_tables(base_dir=tmp)                    # missing files
    if t1["status"] != "SNI_UNVERIFIABLE" or t1["sa"]:
        fails.append("D missing tables: %s" % t1["status"])
    src = os.path.join(_BASE, "data", "unicode", "LineBreak.txt")
    dst = os.path.join(tmp, "LineBreak.txt")
    shutil.copyfile(src, dst)
    with open(dst, "a", encoding="utf-8") as f:
        f.write("\n# tampered\n")
    shutil.copyfile(os.path.join(_BASE, "data", "unicode",
                                 "DerivedCoreProperties.txt"),
                    os.path.join(tmp, "DerivedCoreProperties.txt"))
    t2 = sni.load_sni_tables(base_dir=tmp)                    # hash mismatch
    if t2["status"] != "SNI_UNVERIFIABLE" or t2["sa"]:
        fails.append("D tampered table: %s" % t2["status"])
finally:
    shutil.rmtree(tmp, ignore_errors=True)
# Healthy pin sanity: the machine-derived counts match the round's census.
t_ok = sni.get_sni_tables()
if t_ok["status"] != "OK" or len(t_ok["sa"]) != 757 or len(t_ok["incb_linker"]) != 6:
    fails.append("D pinned tables: status=%s SA=%d Linker=%d"
                 % (t_ok["status"], len(t_ok["sa"]), len(t_ok["incb_linker"])))

# E. REGRESSION_CARD_ZWSP_NATIVE pinned fail-visible: the single-carrier channel in
# SA cover passes the card BY DESIGN (catching it = queueing the writing system),
# and the trail is the witness aggregate -- a bare pass would be the banned form.
r = _run((KH + ZWSP) * 20 + KH)
if r["effective_action"] != "pass":
    fails.append("E single-carrier cover: eff=%s (the pinned blindness moved -- "
                 "any change here needs a round)" % r["effective_action"])
if not r.get("sni_card") or r["sni_card"]["exempted_total"] != 20:
    fails.append("E single-carrier cover: witness trail missing (bare pass banned)")
if r["zw_bits"]["contributed"]:
    fails.append("E single-carrier cover: ZW-BITS claiming a catch it cannot make")
# The printed report must carry the aggregate line and zero raw carriers.
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    rt.print_report(r)
printed = buf.getvalue()
if "SCRIPT-NATIVE FUNCTIONAL POSITIONS" not in printed:
    fails.append("E printed report: witness aggregate line missing")
if any(ord(c) in (0x200B, 0x200C, 0x200D, 0x2060, 0xFEFF, 0x00AD) for c in printed):
    fails.append("E printed report leaked raw carriers")

print("=" * 66)
print("GATE: SNI card-layer functional-position exemption")
print("=" * 66)
if fails:
    for f in fails:
        print("  FAIL: " + f)
    print("\nTOTAL: FAIL")
    sys.exit(1)
print("A 8 native targets -> pass + ONE collapsed aggregate (40 boundaries != 40 rows)")
print("B 8 guards + 2-carrier cover: host/Cf-host/domain hold; Latin, mixed boundary,")
print("  no-virama ZWJ, dominant-script amnesty all stay queue; ZW-BITS attributed")
print("C controls frozen: emoji, Persian ZWNJ, plain prose, COENG+ZWJ residual, BOM")
print("D fail-closed: missing + tampered pin -> UNVERIFIABLE grants nothing; 757/6 pinned")
print("E REGRESSION_CARD_ZWSP_NATIVE pinned fail-visible with its witness trail")
print("\nTOTAL: CLEAN")
sys.exit(0)
