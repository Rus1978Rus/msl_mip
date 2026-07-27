#!/usr/bin/env python3
# SPDX: PRIVATE AUTHORIAL PROJECT / COMMERCIAL USE PROHIBITED
"""CANONICALIZATION_PRE_PASS — skeleton implementation.

Spec: conveyor_runs/PREPASS_IMPL_CHECKLIST_2026-07-27.md
Design note: conveyor_runs/OBSERVERS_CANONICALIZATION_2026-07-27.md

STATUS: WORKING_DRAFT — NOT conveyor-reviewed, NOT wired into the runtime yet.
Frame: witness, not judge. The pre-pass does NOT emit a final risk verdict; it
produces a CANONICAL string for the sign cards (scan_signs), or HOLDs
(fail-closed) when it cannot resolve the input to one form.

Stages (see checklist §3). Coverage is honestly partial where noted:
  S1 percent-decode        -- WORKING (stdlib urllib)
  S2 overlong-UTF-8        -- PARTIAL: detect classic markers -> REJECT (TODO: full byte validation)
  S3 NFKC / confusable     -- PARTIAL: NFKC works; homoglyph skeleton is TODO (needs Unicode data)
  S4 zero-width / bidi      -- WORKING for the listed set (TODO: full Cf / real bidi reorder)
  S5 entity-decode (gated)  -- WORKING (html.unescape), HTML sinks only
  S6 host/IP-normalize (gated) -- PARTIAL: decimal/hex int host (TODO: octal, IPv6, in-URL)

Pure standard library.
"""
from __future__ import annotations

import html
import ipaddress
import unicodedata
from dataclasses import dataclass, field
from urllib.parse import unquote

MAX_PASSES = 16

# sink_type values
URL = "URL"
HOST = "HOST"
HTML = "HTML"
FS = "FS"
TEXT = "TEXT"
UNKNOWN = "UNKNOWN"

_ZERO_WIDTH = {"​", "‌", "‍", "⁠", "﻿"}
_BIDI_CONTROLS = {"‪", "‫", "‬", "‭", "‮",
                  "⁦", "⁧", "⁨", "⁩"}
_STRIP = _ZERO_WIDTH | _BIDI_CONTROLS

# S2: classic overlong-UTF-8 lead markers (invalid shortest-form). Policy = REJECT.
_OVERLONG_MARKERS = ("%c0", "%c1", "%e0%80", "%f0%80%80")


@dataclass
class PrePassResult:
    status: str                       # "CANON" | "HOLD"
    canonical: str | None
    reason: str = ""
    stages_fired: list = field(default_factory=list)
    flags: list = field(default_factory=list)


# ----------------------------- stages ---------------------------------------
def percent_decode_once(s: str) -> str:
    """S1 (WORKING): one pass of percent-decoding (%2e -> .). Non-recursive;
    depth (e.g. %252e over two passes) is handled by the fixpoint loop."""
    return unquote(s)


def has_overlong(s: str) -> bool:
    """S2 (PARTIAL): detect classic overlong-UTF-8 percent markers (C0/C1 lead,
    overlong 3/4-byte forms). Policy in this skeleton = REJECT (fail-closed).
    TODO: full byte-level shortest-form validation via unquote_to_bytes."""
    low = s.lower()
    return any(m in low for m in _OVERLONG_MARKERS)


def nfkc_fold(s: str) -> str:
    """S3 (PARTIAL): NFKC normalization -- folds fullwidth (．／％) and other
    compatibility forms to ASCII. TODO: full Unicode *confusable skeleton*
    (cross-script homoglyphs, e.g. Cyrillic 'а' -> Latin 'a') needs the Unicode
    confusables table, which is not in the standard library."""
    return unicodedata.normalize("NFKC", s)


def strip_invisible(s: str) -> str:
    """S4 (WORKING for the listed set): remove zero-width (ZWSP/ZWNJ/ZWJ/
    word-joiner/BOM) and bidi controls (RLO/LRO/...). TODO: broader
    Default_Ignorable coverage + real bidi reordering."""
    return "".join(ch for ch in s if ch not in _STRIP)


def entity_decode_once(s: str) -> str:
    """S5 (GATED, WORKING): decode HTML entities (&#46; -> ., &sol; -> /).
    Applied ONLY for HTML sinks -- elsewhere it is a false-positive source."""
    return html.unescape(s)


def host_ip_normalize(s: str) -> str:
    """S6 (GATED, PARTIAL): normalize an integer/hex IPv4 host token to
    dotted-quad (2130706433 -> 127.0.0.1). WORKING for a bare decimal or 0x-hex
    integer token. TODO: octal (0177.0.0.1), mixed radices, IPv6, and locating
    the host token inside a full URL."""
    token = s.strip()
    try:
        if token.lower().startswith("0x"):
            val = int(token, 16)
        elif token.isdigit():
            val = int(token)
        else:
            return s
        return str(ipaddress.IPv4Address(val))
    except (ValueError, ipaddress.AddressValueError):
        return s


def detect_use_mention_ambiguity(raw: str, sink_type: str) -> bool:
    """Checklist §6 frontier (STUB): is this data-to-decode (use) or prose ABOUT
    encoding (mention, e.g. the sentence "never allow %2f")? Undecidable from the
    string alone -- needs context the string does not carry. Conservative stub
    returns False (treat as use). TODO: heuristic (sink==TEXT + surrounding
    natural language) -> flag AMBIGUOUS_USE_MENTION and hand to a human/card."""
    return False


# ----------------------------- driver ---------------------------------------
def _canonize(raw: str, entity: bool, host: bool, max_passes: int) -> PrePassResult:
    """Fixpoint loop over the decoder stages. Stages do NOT commute, so we
    iterate until a full pass changes nothing (joint fixpoint) or the pass cap
    is hit (decode-bomb -> HOLD)."""
    s = raw
    fired: list = []
    for _ in range(max_passes):
        if has_overlong(s):
            return PrePassResult("HOLD", None, "overlong-UTF-8 rejected (S2)", fired)
        prev = s
        t = percent_decode_once(s)
        if t != s:
            fired.append("S1")
        u = nfkc_fold(t)
        if u != t:
            fired.append("S3")
        v = strip_invisible(u)
        if v != u:
            fired.append("S4")
        if entity:
            w = entity_decode_once(v)
            if w != v:
                fired.append("S5")
            v = w
        if host:
            x = host_ip_normalize(v)
            if x != v:
                fired.append("S6")
            v = x
        s = v
        if s == prev:
            return PrePassResult("CANON", s, "fixpoint", _dedup(fired))
    return PrePassResult("HOLD", None,
                         f"did not converge in {max_passes} passes (decode-bomb)",
                         _dedup(fired))


def _dedup(xs: list) -> list:
    seen, out = set(), []
    for x in xs:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def pre_pass(raw: str, sink_type: str = UNKNOWN, max_passes: int = MAX_PASSES) -> PrePassResult:
    """Entry point. Returns a canonical string (status CANON) or HOLD.

    Gated stages (S5 entity, S6 host) depend on sink_type. If sink_type is
    UNKNOWN and a gated stage WOULD change the result, we cannot safely apply it
    (false positives) nor skip it (smuggle) -> fail-closed HOLD (checklist §5b).
    """
    if detect_use_mention_ambiguity(raw, sink_type):
        return PrePassResult("HOLD", None, "AMBIGUOUS_USE_MENTION (§6 frontier)",
                             [], ["AMBIGUOUS_USE_MENTION"])

    if sink_type == UNKNOWN:
        off = _canonize(raw, entity=False, host=False, max_passes=max_passes)
        on = _canonize(raw, entity=True, host=True, max_passes=max_passes)
        if off.status == "HOLD":
            return off
        if on.status == "HOLD":
            return on
        if off.canonical != on.canonical:
            return PrePassResult("HOLD", None,
                                 "gated decode changes result under UNKNOWN sink "
                                 "- fail-closed (§5b)",
                                 off.stages_fired, ["FAIL_CLOSED_GATE"])
        return off

    entity = sink_type == HTML
    host = sink_type in (HOST, URL)
    return _canonize(raw, entity, host, max_passes)


if __name__ == "__main__":
    demo = [
        ("%2e%2e%2fetc%2fpasswd", TEXT),
        ("%252e%252e%252fetc/passwd", TEXT),
        ("．．／etc／passwd", TEXT),
        ("&#46;&#46;&#47;etc&#47;passwd", HTML),
        ("&#46;&#46;&#47;etc&#47;passwd", UNKNOWN),
        ("2130706433", HOST),
        ("%c0%ae%c0%aeetc", TEXT),
    ]
    for raw, sink in demo:
        r = pre_pass(raw, sink)
        out = r.canonical if r.status == "CANON" else f"HOLD: {r.reason}"
        print(f"[{sink:7}] {raw!r:34} -> {out}")
