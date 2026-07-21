# -*- coding: utf-8 -*-
"""GATE: O1 increment-0 -- zero-delta + engine self-test + SEAM-LIVENESS.

Parts, all must pass:

PART A (engine self-test, in-process): the active registry lints clean; every kind of
  malformed row is REJECTED by the linter (so the linter is real, not decorative); the
  seam is inert with an empty registry; and the engine is LIVE (an injected row raises
  + audits, raise-only), so a green zero-delta is because the registry is EMPTY.

PART B (zero-delta, subprocess): the two verified batteries (sim_bycode_v2 = ZWSP 21/21,
  zwj_bom_battery = ZWJ/BOM 11/11 + mutations) run with O1 OFF and O1 ON. Both must PASS
  (frozen expectations preserved) AND produce BIT-IDENTICAL stdout OFF vs ON.

PART C (seam-liveness + structured zero-delta + hotspot, in-process):
  C1 SEAM-LIVENESS -- a temporary row must escalate a REAL analyze() verdict (MEDIUM->HIGH
     + o1_policy, driving hold). WITHOUT this, the whole gate is a FALSE-GREEN: PART A
     calls the engine directly and PART B compares OFF/ON with an empty registry, so a
     DISCONNECTED seam passes both. (Found by an adversarial external review; reproduced
     by measurement -- a disconnected seam left A+B green while C1 fails.)
  C2 STRUCTURED zero-delta -- OFF vs ON at the relation-verdict dict level over the ZWJ/BOM
     manifest inputs (catches a non-printable key that stdout would miss); no o1_policy key
     may appear with the empty registry.
  C3 HOTSPOT -- the seam must not add _detect_context_at calls (it reads the ready ctx).

Scoped to INCREMENT-0. Once a behavioral rule is added, O1-ON output will intentionally
differ from O1-OFF and the exact-identity checks are superseded by the delta-census gate.
Basis: AUTHOR_DECISION_20260721_D-O1-IMPL-SCOPE.
"""
import contextlib
import io
import os
import subprocess
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_BASE = os.path.dirname(_HERE)
os.environ["MSL_MIP_HERMETIC_TLD"] = "1"
for _p in ("core", "single_sign", "sequence"):
    sys.path.insert(0, os.path.join(_BASE, _p))
sys.path.insert(0, _BASE)

import o1_policy_engine as o1
from sign_core_card import RiskLevel

fails = []
PR = o1.PolicyRow
BOM_CP = 0xFEFF

# ------------------------------------------------------------------ PART A
# A0: the ACTUAL active registry must lint clean (not just synthetic test rows).
if o1.lint_registry(o1.ACTIVE_POLICY_REGISTRY) != []:
    fails.append("A0 active registry does not lint clean")

# A1: the increment-0 empty registry lints clean.
if o1.lint_registry(()) != []:
    fails.append("A1 empty registry did not lint clean")

# A2: every malformed row must be rejected (linter is real).
bad_rows = [
    ("zwsp-key",        PR(0x200B, "BYTE_EXACT_TOKEN", None, RiskLevel.HIGH, "r", "p")),
    ("wildcard-ctx",    PR(BOM_CP, "ANY",              None, RiskLevel.HIGH, "r", "p")),
    ("empty-ctx",       PR(BOM_CP, "",                 None, RiskLevel.HIGH, "r", "p")),
    ("critical-target", PR(BOM_CP, "HOST",             None, RiskLevel.CRITICAL, "r", "p")),
    ("none-target",     PR(BOM_CP, "HOST",             None, RiskLevel.NONE, "r", "p")),
    ("low-target",      PR(BOM_CP, "HOST",             None, RiskLevel.LOW, "r", "p")),
    ("target-not-enum", PR(BOM_CP, "HOST",             None, "HIGH", "r", "p")),
    ("sign-cp-string",  PR("U+FEFF", "HOST",           None, RiskLevel.HIGH, "r", "p")),
    ("wildcard-role",   PR(BOM_CP, "HOST",             "ANY", RiskLevel.HIGH, "r", "p")),
    ("no-provenance",   PR(BOM_CP, "HOST",             None, RiskLevel.HIGH, "r", "")),
    ("no-rule-id",      PR(BOM_CP, "HOST",             None, RiskLevel.HIGH, "", "p")),
]
for name, row in bad_rows:
    if o1.lint_registry([row]) == []:
        fails.append("A2 malformed row NOT rejected: " + name)

# A2-dup: two rows with the same key must be rejected (silent shadowing in _lookup).
dup = [PR(BOM_CP, "HOST", None, RiskLevel.HIGH, "d1", "p"),
       PR(BOM_CP, "HOST", None, RiskLevel.HIGH, "d2", "p")]
if o1.lint_registry(dup) == []:
    fails.append("A2 duplicate key NOT rejected")

# A3: a well-formed row lints clean.
good = PR(BOM_CP, "BYTE_EXACT_TOKEN", None, RiskLevel.HIGH, "R1", "RECONCILE_B3+AD")
if o1.lint_registry([good]) != []:
    fails.append("A3 well-formed row wrongly rejected")

# A4: with the empty registry the seam is inert even when O1 is enabled.
os.environ["MSL_MIP_O1_ENABLED"] = "1"
fr, dec = o1.final_level(RiskLevel.MEDIUM, BOM_CP, "BYTE_EXACT_TOKEN")
if fr != RiskLevel.MEDIUM or dec.matched or o1.audit_field(dec) is not None:
    fails.append("A4 empty-registry seam not inert when enabled")

# A5: the engine is LIVE (not a dead stub) -- inject a row, it must raise + audit,
#     and it must be RAISE-ONLY (a base already at/above the target is not lowered).
saved = o1.ACTIVE_POLICY_REGISTRY
try:
    o1.ACTIVE_POLICY_REGISTRY = (good,)
    fr, dec = o1.final_level(RiskLevel.MEDIUM, BOM_CP, "BYTE_EXACT_TOKEN")
    if fr != RiskLevel.HIGH or not dec.matched:
        fails.append("A5 engine did not raise on a matching row")
    af = o1.audit_field(dec)
    if not af or af.get("final_level") != "HIGH" or af.get("base_level") != "MEDIUM" \
            or af.get("seam") != o1.SEAM_ID:
        fails.append("A5 audit field wrong on a fired row")
    fr2, dec2 = o1.final_level(RiskLevel.HIGH, BOM_CP, "BYTE_EXACT_TOKEN")
    if fr2 != RiskLevel.HIGH or dec2.matched:
        fails.append("A5 raise-only broken (base at target should be a no-op)")
    fr3, dec3 = o1.final_level(RiskLevel.MEDIUM, BOM_CP, "EMAIL")
    if fr3 != RiskLevel.MEDIUM or dec3.matched:
        fails.append("A5 non-matching key fired")
finally:
    o1.ACTIVE_POLICY_REGISTRY = saved
    os.environ["MSL_MIP_O1_ENABLED"] = "0"

# ------------------------------------------------------------------ PART B
def run_battery(script, enabled):
    env = dict(os.environ, PYTHONIOENCODING="utf-8",
               MSL_MIP_O1_ENABLED=("1" if enabled else "0"))
    p = subprocess.run([sys.executable, os.path.join(_HERE, script)], cwd=_BASE,
                       env=env, capture_output=True, text=True, encoding="utf-8",
                       timeout=300)
    return p.returncode, p.stdout

for script in ("sim_bycode_v2.py", "zwj_bom_battery.py"):
    rc_off, out_off = run_battery(script, False)
    rc_on, out_on = run_battery(script, True)
    if rc_off != 0:
        fails.append("B %s did NOT pass with O1 OFF (rc=%s)" % (script, rc_off))
    if rc_on != 0:
        fails.append("B %s did NOT pass with O1 ON (rc=%s)" % (script, rc_on))
    if out_off != out_on:
        fails.append("B %s stdout DIFFERS OFF vs ON -> seam not inert" % script)

# ------------------------------------------------------------------ PART C
import msl_mip_runtime as rt
import sequence_engine as se
from load_card import load_card
from zwj_bom_manifests import ZWJ_MANIFEST, BOM_MANIFEST
se._force_tld_state_for_test(frozenset({"com", "org", "net", "ru", "io", "dev", "xn--p1ai"}), False)

_C = os.path.join(_BASE, "cards")
MASK = load_card(os.path.join(_C, "SIGN_CORE_CARD_FULLWIDTH_SOLIDUS_UFF0F_GEN3_v0_3_RU.md"))
BOM_CARD = load_card(os.path.join(_C, "SIGN_CORE_CARD_BYTE_ORDER_MARK_UFEFF_GEN3_v0_1_RU.md"))
ZWJ_CARD = load_card(os.path.join(_C, "SIGN_CORE_CARD_ZERO_WIDTH_JOINER_U200D_GEN3_v0_1_RU.md"))
BOMCH = "﻿"


def _analyze(text, cards):
    with contextlib.redirect_stdout(io.StringIO()):
        return rt.analyze(text, cards)


def _proj(rep):
    vs = tuple((v.get("visible_form"), v.get("at_offset"), v.get("detected_context"),
                v.get("risk_level"), v.get("runtime_role"),
                "o1" if "o1_policy" in v else "-")
               for v in rep["sequence_output"].relation_verdicts)
    return (vs, rep.get("effective_action"), rep.get("semantic_action"))


# C1: SEAM-LIVENESS -- a temp row MUST escalate a real analyze() verdict, else the seam
#     is disconnected and PARTs A+B are a false-green.
saved = o1.ACTIVE_POLICY_REGISTRY
try:
    o1.ACTIVE_POLICY_REGISTRY = (PR(BOM_CP, "EMAIL", None, RiskLevel.HIGH, "TEST_SEAM", "PROBE"),)
    os.environ["MSL_MIP_O1_ENABLED"] = "1"
    rep = _analyze("us" + BOMCH + "er@example.com", [BOM_CARD, MASK])
    wired = any(v.get("visible_form") == BOMCH and v.get("risk_level") == "HIGH"
                and v.get("o1_policy", {}).get("rule_id") == "TEST_SEAM"
                for v in rep["sequence_output"].relation_verdicts)
    if not wired:
        fails.append("C1 SEAM NOT WIRED: analyze() did not route through O1 (false-green)")
    elif rep["effective_action"] != "hold_pending_review":
        fails.append("C1 escalated verdict did not drive hold_pending_review")
finally:
    o1.ACTIVE_POLICY_REGISTRY = saved
    os.environ["MSL_MIP_O1_ENABLED"] = "0"

# C2: STRUCTURED zero-delta at the dict level (catches a non-printable key stdout misses).
for manifest, cards in ((ZWJ_MANIFEST, [ZWJ_CARD, MASK]), (BOM_MANIFEST, [BOM_CARD, MASK])):
    for case in manifest:
        text = case["input"]
        os.environ["MSL_MIP_O1_ENABLED"] = "0"
        off = _proj(_analyze(text, cards))
        os.environ["MSL_MIP_O1_ENABLED"] = "1"
        on = _proj(_analyze(text, cards))
        os.environ["MSL_MIP_O1_ENABLED"] = "0"
        if off != on:
            fails.append("C2 structured OFF!=ON on case %s" % case.get("id"))
        if any(row[5] == "o1" for row in on[0]):
            fails.append("C2 o1_policy key present with empty registry, case %s" % case.get("id"))

# C3: HOTSPOT -- the seam must not add _detect_context_at calls.
_real_ctx = se._detect_context_at
_calls = {"n": 0}
def _counting(*a, **k):
    _calls["n"] += 1
    return _real_ctx(*a, **k)
se._detect_context_at = _counting
try:
    txt = "goog" + "‍" + "le.com"
    os.environ["MSL_MIP_O1_ENABLED"] = "0"; _calls["n"] = 0; _analyze(txt, [ZWJ_CARD, MASK]); off_n = _calls["n"]
    os.environ["MSL_MIP_O1_ENABLED"] = "1"; _calls["n"] = 0; _analyze(txt, [ZWJ_CARD, MASK]); on_n = _calls["n"]
    os.environ["MSL_MIP_O1_ENABLED"] = "0"
    if off_n != on_n:
        fails.append("C3 _detect_context_at calls differ OFF=%d ON=%d (seam calls hotspot)" % (off_n, on_n))
finally:
    se._detect_context_at = _real_ctx

# ------------------------------------------------------------------ report
print("=" * 68)
print("GATE: O1 increment-0 -- zero-delta + engine self-test + seam-liveness")
print("=" * 68)
if fails:
    for f in fails:
        print("  FAIL: " + f)
    print("\nTOTAL: FAIL")
    sys.exit(1)
print("A engine: active+empty registry clean; linter rejects %d malformed rows + duplicates; live + raise-only"
      % len(bad_rows))
print("B zero-delta: sim_bycode_v2 (ZWSP) + zwj_bom_battery (ZWJ/BOM) bit-identical OFF vs ON, both pass")
print("C seam-liveness: a temp row escalates a REAL analyze() verdict -> hold; structured OFF==ON; hotspot calls equal")
print("\nTOTAL: CLEAN -- seam RELATION_PATH_O1_HOOK_v0_1 is WIRED and, with an empty registry, changes exactly nothing")
sys.exit(0)
