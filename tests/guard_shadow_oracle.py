# -*- coding: utf-8 -*-
"""Shadow oracle for the increment-1 class_guard field (gate hole #1, P1).

verdict-identity (the ZWSP battery) proves the guard did not change the verdict, but
it CANNOT validate the shadow field itself: class_guard is never read by the verdict
path, so a corrupt map/members stays invisible to a verdict-identity assert. This
oracle validates the shadow field DIRECTLY, by its own properties.

Covers: P1 (census-138, position correctness, identity-on-clean, idempotence),
P2ii (exception containment -> GUARD_FAILURE), P2iii (resource cap -> TRACE_TRUNCATED),
P4 (exact-138 membership), P5/P6 (identity canonical_view + identity trace).

Run: PYTHONUTF8=1 MSL_MIP_HERMETIC_TLD=1 py -3 tests/guard_shadow_oracle.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import msl_mip_runtime as rt


def _guard(text, carded=frozenset()):
    return rt.class_guard_annotate(text, carded=carded)


def test_census_138():
    """A string with every class member exactly once -> exactly 138 members with the
    right buckets. This is the correctness test verdict-identity cannot do."""
    members_cp = sorted(rt._monitored_138_set())
    assert len(members_cp) == 138, len(members_cp)
    text = "".join(chr(cp) for cp in members_cp)
    g = _guard(text)
    assert g["status"] == "OK"
    assert len(g["members"]) == 138, len(g["members"])
    got = [int(m["codepoint"][2:], 16) for m in g["members"]]
    assert got == members_cp, "members codepoints != monitored set"
    from collections import Counter
    bc = Counter(m["class_bucket"] for m in g["members"])
    assert dict(bc) == {"PURE": 23, "DIRECTIONAL": 12, "TAG": 97, "DEPRECATED": 6}, dict(bc)


def test_offset_and_identity_map():
    """Each member.original_offset must point at that member in the original; the
    original is bit-identical to input; canonical_view is identity (increment 1)."""
    ZWSP, RLO, TAGE = "​", "‮", "\U000e0065"
    text = "goog" + ZWSP + "le" + RLO + "x" + TAGE + "y"
    g = _guard(text)
    assert g["original"] == text
    assert g["canonical_view"] == text          # identity in increment 1 (P6)
    assert g["position_trace"] == "identity"
    for m in g["members"]:
        i = m["original_offset"]
        assert "U+%04X" % ord(text[i]) == m["codepoint"], (i, text[i], m)


def test_identity_on_clean():
    for text in ("paypal.com", "cafe resume naive", "", "a b c 123"):
        g = _guard(text)
        assert g["members"] == [], text
        assert g["canonical_view"] == text
        assert g["status"] == "OK"


def test_idempotence():
    text = "a​b‮c\U000e0065d"
    g1 = _guard(text)
    g2 = _guard(g1["original"])
    assert g1["members"] == g2["members"]
    assert g1["canonical_view"] == g2["canonical_view"] == text


def test_purity_call_twice_and_order():
    a, b = "x​y", "z‮w"
    assert _guard(a) == _guard(a)                 # same input -> same result
    a1, b1 = _guard(a), _guard(b)
    b2, a2 = _guard(b), _guard(a)                 # reversed call order
    assert a1 == a2 and b1 == b2                  # order-independent (no shared state)


def test_exact_138_predicate():
    """P4: exact membership, NOT the broader _invisible_candidate set."""
    assert rt.is_monitored_control_138("​")   # ZWSP in
    assert rt.is_monitored_control_138("‮")   # RLO in
    assert rt.is_monitored_control_138("\U000e0065")  # TAG in
    assert not rt.is_monitored_control_138("️")  # VS16 (Mn) OUT
    assert not rt.is_monitored_control_138("⠀")  # braille (So) OUT
    assert not rt.is_monitored_control_138(" ")  # NBSP (Zs) OUT
    assert not rt.is_monitored_control_138("a")


def test_resource_cap_no_oom():
    """P2iii: a flood must not blow up; members are capped, count preserved, status
    reflects truncation."""
    n = rt._GUARD_MEMBER_CAP + 500
    g = _guard("​" * n)
    assert len(g["members"]) == rt._GUARD_MEMBER_CAP
    assert g["truncated"] == 500
    assert g["member_count"] == n
    assert g["status"] == "TRACE_TRUNCATED"


def test_exception_containment_shape():
    """P2ii: even on odd input the guard returns a well-formed dict, never raises."""
    for text in ("\ud800", "\udfff", "\x00\x01"):   # lone surrogates / controls
        try:
            g = _guard(text)
        except Exception as e:
            raise AssertionError("guard raised on %r: %s" % (text, e))
        assert g["status"] in ("OK", "GUARD_FAILURE", "TRACE_TRUNCATED")
        assert g["original"] == text


def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print("OK", t.__name__)
    print("\nSHADOW ORACLE: %d/%d passed" % (len(tests), len(tests)))


if __name__ == "__main__":
    main()
