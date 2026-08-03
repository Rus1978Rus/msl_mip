# -*- coding: utf-8 -*-
"""W7 visible-confusable class axis (VISIBLE_CONFUSABLE_RELATION).

Basis: AUTHOR_DECISION_20260804_D-W7-CONFUSABLE (D1-D8) + SPEC_20260804_W7_BLOCKERS
(S1-S8). One CLASS axis (two-tier, ARCH_DECISION_TWO_TIER): the mixed-script +
UTS#39-skeleton mechanism lives INSIDE this card-governed axis, entering via the
pinned tables of core/unicode_tables.py (HOMOGLYPH_VIA_CARD_ONLY). Witness frame:
the axis only reports and RAISES effective_action at the runtime seam; it never
lowers a verdict and never rewrites the input.

Host candidates (S1.1): any maximal token whose form passes the existing
sequence_engine._looks_like_domain recognizer (measured Unicode-aware), position-
independent -- prose, URL, or either side of '@' (S1.2: the AT card already
escalates the A@B userinfo trick; this axis adds the confusable signal on top).
ACE labels are punycode-decoded BEFORE detection (S2.1); a broken ACE label is a
fail-visible UNVERIFIABLE_ACE witness, never a silent skip (S2.2).

Trigger (D2, tier 1 -> queue): inside ONE label, after Common/Inherited neutrality
and the UTS#39 5.2 CJK exemptions,
  T1 mixed-script: Latin present AND >=1 char of another explicit script whose
     codepoint is in the ACTIVE confusable map; or
  T2 same-script lookalike: >=1 non-ASCII codepoint whose ACTIVE prototype is pure
     ASCII AND the label also contains ASCII alphanumerics (covers Roman numerals /
     fullwidth letters, which are Script=Latin and invisible to T1).
Tier 2 (D3 -> hold): caller-supplied protected target (EXACT_LABEL, P5) whose
UTS#39 skeleton equals the label's skeleton while the raw label differs, with >=1
ACTIVE confusable present. This is the only hold source and the only whole-script
catcher (R1). Deferred sources (D6) are absent from the ACTIVE map, so they
neither trigger nor hold (marker cells R2).

Separator lookalikes (D4/S4.1): fullwidth/ideographic dots in a domain-form token
emit a SEPARATOR_LOOKALIKE event BEFORE canonicalisation is used for recognition
(detect -> event -> canonicalise); level queue, hold on protected-label collision.

DEGRADED registry policy (W5 parity, D5-W5): witness records are always computed,
but the axis level stays "pass" under a degraded TLD registry -- the alphabetic
fallback would accept prose-shaped tokens and false-escalate.
"""
from functools import lru_cache
import unicodedata

import unicode_tables as _ut

_SEP_LOOKALIKES = frozenset((0x3002, 0xFF0E, 0xFF61))  # ideographic / fullwidth / halfwidth stop
_NEUTRAL_SCRIPTS = frozenset(("Common", "Inherited", "Unknown"))
# UTS#39 5.2 Highly Restrictive: Latin + these CJK recommended-script combinations
# are legitimate writing practice inside one label; the exemption applies only when
# at least one actual CJK script is present (Latin+Greek etc. stays covered).
_CJK_COMBOS = (
    frozenset(("Latin", "Han", "Hiragana", "Katakana")),
    frozenset(("Latin", "Han", "Bopomofo")),
    frozenset(("Latin", "Han", "Hangul")),
)
_CJK_CORE = frozenset(("Han", "Hiragana", "Katakana", "Bopomofo", "Hangul"))
_WRAPPERS = "()[]{}<>\"'`,;:!?"
_SCHEMES = ("http://", "https://", "ftp://", "ftps://")
_MAX_RECORDS = 32          # no silent cap: overflow sets "truncated" (B8 discipline)

_SEVERITY = {"pass": 0, "queue_for_review": 1, "hold_pending_review": 2}


def _worse(a, b):
    return a if _SEVERITY[a] >= _SEVERITY[b] else b


def _skeleton(s, full_map):
    """UTS#39 skeleton: NFD -> map every cp through the FULL confusables table ->
    NFD again. Comparison-internal form only (never displayed/stored as text)."""
    nfd = unicodedata.normalize("NFD", s)
    mapped = "".join(full_map.get(ord(ch), ch) for ch in nfd)
    return unicodedata.normalize("NFD", mapped)


def _reveal(label):
    """B7 witness render: non-ASCII codepoints expanded to <U+XXXX NAME> so the
    'look with your eyes' channel is not empty for true homoglyphs."""
    out = []
    for ch in label:
        cp = ord(ch)
        if cp < 0x80:
            out.append(ch)
        else:
            out.append("<U+%04X %s>" % (cp, unicodedata.name(ch, "?")))
    return "".join(out)


def _ace_form(label):
    """xn-- form for the witness line (RFC 3492); ASCII labels pass through."""
    try:
        if all(ord(ch) < 0x80 for ch in label):
            return label
        return "xn--" + label.encode("punycode").decode("ascii")
    except UnicodeError:
        return "?"


def _label_scripts(label, tables):
    scripts = set()
    for ch in label:
        sc = _ut.script_of(tables, ord(ch))
        if sc not in _NEUTRAL_SCRIPTS:
            scripts.add(sc)
    return scripts


def _cjk_exempt(scripts):
    if not (scripts & _CJK_CORE):
        return False
    return any(scripts <= combo for combo in _CJK_COMBOS)


def _candidates(text):
    """Whitespace tokens -> strip ASCII wrappers + scheme -> split on '@' (S1.2).
    Cheap prefilter: a candidate must contain a dot or a dot-lookalike."""
    seen = set()
    for chunk in text.split():
        chunk = chunk.strip(_WRAPPERS)
        low = chunk.lower()
        for scheme in _SCHEMES:
            if low.startswith(scheme):
                chunk = chunk[len(scheme):]
                break
        chunk = chunk.strip(_WRAPPERS)
        for part in chunk.split("@"):
            part = part.strip(_WRAPPERS).rstrip(".")
            if not part or part in seen:
                continue
            if "." not in part and not any(ord(c) in _SEP_LOOKALIKES for c in part):
                continue
            seen.add(part)
            yield part


def scan_confusables(text, tld_set, degraded, protected_targets=None):
    """Pure scan. Returns a structured dict; never raises on data problems.
    Level is raise-only material for the runtime seam (pass/queue/hold)."""
    tables = _ut.get_tables()
    if tables["status"] != "OK":
        # Fail-visible (S3.2): axis OFF, reason surfaced, no fallback.
        return {"status": tables["status"], "reason": tables.get("reason"),
                "records": [], "separator_events": [], "ace_failures": [],
                "witness": [], "level": "pass", "truncated": False}
    import sequence_engine as _se        # lazy: runtime puts sequence/ on sys.path

    full = tables["confusables_full"]
    active = tables["confusables_active"]
    targets = frozenset(t.lower() for t in protected_targets) if protected_targets \
        else frozenset()
    skel = lru_cache(maxsize=1024)(lambda s: _skeleton(s, full))
    target_skels = {t: skel(t) for t in targets}

    records, sep_events, ace_failures, witness = [], [], [], []
    level = "pass"
    truncated = False

    for token in _candidates(text):
        canon = _se._canon_domain_seps(token)
        if not _se._looks_like_domain(canon, tld_set, degraded):
            continue
        # --- separator axis (D4): event BEFORE the canonical form is used ---
        lookalikes = [(i, ord(ch)) for i, ch in enumerate(token)
                      if ord(ch) in _SEP_LOOKALIKES]
        host = _se._domain_prefix(canon)
        labels = [l for l in host.strip(".").split(".") if l]
        if lookalikes:
            ev_level = "queue_for_review"
            if targets and any(l.lower() in targets for l in labels):
                ev_level = "hold_pending_review"
            sep_events.append({
                "token": token, "lookalikes": lookalikes, "canonical": host,
                "level": ev_level})
            witness.append("separator lookalike in '%s': %s -> canonical '%s'" % (
                _reveal(token),
                ", ".join("<U+%04X %s>@%d" % (cp, unicodedata.name(chr(cp), "?"), i)
                          for i, cp in lookalikes),
                host))
            level = _worse(level, ev_level)
        # --- per-label letter-confusable analysis (D2/D3) ---
        for label in labels:
            uni = label
            if label.lower().startswith("xn--"):
                try:
                    uni = label[4:].encode("ascii").decode("punycode")
                except (UnicodeError, ValueError):
                    ace_failures.append({"token": token, "label": label})
                    witness.append(
                        "UNVERIFIABLE_ACE: label '%s' in '%s' failed punycode decode"
                        % (label, _reveal(token)))
                    continue
            low = uni.lower()
            active_cps = [ord(ch) for ch in low if ord(ch) in active]
            if not active_cps:
                continue                      # no active confusable at all
            scripts = _label_scripts(low, tables)
            exempt = _cjk_exempt(scripts)
            t1 = (not exempt) and "Latin" in scripts and any(
                _ut.script_of(tables, cp) not in _NEUTRAL_SCRIPTS
                and _ut.script_of(tables, cp) != "Latin" for cp in active_cps)
            t2 = (not exempt) and any(
                ord(ch) >= 0x80 and ord(ch) in active
                and all(ord(p) < 0x80 for p in active[ord(ch)])
                for ch in low) and any(ch.isalnum() and ord(ch) < 0x80 for ch in low)
            collision = None
            if targets:
                sk = skel(low)
                for t, tsk in target_skels.items():
                    if sk == tsk and low != t:
                        collision = t
                        break
            if not (t1 or t2 or collision):
                continue
            kind = "PROTECTED_TARGET_COLLISION" if collision else \
                "GENERIC_MIXED_SCRIPT_CONFUSABLE"
            rec_level = "hold_pending_review" if collision else "queue_for_review"
            if len(records) >= _MAX_RECORDS:
                truncated = True
                level = _worse(level, rec_level)
                continue
            rec = {
                "token": token, "label": label, "unicode_label": uni,
                "revealed": _reveal(uni),
                "scripts": sorted(scripts),
                "skeleton": skel(low), "ace": _ace_form(low),
                "kind": kind, "target_collision": collision, "level": rec_level,
            }
            records.append(rec)
            witness.append(
                "label '%s' scripts=%s skeleton='%s' ace='%s'%s" % (
                    rec["revealed"], "+".join(rec["scripts"]) or "-",
                    rec["skeleton"], rec["ace"],
                    " TARGET_COLLISION='%s'" % collision if collision else ""))
            level = _worse(level, rec_level)

    if degraded:
        # W5-parity degraded policy: witness kept, verdict never raised.
        level = "pass"
    return {"status": "OK", "records": records, "separator_events": sep_events,
            "ace_failures": ace_failures, "witness": witness, "level": level,
            "truncated": truncated}
