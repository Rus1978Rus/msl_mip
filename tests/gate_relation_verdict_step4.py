#!/usr/bin/env python3
"""
GATE: relation-axis step 4 — mask verdict in the sequence layer.

Basis: AUTHOR_DECISION_20260708 (D-REL-4/6) + step-4 review decisions:
  D1 — scale: HOST->HIGH, URL/PATH->MEDIUM, FREE_TEXT->NONE;
       a CANDIDATE edge downgrades one step.
  D2 — rough HOST detector (main gоog／le.com case).
  D3 — probe deferred: canon_hypothesis stays None.
  Barrier N3 — verdict only from active_relation_candidates;
              disabled edges have NO effect.

Verified live via process_sign + process_sequence.
"""

import os
import sys
import tempfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "core"))
sys.path.insert(0, os.path.join(BASE, "single_sign"))
sys.path.insert(0, os.path.join(BASE, "sequence"))

from load_card import load_card
from module_engine import process_sign
from sequence_engine import process_sequence

PASSED = 0
FAILED = 0


def check(label, cond, detail=""):
    global PASSED, FAILED
    if cond:
        PASSED += 1
        print(f"  ✓ {label}")
    else:
        FAILED += 1
        print(f"  ✗ {label} {detail}")


def _card(text):
    f = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False,
                                    encoding="utf-8")
    f.write(text)
    f.close()
    return load_card(f.name)


def _verdict(card, text):
    off = text.index("／")
    st = process_sign(card, text, off)
    out = process_sequence(text, [card], sign_statuses=[st],
                           known_signs={"／"})
    return out.relation_verdicts


VERIFIED_CARD = """CARD_UID: V
CODEPOINT: U+FF0F
VISIBLE_FORM: ／
UNICODE_NAME: FULLWIDTH SOLIDUS
ZONE: ZONE_1
DOCUMENT_STATUS: WORKING_DRAFT
SIGN_RELATIONS:
  RELATION_001:
    RELATION_TYPE: CONFUSABLE_OF
    TARGET: U+002F
    CONTEXT_SCOPE: URL, HOST, PATH
    VERIFICATION_STATUS: VERIFIED
    RUNTIME_EFFECT: RELATION_ONLY
"""

CANDIDATE_CARD = """CARD_UID: C
CODEPOINT: U+FF0F
VISIBLE_FORM: ／
UNICODE_NAME: FULLWIDTH SOLIDUS
ZONE: ZONE_1
DOCUMENT_STATUS: WORKING_DRAFT
SIGN_RELATIONS:
  RELATION_001:
    RELATION_TYPE: CONFUSABLE_OF
    TARGET: U+002F
    CONTEXT_SCOPE: HOST
    VERIFICATION_STATUS: CANDIDATE
    RUNTIME_EFFECT: RELATION_ONLY
"""

MIXED_CARD = """CARD_UID: MX
CODEPOINT: U+FF0F
VISIBLE_FORM: ／
UNICODE_NAME: FULLWIDTH SOLIDUS
ZONE: ZONE_1
DOCUMENT_STATUS: WORKING_DRAFT
SIGN_RELATIONS:
  RELATION_001:
    RELATION_TYPE: CONFUSABLE_OF
    TARGET: U+002F
    CONTEXT_SCOPE: HOST
    VERIFICATION_STATUS: VERIFIED
    RUNTIME_EFFECT: RELATION_ONLY
  RELATION_002:
    RELATION_TYPE: VISUAL_MIMIC_OF
    TARGET: U+2044
    CONTEXT_SCOPE: HOST
    IS_ACTIVE: FALSE
    VERIFICATION_STATUS: VERIFIED
    RUNTIME_EFFECT: RELATION_ONLY
"""

print("=" * 60)
print("GATE: step 4 — mask verdict (relation axis)")
print("=" * 60)

# --- 1. Risk scale by context (D1) ---
print("\n[1] Risk scale by context (VERIFIED edge)")
v = _card(VERIFIED_CARD)

vd = _verdict(v, "http://gоog／le.com")
check("HOST -> HIGH", vd and vd[0]["risk_level"] == "HIGH", vd)
check("HOST -> detected_context=HOST", vd and vd[0]["detected_context"] == "HOST")

vd = _verdict(v, "http://ok.com/a／b")
check("PATH -> MEDIUM", vd and vd[0]["risk_level"] == "MEDIUM", vd)

vd = _verdict(v, "just ／ text")
check("FREE_TEXT -> NONE (RELATION_FOUND != THREAT)",
      vd and vd[0]["risk_level"] == "NONE", vd)
check("FREE_TEXT -> protected=False", vd and vd[0]["protected"] is False)

# --- 2. CANDIDATE downgrade (D1) ---
print("\n[2] A CANDIDATE edge downgrades risk one step")
c = _card(CANDIDATE_CARD)
vd = _verdict(c, "http://gоog／le.com")
check("CANDIDATE in HOST -> MEDIUM (not HIGH)",
      vd and vd[0]["risk_level"] == "MEDIUM", vd)

# --- 3. Probe deferred (D3) ---
print("\n[3] Canon probe deferred")
vd = _verdict(v, "http://gоog／le.com")
check("canon_hypothesis = None", vd and vd[0]["canon_hypothesis"] is None)

# --- 4. Barrier N3: disabled does not affect the verdict ---
print("\n[4] Barrier N3 — a disabled edge yields no verdict")
mx = _card(MIXED_CARD)
off = "http://x／y.com".index("／")
st = process_sign(mx, "http://x／y.com", off)
check("ALL edges in the candidate (debug): 2",
      len(st.relation_candidates) == 2, len(st.relation_candidates))
check("active_relation_candidates: only 1",
      len(st.active_relation_candidates) == 1)
out = process_sequence("http://x／y.com", [mx], sign_statuses=[st],
                       known_signs={"／"})
check("exactly 1 verdict (from the active U+002F edge)",
      len(out.relation_verdicts) == 1, len(out.relation_verdicts))
check("the disabled U+2044 edge is ABSENT from verdicts",
      all(rv["target"] != "U+2044" for rv in out.relation_verdicts))

# --- 5. D1: legacy signs untouched ---
print("\n[5] D1 — legacy cards without relations yield no verdicts")
legacy = load_card(os.path.join(
    BASE, "cards", "SIGN_CORE_CARD_SOLIDUS_U002F_GEN3_v0_3_RU__1_.md"))
from module_engine import process_sign as ps
st = ps(legacy, "http://ok.com/path", 5)  # an ordinary /
out = process_sequence("http://ok.com/path", [legacy],
                       sign_statuses=[st], known_signs={"/"})
check("an ordinary / produces no relation_verdicts",
      out.relation_verdicts == [], out.relation_verdicts)

print("\n" + "=" * 60)
print(f"TOTAL: {PASSED} OK / {FAILED} FAIL")
print("=" * 60)
sys.exit(1 if FAILED else 0)
