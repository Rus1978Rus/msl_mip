#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIMULATION_GATE for SOLIDUS_SCHEME_PATCH — the permanent suite.
Extended per SIMULATION_GATE_REVIEW (6 reviewers, NEEDS_MORE_TESTS,
2026-07-07): edge-case classes added (scheme case, schemes with
+/-/., triple slash, invalid scheme, idx boundary, combinations,
the "does not crash" class).

Run: python3 gate_solidus_scheme.py
"""
import subprocess, sys, os

# cross-platform run: the runtime prints UTF-8 (Cyrillic in interp,
# emoji ☠), but Windows decodes subprocess as cp1251 by default ->
# the verdict is not found in a mangled string. Force UTF-8 everywhere.
#
# GATE_MUST_BE_HERMETIC (2026-07-12): MSL_MIP_HERMETIC_TLD=1 makes the
# runtime subprocess use the in-repo EMBEDDED TLD/suffix sets instead of
# fetching them LIVE from data.iana.org / publicsuffix.org at startup.
# Proven necessary: the "dot substitution" cases (paypal.com.security-
# check.ru -> HOLD) depend on 'ru' being a recognised TLD; a live fetch
# that dropped/garbled it silently flipped that case to PASS (the 27/28
# flake). The pinned embedded set contains 'ru', so the verdict is now
# deterministic and offline — no network required for the gate.
_ENV = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1",
            MSL_MIP_HERMETIC_TLD="1")

def _run(text):
    return subprocess.run(
        [sys.executable, "msl_mip_runtime.py", text],
        capture_output=True, text=True,
        encoding="utf-8", errors="replace", env=_ENV,
    )

# (input, expected_verdict, comment)
# verdict: PASS | HOLD  (HOLD = HOLD_PENDING_REVIEW)
CASES = [
    # --- basic: patch goal (scheme noise removed) ---
    ("http://example.com/page", "PASS", "clean URL — // noise removed"),
    ("https://github.com/user/repo", "PASS", "clean https"),
    ("ftp://server/file", "PASS", "ftp scheme"),
    # --- the @ discriminator is not broken ---
    ("http://paypal.com@evil.ru", "HOLD", "@ phishing with a scheme"),
    ("подпишись на @user@mastodon.social", "PASS", "federated handle"),
    ("ivan@example.com", "PASS", "ordinary email"),
    ("https://secure-paypal.com@192.168.1.5/verify", "HOLD", "brand+IP @"),
    ("http://evil.ru@paypal.com", "HOLD", "@ HIGH — the flag did NOT lower the neighbour"),
    # --- // without a valid scheme = HIGH (path traversal kept) ---
    ("a//b", "HOLD", "// without a scheme = HIGH"),
    (":://evil.com", "HOLD", "Q1: pseudo-scheme (no letter) NOT lowered"),
    ("://evil.com", "HOLD", "':// at start — idx boundary, no crash, HIGH"),
    ("1http://example", "HOLD", "a scheme starting with a digit is invalid (RFC) -> HIGH"),
    # --- Q4: enum aggregation, multiple // do not crash ---
    ("http://a//b", "HOLD", "Q4: scheme // + path // — enum max without a crash"),
    ("http:///path", "HOLD", "triple slash — the second // without a scheme HIGH"),
    # --- scheme case and special characters (RFC 3986 §3.1) ---
    ("HTTP://evil.com", "PASS", "uppercase scheme (case-insensitive)"),
    ("HtTp://evil.com", "PASS", "mixed-case scheme"),
    ("coap+tcp://host/path", "PASS", "a scheme with '+' is valid"),
    ("view-source://example", "PASS", "a scheme with '-' is valid"),
    # --- combinations of @ + dot + // ---
    ("http://paypal.com.security-check.ru/verify", "HOLD", "scheme + dot substitution"),
    ("paypal.com.security-check.ru/verify", "HOLD", "dot substitution without a scheme (regression)"),
    # --- control: other signs intact ---
    ("я тебя отравлю ☠", "HOLD", "☠ threat — control"),
]

# the "does not crash" class (Q4) — exception absence only
NO_CRASH = ["http://a//b//c", "scheme://///", ":////", "http://a//b//c//d",
            "://", "//", ":"]

def verdict_of(out):
    if "HOLD_PENDING_REVIEW" in out: return "HOLD"
    if "QUEUE" in out: return "QUEUE"
    if "PASS" in out: return "PASS"
    return "?"

def main():
    ok = 0
    print("=== SOLIDUS_SCHEME_PATCH gate ===")
    for text, exp, note in CASES:
        r = _run(text)
        got = verdict_of(r.stdout)
        mark = "✓" if got == exp else "✗"
        if got == exp: ok += 1
        print(f"  {mark} [{got:4}/{exp:4}] {note}")
    print(f"\n  verdicts: {ok}/{len(CASES)}")

    print("\n=== the 'does not crash' class (Q4) ===")
    nc_ok = 0
    for text in NO_CRASH:
        r = _run(text)
        crash = "Traceback" in r.stderr or "Error" in r.stderr
        mark = "✓" if not crash else "✗ CRASH"
        if not crash: nc_ok += 1
        print(f"  {mark} {text!r}")
    print(f"\n  no crashes: {nc_ok}/{len(NO_CRASH)}")

    total = ok + nc_ok
    grand = len(CASES) + len(NO_CRASH)
    print(f"\n=== TOTAL: {total}/{grand} ===")
    sys.exit(0 if total == grand else 1)

if __name__ == "__main__":
    main()
