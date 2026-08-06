# -*- coding: utf-8 -*-
"""Zero-width bit-channel axis, phase 1 (D-ZW-BITS).

Third instance of the covert-channels family (TAG first, VS second) and the hardest so
far: TAG had an oracle ("any assigned tag char outside the three flags") and VS had one
("is the base+selector pair registered"), but here the SAME characters that carry bits
are mandatory orthography -- ZWNJ inside Persian, ZWJ inside every emoji family. There is
no oracle of legitimacy, only an oracle of MEANINGLESSNESS: it can say where a carrier
explains nothing, never that a carrier is innocent.

CARRIER STREAM (D1): the stream is built from carriers alone, with visible characters
ignored entirely. Both measured evasions then stop mattering by construction rather than
by tuning -- measured, a block payload and one spread across 400 visible characters yield
the IDENTICAL stream. Density and run length were already buried by measurement in this
round and in the TAG round.

ALTERNATION IS NOT A PREDICATE (D2). Three of the four reviewers built their second
pillar on it; a shaped 240-bit payload of 80 zeros + 80 ones + 80 zeros switches TWICE,
uses both carriers, and walks past any switch threshold. Switch count is chosen by the
attacker, exactly like run length and density before it.

ADJACENCY (D4) -- found by prototyping this design, not by the round. A carrier next to
another carrier is NONFUNCTIONAL by construction. Without that rule the prototype missed
the block, diluted and shaped payloads: in a block the neighbours of every carrier are
OTHER CARRIERS, so a positional oracle finds no joining context and answers UNVERIFIABLE.
The payload supplies its own context. Premise verified: 0 of 1468 RGI emoji sequences
stack two ZWJ, and no orthography stacks join controls.
"""
import hashlib
import os
import unicodedata

CARRIERS = {0x200B: "ZWSP", 0x200C: "ZWNJ", 0x200D: "ZWJ",
            0x2060: "WJ", 0xFEFF: "BOM", 0x00AD: "SHY"}
JOIN_CONTROLS = (0x200C, 0x200D)
EVIDENCE_BUDGET = 16          # design constant (spec B), never config
PREVIEW_CAP = 128             # carriers shown in the collapsed witness

_JT_FILE = "DerivedJoiningType.txt"
_JT_SHA256 = "6bd08b97da66b70ccfdab105a352de2984e02625239ec5695422c99b33d854f0"
_DEFAULT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "unicode")
_JT = None


def _sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_joining_types(base_dir=None):
    """Pinned Joining_Type. Returns {'status':'OK','map':{...}} or a fail-visible
    UNVERIFIABLE. The file's own '@missing: 0000..10FFFF; Non_Joining' default MUST be
    applied (spec B3): jt(ZWNJ) is ABSENT from the file, so a loader that ignores
    defaults would fail silently on the carrier itself."""
    path = os.path.join(base_dir or _DEFAULT_DIR, _JT_FILE)
    if not os.path.isfile(path):
        return {"status": "UNVERIFIABLE", "reason": "missing %s" % _JT_FILE, "map": {}}
    if _sha256_file(path) != _JT_SHA256:
        return {"status": "UNVERIFIABLE", "reason": "sha256 mismatch for %s" % _JT_FILE,
                "map": {}}
    table = {}
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            for line in f:
                line = line.split("#", 1)[0].strip()
                if not line:
                    continue
                parts = [p.strip() for p in line.split(";")]
                if len(parts) < 2:
                    continue
                rng = parts[0]
                if ".." in rng:
                    lo, hi = rng.split("..")
                    lo, hi = int(lo, 16), int(hi, 16)
                else:
                    lo = hi = int(rng, 16)
                val = parts[1].split()[0]
                for cp in range(lo, hi + 1):
                    table[cp] = val
    except (OSError, ValueError) as exc:
        return {"status": "UNVERIFIABLE", "reason": "parse failure: %s" % exc, "map": {}}
    return {"status": "OK", "map": table}


def get_joining_types():
    global _JT
    if _JT is None:
        _JT = load_joining_types()
    return _JT


def _jt(cp):
    """Joining_Type with the file's @missing default (U = Non_Joining)."""
    return get_joining_types()["map"].get(cp, "U")


def _transparent(ch):
    return unicodedata.category(ch) == "Mn" or 0xFE00 <= ord(ch) <= 0xFE0F


def _is_linker(ch):
    """Conjunct linker for the join-control rule.

    NORMATIVE SOURCE: InCB=Linker (UAX#29 GB9c) from the pinned
    DerivedCoreProperties -- exactly six viramas (Devanagari, Bengali, Gujarati,
    Oriya, Telugu, Malayalam), the same table the card layer's SNI oracle reads.

    This replaced `unicodedata.combining(ch) == 9`, which was measured to be a live
    evasion: ccc==9 holds for 69 codepoints, 63 of them NOT normative linkers
    (Khmer COENG, Thai PHINTHU, Myanmar virama, Javanese pangkon...). A two-carrier
    channel in Khmer cover with every carrier placed just after a COENG -- and COENG
    appears in almost every Khmer word -- read PROVEN_FUNCTIONAL throughout, so the
    nonfunctional count was zero and the axis stayed silent. The same channel between
    ordinary Khmer letters fired. Measured, not reasoned.

    FALLBACK: if the pinned table cannot be verified, fall back to ccc==9 -- the old,
    FP-safe semantics. Failing the other way would judge every Devanagari conjunct
    nonfunctional and flood an entire writing system, which is the failure mode this
    axis exists to avoid. The degradation is surfaced in the axis status."""
    tables = _sni_tables()
    if tables is not None and tables["status"] == "OK":
        return ord(ch) in tables["incb_linker"]
    return unicodedata.combining(ch) == 9


def _sni_tables():
    try:
        import sni_oracle
    except ImportError:
        return None
    return sni_oracle.get_sni_tables()


# Persian enclitics written with a half-space (nim-fasele) after a right-joining
# letter, ISIRI 9147 / normative orthography. A CLOSED list, pinned as data next to
# the rule that reads it: ra, ha, tar, tarin, i, am, at, ash, ist, and the plural haye.
_AFTER_R_SUFFIXES = (
    (0x0631, 0x0627),          # ra
    (0x0647, 0x0627),          # ha
    (0x062A, 0x0631),          # tar / tarin
    (0x0627, 0x06CC),          # i (ay)
    (0x0627, 0x0645),          # am
    (0x0627, 0x062A),          # at
    (0x0627, 0x0634),          # ash
    (0x0627, 0x0633, 0x062A),  # ist
)


def _after_r_suffix(text, right):
    """True when the text at `right` starts one of the closed set of Persian
    enclitic suffixes that normatively follow a half-space. Matching is on the
    literal codepoints, so the rule cannot drift with the surrounding heuristics."""
    for suf in _AFTER_R_SUFFIXES:
        if all(right + k < len(text) and ord(text[right + k]) == cp
               for k, cp in enumerate(suf)):
            return True
    return False


def function_status(text, i):
    """Four-state status (D3). NONFUNCTIONAL means only 'this occurrence explains
    nothing here' -- never 'proven malicious'."""
    cp = ord(text[i])
    # D4: carriers never stack in legitimate orthography.
    if (i > 0 and ord(text[i - 1]) in CARRIERS) or \
            (i + 1 < len(text) and ord(text[i + 1]) in CARRIERS):
        return "NONFUNCTIONAL"
    # The virama must be read from the IMMEDIATE neighbours, before the transparent
    # skip: it is category Mn, so skipping "transparent" marks would step straight over
    # it and the conjunct rule would never fire (caught by the gate, not by reasoning).
    if cp in JOIN_CONTROLS:
        if (i > 0 and _is_linker(text[i - 1])) or \
                (i + 1 < len(text) and _is_linker(text[i + 1])):
            return "PROVEN_FUNCTIONAL"
    left = i - 1
    while left >= 0 and (_transparent(text[left]) or ord(text[left]) in CARRIERS):
        left -= 1
    right = i + 1
    while right < len(text) and (_transparent(text[right])
                                 or ord(text[right]) in CARRIERS):
        right += 1
    lch = text[left] if left >= 0 else ""
    rch = text[right] if right < len(text) else ""
    if cp == 0x200D and lch and rch \
            and unicodedata.category(lch) in ("So", "Sk", "Sm") \
            and unicodedata.category(rch) in ("So", "Sk", "Sm"):
        # Emoji ZWJ by category fallback. Measured: this silences 1468 of 1468 RGI
        # sequences, so the RGI table buys no FP relief -- only a narrower non-RGI
        # bypass (residual R6), which is why it is not pinned here.
        return "PROVEN_FUNCTIONAL"
    if cp in JOIN_CONTROLS and lch and rch:
        if _is_linker(lch) or _is_linker(rch):
            return "PROVEN_FUNCTIONAL"          # normative conjunct linker (InCB)
        lj, rj = _jt(ord(lch)), _jt(ord(rch))
        if lj in ("D", "L", "C") and rj in ("D", "R", "C"):
            return "PROVEN_FUNCTIONAL"          # real cursive joining context
        # AFTER-R CARVE-OUT (D-R4 F4). Measured on the live oracle, and by the panel
        # independently (107 of 396 carriers in a correct 400-word document): a
        # right-joining letter cannot join what follows anyway, so the rule above
        # judged NORMATIVE Persian NONFUNCTIONAL -- the half-space before the enclitic
        # suffixes (ra, ha, tar, tarin, i, am; ISIRI 9147 nim-fasele). The suffix set
        # is CLOSED and its first letters are named explicitly, so the carve-out cannot
        # quietly widen into "anything after a right-joining letter".
        # Named micro-channel BYPASS_AFTER_R_CARVEOUT: an attacker who places carriers
        # exactly on these positions buys silence -- every carve-out mints its own
        # bypass, and this one is registered rather than discovered later.
        if lj == "R" and rj in ("D", "R", "C") and _after_r_suffix(text, right):
            return "PROVEN_FUNCTIONAL"
        return "NONFUNCTIONAL"
    if cp == 0x00AD:
        return "PLAUSIBLE_FUNCTIONAL" if (lch.isalpha() and rch.isalpha()) \
            else "NONFUNCTIONAL"
    if cp == 0xFEFF:
        return "PROVEN_FUNCTIONAL" if i == 0 else "NONFUNCTIONAL"
    if cp == 0x2060:
        # WJ has no positional oracle by construction (residual R7): its effect is on
        # line breaking, which neighbours cannot reveal.
        return "UNVERIFIABLE"
    return "PLAUSIBLE_FUNCTIONAL"                # ZWSP


def _segments(text):
    """D7: paragraphs, so a Persian paragraph's ZWNJ, a heading's WJ and a German
    word's SHY cannot be merged into an artificial pair. Deterministic, and never
    chosen by the content."""
    out, start = [], 0
    for i, ch in enumerate(text):
        if ch in ("\n", "\r", " "):
            if i > start:
                out.append((start, text[start:i]))
            start = i + 1
    if start < len(text):
        out.append((start, text[start:]))
    return out


def scan_zw_bits(text):
    """Pure scan, phase 1. Never raises. `level` is raise-only material for the seam."""
    jt = get_joining_types()
    findings = []
    total = 0
    for base, seg in _segments(text):
        occ = [(base + i, ord(c), function_status(seg, i))
               for i, c in enumerate(seg) if ord(c) in CARRIERS]
        total += len(occ)
        if len(occ) < EVIDENCE_BUDGET:
            continue
        keys = sorted(CARRIERS)
        for a_i in range(len(keys)):
            for b_i in range(a_i + 1, len(keys)):
                a, b = keys[a_i], keys[b_i]
                stream = [(o, cp, st) for o, cp, st in occ if cp in (a, b)]
                if len(stream) < EVIDENCE_BUDGET:
                    continue
                if len({cp for _, cp, _ in stream}) < 2:
                    continue
                nonfunc = sum(1 for _, _, st in stream if st == "NONFUNCTIONAL")
                if not nonfunc:
                    continue
                # A/B is a REPORTING CONVENTION (lower codepoint = A), never a claim
                # about which symbol the attacker meant as 0 or 1 (D9).
                symbols = "".join("A" if cp == a else "B" for _, cp, _ in stream)
                findings.append({
                    "segment_offset": base,
                    "pair": (CARRIERS[a], CARRIERS[b]),
                    "carrier_count": len(stream),
                    "nonfunctional": nonfunc,
                    "first_offset": stream[0][0],
                    "last_offset": stream[-1][0],
                    "symbol_stream": symbols[:PREVIEW_CAP],
                    "stream_truncated": len(symbols) > PREVIEW_CAP,
                    "stream_sha256": hashlib.sha256(symbols.encode()).hexdigest(),
                    "segment_sha256": hashlib.sha256(seg.encode("utf-8")).hexdigest(),
                })
    findings.sort(key=lambda f: (-f["carrier_count"], f["segment_offset"]))
    level = "queue_for_review" if findings else "pass"
    out = {
        "status": jt["status"],
        "phase": 1,
        "findings": findings,
        "carrier_total": total,
        "level": level,
        "contributed": bool(findings),
        "evidence_budget": EVIDENCE_BUDGET,
        "note": ("carrier pair present with nonfunctional occurrences; the encoding "
                 "scheme is NOT established -- A/B is a reporting convention, not a "
                 "decoded payload"),
    }
    if jt["status"] != "OK":
        out["reason"] = jt.get("reason")
    return out
