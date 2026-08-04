# -*- coding: utf-8 -*-
"""Bidi reordering axis, PHASE 1 (D-BIDI-REORDER).

Fourth kind of threat, after BREAK (W4/W5/D-INV-GEN), SUBSTITUTION (W7) and CONCEALMENT
(TAG/VS): REORDERING OF THE VISIBLE ORDER. Nothing is hidden and no byte is swapped, but
the eye reads a different string than the machine -- `invoice<RLO>gpj.exe` renders as
`invoiceexe.jpg`. All 12 bidi controls are already in class-138, so presence is already
witnessed and a host break already escalates via D-INV-GEN; this axis adds the one fact
neither of those carries: an override actually holds a span of text under its effect.

PHASE 1 (D1) deliberately does NOT run UAX#9. It costs zero new artifacts, because
`unicodedata.bidirectional()` ships with the interpreter and matches our pinned UCD
16.0.0 -- unlike the VS round, where the Script property turned out to be absent from
the stdlib and had to be pinned as repo data. The consequence is stated honestly rather
than hidden: phase 1 knows that a control CAN reorder, never that it DOES. Findings are
therefore named REORDERING_CAPABLE, and a no-op override inside an RTL paragraph will
raise a queue it does not deserve (named residual R5, closed by phase 2).

VALVE (D2): only OVERRIDES (LRO/RLO) open the signal contour. EMBEDDINGS (LRE/RLE) are
annotated without a level -- measured, they do not reorder Latin text, and their real
level needs the phase-2 reordering fact. MARKS (LRM/RLM/ALM) and ISOLATES (LRI/RLI/FSI/
PDI) never open it: marks are the measured flood source (Hebrew/Arabic prose produced
one witness per control, x20 -> 20), and isolates are the practice Unicode recommends.

PREDICATE (D3): an override whose scope holds >= 2 non-control characters. Balance is an
ANNOTATION, not a trigger -- a balanced `invoice<RLO>gpj<PDF>.exe` reorders exactly like
the unbalanced form, so requiring unbalancedness would miss the careful attacker. Scope
runs to the matching PDF (nesting-aware) or to the end of the paragraph (X8).
"""
import unicodedata

# The 12 controls, by family. Classes come from unicodedata.bidirectional(), which is
# authoritative here; the literal codepoints only anchor the family split.
OVERRIDES = {0x202D: "LRO", 0x202E: "RLO"}
EMBEDDINGS = {0x202A: "LRE", 0x202B: "RLE"}
POP_FORMATTING = 0x202C                      # PDF
MARKS = {0x200E: "LRM", 0x200F: "RLM", 0x061C: "ALM"}
ISOLATES = {0x2066: "LRI", 0x2067: "RLI", 0x2068: "FSI"}
POP_ISOLATE = 0x2069                         # PDI
_PARAGRAPH_SEPARATORS = ("\n", "\r", " ")

ALL_CONTROLS = (set(OVERRIDES) | set(EMBEDDINGS) | {POP_FORMATTING}
                | set(MARKS) | set(ISOLATES) | {POP_ISOLATE})

_MIN_SCOPE = 2                               # >= 2 non-control chars under the override


def _family(cp):
    if cp in OVERRIDES:
        return "override"
    if cp in EMBEDDINGS:
        return "embedding"
    if cp == POP_FORMATTING:
        return "pop_formatting"
    if cp in MARKS:
        return "mark"
    if cp in ISOLATES:
        return "isolate"
    if cp == POP_ISOLATE:
        return "pop_isolate"
    return None


def _name(cp):
    return (OVERRIDES.get(cp) or EMBEDDINGS.get(cp) or MARKS.get(cp)
            or ISOLATES.get(cp) or {POP_FORMATTING: "PDF", POP_ISOLATE: "PDI"}.get(cp)
            or "?")


def _scope(text, i):
    """Span held by the embedding/override initiator at i (spec B2): to the matching PDF,
    counting nested embeddings/overrides, else to the end of the paragraph. Returns
    (payload_chars, end_index, balanced). Raw nesting is counted regardless of the UAX#9
    depth cap, so an attacker cannot hide an unclosed scope behind an overflow."""
    depth = 1
    payload = 0
    j = i + 1
    while j < len(text):
        ch = text[j]
        if ch in _PARAGRAPH_SEPARATORS:
            return payload, j, False          # X8: closed implicitly, not balanced
        cp = ord(ch)
        if cp in OVERRIDES or cp in EMBEDDINGS:
            depth += 1
        elif cp == POP_FORMATTING:
            depth -= 1
            if depth == 0:
                return payload, j, True
        elif cp not in ALL_CONTROLS:
            payload += 1
        j += 1
    return payload, len(text), False


def scan_bidi(text):
    """Pure scan, phase 1. Never raises. `level` is raise-only material for the seam."""
    findings = []
    marks = []
    annotations = []
    for i, ch in enumerate(text):
        cp = ord(ch)
        fam = _family(cp)
        if fam is None:
            continue
        if fam == "mark":
            marks.append((i, _name(cp)))
            continue
        if fam in ("isolate", "pop_isolate", "pop_formatting"):
            # Isolates are recommended practice; an unmatched isolate is closed by the
            # end of the paragraph (BD9/X10) and an orphan PDF/PDI is a no-op (X6a).
            # Neither is an anomaly -- recorded only as a neutral annotation.
            annotations.append({"offset": i, "control": _name(cp), "family": fam})
            continue
        payload, end, balanced = _scope(text, i)
        record = {
            "offset": i, "control": _name(cp), "family": fam,
            "bidi_class": unicodedata.bidirectional(ch),
            "scope_chars": payload, "scope_end": end, "balanced": balanced,
        }
        if fam == "override" and payload >= _MIN_SCOPE:
            record["finding"] = "REORDERING_CAPABLE"
            findings.append(record)
        else:
            # Embedding (level deferred to phase 2) or a no-op override over <2 chars.
            record["finding"] = ("EMBEDDING_ANNOTATION" if fam == "embedding"
                                 else "OVERRIDE_NO_OP")
            annotations.append(record)
    marks_summary = {}
    if marks:
        # D7: the axis collapses marks in ITS OWN field. The shared uncarded_invisibles
        # channel is left untouched (many gates read it) -- residual R8.
        marks_summary = {
            "count": len(marks),
            "types": sorted({n for _, n in marks}),
            "first_offset": marks[0][0],
            "last_offset": marks[-1][0],
            "collapsed": True,
        }
    level = "queue_for_review" if findings else "pass"
    return {
        "status": "OK",
        "phase": 1,
        "findings": findings,
        "annotations": annotations,
        "marks_summary": marks_summary,
        "level": level,
        "contributed": bool(findings),        # D8: this axis's own attribution
        "note": ("phase 1: reordering capability only -- the UAX#9 reordering fact was "
                 "NOT computed"),
    }
