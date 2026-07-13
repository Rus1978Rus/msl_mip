#!/usr/bin/env python3
"""
msl_mip_runtime.py — the MSL/MIP working program.

Takes text (as a CLI argument or interactively) and runs it
through the whole pipeline:

  1. scans the text, finds positions of signs that have a loaded
     SIGN_CORE_CARD (currently: DOT, SOLIDUS, SKULL)
  2. per sign — module_engine.process_sign (the single-sign layer)
  3. per result — integrator_engine.process_output
     (the single-sign decision)
  4. sequence_engine.process_sequence over the whole text with the
     full known_signs registry (CARD_SET_COMPLETENESS — see review)
  5. sequence_integrator_engine.process_sequence_output (the
     decision on found sequences)
  6. final verdict = the strictest action across all levels

RUN:
    python3 msl_mip_runtime.py "text to analyse"
    python3 msl_mip_runtime.py        (no argument — prompts for text)
"""

from __future__ import annotations

import sys
import os
import unicodedata

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "core"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "single_sign"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "sequence"))

from load_card import load_card
from module_engine import process_sign
from integrator_engine import process_output
from sequence_engine import process_sequence
from sequence_integrator_engine import process_sequence_output
from matchers import dot_matcher


# Action strictness order — shared by single-sign and sequence decisions
_SEVERITY = {
    "pass": 0,
    "log_only": 1,
    "queue_for_review": 2,
    "hold_pending_review": 3,
    "escalate_to_human": 4,
}

CARDS_DIR_CANDIDATES = [
    os.path.join(os.path.dirname(__file__), "cards"),
    "/mnt/user-data/uploads",
]

# Real card file names (ARTIFACT_CONFIRMED) as they sit in the
# project. A missing file just means the card does not load; the
# runtime keeps going with what it has (an explicit warning).
CARD_FILENAMES = [
    "SIGN_CORE_CARD_DOT_U002E_GEN3_v0_3_RU__2_.md",
    "SIGN_CORE_CARD_SOLIDUS_U002F_GEN3_v0_3_RU__1_.md",
    "SIGN_CORE_CARD_SKULL_U1F480_GEN3_v0_3_RU__1_.md",
    "SIGN_CORE_CARD_SKULL_CROSSBONES_U2620_GEN3_v0_3_RU.md",
    "SIGN_CORE_CARD_AT_U0040_GEN3_v0_3_RU.md",
    # Mask card (relation axis): no matcher — relations only.
    "SIGN_CORE_CARD_FULLWIDTH_SOLIDUS_UFF0F_GEN3_v0_3_RU.md",
]


def _find_card_file(filename: str) -> str:
    for d in CARDS_DIR_CANDIDATES:
        path = os.path.join(d, filename)
        if os.path.exists(path):
            return path
    return None


def load_all_cards() -> list:
    """Loads all available cards. Prints a warning when one is
    missing, but does not crash."""
    cards = []
    for fname in CARD_FILENAMES:
        path = _find_card_file(fname)
        if path is None:
            print(f"[WARNING] Card not found: {fname} — sign will not be recognized")
            continue
        try:
            cards.append(load_card(path))
        except Exception as e:
            print(f"[WARNING] Failed to load {fname}: {e}")
    return cards


def scan_signs(text: str, cards: list) -> list:
    """STAGE: finds all text positions of signs that have a loaded
    card, and runs each through module_engine."""
    sign_chars = {c.visible_form: c for c in cards}
    statuses = []
    for i, ch in enumerate(text):
        if ch in sign_chars:
            try:
                statuses.append(process_sign(sign_chars[ch], text, i))
            except Exception as e:
                print(f"[WARNING] Error processing sign {ch!r} at position {i}: {e}")
    return statuses


def most_severe(actions: list) -> str:
    if not actions:
        return "pass"
    return max(actions, key=lambda a: _SEVERITY.get(a, 0))


# Relation (mask) verdict -> action map (relation axis, D-REL-4).
# NONE->pass, LOW->log_only, MEDIUM->queue, HIGH/CRITICAL->hold.
# Module-level (was inline in analyze) so the safeguard chaos gate can
# monkey-patch the mapping to simulate a severed aggregation path.
_REL_ACTION = {"NONE": "pass", "LOW": "log_only",
               "MEDIUM": "queue_for_review",
               "HIGH": "hold_pending_review",
               "CRITICAL": "hold_pending_review"}


def _relation_actions(seq_out) -> list:
    """Derive runtime actions from the sequence layer's relation (mask)
    verdicts. Extracted as a module-level seam so tests/gate_safeguard.py
    can monkey-patch it to simulate a severed mask path WITHOUT touching
    seq_out.relation_verdicts — the source of truth the invariant reads."""
    actions = []
    for v in seq_out.relation_verdicts:
        act = _REL_ACTION.get(v["risk_level"])
        if act is None:
            # Unknown enum value must be visible, not silently mapped.
            print(f"[WARNING] UNKNOWN_RISK_LEVEL in relation verdict: "
                  f"{v['risk_level']!r} — falling back to queue_for_review")
            act = "queue_for_review"
        actions.append(act)
    return actions


class IntegrityViolation(Exception):
    """Raised by the finish-line safeguard in STRICT mode when the
    conservation-of-severity invariant is broken: the main-path verdict is
    weaker than a relation (mask) verdict requires. In production the run is
    NOT stopped — the SEMANTIC verdict (the main path's decision) is left
    unchanged, and a separate EFFECTIVE verdict is raised to the safe minimum
    (D-GUARD-4); strict mode (gates) raises so a regression fails in dev."""


# D-GUARD-3: minimum acceptable action per relation risk level. The invariant
# is conservation of SEVERITY, not a literal "not PASS": a HIGH verdict that
# ends up log_only or queue_for_review is under-escalated just as much as one
# that ends up pass. NONE/LOW carry no minimum.
_REL_MIN_ACTION = {
    "MEDIUM": "queue_for_review",
    "HIGH": "hold_pending_review",
    "CRITICAL": "hold_pending_review",
}


def _integrity_check(semantic_action: str, seq_out, cards: list):
    """D-GUARD-1/2/3 — an INDEPENDENT check of the RESULT, run after
    aggregation and before return. Reads ONLY the main-path verdict
    (semantic_action), the sequence layer's relation_verdicts (source of
    truth for the mask axis), and the loaded cards' edge validation_warnings.
    It does NOT re-walk the aggregation path, so it does not duplicate that
    path's fragility.

    D-GUARD-1/3 (conservation of severity): each relation verdict imposes a
    MINIMUM final action (MEDIUM->queue, HIGH/CRITICAL->hold). If the
    main-path verdict is WEAKER than that minimum, the mask risk was
    under-escalated -> VIOLATION (each violation records the required_action
    so analyze() can raise the EFFECTIVE verdict). This catches HIGH->pass
    AND HIGH->log_only AND HIGH->queue, not only literal PASS.

    Form-robustness (D-GUARD-3): risk_level is normalised (str, strip, upper)
    so "high"/" HIGH "/enum all compare equal; an UNKNOWN risk_level is a
    CONCERN, never a silent skip.

    D-GUARD-2 revives validation_warnings (written by the parser, read
    NOWHERE — dead code that manufactured a false sense of safety): an ACTIVE
    edge that carried a load-time validation_warning AND whose verdict
    contributed nothing (risk NONE) is flagged as a CONCERN — the
    misconfigured edge is silently inert, exactly as its own warning
    predicted.

    Returns (violations, concerns) — lists of detail dicts."""
    sem_sev = _SEVERITY.get(semantic_action, 0)
    violations = []
    concerns = []

    # D-GUARD-1/3 — conservation of severity, form-robust
    for v in seq_out.relation_verdicts:
        rl = str(v.get("risk_level", "")).strip().upper()
        if rl in ("NONE", "LOW"):
            continue
        required = _REL_MIN_ACTION.get(rl)
        if required is None:
            concerns.append({
                "rule": "D-GUARD-3-UNKNOWN",
                "relation_id": v.get("relation_id", ""),
                "relation_risk": v.get("risk_level"),
                "detail": (f"relation verdict has an UNKNOWN risk_level "
                           f"{v.get('risk_level')!r} -> cannot check severity; "
                           f"flagged rather than silently skipped"),
            })
            continue
        if sem_sev < _SEVERITY[required]:
            violations.append({
                "rule": "D-GUARD-1",
                "relation_id": v.get("relation_id", ""),
                "visible_form": v.get("visible_form", ""),
                "at_offset": v.get("at_offset"),
                "detected_context": v.get("detected_context"),
                "relation_risk": rl,
                "semantic_action": semantic_action,
                "required_action": required,
                "detail": (f"relation verdict {rl} at offset {v.get('at_offset')} "
                           f"(context={v.get('detected_context')}) requires at least "
                           f"{required}, but the main-path verdict is "
                           f"{semantic_action} -> mask risk under-escalated"),
            })

    # D-GUARD-2 — revive validation_warnings
    warn_by_edge = {}
    for c in cards:
        for r in getattr(c, "relations", []):
            if getattr(r, "is_active", False) and getattr(r, "validation_warnings", None):
                warn_by_edge[(c.visible_form, r.relation_id)] = list(r.validation_warnings)
    for v in seq_out.relation_verdicts:
        w = warn_by_edge.get((v.get("visible_form"), v.get("relation_id")))
        if w and str(v.get("risk_level", "")).strip().upper() == "NONE":
            concerns.append({
                "rule": "D-GUARD-2",
                "relation_id": v.get("relation_id", ""),
                "visible_form": v.get("visible_form", ""),
                "validation_warnings": w,
                "relation_risk": "NONE",
                "detail": ("active edge carried a load-time validation_warning and "
                           "produced no verdict (risk NONE) -> misconfigured edge "
                           "silently inert"),
            })
    return violations, concerns


# --- INVISIBLE_UNCARDED_REGISTRAR (D-INV witness channel) ------------------
# A LIGHT witness, not a judge. The pipeline above only processes signs that
# have a loaded card (scan_signs keys on card.visible_form) — so an invisible
# character with NO card is simply never seen: it passes in total silence. That
# silence is the danger, not the character. The registrar closes that gap by
# NOTICING such a character and SURFACING it as a fact — nothing more.
#
# It obeys the whole project stance (this is an ALERT system, not an antivirus;
# the machine is a witness, never judge or executioner):
#   - it does NOT decide risk (records never enter semantic/effective_action);
#   - it does NOT delete or "clean" (Default_Ignorable != safe-to-delete);
#   - it does NOT touch carded signs (ZWSP has a card now -> excluded here);
#   - its finding is TRIVALENT and honest: not "dangerous", not "safe", but
#     UNVERIFIABLE — "there is no card, I cannot verify this; here are the
#     facts, hold it and look by eye". The last word stays with the human.
#
# Trigger = an invisible/format code point with no card: General_Category=Cf,
# OR a Bidi_Control, OR a Default_Ignorable_Code_Point. Python's stdlib carries
# no Default_Ignorable property table, so that arm is an HONEST APPROXIMATION —
# a curated set of the well-known ranges (declared as such, not sold as full
# coverage). Ordinary whitespace (space/newline/tab -> Zs/Cc, not Cf) is NOT
# flagged; this channel is only for the truly invisible.

_BIDI_CONTROL_CLASSES = {
    "LRE", "RLE", "LRO", "RLO", "PDF", "LRI", "RLI", "FSI", "PDI",
}

# Curated approximation of Default_Ignorable_Code_Point ranges that are NOT
# already General_Category=Cf (those are caught by the Cf arm). Honest scope:
# the well-known stable ones (soft-hidden joiners, fillers, variation
# selectors). Declared as an approximation on purpose — see D-INV note above.
_DEFAULT_IGNORABLE_EXTRA_RANGES = (
    (0x034F, 0x034F),      # COMBINING GRAPHEME JOINER (Mn)
    (0x115F, 0x1160),      # HANGUL CHOSEONG/JUNGSEONG FILLER (Lo)
    (0x17B4, 0x17B5),      # KHMER VOWEL INHERENT AQ/AA (Mn)
    (0x180B, 0x180F),      # MONGOLIAN FREE/VOWEL SEPARATORS (Mn/Cf)
    (0x3164, 0x3164),      # HANGUL FILLER (Lo)
    (0xFE00, 0xFE0F),      # VARIATION SELECTOR-1..16 (Mn)
    (0xFFA0, 0xFFA0),      # HALFWIDTH HANGUL FILLER (Lo)
    (0xFFF0, 0xFFF8),      # unassigned, Default_Ignorable (Cn)
    (0xE0100, 0xE01EF),    # VARIATION SELECTOR-17..256 (Mn)
)


def _invisible_reason(ch: str) -> str:
    """Why this code point counts as an uncarded-invisible trigger, or ''
    if it does not. Cf first (the broadest, most reliable arm), then bidi
    control, then the curated Default_Ignorable approximation."""
    if unicodedata.category(ch) == "Cf":
        return "FORMAT_CHAR"          # General_Category=Cf
    if unicodedata.bidirectional(ch) in _BIDI_CONTROL_CLASSES:
        return "BIDI_CONTROL"
    cp = ord(ch)
    for lo, hi in _DEFAULT_IGNORABLE_EXTRA_RANGES:
        if lo <= cp <= hi:
            return "DEFAULT_IGNORABLE"
    return ""


def scan_uncarded_invisibles(text: str, cards: list) -> list:
    """Witness pass: report every invisible/format code point that has NO
    loaded card. Returns a list of ACK_GAP witness records (never verdicts).
    Carded code points are excluded — the registrar is for the UNKNOWN only."""
    carded = {ord(c.visible_form) for c in cards if len(c.visible_form) == 1}
    records = []
    for i, ch in enumerate(text):
        if ord(ch) in carded:
            continue                  # a card exists — the normal path handles it
        reason = _invisible_reason(ch)
        if not reason:
            continue
        try:
            name = unicodedata.name(ch)
        except ValueError:
            name = "UNNAMED / UNASSIGNED CODE POINT"
        records.append({
            "codepoint": f"U+{ord(ch):04X}",
            "at_offset": i,
            "unicode_name": name,
            "category": unicodedata.category(ch),
            "trigger": reason,
            # witness fields — deliberately NOT a risk_level:
            "card_status": "NOT_CREATED",
            "finding_status": "UNVERIFIABLE",   # ACK_GAP_TRIVALENT: not safe, not dangerous
            "finding_basis": (
                f"invisible code point ({reason}) with no card -> intent "
                f"cannot be verified by the system"),
            "recommendation": (
                "hold and look by eye; not judged safe and not judged "
                "dangerous; Default_Ignorable != safe-to-delete"),
        })
    return records


def analyze(text: str, cards: list) -> dict:
    """Full text run through all layers. Returns a report structure
    for printing (and possible programmatic use)."""
    known_signs = {c.visible_form for c in cards}

    # --- Single-sign layer ---
    sign_statuses = scan_signs(text, cards)
    single_sign_results = []
    single_actions = []
    for st in sign_statuses:
        decision = process_output(st)
        single_sign_results.append((st, decision))
        single_actions.append(decision.runtime_action)

    # --- Sequence layer ---
    seq_out = process_sequence(text, cards, sign_statuses=sign_statuses,
                               known_signs=known_signs)
    seq_decision = process_sequence_output(seq_out)

    # --- Relation (mask) verdicts -> actions (relation axis, D-REL-4) ---
    relation_actions = _relation_actions(seq_out)

    # --- SEMANTIC verdict (the main path's decision — the author's) ---
    semantic_action = most_severe(single_actions + [seq_decision.runtime_action]
                                  + relation_actions)

    # --- FINISH-LINE SAFEGUARD (D-GUARD-1..4) ---
    # Independent conservation-of-severity check AFTER aggregation, reading
    # only the RESULT (semantic_action + relation_verdicts + edge warnings).
    # It does not re-walk the path, so it does not duplicate the path's
    # fragility. THREE fields are reported (D-GUARD-4) so the integrity signal
    # cannot itself be lost the way a single mislabelled field could:
    #   semantic_action  — what the main path decided (unchanged; author's).
    #   integrity_status — OK / VIOLATION / CONCERN.
    #   effective_action — on VIOLATION, raised to the safe minimum; else the
    #                      semantic_action. print_report shows BOTH so the
    #                      human sees "system said X, integrity broken -> Y".
    # Strict mode (gates) RAISES on a violation so a regression fails in dev.
    integrity_violations, integrity_concerns = _integrity_check(
        semantic_action, seq_out, cards)
    if integrity_violations:
        integrity_status = "VIOLATION"
        effective_action = most_severe(
            [semantic_action] + [v["required_action"] for v in integrity_violations])
        if os.environ.get("MSL_MIP_GUARD_STRICT") == "1":
            raise IntegrityViolation(
                "; ".join(v["detail"] for v in integrity_violations))
    elif integrity_concerns:
        integrity_status = "CONCERN"
        effective_action = semantic_action
    else:
        integrity_status = "OK"
        effective_action = semantic_action

    # --- INVISIBLE_UNCARDED_REGISTRAR (witness channel, D-INV) ---
    # Run LAST and kept in its OWN field. It is deliberately NOT folded into
    # single_actions / relation_actions / semantic_action: an UNVERIFIABLE
    # witness record must never masquerade as a risk verdict. The human reads
    # it alongside the verdict, not inside it.
    uncarded_invisibles = scan_uncarded_invisibles(text, cards)

    return {
        "text": text,
        "sign_statuses": sign_statuses,
        "single_sign_results": single_sign_results,
        "sequence_output": seq_out,
        "sequence_decision": seq_decision,
        "semantic_action": semantic_action,
        "effective_action": effective_action,
        "integrity_status": integrity_status,
        "integrity_violations": integrity_violations,
        "integrity_concerns": integrity_concerns,
        "uncarded_invisibles": uncarded_invisibles,
    }


def print_report(report: dict) -> None:
    text = report["text"]
    print("=" * 60)
    print(f"TEXT: {text!r}")
    print("=" * 60)

    print("\n--- SINGLE SIGNS ---")
    if not report["single_sign_results"]:
        print("  (no signs from loaded cards found)")
    for st, decision in report["single_sign_results"]:
        print(f"  [{st.sign_offset_start}] {st.sign_codepoint} "
              f"interp={st.interpretation} risk={st.risk_level.value} "
              f"-> action={decision.runtime_action}")
        if st.risk_cases_triggered:
            print(f"        cases={st.risk_cases_triggered}")
        for w in st.output_warnings:
            print(f"        [!] {w}")

    print("\n--- SEQUENCES ---")
    seq_out = report["sequence_output"]
    if not seq_out.matches:
        print("  (no sequences found)")
    for m in seq_out.matches:
        rl = m.risk_level.value if hasattr(m.risk_level, "value") else m.risk_level
        print(f"  [{m.match_start}:{m.match_end}] {m.sc_id} {m.sequence!r} "
              f"risk={rl} card={m.candidate_source_card}")
    seq_dec = report["sequence_decision"]
    print(f"  -> action={seq_dec.runtime_action} ({seq_dec.action_rationale})")
    for w in seq_out.warnings:
        print(f"  [!] {w}")

    if seq_out.relation_verdicts:
        print("\n--- RELATION (MASK) VERDICTS ---")
        for v in seq_out.relation_verdicts:
            # relation_type/runtime_role make the "one PRIMARY verdict, the
            # rest supporting facets" story legible — otherwise three lines at
            # the same offset look like three independent verdicts.
            rtype = v.get("relation_type", "")
            role = v.get("runtime_role", "")
            tag = f"[{rtype}/{role}] " if rtype or role else ""
            print(f"  [{v['at_offset']}] {v['visible_form']} {tag}-> {v['target']} "
                  f"context={v['detected_context']} risk={v['risk_level']} "
                  f"protected={v['protected']}")

    invis = report.get("uncarded_invisibles", [])
    if invis:
        # A WITNESS block, printed on its own — never inside the verdict.
        print("\n--- UNCARDED INVISIBLE SIGNS (WITNESS, not a verdict) ---")
        for r in invis:
            print(f"  [{r['at_offset']}] {r['codepoint']} ({r['unicode_name']}) "
                  f"[{r['category']}/{r['trigger']}]")
            print(f"        card: {r['card_status']}   finding: {r['finding_status']}")
            print(f"        basis: {r['finding_basis']}")
            print(f"        -> to the human: {r['recommendation']}")

    print("\n" + "=" * 60)
    sem = report["semantic_action"]
    eff = report["effective_action"]
    status = report.get("integrity_status", "OK")
    if status == "OK":
        print(f"FINAL VERDICT: {sem.upper()}")
    else:
        # D-GUARD-4: show BOTH so the human sees the discrepancy in the window.
        print(f"SEMANTIC VERDICT (main path): {sem.upper()}")
        print(f"INTEGRITY: {status}")
        for viol in report.get("integrity_violations", []):
            print(f"  [INTEGRITY_VIOLATION] {viol['detail']}")
        for con in report.get("integrity_concerns", []):
            print(f"  [{con['rule']}] {con['detail']}")
        print(f"EFFECTIVE VERDICT (integrity-adjusted): {eff.upper()}")
    print("=" * 60)


def main():
    cards = load_all_cards()
    if not cards:
        print("[ERROR] No cards loaded — analysis impossible.")
        sys.exit(1)
    print(f"Cards loaded: {len(cards)} ({', '.join(c.codepoint for c in cards)})")

    suffix_source = dot_matcher.get_compound_suffix_source()
    if suffix_source == "LIVE_FETCH":
        print("Compound suffix list (PSL): up to date (just fetched)")
    elif suffix_source.startswith("CACHE_FROM_"):
        cached_at = suffix_source.replace("CACHE_FROM_", "")
        print(f"[!] Compound suffix list (PSL): could not update, "
              f"using cached copy from {cached_at}")
    elif suffix_source == "EMBEDDED_HERMETIC":
        print("[!] Compound suffix list (PSL): HERMETIC mode "
              "(MSL_MIP_HERMETIC_TLD set) — network and cache deliberately "
              "skipped, using the pinned built-in list (for gates, not prod)")
    else:
        print("[!] Compound suffix list (PSL): no network and no cached copy — "
              "using built-in minimal list (may not know "
              "about rare compound zones)")

    # FIXED (MAJOR, found by GPT-5.5, 2026-06-29): the single-TLD
    # source (IANA registry) used not to be surfaced at all
    tld_source = dot_matcher.get_single_tld_source()
    if tld_source == "LIVE_FETCH":
        print("Single TLD list (IANA): up to date (just fetched)")
    elif tld_source.startswith("CACHE_FROM_"):
        cached_at = tld_source.replace("CACHE_FROM_", "")
        print(f"[!] Single TLD list (IANA): could not update, "
              f"using cached copy from {cached_at}")
    elif tld_source == "EMBEDDED_HERMETIC":
        print("[!] Single TLD list (IANA): HERMETIC mode "
              "(MSL_MIP_HERMETIC_TLD set) — network and cache deliberately "
              "skipped, using the pinned built-in list (for gates, not prod)")
    else:
        print("[!] Single TLD list (IANA): no network and no cached copy — "
              "using built-in minimal list (may not know "
              "about rare TLDs)")
    print()

    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
        report = analyze(text, cards)
        print_report(report)
    else:
        print("Enter text to analyze (Ctrl+C to exit):")
        while True:
            try:
                text = input("> ")
            except (EOFError, KeyboardInterrupt):
                print("\nExiting.")
                break
            if not text.strip():
                continue
            report = analyze(text, cards)
            print_report(report)
            print()


if __name__ == "__main__":
    main()
