#!/usr/bin/env python3
"""
GATE: invisible-sign ZWSP (U+200B) — FIX_FIRST round 1.

Basis: AUTHOR_DECISION_20260712 D-INV-1/2/3 + the ZWSP card first-round
review. This gate pins "promises == reality": every context/level the card
now claims is asserted against what the live pipeline actually produces.

Three levels + the witness registrar:
  L1 (contexts): EMAIL / BYTE_EXACT_TOKEN / PATH are really detected, not
     just named on the card (they used to fall through to FREE_TEXT/NONE).
  L2 (type as contract, not label): ZWSP gives ONE independent verdict via
     BOUNDARY_DISRUPTOR (PRIMARY). ABSENCE_CONFUSABLE (SUPPORTING_FACET) and
     INVISIBLE_CLASS_COLLISION (TAXONOMY_ONLY) emit NONE — the "three names,
     one path" duplicate HIGH is gone.
  L3 (target_kind enforcement): a contract-invalid edge is neither silently
     activated nor silently dropped — it is EXCLUDED and SURFACED.
  Registrar: an uncarded invisible is surfaced as an UNVERIFIABLE witness,
     never a verdict; a carded invisible (ZWSP) is NOT re-reported here.

The only non-ASCII literals are the signs themselves (ZWSP U+200B, fullwidth
solidus U+FF0F, invisible-times U+2062) — none are Cyrillic, so the
english-only gate (which flags U+0400..U+04FF) stays clean.

GATE_MUST_BE_HERMETIC: pin the offline TLD set before any import can fetch.
"""

import os
import sys
import tempfile

os.environ["MSL_MIP_HERMETIC_TLD"] = "1"

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)
sys.path.insert(0, os.path.join(BASE, "core"))
sys.path.insert(0, os.path.join(BASE, "single_sign"))
sys.path.insert(0, os.path.join(BASE, "sequence"))

from load_card import load_card
from module_engine import process_sign
from sequence_engine import process_sequence
import msl_mip_runtime as rt

ZWSP = "​"
FWSOL = "／"     # fullwidth solidus (the mask sign)
ITIMES = "⁢"    # INVISIBLE TIMES — an uncarded invisible (Cf)

PASSED = 0
FAILED = 0


def check(label, cond, detail=""):
    global PASSED, FAILED
    if cond:
        PASSED += 1
        print(f"  [ok] {label}")
    else:
        FAILED += 1
        print(f"  [XX] {label} :: {detail}")


ZCARD = load_card(os.path.join(
    BASE, "cards", "SIGN_CORE_CARD_ZERO_WIDTH_SPACE_U200B_GEN3_v0_3_RU.md"))
MCARD = load_card(os.path.join(
    BASE, "cards", "SIGN_CORE_CARD_FULLWIDTH_SOLIDUS_UFF0F_GEN3_v0_3_RU.md"))


def verdicts(text, cards):
    known = {c.visible_form for c in cards}
    sign_statuses = []
    for i, ch in enumerate(text):
        for c in cards:
            if ch == c.visible_form:
                sign_statuses.append(process_sign(c, text, i))
    out = process_sequence(text, cards, sign_statuses=sign_statuses,
                           known_signs=known)
    return out.relation_verdicts


def zwsp_by_type(text, cards):
    """ZWSP relation verdicts, keyed by relation_type."""
    return {v["relation_type"]: v
            for v in verdicts(text, cards) if v["visible_form"] == ZWSP}


print("=" * 60)
print("GATE: invisible ZWSP (U+200B) — FIX_FIRST round 1")
print("=" * 60)

# --- L1: contexts that the card promises are actually produced ---
print("\n[L1] Contexts really detected (were FREE_TEXT/NONE before)")

by = zwsp_by_type("https://example.com/pa" + ZWSP + "th", [ZCARD])
p = by.get("BOUNDARY_DISRUPTOR")
check("PATH soft-wrap -> context PATH", p and p["detected_context"] == "PATH", by)
check("PATH -> MEDIUM (not HIGH: cannot tell URL wrap from machine path)",
      p and p["risk_level"] == "MEDIUM", p)

by = zwsp_by_type("user" + ZWSP + "name@example.com", [ZCARD])
p = by.get("BOUNDARY_DISRUPTOR")
check("email local-part split -> context EMAIL", p and p["detected_context"] == "EMAIL", by)
check("EMAIL -> MEDIUM", p and p["risk_level"] == "MEDIUM", p)

by = zwsp_by_type("bad" + ZWSP + "word", [ZCARD])
p = by.get("BOUNDARY_DISRUPTOR")
check("keyword split -> context BYTE_EXACT_TOKEN", p and p["detected_context"] == "BYTE_EXACT_TOKEN", by)
check("BYTE_EXACT_TOKEN -> MEDIUM", p and p["risk_level"] == "MEDIUM", p)

by = zwsp_by_type("user" + ZWSP + "name", [ZCARD])
p = by.get("BOUNDARY_DISRUPTOR")
check("identifier split -> context BYTE_EXACT_TOKEN", p and p["detected_context"] == "BYTE_EXACT_TOKEN", by)

# regression-guard: a broken host must still be HOST/HIGH
by = zwsp_by_type("goog" + ZWSP + "le.com", [ZCARD])
p = by.get("BOUNDARY_DISRUPTOR")
check("host label break -> context HOST", p and p["detected_context"] == "HOST", by)
check("HOST -> HIGH (regression-guard)", p and p["risk_level"] == "HIGH", p)

# --- L2: type is a contract — one PRIMARY verdict, no duplicate HIGH ---
print("\n[L2] Type routing: one independent verdict, no 'three names, one path'")
by = zwsp_by_type("goog" + ZWSP + "le.com", [ZCARD])
check("BOUNDARY_DISRUPTOR runtime_role = PRIMARY",
      by.get("BOUNDARY_DISRUPTOR", {}).get("runtime_role") == "PRIMARY", by)
check("ABSENCE_CONFUSABLE runtime_role = SUPPORTING_FACET",
      by.get("ABSENCE_CONFUSABLE", {}).get("runtime_role") == "SUPPORTING_FACET", by)
check("INVISIBLE_CLASS_COLLISION runtime_role = TAXONOMY_ONLY",
      by.get("INVISIBLE_CLASS_COLLISION", {}).get("runtime_role") == "TAXONOMY_ONLY", by)
zhi = [v for v in by.values() if v["risk_level"] == "HIGH"]
check("exactly ONE ZWSP verdict is HIGH (duplicate removed)", len(zhi) == 1, zhi)
check("SUPPORTING_FACET emits NONE",
      by.get("ABSENCE_CONFUSABLE", {}).get("risk_level") == "NONE", by)
check("TAXONOMY_ONLY emits NONE",
      by.get("INVISIBLE_CLASS_COLLISION", {}).get("risk_level") == "NONE", by)

# combined ZWSP + mask on a host: both are independently HIGH (the known hole)
allv = verdicts("goog" + ZWSP + FWSOL + "le.com", [ZCARD, MCARD])
zhi = [v for v in allv if v["visible_form"] == ZWSP and v["risk_level"] == "HIGH"]
mhi = [v for v in allv if v["visible_form"] == FWSOL and v["risk_level"] == "HIGH"]
check("ZWSP+mask host: ZWSP HIGH exactly once", len(zhi) == 1, zhi)
check("ZWSP+mask host: mask HIGH exactly once", len(mhi) == 1, mhi)

# --- L3: a contract-invalid edge is excluded AND surfaced ---
print("\n[L3] Contract-invalid edge: not silently activated, not silently dropped")
INVALID_EDGE_CARD = (
    "CARD_UID: INV\n"
    "CODEPOINT: U+200B\n"
    "VISIBLE_FORM: " + ZWSP + "\n"
    "UNICODE_NAME: ZERO WIDTH SPACE\n"
    "ZONE: ZONE_2\n"
    "DOCUMENT_STATUS: WORKING_DRAFT\n"
    "SIGN_RELATIONS:\n"
    "  RELATION_001:\n"
    "    RELATION_TYPE: BOUNDARY_DISRUPTOR\n"
    "    TARGET_KIND: CODEPOINT\n"           # CODEPOINT but no TARGET -> INVALID
    "    CONTEXT_SCOPE: HOST\n"
    "    VERIFICATION_STATUS: VERIFIED\n"
    "    RUNTIME_EFFECT: RELATION_ONLY\n"
)
f = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8")
f.write(INVALID_EDGE_CARD)
f.close()
badcard = load_card(f.name)
check("parser marks the edge invalid=True", badcard.relations[0].invalid is True,
      badcard.relations[0].validation_warnings)
st = process_sign(badcard, "goog" + ZWSP + "le.com", len("goog"))
check("invalid edge present in debug candidates (not dropped)",
      len(st.relation_candidates) == 1, st.relation_candidates)
check("invalid edge EXCLUDED from active candidates (not activated)",
      len(st.active_relation_candidates) == 0, st.active_relation_candidates)
check("invalid edge SURFACED as a warning",
      any("INVALID_EDGE_NOT_ACTIVATED" in w for w in st.output_warnings),
      st.output_warnings)

# --- Registrar: witness for uncarded invisibles, silent for carded ---
print("\n[REG] Uncarded-invisible registrar (witness, never a verdict)")
cards = [ZCARD, MCARD]
recs = rt.scan_uncarded_invisibles("goog" + ITIMES + "le.com", cards)
check("uncarded U+2062 surfaced", len(recs) == 1 and recs[0]["codepoint"] == "U+2062", recs)
check("surfaced as UNVERIFIABLE (not safe, not dangerous)",
      recs and recs[0]["finding_status"] == "UNVERIFIABLE", recs)
check("surfaced card_status NOT_CREATED", recs and recs[0]["card_status"] == "NOT_CREATED", recs)
recs2 = rt.scan_uncarded_invisibles("goog" + ZWSP + "le.com", cards)
check("carded ZWSP is NOT re-reported by the registrar", recs2 == [], recs2)
# the registrar must not change the verdict: analyze() keeps it out of the action
rep = rt.analyze("goog" + ITIMES + "le.com", cards)
check("registrar record does NOT enter the verdict (stays pass)",
      rep["semantic_action"] == "pass" and rep["effective_action"] == "pass",
      (rep["semantic_action"], rep["effective_action"]))
check("registrar record IS present in the report (surfaced to the human)",
      len(rep["uncarded_invisibles"]) == 1, rep["uncarded_invisibles"])

print("\n" + "=" * 60)
print(f"TOTAL: {PASSED} OK / {FAILED} FAIL")
print("=" * 60)
sys.exit(1 if FAILED else 0)
