# -*- coding: utf-8 -*-
"""Reproduce the run-backed numbers behind D-SUBSTITUTION-OP-COMPOSITION from the repo.

Verifies (by run, not by reviewer claim) the facts recorded in
foundation_layer/AUTHOR_DECISION_20260717_D-SUBSTITUTION-OP-COMPOSITION.md:
  - supervised class = Cf AND Default_Ignorable = 138 (buckets 23/12/97/6)
  - IDNA behaviour on the class, IDNA2003/stringprep proxy (stdlib, local):
      REMOVED (mapped-to-nothing, stringprep table B.1) = 6 (all PURE)
      PROHIBITED (bidi, stringprep table C.8)           = 13 (7 DIRECTIONAL + 6 DEPRECATED)
    -> IDNA is heterogeneous (remove / prohibit / pass), NOT a clean strip; thin as an
       edge generator. Supports R1's CO_REJECTED != SUBSTITUTABLE (prohibited != a key).
  - the Qwen OP-1 6-codepoint list is a valid subset of the class (all Cf, DI, bidi==BN)
  - U+FF0F FULLWIDTH SOLIDUS: NFKC -> "/", and it is OUTSIDE the class (Qwen cross-class)

NOTE: UTS-46 / IDNA2008 (the third-party `idna` package) is NOT required here; the
per-codepoint UTS-46 statuses some reviewers gave are NOT run-verified by this test.
This test uses only the stdlib IDNA2003/stringprep tables.

Run: PYTHONUTF8=1 MSL_MIP_HERMETIC_TLD=1 py -3 tests/verify_op_composition.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unicodedata as u
import stringprep
import msl_mip_runtime as rt

DIRECTIONAL_BIDI = {"L","R","AL","LRE","RLE","PDF","LRO","RLO","LRI","RLI","FSI","PDI"}


def class_members():
    di_set, _ = rt._default_ignorable_set()
    return sorted(cp for cp in di_set if u.category(chr(cp)) == "Cf")


def is_tag(cp): return cp == 0xE0001 or 0xE0020 <= cp <= 0xE007F
def is_deprecated(cp): return 0x206A <= cp <= 0x206F


def bucket(cp):
    if is_tag(cp): return "TAG"
    if is_deprecated(cp): return "DEPRECATED"
    if u.bidirectional(chr(cp)) in DIRECTIONAL_BIDI: return "DIRECTIONAL"
    return "PURE"


def main():
    members = class_members()
    cls = set(members)
    assert len(members) == 138, len(members)

    counts = {k: sum(1 for cp in members if bucket(cp) == k)
              for k in ("PURE", "DIRECTIONAL", "TAG", "DEPRECATED")}
    assert counts == {"PURE": 23, "DIRECTIONAL": 12, "TAG": 97, "DEPRECATED": 6}, counts

    # IDNA2003 / stringprep proxy
    removed = [cp for cp in members if stringprep.in_table_b1(chr(cp))]
    prohibited = [cp for cp in members if stringprep.in_table_c8(chr(cp))]
    assert len(removed) == 6, len(removed)
    assert all(bucket(cp) == "PURE" for cp in removed), removed
    assert len(prohibited) == 13, len(prohibited)
    prob_buckets = sorted(bucket(cp) for cp in prohibited)
    assert prob_buckets.count("DIRECTIONAL") == 7 and prob_buckets.count("DEPRECATED") == 6, prob_buckets

    # Qwen OP-1 6-codepoint list is a valid subset of the class
    q6 = [0x00AD, 0x200B, 0x200C, 0x200D, 0x2060, 0xFEFF]
    assert all(cp in cls for cp in q6), q6
    assert all(u.category(chr(cp)) == "Cf" for cp in q6), q6
    assert all(u.bidirectional(chr(cp)) == "BN" for cp in q6), q6

    # Qwen cross-class example: U+FF0F is outside the class and NFKC-folds to "/"
    assert 0xFF0F not in cls
    assert u.normalize("NFKC", chr(0xFF0F)) == "/"

    print("OK class=138 buckets=%s" % counts)
    print("OK IDNA2003 proxy: removed(B.1)=6 (all PURE), prohibited(C.8)=13 (7 DIR + 6 DEP)")
    print("OK Qwen OP-1 6-list valid subset; U+FF0F outside class, NFKC->'/'")
    print("unicodedata UCD: %s" % u.unidata_version)


if __name__ == "__main__":
    main()
