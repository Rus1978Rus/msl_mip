# -*- coding: utf-8 -*-
"""GATE: the environment probe explains a stall instead of leaving the user in it.

A file-sync service can keep this installation's data files in the cloud and
leave placeholders on disk; reading one then blocks while the OS downloads it,
with no error and no progress. Measured here: a 0.3s gate stalled past a
300-second timeout for exactly that reason.

The answer this project REFUSES is "tell the user to configure their sync
client" -- the same delegate-to-the-consumer move the SNI round rejected, since
an integration that freezes without explanation gets switched off and nobody
reads a manual to find out why. So the system detects the condition and says one
plain sentence about it, before the wait.

  A CHEAP AND SAFE: the probe answers from file ATTRIBUTES, so it must never
    open a data file -- otherwise it would trigger the very download it warns
    about -- and must stay far below the cost of an analysis.
  B HONEST WHEN IT CANNOT KNOW: on a platform without the API the answer is
    UNSUPPORTED and SILENT. A guess about the user's disk is worse than silence.
  C DETECTS THE REAL CONDITION: with the attribute present, the probe reports it,
    names the affected files, and produces a message that explains the pause in
    ordinary words -- no jargon about placeholders or reparse tags.
  D REPORT-ONLY: no verdict may depend on it. Analysis results are byte-identical
    whether the probe reports OK or a hazard.
All non-ASCII literals via chr() (english-only gate).
"""
import contextlib
import io
import os
import sys
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
_BASE = os.path.dirname(_HERE)
os.environ["MSL_MIP_HERMETIC_TLD"] = "1"
for _p in ("core", "single_sign", "sequence"):
    sys.path.insert(0, os.path.join(_BASE, _p))
sys.path.insert(0, _BASE)

import env_probe
import msl_mip_runtime as rt
import sequence_engine as se
_CARDS = rt.load_all_cards()
se._force_tld_state_for_test(
    frozenset({"com", "org", "net", "ru", "xn--p1ai"}), False)

fails = []

# A. Cheap, and it must not read file contents. `open` is replaced by a tripwire:
# any attempt to read a data file during the probe is a failure, because that is
# precisely the blocking operation the probe exists to predict.
_real_open = open
_opened = []


def _tripwire(path, *args, **kwargs):
    _opened.append(str(path))
    return _real_open(path, *args, **kwargs)


import builtins
builtins.open = _tripwire
try:
    t0 = time.perf_counter()
    state = env_probe.probe(_BASE)
    elapsed = time.perf_counter() - t0
finally:
    builtins.open = _real_open

if _opened:
    fails.append("A the probe opened %d file(s), e.g. %s -- it must read "
                 "attributes only" % (len(_opened), _opened[0]))
if elapsed > 2.0:
    fails.append("A probe cost %.2fs -- too slow to run before every session"
                 % elapsed)
if state["checked"] < 10:
    fails.append("A probe examined only %d files; the data directories should "
                 "hold more" % state["checked"])

# B. Honest where it cannot know.
if sys.platform.startswith("win"):
    if state["status"] not in ("OK", "CLOUD_PLACEHOLDERS_PRESENT"):
        fails.append("B unexpected status on Windows: %s" % state["status"])
else:
    if state["status"] != "UNSUPPORTED" or state["message"]:
        fails.append("B off-Windows the probe must be UNSUPPORTED and silent, "
                     "got %s / %r" % (state["status"], state["message"]))
# An unreadable or missing path is not a hazard claim.
if env_probe.is_cloud_placeholder(os.path.join(_BASE, "no_such_file_here.txt")):
    fails.append("B a missing file was reported as a cloud placeholder")

# C. It detects the real condition -- simulated at the attribute layer, which is
# the only part that differs between a hydrated and a dehydrated file.
_real_attrs = env_probe._attributes
try:
    env_probe._attributes = lambda path: 0x00400000  # RECALL_ON_DATA_ACCESS
    hazard = env_probe.probe(_BASE)
finally:
    env_probe._attributes = _real_attrs

if hazard["status"] != "CLOUD_PLACEHOLDERS_PRESENT":
    fails.append("C dehydrated files were not detected: %s" % hazard["status"])
if not hazard["pending"]:
    fails.append("C hazard reported without naming a single affected file")
msg = hazard["message"]
if not msg:
    fails.append("C hazard reported with no message for the human")
else:
    for jargon in ("placeholder", "reparse", "OneDrive", "hydrat", "attribute"):
        if jargon.lower() in msg.lower():
            fails.append("C message uses jargon the reader should not need: %r"
                         % jargon)
    if "download" not in msg.lower() or "not the analyzer" not in msg.lower():
        fails.append("C message must say what the pause IS and what it is not: "
                     "%r" % msg)

# D. Report-only: verdicts cannot depend on the probe.
def _verdict(text):
    with contextlib.redirect_stdout(io.StringIO()):
        return rt.analyze(text, _CARDS)["effective_action"]


SAMPLES = ["paypal.com.security-check.ru/verify", "www.bbc.co.uk/news",
           "goog" + chr(0x200B) + "le.com", "just some words here"]
before = [_verdict(t) for t in SAMPLES]
try:
    env_probe._attributes = lambda path: 0x00400000
    env_probe._CACHED = None
    after = [_verdict(t) for t in SAMPLES]
finally:
    env_probe._attributes = _real_attrs
    env_probe._CACHED = None
if before != after:
    fails.append("D verdicts changed with the probe state: %s vs %s"
                 % (before, after))

print("=" * 66)
print("GATE: environment probe (a stall is explained, not delegated)")
print("=" * 66)
if fails:
    for f in fails:
        print("  FAIL: " + f)
    print("\nTOTAL: FAIL")
    sys.exit(1)
print("A attributes only -- zero data files opened, %.3fs for %d files"
      % (elapsed, state["checked"]))
print("B silent where the platform cannot answer; a missing file is not a claim")
print("C the condition is detected, the files are named, and the sentence is")
print("  free of jargon: it says the pause is a download, not the analyzer")
print("D report-only: verdicts are identical with and without the hazard")
print("\nTOTAL: CLEAN")
sys.exit(0)
