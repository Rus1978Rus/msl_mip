# -*- coding: utf-8 -*-
"""GATE: EN card mirrors carry every field the authoritative RU card declares.

The project rule is "make the EN mirror when a card closes", but nothing enforced it,
so the mirrors drifted silently: the English solidus card was missing the entire
SOLIDUS_SCHEME_PATCH description -- the rule that decides whether "//" after ":" is a
legitimate scheme or a path-traversal signal. An English reader was handed a card that
did not describe how the shipped code behaves.

This gate is the missing enforcement. It is deliberately STRUCTURAL, not linguistic: it
compares FIELD NAMES (the machine-readable skeleton), never prose, because the cards are
translations and their sentences must differ. A field present in the Russian card and
absent from the English one fails the build.

Scope: cards that HAVE an EN mirror. A card without a mirror is not failed here -- the
project rule ties the mirror to closure, and WORKING_DRAFT cards (U+FF0F, U+200D,
U+FEFF) legitimately have none yet. Their pairs join this gate when they close.
"""
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_BASE = os.path.dirname(_HERE)
_CARDS = os.path.join(_BASE, "cards")

# (RU file stem, EN file stem). RU stems carry historical "__1_" / "__2_" suffixes
# from the original upload; the pairing is explicit so a rename cannot silently
# drop a card out of this gate.
PAIRS = [
    ("SIGN_CORE_CARD_DOT_U002E_GEN3_v0_3_RU__2_",
     "SIGN_CORE_CARD_DOT_U002E_GEN3_v0_3_EN"),
    ("SIGN_CORE_CARD_SOLIDUS_U002F_GEN3_v0_3_RU__1_",
     "SIGN_CORE_CARD_SOLIDUS_U002F_GEN3_v0_3_EN"),
    ("SIGN_CORE_CARD_SKULL_U1F480_GEN3_v0_3_RU__1_",
     "SIGN_CORE_CARD_SKULL_U1F480_GEN3_v0_3_EN"),
    ("SIGN_CORE_CARD_SKULL_CROSSBONES_U2620_GEN3_v0_3_RU",
     "SIGN_CORE_CARD_SKULL_CROSSBONES_U2620_GEN3_v0_3_EN"),
    ("SIGN_CORE_CARD_AT_U0040_GEN3_v0_3_RU",
     "SIGN_CORE_CARD_AT_U0040_GEN3_v0_3_EN"),
    ("SIGN_CORE_CARD_ZERO_WIDTH_SPACE_U200B_GEN3_v0_3_RU",
     "SIGN_CORE_CARD_ZERO_WIDTH_SPACE_U200B_GEN3_v0_3_EN"),
]

# Fields that legitimately exist on ONE side only: the document's own identity and
# the note explaining that the English file is a translation.
EXEMPT = {"TRANSLATION_NOTE"}

_FIELD = re.compile(r"^ *([A-Z][A-Z0-9_]{4,}):", re.M)

fails = []
checked = 0

for ru_stem, en_stem in PAIRS:
    ru_path = os.path.join(_CARDS, ru_stem + ".md")
    en_path = os.path.join(_CARDS, en_stem + ".md")
    if not os.path.isfile(ru_path):
        fails.append("RU card missing: %s" % ru_stem)
        continue
    if not os.path.isfile(en_path):
        fails.append("EN mirror missing: %s" % en_stem)
        continue
    ru_text = open(ru_path, encoding="utf-8").read()
    en_text = open(en_path, encoding="utf-8").read()
    ru_fields = {f for f in _FIELD.findall(ru_text)} - EXEMPT
    missing = sorted(f for f in ru_fields if f not in en_text)
    if missing:
        fails.append("%s: EN mirror lacks %s"
                     % (en_stem.replace("SIGN_CORE_CARD_", ""), ", ".join(missing)))
    checked += 1

# Every EN mirror must say it is a translation and which card is authoritative --
# otherwise a reader can mistake the mirror for the source of truth.
for _, en_stem in PAIRS:
    en_path = os.path.join(_CARDS, en_stem + ".md")
    if not os.path.isfile(en_path):
        continue
    text = open(en_path, encoding="utf-8").read()
    if "TRANSLATION_NOTE" not in text or "authoritative" not in text.lower():
        fails.append("%s: no TRANSLATION_NOTE naming the authoritative card"
                     % en_stem.replace("SIGN_CORE_CARD_", ""))

print("=" * 66)
print("GATE: EN card mirrors carry the RU field skeleton")
print("=" * 66)
if fails:
    for f in fails:
        print("  FAIL: " + f)
    print("\nTOTAL: FAIL")
    sys.exit(1)
print("%d card pairs checked: every field declared in the authoritative RU card is"
      % checked)
print("  present in its EN mirror, and every mirror names its source as authoritative")
print("Not checked here (by design): prose, wording, ordering -- these are translations")
print("Not failed here: cards with no mirror yet (WORKING_DRAFT: U+FF0F, U+200D, U+FEFF)")
print("\nTOTAL: CLEAN")
sys.exit(0)
