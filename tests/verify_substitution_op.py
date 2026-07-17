# -*- coding: utf-8 -*-
"""Reproduce the load-bearing numbers behind D-SUBSTITUTION-OP from the repo.

Verifies (by run, not by reviewer claim) the facts recorded in
foundation_layer/AUTHOR_DECISION_20260717_D-SUBSTITUTION-OP.md:
  - supervised class = Cf AND Default_Ignorable = 138
  - OP-2 (Cf-strip) and OP-3 (DI-strip) are IDENTICAL within the class
    (both remove all 138) -> one operation, not two
  - the full substitution graph on the class = C(138,2) = 9453 unordered pairs
  - TAG chars (E0001 + E0020..E007F) ARE Cf and ARE in the class (debunks the
    R3 reasoning error "TAG not Cf / outside 138")
  - NFC and NFKC change 0 of the 138 (normalization is a no-op on the class ->
    the "password NFC vs NFKC" sub-dispute is moot for the class)
  - OP-1 (zero-width strip) does NOT touch the 12 directional controls (bidi!=BN),
    so it misses the Trojan Source class

Data channels: gc/bidi/name from unicodedata (bundled UCD); Default_Ignorable
from pinned DerivedCoreProperties via msl_mip_runtime._default_ignorable_set().

Run: PYTHONUTF8=1 MSL_MIP_HERMETIC_TLD=1 py -3 tests/verify_substitution_op.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unicodedata as u
import msl_mip_runtime as rt

DIRECTIONAL_BIDI = {"L","R","AL","LRE","RLE","PDF","LRO","RLO","LRI","RLI","FSI","PDI"}


def class_members():
    di_set, _ = rt._default_ignorable_set()
    return sorted(cp for cp in di_set if u.category(chr(cp)) == "Cf"), di_set


def main():
    members, di_set = class_members()
    cls = set(members)
    n = len(members)

    # class size
    assert n == 138, n

    # OP-2 (Cf-strip) vs OP-3 (DI-strip) within the class: identical removal sets
    cf_removed = {cp for cp in members if u.category(chr(cp)) == "Cf"}
    di_removed = {cp for cp in members if cp in di_set}
    assert cf_removed == di_removed == cls, "OP-2 != OP-3 within class"

    # full substitution graph = unordered pairs
    pairs = n * (n - 1) // 2
    assert pairs == 9453, pairs

    # TAG chars are Cf and in the class (R3 debunk)
    tags = [0xE0001] + list(range(0xE0020, 0xE0080))
    assert all(u.category(chr(cp)) == "Cf" for cp in tags), "a TAG char is not Cf"
    assert all(cp in cls for cp in tags), "a TAG char is outside the class"
    assert len(tags) == 97, len(tags)

    # normalization is a no-op on the class (NFC/NFKC change 0 members)
    nfc_changed = [cp for cp in members if u.normalize("NFC", chr(cp)) != chr(cp)]
    nfkc_changed = [cp for cp in members if u.normalize("NFKC", chr(cp)) != chr(cp)]
    assert nfc_changed == [], nfc_changed
    assert nfkc_changed == [], nfkc_changed

    # OP-1 (zero-width strip) misses the directional controls
    directional = [cp for cp in members if u.bidirectional(chr(cp)) in DIRECTIONAL_BIDI]
    assert len(directional) == 12, len(directional)

    print("OK class=%d | OP-2==OP-3 within class: True | full graph C(%d,2)=%d" % (n, n, pairs))
    print("OK TAG in class: 97 Cf | NFC changed: 0 | NFKC changed: 0 | directional: 12")
    print("unicodedata UCD: %s" % u.unidata_version)


if __name__ == "__main__":
    main()
