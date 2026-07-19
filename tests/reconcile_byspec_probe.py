# -*- coding: utf-8 -*-
"""Reproducibility probe for RECONCILE_BYSPEC_ZWJ_BOM_2026-07-18.

Measures BY_CODE for the 10 BY_SPEC contexts (Z1-Z5, B1-B5) through the shipped
analyze(), and maps each verdict to the three-level signal used in the reconcile
record. MEASURE-ONLY: prints levels, asserts nothing (the reconcile is a
point-in-time record, not a gate). Run: py -3 tests/reconcile_byspec_probe.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import msl_mip_runtime as rt

ZWJ = "‍"
BOM = "﻿"

# three-level mapping: hold->REAL, queue->POSSIBLE, pass->CLEAN
LEVEL = {"pass": "CLEAN", "queue_for_review": "POSSIBLE",
         "hold_pending_review": "REAL"}

CASES = [
    ("Z1 ZWJ emoji-family", "\U0001F468" + ZWJ + "\U0001F469" + ZWJ + "\U0001F467"),
    ("Z2 ZWJ latin host", "goog" + ZWJ + "le.com"),
    ("Z3 ZWJ persian word", "می" + ZWJ + "خواهم"),
    ("Z4 ZWJ token/ident", "user" + ZWJ + "name"),
    ("Z5 ZWJ free text", "just " + ZWJ + " text"),
    ("B1 leading BOM text", BOM + "hello world"),
    ("B1' leading BOM json", BOM + '{"k":"v"}'),
    ("B2 BOM mid-host", "pay" + BOM + "pal.com"),
    ("B3 BOM mid-email", "us" + BOM + "er@example.com"),
    ("B3' BOM mid-token", "bad" + BOM + "word"),
    ("B4 leading BOM+domain", BOM + "paypal.com"),
    ("B5 parser-desync", None),  # not observable from a single string
]


def main():
    cards = rt.load_all_cards()
    for name, text in CASES:
        if text is None:
            print("%-24s -> PENDING (runtime does not observe cross-parser desync)" % name)
            continue
        r = rt.analyze(text, cards)
        act = r["effective_action"]
        print("%-24s -> action=%-20s LEVEL=%s" % (name, act, LEVEL.get(act, act)))


if __name__ == "__main__":
    main()
