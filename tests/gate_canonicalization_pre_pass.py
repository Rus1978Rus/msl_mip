#!/usr/bin/env python3
# SPDX: PRIVATE AUTHORIAL PROJECT / COMMERCIAL USE PROHIBITED
"""GATE: CANONICALIZATION_PRE_PASS skeleton.

Acceptance cases are the §7 table of
conveyor_runs/PREPASS_IMPL_CHECKLIST_2026-07-27.md, i.e. the concrete attacks
found by the three-observer red-team. This gate pins the skeleton's behaviour;
stages marked PARTIAL/TODO in the module have their currently-covered cases here
and their gaps documented (not silently passed).
"""
import os
import sys

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _BASE)

import canonicalization_pre_pass as pp  # noqa: E402


def encode_n(ch: str, n: int) -> str:
    """Nest percent-encoding n levels deep (one decode pass peels one level)."""
    s = ch
    for _ in range(n):
        s = "".join("%%%02x" % b for b in s.encode())
    return s


# (input, sink, max_passes, expected_status, expected_canonical_or_None, note)
CASES = [
    ("%2e%2e%2fetc%2fpasswd", pp.TEXT, 16, "CANON", "../etc/passwd",
     "percent-encoded traversal"),
    ("%252e%252e%252fetc/passwd", pp.TEXT, 16, "CANON", "../etc/passwd",
     "double-encoded (depth 2)"),
    ("%c0%ae%c0%ae%c0%afetc%c0%afpasswd", pp.TEXT, 16, "HOLD", None,
     "overlong-UTF-8 -> reject (S2)"),
    ("．．／etc／passwd", pp.TEXT, 16, "CANON", "../etc/passwd",
     "fullwidth confusables -> NFKC (S3)"),
    ("..%E2%80%8B/etc/passwd", pp.TEXT, 16, "CANON", "../etc/passwd",
     "zero-width injected -> strip (S4)"),
    ("&#46;&#46;&#47;etc&#47;passwd", pp.HTML, 16, "CANON", "../etc/passwd",
     "HTML entity, sink=HTML -> decode (S5)"),
    ("&#46;&#46;&#47;etc&#47;passwd", pp.UNKNOWN, 16, "HOLD", None,
     "same, sink=UNKNOWN -> fail-closed gate (§5b)"),
    ("2130706433", pp.HOST, 16, "CANON", "127.0.0.1",
     "integer IPv4 host -> dotted-quad (S6)"),
    ("0.0", pp.TEXT, 16, "CANON", "0.0",
     "benign / context-dependent downstream"),
    ("g00gle", pp.TEXT, 16, "CANON", "g00gle",
     "look-alike token -> unchanged canon (risk is downstream)"),
    ("..", pp.TEXT, 16, "CANON", "..",
     "parent-dir atom -> unchanged canon"),
    (encode_n(".", 4), pp.TEXT, 3, "HOLD", None,
     "decode-bomb (depth 4 > max_passes 3)"),
]


def main() -> None:
    print("=== CANONICALIZATION_PRE_PASS gate ===")
    ok = 0
    for raw, sink, mp, exp_status, exp_canon, note in CASES:
        r = pp.pre_pass(raw, sink, max_passes=mp)
        good = r.status == exp_status and (exp_status != "CANON" or r.canonical == exp_canon)
        if good:
            ok += 1
        got = r.canonical if r.status == "CANON" else f"HOLD({r.reason})"
        mark = "✓" if good else "✗"
        print(f"  {mark} [{r.status:5}] {note}")
        if not good:
            print(f"      got: {got!r}  expected: {exp_status}/{exp_canon!r}")

    print(f"\n=== TOTAL: {ok}/{len(CASES)} ===")
    print("KNOWN GAPS (documented, not silently passed): S2 full byte-validation,"
          " S3 cross-script confusable skeleton, S6 octal/IPv6/in-URL host,"
          " §6 use/mention detector (stub).")
    sys.exit(0 if ok == len(CASES) else 1)


if __name__ == "__main__":
    main()
