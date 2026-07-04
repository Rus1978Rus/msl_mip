CONVEYOR RUN RESULTS — SOLIDUS RISK_CASE_001 PATCH
Packet: RUN_002_SOLIDUS_patch_PACKET.md
Date: 2026-07-04
Target: SIGN_CORE_CARD_SOLIDUS_U002F_GEN3_v0_3_RU (PATCH_05)

This run is a good illustration of VERIFY_BEFORE_TRUST: the patch
originated from an EXTERNAL finding, which was checked against the
actual code before anything was changed.

============================================================
ORIGIN OF THE PATCH
============================================================

An external deep-research report (Alibaba Qwen) claimed a spec↔code
mismatch: the card described RISK_CASE_001 as PATH_TRAVERSAL_MIMICRY
only, but solidus_matcher.py raises RISK_CASE_001 for BOTH:
  (a) path traversal ".." (lines 151-152), and
  (b) escape sequence "\" (lines 148-149).

The SAME report also claimed an "unescaped dot in the regex". This was
FALSE — the coordinator checked solidus_matcher.py line 41 directly:
the dot IS escaped (\.). The false finding was rejected; the real one
was accepted.

============================================================
AUTHOR DECISION
============================================================

Variant B (pragmatic): the code was correct all along — both
subpatterns belong to one family ("solidus in a FILESYSTEM context as a
sign of traversal/escaping"). The card receives a retroactive
clarification WITHOUT lowering ARTIFACT_CONFIRMED, since code behavior
did not change — only the card's description of it.

PATCH_05: RISK_CASE_001 renamed PATH_TRAVERSAL_MIMICRY →
  FILESYSTEM_TRAVERSAL_OR_ESCAPE_MIMICRY; added INPUT_ALT, added
  IMPLEMENTATION_NOTE; PATCHES 4→5, VERIFIED 2/2→3/3.

============================================================
REVIEWER VERDICTS
============================================================

All five reviewers (Gemini, GPT-5.5, Kimi, Qwen, Grok) reviewed the
patched card. VERDICT: APPROVE 5/5.

============================================================
COORDINATOR VERIFICATION (VERIFY_BEFORE_TRUST)
============================================================

Verified on the live machine after patching:
  input "../../etc/passwd" → RISK_CASE_001 HIGH at both slash offsets
  + sequence SC3 → FINAL VERDICT: HOLD_PENDING_REVIEW.
  input with escaped slashes → also fires HIGH.

RESULT: APPROVE confirmed. The external finding was real and useful;
the co-reported "unescaped dot" was a false alarm caught by direct
verification. This is exactly why REVIEWER_CLAIM ≠ TRUTH until checked.
