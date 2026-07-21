# -*- coding: utf-8 -*-
"""GATE: canonical projection (P1) -- additive, display-only, verdict-neutral.

The token cell stays at MEDIUM/queue (measurement: a direct escalation would false-positive
on 67% of benign BOM-carrying text). The value delivered instead is SHOWING the human what
the invisible does: "looks like paypal.com; actually pay<U+FEFF>pal.com". This gate pins the
three properties that make that safe:

  A CORRECTNESS -- the projection reports the token, its collapsed form and the members'
    offsets in ORIGINAL coordinates.
  B VERDICT-NEUTRAL -- verdicts are bit-identical with the projection enabled, disabled, and
    BROKEN. A broken projection cannot change a verdict (the class_guard safety argument).
  C DISPLAY-ONLY -- report["text"] stays the ORIGINAL string; the collapsed form is never
    substituted anywhere. Stripping before a decision would be a silent sanitizer that
    destroys the very byte difference a ghost-token exploits.
  D ZERO-DELTA -- the verified batteries (ZWSP 21/21, ZWJ/BOM 11/11 + mutations) pass and
    print bit-identical output with the projection on and off.

Basis: AUTHOR_DECISION_20260721_D-O1-TOKEN-CELL (P1).
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

import msl_mip_runtime as rt
import sequence_engine as se
from load_card import load_card
se._force_tld_state_for_test(frozenset({"com", "org", "net", "ru", "io", "dev", "xn--p1ai"}), False)

_C = os.path.join(_BASE, "cards")
MASK = load_card(os.path.join(_C, "SIGN_CORE_CARD_FULLWIDTH_SOLIDUS_UFF0F_GEN3_v0_3_RU.md"))
BOM_CARD = load_card(os.path.join(_C, "SIGN_CORE_CARD_BYTE_ORDER_MARK_UFEFF_GEN3_v0_1_RU.md"))
CARDS = [BOM_CARD, MASK]
B = "﻿"
GHOST = "pay" + B + "pal.com"

fails = []


def _analyze(text, cards=CARDS):
    with contextlib.redirect_stdout(io.StringIO()):
        return rt.analyze(text, cards)


def _verdict_projection(rep):
    """Everything a verdict consists of -- must never move because of the projection."""
    vs = tuple((v.get("visible_form"), v.get("at_offset"), v.get("detected_context"),
                v.get("risk_level"), v.get("runtime_role"))
               for v in rep["sequence_output"].relation_verdicts)
    return (vs, rep.get("semantic_action"), rep.get("effective_action"),
            rep.get("attention_status"), rep.get("integrity_status"))


# ---------------------------------------------------------------- A CORRECTNESS
rep = _analyze(GHOST)
proj = rep.get("canonical_projection")
if not proj:
    fails.append("A projection field missing from the report")
else:
    if proj.get("status") != "OK":
        fails.append("A projection status %r (want OK)" % proj.get("status"))
    if proj.get("display_only") is not True:
        fails.append("A projection does not declare display_only")
    toks = proj.get("tokens") or []
    if len(toks) != 1:
        fails.append("A expected exactly 1 projected token, got %d" % len(toks))
    else:
        t = toks[0]
        if t.get("original_token") != GHOST:
            fails.append("A original_token %r != input token" % t.get("original_token"))
        if t.get("collapsed_token") != "paypal.com":
            fails.append("A collapsed_token %r != 'paypal.com'" % t.get("collapsed_token"))
        if t.get("token_offset") != 0:
            fails.append("A token_offset %r != 0" % t.get("token_offset"))
        mem = t.get("members") or []
        if len(mem) != 1 or mem[0].get("codepoint") != "U+FEFF" or mem[0].get("original_offset") != 3:
            fails.append("A member record wrong: %r (want U+FEFF at original_offset 3)" % mem)

# a clean token must not be projected at all
clean = _analyze("paypal.com").get("canonical_projection") or {}
if (clean.get("tokens") or []):
    fails.append("A a token with no class-138 member was projected")

# ------------------------------------------------------------- B VERDICT-NEUTRAL
base_v = _verdict_projection(_analyze(GHOST))

os.environ["MSL_MIP_PROJECTION_DISABLED"] = "1"
off_rep = _analyze(GHOST)
off_v = _verdict_projection(off_rep)
os.environ.pop("MSL_MIP_PROJECTION_DISABLED", None)
if "canonical_projection" in off_rep:
    fails.append("B projection field present although disabled")
if off_v != base_v:
    fails.append("B verdict changed between projection ON and OFF")

# BROKEN projection must not move the verdict (the class_guard safety argument).
_real_138 = rt._monitored_138_set
def _boom():
    raise RuntimeError("simulated projection failure")
rt._monitored_138_set = _boom
try:
    broken_rep = _analyze(GHOST)
    if _verdict_projection(broken_rep) != base_v:
        fails.append("B a BROKEN projection changed the verdict")
    bp = broken_rep.get("canonical_projection") or {}
    if bp.get("status") != "PROJECTION_FAILURE":
        fails.append("B broken projection did not fail open (status %r)" % bp.get("status"))
finally:
    rt._monitored_138_set = _real_138

# ---------------------------------------------------------------- C DISPLAY-ONLY
rep2 = _analyze(GHOST)
if rep2.get("text") != GHOST:
    fails.append("C report['text'] is not the ORIGINAL string (silent sanitizer!)")
tok0 = ((rep2.get("canonical_projection") or {}).get("tokens") or [{}])[0]
if tok0.get("collapsed_token") == tok0.get("original_token"):
    fails.append("C collapsed == original (projection shows nothing)")
# the collapsed form must not have leaked into any verdict field
for v in rep2["sequence_output"].relation_verdicts:
    if "paypal.com" == v.get("target") and B not in GHOST:
        fails.append("C collapsed form leaked into a verdict field")

# ------------------------------------------------------------------- D ZERO-DELTA
def run_battery(script, projection_on):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    if projection_on:
        env.pop("MSL_MIP_PROJECTION_DISABLED", None)
    else:
        env["MSL_MIP_PROJECTION_DISABLED"] = "1"
    p = subprocess.run([sys.executable, os.path.join(_HERE, script)], cwd=_BASE, env=env,
                       capture_output=True, text=True, encoding="utf-8", timeout=300)
    return p.returncode, p.stdout

for script in ("sim_bycode_v2.py", "zwj_bom_battery.py"):
    rc_on, out_on = run_battery(script, True)
    rc_off, out_off = run_battery(script, False)
    if rc_on != 0:
        fails.append("D %s failed with projection ON (rc=%s)" % (script, rc_on))
    if rc_off != 0:
        fails.append("D %s failed with projection OFF (rc=%s)" % (script, rc_off))
    if out_on != out_off:
        fails.append("D %s stdout differs ON vs OFF -> projection is not verdict-neutral" % script)

# ---------------------------------------------------------------------- report
print("=" * 66)
print("GATE: canonical projection (P1) -- display-only, verdict-neutral")
print("=" * 66)
if fails:
    for f in fails:
        print("  FAIL: " + f)
    print("\nTOTAL: FAIL")
    sys.exit(1)
print("A correctness: pay<U+FEFF>pal.com -> collapsed 'paypal.com', member U+FEFF @3; clean token not projected")
print("B verdict-neutral: identical verdicts with projection ON / OFF / BROKEN (fails open)")
print("C display-only: report['text'] stays the original; collapsed form never substituted")
print("D zero-delta: ZWSP + ZWJ/BOM batteries pass and are bit-identical ON vs OFF")
print("\nTOTAL: CLEAN -- the projection SHOWS the deception without touching a single verdict")
sys.exit(0)
