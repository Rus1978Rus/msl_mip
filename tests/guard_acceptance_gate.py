# -*- coding: utf-8 -*-
"""Acceptance gate for the increment-1 class_guard (P7 + P3 + P8).

P7 full-differential : analyze() with the guard enabled vs disabled must be IDENTICAL
                       on every verdict-path field; the ONLY allowed delta is the added
                       class_guard key.
P3 mutation-adequacy : inject guard bugs (MUT-G8 card_mask flip, MUT-G9 detect-after-
                       normalization, MUT-G10 offset drift) and assert the shadow-oracle
                       property checks CATCH each one (so the gate is not a false green).
P8 demask integration: an F-NEW-1 scenario (a second invisible next to a carded one in a
                       host) must not silently bypass the guard — the guard runs on the
                       ORIGINAL, so it sees BOTH invisibles, and the host verdict stands.

Run: PYTHONUTF8=1 MSL_MIP_HERMETIC_TLD=1 py -3 tests/guard_acceptance_gate.py
"""
import os, sys, unicodedata
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import msl_mip_runtime as rt

ZWSP, ITIM, RLO, TAGE, BOM = "​", "⁢", "‮", "\U000e0065", "﻿"

# verdict-path projection: everything the verdict depends on (NOT class_guard)
def _verdict_projection(rep):
    rv = [(v.get("visible_form"), v.get("relation_type"), v.get("runtime_role"),
           v.get("risk_level"), v.get("detected_context"))
          for v in rep["sequence_output"].relation_verdicts]
    return {
        "semantic_action": rep["semantic_action"],
        "effective_action": rep["effective_action"],
        "integrity_status": rep["integrity_status"],
        "attention_status": rep["attention_status"],
        "uncarded_invisibles": rep["uncarded_invisibles"],
        "relation_verdicts": rv,
        "n_single": len(rep["single_sign_results"]),
    }


def _analyze(text, cards, guard_disabled):
    if guard_disabled:
        os.environ["MSL_MIP_GUARD_DISABLED"] = "1"
    else:
        os.environ.pop("MSL_MIP_GUARD_DISABLED", None)
    try:
        return rt.analyze(text, cards)
    finally:
        os.environ.pop("MSL_MIP_GUARD_DISABLED", None)


def test_full_differential():
    """P7: guard-enabled vs guard-disabled -> only delta is the class_guard key."""
    cards = rt.load_all_cards()
    cases = [
        "goog" + ZWSP + "le.com", "bad" + ZWSP + "word", "just " + ZWSP + " text",
        "goog" + ITIM + "le.com", "user" + RLO + "name", BOM + "paypal.com",
        "paypal.com", "hi" + TAGE + "there", "a" + ZWSP + "b" + RLO + "c",
    ]
    for text in cases:
        on = _analyze(text, cards, guard_disabled=False)
        off = _analyze(text, cards, guard_disabled=True)
        assert "class_guard" in on and "class_guard" not in off, text
        assert _verdict_projection(on) == _verdict_projection(off), (
            "verdict-path changed for %r" % text)
        # only-allowed-delta: key sets differ by exactly {class_guard}
        assert set(on) - set(off) == {"class_guard"} and set(off) - set(on) == set(), text


# --- P3: property checks that take a GuardResult, so mutations can be injected ---
def _check_census(g, monitored):
    got = sorted(int(m["codepoint"][2:], 16) for m in g["members"])
    assert got == sorted(monitored), "census mismatch"

def _check_offsets(g):
    t = g["original"]
    for m in g["members"]:
        assert "U+%04X" % ord(t[m["original_offset"]]) == m["codepoint"], "offset wrong"

def _check_card_mask(g, carded):
    for m in g["members"]:
        cp = int(m["codepoint"][2:], 16)
        assert m["card_mask"] == (cp in carded), "card_mask wrong"


def test_mutation_adequacy():
    """P3: each injected guard bug MUST be caught by a property check."""
    text = "ﬁ" + ZWSP + "x" + RLO + "y"          # ligature shifts NFKC positions
    carded = frozenset({0x200B})
    good = rt.class_guard_annotate(text, carded=carded)
    _check_offsets(good); _check_card_mask(good, carded)   # sanity: good passes

    def caught(fn):
        try:
            fn(); return False
        except AssertionError:
            return True

    # MUT-G8: card_mask flip
    m8 = {**good, "members": [{**m, "card_mask": not m["card_mask"]} for m in good["members"]]}
    assert caught(lambda: _check_card_mask(m8, carded)), "MUT-G8 not caught"

    # MUT-G9: detect AFTER normalization (positions computed on NFKC, claimed on original)
    norm = unicodedata.normalize("NFKC", text)
    m9 = rt.class_guard_annotate(norm, carded=carded)
    m9 = {**m9, "original": text}                          # claim original but offsets are NFKC-based
    assert caught(lambda: _check_offsets(m9)), "MUT-G9 not caught"

    # MUT-G10: offset drift (codepoint vs UTF-16 style off-by-one)
    m10 = {**good, "members": [{**m, "original_offset": m["original_offset"] + 1}
                               for m in good["members"]]}
    assert caught(lambda: _check_offsets(m10)), "MUT-G10 not caught"


def test_demask_integration_no_bypass():
    """P8: F-NEW-1 scenario — a second invisible next to the carded ZWSP in a host.
    The guard runs on the ORIGINAL, so it must see BOTH; and the host verdict stands
    (no silent bypass through demask)."""
    cards = rt.load_all_cards()
    text = "goog" + ZWSP + ITIM + "le.com"      # carded ZWSP + uncarded INVISIBLE TIMES
    rep = rt.analyze(text, cards)
    cps = {m["codepoint"] for m in rep["class_guard"]["members"]}
    assert "U+200B" in cps and "U+2062" in cps, "guard missed a second invisible"
    # host still flagged (F-NEW-1 fix intact): not a silent pass
    assert rep["effective_action"] == "hold_pending_review", rep["effective_action"]


def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print("OK", t.__name__)
    print("\nACCEPTANCE GATE: %d/%d passed" % (len(tests), len(tests)))


if __name__ == "__main__":
    main()
