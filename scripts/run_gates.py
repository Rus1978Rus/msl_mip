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

ENVIRONMENT NOTE (measured 2026-08-07, keep before blaming a gate). This working
copy lives inside a OneDrive folder, so every one of its files is a cloud
placeholder (reparse tag 0x9000e01a). Two consequences, both observed:
  * git cannot delete .git/worktrees/main-wt -- an orphaned placeholder OneDrive
    holds -- so a "Permission denied" line appears on essentially every git
    command. It is noise from the filesystem, not a repository problem.
  * a gate can stall for minutes while OneDrive syncs or rehydrates files, with
    no fault in the gate. gate_tag_covert_text once hit the 300s timeout here
    immediately after 340KB of new data files were written; the same gate then
    measured 0.30-0.35s over 20 consecutive runs and has never repeated it.
When a timeout appears, check whether files were being written or synced at that
moment BEFORE looking for a hang in the code. The permanent fix is on the
machine, not here: pin the folder as "Always keep on this device", or keep the
working copy outside OneDrive.
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
    "verified_class_harness.py": "module (imported by zwj_bom_battery), not a standalone gate",
    "zwj_bom_manifests.py": "module (ZWJ/BOM manifests imported by zwj_bom_battery), not a gate",
}

TIMEOUT_S = 300
# The slowest honest gate is the UAX#9 conformance run (862k official cases,
# ~12s here); everything else is under a second. 30s is therefore well clear of
# normal work and still far below the timeout -- a gate crossing it is a signal
# to look at the machine while the suite is still green.
SLOW_S = 30


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
    except subprocess.TimeoutExpired as exc:
        # A timeout used to report a bare "exit None", which told us nothing: we
        # could not tell a genuinely hung gate from a stalled machine, and one
        # such event (2026-08-07, gate_tag_covert_text, a gate measured at 0.3s
        # over 20 consecutive runs) cost an investigation from zero. TimeoutExpired
        # CARRIES the partial output -- printing its last line names the section
        # the gate reached before it stopped, which is the difference between
        # evidence and a guess. The verdict stays FAILED either way: a timeout we
        # do not understand must not be swept into green.
        partial = _decode(exc.stdout) or _decode(exc.stderr)
        where = last_line(partial) if partial else "no output before the stall"
        return False, TIMEOUT_S, None, "TIMEOUT (>%ds) last output: %s" % (
            TIMEOUT_S, where)


def _decode(raw):
    if raw is None:
        return ""
    if isinstance(raw, bytes):
        return raw.decode("utf-8", "replace")
    return raw


def main():
    gates = discover()
    print("=" * 74)
    print("GATE RUNNER -- %d gate script(s) from tests/ (excluded: %d)"
          % (len(gates), len(EXCLUDE)))
    print("=" * 74)
    failed = []
    slow = []
    for name in gates:
        ok, dt, rc, note = run_one(name)
        mark = "PASS" if ok else "FAIL"
        # A gate that suddenly takes 30s where it used to take 0.3s is a warning
        # long before it becomes a 300s timeout. Flag it while it is still cheap
        # to notice: on this repository the usual cause is not the gate at all
        # but the filesystem (see ENVIRONMENT NOTE in the module docstring).
        tag = "  [SLOW]" if (ok and dt > SLOW_S) else ""
        print("[%s] %-34s %7.2fs  %s%s" % (mark, name, dt, note, tag))
        if not ok:
            failed.append((name, rc))
        elif dt > SLOW_S:
            slow.append((name, dt))
    print("=" * 74)
    if slow:
        print("SLOW (green, but far above their usual cost -- check the machine "
              "before the code):")
        for name, dt in slow:
            print("  %-34s %.2fs" % (name, dt))
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
