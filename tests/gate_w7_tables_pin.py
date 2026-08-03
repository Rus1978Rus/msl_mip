# -*- coding: utf-8 -*-
"""GATE: W7 pinned Unicode tables (B3/S3 oracle).

Verifies the three repo artifacts (confusables.txt, Scripts.txt, ScriptExtensions.txt)
against the pinned sha256 + unidata_version, spot-checks known oracle values measured
from the official 16.0.0 files, asserts the D6 deferral (full minus active == exactly
the 4 disputed sources), and proves fail-visible behavior on tampered/missing data
(S3.2: structured UNVERIFIABLE status, no exception, no silent fallback).
Basis: AUTHOR_DECISION_20260804_D-W7-CONFUSABLE (D5, D6) + SPEC B3.
All non-ASCII literals via chr() (english-only gate).
"""
import os
import shutil
import sys
import tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))
_BASE = os.path.dirname(_HERE)
sys.path.insert(0, os.path.join(_BASE, "core"))

import unicode_tables as ut

fails = []
t = ut.load_tables()

# A. Pins verified (hashes + unidata_version) via the loader itself.
if t["status"] != "OK":
    fails.append("A load_tables status=%s reason=%s" % (t["status"], t.get("reason")))
else:
    full = t["confusables_full"]
    active = t["confusables_active"]

    # B. Confusables oracle (values measured from the official 16.0.0 table).
    for cp, want, name in [
            (0x0430, "a", "CYRILLIC A"),
            (0x043E, "o", "CYRILLIC O"),
            (0x03B1, "a", "GREEK ALPHA"),
            (0x0585, "o", "ARMENIAN OH"),
            (0x3002, chr(0x02F3), "IDEOGRAPHIC FULL STOP (maps to low ring, NOT dot)")]:
        got = full.get(cp)
        if got != want:
            fails.append("B confusables %s: U+%04X -> %r want %r" % (name, cp, got, want))
    if 0xFF0E in full:
        fails.append("B U+FF0E unexpectedly present in confusables (svod said absent)")

    # C. Scripts oracle.
    for cp, want in [(0x0430, "Cyrillic"), (0x0061, "Latin"), (0x0031, "Common"),
                     (0x03B1, "Greek"), (0x4E00, "Han"), (0x30A2, "Katakana"),
                     (0x0300, "Inherited"), (0x0561, "Armenian")]:
        got = ut.script_of(t, cp)
        if got != want:
            fails.append("C script U+%04X -> %r want %r" % (cp, got, want))
    # Script_Extensions oracle: U+30FC is Hira+Kana; plain Latin letter has no entry.
    se = ut.script_extensions_of(t, 0x30FC)
    if se != ("Hira", "Kana"):
        fails.append("C script_ext U+30FC -> %r want ('Hira','Kana')" % (se,))
    if ut.script_extensions_of(t, 0x0061) is not None:
        fails.append("C script_ext U+0061 should have no entry")

    # D. D6 deferral: 4 disputed sources in FULL, not in ACTIVE, delta exactly 4.
    for cp in sorted(ut.DEFERRED_SOURCES):
        if cp not in full:
            fails.append("D deferred U+%04X missing from full map" % cp)
        if cp in active:
            fails.append("D deferred U+%04X leaked into active map" % cp)
    if len(full) - len(active) != len(ut.DEFERRED_SOURCES):
        fails.append("D full-active delta %d != %d" % (
            len(full) - len(active), len(ut.DEFERRED_SOURCES)))
    if len(full) < 5000:
        fails.append("D suspiciously small confusables map: %d" % len(full))

# E. Fail-visible on tamper + on missing artifacts (no exception, no fallback).
tmp = tempfile.mkdtemp(prefix="w7pin_")
try:
    for fname in ut.PINNED_SHA256:
        shutil.copy(os.path.join(ut._DEFAULT_DIR, fname), os.path.join(tmp, fname))
    with open(os.path.join(tmp, "confusables.txt"), "ab") as f:
        f.write(b"\n# tampered\n")
    bad = ut.load_tables(base_dir=tmp)
    if bad["status"] != "CONFUSABLE_AXIS_UNVERIFIABLE" or \
            "confusables.txt" not in bad.get("reason", ""):
        fails.append("E tamper not detected: %s" % bad)
    empty = tempfile.mkdtemp(prefix="w7pin_empty_")
    try:
        miss = ut.load_tables(base_dir=empty)
        if miss["status"] != "CONFUSABLE_AXIS_UNVERIFIABLE":
            fails.append("E missing artifacts not detected: %s" % miss)
    finally:
        shutil.rmtree(empty, ignore_errors=True)
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print("=" * 66)
print("GATE: W7 pinned Unicode tables (B3/S3 oracle)")
print("=" * 66)
if fails:
    for f in fails:
        print("  FAIL: " + f)
    print("\nTOTAL: FAIL")
    sys.exit(1)
print("A pins verified (sha256 x3 + unidata_version %s)" % ut.PINNED_UNIDATA_VERSION)
print("B confusables oracle (cyr-a/cyr-o/alpha/armenian-oh; U+3002 -> low ring; no U+FF0E)")
print("C Scripts + Script_Extensions oracle (8 scripts + Hira/Kana)")
print("D deferral D6: full minus active == exactly 4 disputed sources")
print("E fail-visible: tampered + missing artifacts -> UNVERIFIABLE, no fallback")
print("\nTOTAL: CLEAN")
sys.exit(0)
