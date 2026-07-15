# -*- coding: utf-8 -*-
# SIMULATION of the "functional neighbors" rule as a checkable function
# over UCD properties. Not prose - we COMPUTE what the criterion emits.
#
# Rule (from conveyor, in words):
#  - a sign falls under the rule if it produces NO VISIBLE GLYPH (observed
#    effect, not formal Unicode category);
#  - a FUNCTIONAL NEIGHBOR = a sign INDISTINGUISHABLE TO A NAIVE FILTER
#    (both invisible/ignorable under crude processing) - NOT "similar function";
#  - list ALL real neighbors; number is NOT fixed; padding to 5 is forbidden;
#  - borderline (visible in some conditions) -> mark explicitly.
import sys, unicodedata
u = unicodedata
print("Unicode DB:", u.unidata_version, "| Python", sys.version.split()[0])

# --- Default_Ignorable_Code_Point ranges (UCD DerivedCoreProperties) ---
DI_RANGES = [
    (0x00AD,0x00AD),(0x034F,0x034F),(0x061C,0x061C),(0x115F,0x1160),
    (0x17B4,0x17B5),(0x180B,0x180F),(0x200B,0x200F),(0x202A,0x202E),
    (0x2060,0x206F),(0x3164,0x3164),(0xFE00,0xFE0F),(0xFEFF,0xFEFF),
    (0xFFA0,0xFFA0),(0xFFF0,0xFFF8),(0x1BCA0,0x1BCA3),(0x1D173,0x1D17A),
    (0xE0000,0xE0FFF),
]
def is_DI(cp):
    return any(a<=cp<=b for a,b in DI_RANGES)

DIRECTIONAL_BIDI = {"L","R","AL","LRE","RLE","PDF","LRO","RLO","LRI","RLI","FSI","PDI"}
TAG_CP = lambda cp: cp==0xE0001 or 0xE0020<=cp<=0xE007F
DEPRECATED_FMT = lambda cp: 0x206A<=cp<=0x206F  # deprecated since Unicode 6.3

def props(cp):
    ch=chr(cp)
    return dict(cp=cp, ch=ch, name=u.name(ch,"<unassigned/unnamed>"),
                gc=u.category(ch), bidi=u.bidirectional(ch), di=is_DI(cp))

def visibility(cp, gc, bidi):
    # OBSERVED visibility model (not the formal category alone)
    if cp==0x00AD: return ("BORDERLINE","in-line invisible; renders as HYPHEN at line-break")
    if cp==0x2800: return ("BORDERLINE","formal So (visible); renders as EMPTY braille cell")
    if gc=="Mn":
        if 0xFE00<=cp<=0xFE0F or 0xE0100<=cp<=0xE01EF:
            return ("BORDERLINE","variation selector: no own glyph, alters preceding char")
        return ("BORDERLINE","combining mark: no advance, modifies neighbor")
    if gc=="Lo":  # Hangul fillers
        return ("BORDERLINE","filler: occupies LAYOUT WIDTH, no ink")
    if gc=="Cf":
        if bidi in DIRECTIONAL_BIDI:
            return ("INVISIBLE_DIRECTIONAL","no glyph, but REORDERS surrounding text")
        return ("INVISIBLE","no glyph, zero advance")
    if gc=="Zs":
        return ("VISIBLE","space: takes advance width (naive filter sees whitespace)")
    return ("VISIBLE","has a glyph / advance width")

# under the rule = no visible glyph by observed effect
UNDER_RULE_VIS = {"INVISIBLE","INVISIBLE_DIRECTIONAL","BORDERLINE"}
def under_rule(cp, gc, bidi):
    v,_ = visibility(cp,gc,bidi)
    if v=="BORDERLINE" and gc=="Lo": return False  # filler occupies width -> not invisible
    if v=="BORDERLINE" and cp==0x2800: return False # visible glyph (empty), not DI-invisible
    if v=="VISIBLE": return False
    return True

# --- build the neighbor POOL = all assigned DI code points ---
POOL=[]
for a,b in DI_RANGES:
    for cp in range(a,b+1):
        p=props(cp)
        if p["gc"]=="Cn": continue  # unassigned/reserved - not a live sign
        POOL.append(p)

def bucket_of(p):
    cp,gc,bidi=p["cp"],p["gc"],p["bidi"]
    if TAG_CP(cp): return "TAG"
    if gc=="Lo": return "FILLER_WIDTH"
    if gc=="Mn": return "ATTACHING"
    if gc=="Cf" and bidi in DIRECTIONAL_BIDI: return "DIRECTIONAL_FMT"
    if gc=="Cf" and DEPRECATED_FMT(cp): return "DEPRECATED_FMT"
    if gc=="Cf": return "ZW_TEXT_FMT"   # non-directional zero-width text format
    return "OTHER"

def fmt(cp): return f"U+{cp:04X}"

def neighbors(target_cp):
    # naive-filter bucket: strict (all standalone zero-width no-glyph) and
    # text (non-directional zero-width format = closest to what a card lists)
    strict, text = [], []
    for p in POOL:
        if p["cp"]==target_cp: continue
        b=bucket_of(p)
        if b in ("ZW_TEXT_FMT","DIRECTIONAL_FMT","DEPRECATED_FMT"):
            strict.append(p)
        if b=="ZW_TEXT_FMT":
            text.append(p)
    return strict, text

CARD_ZWSP = {0x200C,0x200D,0x2060,0xFEFF,0x00AD}  # ZWNJ ZWJ WJ BOM SHY

BATTERY = [
    ("MUST FIRE",   0x200B,"ZWSP"),
    ("MUST FIRE",   0xFEFF,"BOM"),
    ("MUST FIRE",   0x200D,"ZWJ"),
    ("MUST FIRE",   0x200C,"ZWNJ"),
    ("BORDERLINE",  0x00AD,"SHY"),
    ("BORDERLINE",  0x2800,"BRAILLE BLANK"),
    ("BORDERLINE",  0x00A0,"NBSP"),
    ("MUST NOT",    0x0020,"SPACE"),
    ("MUST NOT",    0x0430,"CYRILLIC a"),
    ("MUST NOT",    0x0061,"LATIN a"),
]

print("="*74)
print("STEP 1 - does each sign FALL UNDER the rule? (property reason)")
print("="*74)
for tag,cp,lbl in BATTERY:
    p=props(cp); v,why=visibility(cp,p["gc"],p["bidi"])
    ur=under_rule(cp,p["gc"],p["bidi"])
    print(f"[{tag:10}] {fmt(cp)} {lbl:14} gc={p['gc']:3} bidi={p['bidi']:3} DI={str(p['di']):5} "
          f"-> UNDER_RULE={'YES' if ur else 'NO ':3} vis={v}")
    print(f"{'':13} reason: {why}")

print("\n"+"="*74)
print("STEP 2 - NEIGHBORS emitted by the criterion (the real question)")
print("="*74)
for cp,lbl in [(0x200B,"ZWSP"),(0xFEFF,"BOM"),(0x200D,"ZWJ"),(0x200C,"ZWNJ")]:
    strict,text=neighbors(cp)
    print(f"\n--- {fmt(cp)} {lbl} ---")
    print(f"  non-directional ZW text-format neighbors (tightest sensible bucket): {len(text)}")
    for p in sorted(text,key=lambda x:x['cp']):
        mark=" <== IN CARD" if (cp==0x200B and p['cp'] in CARD_ZWSP) else ""
        extra=" **NOT IN CARD**" if (cp==0x200B and p['cp'] not in CARD_ZWSP) else ""
        print(f"      {fmt(p['cp'])} {p['name']:38}{mark}{extra}")
    print(f"  + strict naive-filter bucket (also pulls directional+deprecated): {len(strict)} total")

print("\n"+"="*74)
print("STEP 3 - ZWSP vs CARD (name divergence PLAINLY)")
print("="*74)
strict,text=neighbors(0x200B)
text_cps={p['cp'] for p in text}
strict_cps={p['cp'] for p in strict}
print(f"  CARD lists ({len(CARD_ZWSP)}): "+", ".join(fmt(c) for c in sorted(CARD_ZWSP)))
print(f"  CRITERION text-bucket ({len(text_cps)}): "+", ".join(fmt(c) for c in sorted(text_cps)))
print(f"  CRITERION strict-bucket: {len(strict_cps)}")
missing_from_card = text_cps - CARD_ZWSP
card_not_in_crit  = CARD_ZWSP - text_cps
print(f"\n  in CRITERION text-bucket but NOT in card ({len(missing_from_card)}):")
for c in sorted(missing_from_card):
    print(f"      {fmt(c)} {u.name(chr(c),'?')}")
print(f"  in CARD but NOT in criterion text-bucket ({len(card_not_in_crit)}): "
      +(", ".join(fmt(c) for c in sorted(card_not_in_crit)) or "(none)"))

print("\n"+"="*74)
print("STEP 4 - neighbor COUNT per sign (detachment from '5')")
print("="*74)
for cp,lbl in [(0x200B,"ZWSP"),(0xFEFF,"BOM"),(0x200D,"ZWJ"),(0x200C,"ZWNJ"),(0x00AD,"SHY"),(0x2060,"WJ")]:
    strict,text=neighbors(cp)
    print(f"  {fmt(cp)} {lbl:6}: text-bucket={len(text):2}  strict-bucket={len(strict):2}")

print("\n"+"="*74)
print("STEP 5 - where the criterion is AMBIGUOUS (the naive filter is under-specified)")
print("="*74)
counts={}
for p in POOL:
    counts[bucket_of(p)]=counts.get(bucket_of(p),0)+1
print("  assigned DI pool by bucket:", {k:counts[k] for k in sorted(counts)})
