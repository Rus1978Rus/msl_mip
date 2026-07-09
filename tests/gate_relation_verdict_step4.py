#!/usr/bin/env python3
"""
GATE: шаг 4 оси «отношение» — вердикт маски в sequence-слое.

Основание: AUTHOR_DECISION_20260708 (D-REL-4/6) + решения ревью шага 4:
  D1 — шкала: HOST→HIGH, URL/PATH→MEDIUM, FREE_TEXT→NONE;
       CANDIDATE-ребро понижает на ступень.
  D2 — грубый HOST-детектор (главный кейс gоog／le.com).
  D3 — зонд отложен: canon_hypothesis остаётся None.
  Барьер N3 — вердикт только по active_relation_candidates;
              выключенные рёбра НЕ влияют.

Проверяется вживую через process_sign + process_sequence.
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
print("GATE: шаг 4 — вердикт маски (ось «отношение»)")
print("=" * 60)

# --- 1. Шкала риска по контексту (D1) ---
print("\n[1] Шкала риска по контексту (VERIFIED ребро)")
v = _card(VERIFIED_CARD)

vd = _verdict(v, "http://gоog／le.com")
check("HOST → HIGH", vd and vd[0]["risk_level"] == "HIGH", vd)
check("HOST → detected_context=HOST", vd and vd[0]["detected_context"] == "HOST")

vd = _verdict(v, "http://ok.com/a／b")
check("PATH → MEDIUM", vd and vd[0]["risk_level"] == "MEDIUM", vd)

vd = _verdict(v, "просто ／ текст")
check("FREE_TEXT → NONE (RELATION_FOUND ≠ THREAT)",
      vd and vd[0]["risk_level"] == "NONE", vd)
check("FREE_TEXT → protected=False", vd and vd[0]["protected"] is False)

# --- 2. CANDIDATE-понижение (D1) ---
print("\n[2] CANDIDATE-ребро понижает риск на ступень")
c = _card(CANDIDATE_CARD)
vd = _verdict(c, "http://gоog／le.com")
check("CANDIDATE в HOST → MEDIUM (не HIGH)",
      vd and vd[0]["risk_level"] == "MEDIUM", vd)

# --- 3. Зонд отложен (D3) ---
print("\n[3] Зонд канона отложен")
vd = _verdict(v, "http://gоog／le.com")
check("canon_hypothesis = None", vd and vd[0]["canon_hypothesis"] is None)

# --- 4. Барьер N3: disabled не влияет на вердикт ---
print("\n[4] Барьер N3 — выключенное ребро не даёт вердикт")
mx = _card(MIXED_CARD)
off = "http://x／y.com".index("／")
st = process_sign(mx, "http://x／y.com", off)
check("в кандидате ВСЕ рёбра (отладка): 2",
      len(st.relation_candidates) == 2, len(st.relation_candidates))
check("active_relation_candidates: только 1",
      len(st.active_relation_candidates) == 1)
out = process_sequence("http://x／y.com", [mx], sign_statuses=[st],
                       known_signs={"／"})
check("вердикт ровно 1 (по активному ребру U+002F)",
      len(out.relation_verdicts) == 1, len(out.relation_verdicts))
check("выключенное ребро U+2044 в вердиктах ОТСУТСТВУЕТ",
      all(rv["target"] != "U+2044" for rv in out.relation_verdicts))

# --- 5. D1: legacy знаки не задеты ---
print("\n[5] D1 — legacy карточки без relations не дают вердиктов")
legacy = load_card(os.path.join(
    BASE, "cards", "SIGN_CORE_CARD_SOLIDUS_U002F_GEN3_v0_3_RU__1_.md"))
from module_engine import process_sign as ps
st = ps(legacy, "http://ok.com/path", 5)  # обычный /
out = process_sequence("http://ok.com/path", [legacy],
                       sign_statuses=[st], known_signs={"/"})
check("обычный / не порождает relation_verdicts",
      out.relation_verdicts == [], out.relation_verdicts)

print("\n" + "=" * 60)
print(f"ИТОГО: {PASSED} OK / {FAILED} FAIL")
print("=" * 60)
sys.exit(1 if FAILED else 0)
