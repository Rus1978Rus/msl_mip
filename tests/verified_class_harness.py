# -*- coding: utf-8 -*-
"""VERIFIED-CLASS BY_CODE HARNESS -- sign-parameterized battery runner.

Generalizes the ZWSP TIER_2 harness (tests/sim_bycode_v2.py, a frozen verified
artifact -- NOT touched here) so the SAME measure/classify/mutation-adequacy
logic can drive a battery for any carded invisible sign (ZWJ, BOM, ...). A
battery = a manifest of cases pinned by Unicode property / structure / the card,
run SIGN-SCOPED (only that sign's card + the mask card are loaded) so the sign's
verified artifact is not contaminated by other cards.

Measure-only, no fix. Live msl_mip_runtime. Import and call run_battery() +
mutation_adequacy() from a per-sign runner (tests/zwj_bom_battery.py).
"""
import os, sys, io, contextlib
os.environ["MSL_MIP_HERMETIC_TLD"] = "1"
_HERE = os.path.dirname(os.path.abspath(__file__))
_BASE = os.path.dirname(_HERE)
for _p in ("core", "single_sign", "sequence"):
    sys.path.insert(0, os.path.join(_BASE, _p))
sys.path.insert(0, _BASE)
import msl_mip_runtime as rt
import sequence_engine as se
from sequence_engine import _force_tld_state_for_test
_force_tld_state_for_test(frozenset({"com", "org", "net", "ru", "io", "dev", "xn--p1ai"}), False)

# Independent authoritative RELATION_TYPE -> EXPECTED_ROLE map, kept here and NOT
# imported from the runtime, so a mutation moving the runtime role map is caught.
_AUTH_EXPECTED_ROLE = {
    "BOUNDARY_DISRUPTOR": "PRIMARY",
    "ABSENCE_CONFUSABLE": "SUPPORTING_FACET",
    "INVISIBLE_CLASS_COLLISION": "TAXONOMY_ONLY",
    "CONFUSABLE_OF": "PRIMARY", "NFKC_MAPS_TO": "PRIMARY", "VISUAL_MIMIC_OF": "PRIMARY",
    "": "PRIMARY",
}
_NONRISK_ROLES = {"SUPPORTING_FACET", "TAXONOMY_ONLY", "INVALID_EDGE"}


def cps(s):
    out = []
    for ch in s:
        o = ord(ch)
        show = (o < 0x20 or o == 0x7f or 0x200b <= o <= 0x206f or o in (0xfeff, 0x2062, 0x2063, 0xff0f, 0x00a0, 0x202f, 0x2800)
                or 0x2028 <= o <= 0x2029 or 0xfe00 <= o <= 0xfe0f or o == 0x202e or o >= 0xe0000)
        out.append("<U+%04X>" % o if show else ch)
    return "".join(out)


def measure(text, sign, cards):
    """Measured tuple for one input, for the given carded SIGN."""
    with contextlib.redirect_stdout(io.StringIO()):
        rep = rt.analyze(text, cards)
    prim = None
    facet_leak = []
    for v in rep["sequence_output"].relation_verdicts:
        if v["visible_form"] != sign:
            continue
        rt_ = v.get("relation_type")
        role = v.get("runtime_role")
        rk = v.get("risk_level")
        if rt_ == "BOUNDARY_DISRUPTOR":
            prim = v
        exp = _AUTH_EXPECTED_ROLE.get(rt_, "INVALID_EDGE")
        if role != exp:
            facet_leak.append(("ROLE_TAMPERED", "%s: emitted %s, auth %s" % (rt_, role, exp)))
        if exp in _NONRISK_ROLES and rk != "NONE":
            facet_leak.append(("FACET_RISK", "%s(%s) emitted %s" % (rt_, exp, rk)))
    ctx = prim["detected_context"] if prim else "-"
    role = prim["runtime_role"] if prim else "-"
    risk = str(prim["risk_level"]) if prim else "-"
    wit = {w["codepoint"] for w in rep["uncarded_invisibles"]}
    return dict(ctx=ctx, role=role, risk=risk, verdict=rep["effective_action"],
                witness=wit, facet_leak=facet_leak)


def classify(m, meas, stage=""):
    errs = []
    key = lambda n: (m[stage + n] if (stage + n) in m else m[n])
    exp_ctx = key("ctx"); exp_risk = key("risk"); exp_verd = key("verdict")
    exp_wit = m["witness"]
    forb = m.get("forbidden", {})
    if meas["facet_leak"]:
        errs.append(("FACET_LEAK", str(meas["facet_leak"])))
    if meas["witness"] != exp_wit:
        missing = exp_wit - meas["witness"]; extra = meas["witness"] - exp_wit
        if missing:
            errs.append(("WITNESS_LOST", "missing %s" % sorted(missing)))
        if extra:
            errs.append(("WITNESS_FLOOD", "extra %s" % sorted(extra)))
    if meas["ctx"] in forb.get("ctx", set()):
        errs.append(("FORBIDDEN_CTX", meas["ctx"]))
    if meas["risk"] in forb.get("risk", set()):
        errs.append(("FORBIDDEN_RISK", meas["risk"]))
    if meas["verdict"] in forb.get("verdict", set()):
        errs.append(("FORBIDDEN_VERDICT", meas["verdict"]))
    verd_ok = meas["verdict"] in exp_verd
    ctx_ok = meas["ctx"] in exp_ctx
    risk_ok = meas["risk"] in exp_risk
    if not verd_ok:
        if meas["verdict"] == "pass" and any(x in exp_verd for x in ("queue_for_review", "hold_pending_review")):
            errs.append(("FALSE_NEGATIVE", meas["verdict"]))
        elif meas["verdict"] == "hold_pending_review":
            errs.append(("FALSE_POSITIVE_HOLD", meas["verdict"]))
        elif meas["verdict"] == "queue_for_review":
            errs.append(("FALSE_POSITIVE_QUEUE", meas["verdict"]))
        else:
            errs.append(("VERDICT_MISMATCH", meas["verdict"]))
    if verd_ok and not ctx_ok and exp_ctx != {"-"}:
        errs.append(("CONTEXT_MISMATCH_SAME_VERDICT", "got %s want %s" % (meas["ctx"], sorted(exp_ctx))))
    if not risk_ok and meas["risk"] != "-" and "-" not in exp_risk and verd_ok:
        errs.append(("RISK_MISMATCH", "got %s want %s" % (meas["risk"], sorted(exp_risk))))
    return (len(errs) == 0, errs)


def run_case(m, sign, cards):
    meas = measure(m["input"], sign, cards)
    ok, errs = classify(m, meas)
    if m.get("differential"):
        raw = m["input"]; recon = raw.replace(sign, "")
        if sign not in raw:
            errs.append(("DIFF_NO_SOURCE_SIGN", "")); ok = False
        if recon == raw:
            errs.append(("DIFF_NO_RECONSTRUCTION", "")); ok = False
    dec = None
    if m.get("decoded_input"):
        dec = measure(m["decoded_input"], sign, cards)
        ok2, errs2 = classify(m, dec, stage="decoded_")
        errs += [("STAGE2:" + e[0], e[1]) for e in errs2]
        ok = ok and ok2
    return meas, dec, ok, errs


def battery_pass_set(sign, cards, manifest):
    ps = set()
    for m in manifest:
        _, _, ok, _ = run_case(m, sign, cards)
        if ok:
            ps.add(m["id"])
    return ps


def run_battery(name, sign, cards, manifest):
    print("=" * 130)
    print("%s BY_CODE battery -- verified core %d (live msl_mip_runtime; sign-scoped; hermetic TLD)"
          % (name, len(manifest)))
    print("=" * 130)
    print("\n[PREFLIGHT] codepoint dump + must_contain assertion")
    pf_fail = []
    for m in manifest:
        ords = [ord(c) for c in m["input"]]
        miss = ["U+%04X" % x for x in m["must_contain"] if x not in ords]
        if miss:
            pf_fail.append(m["id"])
        print("  %-4s len=%-3d must_contain=%s  %s"
              % (m["id"], len(m["input"]), ["U+%04X" % x for x in m["must_contain"]],
                 "OK" if not miss else "MISSING %s" % miss))
    print("  PREFLIGHT: %s" % ("ALL OK" if not pf_fail else "FAIL " + str(pf_fail)))

    print("\n[BASELINE] measured tuple vs manifest")
    print("%-4s %-10s %-34s %-22s %-6s %-20s %-8s %s"
          % ("ID", "CLASS", "INPUT", "CTX", "RISK", "VERDICT", "WIT", "RES"))
    print("-" * 130)
    cls_tally = {}
    err_counts = {}
    results = {}
    for m in manifest:
        meas, dec, ok, errs = run_case(m, sign, cards)
        results[m["id"]] = (ok, errs)
        cls_tally.setdefault(m["cls"], [0, 0])
        cls_tally[m["cls"]][0 if ok else 1] += 1
        for e, _ in errs:
            err_counts[e] = err_counts.get(e, 0) + 1
        res = "OK" if ok else "FAIL: " + ",".join(sorted({e for e, _ in errs}))
        print("%-4s %-10s %-34s %-22s %-6s %-20s %-8s %s"
              % (m["id"], m["cls"], cps(m["input"])[:34], meas["ctx"], meas["risk"],
                 meas["verdict"], (",".join(sorted(meas["witness"])) or "-"), res))
        if dec is not None:
            print("        - STAGE2(decoded): ctx=%s risk=%s verdict=%s wit=%s"
                  % (dec["ctx"], dec["risk"], dec["verdict"], sorted(dec["witness"]) or "-"))
        if not ok:
            for e, d in errs:
                print("           - %s: %s" % (e, d))
    tp = sum(v[0] for v in cls_tally.values())
    tt = sum(v[0] + v[1] for v in cls_tally.values())
    print("\n  %s SCORE: %d/%d" % (name, tp, tt))
    if err_counts:
        print("  ERRORS BY TYPE: " + ", ".join("%s=%d" % (e, err_counts[e]) for e in sorted(err_counts)))
    return {cid for cid, (ok, _) in results.items() if ok}


def mutation_adequacy(name, sign, cards, manifest, baseline_pass):
    print("\n" + "=" * 60)
    print("%s MUTATION-ADEQUACY (test of the test)" % name)
    print("=" * 60)
    _orig_ctx = se._detect_context_at
    _orig_cand = rt._invisible_candidate
    _orig_scan = rt.scan_signs
    _orig_role = dict(se._RELATION_RUNTIME_ROLE)

    def m1():
        def swapped(text, offset, mask=frozenset()):
            r = _orig_ctx(text, offset, mask)
            return {"HOST": "PATH", "PATH": "HOST"}.get(r, r)
        se._detect_context_at = swapped

    def m3():
        def noz(text, cs):
            return _orig_scan(text, [c for c in cs if c.visible_form != sign])
        rt.scan_signs = noz

    muts = [
        ("M1_HOST_PATH_SWAP", m1, lambda: setattr(se, "_detect_context_at", _orig_ctx)),
        ("M2_WITNESS_OFF", lambda: setattr(rt, "_invisible_candidate", lambda ch: (None, "")),
         lambda: setattr(rt, "_invisible_candidate", _orig_cand)),
        ("M3_SIGN_SCAN_OFF", m3, lambda: setattr(rt, "scan_signs", _orig_scan)),
        ("M4_FACET_RISK_PRODUCING",
         lambda: se._RELATION_RUNTIME_ROLE.__setitem__("ABSENCE_CONFUSABLE", "PRIMARY"),
         lambda: (se._RELATION_RUNTIME_ROLE.clear(), se._RELATION_RUNTIME_ROLE.update(_orig_role))),
        ("M5_CTX_ALWAYS_FREETEXT",
         lambda: setattr(se, "_detect_context_at", lambda text, offset, mask=frozenset(): "FREE_TEXT"),
         lambda: setattr(se, "_detect_context_at", _orig_ctx)),
    ]
    killed = 0
    for nm, do, undo in muts:
        try:
            do()
            mut_pass = battery_pass_set(sign, cards, manifest)
        finally:
            undo()
        regressed = baseline_pass - mut_pass
        is_killed = len(regressed) > 0
        killed += 1 if is_killed else 0
        print("  %-26s: %s  (breaks %d baseline-correct: %s)"
              % (nm, "KILLED" if is_killed else "SURVIVED (BLIND SPOT)",
                 len(regressed), sorted(regressed)[:8]))
    print("\n  %s MUTATION_ADEQUACY: %d/%d killed" % (name, killed, len(muts)))
    stable = battery_pass_set(sign, cards, manifest) == baseline_pass
    print("  (sanity) baseline pass-set stable after mutations: %s" % stable)
    return killed, len(muts), stable
