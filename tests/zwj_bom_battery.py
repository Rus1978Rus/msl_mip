# -*- coding: utf-8 -*-
"""ZWJ + BOM verified-class batteries -- baseline + mutation-adequacy.

Each battery is SIGN-SCOPED: loads only that sign's card + the fullwidth-solidus
mask card, so the sign's artifact is not contaminated by other invisible cards
(mirrors the ZWSP battery's [ZWSP, mask] scoping). Measure-only.

Run:  py -3 tests/zwj_bom_battery.py
Exit 0 iff both batteries are all-green AND both hit full mutation-adequacy.
"""
import os
import sys

import verified_class_harness as H  # sets sys.path + imports the live runtime
from load_card import load_card
from zwj_bom_manifests import ZWJ_MANIFEST, BOM_MANIFEST

BASE = H._BASE
MASK = load_card(os.path.join(BASE, "cards", "SIGN_CORE_CARD_FULLWIDTH_SOLIDUS_UFF0F_GEN3_v0_3_RU.md"))
ZWJ_CARD = load_card(os.path.join(BASE, "cards", "SIGN_CORE_CARD_ZERO_WIDTH_JOINER_U200D_GEN3_v0_1_RU.md"))
BOM_CARD = load_card(os.path.join(BASE, "cards", "SIGN_CORE_CARD_BYTE_ORDER_MARK_UFEFF_GEN3_v0_1_RU.md"))

ZWJ = "‍"
BOM = "﻿"

SUITES = [
    ("ZWJ", ZWJ, [ZWJ_CARD, MASK], ZWJ_MANIFEST),
    ("BOM", BOM, [BOM_CARD, MASK], BOM_MANIFEST),
]


def main():
    all_green = True
    for name, sign, cards, manifest in SUITES:
        baseline_pass = H.run_battery(name, sign, cards, manifest)
        full = len(baseline_pass) == len(manifest)
        if not full:
            all_green = False
            print("  %s BASELINE NOT FULL: %d/%d (failing: %s)"
                  % (name, len(baseline_pass), len(manifest),
                     sorted({m["id"] for m in manifest} - baseline_pass)))
        killed, total, stable = H.mutation_adequacy(name, sign, cards, manifest, baseline_pass)
        if killed != total or not stable:
            all_green = False
        print()

    print("=" * 60)
    if all_green:
        print("RESULT: ZWJ + BOM batteries GREEN, full baseline + full mutation-adequacy.")
        return 0
    print("RESULT: NOT GREEN -- see failures above.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
