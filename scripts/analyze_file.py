# -*- coding: utf-8 -*-
"""Run a real text file through the live core and print an honest summary.

Usage:  py -3 scripts/analyze_file.py <path> [--report]

Built for the question "how do I check this on REAL Khmer text" (2026-08-06):
counts every carded-invisible occurrence, shows how many were exempted as
normative functional positions (and on what basis), which contexts kept their
risk, and the final verdict. --report additionally prints the full report.
The summary never prints raw invisible characters (anti-retransmission).
"""
import contextlib
import io
import os
import sys
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
_BASE = os.path.dirname(_HERE)
for _p in ("core", "single_sign", "sequence"):
    sys.path.insert(0, os.path.join(_BASE, _p))
sys.path.insert(0, _BASE)

import msl_mip_runtime as rt   # noqa: E402


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    path = sys.argv[1]
    text = open(path, "r", encoding="utf-8", errors="replace").read()
    cards = rt.load_all_cards()

    t0 = time.perf_counter()
    with contextlib.redirect_stdout(io.StringIO()):
        r = rt.analyze(text, cards)
    dt = time.perf_counter() - t0

    invis = {0x200B: "ZWSP", 0x200C: "ZWNJ", 0x200D: "ZWJ",
             0x2060: "WJ", 0xFEFF: "BOM", 0x00AD: "SHY"}
    counts = {}
    for ch in text:
        if ord(ch) in invis:
            counts[invis[ord(ch)]] = counts.get(invis[ord(ch)], 0) + 1

    print("=" * 66)
    print("FILE: %s  (%d chars, %.2fs)" % (os.path.basename(path), len(text), dt))
    print("invisible carriers present: %s"
          % (", ".join("%s x%d" % kv for kv in sorted(counts.items())) or "none"))

    bd = [v for v in r["sequence_output"].relation_verdicts
          if v.get("relation_type") == "BOUNDARY_DISRUPTOR"]
    exempted = [v for v in bd if v.get("sni_functional")]
    live = [v for v in bd if not v.get("sni_functional")
            and v.get("risk_level") not in (None, "NONE")]
    print("BOUNDARY_DISRUPTOR occurrences: %d" % len(bd))
    by_basis = {}
    for v in exempted:
        by_basis[v["sni_functional"]] = by_basis.get(v["sni_functional"], 0) + 1
    print("  exempted as normative:  %d  %s"
          % (len(exempted),
             " ".join("[%s x%d]" % kv for kv in sorted(by_basis.items()))))
    by_ctx = {}
    for v in live:
        key = (v["detected_context"], v["risk_level"])
        by_ctx[key] = by_ctx.get(key, 0) + 1
    print("  still carrying risk:    %d  %s"
          % (len(live),
             " ".join("[%s/%s x%d]" % (c, rl, n)
                      for (c, rl), n in sorted(by_ctx.items()))))

    agg = r.get("sni_card")
    if agg:
        print("witness aggregate: %d occurrence(s): %s"
              % (agg["exempted_total"],
                 ", ".join("%s %s x%d" % (x["sign"], x["basis"], x["count"])
                           for x in agg["by_sign_basis"])))
    zw = r.get("zw_bits") or {}
    if zw.get("contributed"):
        print("ZW-BITS: CONTRIBUTED (carrier-pair channel candidate)")
    ig = r.get("input_guard") or {}
    print("input guard: %s (invisible share %.4f)"
          % (ig.get("status"), (ig.get("counters") or {}).get("invisible_share", 0)))
    print("FINAL: semantic=%s  effective=%s"
          % (r["semantic_action"], r["effective_action"]))
    print("=" * 66)
    if "--report" in sys.argv:
        rt.print_report(r)


if __name__ == "__main__":
    main()
