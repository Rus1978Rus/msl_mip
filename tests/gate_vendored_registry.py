# -*- coding: utf-8 -*-
"""GATE: vendored domain registries + honest degradation (2026-08-07).

Two defects were measured and are pinned here so they cannot return.

  1. THE DEFAULT REACHED FOR THE NETWORK. An air-gapped install -- the environment
     that needs this system most -- silently ran on a 163-entry embedded remnant
     standing in for a 1438-entry registry. The registries now ship in the repo and
     are the default; the network is opt-in via MSL_MIP_ALLOW_NETWORK.
  2. THE DEGRADATION WAS INVISIBLE. The health check asked only "are there at least
     100 entries?" and threw the SOURCE away, so the 163-entry remnant reported
     itself HEALTHY. Degradation is now decided by provenance, with the size floor
     KEPT as an independent second condition (a truncated full registry is degraded
     too, whatever its label says).

  A DEFAULT IS OFFLINE: with the network forbidden and no cache, resolution must
    succeed from the vendored snapshot and must not attempt a single connection.
  B PINS: both snapshots verify by sha256; a tampered or missing file is refused
    rather than used silently (the pattern the Unicode tables already follow).
  C HONEST DEGRADATION: every source string maps to the right flag -- full
    registries healthy, stand-ins degraded, unknown/empty degraded (fail-closed).
  D ZERO VERDICT DELTA: moving from the embedded remnant to the vendored registry
    must not move verdicts on a domain corpus. The vendored list is a superset,
    so this proves the change is provenance-only, not a behaviour change.
  E COVERAGE: the vendored registry must actually be the full one -- an order of
    magnitude more entries than the remnant it replaces.
All non-ASCII literals via chr() (english-only gate).
"""
import contextlib
import io
import os
import shutil
import sys
import tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))
_BASE = os.path.dirname(_HERE)
for _p in ("core", "single_sign", "sequence"):
    sys.path.insert(0, os.path.join(_BASE, _p))
sys.path.insert(0, _BASE)

# NOTE: this gate must NOT set MSL_MIP_HERMETIC_TLD -- hermetic mode bypasses the
# very resolution path under test. It stays offline by asserting zero network use.
os.environ.pop("MSL_MIP_HERMETIC_TLD", None)
os.environ.pop("MSL_MIP_ALLOW_NETWORK", None)

import urllib.request

_NETWORK_CALLS = []


def _blocked(*args, **kwargs):
    _NETWORK_CALLS.append(args[0] if args else "?")
    raise OSError("network access is not permitted in this gate")


urllib.request.urlopen = _blocked

import public_suffix as ps          # noqa: E402
import sequence_engine as se        # noqa: E402
import msl_mip_runtime as rt        # noqa: E402

fails = []

# A. Default resolution is offline and complete.
tlds, tld_source = ps.load_single_tlds()
comp, comp_source = ps.load_compound_suffixes()
if tld_source != "VENDORED":
    fails.append("A single TLDs came from %r, expected VENDORED" % tld_source)
if comp_source != "VENDORED":
    fails.append("A compound suffixes came from %r, expected VENDORED" % comp_source)
if _NETWORK_CALLS:
    fails.append("A the default path attempted %d network call(s): %s"
                 % (len(_NETWORK_CALLS), _NETWORK_CALLS[:2]))

# B. Pins: tampered and missing snapshots are refused, not used.
_tmp = tempfile.mkdtemp(prefix="vendor_gate_")
try:
    tampered = os.path.join(_tmp, "tlds.txt")
    shutil.copyfile(ps._VENDORED_TLD_FILE, tampered)
    with open(tampered, "a", encoding="utf-8") as f:
        f.write("\nattacker-controlled-tld\n")
    if ps._read_vendored(tampered, ps._VENDORED_TLD_SHA256) is not None:
        fails.append("B a tampered snapshot was accepted")
    if ps._read_vendored(os.path.join(_tmp, "absent.txt"),
                         ps._VENDORED_TLD_SHA256) is not None:
        fails.append("B a missing snapshot was accepted")
finally:
    shutil.rmtree(_tmp, ignore_errors=True)

# C. Honest degradation by provenance.
for source, want_full in [("LIVE_FETCH", True), ("VENDORED", True),
                          ("CACHE_FROM_2026-08-06T12:00:00", True),
                          ("EMBEDDED_FALLBACK", False),
                          ("EMBEDDED_HERMETIC", False), ("", False),
                          ("SOMETHING_NEW", False)]:
    if ps.is_full_registry(source) != want_full:
        fails.append("C source %r classified wrongly (full=%s, want %s)"
                     % (source, not want_full, want_full))
# And the live flag agrees with the live source.
se._reset_tld_state_for_test()
live_set, live_degraded = se._tlds()
if se.tld_source() != "VENDORED" or live_degraded:
    fails.append("C live state: source=%s degraded=%s (want VENDORED / False)"
                 % (se.tld_source(), live_degraded))

# D. Zero verdict delta between the remnant and the vendored registry.
_CARDS = rt.load_all_cards()
CORPUS = ["paypal.com.security-check.ru/verify", "www.bbc.co.uk/news",
          "shop.mysite.io", "a.co.jp/x", "cdn.jsdelivr.net/npm/pkg/dist/x.js",
          "s3.eu-central-1.amazonaws.com/b/k", "blog.stackoverflow.com.au",
          "com.apple.finder", "mail.google.com", "test.gov.uk/page",
          "site.com.br/login", "x.net.au", "foo.bar.edu.pl",
          "paypal.com.verify.shop", "api.service.travel", "my.app.dev",
          "deep.sub.domain.co.za", "bank.com.mx/auth", "example.museum"]


def _verdicts(tld_set):
    se._force_tld_state_for_test(tld_set, False)
    out = {}
    for text in CORPUS:
        with contextlib.redirect_stdout(io.StringIO()):
            out[text] = rt.analyze(text, _CARDS)["effective_action"]
    return out


before = _verdicts(ps.EMBEDDED_TLD_FALLBACK)
after = _verdicts(tlds)
moved = [(t, before[t], after[t]) for t in CORPUS if before[t] != after[t]]
for text, a, b in moved:
    fails.append("D verdict moved with the registry swap: %s %s -> %s" % (text, a, b))
se._reset_tld_state_for_test()

# E. The vendored registry is the full one, not another remnant.
if len(tlds) < 1000:
    fails.append("E vendored TLD registry has only %d entries" % len(tlds))
if len(comp) < 5000:
    fails.append("E vendored compound suffixes have only %d entries" % len(comp))
if len(tlds) <= len(ps.EMBEDDED_TLD_FALLBACK) * 5:
    fails.append("E vendored registry is not materially larger than the remnant")

print("=" * 66)
print("GATE: vendored domain registries + honest degradation")
print("=" * 66)
if fails:
    for f in fails:
        print("  FAIL: " + f)
    print("\nTOTAL: FAIL")
    sys.exit(1)
print("A default resolves offline from the vendored snapshots, zero network calls")
print("B tampered and missing snapshots are refused, never used silently")
print("C degradation follows provenance: %d source labels checked, live state honest"
      % 7)
print("D zero verdict delta across %d domains when swapping remnant -> vendored"
      % len(CORPUS))
print("E vendored registry is the full one: %d TLDs, %d compound suffixes (remnant: %d/%d)"
      % (len(tlds), len(comp), len(ps.EMBEDDED_TLD_FALLBACK), len(ps.EMBEDDED_FALLBACK)))
print("\nTOTAL: CLEAN")
sys.exit(0)
