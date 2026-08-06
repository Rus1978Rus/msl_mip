# -*- coding: utf-8 -*-
"""GATE: VS-STEGO — exact-pair variation validity (D-VS-STEGO D1-D9, spec B1-B8).

  A THE MEASURED HOLE: CJK cover with one selector per character (13/50/200/1000/3000
    bytes) was pass/attn=NONE/witness=0; must now be queue with a payload witness.
  B LEGIT SILENCE (criterion (b) -- the flood D3 was written to kill must NOT return):
    registered emoji pairs, registered IVD, registered StandardizedVariants, and the
    measured presentation carve-out (redundant FE0F on emoji-default bases).
  C UNREGISTERED pairs that the old shape rule trusted -> queue (this is the amendment).
  D REGISTRY: pins verified; composite counts; tampered/missing -> UNVERIFIABLE with a
    VISIBLE notice and no silent pass (B3).
  E DISCLOSURE (D6): hex only, cap 64, full length, sha256 of the WHOLE payload, a
    mechanical utf8 flag, and NO content typing; carrier selectors only (registered
    presentation pairs are not payload).
  F ADDITIVE: W4 baseline cells that must NOT move (CONTROL), carded ZWSP still holds,
    raw text preserved, other axes unchanged.
Expectations for registry membership are GENERATED from the pinned tables (spec B6),
never hand-written. All non-ASCII literals via chr() (english-only gate).
"""
import contextlib
import hashlib
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
import variation_registry as vr
_CARDS = rt.load_all_cards()
se._force_tld_state_for_test(
    frozenset({"com", "org", "net", "ru", "xn--p1ai"}), False)

QUEUE = "queue_for_review"
Z = chr(0x200B)
EMOJI_DEFAULT = chr(0x1F600)          # grinning face: NO registered FE0F sequence
CJK = [chr(c) for c in (0x845B, 0x8FBB, 0x9089, 0x91CE, 0x6F22,
                        0x5B57, 0x6771, 0x4EAC, 0x795E, 0x6238)]


def _run(text):
    with contextlib.redirect_stdout(io.StringIO()):
        return rt.analyze(text, _CARDS)


def _eff(text):
    return _run(text)["effective_action"]


def _vs(b):
    return chr(0xFE00 + b) if b < 16 else chr(0xE0100 + (b - 16))


def _cover(data):
    return "".join(CJK[i % len(CJK)] + _vs(b) for i, b in enumerate(data))


fails = []
_reg = vr.get_registry()

# D (first: everything else depends on a verified registry).
if _reg["status"] != "OK":
    fails.append("D registry not OK: %s" % _reg.get("reason"))
else:
    if _reg["counts"] != {"StandardizedVariants.txt": 1306,
                          "emoji-variation-sequences.txt": 742,
                          "IVD_Sequences.txt": 29437}:
        fails.append("D composite counts drifted: %s" % _reg["counts"])
    if _reg["ivd_release"] != "2022-09-13":
        fails.append("D IVD pin is not the authored release date")

# A. The measured hole must now fire, with a payload witness.
for n in (13, 50, 200, 1000, 3000):
    r = _run(_cover(b"A" * n))
    if r["effective_action"] != QUEUE:
        fails.append("A cover %d bytes: eff=%s want=queue" % (n, r["effective_action"]))
    if r["vs_payload"].get("byte_length") != n:
        fails.append("A cover %d: payload witness = %s"
                     % (n, r["vs_payload"].get("byte_length")))

# B. Legit silence. Registered pairs are taken FROM the pinned tables (B6).
_registered_samples = []
for (b, s) in sorted(_reg["pairs"]):
    if 0xE0100 <= s <= 0xE01EF and not _registered_samples:
        _registered_samples.append((b, s))
    if s == 0xFE00 and 0x3400 <= b <= 0x9FFF and len(_registered_samples) < 2:
        _registered_samples.append((b, s))
    if s == 0xFE0F and len(_registered_samples) < 3:
        _registered_samples.append((b, s))
    if len(_registered_samples) >= 3:
        break
for (b, s) in _registered_samples:
    t = chr(b) + chr(s)
    if _eff(t) != "pass":
        fails.append("B registered pair U+%04X+U+%04X should stay silent" % (b, s))
for name, t in [
        ("heart+FE0F", chr(0x2764) + chr(0xFE0F)),
        ("redundant FE0F on emoji-default", EMOJI_DEFAULT + chr(0xFE0F)),
        ("redundant FE0F on fire", chr(0x1F525) + chr(0xFE0F)),
        ("chat text with emoji", "great work " + EMOJI_DEFAULT + chr(0xFE0F) + " thanks"),
        ("50 hearts", (chr(0x2764) + chr(0xFE0F)) * 50),
        ("plain prose", "just some words here")]:
    if _eff(t) != "pass":
        fails.append("B %s: eff=%s want=pass" % (name, _eff(t)))

# C. Unregistered pairs the old shape rule trusted.
for name, t in [
        ("CJK + unregistered FE00", chr(0x845B) + chr(0xFE00)),
        ("CJK + unregistered supplement", chr(0x845B) + chr(0xE0150)),
        ("emoji + FE00 (byte-0 channel)", EMOJI_DEFAULT + chr(0xFE00)),
        ("emoji + supplement selector", EMOJI_DEFAULT + chr(0xE0100))]:
    if _eff(t) != QUEUE:
        fails.append("C %s: eff=%s want=queue" % (name, _eff(t)))

# E. Disclosure contract. Expected payload is derived MACHINE-WISE from the pins (B6):
# a pair that happens to be REGISTERED is legitimate presentation, not payload, so it is
# excluded -- exactly what the axis must do. Hand-writing "256" here would encode a wrong
# expectation (measured: 7 of the 256 pairs are registered).
payload_all = bytes(range(256))
cover_text = _cover(payload_all)
expected = bytes(b for i, b in enumerate(payload_all)
                 if (ord(CJK[i % len(CJK)]), ord(_vs(b))) not in _reg["pairs"])
r = _run(cover_text)
p = r["vs_payload"]
if p.get("byte_length") != len(expected) or not p.get("truncated"):
    fails.append("E length/truncation wrong: got %s want %d"
                 % (p.get("byte_length"), len(expected)))
if p.get("payload_sha256") != hashlib.sha256(expected).hexdigest():
    fails.append("E sha256 is not of the FULL carrier payload")
if len(expected) == 256:
    fails.append("E test is not exercising the registered-pair exclusion")
if len(p.get("hex_preview", "").split()) != 64:
    fails.append("E hex preview is not capped at 64 bytes")
if p.get("utf8_valid") is not False:
    fails.append("E binary payload should report utf8_valid=False")
for banned in ("type", "kind", "classification"):
    if banned in p:
        fails.append("E content typing leaked into disclosure: %s" % banned)
r2 = _run(_cover(b"sample data1"))
if r2["vs_payload"].get("utf8_valid") is not True:
    fails.append("E ASCII payload should report utf8_valid=True")
# Registered presentation pairs must NOT be counted as payload.
if _run("hi " + chr(0x2764) + chr(0xFE0F)).get("vs_payload"):
    fails.append("E registered presentation pair leaked into payload")

# D2. Fail-visible registry.
tmp = tempfile.mkdtemp(prefix="vsreg_")
try:
    for fname in vr.PINNED_SHA256:
        shutil.copy(os.path.join(vr._DEFAULT_DIR, fname), os.path.join(tmp, fname))
    with open(os.path.join(tmp, "IVD_Sequences.txt"), "a", encoding="utf-8") as fh:
        fh.write("\n# tampered\n")
    bad = vr.load_registry(base_dir=tmp)
    if bad["status"] != "UNVERIFIABLE" or "IVD_Sequences.txt" not in bad.get("reason", ""):
        fails.append("D tamper not detected: %s" % bad)
    empty = tempfile.mkdtemp(prefix="vsreg_empty_")
    try:
        if vr.load_registry(base_dir=empty)["status"] != "UNVERIFIABLE":
            fails.append("D missing artifacts not detected")
    finally:
        shutil.rmtree(empty, ignore_errors=True)
    saved = vr._CACHE
    vr._CACHE = bad
    try:
        # No silent pass: the notice must reach the report even when nothing else fires.
        rep = _run("hi " + chr(0x2764) + chr(0xFE0F))
        if rep["vs_payload"].get("registry_status") != "UNVERIFIABLE":
            fails.append("D unverifiable registry not surfaced in the report")
    finally:
        vr._CACHE = saved
finally:
    shutil.rmtree(tmp, ignore_errors=True)

# F. Additive / CONTROL cells from the frozen W4 baseline (must NOT move).
for name, t, want in [
        ("orphan on letter", "a" + chr(0xFE0F) + "b", QUEUE),
        ("orphan leading", chr(0xFE00) + "text", QUEUE),
        ("chain on one base", chr(0x845B) + chr(0xE0100) + chr(0xE0101), QUEUE),
        ("carded ZWSP host", "paypal" + Z + ".com", "hold_pending_review"),
        ("ascii domain", "paypal.com", "pass")]:
    if _eff(t) != want:
        fails.append("F CONTROL %s moved: eff=%s want=%s" % (name, _eff(t), want))
raw = "hi" + _cover(b"abc")
if _run(raw).get("text") != raw:
    fails.append("F raw input not preserved")

print("=" * 66)
print("GATE: VS-STEGO — exact-pair variation validity")
print("=" * 66)
if fails:
    for f in fails:
        print("  FAIL: " + f)
    print("\nTOTAL: FAIL")
    sys.exit(1)
print("A measured hole closed: CJK cover 13/50/200/1000/3000 -> queue + payload witness")
print("B legit silent: registered pairs (from the pins) + presentation carve-out + prose")
print("C unregistered pairs the shape rule trusted -> queue (the amendment)")
print("D registry pinned (1306/742/29437, IVD %s); tamper/missing -> UNVERIFIABLE,"
      % _reg.get("ivd_release"))
print("  surfaced in the report, never a silent pass")
print("E disclosure: hex cap 64, full length, whole-payload sha256, utf8 flag, no typing")
print("F CONTROL cells unmoved (orphan/chain/carded ZWSP/ascii), raw text preserved")
print("\nTOTAL: CLEAN")
sys.exit(0)
