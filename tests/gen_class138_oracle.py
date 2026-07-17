# -*- coding: utf-8 -*-
"""Generate the supervised-class (class-138) oracle manifest, machine-built.

Predicate (D-NEIGHBORS-BORDER-138): General_Category == Cf AND
Default_Ignorable_Code_Point == True. This enumerates EVERY member of the
supervised class, not the 5 card exemplars. It supersedes the old 22-member
ORACLE_ZWSP_NEIGHBORS (predicate-22, commit 5476d9d).

Data channels (honest provenance):
  - gc / bidi / name : unicodedata (bundled UCD, currently 16.0.0)
  - Default_Ignorable: pinned tools/sources/<ver>/DerivedCoreProperties.txt via
    msl_mip_runtime._default_ignorable_set() (currently UCD_17.0.0)
Cf and Cf∧DI are identical on UCD 16.0 and 17.0 (verified 2026-07-17, see the
BORDER-138 decision VERIFICATION block); the number 138 is version-stable.

Run: PYTHONUTF8=1 MSL_MIP_HERMETIC_TLD=1 py -3 tests/gen_class138_oracle.py
Writes conveyor_runs/oracle_class_138_2026-07-17.json (deterministic).
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unicodedata as u
import msl_mip_runtime as rt

TARGET = 0x200B                                  # ZWSP, the card subject
IN_CARD = {0x200C, 0x200D, 0x2060, 0xFEFF, 0x00AD}  # 5 card exemplars (obraztsy)

DIRECTIONAL_BIDI = {"L","R","AL","LRE","RLE","PDF","LRO","RLO","LRI","RLI","FSI","PDI"}

def is_tag(cp): return cp == 0xE0001 or 0xE0020 <= cp <= 0xE007F
def is_deprecated(cp): return 0x206A <= cp <= 0x206F

def bucket(cp):
    if is_tag(cp): return "TAG"
    if is_deprecated(cp): return "DEPRECATED"
    if u.bidirectional(chr(cp)) in DIRECTIONAL_BIDI: return "DIRECTIONAL"
    return "PURE"

def build():
    di_set, di_src = rt._default_ignorable_set()
    members = sorted(cp for cp in di_set if u.category(chr(cp)) == "Cf")
    rows = [dict(
        cp="U+%04X" % cp, codepoint=cp, name=u.name(chr(cp), "<no name>"),
        gc=u.category(chr(cp)), bidi=u.bidirectional(chr(cp)), di=True,
        bucket=bucket(cp), is_target=(cp == TARGET), in_card=(cp in IN_CARD),
    ) for cp in members]
    counts = {k: sum(1 for r in rows if r["bucket"] == k)
              for k in ("PURE", "DIRECTIONAL", "TAG", "DEPRECATED")}
    return dict(
        schema="ORACLE_CLASS_138_v0_1",
        predicate="General_Category==Cf AND Default_Ignorable_Code_Point==True",
        di_source=di_src, unicodedata_ucd=u.unidata_version,
        target="U+200B", total=len(rows), buckets=counts,
        in_card_count=sum(1 for r in rows if r["in_card"]), members=rows,
    )

def main():
    manifest = build()
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "conveyor_runs", "oracle_class_138_2026-07-17.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
    assert manifest["total"] == 138, manifest["total"]
    assert manifest["buckets"] == {"PURE":23,"DIRECTIONAL":12,"TAG":97,"DEPRECATED":6}
    assert manifest["in_card_count"] == 5
    print("OK total=%d buckets=%s in_card=%d di_source=%s ucd=%s" % (
        manifest["total"], manifest["buckets"], manifest["in_card_count"],
        manifest["di_source"], manifest["unicodedata_ucd"]))
    print("wrote", out)

if __name__ == "__main__":
    main()
