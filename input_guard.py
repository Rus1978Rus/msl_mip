# -*- coding: utf-8 -*-
"""Input-Guard Mode A -- a DoS cost budget on the INPUT, run before the sign
layers (design: AUTHOR_DECISION_20260721_D-INPUT-GUARD-MODE-A-DESIGN; plan:
conveyor_runs/IG_IMPL_PLAN_2026-07-26). FIRST-CUT implementation.

FRAME: this is the WITNESS frame -- the guard NEVER blocks. A collapse produces a
single HOLD recommendation (a suggestion to the human), never an automatic block.
RESOURCE_LIMIT_EXCEEDED is NOT a proven attack.

One O(n) pass computes a few cheap statistics, then a two-tier, conjunctive,
threshold decision:
  OK                    -> analysis proceeds unchanged (the common case).
  DENSITY_SIGNAL        -> analysis proceeds, but a bare PASS is forbidden: the
                           caller raises the verdict to at least queue_for_review
                           and records DENSITY_ANOMALY. (medium invisible density)
  INGESTION_HOLD_SUMMARY-> the input is pathological; the caller short-circuits the
                           heavy layers, analysing only the VISIBLE PROJECTION
                           (flood stripped / long runs collapsed) so a flood can
                           NOT hide a phishing tail (anti-smokescreen, G10), and
                           surfaces ONE hold summary.

Thresholds are deliberately conservative FIRST-CUT values, set far above any
honest input so the guard never false-collapses ordinary text/code (calibration
by a larger benchmark corpus is a follow-up, per the plan). ASCII/machine text
uses the base thresholds; text carrying non-ASCII letters (CJK/Arabic/...) is
given headroom, while the hard byte/compute backstops stay profile-independent.
"""
import unicodedata

SCHEMA_VERSION = 1

# --- hard, profile-independent backstops ---
_BYTE_BACKSTOP = 500_000          # ~0.5 MB free backstop (honest long input is fine)
_COMPUTE_MIN = 2048               # below this, never collapse (short input is cheap)

# --- collapse (T_collapse) thresholds (conjunctive with _COMPUTE_MIN) ---
# Calibrated 2026-07-26 on a broad honest corpus (prose/code/CSV/base64/json/log/
# CJK/markdown/URL-lists): the per-char DoS these once guarded is now removed
# algorithmically (D-ONSQ-FIX + D-ONSQ-CLAIMED-FIX + substrate round 4), so the
# thresholds are relaxed to stop false-collapsing legit dense/repetitive content
# (deeply-indented code was ~0.89 dominant; a single-digit CSV is exactly 0.50).
# Only a near-pure single-char flood (>=0.95) or a large invisible/trigger flood trips.
_DOMINANT_COLLAPSE = 0.95         # one code point is >=95% of the input (near-pure flood)
_INVIS_SHARE_COLLAPSE = 0.30      # invisibles (Cf) are >30% of the input (hidden channel)
_TRIGGER_COLLAPSE = 4096          # invisibles + url-structural chars (legit URL lists are fine)

# --- signal (T_signal) thresholds (count-floor: count AND ratio) ---
_SIGNAL_INVIS_COUNT = 20
_SIGNAL_INVIS_RATIO = 0.20

# --- projection ---
_MAX_RUN = 8                      # collapse any run of one char longer than this


def _is_invisible(ch: str) -> bool:
    """Coarse invisible/format predicate for the budget layer (Cf format chars,
    which covers the supervised class-138 plus related formats). Deliberately
    broad -- this is a cost budget, not the precise verdict class."""
    return unicodedata.category(ch) == "Cf"


def _script_headroom(text: str) -> float:
    """Non-ASCII letters (real i18n prose) get threshold headroom so dense CJK/
    Arabic text is not mistaken for a flood; the hard backstops are unaffected."""
    for ch in text:
        if ord(ch) > 0x2FF and unicodedata.category(ch).startswith("L"):
            return 1.5
    return 1.0


def visible_projection(text: str) -> str:
    """Flood-stripped view for collapse analysis: drop invisibles (Cf) and
    collapse any run of the same character longer than _MAX_RUN. A hidden
    phishing tail (invisibles stripped) stays intact; a visible single-char flood
    shrinks to a short residue. Best-effort view -- offsets are projection-relative."""
    out = []
    prev = None
    run = 0
    for ch in text:
        if _is_invisible(ch):
            continue
        if ch == prev:
            run += 1
            if run > _MAX_RUN:
                continue
        else:
            prev = ch
            run = 1
        out.append(ch)
    return "".join(out)


def input_guard_scan(text: str) -> dict:
    """Single O(n) weighing pass + two-tier decision. Returns the input_guard
    report contract (never raises on ordinary input)."""
    n = len(text)
    counts = {}
    invis = 0
    triggers = 0
    for ch in text:
        counts[ch] = counts.get(ch, 0) + 1
        if _is_invisible(ch):
            invis += 1
            triggers += 1
        elif ch in "/\\":
            triggers += 1
    dominant = max(counts.values()) if counts else 0
    dominant_share = dominant / n if n else 0.0
    invis_share = invis / n if n else 0.0
    hr = _script_headroom(text)

    status = "OK"
    reason = "within_budget"
    action = "none"

    big = n >= _COMPUTE_MIN
    if (n > _BYTE_BACKSTOP
            or (big and dominant_share > _DOMINANT_COLLAPSE * hr)
            or (big and invis_share > _INVIS_SHARE_COLLAPSE * hr)
            or triggers > _TRIGGER_COLLAPSE):
        status = "INGESTION_HOLD_SUMMARY"
        reason = "ingestion_flood"
        action = "hold_pending_review"
    elif invis >= _SIGNAL_INVIS_COUNT and invis_share > _SIGNAL_INVIS_RATIO * hr:
        status = "DENSITY_SIGNAL"
        reason = "invisible_density_anomaly"
        action = "queue_for_review"

    # a handful of sampled invisible offsets for the human (bounded, anti-flood)
    sampled = []
    if status != "OK":
        for i, ch in enumerate(text):
            if _is_invisible(ch):
                sampled.append(i)
                if len(sampled) >= 8:
                    break

    return {
        "schema_version": SCHEMA_VERSION,
        "mode": "A",
        "status": status,
        "reason_class": reason,
        "action_recommendation": action,
        "counters": {
            "length": n,
            "invisibles": invis,
            "invisible_share": round(invis_share, 4),
            "dominant_share": round(dominant_share, 4),
            "trigger_total": triggers,
        },
        "sampled_offsets": sampled,
        "truncated": status == "INGESTION_HOLD_SUMMARY",
    }
