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
import sequence_engine as _se   # F-NEW-3: reuse domain/context helpers for the removal probe
from sequence_integrator_engine import process_sequence_output
from o1_policy_engine import pending_for as _o1_pending_for  # P3: report-only disposition
from o1_policy_engine import O1Context as _O1Context         # C6: caller-supplied targets
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
    # First invisible-class card (ZWSP, WORKINGLY_CLOSED, battery 21/21).
    # Was harness-only (sim_bycode_v2 loaded it by explicit path); attached to
    # the default loadout 2026-07-17 so the shipped analyze() path actually
    # carries the invisible-sign protection the card verifies.
    "SIGN_CORE_CARD_ZERO_WIDTH_SPACE_U200B_GEN3_v0_3_RU.md",
    # Second invisible-class card (ZWJ, WORKING_DRAFT, probe-verified 2026-07-17).
    # Gives the class behavioural spread: ZWSP breaks, ZWJ joins (Join_Control).
    # Legit emoji sequences read as FREE_TEXT (no FP); Arabic/Persian joining is
    # an honest MAY_QUEUE boundary (mirrors the ZWSP<->CJK precedent).
    "SIGN_CORE_CARD_ZERO_WIDTH_JOINER_U200D_GEN3_v0_1_RU.md",
    # Third invisible-class card (BOM, WORKING_DRAFT, probe-verified 2026-07-18).
    # Third profile: a service/stream marker whose legitimacy is POSITIONAL (first
    # char of a file), not functional. First carrier of the three-level signal
    # principle on the existing pass/queue/hold outputs (leading BOM -> queue =
    # "possible danger", not freed to pass, not escalated to hold).
    "SIGN_CORE_CARD_BYTE_ORDER_MARK_UFEFF_GEN3_v0_1_RU.md",
]


def _find_card_file(filename: str) -> str:
    for d in CARDS_DIR_CANDIDATES:
        path = os.path.join(d, filename)
        if os.path.exists(path):
            return path
    return None


def load_cards_report() -> dict:
    """Load all cards AND return a STRUCTURED load report, so a programmatic caller can
    tell that a detector was dropped instead of only seeing a stdout warning.

    Returns {cards, load_warnings, expected, loaded, degraded}:
      - cards        -- the SignCoreCards that loaded (same list as load_all_cards()).
      - load_warnings-- one entry per missing/failed card: {card, status, error}
                        (status = MISSING | FAILED).
      - expected/loaded/degraded -- counts + a bool flag; degraded=True means at least
        one card did not load, so the corresponding sign will not be recognized.

    A missing DETECTOR is a silent-pass risk (a threat becomes invisible to that
    subsystem), so this must be visible in a structured form, not only on stdout.
    load_all_cards() stays the simple list-returning entry point (CLI/back-compat)."""
    cards = []
    warnings = []
    for fname in CARD_FILENAMES:
        path = _find_card_file(fname)
        if path is None:
            warnings.append({"card": fname, "status": "MISSING", "error": "file not found"})
            continue
        try:
            cards.append(load_card(path))
        except Exception as e:
            warnings.append({"card": fname, "status": "FAILED", "error": str(e)})
    return {
        "cards": cards,
        "load_warnings": warnings,
        "expected": len(CARD_FILENAMES),
        "loaded": len(cards),
        "degraded": bool(warnings),
    }


def load_all_cards() -> list:
    """Loads all available cards. Prints a warning when one is missing/failed, but does
    not crash. Backward-compatible list-returning entry point; for a structured load
    status (programmatic callers that must not silently run with a dropped detector) use
    load_cards_report()."""
    report = load_cards_report()
    for w in report["load_warnings"]:
        print(f"[WARNING] {w['status']} card {w['card']}: {w['error']} "
              f"— sign will not be recognized")
    return report["cards"]


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
# F-NEW-3 — the witness predicate is TWO-STAGE (candidate detection, then
# context-gated emission) so it neither floods (NBSP in prose) nor goes blind
# (NBSP hiding a host).
#
# STAGE_A candidate = union of PROPERTIES (not a hand-typed list):
#   General_Category == Cf, OR Default_Ignorable_Code_Point (loaded from the
#   pinned UCD DerivedCoreProperties.txt, not hardcoded), OR {Zl, Zp}, OR a
#   fixed set of non-ASCII whitespace, OR the braille blank U+2800 (blank
#   rendering, cat So — the P0 slice folded in here, NOT duplicated).
#   Deliberately NOT the whole of Mn (ordinary script), nor all So, nor all Zs.
#
# STAGE_B emission by FAMILY x CONTEXT (the anti-flood boundary — context gate,
# not a bare block-list):
#   CONTROL family (Cf / bidi / join / variation / braille) -> witness EVERYWHERE
#     (anomalous in any context, incl. FREE_TEXT).
#   WHITESPACE family (Zl/Zp, non-ASCII spaces, NBSP) -> witness ONLY when a
#     REMOVAL PROBE shows a machine context (the whitespace itself can hide its
#     own context: paypal<NBSP>.com tokenises as FREE_TEXT until the NBSP is
#     removed and 'paypal.com' reappears as HOST). In prose/typography -> silent.
#   Ordinary ASCII space/tab/LF/CR -> NEVER a candidate (N1 must pass).
#
# The witness NEVER changes the verdict; it is surfaced next to it. Default_
# Ignorable != safe-to-delete: we remove a whitespace ONLY to PROBE the context,
# never from the text.

_BIDI_CONTROL_CLASSES = {
    "LRE", "RLE", "LRO", "RLO", "PDF", "LRI", "RLI", "FSI", "PDI",
}
# Fallback ONLY if the pinned UCD file is unreadable (honest DEGRADED, declared).
_DEFAULT_IGNORABLE_EXTRA_RANGES = (
    (0x034F, 0x034F), (0x115F, 0x1160), (0x17B4, 0x17B5), (0x180B, 0x180F),
    (0x200B, 0x200F), (0x202A, 0x202E), (0x2060, 0x2064), (0x206A, 0x206F),
    (0x3164, 0x3164), (0xFE00, 0xFE0F), (0xFEFF, 0xFEFF), (0xFFA0, 0xFFA0),
    (0xFFF0, 0xFFF8), (0xE0100, 0xE01EF),
)
_VARIATION_SELECTOR_RANGES = ((0xFE00, 0xFE0F), (0xE0100, 0xE01EF))
# Non-ASCII whitespace (the explicit set, NOT "all Zs without context").
_NON_ASCII_WS = frozenset(
    {0x0085, 0x00A0, 0x1680, 0x202F, 0x205F, 0x3000} | set(range(0x2000, 0x200B)))
_ASCII_WS = " \t\n\r\f\v"
_MACHINE_STRUCTURED = {"HOST", "EMAIL", "PATH", "URL", "HIDDEN_BOUNDARY_PADDING"}

_DI_CACHE = {}


def _default_ignorable_set():
    """Default_Ignorable_Code_Point from the pinned UCD source (STAGE_A). Loaded
    from DerivedCoreProperties.txt (tools/sources/<ver>/), NOT hardcoded, so it
    tracks the pinned Unicode version. Falls back to a curated set (declared
    DEGRADED) only if the file is unreadable."""
    if "set" in _DI_CACHE:
        return _DI_CACHE["set"], _DI_CACHE["source"]
    di, source = set(), "EMBEDDED_FALLBACK_DEGRADED"
    try:
        import json
        tools = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools")
        with open(os.path.join(tools, "sources", "CURRENT_VERSION.json"),
                  encoding="utf-8") as f:
            man = json.load(f)
        # the manifest path is relative to tools/ (where the pointer lives),
        # and uses OS-native separators — normalise for the current platform.
        rel = man["files"]["DerivedCoreProperties.txt"]["path"].replace("\\", os.sep)
        dcp = os.path.join(tools, rel)
        with open(dcp, encoding="utf-8") as f:
            for line in f:
                line = line.split("#", 1)[0].strip()
                if not line or "Default_Ignorable_Code_Point" not in line:
                    continue
                rng = line.split(";", 1)[0].strip()
                if ".." in rng:
                    a, b = rng.split("..")
                    di.update(range(int(a, 16), int(b, 16) + 1))
                else:
                    di.add(int(rng, 16))
        source = "UCD_" + man.get("unicode_version", "?")
    except Exception:
        for lo, hi in _DEFAULT_IGNORABLE_EXTRA_RANGES:
            di.update(range(lo, hi + 1))
    _DI_CACHE["set"], _DI_CACHE["source"] = di, source
    return di, source


def _invisible_candidate(ch: str):
    """STAGE_A. Returns (family, reason_tag) or (None, ''). family is CONTROL
    (witness everywhere) or WHITESPACE (context-gated in STAGE_B)."""
    cp = ord(ch)
    if cp in (0x20, 0x09, 0x0A, 0x0D):
        return (None, "")                       # ordinary ASCII ws -> NEVER
    cat = unicodedata.category(ch)
    # ---- CONTROL families: anomalous in ANY context ----
    if cat == "Cf":
        if unicodedata.bidirectional(ch) in _BIDI_CONTROL_CLASSES:
            return ("CONTROL", "BIDI_CONTROL")
        if cp in (0x200C, 0x200D):
            return ("CONTROL", "JOIN_CONTROL")
        return ("CONTROL", "FORMAT_CONTROL")
    if cp == 0x2800:                             # BRAILLE PATTERN BLANK (So)
        return ("CONTROL", "BLANK_RENDERING")
    if any(lo <= cp <= hi for lo, hi in _VARIATION_SELECTOR_RANGES):
        return ("CONTROL", "VARIATION_SELECTOR")
    di, _src = _default_ignorable_set()
    if cp in di:
        return ("CONTROL", "DEFAULT_IGNORABLE")
    # ---- WHITESPACE families: context-gated (STAGE_B) ----
    if cat == "Zl":
        return ("WHITESPACE", "LINE_SEPARATOR")
    if cat == "Zp":
        return ("WHITESPACE", "PARAGRAPH_SEPARATOR")
    if cp in _NON_ASCII_WS:
        return ("WHITESPACE", "NON_ASCII_WHITESPACE")
    return (None, "")


def _reconstructed_context(text: str, i: int) -> str:
    """REMOVAL PROBE: drop the char at i, take the joined token around the join
    (bounded by ordinary ASCII whitespace), and classify its machine context.
    Reuses the sequence-layer domain/token helpers so the classification matches
    the detector. Returns HOST/EMAIL/BYTE_EXACT_TOKEN/FREE_TEXT."""
    a = i
    while a > 0 and text[a - 1] not in _ASCII_WS:
        a -= 1
    b = i + 1
    while b < len(text) and text[b] not in _ASCII_WS:
        b += 1
    joined = _se._strip_label_invisibles(text[a:i] + text[i + 1:b])
    if not joined:
        return "FREE_TEXT"
    tld_set, degraded = _se._tlds()
    if _se._looks_like_domain(joined, tld_set, degraded):
        return "HOST"
    if "@" in joined:
        at = joined.rfind("@")
        local, dom = joined[:at], joined[at + 1:]
        if local and _se._looks_like_domain(dom, tld_set, degraded):
            return "EMAIL"
    if _se._is_byte_exact_token(joined):
        return "BYTE_EXACT_TOKEN"
    return "FREE_TEXT"


def _whitespace_witnesses(text: str, i: int):
    """STAGE_B for the WHITESPACE family. Returns the machine context (-> witness)
    or None (-> silent, no flood). A domain-structured reconstruction witnesses
    even inside prose (a hidden host is dangerous anywhere); a bare byte-token
    witnesses only when the text is NOT prose (a standalone machine token, not a
    word in a sentence — this is the NBSP-in-'100 km' flood guard)."""
    ctx = _reconstructed_context(text, i)
    if ctx in _MACHINE_STRUCTURED:
        return ctx
    if ctx == "BYTE_EXACT_TOKEN" and not any(c in _ASCII_WS for c in text):
        return ctx
    return None


def _witness_record(ch, i, family, tag, context_note):
    try:
        name = unicodedata.name(ch)
    except ValueError:
        name = "UNNAMED / UNASSIGNED CODE POINT"
    basis = f"invisible code point ({tag}, family {family}) with no card"
    if context_note:
        basis += f" — {context_note}"
    basis += " -> intent cannot be verified by the system"
    return {
        "codepoint": f"U+{ord(ch):04X}",
        "at_offset": i,
        "unicode_name": name,
        "category": unicodedata.category(ch),
        "trigger": tag,
        "family": family,
        "context_note": context_note,
        "card_status": "NOT_CREATED",
        "finding_status": "UNVERIFIABLE",   # ACK_GAP_TRIVALENT: not safe, not dangerous
        "finding_basis": basis,
        "recommendation": (
            "hold and look by eye; not judged safe and not judged "
            "dangerous; Default_Ignorable != safe-to-delete"),
    }


def scan_uncarded_invisibles(text: str, cards: list) -> list:
    """Witness pass (F-NEW-3, two-stage). Reports uncarded invisibles that
    STAGE_A flags AND STAGE_B admits. Never a verdict; carded code points and
    ordinary ASCII whitespace are excluded."""
    carded = {ord(c.visible_form) for c in cards if len(c.visible_form) == 1}
    records = []
    for i, ch in enumerate(text):
        if ord(ch) in carded:
            continue
        family, tag = _invisible_candidate(ch)
        if family is None:
            continue
        note = ""
        if family == "WHITESPACE":
            wctx = _whitespace_witnesses(text, i)
            if wctx is None:
                continue                  # STAGE_B gate: prose/typography -> no flood
            note = f"inside reconstructed {wctx}"
        records.append(_witness_record(ch, i, family, tag, note))
    return records


# --- INVISIBLE_DEFAULT_IGNORABLE_GUARD (increment 1: shadow annotator) ---------
# Approved via conveyor (D-GUARD-IMPL-PLAN, 2026-07-18). ADDITIVE and CONTEXT-FREE:
# it observes the supervised class (Cf AND Default_Ignorable = the 138) and emits a
# report-ONLY field. It NEVER enters the verdict path (single/relation/semantic/
# effective_action) and NEVER strips the stream. Increment 1 keeps canonical_view =
# identity (no destructive canonicalization yet) and the position trace = identity.
#
# Mandatory patches carried here (from the approved plan):
#   P4  is_monitored_control_138: the EXACT 138 predicate (Cf AND DI), SEPARATE from
#       the broader _invisible_candidate (which also flags VS / braille / whitespace).
#   P2ii exception containment: any internal error -> status GUARD_FAILURE, the caller
#       keeps the original analysis bit-for-bit (fail-open at runtime; witness, not judge).
#   P2iii resource bound: members are capped; on overflow status = TRACE_TRUNCATED and
#       the total count is preserved (a megabyte flood of invisibles must not OOM the
#       pipeline; the ZWSP battery never floods, so it cannot catch this).
#   P5/P6 canonical_view identity-only + identity position trace in increment 1.
# The shadow field is validated by its OWN oracle (tests/guard_shadow_oracle.py), because
# verdict-identity cannot see a field the verdict path never reads (gate hole #1).

GUARD_SCHEMA_VERSION = "class_guard/0.1"
_GUARD_MEMBER_CAP = 4096            # resource bound (P2iii); TRACE_TRUNCATED beyond this
_MONITORED_138_CACHE = {}


def _monitored_138_set():
    """The EXACT supervised class = General_Category==Cf AND Default_Ignorable
    (from the pinned UCD via _default_ignorable_set). Cached. This is the 138,
    NOT the broader _invisible_candidate STAGE_A set (P4)."""
    if "set" in _MONITORED_138_CACHE:
        return _MONITORED_138_CACHE["set"]
    di, _src = _default_ignorable_set()
    s = frozenset(cp for cp in di if unicodedata.category(chr(cp)) == "Cf")
    _MONITORED_138_CACHE["set"] = s
    return s


def is_monitored_control_138(ch: str) -> bool:
    """P4 exact-138 membership by pinned Unicode properties only (no rendering,
    no heuristic, no context)."""
    return ord(ch) in _monitored_138_set()


# Full Bidi_Class set that marks a class-138 member as DIRECTIONAL. NOT the registrar's
# _BIDI_CONTROL_CLASSES (which omits the strong marks L/R/AL) — the class bucket must
# match the verified oracle (gen_class138_oracle.py): DIRECTIONAL = 12 incl LRM/RLM/ALM.
_DIRECTIONAL_BIDI_138 = frozenset({
    "L", "R", "AL", "LRE", "RLE", "PDF", "LRO", "RLO", "LRI", "RLI", "FSI", "PDI",
})


def _class_bucket_138(cp: int) -> str:
    if cp == 0xE0001 or 0xE0020 <= cp <= 0xE007F:
        return "TAG"
    if 0x206A <= cp <= 0x206F:
        return "DEPRECATED"
    if unicodedata.bidirectional(chr(cp)) in _DIRECTIONAL_BIDI_138:
        return "DIRECTIONAL"
    return "PURE"


def class_guard_annotate(text: str, carded=frozenset()) -> dict:
    """Increment-1 shadow annotator. PURE and CONTEXT-FREE. Returns a report-only
    GuardResult dict; it is NEVER read by the verdict path. On any internal error it
    returns status GUARD_FAILURE so the caller keeps its analysis unchanged."""
    try:
        monitored = _monitored_138_set()
        members = []
        overflow = 0
        for i, ch in enumerate(text):
            cp = ord(ch)
            if cp not in monitored:
                continue
            if len(members) >= _GUARD_MEMBER_CAP:
                overflow += 1
                continue
            try:
                name = unicodedata.name(ch)
            except ValueError:
                name = "UNNAMED / UNASSIGNED CODE POINT"
            members.append({
                "codepoint": "U+%04X" % cp,
                "unicode_name": name,
                "original_offset": i,          # codepoint index in the original (P5)
                "class_bucket": _class_bucket_138(cp),
                "family": "CONTROL",
                "card_mask": cp in carded,
            })
        return {
            "schema_version": GUARD_SCHEMA_VERSION,
            "ucd_source": _default_ignorable_set()[1],
            "original": text,                  # exact input STRING (not bytes; P5)
            "members": members,
            "canonical_view": text,            # identity in increment 1 (P6)
            "position_trace": "identity",      # identity spans in increment 1 (P5)
            "member_count": len(members) + overflow,
            "truncated": overflow,
            "status": "OK" if overflow == 0 else "TRACE_TRUNCATED",
        }
    except Exception as e:                     # P2ii: fail-open, never crash the pipeline
        return {
            "schema_version": GUARD_SCHEMA_VERSION,
            "original": text,
            "members": [],
            "canonical_view": text,
            "position_trace": "identity",
            "member_count": 0,
            "truncated": 0,
            "status": "GUARD_FAILURE",
            "error": type(e).__name__,
        }


# --- CANONICAL PROJECTION (P1 of AUTHOR_DECISION_20260721_D-O1-TOKEN-CELL) -----------
# WHY: the token cell stays at MEDIUM/queue -- measurement showed a direct escalation
# would false-positive on 67% of benign BOM-carrying text. The value is not a louder
# siren but SHOWING the human what the invisible does: "looks like paypal; actually
# pay<U+FEFF>pal". The projection states a STRUCTURAL fact and judges nothing.
#
# HARD LIMIT: this is DISPLAY ONLY. The collapsed form must NEVER be used as the string
# a decision is made on -- that would be a silent sanitizer, destroying the very byte
# difference a ghost-token exploits. Like class_guard, it lives in its own report field
# and is NEVER read by the verdict path.
PROJECTION_SCHEMA_VERSION = "canonical_projection/0.1"
_PROJECTION_TOKEN_CAP = 512               # resource bound; TRACE_TRUNCATED beyond this


def canonical_projection_annotate(text: str) -> dict:
    """Report-only projection. PURE and CONTEXT-FREE. For every whitespace-delimited
    token carrying a class-138 member, report the token as written, its collapsed form
    (members removed) and the members' offsets in ORIGINAL coordinates. Fail-open."""
    try:
        monitored = _monitored_138_set()
        tokens = []
        overflow = 0
        i = 0
        n = len(text)
        while i < n:
            if text[i].isspace():
                i += 1
                continue
            start = i
            while i < n and not text[i].isspace():
                i += 1
            tok = text[start:i]
            members = [(start + k, ord(ch)) for k, ch in enumerate(tok)
                       if ord(ch) in monitored]
            if not members:
                continue
            if len(tokens) >= _PROJECTION_TOKEN_CAP:
                overflow += 1
                continue
            collapsed = "".join(ch for ch in tok if ord(ch) not in monitored)
            tokens.append({
                "token_offset": start,             # original coordinates (P5 convention)
                "original_token": tok,
                "collapsed_token": collapsed,      # DISPLAY ONLY -- never a decision string
                "members": [{"codepoint": "U+%04X" % cp, "original_offset": off}
                            for off, cp in members],
                "tag": "PROJECTION",
            })
        return {
            "schema_version": PROJECTION_SCHEMA_VERSION,
            "tokens": tokens,
            "token_count": len(tokens) + overflow,
            "truncated": overflow,
            "display_only": True,                  # contract: not a normalization source
            "status": "OK" if overflow == 0 else "TRACE_TRUNCATED",
        }
    except Exception as e:                         # fail-open, never crash the pipeline
        return {
            "schema_version": PROJECTION_SCHEMA_VERSION,
            "tokens": [],
            "token_count": 0,
            "truncated": 0,
            "display_only": True,
            "status": "PROJECTION_FAILURE",
            "error": type(e).__name__,
        }


def analyze(text: str, cards: list, protected_targets=None) -> dict:
    """Full text run through all layers. Returns a report structure
    for printing (and possible programmatic use).

    protected_targets — OPTIONAL set of strings the CALLER protects (exact-match
      allowlist / policy keywords). Supplying it enables the C6 stripped-match rule: a
      token whose written form is NOT a target but whose collapse IS is an impersonation
      and is raised to hold. Default None = the rule is unreachable and the analysis is
      byte-identical to before. The consumer owns these semantics; the system ships no
      word list of its own. See AUTHOR_DECISION_20260721_D-O1-C6-NARROW for the measured
      caveat: ORDINARY-WORD targets (system/select/root/...) also occur in prose and
      raise false positives — keep the list narrow and specific until CONTEXT_V2 lands."""
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
    # C6 context passed DOWN as data (no import upward, no global state): the caller's
    # protected targets plus the verified class-138 set, which lives here. With no targets
    # the deriver returns nothing and the O1 row is unreachable.
    _o1_ctx = None
    if protected_targets:
        _o1_ctx = _O1Context(
            protected_targets=frozenset(t.lower() for t in protected_targets),
            class138=_monitored_138_set(),
        )
    seq_out = process_sequence(text, cards, sign_statuses=sign_statuses,
                               known_signs=known_signs, o1_ctx=_o1_ctx)
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

    # --- UNCARDED class-138 host-break -> a VERDICT, not only a witness (D-INV-GEN) ---
    # AUTHOR-directed generalization (2026-07-22): an invisible that breaks a HOST label is
    # the same byte-exact evasion whether or not it happens to be carded. Only ZWSP/ZWJ/BOM
    # are carded, so the other ~135 supervised code points (invisible math operators, word
    # joiner, soft hyphen, tag chars, ...) previously reached the human only as a
    # non-blocking witness. In a HOST the case is UNAMBIGUOUS (no invisible is legitimate
    # inside a domain), so it is escalated here. FIRST CUT: HOST only (token/email/other stay
    # witness-only, pending the follow-up conveyor). ADDITIVE: the witness channel is
    # untouched and this only RAISES effective_action; it never lowers a verdict. A
    # combining mark can no longer hide the host (419cae2), so this reconstruction is robust.
    # mask=EMPTY on purpose: _detect_context_at strips residual invisibles for the
    # reconstruction itself (F-NEW-1), so the uncarded char at the offset is removed anyway;
    # passing the carded alphabet here would wrongly demask a structural '.' (the DOT card)
    # and break domain reconstruction -> BYTE_EXACT_TOKEN instead of HOST.
    try:
        _mon138 = _monitored_138_set()
        for _u in uncarded_invisibles:
            _off = _u.get("at_offset")
            if _off is None or not (0 <= _off < len(text)):
                continue
            if ord(text[_off]) not in _mon138:
                continue                   # only the supervised class; braille/VS/whitespace stay witness
            if _se._detect_context_at(text, _off, frozenset()) == "HOST":
                effective_action = most_severe([effective_action, "hold_pending_review"])
                break
    except Exception:
        pass                               # fail-open: on any error keep the verdict, never crash

    # --- INVISIBLE_DEFAULT_IGNORABLE_GUARD (increment 1, shadow, report-ONLY) ---
    # Additive: placed in its OWN field, NEVER read by single_actions /
    # relation_actions / semantic_action / effective_action. A broken class_guard
    # cannot change the verdict (that is the whole safety argument, gate hole #1).
    # MSL_MIP_GUARD_DISABLED=1 omits the field entirely — used ONLY by the
    # full-differential gate (P7) to prove the rest of the report is byte-identical
    # with and without the guard. Default: guard enabled.
    if os.environ.get("MSL_MIP_GUARD_DISABLED") == "1":
        class_guard = None
    else:
        _carded_cps = {ord(c.visible_form) for c in cards if len(c.visible_form) == 1}
        class_guard = class_guard_annotate(text, carded=_carded_cps)
    # ATTENTION_STATUS (F-NEW-3): an uncarded witness alongside the verdict means
    # the interface must NOT show a clean PASS — the human sees "PASS, but hold
    # your eye: an invisible with no card is present". The verdict is untouched.
    attention_status = "WITNESS_PRESENT" if uncarded_invisibles else "NONE"

    report = {
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
        "attention_status": attention_status,
    }
    if class_guard is not None:              # omitted only under MSL_MIP_GUARD_DISABLED
        report["class_guard"] = class_guard  # increment-1 shadow field (report-only)
    # CANONICAL PROJECTION (P1): additive, report-ONLY, display-only. Never read by
    # single_actions / relation_actions / semantic_action / effective_action, so a broken
    # projection cannot change a verdict. MSL_MIP_PROJECTION_DISABLED=1 omits the field
    # entirely -- used by the zero-delta gate to prove the rest of the report is identical
    # with and without it. Default: projection enabled.
    if os.environ.get("MSL_MIP_PROJECTION_DISABLED") != "1":
        report["canonical_projection"] = canonical_projection_annotate(text)
    # PENDING DISPOSITION (P3): a cell that was examined and deliberately left
    # un-escalated must not read as silence. For every occurrence landing in a cell the
    # O1 registry documents as PENDING_PREDICATE, report BOTH honest readings plus the
    # gap and the evidence that would unblock a rule. Report-ONLY and additive: it is
    # never read by any action path, and a level is never derived from it.
    _pending = []
    for _v in seq_out.relation_verdicts:
        _vf = _v.get("visible_form", "")
        if len(_vf) != 1:
            continue
        _rec = _o1_pending_for(ord(_vf), _v.get("detected_context"))
        if _rec is not None:
            _entry = dict(_rec)
            _entry["at_offset"] = _v.get("at_offset")
            _pending.append(_entry)
    if _pending:
        report["pending_disposition"] = _pending
    return report


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
            fam = f"{r.get('family', '')}/" if r.get('family') else ""
            note = f"  ({r['context_note']})" if r.get('context_note') else ""
            print(f"  [{r['at_offset']}] {r['codepoint']} ({r['unicode_name']}) "
                  f"[{r['category']}/{fam}{r['trigger']}]{note}")
            print(f"        card: {r['card_status']}   finding: {r['finding_status']}")
            print(f"        basis: {r['finding_basis']}")
            print(f"        -> to the human: {r['recommendation']}")

    print("\n" + "=" * 60)
    sem = report["semantic_action"]
    eff = report["effective_action"]
    status = report.get("integrity_status", "OK")
    attention = report.get("attention_status", "NONE")
    # F-NEW-3: never a clean PASS in the window when an uncarded invisible is
    # present — the witness rides ALONGSIDE the verdict, does not change it.
    att_tag = ("   [⚠ ATTENTION: WITNESS_PRESENT — uncarded invisible above; "
               "hold your eye]" if attention == "WITNESS_PRESENT" else "")
    if status == "OK":
        print(f"FINAL VERDICT: {sem.upper()}{att_tag}")
    else:
        # D-GUARD-4: show BOTH so the human sees the discrepancy in the window.
        print(f"SEMANTIC VERDICT (main path): {sem.upper()}")
        print(f"INTEGRITY: {status}")
        for viol in report.get("integrity_violations", []):
            print(f"  [INTEGRITY_VIOLATION] {viol['detail']}")
        for con in report.get("integrity_concerns", []):
            print(f"  [{con['rule']}] {con['detail']}")
        print(f"EFFECTIVE VERDICT (integrity-adjusted): {eff.upper()}{att_tag}")
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
