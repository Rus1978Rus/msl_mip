# -*- coding: utf-8 -*-
"""Composite registry of SANCTIONED variation sequences (D-VS-STEGO D4, spec B2/B3).

Unicode sanctions exactly three kinds of variation sequence, and a selector means
nothing outside them:
  StandardizedVariants.txt        (UCD 16.0.0)   1306 pairs
  emoji-variation-sequences.txt   (UCD 16.0.0)    742 pairs (371 bases x FE0E/FE0F)
  IVD_Sequences.txt               (release-dated) 29437 pairs, 15290 bases
The registry answers ONE question -- is this exact (base, selector) pair registered --
which is what the W4 silence predicate needs. Structural shape ("CJK + anything in the
E0100 block", "emoji-looking base + FE0F") was rejected by measurement: it leaves 7.907
of 8.00 bits (98.8%) of the covert channel inside "legitimacy", and it was the cause of
the measured silent kilobyte channel.

IVD is pinned by RELEASE DATE, not by UCD version: its releases are dated and immutable
and are published independently of the UCD (2022-09-13, 2025-07-14, 2026-07-31,
2026-08-03 ...). There is no "IVD for UCD 16.0.0" (svod SIM-D). Pin here = 2022-09-13,
the snapshot contemporary with our UCD 16.0.0 pin; later registrations therefore read as
UNREGISTERED until an authored re-pin (residual RESIDUAL_POST_PIN).

Fail-visible (B3): a missing or tampered file yields status UNVERIFIABLE. Neither
"assume valid" nor "assume invalid and hold everything" is permitted; the caller keeps
applying exemptions (else the emoji flood D3 killed returns) but MUST surface the
unverifiable notice, so the pass is never silent.
"""
import hashlib
import os

IVD_RELEASE = "2022-09-13"          # pinned by DATE (B2), independent of the UCD pin

PINNED_SHA256 = {
    "StandardizedVariants.txt":
        "36e799b2c5d902af094b4dd2cb60622bffc079824bfd0bf62e3a636d698b3fb5",
    "emoji-variation-sequences.txt":
        "71d93ec015011371a027ba2bc0a63155d381c6e0b94a586c1a88a49400cd6864",
    "IVD_Sequences.txt":
        "e6168c2ed8e0834d3eccb8a6d43aad004c97c8216e237101f1c2e8347be2b523",
}

_DEFAULT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "unicode")


def _sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _parse_pairs(path):
    """All three files share the shape '<base> <selector> ; <data> # comment'."""
    pairs = set()
    with open(path, "r", encoding="utf-8-sig") as f:
        for line in f:
            line = line.split("#", 1)[0].strip()
            if not line:
                continue
            fields = line.split(";")[0].strip().split()
            if len(fields) < 2:
                continue
            try:
                pairs.add((int(fields[0], 16), int(fields[1], 16)))
            except ValueError:
                continue
    return pairs


def load_registry(base_dir=None):
    """Verify pins, parse, and merge. Returns {'status': 'OK', 'pairs': frozenset, ...}
    or {'status': 'UNVERIFIABLE', 'reason': ..., 'pairs': frozenset()} -- never raises."""
    base = base_dir or _DEFAULT_DIR
    per_file = {}
    for fname, want in PINNED_SHA256.items():
        path = os.path.join(base, fname)
        if not os.path.isfile(path):
            return {"status": "UNVERIFIABLE", "reason": "missing artifact %s" % fname,
                    "pairs": frozenset(), "counts": {}}
        if _sha256_file(path) != want:
            return {"status": "UNVERIFIABLE", "reason": "sha256 mismatch for %s" % fname,
                    "pairs": frozenset(), "counts": {}}
        try:
            per_file[fname] = _parse_pairs(path)
        except OSError as exc:
            return {"status": "UNVERIFIABLE", "reason": "read failure: %s" % exc,
                    "pairs": frozenset(), "counts": {}}
    merged = set()
    for pairs in per_file.values():
        merged |= pairs
    return {
        "status": "OK",
        "pairs": frozenset(merged),
        "counts": {k: len(v) for k, v in per_file.items()},
        "ivd_release": IVD_RELEASE,
    }


_CACHE = None


def get_registry():
    global _CACHE
    if _CACHE is None:
        _CACHE = load_registry()
    return _CACHE


def is_registered(base_cp, selector_cp):
    """Exact pair membership. Under an UNVERIFIABLE registry this returns True for the
    shapes the old approximation trusted, so the caller does not flood -- but the caller
    is required to surface the unverifiable status alongside (B3, no silent pass)."""
    reg = get_registry()
    if reg["status"] != "OK":
        return None                      # caller decides, with a visible notice
    return (base_cp, selector_cp) in reg["pairs"]
