# SILENT-PATH AUDIT — MSL/MIP full code tract — 2026-07-12

**Status of this document: MAP FOR EXTERNAL CONVEYOR, not a verdict.**
This is not a "clean" sign-off. It is a deliberately paranoid list of places
where a protection can go quiet on some input. Author-produced (I wrote most
of this code, so my blind spots are real), cross-checked by four independent
adversarial audit agents, one per layer, and the load-bearing findings were
re-reproduced by me directly (VERIFY_BEFORE_TRUST applies to my own subagents
too). Final call on severity/reachability is for the external reviewers, not
for me. Nothing was fixed; no commit made.

**Provenance tag** on each finding: `(repro: self)` = I ran it this session;
`(repro: agent)` = an audit agent reproduced it and I accepted the trace but
did not personally re-run; `(read-only)` = established by reading code, not
executed.

**One reassurance that survived the audit, stated plainly so it is not
mistaken for more:** in the SHIPPED entry point `msl_mip_runtime.analyze()`,
all three verdict streams (single-sign, sequence, relation/mask) are folded
into `most_severe(...)`. Agent-4 verified end-to-end that a mask HOST
substitution reaches `HOLD_PENDING_REVIEW`. So there is currently no verdict
that is computed and then dropped **in aggregation**. Every silent pass below
is either (a) a verdict never computed because a sign/edge is quietly removed
or mis-scoped upstream, (b) a fallback that defaults toward pass, or (c) a
seam that is safe ONLY because the runtime re-plumbs it by hand — one
regression away from a silent phishing PASS.

---

## GROUP 1 — LAYER SEAMS / VERDICT FLOW (highest value)

### S1 — Sequence integrator ignores relation_verdicts entirely
- **MESTO:** `sequence/sequence_integrator_engine.py:103-109` (`if not seq_out.matches: return pass`) and `:95-101` (`check_unavailable → pass`); root cause `sequence/sequence_output.py:91` (`aggregate_risk` iterates `self.matches` only)
- **TYPE:** 5 LAYER SEAM
- **INPUT:** any mask-only phishing string, e.g. `gоog／le.com` — produces `relation_verdicts=[HOST/HIGH]`, `matches=[]`
- **STATUS:** VERIFIED (repro: self + agent) — `process_sequence_output(out).runtime_action == 'pass'` while a HOST/HIGH mask verdict rides in the same struct.
- **WHY:** The component whose entire job is "turn sequence output into a decision" never references `relation_verdicts` or `degraded`. The end-to-end runtime is safe ONLY because `msl_mip_runtime.analyze()` re-derives relation actions in a separate loop. That redundancy is the single point of failure for the whole homoglyph axis; this is the exact precedent the author cited ("relation_verdicts once didn't reach final verdict → phishing PASS").

### S2 — EMPTY_CANDIDATE_POOL exits check_unavailable=True while carrying a live HIGH verdict
- **MESTO:** `sequence/sequence_engine.py` EMPTY_CANDIDATE_POOL early return (the `if not pool:` branch) + integrator `:95-101`
- **TYPE:** 1 EARLY RETURN + 5 SEAM
- **INPUT:** a card set whose cards declare no SEQUENCE_CANDIDATES — e.g. the fullwidth-solidus **mask card alone** + `gоog／le.com`
- **STATUS:** VERIFIED (repro: agent)
- **WHY:** `process_sequence` returns `check_unavailable=True` AND `relation_verdicts=[HIGH]`; the integrator's `check_unavailable` short-circuit returns "pass", dropping the HIGH. `check_unavailable=True` reads downstream as "safe" even with a live threat verdict attached. Latent in prod (DOT/SOLIDUS keep the pool non-empty) but real for any mask-only card set.

### S3 — `degraded` flag is inert: never influences a decision, never printed with the verdict
- **MESTO:** `sequence/sequence_output.py:74` (field); not read in `process_sequence_output`; absent from `msl_mip_runtime.print_report` (prints only `seq_out.warnings`); not in `analyze()` `most_severe`
- **TYPE:** 4 DEGRADED + 5 SEAM
- **INPUT:** any run with TLD registry unavailable
- **STATUS:** VERIFIED (repro: agent, read-only for print_report)
- **WHY:** `SequenceOutput.degraded` is pure metadata. The D-DET-2 "fail-closed by behaviour" is only true because `_is_tld` raises risk in degraded mode (see D2 for where that itself leaks); the flag as a signal does nothing and an operator reading the FINAL VERDICT cannot tell the run was degraded.

### S4 — `SequenceOutput.as_dict()` omits relation_verdicts
- **MESTO:** `sequence/sequence_output.py:100-113`
- **TYPE:** 5 SEAM
- **INPUT:** any serialization-based consumer of the sequence output
- **STATUS:** VERIFIED (read-only)
- **WHY:** Mask verdicts are not in the serialized form; any downstream that consumes the JSON/dict (not the live object) loses every homoglyph verdict silently.

### S5 — Edge `validation_warnings` are stored but consumed NOWHERE
- **MESTO:** generated `core/load_card.py:129-148`; field `core/sign_core_card.py:107`; NOT copied into the candidate dict `single_sign/module_engine.py:154-168`; not surfaced in `output_warnings`; grep confirms no reader
- **TYPE:** 2 SWALLOWED SIGNAL + 5 SEAM
- **INPUT:** any misconfigured edge (empty scope, unknown scope, bad type)
- **STATUS:** VERIFIED (repro: self grep + agent)
- **WHY:** The loader literally writes a warning that says an edge "silently yields no verdict" — and then nothing ever reads that warning. The one signal that a mask edge is dead is itself dead.

---

## GROUP 2 — CONTEXT_SCOPE (rules/code mismatch → dead protection)

### SC1 — 5 of the 10 spec scope values are unreachable → edges scoped to them are silently NONE
- **MESTO:** `sequence/sequence_engine.py` `_detect_context_at` (only ever returns HOST/URL/PATH/FREE_TEXT) + `_SCOPE_RISK` (maps only those 4) + the `protected` computation in `_assess_relation_risk`; spec lists 10 values at `foundation_layer/STEP0_SIGN_RELATIONS_STRUCTURE_v0_2_RU` and `templates/...CONVEYOR...` / loader `_VALID_SCOPE` `core/load_card.py:114-115`
- **TYPE:** 6 RULES/CODE MISMATCH + 3 DEFAULT NONE
- **INPUT:** a mask card edge with `CONTEXT_SCOPE: PORT` + `http://ok.com:8080／x` (the detector itself calls this mask HOST). Also EMAIL, IDN, CODE, IDENTIFIER.
- **STATUS:** VERIFIED (repro: self + agent) — `scope=PORT` → `('HOST','NONE',protected=False)`; `scope=HOST` on the identical input → `('HOST','HIGH',True)`.
- **WHY:** The loader accepts PORT/EMAIL/IDN/CODE/IDENTIFIER as valid scopes **with no warning** (PORT produced zero load warnings), but the detector can never emit those contexts, so every such edge is `protected=False → risk=NONE`. Declared protection that is inert by construction. An author following the spec exactly gets zero detection and zero signal.

### SC2 — Typo'd scope loads (warning stored-but-unsurfaced) → silently NONE
- **MESTO:** `core/load_card.py:132-134` (warns, does not block) + S5 (warning never read)
- **TYPE:** 6 RULES/CODE MISMATCH + 3 DEFAULT
- **INPUT:** `CONTEXT_SCOPE: HSOT` (typo of HOST) + `gоog／le.com`
- **STATUS:** VERIFIED (repro: self) — loads with `UNKNOWN_CONTEXT_SCOPE: ['HSOT']` warning, then `('HOST','NONE',False)` (should have been HOST/HIGH).
- **WHY:** One-character scope typo silently disables the edge; the only trace is a warning nothing reads.

---

## GROUP 3 — DEGRADED / TLD PATHS (several are holes in the recently-shipped D-DET-2)

### D1 — Embedded fallback (163 entries) sits ABOVE the fail-closed threshold (100) → offline masked phishing passes with no alarm
- **MESTO:** `sequence/sequence_engine.py` `_TLD_MIN_HEALTHY = 100` health check vs `core/public_suffix.py:127-152` `EMBEDDED_TLD_FALLBACK` (163 entries)
- **TYPE:** 4 DEGRADED/FALLBACK
- **INPUT:** offline/hermetic deploy (live+cache fail → embedded) + masked domain on a real TLD absent from the ~163-entry embedded list, e.g. `gоog／le.gay`, `pаypa／l.moscow`
- **STATUS:** VERIFIED (repro: self + agent) — `.gay/.moscow ∉ embedded`; both → `FREE_TEXT/NONE`, `run.degraded=False`, no warning.
- **WHY:** **This is a hole in my own D-DET-2.** The alarm is designed to fire when the registry is unavailable, but the embedded fallback — the very list that is known-incomplete (~163 of ~1450 real TLDs) — is classified "healthy" because 163 ≥ 100. The one fallback that most needs the alarm never trips it. Offline, a whole class of masked phishing passes silently.

### D2 — Degraded fail-closed's `isalpha()` gate rejects punycode/IDN TLDs → the homoglyph surface bypasses the alarm
- **MESTO:** `sequence/sequence_engine.py` `_is_tld` degraded branch `return label.isalpha() and 2 <= len(label) <= 63`
- **TYPE:** 4 DEGRADED/FALLBACK (fed by the idna swallow, D3)
- **INPUT:** DEGRADED run + `при／мер.xn--p1ai` (A-label of `.рф`)
- **STATUS:** VERIFIED (repro: self + agent) — `_is_tld('xn--p1ai', empty, degraded=True)` → False; `при／мер.xn--p1ai` → `FREE_TEXT/NONE` even with `degraded=True`.
- **WHY:** **Second hole in my own D-DET-2.** "Alarm, not silence" only accepts purely-alphabetic TLDs, so IDN/punycode TLDs (`xn--…`) — exactly the international homoglyph attack surface — slip through even in alarm mode.

### D3 — `_is_tld` idna `except Exception: pass` swallows already-punycode labels
- **MESTO:** `sequence/sequence_engine.py` `_is_tld` (`try: label.encode("idna") … except Exception: pass`)
- **TYPE:** 2 SWALLOWED ERROR
- **INPUT:** non-degraded run, registry stores unicode ccTLDs, input carries A-label `xn--p1ai` not verbatim in the set
- **STATUS:** VERIFIED (repro: agent) — `'xn--p1ai'.encode('idna')` raises UnicodeError (double ACE prefix), swallowed → non-degraded returns False → FREE_TEXT/NONE.
- **WHY:** An encoding failure is converted into a quiet "not a TLD → safe."

### D4 — dot_matcher domain-mimicry (RISK_CASE_002) is gated entirely behind `is_domain_like` → thin/empty TLD set fails open
- **MESTO:** `single_sign/matchers/dot_matcher.py:228` (`is_domain_like = last_segment in single_tlds`) gating `:255-267`
- **TYPE:** 4 DEGRADED/FALLBACK
- **INPUT:** `paypal.com.verify.shop` (or `.tokyo`) with an empty/thin `_single_tlds_cache`
- **STATUS:** VERIFIED (repro: self earlier + agent) — empty TLD set → every dot `interp=file_extension`, `risk=[]`; with the TLD present → RISK_CASE_002 on every dot.
- **WHY:** The imitation check runs only inside the `if is_domain_like:` branch; when the IANA list degrades, phishing chains fall through to a safe file-extension reading with no risk. (This is the same class as the gate-hermeticity flip proven earlier for `paypal.com.security-check.ru`.)

### D5 — public_suffix accepts ANY non-empty parse as LIVE_FETCH (no min-size sanity) and overwrites good cache with poison
- **MESTO:** `core/public_suffix.py:292-295` and `:216-222` (`if entries: _save_to_cache`); parsers `:155-172` / `:217-238`; `errors="replace"` at the decode sites; cache trusted on one header line `:183-215` / `:249-284`
- **TYPE:** 6 RULES/CODE MISMATCH + 4 DEGRADED + 2 SWALLOWED
- **INPUT:** the fetch returns an HTML error / captive-portal / truncated body
- **STATUS:** VERIFIED-parse (repro: agent); full network path SUSPECTED
- **WHY:** The only gate is truthiness. An HTML `503` page parses to junk "entries", is treated as `LIVE_FETCH`, and is written to cache, destroying the last-good list. There is NO `len < 100` (or any) sanity floor inside `public_suffix.py`; the only such check lives downstream in `sequence_engine` and guards single-TLDs only, and (per D1) even that floor is below the incomplete embedded size. Poison persists across restarts.

---

## GROUP 4 — CARD LOADER / PARSER (untrusted input → sign silently dropped or downgraded)

### L1 — TAB-indented card silently blanks entire sections
- **MESTO:** `core/tree_parser.py` indent computed by `lstrip(" ")` (spaces only)
- **TYPE:** 5 SEAM + 4 DEGRADED
- **INPUT:** any card indented with tabs instead of spaces
- **STATUS:** VERIFIED (repro: self + agent) — same SAFE_CASES block: spaces → 1 child, **tabs → 0 children**.
- **WHY:** Tab-indented children get indent 0, attach to root, and `section.child(...)` returns nothing. SAFE_CASES / RISK_CASES / SIGN_RELATIONS / SEQUENCE_LAYER_BOUNDARY all come back empty on a whitespace mistake — the mask/relation axis and every case vanish with no error.

### L2 — `_parse_risk` returns a raw STRING on any non-enum RISK (type confusion → silent not-HIGH)
- **MESTO:** `core/load_card.py:40-43`
- **TYPE:** 3 DEFAULT VALUES + 5 SEAM
- **INPUT:** `RISK: high` / `critical` / `HIGHH` / `None`
- **STATUS:** VERIFIED (repro: self) — `_parse_risk('high') → 'high'` (not a RiskLevel); `RiskLevel.HIGH == _parse_risk('high')` is **False**.
- **WHY:** Downstream `risk == RiskLevel.HIGH` is silently False and `RiskLevel.max()` raises `ValueError` on the string; a lowercase/typo'd HIGH case reads as not-high.

### L3 — Missing/empty RISK defaults to `RiskLevel.NONE`
- **MESTO:** `core/load_card.py:38-39` + default arg `"NONE"` at the extractor call sites
- **TYPE:** 3 DEFAULT VALUES
- **INPUT:** a RISK_CASE/CONFUSABLE with no RISK field (or one dropped by L1/L4)
- **STATUS:** VERIFIED (repro: self) — `_parse_risk('') → RiskLevel.NONE`.
- **WHY:** A known-bad case that omits or mis-indents its RISK silently becomes zero-risk.

### L4 — Mixed/lower-case field KEY is dropped and pollutes the previous value
- **MESTO:** `core/tree_parser.py` `_KEY_LINE_RE` requires `[A-Z]`
- **TYPE:** 5 SEAM (feeds L3)
- **INPUT:** `Risk: HIGH` (any non-UPPERCASE field name)
- **STATUS:** VERIFIED (repro: agent) — `child('RISK') → None`, the `Risk: HIGH` text appends to the previous node's value.
- **WHY:** A field authored with wrong casing disappears; the safe NONE default applies → HIGH becomes NONE.

### L5 — Composite RISK takes the first token (`MEDIUM / HIGH` → MEDIUM)
- **MESTO:** `core/load_card.py:40`
- **TYPE:** 3 DEFAULT VALUES (downgrade)
- **INPUT:** `RISK: MEDIUM / HIGH`
- **STATUS:** VERIFIED (repro: self) — → `RiskLevel.MEDIUM`.
- **WHY:** Designed for `LOW / CONTEXT_DEPENDENT`, but an escalating composite silently keeps the lower token.

### L6 — Prefix-matched RELATION keys drop mis-keyed edges / can absorb phantoms
- **MESTO:** `core/load_card.py:118` (`children_with_prefix("RELATION_")`)
- **TYPE:** 5 SEAM
- **INPUT:** an edge keyed `REL_1` (dropped → 0 relations); conversely a `RELATION_001_JUSTIFICATION` node nested under SIGN_RELATIONS would be picked up as a phantom empty edge (the real card has such a node, saved only by its indentation)
- **STATUS:** VERIFIED-drop (repro: agent); collision SUSPECTED
- **WHY:** The runtime source-of-truth relation set is string-prefix matched — one naming slip loses (or fabricates) a homoglyph relation.

### L7 — `IS_ACTIVE` disable set is narrow; intent-to-disable words parse as ACTIVE, and one word can silence a mask
- **MESTO:** `core/load_card.py:125` (`not in ("FALSE","NO","0","OFF")`); consumed `single_sign/module_engine.py:170-174`
- **TYPE:** 6 RULES/CODE MISMATCH
- **INPUT:** `IS_ACTIVE: disabled` / `inactive` / `n` / `FALSE (experiment)` → **active=True**; conversely `IS_ACTIVE: FALSE` on all edges → mask silently off with only an `ALL_RELATIONS_INACTIVE` soft warning
- **STATUS:** VERIFIED (repro: agent)
- **WHY:** Author-intent vs parser mismatch both ways: an edge believed disabled stays live, and a legitimately disabled mask turns off homoglyph protection with no verdict-level signal.

### L8 — `document_status` is stored but the LOADER gates nothing
- **MESTO:** `core/load_card.py:244`
- **TYPE:** 6 RULES/CODE MISMATCH
- **INPUT:** `DOCUMENT_STATUS: DEPRECATED` / `REVOKED` / anything
- **STATUS:** VERIFIED (repro: agent, read-only)
- **WHY:** The loader loads a revoked/unknown-status card identically to ARTIFACT_CONFIRMED. (module_engine does re-check: WORKING_DRAFT warns, an out-of-set status raises → the sign is then dropped by the runtime's swallow, L9/R2 — i.e. an unknown status becomes a silent skip, not a block.)

### L9 — `load_card` raises on malformed header; the runtime swallows it → the sign becomes undetectable
- **MESTO:** core raise: `core/load_card.py:225,240,241,244` (`.text()` on possibly-None) + `_parse_zone` KeyError `:46-52`; runtime swallow: `msl_mip_runtime.py:86-90`
- **TYPE:** 2 SWALLOWED ERROR (at the runtime seam) + 5 SEAM
- **INPUT:** a card missing ZONE/CODEPOINT/VISIBLE_FORM/DOCUMENT_STATUS, or `ZONE: ZONE_9`, or even `ZONE: ZONE_1 (stable)` (trailing comment breaks the exact dict lookup)
- **STATUS:** VERIFIED (repro: agent, both halves)
- **WHY:** `load_card` fails loud (good) but returns no "UNKNOWN/ERROR" card; `load_all_cards` catches, warns, and continues with fewer cards. That sign's character is then absent from `sign_chars`, so it is never scanned and produces no verdict — a whole sign class silently undetectable on a load hiccup, and `main()` proceeds unless ZERO cards load.

### L10 — CONFUSABLES are documentation-only; split source of truth invites a silent gap
- **MESTO:** `core/load_card.py:106-110` (docstring) + `:89-103` (parsed only into a doc list, not into relations)
- **TYPE:** 3 DEFAULT + 5 SEAM
- **INPUT:** a mask whose confusable is written only in CONFUSABLES and not mirrored into SIGN_RELATIONS
- **STATUS:** SUSPECTED (by-design, but a real silence)
- **WHY:** If an author documents a confusable but forgets the parallel SIGN_RELATIONS edge, the runtime sees no relation and the mask is invisible.

---

## GROUP 5 — MODULE ENGINE / MATCHERS

### M1 — Mask branch keys ONLY on `if card.relations:` → free risk=NONE for any relations-bearing card without a matcher
- **MESTO:** `single_sign/module_engine.py:146` (branch) and `:196` (loud MATCHER_NOT_FOUND it bypasses); conditional matcher registration `:32-56`
- **TYPE:** 1 EARLY RETURN
- **INPUT:** a card with a codepoint NOT in `_MATCHER_REGISTRY` and any non-empty `relations` list (reproduced with a bogus `A` (U+0041) card carrying one relation → risk=NONE, `relation_candidate`)
- **STATUS:** VERIFIED-mechanism (repro: agent); prod reachability SUSPECTED
- **WHY:** Any sign whose card gains a relations block but whose matcher is missing/renamed silently downgrades from the loud `MATCHER_NOT_FOUND` to a silent risk=NONE. `@` (U+0040) and `☠` (U+2620) are registered conditionally — if such a matcher file goes missing and that card ever gains a relations block, protection flips from loud error to silent pass.

### M2 — Single-sign layer gives every mask risk=NONE by design; the single-sign integrator never reads relation evidence
- **MESTO:** `single_sign/module_engine.py:146-195` + `single_sign/integrator_engine.py:60-101`
- **TYPE:** 5 SEAM (design)
- **INPUT:** any mask, e.g. `／` in `http:／evil.ru`
- **STATUS:** VERIFIED (repro: agent) — `process_sign → NONE`; `process_output → pass`.
- **WHY:** The whole confusable protection lives outside the single-sign layer. Correct by design, but any single-sign-only consumer treats every homoglyph as pass; combined with S1, the protection has exactly one real home (the runtime's relation loop).

### M3 — A FIRED risk case whose card RISK is a non-enum string yields risk_level NONE
- **MESTO:** `single_sign/module_engine.py:99-105` (`_risk_level_for_ids`, `is_enum_value` filter)
- **TYPE:** 3 DEFAULT VALUE
- **INPUT:** `risk_ids=["RISK_CASE_002"]` where the card's `RiskCase.risk = "intensity-dependent"` (or any string, e.g. via L2)
- **STATUS:** VERIFIED-mechanism (repro: agent); latent today
- **WHY:** The id is reported in `risk_cases_triggered` but the numeric risk is filtered to NONE → action pass. A fired detection that produces "pass". Currently latent (real DOT/SOLIDUS/SKULL matcher-fired cases carry enum risks) but one card edit (L2/L5) away.

### M4 — Matcher fall-through returns `"unknown"` / no risk → downstream NONE = pass
- **MESTO:** `dot_matcher.py:125,188`; `solidus_matcher.py:107`; `at_matcher.py:74`
- **TYPE:** 3 DEFAULT VALUE
- **INPUT:** any shape a matcher fails to classify (e.g. a dot whose neighbours aren't both alnum)
- **STATUS:** SUSPECTED (repro: agent)
- **WHY:** "Unrecognized shape" and "safe" are conflated — an unclassified shape is treated as safe by default rather than flagged.

### M5 — skull_crossbones (☠) threat detection is SENTENCE-scoped → cross-sentence evasion
- **MESTO:** `single_sign/matchers/skull_crossbones_matcher.py:120` (`_sentence_around`) + `:85-101`
- **TYPE:** 5 SEAM (scope narrowing)
- **INPUT:** `я тебя убью ☠` → RISK_CASE_001 fires; `я тебя убью. смотри сюда ☠` → `risk=[]`
- **STATUS:** VERIFIED (repro: agent)
- **WHY:** A patch restricted threat/instruction/authority triggers to the sign's sentence; splitting the threat and the ☠ into adjacent sentences drops risk to nothing. The sibling `skull_matcher.py` scans the whole text — the two ZONE_3 matchers are INCONSISTENT.

### M6 — 💀 with a death keyword but no threat phrase → no safe case AND no risk (NONE)
- **MESTO:** `single_sign/matchers/skull_matcher.py:98-120` + default EPOCH_3 at `:84`
- **TYPE:** 3 DEFAULT VALUE
- **INPUT:** bare death/danger keyword + 💀, no threat/cancel phrase, no Halloween/medical context
- **STATUS:** SUSPECTED (repro: agent; partly by-design)
- **WHY:** The dominant-epoch default plus the "no approximate label" rule mean a literal-death reading contributes zero risk unless an explicit threat phrase is present.

### M7 — Documented-but-unimplemented RISK_CASES (self-admitted rules/code mismatch)
- **MESTO:** `dot_matcher.py:4-17` (RC001/003/004/005); `solidus_matcher.py:8-14` (RC005/006/007); `skull_matcher.py:13-28` (RC001/005; RC003/006/008 metadata-only)
- **TYPE:** 6 RULES/CODE MISMATCH
- **INPUT:** the attack classes those RISK_CASES name (FAKE_OFFICIAL_NOTATION, STATUS_CHAIN/ROLE_BINDING mimicry, etc.)
- **STATUS:** VERIFIED-by-docstring (read-only)
- **WHY:** The cards advertise these detections; the code returns no risk for them. Honestly disclosed and arguably correct (semantic not structural), but each is a permanent quiet pass for that attack class — and a card/code mismatch a reviewer should see.

### M8 — Scheme neutralization `//`→NONE for ANY alpha-leading pseudo-scheme
- **MESTO:** `sequence/sequence_engine.py:149-157` via `_valid_scheme_before`
- **TYPE:** 3 DEFAULT VALUE
- **INPUT:** `javascript://…`, `data://…`, `evil://…` — all "start with a letter" so `//` is neutralized to `RiskLevel.NONE`
- **STATUS:** SUSPECTED (repro: agent)
- **WHY:** The scheme discriminator lowers the SOLIDUS `//` risk to NONE based on scheme *validity* (RFC shape), not scheme *safety*. `javascript:`/`data:` are RFC-valid schemes; the `//` risk for them is unconditionally neutralized. (The url_context_flag only raises scrutiny; the risk-to-NONE is unconditional.)

---

## GROUP 6 — RUNTIME ENTRY POINT

### R1 — `scan_signs` swallows matcher exceptions → the crashed sign contributes NOTHING → HOLD flips to PASS
- **MESTO:** `msl_mip_runtime.py:98-104` (try/except in `scan_signs`)
- **TYPE:** 2 SWALLOWED ERROR
- **INPUT:** any sign whose matcher/engine raises (reproduced by injecting a crash on the U+FF0F mask in `paypal.com／evil.com`)
- **STATUS:** VERIFIED (repro: agent)
- **WHY:** The except prints a `[WARNING]` and continues; the crashed sign never enters `sign_statuses`, so it contributes no single action, no validated offset, AND no relation verdict. Repro flipped FINAL from `hold_pending_review` to **PASS**. A malicious input that trips ANY matcher bug turns that sign's protection off with only a stderr line.

### R2 — `load_all_cards` swallows load failures → an entire sign class becomes invisible
- **MESTO:** `msl_mip_runtime.py:86-90` (try/except) + `:84` (missing-file continue)
- **TYPE:** 2 SWALLOWED ERROR
- **INPUT:** mask card missing/unparseable (reproduced by dropping the fullwidth-solidus card; same input `paypal.com／evil.com`)
- **STATUS:** VERIFIED (repro: agent) — WITH card → hold; WITHOUT → **PASS**, `relation_verdicts: []`.
- **WHY:** A failed `load_card` is caught, warned, skipped; the sign's char is absent from `sign_chars`, never scanned, no verdict. `main()` proceeds unless zero cards load. (This is the runtime half of L9.)

### R3 — Hardcoded `CARD_FILENAMES` list → a card that exists but isn't listed is invisible
- **MESTO:** `msl_mip_runtime.py` `CARD_FILENAMES` (hardcoded)
- **TYPE:** 6 RULES/CODE MISMATCH
- **INPUT:** any sign whose card file is present in `cards/` but not in the list
- **STATUS:** SUSPECTED (read-only)
- **WHY:** Detection coverage is a hand-maintained list, not derived from the card set; a new/renamed card silently does nothing until edited into the list.

### R4 — Unknown action string / unmapped risk defaults to `pass` severity everywhere
- **MESTO:** `msl_mip_runtime.py:110` (`_SEVERITY.get(a, 0)`); `single_sign/integrator_engine.py:74`; `sequence/sequence_integrator_engine.py:81,114`
- **TYPE:** 3 DEFAULT VALUES + 6 vocab mismatch
- **INPUT:** any action string outside `_SEVERITY`, any RiskLevel outside the action maps
- **STATUS:** SUSPECTED (latent — not triggerable today)
- **WHY:** Every lookup treats an unrecognized action as severity 0 (=pass) and an unmapped risk as "pass". No test guards vocab alignment; add one action/risk anywhere and a real verdict silently becomes pass.

### R5 — `_REL_ACTION` maps CRITICAL weaker than the sequence integrator does
- **MESTO:** `msl_mip_runtime.py:135-138` (CRITICAL→`hold_pending_review`) vs `sequence/sequence_integrator_engine.py:33` (CRITICAL→`escalate_to_human`)
- **TYPE:** 3 DEFAULT VALUES (inconsistent ladder)
- **INPUT:** a relation verdict of CRITICAL
- **STATUS:** SUSPECTED (not reachable today — `_SCOPE_RISK` caps relation risk at HIGH)
- **WHY:** If a future scope yields CRITICAL, the relation stream under-escalates relative to the sequence stream.

### R7 — `paypal.com@evil.ru` (scheme-less userinfo) → PASS
- **MESTO:** `single_sign/matchers/at_matcher.py:120-134`
- **TYPE:** 6 RULES/CODE MISMATCH (documented gap)
- **INPUT:** `paypal.com@evil.ru`
- **STATUS:** VERIFIED (repro: agent)
- **WHY:** The `@` matcher treats scheme-less userinfo as a legitimate email per WHATWG; documented, but a phishing-shaped input that passes. Worth a reviewer's eyes as a policy call.

---

## SUMMARY TABLE

### By pattern type (primary classification; many findings span two)
| Type | Findings | Count |
|------|----------|-------|
| 1 EARLY RETURN | S2, M1 | 2 |
| 2 SWALLOWED ERRORS | S5, D3, D5, L9, R1, R2 | 6 |
| 3 DEFAULT VALUES | L2, L3, L5, M3, M4, M6, M8, R4, R5 | 9 |
| 4 DEGRADED / FALLBACK | S3, D1, D2, D4, L1 | 5 |
| 5 LAYER SEAMS | S1, S4, L4, L6, M2, M5 | 6 |
| 6 RULES/CODE MISMATCH | SC1, SC2, L7, L8, L10, M7, R3, R7 | 8 |
| **Total unique findings** | | **36** |

### By verification status (36 unique findings, each counted once under its dominant status)
| Status | Count | Findings |
|--------|-------|----------|
| VERIFIED | 28 | S1, S2, S3, S4, S5, SC1, SC2, D1, D2, D3, D4, L1, L2, L3, L4, L5, L6, L7, L8, L9, M1, M2, M3, M5, M7, R1, R2, R7 |
| SUSPECTED | 8 | D5, L10, M4, M6, M8, R3, R4, R5 |
| UNVERIFIABLE | 0 | — |

*(Some findings are VERIFIED for the core mechanism but carry a SUSPECTED sub-part, counted once under the dominant status: L6 VERIFIED for the mis-key drop, SUSPECTED for the phantom-collision variant; D5 VERIFIED that the parser accepts junk with no sanity floor, SUSPECTED for the full live-server→cache-poison delivery; M1/M3 VERIFIED-mechanism but latent — no current card reaches them.)*

### Highest-priority for the external conveyor (author's own ranking, to be overridden by reviewers)
1. **S1 + S2 + S5** — the relation/mask verdict reaches the final verdict through exactly one hand-wired path in the runtime; the sequence integrator, the empty-pool exit, and the serialized form all drop it, and the one signal that an edge is dead is never read. One regression = silent phishing PASS.
2. **SC1** — 5 of 10 spec scopes are dead protection by construction, with no load warning (PORT case). A spec-compliant card gets zero detection.
3. **D1 + D2** — two holes in the just-shipped D-DET-2: the incomplete embedded TLD list is deemed "healthy" (163 ≥ 100) so offline masked phishing passes with no alarm, and the fail-closed alarm rejects the punycode/IDN TLDs that ARE the homoglyph surface.
4. **R1 + R2 + L9** — a swallowed matcher exception or a swallowed card-load failure flips a phishing host-substitution from HOLD to PASS with only a stderr line.
5. **L1 + L2/L3/L4/L5** — parser/loader fragility: tabs blank whole sections, and a casing/typo/composite RISK silently downgrades a HIGH case to NONE.

---

## METHOD NOTE (honesty / provenance)
- Auditors: the code author (blind-spot-prone, disclosed) + 4 independent adversarial agents, one per layer (core, single_sign, sequence+integrators, runtime+seams).
- The author personally reproduced: S1, SC1, SC2, D1, D2, L1, L2, L3, L5 (plus the earlier gate-hermeticity flip that seeded D4). The rest carry an audit-agent reproduction, accepted after reading the trace; re-run any before acting.
- This is a discovery map, intentionally over-inclusive. "Flagged" ≠ "confirmed exploitable in production". Several VERIFIED-mechanism findings are latent (no current card reaches them). The external reviewers decide severity, reachability, and fix order.
- Nothing here was fixed. No commit made.
