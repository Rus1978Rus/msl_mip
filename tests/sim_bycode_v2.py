# -*- coding: utf-8 -*-
"""ZWSP TIER_2 BY_CODE v2 — verified core 21, tuple-reconcile, preflight,
mutation-adequacy. Live msl_mip_runtime. Measure only, no fix."""
import os, sys, importlib
os.environ["MSL_MIP_HERMETIC_TLD"]="1"
# Repo-relative paths (persistence fix, 2026-07-15): harness lives in
# <repo>/tests/, oracle manifest (zwsp_oracle_manifest.py) sits beside it.
# ONLY this path block differs from the original scratchpad harness
# (sha A55AF12BEC58750201806C21E69BD1582BFE24B1164CC8E3CD3E83A392D91699);
# battery, oracle import, measure/classify logic, mutations - byte-identical.
HERE=os.path.dirname(os.path.abspath(__file__))
BASE=os.path.dirname(HERE)
for p in ("core","single_sign","sequence"): sys.path.insert(0, os.path.join(BASE,p))
sys.path.insert(0, BASE); sys.path.insert(0, HERE)
import msl_mip_runtime as rt
import sequence_engine as se
from load_card import load_card
from sequence_engine import _force_tld_state_for_test
from zwsp_oracle_manifest import MANIFEST
_force_tld_state_for_test(frozenset({"com","org","net","ru","io","dev","xn--p1ai"}), False)
zwsp=load_card(os.path.join(BASE,"cards","SIGN_CORE_CARD_ZERO_WIDTH_SPACE_U200B_GEN3_v0_3_RU.md"))
mask=load_card(os.path.join(BASE,"cards","SIGN_CORE_CARD_FULLWIDTH_SOLIDUS_UFF0F_GEN3_v0_3_RU.md"))
CARDS=[zwsp,mask]
Z="​"

# M4-fix: an INDEPENDENT authoritative RELATION_TYPE -> EXPECTED_ROLE map, kept
# in the checker and NOT imported from the runtime, so a mutation that moves the
# runtime role map (and thus the emitted role too — the "consistent lie" M4
# exploited) is caught by comparison against this fixed reference.
_AUTH_EXPECTED_ROLE = {
    "BOUNDARY_DISRUPTOR": "PRIMARY",
    "ABSENCE_CONFUSABLE": "SUPPORTING_FACET",   # risk contribution NONE
    "INVISIBLE_CLASS_COLLISION": "TAXONOMY_ONLY",  # risk NONE
    "CONFUSABLE_OF": "PRIMARY", "NFKC_MAPS_TO": "PRIMARY", "VISUAL_MIMIC_OF": "PRIMARY",
    "": "PRIMARY",
}
_NONRISK_ROLES = {"SUPPORTING_FACET", "TAXONOMY_ONLY", "INVALID_EDGE"}

def cps(s):
    out=[]
    for ch in s:
        o=ord(ch)
        show=(o<0x20 or o==0x7f or 0x200b<=o<=0x206f or o in (0xfeff,0x2062,0x2063,0x043e,0xff0f,0x00a0,0x202f,0x2800)
              or 0x2028<=o<=0x2029 or 0xfe00<=o<=0xfe0f or o==0x202e or o>=0xe0000)
        out.append(f"<U+{o:04X}>" if show else ch)
    return "".join(out)

def measure(text):
    """Return the measured tuple for one input."""
    rep=rt.analyze(text,CARDS)
    prim=None; facet_leak=[]
    for v in rep["sequence_output"].relation_verdicts:
        if v["visible_form"]!=Z: continue
        rt_=v.get("relation_type"); role=v.get("runtime_role"); rk=v.get("risk_level")
        if rt_=="BOUNDARY_DISRUPTOR": prim=v
        # M4-fixed invariant (type-keyed, independent authoritative map):
        #  (a) emitted role MUST equal the authoritative EXPECTED_ROLE[type];
        #  (b) a non-PRIMARY role MUST emit NONE risk.
        # Either check kills a facet-risk mutation, even one that moves the
        # runtime role map in lock-step with the emitted value.
        exp=_AUTH_EXPECTED_ROLE.get(rt_, "INVALID_EDGE")
        if role!=exp:
            facet_leak.append(("ROLE_TAMPERED", f"{rt_}: emitted {role}, auth {exp}"))
        if exp in _NONRISK_ROLES and rk!="NONE":
            facet_leak.append(("FACET_RISK", f"{rt_}({exp}) emitted {rk}"))
    ctx=prim["detected_context"] if prim else "-"
    role=prim["runtime_role"] if prim else "-"
    risk=str(prim["risk_level"]) if prim else "-"
    wit={w["codepoint"] for w in rep["uncarded_invisibles"]}
    return dict(ctx=ctx, role=role, risk=risk, verdict=rep["effective_action"],
                witness=wit, facet_leak=facet_leak)

def classify(m, meas, stage=""):
    """Compare measured tuple to manifest expected. Return (ok, errors[])."""
    errs=[]
    key=lambda n: (m[stage+n] if (stage+n) in m else m[n])
    exp_ctx=key("ctx"); exp_risk=key("risk"); exp_verd=key("verdict")
    exp_wit=m["witness"]
    forb=m.get("forbidden",{})
    # facet leak = invariant break (kills M4)
    if meas["facet_leak"]:
        errs.append(("FACET_LEAK", str(meas["facet_leak"])))
    # witness
    if meas["witness"]!=exp_wit:
        missing=exp_wit-meas["witness"]; extra=meas["witness"]-exp_wit
        if missing: errs.append(("WITNESS_LOST", f"missing {sorted(missing)}"))
        if extra:   errs.append(("WITNESS_FLOOD", f"extra {sorted(extra)}"))
    # forbidden (hard)
    if meas["ctx"] in forb.get("ctx",set()):
        errs.append(("FORBIDDEN_CTX", meas["ctx"]))
    if meas["risk"] in forb.get("risk",set()):
        errs.append(("FORBIDDEN_RISK", meas["risk"]))
    if meas["verdict"] in forb.get("verdict",set()):
        errs.append(("FORBIDDEN_VERDICT", meas["verdict"]))
    # verdict acceptability
    verd_ok = meas["verdict"] in exp_verd
    ctx_ok  = meas["ctx"] in exp_ctx
    risk_ok = meas["risk"] in exp_risk
    if not verd_ok:
        if meas["verdict"]=="pass" and any(x in exp_verd for x in ("queue_for_review","hold_pending_review")):
            errs.append(("FALSE_NEGATIVE", meas["verdict"]))
        elif meas["verdict"]=="hold_pending_review":
            errs.append(("FALSE_POSITIVE_HOLD", meas["verdict"]))
        elif meas["verdict"]=="queue_for_review":
            errs.append(("FALSE_POSITIVE_QUEUE", meas["verdict"]))
        else:
            errs.append(("VERDICT_MISMATCH", meas["verdict"]))
    if verd_ok and not ctx_ok and exp_ctx!={"-"}:
        errs.append(("CONTEXT_MISMATCH_SAME_VERDICT", f"got {meas['ctx']} want {sorted(exp_ctx)}"))
    if not risk_ok and risk_ok is False and meas["risk"]!="-" and "-" not in exp_risk:
        # only report risk mismatch if not already covered by a verdict error
        if verd_ok:
            errs.append(("RISK_MISMATCH", f"got {meas['risk']} want {sorted(exp_risk)}"))
    return (len(errs)==0, errs)

def run_case(m):
    """Full evaluation of one manifest case (handles D4 two-stage)."""
    meas=measure(m["input"])
    ok, errs = classify(m, meas)
    # differential assert (D1)
    if m.get("differential"):
        raw=m["input"]; recon=raw.replace(Z,"")
        if Z not in raw: errs.append(("DIFF_NO_SOURCE_ZWSP","")); ok=False
        if recon==raw:   errs.append(("DIFF_NO_RECONSTRUCTION","")); ok=False
    # host attribution (D2)
    if m.get("host_must_not_be"):
        # engine has no host extraction at this layer -> record as capability note
        errs.append(("NO_HOST_EXTRACTION", f"engine cannot confirm host={m['host_should_be']} / not {m['host_must_not_be']}"))
        ok=False
    # D4 two-stage
    dec=None
    if m.get("decoded_input"):
        dec=measure(m["decoded_input"])
        ok2, errs2 = classify(m, dec, stage="decoded_")
        errs += [("STAGE2:"+e[0], e[1]) for e in errs2]
        ok = ok and ok2
    return meas, dec, ok, errs

# ---------- PREFLIGHT + BASELINE RUN ----------
print("="*130)
print("ZWSP TIER_2 BY_CODE v2 — verified core 21 (live msl_mip_runtime; cards=[ZWSP,FW-SOLIDUS]; hermetic TLD)")
print("="*130)
print("\n[PREFLIGHT] codepoint dump + must_contain assertion")
pf_fail=[]
for m in MANIFEST:
    ords=[ord(c) for c in m["input"]]
    miss=[f"U+{x:04X}" for x in m["must_contain"] if x not in ords]
    tag="OK" if not miss else f"MISSING {miss}"
    if miss: pf_fail.append(m["id"])
    print(f"  {m['id']:3} len={len(m['input']):3} must_contain={['U+%04X'%x for x in m['must_contain']]}  {tag}")
    if m.get("decoded_input"):
        do=[ord(c) for c in m["decoded_input"]]
        dm=[f"U+{x:04X}" for x in m.get("decoded_must_contain",[]) if x not in do]
        print(f"      decoded len={len(m['decoded_input'])} must_contain={['U+%04X'%x for x in m.get('decoded_must_contain',[])]}  {'OK' if not dm else 'MISSING '+str(dm)}")
print(f"  PREFLIGHT: {'ALL OK' if not pf_fail else 'FAIL '+str(pf_fail)}")

print("\n[BASELINE] measured tuple vs manifest")
hdr=f"{'ID':3} {'CLASS':10} {'INPUT':40} {'CTX':16} {'RISK':6} {'VERDICT':20} {'WIT':8} {'RES'}"
print(hdr); print("-"*130)
results={}
cls_tally={}
err_counts={}
for m in MANIFEST:
    meas,dec,ok,errs=run_case(m)
    results[m["id"]]=(ok,errs)
    cls_tally.setdefault(m["cls"],[0,0]); cls_tally[m["cls"]][0 if ok else 1]+=1
    for e,_ in errs: err_counts[e]=err_counts.get(e,0)+1
    res="OK" if ok else "FAIL: "+",".join(sorted({e for e,_ in errs}))
    print(f"{m['id']:3} {m['cls']:10} {cps(m['input'])[:40]:40} {meas['ctx']:16} {meas['risk']:6} {meas['verdict']:20} {(','.join(sorted(meas['witness'])) or '-'):8} {res}")
    if dec is not None:
        print(f"        └ STAGE2(decoded): ctx={dec['ctx']} risk={dec['risk']} verdict={dec['verdict']} wit={sorted(dec['witness']) or '-'}")
    if not ok:
        for e,d in errs: print(f"           - {e}: {d}")

print("\n"+"="*60); print("SCORE BY CLASS"); print("="*60)
for cls in ("registrar","positions","combo","url","dangerous","controls"):
    p,f=cls_tally.get(cls,[0,0]); print(f"  {cls:10}: {p}/{p+f} correct  ({f} errors)")
tp=sum(v[0] for v in cls_tally.values()); tt=sum(v[0]+v[1] for v in cls_tally.values())
print(f"  {'TOTAL':10}: {tp}/{tt}")
print("\nERRORS BY TYPE:")
for e in sorted(err_counts): print(f"  {e:32}: {err_counts[e]}")
baseline_pass={cid for cid,(ok,_) in results.items() if ok}

# ---------- MUTATION-ADEQUACY ----------
print("\n"+"="*60); print("MUTATION-ADEQUACY (test of the test)"); print("="*60)
def battery_pass_set():
    ps=set()
    for m in MANIFEST:
        _,_,ok,_=run_case(m)
        if ok: ps.add(m["id"])
    return ps

mutations=[]
# M1 HOST<->PATH swap in the context detector
_orig_ctx=se._detect_context_at
def m1():
    def swapped(text,offset,mask=frozenset()):
        r=_orig_ctx(text,offset,mask); return {"HOST":"PATH","PATH":"HOST"}.get(r,r)
    se._detect_context_at=swapped
def m1_undo(): se._detect_context_at=_orig_ctx
mutations.append(("M1_HOST_PATH_SWAP",m1,m1_undo))
# M2 disable witness predicate (STAGE_A candidate detection off)
_orig_cand=rt._invisible_candidate
def m2(): rt._invisible_candidate=lambda ch: (None,"")
def m2_undo(): rt._invisible_candidate=_orig_cand
mutations.append(("M2_WITNESS_OFF",m2,m2_undo))
# M3 disable U+200B scan (drop ZWSP from single-sign scan)
_orig_scan=rt.scan_signs
def m3():
    def noz(text,cards):
        return _orig_scan(text,[c for c in cards if c.visible_form!=Z])
    rt.scan_signs=noz
def m3_undo(): rt.scan_signs=_orig_scan
mutations.append(("M3_ZWSP_SCAN_OFF",m3,m3_undo))
# M4 supporting-facet made risk-producing (ABSENCE_CONFUSABLE -> PRIMARY)
_orig_role=dict(se._RELATION_RUNTIME_ROLE)
def m4(): se._RELATION_RUNTIME_ROLE["ABSENCE_CONFUSABLE"]="PRIMARY"
def m4_undo(): se._RELATION_RUNTIME_ROLE.clear(); se._RELATION_RUNTIME_ROLE.update(_orig_role)
mutations.append(("M4_FACET_RISK_PRODUCING",m4,m4_undo))
# M5 default context -> FREE_TEXT always
def m5(): se._detect_context_at=lambda text,offset,mask=frozenset(): "FREE_TEXT"
def m5_undo(): se._detect_context_at=_orig_ctx
mutations.append(("M5_CTX_ALWAYS_FREETEXT",m5,m5_undo))

killed=0
for name,do,undo in mutations:
    try:
        do(); mut_pass=battery_pass_set()
    finally:
        undo()
    regressed=baseline_pass - mut_pass   # baseline-correct cases the mutation breaks
    is_killed=len(regressed)>0
    killed+= 1 if is_killed else 0
    print(f"  {name:26}: {'KILLED' if is_killed else 'SURVIVED (BLIND SPOT)'}  "
          f"(breaks {len(regressed)} baseline-correct: {sorted(regressed)[:8]})")
print(f"\n  MUTATION_ADEQUACY: {killed}/{len(mutations)} killed")
# sanity: baseline unchanged after all undo
after={cid for cid,(ok,_) in [(m['id'],run_case(m)[2:3]+([],)) for m in MANIFEST]}
print(f"  (sanity) baseline pass-set stable after mutations: {battery_pass_set()==baseline_pass}")
