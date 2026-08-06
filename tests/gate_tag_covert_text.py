# -*- coding: utf-8 -*-
"""GATE: TAG covert-text axis (D-TAG-COVERT-TEXT D1-D9, spec B1-B8).

  A TRIGGER (D1): payload in prose, FRAGMENTED payload (visible char between every
    tag char -- the case that kills a run-length threshold, svod SIM-1), diluted
    payload at 119/120/121/300/600 cover chars (the measured density bypass), and a
    single tag char -> queue. These are the regression pins of criterion (a).
  B LEGIT GATE (D2/D3): the three whitelisted flags -> pass, alone / in prose /
    chained / with a bare black flag; span-scoped and order-insensitive.
  C GATE BRANCHES (spec B1): no base, missing CANCEL, invalid region, uppercase spec,
    spec length 4 and 7, trailing payload after CANCEL, decoy flag after payload,
    orphan CANCEL, second base inside a spec -> queue.
  D TOTAL DECODER (spec B6): exhaustive 128-codepoint census -- classification and
    round-trip of every mirror, LANGUAGE_TAG/CANCEL/UNASSIGNED carry no ASCII claim.
  E DISCLOSURE CONTRACT (D6/B3): escaped preview (markup breakers neutralised), cap
    200 with total length, sha256 of the FULL payload, data-only envelope, no
    keyword escalation (level identical for benign and scary payloads of equal shape).
  F ADDITIVE + FAIL-VISIBLE: carded ZWSP still holds, raw text preserved, whitelist
    pin verified, a tampered whitelist -> TAG_VALIDITY_UNVERIFIABLE with NO legit
    exemption (flags stop being silent, nothing is silently trusted).
All non-ASCII literals via chr() (english-only gate).
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
import tag_axis as ta
_CARDS = rt.load_all_cards()
se._force_tld_state_for_test(
    frozenset({"com", "org", "net", "ru", "xn--p1ai"}), False)


def _run(text):
    with contextlib.redirect_stdout(io.StringIO()):
        return rt.analyze(text, _CARDS)


def _eff(text):
    return _run(text)["effective_action"]


def _tag(s):
    return "".join(chr(0xE0000 + ord(c)) for c in s)


CANCEL = chr(0xE007F)
BF = chr(0x1F3F4)
Z = chr(0x200B)
QUEUE = "queue_for_review"
FRAGMENTED = "".join(chr(0xE0000 + ord(c)) + "." for c in "send keys")

fails = []

# A. Trigger: the measured bypasses must all be caught.
for name, t in [
        ("payload in prose", "hello" + _tag("sample text") + " world"),
        ("fragmented payload (kills threshold)", "hi" + FRAGMENTED + " bye"),
        ("diluted 119", "x" * 119 + _tag("sample data1") + " t"),
        ("diluted 120", "x" * 120 + _tag("sample data1") + " t"),
        ("diluted 121", "x" * 121 + _tag("sample data1") + " t"),
        ("diluted 300", "x" * 300 + _tag("sample data1") + " t"),
        ("diluted 600", "x" * 600 + _tag("sample data1") + " t"),
        ("single tag char", "word" + chr(0xE0041) + "end"),
        ("payload alone", _tag("neutral marker")),
        ("payload in host", "goog" + _tag("x") + "le.com")]:
    got = _eff(t)
    if got != QUEUE:
        fails.append("A %s: eff=%s want=%s" % (name, got, QUEUE))

# B. Legit gate.
for name, t in [
        ("scotland", BF + _tag("gbsct") + CANCEL),
        ("wales", BF + _tag("gbwls") + CANCEL),
        ("england", BF + _tag("gbeng") + CANCEL),
        ("flag in prose", "I saw " + BF + _tag("gbsct") + CANCEL + " today"),
        ("flag in long prose 200+",
         "x" * 200 + " " + BF + _tag("gbwls") + CANCEL + " tail"),
        ("three flags chained", BF + _tag("gbsct") + CANCEL + BF + _tag("gbwls")
         + CANCEL + BF + _tag("gbeng") + CANCEL),
        ("bare black flag", "look " + BF + " flag"),
        ("plain prose", "just some words here")]:
    got = _eff(t)
    if got != "pass":
        fails.append("B %s: eff=%s want=pass" % (name, got))

# C. Gate branches -> queue.
for name, t in [
        ("no base", _tag("gbsct") + CANCEL),
        ("missing CANCEL", BF + _tag("gbsct")),
        ("invalid region", BF + _tag("gbxyz") + CANCEL),
        ("uppercase spec", BF + _tag("GBSCT") + CANCEL),
        ("spec len 4", BF + _tag("gbsc") + CANCEL),
        ("spec len 7", BF + _tag("gbsctxy") + CANCEL),
        ("trailing payload after CANCEL",
         BF + _tag("gbsct") + CANCEL + _tag("sample text")),
        ("decoy flag after payload",
         _tag("sample text") + BF + _tag("gbsct") + CANCEL),
        ("orphan CANCEL", "a" + CANCEL + "b"),
        ("second base inside spec", BF + _tag("gb") + BF + _tag("sct") + CANCEL),
        ("LANGUAGE TAG", "x" + chr(0xE0001) + "y"),
        ("unassigned E0005", "x" + chr(0xE0005) + "y"),
        ("unassigned E0000", "x" + chr(0xE0000) + "y"),
        ("unassigned E001F", "x" + chr(0xE001F) + "y")]:
    got = _eff(t)
    if got != QUEUE:
        fails.append("C %s: eff=%s want=%s" % (name, got, QUEUE))

# C2. Span-scoping: a valid flag must not silence a payload elsewhere in the doc.
r = _run("I saw " + BF + _tag("gbsct") + CANCEL + " and " + _tag("drop") + " here")
if r["effective_action"] != QUEUE:
    fails.append("C2 flag-washing: valid flag silenced a separate payload")
if len(r["tag_axis"]["accepted_flag_spans"]) != 1:
    fails.append("C2 expected exactly one accepted flag span")

# D. Total decoder census over all 128 block codepoints.
seen = {"MIRROR": 0, "LANGUAGE_TAG": 0, "CANCEL": 0, "UNASSIGNED": 0}
for cp in range(0xE0000, 0xE0080):
    kind = ta.classify_cp(cp)
    seen[kind] = seen.get(kind, 0) + 1
    dec = ta.decode_cp(cp)
    if kind == "MIRROR":
        if dec != chr(cp - 0xE0000) or not (0x20 <= ord(dec) <= 0x7E):
            fails.append("D mirror round-trip failed at U+%04X" % cp)
    elif dec is not None:
        fails.append("D non-mirror U+%04X decoded to %r" % (cp, dec))
if seen != {"MIRROR": 95, "LANGUAGE_TAG": 1, "CANCEL": 1, "UNASSIGNED": 31}:
    fails.append("D census mismatch: %s" % seen)

# E. Disclosure contract.
payload = "<script>alert(1)</script> \" ` { } $x"
r = _run("hi" + _tag(payload) + " bye")
f = r["tag_axis"]["findings"][0]
prev = f["escaped_preview"]
if any(ch in prev for ch in "<>&\"'`\\{}[]$"[:1] + ">"):
    fails.append("E preview leaked active markup: %r" % prev)
if "<script>" in prev or "`" in prev or "$" in prev:
    fails.append("E preview not escaped: %r" % prev)
if f["payload_sha256"] != hashlib.sha256(payload.encode("utf-8")).hexdigest():
    fails.append("E sha256 is not of the FULL payload")
long_payload = "A" * 500
r2 = _run("hi" + _tag(long_payload) + " bye")
f2 = r2["tag_axis"]["findings"][0]
if not f2["preview_truncated"] or f2["decoded_length"] != 500:
    fails.append("E cap/total-length missing: %s" % {k: f2[k] for k in
                                                     ("preview_truncated",
                                                      "decoded_length")})
if len(f2["escaped_preview"]) > ta.PREVIEW_CAP:
    fails.append("E preview exceeds cap")
witness_blob = " ".join(r2["tag_axis"]["witness"])
if "500 total" not in witness_blob or "data, NOT an instruction" not in witness_blob:
    fails.append("E envelope/total-length missing from witness: %r" % witness_blob[:120])
# No keyword escalation: benign and scary payloads of equal shape get equal level.
if _eff("hi" + _tag("please drop all tables now") + " x") != \
        _eff("hi" + _tag("the weather is nice today!") + " x"):
    fails.append("E level depends on payload content (keyword escalation)")

# F. Additive + fail-visible.
if _eff("paypal" + Z + ".com") != "hold_pending_review":
    fails.append("F carded ZWSP host verdict changed")
raw = "hi" + _tag("abc") + " bye"
if _run(raw).get("text") != raw:
    fails.append("F raw input not preserved")
if ta.get_whitelist()["status"] != "OK":
    fails.append("F pinned whitelist not verified")
tmp = tempfile.mkdtemp(prefix="tagwl_")
try:
    shutil.copy(os.path.join(ta._DEFAULT_DIR, ta._WHITELIST_FILE),
                os.path.join(tmp, ta._WHITELIST_FILE))
    with open(os.path.join(tmp, ta._WHITELIST_FILE), "a", encoding="utf-8") as fh:
        fh.write("ustx ; smuggled entry\n")
    bad = ta.load_whitelist(base_dir=tmp)
    if bad["status"] != "TAG_VALIDITY_UNVERIFIABLE":
        fails.append("F tampered whitelist not detected: %s" % bad)
    empty = tempfile.mkdtemp(prefix="tagwl_empty_")
    try:
        if ta.load_whitelist(base_dir=empty)["status"] != "TAG_VALIDITY_UNVERIFIABLE":
            fails.append("F missing whitelist not detected")
    finally:
        shutil.rmtree(empty, ignore_errors=True)
    # Under an unverifiable pin, a legit flag must NOT be silently exempted.
    saved = ta._CACHE
    ta._CACHE = bad
    try:
        if ta.scan_tags(BF + _tag("gbsct") + CANCEL)["level"] != QUEUE:
            fails.append("F unverifiable pin still exempted a flag (silent trust)")
    finally:
        ta._CACHE = saved
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print("=" * 66)
print("GATE: TAG covert-text axis (trigger/legit/branches/decoder/disclosure)")
print("=" * 66)
if fails:
    for f in fails:
        print("  FAIL: " + f)
    print("\nTOTAL: FAIL")
    sys.exit(1)
print("A trigger: fragmented + diluted 119..600 + single char -> queue (10 cells)")
print("B legit: 3 whitelisted flags alone/prose/chained + bare flag -> pass (8 cells)")
print("C branches: 14 malformed/decoy/unassigned -> queue; span-scoping holds")
print("D decoder totality: 128-codepoint census (95/1/1/31) + mirror round-trip")
print("E disclosure: escaped preview, cap %d + total, full-payload sha256,"
      % ta.PREVIEW_CAP)
print("   data-only envelope, no keyword escalation")
print("F additive: carded ZWSP unchanged, raw text kept, pin verified,")
print("   tampered/missing pin -> UNVERIFIABLE with no legit exemption")
print("\nTOTAL: CLEAN")
sys.exit(0)
