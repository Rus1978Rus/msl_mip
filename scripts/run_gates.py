#!/usr/bin/env python3
"""
Single reproducible entry point for the repo's gate / battery scripts.

WHY THIS EXISTS: the gates in tests/ are standalone `__main__` runners (each
exits non-zero on failure), NOT pytest tests -- so `python -m pytest` discovers
nothing. This runner executes every gate as a subprocess, prints a pass/fail
summary, and exits non-zero if any gate fails. It is the CI / local entrypoint.

Run:  py -3 scripts/run_gates.py        (Windows)
      python3 scripts/run_gates.py      (Mac/Linux)

Exit code 0 = every gate green; 1 = at least one gate failed (or timed out).

Auto-discovers tests/*.py minus an explicit EXCLUDE list. New gate files are
picked up automatically; non-gate helpers must be added to EXCLUDE with a reason.
"""
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
TESTS = os.path.join(REPO, "tests")

# Non-gate files: imported modules or measure-only probes (no pass/fail contract).
EXCLUDE = {
    "zwsp_oracle_manifest.py": "module (MANIFEST imported by sim_bycode_v2), not a standalone gate",
    "reconcile_byspec_probe.py": "measure-only probe (no assert; always exits 0)",
}

TIMEOUT_S = 300


def discover():
    names = sorted(f for f in os.listdir(TESTS)
                   if f.endswith(".py") and not f.startswith("_"))
    return [n for n in names if n not in EXCLUDE]


def last_line(text):
    for line in reversed(text.splitlines()):
        if line.strip():
            return line.strip()[:80]
    return ""


def run_one(name):
    path = os.path.join(TESTS, name)
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    t0 = time.perf_counter()
    try:
        p = subprocess.run([sys.executable, path], cwd=REPO, env=env,
                           capture_output=True, text=True, encoding="utf-8",
                           timeout=TIMEOUT_S)
        dt = time.perf_counter() - t0
        ok = p.returncode == 0
        note = last_line(p.stdout) if ok else (last_line(p.stderr) or last_line(p.stdout))
        return ok, dt, p.returncode, note
    except subprocess.TimeoutExpired:
        return False, TIMEOUT_S, None, "TIMEOUT (> %ds)" % TIMEOUT_S


def main():
    gates = discover()
    print("=" * 74)
    print("GATE RUNNER -- %d gate script(s) from tests/ (excluded: %d)"
          % (len(gates), len(EXCLUDE)))
    print("=" * 74)
    failed = []
    for name in gates:
        ok, dt, rc, note = run_one(name)
        mark = "PASS" if ok else "FAIL"
        print("[%s] %-34s %7.2fs  %s" % (mark, name, dt, note))
        if not ok:
            failed.append((name, rc))
    print("=" * 74)
    if failed:
        print("RESULT: %d/%d PASSED, %d FAILED" % (len(gates) - len(failed), len(gates), len(failed)))
        for name, rc in failed:
            print("  FAILED: %s (exit %s)" % (name, rc))
        return 1
    print("RESULT: %d/%d PASSED -- all gates green" % (len(gates), len(gates)))
    if EXCLUDE:
        print("excluded (not gates): " + ", ".join(sorted(EXCLUDE)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
