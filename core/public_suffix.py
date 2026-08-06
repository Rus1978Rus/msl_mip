"""
public_suffix.py — three-level protection for two lists:
  1. COMPOUND domain suffixes (Public Suffix List, dotted entries only
     — "co.uk", "com.au", "gov.scot" etc.).
  2. SINGLE TLDs (IANA registry, "com", "shop", "xyz" etc.).

Both are needed for correct domain-mimicry detection in dot_matcher.py:
  - compound — so gov.scot/com.au are not flagged as phishing
  - single — so paypal.com.verify.shop IS caught as phishing

PROTECTION LEVELS (in order of decreasing freshness):
  1. Canonical source: https://publicsuffix.org/list/public_suffix_list.dat
     The file itself asks to pull ONLY from that address, not mirrors
     ("Please pull this list from, and only from ..."). So when the
     site is unavailable we do NOT look for alternative URLs — we fall
     to level 2.
  2. Local cache — result of the last successful level-1 fetch,
     saved to disk with a date. Survives temporary site outages OR its
     complete move/disappearance — the system just "freezes" on the
     last good version.
  3. Built-in minimal list — for a first run with no internet at all
     (no network, no cache). Does NOT claim completeness — a practical
     core of the most common compound suffixes, hand-picked from the
     real list (not invented), without rare regional entries such as
     Japanese municipalities.
     

HONESTY: the caller MUST get an explicit signal of which protection
level fired — silent degradation to cache/minimum is not allowed
(same discipline as the WORKING_DRAFT warnings).
"""

from __future__ import annotations

import hashlib
import os
import re
import urllib.request
import urllib.error
from datetime import datetime, timezone

CANONICAL_URL = "https://publicsuffix.org/list/public_suffix_list.dat"
FETCH_TIMEOUT_SECONDS = 3

# GATE_MUST_BE_HERMETIC (2026-07-12): when MSL_MIP_HERMETIC_TLD is set (to
# anything other than ""/"0"/"false"), load_compound_suffixes() and
# load_single_tlds() SKIP the network and the on-disk cache entirely and
# return the in-repo EMBEDDED fallbacks — a deterministic, offline, pinned
# set. This exists so gates never depend on an external source: a live
# registry is for the RUNTIME, a pinned one for GATES. A gate that green-
# lights on a network hint is silent degradation, not test signal. Default
# (env unset) is unchanged: live fetch -> cache -> embedded, as production.
_HERMETIC_ENV = "MSL_MIP_HERMETIC_TLD"

# VENDORED SNAPSHOTS (2026-08-07). The registries now ship IN THE REPOSITORY and
# are the DEFAULT source; the network is reached only when explicitly allowed.
# The old default (fetch first, fall back to a ~163-entry embedded list) failed
# badly in the environment that needs this most: an air-gapped install silently
# ran on the embedded remnant of the registry, and — worse — reported itself as
# NOT degraded, because the health check looked only at the entry COUNT (163 is
# above the threshold) and threw the SOURCE string away. Whether a verdict rests
# on 1438 official TLDs or on 163 hand-picked ones is exactly the kind of fact
# this project refuses to hide, so the source now travels with the data.
# Set MSL_MIP_ALLOW_NETWORK=1 to re-enable live fetching (it then takes
# precedence over the snapshot, as before, and the cache still works).
_ALLOW_NETWORK_ENV = "MSL_MIP_ALLOW_NETWORK"
_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                         "data", "net")
_VENDORED_TLD_FILE = os.path.join(_DATA_DIR, "tlds-alpha-by-domain.txt")
_VENDORED_PSL_FILE = os.path.join(_DATA_DIR, "public_suffix_list.dat")
_VENDORED_TLD_SHA256 = \
    "932b5f31c5ef487ff7c4e70ef7d159a2ddc41e5d827d60a5fce9320d806c7b6d"
_VENDORED_PSL_SHA256 = \
    "084a5674d77c1d14900b16da5fc8afee9765af2f00a638552a8c7aa18f44ae81"

# Source strings that mean "this is a COMPLETE registry" (live, cached, or the
# vendored snapshot). Anything else is a stand-in and must be reported degraded.
FULL_REGISTRY_SOURCES = ("LIVE_FETCH", "VENDORED", "CACHE_FROM_")


def _hermetic_tlds() -> bool:
    return os.environ.get(_HERMETIC_ENV, "").strip().lower() not in ("", "0", "false", "no", "off")


def _network_allowed() -> bool:
    return os.environ.get(_ALLOW_NETWORK_ENV, "").strip().lower() \
        not in ("", "0", "false", "no", "off")


def is_full_registry(source: str) -> bool:
    """True when `source` denotes a complete registry rather than a stand-in.
    Used by the sequence layer to decide the DEGRADED flag by provenance
    instead of by entry count."""
    return bool(source) and any(source.startswith(p) for p in FULL_REGISTRY_SOURCES)


def _sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _read_vendored(path: str, expected_sha: str):
    """Vendored registry text, or None when the file is absent or its hash does
    not match the pin. A tampered snapshot must NOT be used silently — the
    caller falls through to the next level and the source string records it."""
    if not os.path.isfile(path):
        return None
    try:
        if _sha256_file(path) != expected_sha:
            return None
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except OSError:
        return None


_CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "cache")
_CACHE_FILE = os.path.join(_CACHE_DIR, "public_suffix_compound_cache.txt")

# FIXED (found in code review MINOR01_FIX, 2026-06-29, GPT-5.5):
# "single TLDs are already covered by a separate list in dot_
# matcher.py" — turned out FALSE in practice: that list (_TLDS)
# was tiny (20 entries), hand-made, and MISSED many actually
# active TLDs (.shop, .xyz, .site, .online, .top and hundreds
# more). As a result domain_mimicry_risk (which now depends on
# is_domain_like) produced false negatives on real phishing
# patterns like "paypal.com.verify.shop". The fix — the same
# three-level principle for single TLDs, source — the official
# IANA registry (https://data.iana.org/TLD/tlds-alpha-by-
# domain.txt), no less authoritative than the Public Suffix List
# itself (the PSL is partly based on this same registry).
IANA_TLD_URL = "https://data.iana.org/TLD/tlds-alpha-by-domain.txt"
_TLD_CACHE_FILE = os.path.join(_CACHE_DIR, "iana_single_tld_cache.txt")

# Level 3: built-in minimum. Every entry actually exists in the
# Public Suffix List (verified by direct download of the canonical
# 2026-06-29) — not guesses but a deliberately narrowed subset:
# the most common compound suffixes without rare regional entries
# (Japanese municipalities, Italian provinces etc.).
EMBEDDED_FALLBACK = frozenset({
    # United Kingdom
    "co.uk", "org.uk", "gov.uk", "ac.uk", "ltd.uk", "plc.uk", "sch.uk", "net.uk", "me.uk",
    # Australia
    "com.au", "net.au", "org.au", "edu.au", "gov.au", "asn.au", "id.au",
    # Brazil
    "com.br", "net.br", "org.br", "gov.br", "edu.br",
    # China
    "com.cn", "net.cn", "org.cn", "gov.cn", "edu.cn", "ac.cn",
    # Mexico
    "com.mx", "gob.mx", "edu.mx", "net.mx", "org.mx",
    # New Zealand
    "co.nz", "net.nz", "org.nz", "govt.nz",
    # India
    "co.in", "net.in", "org.in", "gov.in", "edu.in", "ac.in",
    # Turkey
    "com.tr", "gov.tr", "edu.tr",
    # Japan (organisational types only, no geography)
    "co.jp", "or.jp", "ne.jp", "ac.jp", "go.jp", "gr.jp", "ed.jp", "lg.jp", "ad.jp",
    # Scotland/Wales — found in code review as a real counter-example
    "gov.scot", "gov.wales",
    # Singapore
    "com.sg", "gov.sg", "edu.sg", "net.sg", "org.sg",
    # South Africa
    "co.za", "org.za", "gov.za", "net.za",
    # Hong Kong
    "com.hk", "net.hk", "org.hk", "edu.hk", "gov.hk",
    # South Korea
    "co.kr", "or.kr", "go.kr", "ac.kr", "ne.kr",
    # Argentina
    "com.ar", "gob.ar", "gov.ar", "net.ar", "org.ar",
    # Colombia
    "com.co", "edu.co", "gov.co", "net.co", "org.co",
    # Ukraine
    "com.ua", "gov.ua", "edu.ua", "net.ua", "org.ua",
    # Poland
    "com.pl", "gov.pl", "edu.pl", "net.pl", "org.pl",
    # Indonesia
    "co.id", "go.id", "or.id", "ac.id", "web.id",
    # Vietnam
    "com.vn", "gov.vn", "edu.vn", "net.vn", "org.vn",
    # Philippines
    "com.ph", "gov.ph", "edu.ph", "net.ph", "org.ph",
    # Malaysia
    "com.my", "gov.my", "edu.my", "net.my", "org.my",
    # Thailand
    "co.th", "go.th", "ac.th", "net.th", "org.th",
    # Israel
    "co.il", "gov.il", "ac.il", "net.il", "org.il",
    # Ireland
    "gov.ie",
})

# Built-in minimum of SINGLE TLDs (level 3 for the IANA root zone).
# Every entry actually exists in the current IANA registry
# (verified by direct lookup, 2026-06-29). NOT a complete list
# (~1437 TLDs in the registry) — a practical core of gTLDs, ccTLDs
# and frequently abused "fresh" zones (.shop/.xyz/.site/.online/
# .top etc., especially relevant for phishing detection because
# cheap unregulated domains are used for fakes more often).
EMBEDDED_TLD_FALLBACK = frozenset({
    # the original hand list (kept for compatibility)
    "com", "org", "net", "ru", "io", "dev", "app", "info", "biz",
    "co", "uk", "de", "fr", "ua", "by", "kz", "gov", "edu", "jp", "cn",
    # frequently abused "fresh" gTLDs in phishing
    "shop", "xyz", "site", "online", "top", "club", "store", "tech",
    "win", "click", "link", "loan", "work", "live", "world", "space",
    "vip", "icu", "buzz", "rest", "fun", "pro", "name", "mobi",
    "tk", "ml", "ga", "cf", "gq",
    # major ccTLDs/gTLDs not covered by the original list
    "us", "ca", "au", "nz", "in", "br", "mx", "es", "it", "nl", "se",
    "no", "fi", "dk", "pl", "ch", "at", "be", "pt", "gr", "cz", "hu",
    "ro", "bg", "tr", "il", "sa", "ae", "eg", "za", "ng", "ke", "gh",
    "th", "vn", "id", "ph", "my", "sg", "hk", "tw", "kr", "pk", "bd",
    "lk", "np", "ir", "iq", "sy", "jo", "lb", "kw", "qa", "bh", "om",
    "ye", "ma", "tn", "ly", "sd", "et", "ug", "tz", "zm", "zw", "mw",
    "mz", "ao", "cm", "ci", "sn", "bf", "ne", "gn", "rw",
    "ec", "pe", "ve", "cl", "py", "uy", "bo", "do", "gt",
    "hn", "ni", "pa", "cr", "cu", "ht",
    # infrastructure/special
    "asia", "eu", "int", "arpa", "cat", "jobs", "mobi", "museum",
    "travel", "coop", "aero", "post",
    # flagged by reviewers as missing, phishing-relevant
    "zip", "mov", "page", "email", "cloud", "website", "support",
    "services", "finance", "bank", "secure", "download", "review",
})


def _parse_single_tld_entries(raw_text: str) -> frozenset:
    """Extracts single TLDs from IANA tlds-alpha-by-domain.txt.
    Format: one TLD per line (UPPERCASE), the first line is a
    "# Version ... Last Updated ..." comment."""
    result = set()
    for line in raw_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        result.add(line.lower())
    return frozenset(result)


def _fetch_single_tlds_from_iana() -> frozenset:
    req = urllib.request.Request(IANA_TLD_URL, headers={"User-Agent": "MSL-MIP/1.0"})
    with urllib.request.urlopen(req, timeout=FETCH_TIMEOUT_SECONDS) as resp:
        raw = resp.read().decode("utf-8", errors="replace")
    return _parse_single_tld_entries(raw)


def _save_tld_cache(entries: frozenset) -> None:
    os.makedirs(_CACHE_DIR, exist_ok=True)
    with open(_TLD_CACHE_FILE, "w", encoding="utf-8") as f:
        f.write(f"# CACHED: {datetime.now(timezone.utc).isoformat()}\n")
        for e in sorted(entries):
            f.write(e + "\n")


def _load_tld_cache():
    if not os.path.exists(_TLD_CACHE_FILE):
        return None, None
    with open(_TLD_CACHE_FILE, encoding="utf-8") as f:
        lines = f.readlines()
    if not lines or not lines[0].startswith("# CACHED:"):
        return None, None
    cached_at = lines[0].split("CACHED:", 1)[1].strip()
    entries = frozenset(
        line.strip().lower() for line in lines[1:]
        if line.strip() and not line.startswith("#")
    )
    return entries, cached_at


def load_single_tlds():
    """Same as load_compound_suffixes() but for single TLDs from the
    IANA root zone. Same discipline — three levels, explicit source.
    returned to the caller."""
    if _hermetic_tlds():
        return EMBEDDED_TLD_FALLBACK, "EMBEDDED_HERMETIC"
    if _network_allowed():
        try:
            entries = _fetch_single_tlds_from_iana()
            if entries:
                _save_tld_cache(entries)
                return entries, "LIVE_FETCH"
        except (urllib.error.URLError, TimeoutError, OSError, ValueError):
            pass
        cached_entries, cached_at = _load_tld_cache()
        if cached_entries:
            return cached_entries, f"CACHE_FROM_{cached_at}"

    raw = _read_vendored(_VENDORED_TLD_FILE, _VENDORED_TLD_SHA256)
    if raw:
        entries = frozenset(
            line.strip().lower() for line in raw.splitlines()
            if line.strip() and not line.startswith("#"))
        if entries:
            return entries, "VENDORED"

    return EMBEDDED_TLD_FALLBACK, "EMBEDDED_FALLBACK"


def _parse_compound_entries(raw_text: str) -> frozenset:
    """Extracts only COMPOUND (dotted) entries from the PSL text,
    skipping comments (//), empty lines and wildcard rules
    (*.xx / !exception — a rare case, not handled separately;
    a known, deliberate parser limitation)."""
    result = set()
    for line in raw_text.splitlines():
        line = line.strip()
        if not line or line.startswith("//") or "*" in line or line.startswith("!"):
            continue
        if "." in line:
            result.add(line.lower())
    return frozenset(result)


def _fetch_from_canonical_source() -> frozenset:
    """Level 1. Returns a frozenset or raises if the download failed
    (the caller falls through to level 2)."""
    req = urllib.request.Request(CANONICAL_URL, headers={"User-Agent": "MSL-MIP/1.0"})
    with urllib.request.urlopen(req, timeout=FETCH_TIMEOUT_SECONDS) as resp:
        raw = resp.read().decode("utf-8", errors="replace")
    return _parse_compound_entries(raw)


def _save_to_cache(entries: frozenset) -> None:
    os.makedirs(_CACHE_DIR, exist_ok=True)
    with open(_CACHE_FILE, "w", encoding="utf-8") as f:
        f.write(f"# CACHED: {datetime.now(timezone.utc).isoformat()}\n")
        for e in sorted(entries):
            f.write(e + "\n")


def _load_from_cache():
    """Level 2. Returns (frozenset, cache_date) or (None, None)
    when there is no cache."""
    if not os.path.exists(_CACHE_FILE):
        return None, None
    with open(_CACHE_FILE, encoding="utf-8") as f:
        lines = f.readlines()
    if not lines or not lines[0].startswith("# CACHED:"):
        return None, None
    cached_at = lines[0].split("CACHED:", 1)[1].strip()
    entries = frozenset(
        line.strip().lower() for line in lines[1:]
        if line.strip() and not line.startswith("#")
    )
    return entries, cached_at


def load_compound_suffixes():
    """Main entry point. Returns (frozenset, source: str) where
    source is one of 'LIVE_FETCH' / 'CACHE_FROM_<date>' /
    'EMBEDDED_FALLBACK'. The caller MUST surface the source to the
    user when it is not LIVE_FETCH (see module docstring,
    the HONESTY section)."""
    if _hermetic_tlds():
        return EMBEDDED_FALLBACK, "EMBEDDED_HERMETIC"
    if _network_allowed():
        try:
            entries = _fetch_from_canonical_source()
            if entries:
                _save_to_cache(entries)
                return entries, "LIVE_FETCH"
        except (urllib.error.URLError, TimeoutError, OSError, ValueError):
            pass
        cached_entries, cached_at = _load_from_cache()
        if cached_entries:
            return cached_entries, f"CACHE_FROM_{cached_at}"

    raw = _read_vendored(_VENDORED_PSL_FILE, _VENDORED_PSL_SHA256)
    if raw:
        entries = _parse_compound_entries(raw)
        if entries:
            return entries, "VENDORED"

    return EMBEDDED_FALLBACK, "EMBEDDED_FALLBACK"
