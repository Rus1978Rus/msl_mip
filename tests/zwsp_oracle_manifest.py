# -*- coding: utf-8 -*-
"""ZWSP TIER_2 ORACLE MANIFEST — independent third reference.
Written BEFORE the run. Expected tuple per case is pinned here by Unicode
property / structure, NOT derived from either leg (BY_CODE or BY_SPEC).
Guards against 'both legs erred identically'.

Each case:
  id, cls, input (built from codepoints), must_contain (ord list — preflight),
  ctx / risk / verdict / witness = ACCEPTABLE sets (measured must fall inside),
  forbidden = values that must NOT appear (hard fail),
  basis = why (Unicode property / structure),
  decoded_input = optional 2nd stage (D4 percent-decode).
'-' means 'no ZWSP relation verdict expected' (context/risk not applicable).
witness codepoints are strings like 'U+2800'.
"""

Z="​"; ZWJ="‍"; ITIM="⁢"; BRAILLE="⠀"
NBSP=" "; NNBSP=" "; LSEP=" "; PSEP=" "
FW="／"; O="о"

def C(**k): return k

MANIFEST = [
# ===== REGISTRAR (6) — uncarded invisibles get a witness; carded do not =====
 C(id="R1", cls="registrar", input="goog"+BRAILLE+"le.com", must_contain=[0x2800],
   ctx={"-"}, risk={"-"}, verdict={"pass"}, witness={"U+2800"},
   basis="U+2800 BRAILLE PATTERN BLANK (cat So). Renders empty; OUTSIDE Cf/Zs. "
         "A witness system should surface it (explicit exception) as UNVERIFIABLE."),
 C(id="R2", cls="registrar", input="paypal"+NBSP+".com", must_contain=[0x00A0],
   ctx={"-"}, risk={"-"}, verdict={"pass"}, witness={"U+00A0"},
   basis="U+00A0 NO-BREAK SPACE (cat Zs). Invisible-width, evasion-capable."),
 C(id="R3", cls="registrar", input="admin"+NNBSP+"panel", must_contain=[0x202F],
   ctx={"-"}, risk={"-"}, verdict={"pass"}, witness={"U+202F"},
   basis="U+202F NARROW NO-BREAK SPACE (cat Zs). Distinct codepoint, not R2."),
 C(id="R4", cls="registrar", input="line1"+LSEP+"line2", must_contain=[0x2028],
   ctx={"-"}, risk={"-"}, verdict={"pass"}, witness={"U+2028"},
   basis="U+2028 LINE SEPARATOR (cat Zl)."),
 C(id="R5", cls="registrar", input="para"+PSEP+"break", must_contain=[0x2029],
   ctx={"-"}, risk={"-"}, verdict={"pass"}, witness={"U+2029"},
   basis="U+2029 PARAGRAPH SEPARATOR (cat Zp)."),
 C(id="R6", cls="registrar", input="text"+Z+"here", must_contain=[0x200B],
   ctx={"BYTE_EXACT_TOKEN"}, risk={"MEDIUM"}, verdict={"queue_for_review"}, witness=set(),
   basis="ZWSP is CARDED -> NO witness; but the card verdict must NOT be lost. "
         "'texthere' is a no-space word to exact-compare -> BYTE_EXACT_TOKEN/MEDIUM."),

# ===== POSITIONS (4) — where the ZWSP sits changes context, NOT always HOST =====
 C(id="P1", cls="positions", input=Z+"paypal.com", must_contain=[0x200B],
   ctx={"HIDDEN_BOUNDARY_PADDING"}, risk={"MEDIUM"}, verdict={"queue_for_review"}, witness=set(),
   forbidden={"ctx":{"HOST"},"risk":{"HIGH"},"verdict":{"hold_pending_review","pass"}},
   basis="LEADING hidden padding. U+200B is NOT White_Space (trim won't remove). "
         "Domain 'paypal.com' intact after the pad -> NOT a label break; but NOT a "
         "silent pass either -> HIDDEN_BOUNDARY_PADDING/MEDIUM (F-NEW-2 2A)."),
 C(id="P2", cls="positions", input="paypal.com"+Z, must_contain=[0x200B],
   ctx={"HIDDEN_BOUNDARY_PADDING"}, risk={"MEDIUM"}, verdict={"queue_for_review"}, witness=set(),
   forbidden={"ctx":{"HOST"},"risk":{"HIGH"},"verdict":{"hold_pending_review","pass"}},
   basis="TRAILING hidden padding. Domain intact -> HIDDEN_BOUNDARY_PADDING/MEDIUM (2A)."),
 C(id="P4", cls="positions", input="paypal.com"+Z+"/path", must_contain=[0x200B],
   ctx={"PATH"}, risk={"MEDIUM"}, verdict={"queue_for_review"}, witness=set(),
   forbidden={"ctx":{"HOST"},"risk":{"HIGH"},"verdict":{"hold_pending_review"}},
   basis="ZWSP AFTER a whole domain, before '/'. Does NOT break the label -> PATH "
         "(2B: left is already a complete domain). FORBIDDEN HOST/HIGH/HOLD."),
 C(id="P5", cls="positions", input="docs.example.com/guide/very-long"+Z+"-section", must_contain=[0x200B],
   ctx={"PATH"}, risk={"MEDIUM"}, verdict={"queue_for_review"}, witness=set(),
   forbidden={"ctx":{"HOST"},"risk":{"HIGH"},"verdict":{"hold_pending_review"}},
   basis="R8/deep-path: schemeless domain + ZWSP DEEP in path. ZWSP is in the path, "
         "not the host -> PATH/MEDIUM. FORBIDDEN HOST/HIGH/HOLD."),

# ===== COMBO (2) — carded ZWSP + a second invisible =====
 C(id="K1", cls="combo", input="goog"+Z+ZWJ+"le.com", must_contain=[0x200B,0x200D],
   ctx={"HOST"}, risk={"HIGH"}, verdict={"hold_pending_review"}, witness={"U+200D"},
   basis="ZWSP breaks the host label -> HOST/HIGH. U+200D (ZWJ) is uncarded IN THIS "
         "ZWSP-scoped battery (it loads [ZWSP, mask] only) -> witness. This still tests "
         "the no-suppression invariant (strong ZWSP verdict must not swallow a co-present "
         "uncarded invisible's witness). NB 2026-07-17: a ZWJ WORKING_DRAFT card now "
         "exists and the SHIPPED loadout (CARD_FILENAMES) cards it -> there ZWJ routes "
         "via its own card (HOST/HIGH, no witness). This battery deliberately stays "
         "ZWSP-scoped and does NOT load the unverified ZWJ card, so the verified ZWSP "
         "artifact is not contaminated. Shipped ZWJ behavior is probe-verified in the "
         "ZWJ card. K3 (U+2062) also covers no-suppression with a still-uncarded sign."),
 C(id="K3", cls="combo", input="goog"+Z+ITIM+"le.com", must_contain=[0x200B,0x2062],
   ctx={"HOST"}, risk={"HIGH"}, verdict={"hold_pending_review"}, witness={"U+2062"},
   basis="known(ZWSP)+unknown(U+2062): ZWSP -> HOST/HIGH AND the U+2062 witness "
         "must NOT be suppressed by the strong known verdict."),

# ===== URL (2) — component matters =====
 C(id="U1", cls="url", input="https://site.example/?q=bad"+Z+"word", must_contain=[0x200B],
   ctx={"QUERY_VALUE"}, risk={"MEDIUM"}, verdict={"queue_for_review"}, witness=set(),
   forbidden={"ctx":{"HOST"},"risk":{"HIGH"}},
   basis="Full URL. ZWSP in the QUERY value 'bad<ZWSP>word' -> QUERY_VALUE/MEDIUM. "
         "FORBIDDEN HOST/HIGH."),
 C(id="U2", cls="url", input="us"+Z+"er@example.com", must_contain=[0x200B],
   ctx={"EMAIL"}, risk={"MEDIUM"}, verdict={"queue_for_review"}, witness=set(),
   basis="ZWSP BEFORE @ -> email local-part split -> EMAIL/MEDIUM."),

# ===== DANGEROUS (5) =====
 C(id="D1", cls="dangerous", input="paypal"+Z+".com", must_contain=[0x200B],
   ctx={"HOST"}, risk={"HIGH"}, verdict={"hold_pending_review"}, witness=set(),
   differential=True,
   basis="ZWSP inside the domain label -> HOST/HIGH, NEVER a silent PASS. "
         "Double assert: (1) source has U+200B; (2) reconstructed host != raw."),
 C(id="D2", cls="dangerous", input="http://paypal.com"+Z+"@evil.com", must_contain=[0x200B],
   ctx={"USERINFO"}, risk={"MEDIUM"}, verdict={"queue_for_review"}, witness=set(),
   forbidden={"ctx":{"HOST"},"risk":{"HIGH"},"verdict":{"hold_pending_review"}},
   basis="userinfo@host (F-NEW-5): the mask is in the USERINFO (before the LAST @); "
         "the real host is evil.com (after @), intact. Achievable fix = correct "
         "COMPONENT attribution USERINFO/MEDIUM, NOT the old HOST/HIGH over-"
         "attribution. Full host-string extraction is a separate capability; "
         "labeling the mask's component is the fix. FORBIDDEN: treat paypal.com as HOST."),
 C(id="D3", cls="dangerous", input="paypal"+Z+".com.", must_contain=[0x200B],
   ctx={"HOST"}, risk={"HIGH"}, verdict={"hold_pending_review"}, witness=set(),
   basis="Trailing FQDN dot adds a canonicalization boundary (not a dup of D1). "
         "Still HOST/HIGH."),
 C(id="D4", cls="dangerous", input="paypal%E2%80%8Bl.com", must_contain=[],
   decoded_input="paypal"+Z+"l.com", decoded_must_contain=[0x200B],
   ctx={"-"}, risk={"-"}, verdict={"pass"}, witness=set(),
   decoded_ctx={"HOST"}, decoded_risk={"HIGH"}, decoded_verdict={"hold_pending_review"},
   basis="Stage1 RAW: no literal U+200B (percent-escaped) -> ZWSP card must NOT "
         "falsely fire on %E2%80%8B. Stage2 POST-DECODE: bytes -> U+200B -> HOST/HIGH."),
 C(id="D5", cls="dangerous", input="goog"+Z+BRAILLE+"le.com", must_contain=[0x200B,0x2800],
   ctx={"HOST"}, risk={"HIGH"}, verdict={"hold_pending_review"}, witness={"U+2800"},
   basis="Stacking: ZWSP breaks the label -> HOST/HIGH; braille U+2800 is outside "
         "the OLD Cf/Zs predicate -> is it seen by the (extended?) witness net?"),

# ===== CONTROLS (2) — CRITICAL for an alert system =====
 C(id="T1", cls="controls", input="日本語"+Z+"のテキスト", must_contain=[0x200B],
   ctx={"BYTE_EXACT_TOKEN","FREE_TEXT","-"}, risk={"MEDIUM","NONE","-"},
   verdict={"queue_for_review","pass"}, witness=set(),
   basis="Legit CJK line-break (SAFE_CASE_002). Fixed by CARD HONESTY, not code "
         "(a 'CJK=safe' heuristic would open a mask-miss in a CJK DOMAIN). The "
         "card now declares CURRENT_RUNTIME_EXPECTATION: MAY_QUEUE -- the detector "
         "without typography context collapses the CJK token to BYTE_EXACT_TOKEN "
         "-> MEDIUM. Oracle expectation brought to REALITY (MAY_QUEUE, not NONE); "
         "NOT a bug -- an honest boundary until typography-context (v0.5)."),
 C(id="N1", cls="controls", input="обычный текст с пробелами", must_contain=[0x20],
   ctx={"-"}, risk={"-"}, verdict={"pass"}, witness=set(),
   basis="Negative control: ordinary U+0020 spaces (Zs, White_Space) must NOT "
         "create a witness-flood if the predicate is widened to Zs. No witness."),
]

assert len(MANIFEST) == 21, f"expected 21 cases, got {len(MANIFEST)}"
