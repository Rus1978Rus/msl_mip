# -*- coding: utf-8 -*-
"""GATE: an uncarded class-138 member that breaks a HOST escalates (D-INV-GEN).

MEASURED systemic hole: only ZWSP/ZWJ/BOM are carded, so the other ~135 supervised code
points (invisible math operators U+2061..U+2064, WORD JOINER, SOFT HYPHEN, TAG chars, ...)
reached the human only as a non-blocking witness -- effective pass -- even inside a phishing
host, where the byte-exact evasion is identical to a carded sign's. AUTHOR_DECISION
D-O1... D-INV-GEN 2026-07-22 generalizes: an invisible that breaks a HOST label escalates
whether or not it is carded.

FIRST CUT scope (pending the follow-up conveyor): HOST only. Token/email/free-text stay
witness-only. The change is ADDITIVE -- an effective_action raise; the witness channel and
the main path (semantic_action) are untouched, and it fails open.

  A ESCALATES -- several uncarded class-138 members in a host -> effective hold, witness kept.
  B WITNESS-ONLY ELSEWHERE -- the same member in a token / free text stays pass + witness.
  C NO REGRESSION -- carded host-break still hold; clean domain passes; non-138 invisible
    (braille) does not escalate; a legit accented domain with no invisible passes.
Basis: hole-hunt 2026-07-22; AUTHOR_DECISION_20260722_D-INV-GEN.
"""
import contextlib
import io
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_BASE = os.path.dirname(_HERE)
os.environ["MSL_MIP_HERMETIC_TLD"] = "1"
for _p in ("core", "single_sign", "sequence"):
    sys.path.insert(0, os.path.join(_BASE, _p))
sys.path.insert(0, _BASE)

import msl_mip_runtime as rt
import sequence_engine as se
se._force_tld_state_for_test(frozenset({"com", "org", "net", "ru", "io", "dev", "xn--p1ai"}), False)
CARDS = rt.load_all_cards()

fails = []
UNCARDED = {0x2061: "FUNCTION APPLICATION", 0x2062: "INVISIBLE TIMES",
            0x2063: "INVISIBLE SEPARATOR", 0x2064: "INVISIBLE PLUS",
            0x2060: "WORD JOINER", 0x00AD: "SOFT HYPHEN", 0x061C: "ARABIC LETTER MARK",
            0xE0061: "TAG LATIN SMALL A"}
ZWSP = 0x200B
BRAILLE = 0x2800   # visible-blank, NOT class-138 (Cf∧DI) -> must stay witness-only


def rep(text):
    with contextlib.redirect_stdout(io.StringIO()):
        return rt.analyze(text, CARDS)


# ------------------------------------------------------------------ A ESCALATES
# Level is QUEUE, not hold (corrected 2026-07-22): the escalation fires on ordinary prose
# that reconstructs to a "word.tld" shape too (measured 5/8 benign), so hold was
# over-alarming. queue surfaces the anomaly quietly; hold returns with CONTEXT_V2.
for cp, name in UNCARDED.items():
    r = rep("goog" + chr(cp) + "le.com")
    if r["effective_action"] != "queue_for_review":
        fails.append("A uncarded %s (U+%04X) host-break did not surface at queue: %s"
                     % (name, cp, r["effective_action"]))
    if not r["uncarded_invisibles"]:
        fails.append("A uncarded %s lost its witness record while escalating" % name)
    if r["semantic_action"] != "pass":
        fails.append("A main-path semantic_action changed for %s (want pass): %s"
                     % (name, r["semantic_action"]))

# --------------------------------------------------- B WITNESS-ONLY ELSEWHERE
for cp, name in list(UNCARDED.items())[:4]:
    for label, text in (("token", "bad" + chr(cp) + "word"),
                        ("free text", "hello " + chr(cp) + " there")):
        r = rep(text)
        if r["effective_action"] != "pass":
            fails.append("B uncarded %s in %s escalated (want pass): %s"
                         % (name, label, r["effective_action"]))
        if not r["uncarded_invisibles"]:
            fails.append("B uncarded %s in %s lost its witness" % (name, label))

# --------------------------------------------------------------- C NO REGRESSION
noreg = [
    ("carded ZWSP host still holds", "goog" + chr(ZWSP) + "le.com", "hold_pending_review"),
    ("clean domain passes", "google.com", "pass"),
    ("braille (not class-138) does NOT escalate in host", "goog" + chr(BRAILLE) + "le.com", "pass"),
    ("legit accented domain, no invisible, passes", "caf" + "́" + "e.com", "pass"),
    ("clean text passes", "the quick brown fox", "pass"),
]
for label, text, want in noreg:
    got = rep(text)["effective_action"]
    if got != want:
        fails.append("C REGRESSION [%s]: %s (want %s)" % (label, got, want))

print("=" * 66)
print("GATE: uncarded class-138 host-break escalates (D-INV-GEN)")
print("=" * 66)
if fails:
    for f in fails:
        print("  FAIL: " + f)
    print("\nTOTAL: FAIL")
    sys.exit(1)
print("A %d uncarded members (math ops / word joiner / soft hyphen / tag / arabic mark) escalate in a host, witness kept"
      % len(UNCARDED))
print("B the same members in a token / free text stay pass + witness (HOST-only first cut)")
print("C no regression: carded still holds; clean/braille/accented pass")
print("\nTOTAL: CLEAN -- an invisible that breaks a host is held whether or not it is carded")
sys.exit(0)
