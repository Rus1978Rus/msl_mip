#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
unicode_sources_update.py — Unicode source updater for MSL/MIP.

PURPOSE (narrow, per AUTHOR_DECISION 2026-07-07):
  Remove the operational debt of manual Unicode reference updates,
  which both conveyors (invisibles + digits) stumbled over.

WHAT IT DOES:
  1. Downloads the three canonical Unicode files.
  2. Puts them under sources/<UNICODE_VERSION>/ (version pinning).
  3. Compares with the currently pinned version — shows a diff.
  4. Stages the new next to the old. Does NOT apply automatically.

WHAT IT DOES NOT DO (honest boundary):
  - does NOT assign risk to signs. Only fetches references.
  - does NOT decide whether to accept the new version — AUTHOR_DECISION.
  - does NOT validate the noise criterion on a corpus (a separate,
    manual task — the script removes mechanics, not the semantic check).
  - is NOT a sanitiser nor an analyser. Auxiliary tooling only.

DISCIPLINE:
  flag-only for sources: shows WHAT changed; the decision is the
  author's (VERIFY_BEFORE_TRUST applied to the references themselves).

RUN:
  py unicode_sources_update.py            — check and show the diff
  py unicode_sources_update.py --apply    — pin as current
  py unicode_sources_update.py --only dcp — DerivedCoreProperties only
"""

import sys
import os
import re
import json
import hashlib
import urllib.request
from datetime import datetime, timezone

# ── Sources: unicode.org primary, then the official GitHub mirror ──
# Both canonical (the second is the Unicode Consortium repository).
SOURCES = {
    "dcp": {
        "name": "DerivedCoreProperties.txt",
        "purpose": "Default_Ignorable and other properties (invisible signs)",
        "urls": [
            "https://www.unicode.org/Public/UCD/latest/ucd/DerivedCoreProperties.txt",
            "https://raw.githubusercontent.com/unicode-org/unicodetools/main/unicodetools/data/ucd/dev/DerivedCoreProperties.txt",
        ],
    },
    "udata": {
        "name": "UnicodeData.txt",
        "purpose": "category/bidi/name of every codepoint (sign passport)",
        "urls": [
            "https://www.unicode.org/Public/UCD/latest/ucd/UnicodeData.txt",
            "https://raw.githubusercontent.com/unicode-org/unicodetools/main/unicodetools/data/ucd/dev/UnicodeData.txt",
        ],
    },
    "confusables": {
        "name": "confusables.txt",
        "purpose": "UTS#39 skeleton — homoglyphs (similar signs)",
        "urls": [
            "https://www.unicode.org/Public/security/latest/confusables.txt",
            "https://raw.githubusercontent.com/unicode-org/unicodetools/main/unicodetools/data/security/dev/confusables.txt",
        ],
    },
}

ROOT = os.path.dirname(os.path.abspath(__file__))
SOURCES_DIR = os.path.join(ROOT, "sources")
CURRENT_PTR = os.path.join(SOURCES_DIR, "CURRENT_VERSION.json")

UA = "Mozilla/5.0 (MSL-MIP unicode_sources_update; +local tooling)"


def _fetch(urls):
    """Tries the addresses in order. Returns (text, url, idx).
    idx=0 — the primary (unicode.org, stable release);
    idx>0 — a fallback address (e.g. the github /dev/ mirror, which
    may hold a DRAFT of the next version, not a stable release)."""
    last = None
    for idx, u in enumerate(urls):
        try:
            req = urllib.request.Request(u, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                raw = r.read()
            return raw.decode("utf-8", errors="replace"), u, idx
        except Exception as e:
            last = f"{type(e).__name__}: {str(e)[:80]}"
            continue
    raise RuntimeError(f"all addresses unavailable, last error: {last}")


def _sha(text):
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()[:16]


def _parse_version(dcp_text):
    """Extracts the Unicode version from the file header (# DerivedCoreProperties-16.0.0.txt)."""
    m = re.search(r"-(\d+\.\d+\.\d+)\.txt", dcp_text[:500])
    if m:
        return m.group(1)
    m = re.search(r"Version:?\s*(\d+\.\d+\.\d+)", dcp_text[:1000])
    return m.group(1) if m else "UNKNOWN"


def _load_current():
    if os.path.exists(CURRENT_PTR):
        with open(CURRENT_PTR, encoding="utf-8") as f:
            return json.load(f)
    return None


def _di_codepoints(dcp_text):
    """The set of Default_Ignorable_Code_Point codepoints — the invisible guard core."""
    di = set()
    for line in dcp_text.splitlines():
        line = line.split("#", 1)[0].strip()
        if not line or "Default_Ignorable_Code_Point" not in line:
            continue
        rng = line.split(";", 1)[0].strip()
        if ".." in rng:
            a, b = rng.split("..")
            di.update(range(int(a, 16), int(b, 16) + 1))
        else:
            di.add(int(rng, 16))
    return di


def main():
    args = set(sys.argv[1:])
    apply = "--apply" in args
    only = None
    for a in list(args):
        if a == "--only":
            # next token
            idx = sys.argv.index("--only")
            if idx + 1 < len(sys.argv):
                only = sys.argv[idx + 1]

    keys = [only] if only in SOURCES else list(SOURCES.keys())

    print("=" * 60)
    print("UNICODE SOURCES UPDATE — MSL/MIP tooling")
    print("mode:", "APPLY (pin)" if apply else "CHECK (diff only)")
    print("=" * 60)

    os.makedirs(SOURCES_DIR, exist_ok=True)
    current = _load_current()
    cur_ver = current.get("unicode_version") if current else None
    if cur_ver:
        print(f"currently pinned version: {cur_ver}")
    else:
        print("current version: NONE (first download)")

    fetched = {}
    new_version = None
    fallback_used = False
    for k in keys:
        src = SOURCES[k]
        print(f"\n── {src['name']} ({src['purpose']}) ──")
        try:
            text, used, idx = _fetch(src["urls"])
        except Exception as e:
            print(f"  ERROR: {e}")
            continue
        sha = _sha(text)
        host = used.split('/')[2]
        print(f"  downloaded: {len(text):,} chars | sha {sha} | via {host}")
        if idx > 0:
            fallback_used = True
            print(f"  ⚠️ WARNING: the primary is unavailable, taken from a FALLBACK")
            print(f"     address ({host}). It may be a development branch")
            print(f"     (/dev/) with a DRAFT of the next version, NOT a")
            print(f"     stable release. Re-check the version manually.")
        fetched[k] = {"text": text, "sha": sha, "name": src["name"],
                      "source_url": used, "is_fallback": idx > 0}
        if k == "dcp":
            new_version = _parse_version(text)

    if not fetched:
        print("\nnothing downloaded. check the network.")
        return 1

    if new_version:
        print(f"\nUnicode version from the downloaded DerivedCoreProperties: {new_version}")

    # ── DIFF against current ──
    print("\n" + "=" * 60)
    print("COMPARISON WITH CURRENT")
    print("=" * 60)
    changed = False
    if current is None:
        print("no baseline — everything is new (first pin).")
        changed = True
    else:
        old_sha = current.get("files", {})
        for k, info in fetched.items():
            prev = old_sha.get(info["name"], {}).get("sha")
            if prev != info["sha"]:
                changed = True
                print(f"  CHANGED: {info['name']}  {prev} -> {info['sha']}")
            else:
                print(f"  unchanged: {info['name']}")
        if new_version and cur_ver and new_version != cur_ver:
            print(f"  Unicode VERSION: {cur_ver} -> {new_version}")

    # a substantive DI diff (what matters for the invisible guard)
    if "dcp" in fetched:
        new_di = _di_codepoints(fetched["dcp"]["text"])
        print(f"\n  Default_Ignorable codepoints now: {len(new_di)}")
        if current and current.get("di_count"):
            delta = len(new_di) - current["di_count"]
            if delta:
                print(f"  DI codepoint count CHANGE: {delta:+d} "
                      f"(was {current['di_count']})")
                print("  ⚠️ the invisible-guard noise criterion may have changed — "
                      "manual corpus validation required")

    # ── APPLY or stop ──
    if not changed:
        print("\nALL UP TO DATE. no update needed.")
        return 0

    if not apply:
        print("\n" + "=" * 60)
        print("CHANGES FOUND. NOTHING PINNED.")
        print("The script is flag-only: acceptance is the author decision.")
        print("To pin: py unicode_sources_update.py --apply")
        print("=" * 60)
        return 0

    # GUARD: never silently pin a version from a FALLBACK address.
    # The fallback may be a /dev/ branch with a draft — NOT a stable
    # release. Explicit author consent required (VERIFY_BEFORE_TRUST).
    if fallback_used and "--allow-fallback" not in args:
        print("\n" + "=" * 60)
        print("PINNING STOPPED: some files came from a FALLBACK address.")
        print("It may be a development branch (a draft of the next version),")
        print("not a stable Unicode release. Silent pinning is not allowed.")
        print("If you knowingly accept the fallback source:")
        print("  py unicode_sources_update.py --apply --allow-fallback")
        print("=" * 60)
        return 2

    # APPLY: save under sources/<version>/ and update the pointer
    ver = new_version or datetime.now(timezone.utc).strftime("snapshot-%Y%m%d")
    vdir = os.path.join(SOURCES_DIR, ver)
    os.makedirs(vdir, exist_ok=True)
    manifest = {
        "unicode_version": ver,
        "fixed_at_utc": datetime.now(timezone.utc).isoformat(),
        "fetched_from_fallback": fallback_used,
        "di_count": len(_di_codepoints(fetched["dcp"]["text"])) if "dcp" in fetched else None,
        "files": {},
    }
    for k, info in fetched.items():
        path = os.path.join(vdir, info["name"])
        with open(path, "w", encoding="utf-8") as f:
            f.write(info["text"])
        manifest["files"][info["name"]] = {
            "sha": info["sha"],
            "path": os.path.relpath(path, ROOT),
            "source_url": info.get("source_url"),
            "is_fallback": info.get("is_fallback", False),
        }
        print(f"  saved: {os.path.relpath(path, ROOT)}")
    with open(CURRENT_PTR, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"\nPINNED as current: version {ver}")
    if fallback_used:
        print("⚠️ pinned from a FALLBACK source (see the manifest)")
    print(f"pointer: {os.path.relpath(CURRENT_PTR, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
