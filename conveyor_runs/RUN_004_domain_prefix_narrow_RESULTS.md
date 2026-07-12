CONVEYOR RUN RESULTS — NARROW CIRCLE: _domain_prefix REWRITE
Packet: CONVEYOR_PACKET_NARROW_DOMAIN_PREFIX_2026-07-12.txt (project root)
Date: 2026-07-12
Target: sequence/sequence_engine.py :: _domain_prefix (bare-domain detector G1)
Type: NARROW_CIRCLE_REVIEW (single function; N1 new misses / N2 new FPs /
      N3 IDN not broken)
Prior rounds: RUN implicit — FIX_FIRST_ROUND1 (block-list -> positive
      extraction) produced this function; this round reviews only it.

============================================================
WHAT WAS REVIEWED
============================================================

One function, rewritten in the previous round from a punctuation
block-list (_STRIP_OUTER) to a positive character allow-list (first
maximal run of isalnum()-or-'.'-or-'-'). Three narrow questions: does
the positive scan lose anything the block-list caught (N1), glue too
much (N2), or break IDN (N3).

============================================================
REVIEWER VERDICTS (as submitted)
============================================================

Six review artifacts were returned. Two are SET ASIDE as invalid (basis
below); the remaining live voices decided the round. NOTE ON COUNT: the
author's instruction described this two ways ("two invalid, five live"
and "five live + one filtered"); the artifacts as pasted do not resolve
to a single clean tally — recorded honestly here rather than forced into
a round number. What is firm and decision-relevant: at least one live
voice found the real blocker, and the two clearly-invalid patterns are
identified with basis.

LIVE (counted):
  - Gemini / MASTER-AUDITOR — VERDICT: READY_TO_SAVE. N1/N2/N3 PASS.
    ONE_QUESTION: "largest valid run" vs "first run" (junk_prefix_...).
  - Narrow-circle voice ("ACCEPT_WITH_ONE_NARROW_PATCH") — found the
    BLOCKER: leading structural separator skipped as if a wrapper
    (#/@ /: before the domain -> PATH instead of FREE_TEXT). Proposed the
    exact HARD_STOP patch adopted as D-DET-4. THIS IS THE DECISIVE VOICE.
  - Kimi K2.6 — VERDICT: READY. FLAGGED: asserted a Devanagari IDN case
    (उदाहरण.भारत -> HOST) WITHOUT verifying — took the bare base letter,
    not the real combining-mark form; the vowel sign U+093E halts the
    scan. Guess passed off as verification (this is why the
    FINDING_BASIS rule was raised to section 0 — see below).
  - DeepSeek-R1 — VERDICT: READY. N1/N2/N3 PASS with code-cited reasoning.
  - Qwen — VERDICT: READY_TO_SAVE. Found the mask-AFTER-domain FP
    (gоogle.com*／path -> HOST, expected PATH); recommended document-not-fix.
  - "IDN Punycode Handling" voice — PASS with MINOR FIXES (edge-hyphen,
    zero-width). Both already tracked (v0.5 tail / ARCH boundary).
  - ASCII-trace voice — VERDICT: READY_FOR_MERGE.

SET ASIDE (not counted):
  - Dead-code reviewer — "FIX_VERIFICATION V1–V6 ... READY_TO_SAVE",
    discussing "P1–P7", "V5 P6 CURRENT_MASK_ONLY", degraded-source.
    FINDING_STATUS: REJECTED.
    FINDING_BASIS: METHOD=grep/read of the artifact; TARGET=
      sequence/sequence_engine.py; OBSERVED=no "P1"–"P7" and no
      "CURRENT_MASK_ONLY" identifiers exist in the reviewed code — these
      are artifacts of a dead prior session, not this narrow packet. The
      voice reviewed content that is not in the packet.
  - "Could not read the packet / offered to compose a report" voice —
    author-reported.
    FINDING_STATUS: UNVERIFIABLE (from the pasted material alone).
    FINDING_BASIS: the author stated a second voice failed to read the
      packet and proposed fabricating a report; that specific block is
      not positively locatable in the pasted text, so its identity is
      taken on the author's statement, not independently verified here.
      Either way it carries no BASIS and is not admissible.

============================================================
AUTHOR DECISIONS (this round)
============================================================

D-DET-4 (ACCEPTED): a leading structural separator (/ \\ ? # : @) is a
  HARD_STOP in _domain_prefix (returns ""), not a skippable wrapper.
  Closes the blocker. See foundation_layer/AUTHOR_DECISION_20260712_
  BARE_DOMAIN_DETECTOR_FIX_FIRST_ROUND2.md.

Wording correction (ACCEPTED, docs only): "letter of ANY script" was
  false — the truth is "characters for which str.isalnum() is True";
  combining marks (Mn/Mc) fail it. Corrected in the _domain_prefix
  docstring, the detector header comment, the card LIMITATION_STATEMENT,
  and ROUND2. Added a gate case (Devanagari + vowel sign -> FREE_TEXT,
  built from escapes for byte-exactness). NOT a regression.

D-DET-3 addendum (ACCEPTED, document-not-fix): mask AFTER the domain
  (gоogle.com*／path -> HOST, expected PATH). Pinned in the gate.

============================================================
REJECTED / DEFERRED FINDINGS (with reason)
============================================================

- Edge-hyphen label ban: already deferred to v0.5 in ROUND1; gate pins
  it. Not reopened.
- Zero-width normalisation: out of scope and would violate ARCH_DECISION_
  HOMOGLYPH_VIA_CARD_ONLY (zero-width is not a carded mask). Boundary
  already documented. REJECTED this round.
- "Largest valid run" instead of "first run" (junk_prefix_gоog／le.com):
  measured — the OLD block-list also returned FREE_TEXT on such input, so
  it is not a new regression. Candidate for v0.5. DEFERRED.
- IDNA logging / normalise-all-labels: robustness improvements, not
  correctness of this narrow change. DEFERRED.

============================================================
COORDINATOR VERIFICATION (VERIFY_BEFORE_TRUST)
============================================================

Measured on the live machine (py -3), TLD set pinned offline, verdicts
read from process_sign + process_sequence, NOT reasoned:
  #example.com／x, /example.com／x, @example.com／x, :example.com／x
      -> FREE_TEXT (were PATH/MEDIUM before D-DET-4)
  *gоog／le.com*, gоog／le.com—x, ~gоog／le.com~, |gоog／le.com|,
  ＂gоog／le.com＂  -> HOST/HIGH (five wrapper bypasses intact)
  Devanagari+vowel-sign (escape-built _DEVA_COMBINING) -> FREE_TEXT
  gоogle.com*／path -> HOST (D-DET-3 addendum)
  gоog／le.com, приме／р.рф -> HOST/HIGH (base cases unaffected)

Gates after the change: gate_bare_domain_detector 40/40 (was 34),
gate_relation_verdict_step4 12/12, gate_solidus_scheme 28/28,
gate_english_only CLEAN. Zero regressions.

Note on the Kimi guess: the coordinator specifically re-measured the
Devanagari case that Kimi asserted without checking, and it returns
FREE_TEXT (the scan halts at U+093E). Kimi's "HOST ✅" was wrong. This is
the concrete case that promoted PER_FINDING_STATUS_AND_BASIS_MANDATORY
into section 0 of the conveyor packet template.

============================================================
OUTCOME
============================================================

RESULT: FIX_FIRST — blocker (D-DET-4) accepted and applied; wording
corrected; two known FPs/limitations pinned; four findings deferred.
Detector code remains NEW_ARTIFACT, NOT_REVIEWED — heading to the next
round. This RUN is the provenance for the card's RUN_CARD_REFERENCE.
