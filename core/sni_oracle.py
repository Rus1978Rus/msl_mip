# -*- coding: utf-8 -*-
"""Functional-position oracle for the card layer (D-SNI, SNI_SVOD_AND_SIM 2026-08-06).

First round to touch the card layer. The measured defect: BOUNDARY_DISRUPTOR fired
identically on Latin ZWSP (an anomaly) and on Khmer ZWSP (the script's word separator),
so the card queued 100% of normal text in nine writing systems -- a verdict with zero
specificity. The round's converged fix judges the FUNCTION OF THE POSITION, never the
script alone and never the writing system as a whole:

  ZWSP -- functional word-boundary candidate when BOTH significant neighbours carry
          Line_Break=SA (UAX#14): the property of complex-context scripts whose
          orthography separates words with ZWSP instead of spaces. Both neighbours,
          not one: the attacker owns both sides of every inserted character, and the
          one-neighbour variant was measured as a full amnesty (62/62 carriers).
  ZWJ  -- functional conjunct/chillu joiner when the IMMEDIATE left neighbour has
          InCB=Linker (UAX#29 GB9c): exactly six viramas. Script equality cannot see
          this -- Devanagari with and without the virama has identical neighbour
          scripts; only the linker separates conjunct from anomaly. No right-neighbour
          requirement: the Malayalam legacy chillu is precisely virama+ZWJ at the end
          of a word, and demanding a consonant after it would keep 6 queue per
          document on normative text (measured by the round).
  ZWNJ -- no card, no exemption to grant.
  BOM  -- NEVER exempt: its role is transport-level and script-independent.

Both tables are machine-derived from files pinned under the existing UCD 16.0.0 pin
(dissent D1 resolved: a derivative requires a pinned input -- the hand-written
"4 scripts" constant was already short against the normative 9). A hash mismatch is
SNI_UNVERIFIABLE and grants NOTHING: unknown is not amnesty, and the status is
surfaced in the report rather than swallowed. Zero numeric thresholds by construction.
"""
import hashlib
import os
import unicodedata

ZWSP, ZWJ = 0x200B, 0x200D

_LB_FILE = "LineBreak.txt"
_LB_SHA256 = "e97e4259d0d20fab150b9c7b4b28abfae5cd78ca97e7f4ac6ed20d685d5f4a7c"
_DCP_FILE = "DerivedCoreProperties.txt"
_DCP_SHA256 = "39d35161f2954497f69e08bdb9e701493f476a3d30222de20028feda36c1dabd"
# Guards on the machine-derived sets: the exact counts measured from the pinned
# files and confirmed against the round's independent census (757 / 6). A parse
# drift that changes either count is a fail, not a silent new behaviour.
_SA_EXPECT = 757
_LINKER_EXPECT = 6

_DEFAULT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "unicode")
_TABLES = None


def _sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _parse_ranges(path, want_prop, subprop=None):
    """Collect codepoints from 'range;prop[;value]' UCD lines. With subprop, match
    files like DerivedCoreProperties where the property has a value column
    (`094D ; InCB; Linker`)."""
    out = set()
    with open(path, "r", encoding="utf-8-sig") as f:
        for line in f:
            line = line.split("#", 1)[0].strip()
            if not line:
                continue
            parts = [p.strip() for p in line.split(";")]
            if subprop is None:
                if len(parts) < 2 or parts[1].split()[0] != want_prop:
                    continue
            else:
                if len(parts) < 3 or parts[1] != want_prop or parts[2] != subprop:
                    continue
            rng = parts[0]
            if ".." in rng:
                lo, hi = rng.split("..")
                lo, hi = int(lo, 16), int(hi, 16)
            else:
                lo = hi = int(rng, 16)
            out.update(range(lo, hi + 1))
    return out


def load_sni_tables(base_dir=None):
    """Pinned SA + InCB=Linker sets. Fail-visible: any missing file, hash mismatch,
    parse failure or count drift -> SNI_UNVERIFIABLE with empty sets, and the
    exemption below grants nothing."""
    base = base_dir or _DEFAULT_DIR
    for fname, sha in ((_LB_FILE, _LB_SHA256), (_DCP_FILE, _DCP_SHA256)):
        path = os.path.join(base, fname)
        if not os.path.isfile(path):
            return {"status": "SNI_UNVERIFIABLE", "reason": "missing %s" % fname,
                    "sa": frozenset(), "incb_linker": frozenset()}
        if _sha256_file(path) != sha:
            return {"status": "SNI_UNVERIFIABLE",
                    "reason": "sha256 mismatch for %s" % fname,
                    "sa": frozenset(), "incb_linker": frozenset()}
    try:
        sa = frozenset(_parse_ranges(os.path.join(base, _LB_FILE), "SA"))
        linker = frozenset(
            _parse_ranges(os.path.join(base, _DCP_FILE), "InCB", "Linker"))
    except (OSError, ValueError) as exc:
        return {"status": "SNI_UNVERIFIABLE", "reason": "parse failure: %s" % exc,
                "sa": frozenset(), "incb_linker": frozenset()}
    if len(sa) != _SA_EXPECT or len(linker) != _LINKER_EXPECT:
        return {"status": "SNI_UNVERIFIABLE",
                "reason": "derived count drift: SA=%d InCB_Linker=%d"
                          % (len(sa), len(linker)),
                "sa": frozenset(), "incb_linker": frozenset()}
    return {"status": "OK", "sa": sa, "incb_linker": linker}


def get_sni_tables():
    global _TABLES
    if _TABLES is None:
        _TABLES = load_sni_tables()
    return _TABLES


def _transparent(ch):
    """Characters skipped when seeking a SIGNIFICANT neighbour for the ZWSP rule:
    nonspacing/enclosing marks and other invisibles carry no script evidence of
    their own. Punctuation and digits are NOT transparent -- a letter|ZWSP|digit
    boundary stays queued (named residual SNI-FP-SA-DIGIT-PUNCT-BOUNDARY: the
    price of strictness, taken knowingly over an amnesty edge)."""
    return unicodedata.category(ch) in ("Mn", "Me", "Cf")


def functional_position(text, i):
    """Basis string when the sign at offset i occupies a NORMATIVE functional
    position ('SA_BOUNDARY' / 'INCB_LINKER'), else None. None means only 'no
    exemption here' -- it is never a claim of malice. Fail-closed: with the
    tables UNVERIFIABLE every answer is None."""
    tables = get_sni_tables()
    if tables["status"] != "OK":
        return None
    cp = ord(text[i])
    if cp == ZWSP:
        j = i - 1
        while j >= 0 and _transparent(text[j]):
            j -= 1
        k = i + 1
        while k < len(text) and _transparent(text[k]):
            k += 1
        if j >= 0 and k < len(text) \
                and ord(text[j]) in tables["sa"] and ord(text[k]) in tables["sa"]:
            return "SA_BOUNDARY"
        return None
    if cp == ZWJ:
        # Immediate neighbour on purpose: the linker is category Mn, so a
        # transparent skip would step over the very character that carries the
        # evidence (same trap the ZW-BITS virama rule hit, caught by its gate).
        if i > 0 and ord(text[i - 1]) in tables["incb_linker"]:
            return "INCB_LINKER"
        return None
    return None
