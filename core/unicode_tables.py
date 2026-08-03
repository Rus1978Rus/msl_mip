# -*- coding: utf-8 -*-
"""Pinned Unicode data tables for the W7 visible-confusable axis.

Basis: AUTHOR_DECISION_20260804_D-W7-CONFUSABLE (D5) + SPEC_20260804_W7_BLOCKERS_B1-B8
(S3.1-S3.3). Three repo artifacts in data/unicode/ (confusables.txt UTS#39 16.0.0,
Scripts.txt + ScriptExtensions.txt UCD 16.0.0) are verified against pinned sha256 AND
the running interpreter's unicodedata.unidata_version at load time. Any mismatch =>
the loader returns a structured CONFUSABLE_AXIS_UNVERIFIABLE status (fail-visible,
S3.2): the axis must stay OFF, carded/semantic paths are untouched, and NO silent
fallback to handcrafted mappings is allowed (V-OTHER-3). Tables are never fetched at
runtime (S6.2); updating them is a separate author decision (B6).

D6: four disputed source codepoints are excluded from the ACTIVE policy map but kept
in the FULL data map (data preserved, active severity disabled). The official UTS#39
prototypes differ slightly from the Vakhter nursery claims (U+0561 -> 'w' not 'a';
U+03B7 -> 'n'+U+0329): deferral is keyed by SOURCE codepoint, so the difference does
not matter here; gate_w7_tables_pin.py asserts full-minus-active == exactly these 4.
"""
import bisect
import hashlib
import os
import unicodedata

PINNED_UNIDATA_VERSION = "16.0.0"

# sha256 of the pinned artifacts (see data/unicode/PIN_MANIFEST.md; B3/S3.1).
PINNED_SHA256 = {
    "confusables.txt":
        "95bd0aad6dced5ebc63436f459c06ab21a8d107cd842fb57f5c3a1e91bca8611",
    "Scripts.txt":
        "9e88f0a677df47311106340be8ede2ecdacd9c1c931831218d2be6d5508e0039",
    "ScriptExtensions.txt":
        "049117ce26b9769fe2749b06eef51a50a89faef4a97764dd2d81daa715980700",
}

# D6 deferred sources: CYRILLIC SMALL OMEGA, GREEK SMALL ETA, ARMENIAN AYB, ARMENIAN SEH.
DEFERRED_SOURCES = frozenset((0x0461, 0x03B7, 0x0561, 0x057D))

_DEFAULT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "unicode")


def _sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _parse_cp_field(field):
    """'0061 0329' -> 'a' + chr(0x329). Single-cp fields are the common case."""
    return "".join(chr(int(tok, 16)) for tok in field.split())


def _parse_confusables(path):
    """confusables.txt: 'XXXX ; YYYY [ZZZZ..] ; MA # ...' -> {source_cp: prototype_str}.
    Source is always a single codepoint in the published table."""
    out = {}
    with open(path, "r", encoding="utf-8-sig") as f:
        for line in f:
            line = line.split("#", 1)[0].strip()
            if not line:
                continue
            parts = [p.strip() for p in line.split(";")]
            if len(parts) < 3 or parts[2] != "MA":
                continue
            out[int(parts[0], 16)] = _parse_cp_field(parts[1])
    return out


def _parse_ranged_property(path):
    """Scripts.txt / ScriptExtensions.txt: 'XXXX[..YYYY] ; Value(s) # ...' ->
    (sorted starts, [(start, end, value)]). Value is a str for Scripts (one name)
    and a tuple of short codes for ScriptExtensions (several)."""
    records = []
    with open(path, "r", encoding="utf-8-sig") as f:
        for line in f:
            line = line.split("#", 1)[0].strip()
            if not line:
                continue
            rng, _, val = line.partition(";")
            rng = rng.strip()
            vals = val.strip().split()
            if not rng or not vals:
                continue
            if ".." in rng:
                lo, hi = rng.split("..")
                start, end = int(lo, 16), int(hi, 16)
            else:
                start = end = int(rng, 16)
            records.append((start, end, vals[0] if len(vals) == 1 else tuple(vals)))
    records.sort(key=lambda r: r[0])
    return [r[0] for r in records], records


def _lookup_range(starts, records, cp, default):
    i = bisect.bisect_right(starts, cp) - 1
    if i >= 0:
        start, end, value = records[i]
        if start <= cp <= end:
            return value
    return default


def load_tables(base_dir=None):
    """Verify pins and parse all three tables. Returns {'status': 'OK', ...} or
    {'status': 'CONFUSABLE_AXIS_UNVERIFIABLE', 'reason': ...} (fail-visible, S3.2).
    Never raises on data problems."""
    base = base_dir or _DEFAULT_DIR
    if unicodedata.unidata_version != PINNED_UNIDATA_VERSION:
        return {"status": "CONFUSABLE_AXIS_UNVERIFIABLE",
                "reason": "unidata_version %s != pinned %s" % (
                    unicodedata.unidata_version, PINNED_UNIDATA_VERSION)}
    for fname, want in PINNED_SHA256.items():
        path = os.path.join(base, fname)
        if not os.path.isfile(path):
            return {"status": "CONFUSABLE_AXIS_UNVERIFIABLE",
                    "reason": "missing artifact %s" % fname}
        got = _sha256_file(path)
        if got != want:
            return {"status": "CONFUSABLE_AXIS_UNVERIFIABLE",
                    "reason": "sha256 mismatch for %s" % fname}
    try:
        conf = _parse_confusables(os.path.join(base, "confusables.txt"))
        sc_starts, sc_records = _parse_ranged_property(os.path.join(base, "Scripts.txt"))
        se_starts, se_records = _parse_ranged_property(
            os.path.join(base, "ScriptExtensions.txt"))
    except (ValueError, OSError) as exc:
        return {"status": "CONFUSABLE_AXIS_UNVERIFIABLE",
                "reason": "parse failure: %s" % exc}
    active = {cp: proto for cp, proto in conf.items() if cp not in DEFERRED_SOURCES}
    return {
        "status": "OK",
        "confusables_full": conf,
        "confusables_active": active,
        "scripts": (sc_starts, sc_records),
        "script_extensions": (se_starts, se_records),
    }


def script_of(tables, cp):
    """Script property name for a codepoint ('Latin', 'Cyrillic', 'Common', ...).
    Codepoints outside every range are 'Unknown' per UAX#24."""
    starts, records = tables["scripts"]
    return _lookup_range(starts, records, cp, "Unknown")


def script_extensions_of(tables, cp):
    """Tuple of short script codes for cps used across several scripts (UAX#24
    Script_Extensions), or None when the file has no entry (extensions == script)."""
    starts, records = tables["script_extensions"]
    val = _lookup_range(starts, records, cp, None)
    if val is None:
        return None
    return val if isinstance(val, tuple) else (val,)


_CACHE = None


def get_tables():
    """Lazy singleton over load_tables() with the default repo data dir."""
    global _CACHE
    if _CACHE is None:
        _CACHE = load_tables()
    return _CACHE
