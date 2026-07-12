#!/usr/bin/env python3
"""
CHAOS GATE for the finish-line safeguard (D-GUARD-1 / D-GUARD-2).

This gate tests the WATCHDOG, not the detector. It deliberately SEVERS the
mask aggregation path (monkey-patch) and asserts that the conservation-of-
risk invariant in analyze() CATCHES the mismatch. A watchdog that died
quietly is worse than no watchdog — so if a severed path returns a clean
PASS with the guard silent, THIS GATE FAILS.

Each chaos case:
  1. a phishing input with a mask whose relation verdict is HOST/HIGH,
  2. the aggregation path is intentionally broken (monkey-patch), leaving
     seq_out.relation_verdicts (the source of truth the guard reads) intact,
  3. analyze() is run in STRICT mode (MSL_MIP_GUARD_STRICT=1),
  4. expectation: the invariant raises IntegrityViolation.

Hermetic: the TLD set is pinned offline (no network / cache / clock /
randomness). Deterministic across runs.

Homoglyph specimens are written as \\u escapes (Cyrillic 'o' = U+043E,
fullwidth solidus = U+FF0F) so this file stays literally ASCII and needs
no english-only allowlist entry.

Run: py -3 tests/gate_safeguard.py
"""
import os
import sys
import tempfile

os.environ["MSL_MIP_HERMETIC_TLD"] = "1"

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for p in ("core", "single_sign", "sequence"):
    sys.path.insert(0, os.path.join(BASE, p))
sys.path.insert(0, BASE)  # for msl_mip_runtime

import msl_mip_runtime as rt
from load_card import load_card
from sequence_engine import _force_tld_state_for_test, _reset_tld_state_for_test

# Pin the TLD set offline — deterministic, no network (memory: GATE_MUST_BE_HERMETIC).
_PINNED = frozenset({"com", "org", "net", "ru", "io", "xn--p1ai"})
_force_tld_state_for_test(_PINNED, degraded=False)

_MASK = "\uff0f"   # FULLWIDTH SOLIDUS (the carded mask)
_CYR_O = "\u043e"  # Cyrillic small o (homoglyph of Latin o)
# Phishing: a bare masked domain -> relation verdict HOST/HIGH.
PHISH = "g" + _CYR_O + "og" + _MASK + "le.com"   # goog/le.com with homoglyphs

PASSED = 0
FAILED = 0


def check(label, cond, detail=""):
    global PASSED, FAILED
    if cond:
        PASSED += 1
        print(f"  ✓ {label}")
    else:
        FAILED += 1
        print(f"  ✗ {label}  {detail}")


def _card(scope="URL, HOST, PATH"):
    txt = ("CARD_UID: BD\nCODEPOINT: U+FF0F\nVISIBLE_FORM: " + _MASK + "\n"
           "UNICODE_NAME: FULLWIDTH SOLIDUS\nZONE: ZONE_2\n"
           "DOCUMENT_STATUS: WORKING_DRAFT\nSIGN_RELATIONS:\n"
           "  RELATION_001:\n    RELATION_TYPE: NFKC_MAPS_TO\n"
           "    TARGET: U+002F\n    CONTEXT_SCOPE: " + scope + "\n"
           "    VERIFICATION_STATUS: VERIFIED\n    RUNTIME_EFFECT: RELATION_ONLY\n")
    f = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8")
    f.write(txt)
    f.close()
    return load_card(f.name)


MASK = _card()


def run(text, cards, strict):
    """Run analyze() with/without strict mode; return ('report', dict) or
    ('raised', message)."""
    if strict:
        os.environ["MSL_MIP_GUARD_STRICT"] = "1"
    else:
        os.environ.pop("MSL_MIP_GUARD_STRICT", None)
    try:
        return ("report", rt.analyze(text, cards))
    except rt.IntegrityViolation as e:
        return ("raised", str(e))
    finally:
        os.environ.pop("MSL_MIP_GUARD_STRICT", None)


print("=" * 64)
print("CHAOS GATE — finish-line safeguard (D-GUARD-1/2)")
print("=" * 64)

# --- SANITY: intact path -> guard silent, phishing -> HOLD ---
print("\n[sanity] Intact path: guard silent, masked phishing -> HOLD")
kind, res = run(PHISH, [MASK], strict=True)
check("intact path does NOT raise in strict mode", kind == "report", kind)
if kind == "report":
    rv = [(v["detected_context"], v["risk_level"])
          for v in res["sequence_output"].relation_verdicts]
    check("relation verdict is HOST/HIGH", ("HOST", "HIGH") in rv, rv)
    check("final verdict is hold_pending_review",
          res["final_action"] == "hold_pending_review", res["final_action"])
    check("integrity_status OK on intact path",
          res["integrity_status"] == "OK", res["integrity_status"])

_ORIG_REL_ACTION = dict(rt._REL_ACTION)
_ORIG_REL_FN = rt._relation_actions

# --- CHAOS A: integrator/mapping returns PASS at a HIGH relation (main) ---
print("\n[chaos A] Mapping corrupted: HIGH relation -> 'pass' action")
try:
    rt._REL_ACTION = dict(_ORIG_REL_ACTION)
    rt._REL_ACTION["HIGH"] = "pass"
    kind, res = run(PHISH, [MASK], strict=True)
    check("severed path (HIGH->pass) RAISES IntegrityViolation in strict",
          kind == "raised", (kind, res))
finally:
    rt._REL_ACTION = dict(_ORIG_REL_ACTION)

# --- CHAOS B: relation_verdicts lost at serialization (empty where HIGH was) ---
print("\n[chaos B] Serialization loss: actions derived from as_dict (drops verdicts)")


def _severed_serialize(seq_out):
    # a consumer that reads the SERIALIZED form; as_dict() omits
    # relation_verdicts entirely (finding S4) -> empty action list
    return [rt._REL_ACTION.get(v.get("RISK_LEVEL"), "pass")
            for v in seq_out.as_dict().get("RELATION_VERDICTS", [])]


try:
    rt._relation_actions = _severed_serialize
    kind, res = run(PHISH, [MASK], strict=True)
    check("severed path (serialized/empty verdicts) RAISES in strict",
          kind == "raised", (kind, res))
finally:
    rt._relation_actions = _ORIG_REL_FN

# --- CHAOS C: empty-pool exit before mask accounting ---
print("\n[chaos C] Empty-pool exit: mask accounting skipped on check_unavailable")


def _severed_emptypool(seq_out):
    if seq_out.check_unavailable:   # regression: forgot masks on the early exit
        return []
    return _ORIG_REL_FN(seq_out)


try:
    rt._relation_actions = _severed_emptypool
    kind, res = run(PHISH, [MASK], strict=True)   # mask-only -> check_unavailable True
    check("severed path (empty-pool skip) RAISES in strict",
          kind == "raised", (kind, res))
finally:
    rt._relation_actions = _ORIG_REL_FN

# --- HYBRID: production (non-strict) leaves the verdict but FLAGS it ---
print("\n[hybrid] Non-strict: verdict unchanged (pass) but flagged")
try:
    rt._REL_ACTION = dict(_ORIG_REL_ACTION)
    rt._REL_ACTION["HIGH"] = "pass"
    kind, res = run(PHISH, [MASK], strict=False)
    check("non-strict does NOT raise", kind == "report", kind)
    if kind == "report":
        check("verdict left as pass (author is the sole authority)",
              res["final_action"] == "pass", res["final_action"])
        check("report marked PASS_WITH_INTEGRITY_VIOLATION",
              res["integrity_status"] == "PASS_WITH_INTEGRITY_VIOLATION",
              res["integrity_status"])
        check("violation detail names the relation risk + final",
              any(v["relation_risk"] == "HIGH" and v["final_action"] == "pass"
                  for v in res["integrity_violations"]),
              res["integrity_violations"])
finally:
    rt._REL_ACTION = dict(_ORIG_REL_ACTION)

# --- D-GUARD-2: a validation_warning on an active inert edge is revived ---
print("\n[D-GUARD-2] validation_warning on an inert edge -> INTEGRITY_CONCERN")
TYPO = _card(scope="HSOT")   # unknown scope -> load warning + verdict NONE
kind, res = run(PHISH, [TYPO], strict=True)   # concerns never raise, only violations do
check("typo-scope run does NOT raise (concern, not violation)", kind == "report", kind)
if kind == "report":
    dg2 = [c for c in res["integrity_concerns"] if c["rule"] == "D-GUARD-2"]
    check("D-GUARD-2 concern raised for the warned inert edge",
          len(dg2) >= 1, res["integrity_concerns"])
    check("concern carries the load-time validation_warning",
          bool(dg2) and any("UNKNOWN_CONTEXT_SCOPE" in w
                            for w in dg2[0]["validation_warnings"]),
          dg2)
    check("integrity_status is INTEGRITY_CONCERN",
          res["integrity_status"] == "INTEGRITY_CONCERN", res["integrity_status"])

_reset_tld_state_for_test()

print("\n" + "=" * 64)
print(f"TOTAL: {PASSED} OK / {FAILED} FAIL")
print("=" * 64)
sys.exit(1 if FAILED else 0)
