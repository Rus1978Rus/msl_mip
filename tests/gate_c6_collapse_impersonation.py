# -*- coding: utf-8 -*-
"""GATE: C6 collapse-impersonation rule -- the first BEHAVIORAL O1 rule.

A ghost-token attack has one necessary property: with the invisibles removed the token must
impersonate something the consumer actually protects. So the rule is the STRIPPED-MATCH
signature -- the token as written is NOT a protected target, but its collapse IS -> hold.

  A INERT BY DEFAULT -- with no caller-supplied targets nothing is derived, no row can
    match, and the analysis is identical. This is what keeps every existing battery green.
  B FIRES on impersonation -- with targets supplied, pay<BOM>pal escalates MEDIUM -> HIGH
    (hold) and carries the audit with rule_id and provenance.
  C STRIPPED-MATCH semantics -- a collapse that matches nothing does not fire; a token that
    is ALREADY the target does not fire (nothing was hidden); a clean token never fires.
  D RAISE-ONLY -- the rule only lifts a level, and the sign/context key is exact.
  E KNOWN LIMIT, PINNED -- an ORDINARY-WORD target also occurs in prose, where a stray
    invisible collapses to a "match". This gate ASSERTS that false positive so the
    limitation stays visible: it is the caller's list that must stay narrow, and the real
    fix is the context front (CONTEXT_V2), not a hidden heuristic here.
Basis: AUTHOR_DECISION_20260721_D-O1-C6-NARROW.
"""
import contextlib
import io
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_BASE = os.path.dirname(_HERE)
os.environ["MSL_MIP_HERMETIC_TLD"] = "1"
for _p in ("core", "single_sign", "sequence"):
    sys.path.insert(0, os.path.join(_BASE, _p))
sys.path.insert(0, _BASE)

import msl_mip_runtime as rt
import o1_policy_engine as o1
import sequence_engine as se
from load_card import load_card
se._force_tld_state_for_test(frozenset({"com", "org", "net", "ru", "io", "dev", "xn--p1ai"}), False)

_C = os.path.join(_BASE, "cards")
MASK = load_card(os.path.join(_C, "SIGN_CORE_CARD_FULLWIDTH_SOLIDUS_UFF0F_GEN3_v0_3_RU.md"))
BOM_CARD = load_card(os.path.join(_C, "SIGN_CORE_CARD_BYTE_ORDER_MARK_UFEFF_GEN3_v0_1_RU.md"))
CARDS = [BOM_CARD, MASK]
B = "﻿"
GHOST = "pay" + B + "pal"            # collapses to a protected target
ARTIFACT = "paragraph" + B + "joined"  # collapses to nothing anyone protects
TARGETS = {"paypal", "apikey", "sudo", "passwd"}   # narrow, non-dictionary

fails = []


def _run(text, targets=None):
    with contextlib.redirect_stdout(io.StringIO()):
        return rt.analyze(text, CARDS, protected_targets=targets)


def _bom_verdicts(rep):
    return [v for v in rep["sequence_output"].relation_verdicts
            if v["visible_form"] == B and v.get("relation_type") == "BOUNDARY_DISRUPTOR"]


# ------------------------------------------------------------------ A INERT BY DEFAULT
plain = _run(GHOST)                       # no targets
pv = _bom_verdicts(plain)
if not pv:
    fails.append("A no BOM verdict for the ghost token at all")
else:
    if pv[0].get("detected_context") != "BYTE_EXACT_TOKEN":
        fails.append("A ghost token context %r (expected BYTE_EXACT_TOKEN)"
                     % pv[0].get("detected_context"))
    if pv[0].get("risk_level") != "MEDIUM":
        fails.append("A without targets the level moved: %r" % pv[0].get("risk_level"))
    if "o1_policy" in pv[0]:
        fails.append("A audit field present although no targets were supplied")
if plain.get("effective_action") != "queue_for_review":
    fails.append("A default action changed: %r" % plain.get("effective_action"))

# ---------------------------------------------------------------------- B FIRES
fired = _run(GHOST, TARGETS)
fv = _bom_verdicts(fired)
if not fv:
    fails.append("B no BOM verdict with targets supplied")
else:
    if fv[0].get("risk_level") != "HIGH":
        fails.append("B impersonation did NOT escalate: %r" % fv[0].get("risk_level"))
    aud = fv[0].get("o1_policy")
    if not aud:
        fails.append("B fired row carries no audit field")
    else:
        if aud.get("base_level") != "MEDIUM" or aud.get("final_level") != "HIGH":
            fails.append("B audit levels wrong: %r" % aud)
        if aud.get("rule_id") != "O1-BOM-TOKEN-COLLAPSE-IMPERSONATION":
            fails.append("B audit rule_id wrong: %r" % aud.get("rule_id"))
        if not aud.get("provenance"):
            fails.append("B audit carries no provenance")
if fired.get("effective_action") != "hold_pending_review":
    fails.append("B escalation did not drive hold: %r" % fired.get("effective_action"))

# ------------------------------------------------------- C STRIPPED-MATCH semantics
art = _bom_verdicts(_run(ARTIFACT, TARGETS))
if art and art[0].get("risk_level") != "MEDIUM":
    fails.append("C a benign artifact collapse fired: %r" % art[0].get("risk_level"))

# Written form ALREADY a listed target -> NOTHING is hidden, so the stripped-match must
# REFUSE: this is not an impersonation of some other target, it is the target itself.
already = _bom_verdicts(_run(GHOST, {"pay" + B + "pal", "paypal"}))
if already and already[0].get("risk_level") != "MEDIUM":
    fails.append("C fired although the WRITTEN form is itself a listed target "
                 "(nothing hidden -> not an impersonation)")

# a clean token with no invisible produces no BOM verdict at all
if _bom_verdicts(_run("paypal", TARGETS)):
    fails.append("C a clean token produced a BOM verdict")

# ------------------------------------------------------------------- D RAISE-ONLY
# exact key: the same collapse in a DIFFERENT context (mid-host) must not use this row
host = _bom_verdicts(_run("pay" + B + "pal.com", TARGETS))
if host:
    if host[0].get("detected_context") != "HOST":
        fails.append("D host case context %r (expected HOST)" % host[0].get("detected_context"))
    elif host[0].get("o1_policy") is not None:
        fails.append("D the BYTE_EXACT_TOKEN row fired in HOST context (key not exact)")

# ------------------------------------------------------------- E KNOWN LIMIT, PINNED
# An ordinary-word target also occurs in prose. This IS a false positive and it is pinned
# here on purpose: the caller's list must stay narrow until CONTEXT_V2 lands.
prose = _bom_verdicts(_run("the sy" + B + "stem crashed", {"system"}))
if not prose or prose[0].get("risk_level") != "HIGH":
    fails.append("E the known ordinary-word false positive did NOT reproduce -- the "
                 "documented limitation may have silently changed; re-measure before trusting")

print("=" * 68)
print("GATE: C6 collapse-impersonation -- first behavioral O1 rule")
print("=" * 68)
if fails:
    for f in fails:
        print("  FAIL: " + f)
    print("\nTOTAL: FAIL")
    sys.exit(1)
print("A inert by default: no targets -> MEDIUM/queue, no audit, analysis unchanged")
print("B fires: pay<BOM>pal + targets -> HIGH/hold with rule_id + provenance")
print("C stripped-match: benign collapse does not fire; clean token yields no verdict")
print("D exact key: the BYTE_EXACT_TOKEN row does not fire in HOST context")
print("E known limit PINNED: an ordinary-word target ('system') DOES false-positive on prose")
print("\nTOTAL: CLEAN -- impersonation is held, and the list-composition limit stays visible")
sys.exit(0)
