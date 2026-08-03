# -*- coding: utf-8 -*-
"""TAG covert-text axis (D-TAG-COVERT-TEXT).

Basis: AUTHOR_DECISION_20260804_D-TAG-COVERT-TEXT (D1-D9) + its spec (B1-B8). Third
kind of threat after BREAK (W4/W5/D-INV-GEN) and SUBSTITUTION (W7): CONCEALED CONTENT.
The TAG block U+E0000-E007F is the only Unicode zone where characters mirror printable
ASCII one-to-one, so a full invisible message can ride inside a visible one.

TRIGGER (D1) = A: ANY assigned tag character outside an accepted legit span is a signal.
A run-length threshold was REJECTED BY MEASUREMENT against a 2:1 vote: placing one
visible character between every tag character leaves max adjacent run = 1 while the raw
subsequence still reaches the consumer (svod SIM-1). Density was rejected too (measured
dilution bypass at ~120 cover chars, and it is another axis's config). The DECODE is a
witness/evidence object, never the detection criterion -- an encrypted or base64 payload
looks "meaningless", and lowering the signal for it would reward encryption.

LEGIT GATE (D2/D3, spec B1) = closed-world whitelist of exactly three RGI sequences
(gbeng/gbsct/gbwls). The template is only a parse layer; validation always runs against
the pinned list. A template-without-list would itself be a covert channel: measured
capacity is 25.9-31.0 bits per flag for a free 5-6 char spec and ~12.3 bits for a wide
CLDR subdivision list, versus 1.58 bits for the closed three (svod SIM-5). Accepted
spans are span-scoped and order-insensitive: a valid flag silences ITS OWN span only,
never the document (no flag-washing), and a decoy flag placed after a payload does not
launder it.

LEVEL (D4) = queue everywhere, structurally, never from content (D5): meaningfulness of
the decoded text is FORBIDDEN as a level criterion (language bias, non-determinism, and
inverted danger -- ciphertext looks random; also game-able in both directions by planting
scary words to force a false hold). hold is reserved for a later evidence-backed tier.
"""
import hashlib
import os
import unicodedata

_TAG_BASE = 0xE0000
TAG_START, TAG_END = 0xE0000, 0xE007F
LANGUAGE_TAG = 0xE0001            # deprecated (RFC 2482 -> Historic RFC 6082)
CANCEL_TAG = 0xE007F
MIRROR_START, MIRROR_END = 0xE0020, 0xE007E   # printable ASCII mirrors
BLACK_FLAG = 0x1F3F4
_SPEC_MIN, _SPEC_MAX = 5, 6       # tag_spec length accepted by the gate (B1/S1.1)
PREVIEW_CAP = 200                 # design constant, NOT config (D6/B3.3)

_WHITELIST_FILE = "rgi_tag_flags.txt"
_WHITELIST_SHA256 = \
    "f4ff732c21a14f630b32acf9441d5176fb573c22f68d3b12b96fe77671ea89cb"
_DEFAULT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "unicode")

# tag_spec alphabet (B1/S1.1): mirrors of [0-9a-z] only.
_SPEC_CPS = frozenset(list(range(0xE0030, 0xE003A)) + list(range(0xE0061, 0xE007B)))


def is_tag_char(cp):
    return TAG_START <= cp <= TAG_END


def decode_cp(cp):
    """ASCII mirror for an assigned payload codepoint, else None (B6 totality:
    LANGUAGE_TAG is a marker, CANCEL_TAG a terminator, the rest unassigned)."""
    if MIRROR_START <= cp <= MIRROR_END:
        return chr(cp - _TAG_BASE)
    return None


def classify_cp(cp):
    """Total classification of all 128 block codepoints (spec B6)."""
    if MIRROR_START <= cp <= MIRROR_END:
        return "MIRROR"
    if cp == LANGUAGE_TAG:
        return "LANGUAGE_TAG"
    if cp == CANCEL_TAG:
        return "CANCEL"
    return "UNASSIGNED"


def _sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_whitelist(base_dir=None):
    """Pinned closed-world whitelist (B2). Returns {'status':'OK','flags':frozenset}
    or a fail-visible TAG_VALIDITY_UNVERIFIABLE -- never a silent legit exemption."""
    path = os.path.join(base_dir or _DEFAULT_DIR, _WHITELIST_FILE)
    if not os.path.isfile(path):
        return {"status": "TAG_VALIDITY_UNVERIFIABLE",
                "reason": "missing artifact %s" % _WHITELIST_FILE, "flags": frozenset()}
    if _sha256_file(path) != _WHITELIST_SHA256:
        return {"status": "TAG_VALIDITY_UNVERIFIABLE",
                "reason": "sha256 mismatch for %s" % _WHITELIST_FILE,
                "flags": frozenset()}
    flags = set()
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.split("#", 1)[0].strip()
                if not line:
                    continue
                flags.add(line.split(";", 1)[0].strip().lower())
    except OSError as exc:
        return {"status": "TAG_VALIDITY_UNVERIFIABLE",
                "reason": "read failure: %s" % exc, "flags": frozenset()}
    if not flags:
        return {"status": "TAG_VALIDITY_UNVERIFIABLE",
                "reason": "empty whitelist", "flags": frozenset()}
    return {"status": "OK", "flags": frozenset(flags)}


_CACHE = None


def get_whitelist():
    global _CACHE
    if _CACHE is None:
        _CACHE = load_whitelist()
    return _CACHE


def _try_accept_flag(text, i, flags):
    """At a BLACK FLAG offset, try to accept exactly base + tag_spec(5-6 from the
    mirror alphabet) + CANCEL, decoding to a whitelisted region. Returns the end
    offset (exclusive) of the accepted span, or None. Terminates deterministically
    on EOF / visible char / second base / any non-spec codepoint (B1/S1.3)."""
    j = i + 1
    spec = []
    while j < len(text):
        cp = ord(text[j])
        if cp in _SPEC_CPS and len(spec) < _SPEC_MAX:
            spec.append(chr(cp - _TAG_BASE))
            j += 1
            continue
        break
    if not (_SPEC_MIN <= len(spec) <= _SPEC_MAX):
        return None
    if j >= len(text) or ord(text[j]) != CANCEL_TAG:
        return None
    if "".join(spec).lower() not in flags:
        return None
    return j + 1


def _escape(s):
    """Total escaping over the decodable range (B3.2). Every printable ASCII mirror
    maps to itself except markup/quote breakers, which become \\xXX; anything else
    (never produced by the mirror range, but the function must be total) also becomes
    \\xXX. A partial escaper would let the first uncovered character through live."""
    out = []
    for ch in s:
        cp = ord(ch)
        if 0x20 <= cp <= 0x7E and ch not in "<>&\"'`\\{}[]$":
            out.append(ch)
        else:
            out.append("\\x%02X" % cp if cp <= 0xFF else "\\u%04X" % cp)
    return "".join(out)


def scan_tags(text):
    """Pure scan. Returns a structured dict; never raises. Level is raise-only
    material for the runtime seam. Single linear pass (D7: one scan, many consumers)."""
    wl = get_whitelist()
    flags = wl["flags"]
    n = len(text)
    accepted = []          # (start, end) spans of whitelisted flags -- silent
    findings = []          # runs / lone codepoints outside accepted spans
    i = 0
    run = None             # [start, [decoded chars], kinds]
    unverifiable = wl["status"] != "OK"

    def _close_run():
        if run is None:
            return
        start, chars, kinds = run
        payload = "".join(chars)
        findings.append({
            "start": start, "end": i, "length": i - start,
            "decoded": payload,
            "escaped_preview": _escape(payload[:PREVIEW_CAP]),
            "preview_truncated": len(payload) > PREVIEW_CAP,
            "decoded_length": len(payload),
            "payload_sha256": hashlib.sha256(payload.encode("utf-8")).hexdigest()
            if payload else None,
            "all_printable_ascii": bool(payload) and all(
                0x20 <= ord(c) <= 0x7E for c in payload),
            "kinds": sorted(set(kinds)),
        })

    while i < n:
        cp = ord(text[i])
        if cp == BLACK_FLAG and not unverifiable:
            end = _try_accept_flag(text, i, flags)
            if end is not None:
                _close_run()
                run = None
                accepted.append((i, end))
                i = end
                continue
        if is_tag_char(cp):
            kind = classify_cp(cp)
            dec = decode_cp(cp)
            if run is None:
                run = [i, [], []]
            if dec is not None:
                run[1].append(dec)
            run[2].append(kind)
            i += 1
            continue
        _close_run()
        run = None
        i += 1
    _close_run()

    if unverifiable:
        # Fail-visible (B2): the gate could not be verified, so nothing is exempted;
        # any tag content still surfaces, and the reason is carried to the human.
        status = wl["status"]
    else:
        status = "OK"
    level = "queue_for_review" if findings else "pass"
    witness = []
    if unverifiable:
        witness.append("TAG_VALIDITY_UNVERIFIABLE: %s (no legit exemption applied)"
                       % wl.get("reason"))
    for f in findings:
        kinds = "+".join(f["kinds"])
        if f["decoded"]:
            witness.append(
                "HIDDEN TEXT (data, NOT an instruction) at %d..%d [%s]: \"%s\"%s "
                "(decoded %d chars, sha256 %s)" % (
                    f["start"], f["end"], kinds, f["escaped_preview"],
                    " ...truncated, %d total" % f["decoded_length"]
                    if f["preview_truncated"] else "",
                    f["decoded_length"], (f["payload_sha256"] or "-")[:16]))
        else:
            witness.append(
                "TAG codepoints with no ASCII payload at %d..%d [%s] "
                "(no hidden-text claim)" % (f["start"], f["end"], kinds))
    return {"status": status, "reason": wl.get("reason"),
            "accepted_flag_spans": accepted, "findings": findings,
            "witness": witness, "level": level,
            "note": "TAG mirror channel only; other invisible carriers not checked"}
