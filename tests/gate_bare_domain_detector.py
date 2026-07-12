#!/usr/bin/env python3
"""
GATE: bare-domain detector (Г1) — NEW_ARTIFACT reconstructed 2026-07-12
from the six FIX_VERIFICATION runs used AS A REQUIREMENTS SPEC.

Covers every reviewer finding, including the two that became author
decisions:
  D-DET-1  two+ masks in one token -> remove ALL masks before the domain
           check; remainder domain-like -> HOST (the P6 double-mask miss).
  D-DET-2  TLD registry unavailable -> domain-shaped token with a mask
           raises an alarm, not silence; the whole run is marked DEGRADED.

Plus the unanimously-passing patches (P2 IDN, P3 outer punctuation, P4
scheme-scope, P5 right-domain tail), the glued-scheme V2 concern, a CJK
false-positive guard, and the zero-width boundary (asserted as a KNOWN
LIMITATION, shown explicitly — not hidden).

FIX_FIRST (2026-07-12, first conveyor round — see foundation_layer/
AUTHOR_DECISION_20260712_BARE_DOMAIN_DETECTOR_FIX_FIRST_ROUND1.md):
  BLOCKER   _domain_prefix rewritten from a punctuation block-list to a
            positive letter/digit/'-'/'.' extraction — three reviewers
            found the block-list bypass (any wrapping character absent
            from the list stuck to the domain and silently fell to
            FREE_TEXT).
  D-DET-3   concatenation false positives from the positive-extraction
            heuristic are DOCUMENTED here as known/accepted, not fixed
            (no full URL parser in scope).
  v0.5      two further tails added as known, deferred: an
            already-punycode TLD label absent from the active registry,
            and a leading-hyphen label (RFC-invalid, currently accepted).

Hermetic: the TLD registry is pinned via _force_tld_state_for_test, so
the gate needs no network and can drive the DEGRADED path deterministically.

Verified live via process_sign + process_sequence.
"""

import os
import sys
import tempfile

# GATE_MUST_BE_HERMETIC: this gate already pins the TLD state in-process via
# _force_tld_state_for_test (so sequence_engine._tlds() never fetches), but
# set the env flag too so ANY public_suffix.load_*() reached by an
# unforeseen path also returns the offline embedded set — belt and braces,
# uniform with the other gates. No network required, deterministic.
os.environ["MSL_MIP_HERMETIC_TLD"] = "1"

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "core"))
sys.path.insert(0, os.path.join(BASE, "single_sign"))
sys.path.insert(0, os.path.join(BASE, "sequence"))

from load_card import load_card
from module_engine import process_sign
from sequence_engine import (
    process_sequence,
    _detect_context_at,
    _looks_like_domain,
    _force_tld_state_for_test,
    _reset_tld_state_for_test,
)

PASSED = 0
FAILED = 0


def check(label, cond, detail=""):
    global PASSED, FAILED
    if cond:
        PASSED += 1
        print(f"  ✓ {label}")
    else:
        FAILED += 1
        print(f"  ✗ {label}  {detail}")


def _card(text):
    f = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8")
    f.write(text)
    f.close()
    return load_card(f.name)


# VERIFIED mask card, scope URL/HOST/PATH — mirrors the real fullwidth
# solidus card, so HOST->HIGH, PATH/URL->MEDIUM, FREE_TEXT->NONE.
MASK_CARD = """CARD_UID: BD
CODEPOINT: U+FF0F
VISIBLE_FORM: ／
UNICODE_NAME: FULLWIDTH SOLIDUS
ZONE: ZONE_2
DOCUMENT_STATUS: WORKING_DRAFT
SIGN_RELATIONS:
  RELATION_001:
    RELATION_TYPE: NFKC_MAPS_TO
    TARGET: U+002F
    CONTEXT_SCOPE: URL, HOST, PATH
    VERIFICATION_STATUS: VERIFIED
    RUNTIME_EFFECT: RELATION_ONLY
"""


def _run(card, text):
    """Process EVERY mask occurrence in the text (so double-mask tokens
    produce a verdict per mask), then run the sequence layer."""
    offs = [i for i, ch in enumerate(text) if ch == "／"]
    sts = [process_sign(card, text, o) for o in offs]
    return process_sequence(text, [card], sign_statuses=sts, known_signs={"／"})


def _ctx(card, text):
    """detected_context of the FIRST mask verdict."""
    vd = _run(card, text).relation_verdicts
    return vd[0]["detected_context"] if vd else None


def _risk(card, text):
    vd = _run(card, text).relation_verdicts
    return vd[0]["risk_level"] if vd else None


# A pinned, healthy TLD set — deterministic and offline. Includes the
# punycode A-label for .рф so the IDN case does not depend on the live
# IANA registry.
_PINNED_TLDS = frozenset({"com", "org", "net", "md", "ru", "io", "xn--p1ai"})

print("=" * 64)
print("GATE: bare-domain detector (Г1) — NEW_ARTIFACT, NOT_REVIEWED")
print("=" * 64)

card = _card(MASK_CARD)
_force_tld_state_for_test(_PINNED_TLDS, degraded=False)

# --- V1/P3: outer punctuation trimmed, domain still recognised ---
print("\n[P3] Outer punctuation around a bare domain -> HOST")
check("(gоog／le.com) -> HOST", _ctx(card, "(gоog／le.com)") == "HOST", _ctx(card, "(gоog／le.com)"))
check('"gоog／le.com" -> HOST', _ctx(card, '"gоog／le.com"') == "HOST")
check("gоog／le.com, -> HOST", _ctx(card, "gоog／le.com,") == "HOST")
check("bare gоog／le.com -> HOST/HIGH", _risk(card, "gоog／le.com") == "HIGH", _risk(card, "gоog／le.com"))

# --- V1/P4: scheme counts only inside the mask's own token ---
print("\n[P4] Scheme scope is token-local")
check("http://safe.com/path then gоog／le.com -> HOST",
      _ctx(card, "http://safe.com/path then gоog／le.com") == "HOST",
      _ctx(card, "http://safe.com/path then gоog／le.com"))
check("http://safe.com then readme.md／x -> PATH",
      _ctx(card, "http://safe.com then readme.md／x") == "PATH",
      _ctx(card, "http://safe.com then readme.md／x"))
check("http://gоog／le.com -> HOST (in-scheme host)", _ctx(card, "http://gоog／le.com") == "HOST")
check("http://ok.com/a／b -> PATH (in-scheme path)", _ctx(card, "http://ok.com/a／b") == "PATH")

# --- V1/P5: right domain with a tail (path/port/query) ---
print("\n[P5] Domain on both sides with a tail -> HOST")
check("a.com／evil.com/path -> HOST", _ctx(card, "a.com／evil.com/path") == "HOST")
check("a.com／evil.com:443 -> HOST", _ctx(card, "a.com／evil.com:443") == "HOST")
check("a.com／evil.com?x=1 -> HOST", _ctx(card, "a.com／evil.com?x=1") == "HOST")

# --- V4/P2: IDN / punycode ---
print("\n[P2] IDN / punycode")
check("приме／р.рф -> HOST", _ctx(card, "приме／р.рф") == "HOST", _ctx(card, "приме／р.рф"))
check("_looks_like_domain(пример.рф) True",
      _looks_like_domain("пример.рф", _PINNED_TLDS, False) is True)

# --- D-DET-1: two+ masks in one token ---
print("\n[D-DET-1] Double mask in one token -> HOST (all masks stripped)")
out = _run(card, "gоog／le.／com")
check("gоog／le.／com yields 2 verdicts (one per mask)", len(out.relation_verdicts) == 2,
      len(out.relation_verdicts))
check("both masks -> HOST",
      all(v["detected_context"] == "HOST" for v in out.relation_verdicts),
      [v["detected_context"] for v in out.relation_verdicts])

# --- V2 concern: glued scheme without a space -> conservative HOST ---
print("\n[V2] Glued scheme (no space) is not downgraded")
check("http://safe.comgоog／le.com -> HOST",
      _ctx(card, "http://safe.comgоog／le.com") == "HOST",
      _ctx(card, "http://safe.comgоog／le.com"))

# --- False-positive guard: CJK fullwidth date is NOT a domain ---
print("\n[FP-guard] CJK fullwidth date stays FREE_TEXT")
out = _run(card, "2026／07／11")
check("2026／07／11 -> all FREE_TEXT/NONE",
      all(v["detected_context"] == "FREE_TEXT" and v["risk_level"] == "NONE"
          for v in out.relation_verdicts),
      [(v["detected_context"], v["risk_level"]) for v in out.relation_verdicts])

# --- FREE_TEXT: a lone mask is not a threat ---
print("\n[FREE_TEXT] Lone mask -> NONE, not protected")
vd = _run(card, "just ／ text").relation_verdicts
check("just ／ text -> FREE_TEXT/NONE", vd and vd[0]["detected_context"] == "FREE_TEXT"
      and vd[0]["risk_level"] == "NONE")
check("just ／ text -> protected=False", vd and vd[0]["protected"] is False)

# --- Known boundary (shown, not hidden): zero-width between labels ---
print("\n[BOUNDARY] Zero-width between labels defeats detection (documented)")
zw = "gоog​／le.com"
check("gоog<ZWSP>／le.com -> FREE_TEXT (KNOWN LIMITATION, D-DET doc)",
      _ctx(card, zw) == "FREE_TEXT", _ctx(card, zw))

# --- D-DET-2: TLD registry unavailable -> alarm, not silence; DEGRADED ---
print("\n[D-DET-2] Degraded TLD registry -> HOST + run marked DEGRADED")
_force_tld_state_for_test(frozenset(), degraded=True)
out = _run(card, "gоog／le.com")
check("degraded: gоog／le.com -> HOST (not silent FREE_TEXT)",
      out.relation_verdicts and out.relation_verdicts[0]["detected_context"] == "HOST",
      out.relation_verdicts and out.relation_verdicts[0]["detected_context"])
check("degraded: verdict carries tld_source_degraded=True",
      out.relation_verdicts and out.relation_verdicts[0]["tld_source_degraded"] is True)
check("degraded: SequenceOutput.degraded=True", out.degraded is True)
check("degraded: TLD_SOURCE_DEGRADED warning present",
      any("TLD_SOURCE_DEGRADED" in w for w in out.warnings), out.warnings)

# healthy source must NOT mark the run degraded
_force_tld_state_for_test(_PINNED_TLDS, degraded=False)
out = _run(card, "gоog／le.com")
check("healthy: run not marked degraded", out.degraded is False)

# --- FIX_FIRST blocker (2026-07-12, first conveyor round): the old
# _STRIP_OUTER block-list only trimmed punctuation someone thought to
# enumerate. Wrapping the domain in ANY character absent from that list
# (markdown asterisk, an em dash, a tilde, a pipe, a fullwidth quotation
# mark) stuck to the domain, failed the per-label isalnum-or-hyphen check,
# and silently fell to FREE_TEXT. _domain_prefix now does a POSITIVE
# extraction (letter/digit/'-'/'.') instead of a block-list, closing the
# whole class at once. ---
print("\n[FIX_FIRST] Block-list punctuation bypass is closed (positive extraction)")
for wrapped in ("*gоog／le.com*", "gоog／le.com—x", "~gоog／le.com~",
                "|gоog／le.com|", "＂gоog／le.com＂"):
    check(f"{wrapped!r} -> HOST/HIGH (was a silent FREE_TEXT bypass)",
          _ctx(card, wrapped) == "HOST" and _risk(card, wrapped) == "HIGH",
          (_ctx(card, wrapped), _risk(card, wrapped)))

# --- AUTHOR_DECISION D-DET-4 (2026-07-12, FIX_FIRST round 2): a LEADING
# structural separator is NOT a wrapper. The round-1 positive scan skipped
# everything before the first domain char, so a leading '@' (email/mention)
# or '/' (path) vanished and '@example.com／x' / '/example.com／x' mis-read
# as bare domains -> PATH/MEDIUM. D-DET-4 makes leading / \ ? # : @ a
# HARD_STOP (_domain_prefix returns ""), so these are FREE_TEXT again — the
# structural character keeps its meaning instead of being discarded as
# framing. The five wrapper bypasses above must still be HOST/HIGH (a
# wrapper is not a structural separator). ---
print("\n[D-DET-4] Leading structural separator is a HARD_STOP, not a wrapper")
for lead in ("#example.com／x", "/example.com／x", "@example.com／x", ":example.com／x"):
    check(f"{lead!r} -> FREE_TEXT (leading structural char kept, not skipped; "
          f"was PATH/MEDIUM before D-DET-4)",
          _ctx(card, lead) == "FREE_TEXT",
          _ctx(card, lead))

# --- AUTHOR_DECISION D-DET-3 (2026-07-12): concatenation false positives
# are DOCUMENTED here, not fixed. The positive-extraction fix above is
# necessarily a heuristic without a full URL parser: once masks are
# stripped, two unrelated fragments sitting either side of the mask can
# glue into something domain-shaped even when nothing is actually being
# spoofed. Recorded as known/accepted behaviour — see
# foundation_layer/AUTHOR_DECISION_20260712_BARE_DOMAIN_DETECTOR_
# FIX_FIRST_ROUND1.md. These assertions pin down the OBSERVED verdict so
# a future change to the heuristic surfaces here instead of drifting
# silently. ---
print("\n[D-DET-3, known] Concatenation false positives — documented, not fixed")
check("my-host／name.com -> HOST/HIGH (known_behavior: 'my-host'+'name.com' "
      "glues into 'my-hostname.com', a syntactically valid domain — no real "
      "attack here, just two hyphenated/dotted fragments coinciding)",
      _ctx(card, "my-host／name.com") == "HOST" and _risk(card, "my-host／name.com") == "HIGH",
      (_ctx(card, "my-host／name.com"), _risk(card, "my-host／name.com")))
check("example.com,／test -> HOST/HIGH (known_behavior: the comma stops the "
      "positive-extraction run before 'test', so the concatenated check "
      "just re-derives the left-hand domain and fires HOST rather than "
      "PATH; 'test' is silently dropped from consideration)",
      _ctx(card, "example.com,／test") == "HOST" and _risk(card, "example.com,／test") == "HIGH",
      (_ctx(card, "example.com,／test"), _risk(card, "example.com,／test")))
# D-DET-3 addendum (round 2): a mask AFTER the domain reads as HOST, not
# PATH. 'gоogle.com*／path' — the '*' ends the positive run at 'gоogle.com',
# and both the left-only check and the concat check re-derive that domain
# and fire HOST; the ／ mask actually sits in the PATH segment. Kin to the
# concatenation FPs (same rough-heuristic root), but a distinct mechanism
# (trailing wrapper, not gluing). Documented/accepted, pinned, not fixed.
check("gоogle.com*／path -> HOST/HIGH (known_behavior: mask AFTER the domain; "
      "the trailing '*' ends the run at gоogle.com so it reads HOST, not the "
      "PATH the mask position would suggest — D-DET-3 addendum)",
      _ctx(card, "gоogle.com*／path") == "HOST" and _risk(card, "gоogle.com*／path") == "HIGH",
      (_ctx(card, "gоogle.com*／path"), _risk(card, "gоogle.com*／path")))

# --- Deferred to v0.5 (known, not fixed in this round) ---
print("\n[v0.5, known] Deferred tails — not fixed in this round")
check("gоog／le.xn--zckzah -> FREE_TEXT/NONE (known_behavior: an "
      "already-punycode TLD label absent from the ACTIVE registry is a "
      "silent miss — a registry-completeness dependency, not a distinct "
      "detector bug; production risk is low since the real IANA registry "
      "carries current punycode ccTLDs, but a stale/narrow registry can "
      "still miss one)",
      _ctx(card, "gоog／le.xn--zckzah") == "FREE_TEXT",
      _ctx(card, "gоog／le.xn--zckzah"))
check("-example.com／x -> PATH/MEDIUM (known_behavior: a leading hyphen on "
      "a label is RFC 952/1035-invalid but the per-label check only tests "
      "isalnum-or-hyphen membership, not position, so '-example' still "
      "validates as a domain label)",
      _ctx(card, "-example.com／x") == "PATH",
      _ctx(card, "-example.com／x"))
# Combining-mark IDN (round 2, corrects a docstring that claimed "any
# script"): U+093E DEVANAGARI VOWEL SIGN AA is a combining mark (category
# Mc) and returns isalnum()=False, so the positive run is cut at the base
# letter and the label is dropped. FREE_TEXT. NOT a regression (the old
# block-list kept the mark but the per-label check rejected it just the
# same); a pre-existing limitation for combining marks / diacritics /
# niqqud / NFD Latin. Closing it needs IDNA/NFC canonicalisation of the
# candidate — out of this rough detector's scope. The test string is
# built from escapes so its bytes are unambiguous: bha + VOWEL SIGN AA +
# fullwidth solidus mask + ra + ta + "." + bha + VOWEL SIGN AA + ra + ta.
_DEVA_COMBINING = (
    "\u092d\u093e\uff0f\u0930\u0924\u002e\u092d\u093e\u0930\u0924"
)  # भा／रत.भारत (bharat.bharat, masked after the first syllable)
check("Devanagari label with a combining vowel sign -> FREE_TEXT "
      "(known_limitation: the vowel sign is a combining mark, "
      "isalnum()=False, so the run is cut; documents that 'isalnum()' "
      "!= 'any letter of any script')",
      _ctx(card, _DEVA_COMBINING) == "FREE_TEXT",
      _ctx(card, _DEVA_COMBINING))

_reset_tld_state_for_test()

print("\n" + "=" * 64)
print(f"TOTAL: {PASSED} OK / {FAILED} FAIL")
print("=" * 64)
sys.exit(1 if FAILED else 0)
