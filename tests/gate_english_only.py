#!/usr/bin/env python3
"""
GATE: English-only code (hygiene guard).

Project rule: code text (comments, docstrings, warnings, outputs) is
ENGLISH ONLY. Cards/templates/manifest are multilingual — but they are
documents, not code, and are not checked here.

Allowlist — functional non-English DATA is permitted by design:
  DETECTION_KEYWORDS      — multilingual threat dictionaries in matchers;
  TEST_INPUTS             — test strings exercising Russian detection;
  HOMOGLYPH_SPECIMENS     — e.g. a Cyrillic letter inside a test domain is the
                            very subject of a homoglyph test.

Any OTHER Cyrillic line in a .py file fails this gate: it means a new
tool/session dragged Russian text back into the code.
"""

import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# file -> reason (whole-file allowlist: data-bearing files)
ALLOWLIST = {
    os.path.join("single_sign", "matchers", "skull_matcher.py"):
        "DETECTION_KEYWORDS (multilingual dictionaries)",
    os.path.join("single_sign", "matchers", "skull_crossbones_matcher.py"):
        "DETECTION_KEYWORDS (multilingual dictionaries)",
    os.path.join("tests", "gate_solidus_scheme.py"):
        "TEST_INPUTS (Russian detection cases)",
    os.path.join("tests", "gate_relation_verdict_step4.py"):
        "HOMOGLYPH_SPECIMENS (Cyrillic letter in the test domain is the test subject)",
    os.path.join("tests", "gate_bare_domain_detector.py"):
        "HOMOGLYPH_SPECIMENS (Cyrillic homoglyph + IDN domains are the test subject)",
}

CYR = re.compile(r"[\u0400-\u04FF]")

failures = []
checked = 0
allowed_hits = 0

for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in dirs if d != "__pycache__" and not d.startswith(".")]
    for fname in files:
        if not fname.endswith(".py"):
            continue
        path = os.path.join(root, fname)
        rel = os.path.relpath(path, BASE)
        checked += 1
        try:
            text = open(path, encoding="utf-8").read()
        except UnicodeDecodeError:
            failures.append((rel, 0, "NOT UTF-8"))
            continue
        for n, line in enumerate(text.splitlines(), 1):
            if CYR.search(line):
                if rel in ALLOWLIST:
                    allowed_hits += 1
                else:
                    failures.append((rel, n, line.strip()[:70]))

print("=" * 60)
print("GATE: English-only code")
print("=" * 60)
print(f"checked .py files: {checked}")
print(f"allowlisted data lines: {allowed_hits} "
      f"(in {len(ALLOWLIST)} data-bearing files)")

if failures:
    print(f"\nFAIL — Cyrillic outside the allowlist ({len(failures)} lines):")
    for rel, n, frag in failures[:20]:
        print(f"  {rel}:{n}: {frag}")
    print("\nTOTAL: FAIL")
    sys.exit(1)

print("\nTOTAL: CLEAN — no Cyrillic outside functional data")
sys.exit(0)
