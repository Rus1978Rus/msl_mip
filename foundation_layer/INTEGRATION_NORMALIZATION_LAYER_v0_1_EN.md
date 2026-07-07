════════════════════════════════════════════════════════════════════
CONVEYOR INTEGRATION — NORMALIZATION LAYER ARCHITECTURE
Packet: NORMALIZATION_LAYER_DESIGN_v0_1 | Date: 2026-07-07
Reviewers on the layer: 6 (+1 doc about VS16 — a DIFFERENT packet, set aside)
Type: DESIGN_ARCHITECTURE_REVIEW
Status: for AUTHOR_DECISION. THERE IS NO UNANIMITY HERE — there is a SPLIT.
════════════════════════════════════════════════════════════════════

──────────────────────────────────────────────────────────────────
0. IMPORTANT: THIS IS NOT A UNANIMOUS RUN
──────────────────────────────────────────────────────────────────
Unlike the scope runs (7/7, 6/6), reviewers here DIVERGED on the main
question (OFFSET_STRATEGY + INSERTION_POINT). This is not noise — it is
a real architectural fork with security consequences. I do not average.
I state the split as-is, then show it all reduces to ONE author decision.

──────────────────────────────────────────────────────────────────
1. WHAT IS CLOSED UNANIMOUSLY (6/6)
──────────────────────────────────────────────────────────────────
A. FLAG_ONLY — the layer flags, does NOT mutate text. Analyzer ≠
   sanitizer. Consistent with invisible-guard. 6/6.
B. CARD_CONFUSABLES = manual OVERRIDE over the auto UTS#39 base. Base
   automatic; the card refines/overrides/sets risk for a specific
   homoglyph (e.g. ／ fullwidth @ = HIGH). Do not delete (breaks 5
   cards), not hand-only (quadratic). 6/6.
C. Offsets are the foundation; direct transformation of text BEFORE
   scan_signs is FORBIDDEN (breaks text[offset]==card assert). 6/6.

──────────────────────────────────────────────────────────────────
2. THE SPLIT (main) — TWO QUESTIONS, ONE ROOT
──────────────────────────────────────────────────────────────────
Verified against code (VERIFIED): sequence strict-mode contains
  `if pos not in validated_offsets: return False`
— i.e. sequence REJECTS a candidate if any of its positions did not
pass single-sign validation.

The entire dispute grows from here. Detonator example: path obfuscation
with fullwidth slashes  http:／／  (U+FF0F instead of /).
- For sequence to catch this as path-traversal, the ／ positions MUST
  reach validated_offsets.
- But ／ is not a card sign, scan_signs skips it → no positions in
  validated_offsets → strict-sequence REJECTS the attack.

Reviewers split on what to do:

CAMP 1 — "INSIDE scan_signs, homoglyph → into validated_offsets"
  (1 reviewer, Gemini-class). Extend the condition:
  `if ch in cards OR NFKC(ch) in cards OR skeleton(ch) in cards`.
  Then ／ is added to validated_offsets like a sign, and sequence CATCHES
  http:／／. PRO: full protection from structural homoglyph attacks.
  CON: erases the "exact match" vs "fuzzy match" boundary — a false
  confusable could inject a false validated position.

CAMP 2 — "AFTER scan_signs, a SEPARATE confusable_flags structure, NOT
  in validated_offsets" (majority, ~4 reviewers). The layer builds a
  separate flag list without touching validated_offsets.
  PRO: validated_offsets strictness preserved, clean architecture.
  CON (critical, not named by all): sequence will NOT catch http:／／,
  because the ／ positions are not in validated_offsets. Protection is
  PARTIAL: single-sign flags "homoglyph of / here," but sequence MISSES
  the structural attack made of homoglyphs.

CAMP 3 — "exclude collapsing entirely, declare a LIMITATION" (1
  reviewer, Gemini-class from digits). Multi-codepoint cases (ﬁ→fi,
  ½→1⁄2) are not mapped; honestly record in limitations that
  NFKC-expansion is not covered — for the sake of offset integrity.

──────────────────────────────────────────────────────────────────
3. ROOT OF THE SPLIT = ONE AUTHOR DECISION
──────────────────────────────────────────────────────────────────
The whole dispute (camps 1/2/3, mapping vs per-symbol, insertion point)
REDUCES to one question that 4 of 6 reviewers independently put to the
author in ONE_QUESTION_TO_AUTHOR:

  ★ MUST the sequence layer CATCH structural attacks made of homoglyphs
    (http:／／ fullwidth, ../ via look-alikes), OR is it enough for
    single-sign to FLAG individual homoglyph positions? ★

  IF YES (sequence must catch):
    → homoglyph positions must reach validated_offsets
    → camp 1 (inside scan_signs) OR a mapping table translating
      normalized offsets to originals
    → harder, but full protection
  IF NO (flagging the position is enough):
    → camp 2 (separate structure), simpler, cleaner
    → but sequence misses structural homoglyph attacks

This is NOT a technical detail for reviewers. It is a PRODUCT decision
about depth of protection — and it is yours.

──────────────────────────────────────────────────────────────────
4. OFFSET STRATEGY (consequence of the Sec.3 question)
──────────────────────────────────────────────────────────────────
Approach tally:
- Pure (b) per-symbol: 1 reviewer (contested, see below).
- Hybrid b + mapping ONLY for collapse: 3 reviewers.
- Mapping-primary (a): 1 reviewer.
- b + exclude collapse (limitation): 1 reviewer.

DISPUTE OVER MY PA2 (I claimed: per-symbol misses ﬁ→fi):
- 5 reviewers: PA2 CORRECT — per-symbol misses multi-codepoint.
- 1 reviewer (Kimi-class): PA2 WRONG — per-symbol catches them too, if
  you flag the source symbol ﬁ with metadata "expands to fi," without
  changing length.
  ANALYSIS: this reviewer is RIGHT for the "flag the position" case, but
  WRONG for the "sequence must search the expanded pattern" case. So the
  PA2 dispute is THE SAME Sec.3 question in miniature: is sequence
  matching over the normalized form needed.

CONCLUSION: the offset strategy is NOT chosen separately — it falls out
of the Sec.3 answer. Resolve Sec.3 and the strategy is determined:
  "sequence catches" → hybrid b+mapping (translate norm→orig offsets);
  "flag is enough"   → pure b, no mapping.

──────────────────────────────────────────────────────────────────
5. CRITIQUE OF MY PA5 (insertion point) — DIVERGED
──────────────────────────────────────────────────────────────────
I proposed "after scan_signs, before sequence." All criticized it, but
in DIFFERENT directions — which itself proves it is unresolved:
- "before scan_signs" (pre-scan): 1.
- "inside scan_signs" (else homoglyph won't reach validated): 1-2.
- "after, but confusable_flags SEPARATE, not in validated": 3.
All three are consequences of the Sec.3 question. There is no single
"right place" until Sec.3 is resolved.

──────────────────────────────────────────────────────────────────
6. MISSED_CONSIDERATIONS (converged independently, valuable)
──────────────────────────────────────────────────────────────────
M1. Bidi vs NFKC: RLO/LRO (U+202E/202D) are NOT normalized by NFKC but
    change visual order. Bidi is a SEPARATE analysis, not via NFKC.
M2. casefold/NFKC order: UTS#39 prescribes NFKC(CaseFold(x)). Fix the
    order explicitly, else Cyrillic/Latin are inconsistent.
M3. Performance: per-symbol NFKC+skeleton on large texts is expensive.
    Need an ASCII fast-path (ord<128 → skip) + codepoint cache (lru_cache).
M4. NFC vs NFKC: NFKC is more aggressive (①→1, ½→1⁄2). Security needs
    NFKC, but document the choice.
M5. VS16 survives NFKC (from the set-aside VS16 packet, R7, VERIFIED):
    normalization does NOT remove U+FE0F. THEREFORE invisible-guard and
    normalization are DIFFERENT layers, not replacing each other.
    Invisibles caught by DI-guard, homoglyphs by norm-layer. Confirms
    these are two layers, not one.

──────────────────────────────────────────────────────────────────
7. WHAT REQUIRES AUTHOR_DECISION
──────────────────────────────────────────────────────────────────
MAIN (Sec.3): must sequence catch structural homoglyph attacks
  (http:／／), or is a single-sign position flag enough?
  → this answer determines both the offset strategy AND insertion point.

After it, almost automatically:
D-a. Offset strategy (falls out of Sec.3).
D-b. Insertion point (falls out of Sec.3).
D-c. FLAG_ONLY — accept (6/6).
D-d. confusables = override over auto — accept (6/6).
D-e. Fix M1-M4 as mandatory implementation points (bidi separate,
     NFKC(CaseFold) order, ASCII fast-path+cache, explicit NFKC choice).
D-f. Does a confusable flag affect card RISK, or is it purely
     informational? (one reviewer's ONE_QUESTION — secondary).

──────────────────────────────────────────────────────────────────
8. CLAUDE'S RECOMMENDATION (OPINION, not a decision)
──────────────────────────────────────────────────────────────────
On Sec.3 — my honest advice, with the cost stated:

  "sequence MUST catch" (camp 1 / hybrid with mapping).
  Reason: MSL/MIP's main threat is exactly STRUCTURAL attacks on
  separators (. / @). A homoglyph slash http:／／ is precisely the class
  the project exists for. A layer that flags a lone ／ but misses the
  ASSEMBLY of homoglyphs in sequence leaves the main door open.
  Flag-without-sequence is half protection in the most important place.
  Cost, honestly: harder (mapping norm→orig offsets OR careful addition
  to validated_offsets tagged source="confusable, not exact"), higher
  risk of a bug in the foundation. This is NOT an evening's task.

  BUT — by anti-overclaim an honest narrow start is possible:
  begin with CAMP 2 (flag-only, separate structure) as v0.1, DECLARING
  in LIMITATION that sequence detection of homoglyph attacks is NOT yet
  covered — and add it via a separate conveyor later. Not an omission
  but a named boundary. Then the Sec.3 decision becomes "flag first,
  sequence coverage — next stage."

Both paths are honest. The choice is depth of protection now vs speed
and cleanliness now. This is your product call, not an architecture detail.

──────────────────────────────────────────────────────────────────
9. LINK TO THE ECOSYSTEM
──────────────────────────────────────────────────────────────────
M5 (VS16 survives NFKC) closes an earlier question: invisibles and
homoglyphs are TWO different layers. This confirms the scope decisions:
invisibles (DI-guard) and normalization (homoglyphs) do not merge, they
run in parallel. Non-ASCII Nd digits (٠١ ０１) are served by THIS
norm-layer — as decided in the digits run (D8).

NOTE (post-run, 2026-07-07): the author later added a disciplinary
decision (ARCH_DECISION_HOMOGLYPH_VIA_CARD_ONLY) resolving the Sec.3
split via a THIRD path absent from reviewers: a homoglyph enters
sequence ONLY through its own verified card (not on-the-fly in code),
preserving both discipline and sequence's ability to read combinations.
See that document.
════════════════════════════════════════════════════════════════════
