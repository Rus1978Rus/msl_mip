# -*- coding: utf-8 -*-
"""ZWJ (U+200D) and BOM (U+FEFF) ORACLE MANIFESTS -- independent third reference.
Expected tuple per case is pinned by Unicode property / structure / the CARD's
declared behavior, NOT derived from either leg. ACCEPTABLE sets (measured must
fall inside); forbidden = values that must NOT appear (hard fail).

ZWJ: Join_Control=YES, joins adjacent forms; legit in emoji + Arabic/Indic
  joining; Latin does not join so ZWJ in a Latin token is pure insertion.
BOM: byte-order-mark, positional legitimacy (first char of a transport stream);
  the mid-stream zero-width-no-break role is deprecated since Unicode 3.2.
Card grounding: ZWJ PER_OCCURRENCE_BOUNDARY (functional=clean / redundant=possible);
  BOM OBSERVATION_LEVEL (transport-stream=clean / application-prefix=possible).
'-' means no relation verdict expected. Witness codepoints are 'U+XXXX' strings.
Battery is SIGN-SCOPED: a co-present ZWSP (U+200B) is UNCARDED here -> witnessed,
which also tests the no-suppression invariant.
"""
ZWJ = "‍"; BOM = "﻿"; ZWSP = "​"
EMOJI = "\U0001F468" + ZWJ + "\U0001F469" + ZWJ + "\U0001F467"


def C(**k):
    return k


ZWJ_MANIFEST = [
 C(id="Z1", cls="legit", input=EMOJI, must_contain=[0x200D],
   ctx={"FREE_TEXT", "-"}, risk={"NONE", "-"}, verdict={"pass"}, witness=set(),
   forbidden={"verdict": {"queue_for_review", "hold_pending_review"}},
   basis="Legit RGI emoji ZWJ sequence (family). Card SAFE_CASE_001: emoji join is "
         "the canonical legitimate use -> FREE_TEXT/NONE, no false positive."),
 C(id="Z2", cls="dangerous", input="goog" + ZWJ + "le.com", must_contain=[0x200D],
   ctx={"HOST"}, risk={"HIGH"}, verdict={"hold_pending_review"}, witness=set(),
   differential=True, forbidden={"verdict": {"pass"}},
   basis="Latin script does NOT join -> ZWJ inside a host label is a pure diversion "
         "breaking the label. HOST/HIGH, NEVER a silent pass."),
 C(id="Z3", cls="boundary", input="می" + ZWJ + "خواهم", must_contain=[0x200D],
   ctx={"BYTE_EXACT_TOKEN", "FREE_TEXT"}, risk={"MEDIUM", "NONE"},
   verdict={"queue_for_review", "pass"}, witness=set(),
   forbidden={"verdict": {"hold_pending_review"}},
   basis="Persian joining context. Card PER_OCCURRENCE_BOUNDARY: functional vs "
         "redundant ZWJ is not distinguishable without script context (v0.5) -> honest "
         "MAY_QUEUE. Not a bug -- a declared boundary. FORBIDDEN hold (over-escalation)."),
 C(id="Z4", cls="boundary", input="user" + ZWJ + "name", must_contain=[0x200D],
   ctx={"BYTE_EXACT_TOKEN"}, risk={"MEDIUM"}, verdict={"queue_for_review"}, witness=set(),
   forbidden={"verdict": {"pass"}},
   basis="No-space token to exact-compare; ZWJ defeats byte-exact matching of the "
         "identifier -> BYTE_EXACT_TOKEN/MEDIUM, not a silent pass."),
 C(id="Z5", cls="soft", input="just " + ZWJ + " text", must_contain=[0x200D],
   ctx={"FREE_TEXT"}, risk={"NONE"}, verdict={"pass"}, witness=set(),
   basis="Free-text ZWJ. Current honest CLEAN; reconcile Z5 flagged this as code-softer-"
         "than-blind (RISK_CASE_004 free-text padding PENDING) -> an OPEN softness the "
         "battery records, not asserts away. Acceptable {pass} for the current design."),
 C(id="Z6", cls="positions", input=ZWJ + "paypal.com", must_contain=[0x200D],
   ctx={"HIDDEN_BOUNDARY_PADDING"}, risk={"MEDIUM"}, verdict={"queue_for_review"}, witness=set(),
   forbidden={"verdict": {"pass"}, "risk": {"HIGH"}},
   basis="Leading ZWJ padding before a whole domain. Not a label break (domain intact) "
         "but not a silent pass -> HIDDEN_BOUNDARY_PADDING/MEDIUM."),
 C(id="Z7", cls="url", input="us" + ZWJ + "er@example.com", must_contain=[0x200D],
   ctx={"EMAIL"}, risk={"MEDIUM"}, verdict={"queue_for_review"}, witness=set(),
   forbidden={"ctx": {"HOST"}, "risk": {"HIGH"}},
   basis="ZWJ before @ -> email local-part split -> EMAIL/MEDIUM. FORBIDDEN HOST/HIGH."),
 C(id="Z8", cls="combo", input="goog" + ZWJ + ZWSP + "le.com", must_contain=[0x200D, 0x200B],
   ctx={"HOST"}, risk={"HIGH"}, verdict={"hold_pending_review"}, witness={"U+200B"},
   basis="ZWJ breaks the host label -> HOST/HIGH. The co-present ZWSP (uncarded in this "
         "ZWJ-scoped battery) MUST still witness -> tests the no-suppression invariant "
         "(a strong known verdict must not swallow a co-present uncarded invisible)."),
 C(id="Z9", cls="dangerous", input="goog%E2%80%8Dle.com", must_contain=[],
   decoded_input="goog" + ZWJ + "le.com", decoded_must_contain=[0x200D],
   ctx={"-"}, risk={"-"}, verdict={"pass"}, witness=set(),
   decoded_ctx={"HOST"}, decoded_risk={"HIGH"}, decoded_verdict={"hold_pending_review"},
   basis="Stage1 RAW: percent-escaped, no literal U+200D -> ZWJ card must NOT falsely "
         "fire on %E2%80%8D. Stage2 POST-DECODE: bytes -> U+200D -> HOST/HIGH."),
 C(id="Z10", cls="controls", input="the zero width joiner is U plus 200D", must_contain=[],
   ctx={"-"}, risk={"-"}, verdict={"pass"}, witness=set(),
   basis="Mention != use: prose ABOUT ZWJ with no actual U+200D char -> no relation "
         "verdict, pass, no witness (card SAFE_CASE_003 mention)."),
 C(id="Z11", cls="controls", input="just plain text here", must_contain=[],
   ctx={"-"}, risk={"-"}, verdict={"pass"}, witness=set(),
   basis="Negative control: ordinary text, no ZWJ -> pass, no witness flood."),
]

BOM_MANIFEST = [
 C(id="B1", cls="observation", input=BOM + "hello world", must_contain=[0xFEFF],
   ctx={"BYTE_EXACT_TOKEN", "HIDDEN_BOUNDARY_PADDING"}, risk={"MEDIUM"},
   verdict={"queue_for_review"}, witness=set(),
   forbidden={"verdict": {"pass", "hold_pending_review"}},
   basis="Leading BOM in an application text string. Card OBSERVATION_LEVEL: a BOM that "
         "survived into an application string is an observation (application-string != "
         "transport-stream) -> POSSIBLE (queue), not a silent CLEAN. FORBIDDEN pass."),
 C(id="B1J", cls="observation", input=BOM + '{"k":"v"}', must_contain=[0xFEFF],
   ctx={"FREE_TEXT", "-"}, risk={"NONE", "-"}, verdict={"pass"}, witness=set(),
   basis="Leading BOM directly before a JSON/structure = TRANSPORT_LIKE_POSITION, the "
         "canonical legitimate spot for an encoding marker -> CLEAN (card SAFE_CASE_002 "
         "after B1 refinement)."),
 C(id="B2", cls="dangerous", input="pay" + BOM + "pal.com", must_contain=[0xFEFF],
   ctx={"HOST"}, risk={"HIGH"}, verdict={"hold_pending_review"}, witness=set(),
   differential=True, forbidden={"verdict": {"pass"}},
   basis="BOM inside a host label = domain-label evasion (the mid-stream zero-width role "
         "is deprecated since Unicode 3.2). HOST/HIGH, NEVER a silent pass."),
 C(id="B3", cls="url", input="us" + BOM + "er@example.com", must_contain=[0xFEFF],
   ctx={"EMAIL"}, risk={"MEDIUM"}, verdict={"queue_for_review"}, witness=set(),
   forbidden={"ctx": {"HOST"}, "risk": {"HIGH"}},
   basis="BOM before @ -> email local-part split -> EMAIL/MEDIUM. FORBIDDEN HOST/HIGH."),
 C(id="B4", cls="boundary", input="bad" + BOM + "word", must_contain=[0xFEFF],
   ctx={"BYTE_EXACT_TOKEN"}, risk={"MEDIUM"}, verdict={"queue_for_review"}, witness=set(),
   forbidden={"verdict": {"pass"}},
   basis="BOM in a no-space token defeats byte-exact matching -> BYTE_EXACT_TOKEN/MEDIUM."),
 C(id="B5", cls="positions", input=BOM + "paypal.com", must_contain=[0xFEFF],
   ctx={"HIDDEN_BOUNDARY_PADDING"}, risk={"MEDIUM"}, verdict={"queue_for_review"}, witness=set(),
   forbidden={"verdict": {"pass"}, "risk": {"HIGH"}},
   basis="Leading BOM before a whole domain -> hidden padding, not a label break but not "
         "a silent pass -> HIDDEN_BOUNDARY_PADDING/MEDIUM."),
 C(id="B6", cls="positions", input="paypal.com" + BOM, must_contain=[0xFEFF],
   ctx={"HIDDEN_BOUNDARY_PADDING"}, risk={"MEDIUM"}, verdict={"queue_for_review"}, witness=set(),
   forbidden={"risk": {"HIGH"}},
   basis="Trailing BOM padding after a complete domain -> HIDDEN_BOUNDARY_PADDING/MEDIUM."),
 C(id="B7", cls="combo", input="pay" + BOM + ZWSP + "pal.com", must_contain=[0xFEFF, 0x200B],
   ctx={"HOST"}, risk={"HIGH"}, verdict={"hold_pending_review"}, witness={"U+200B"},
   basis="BOM breaks the host label -> HOST/HIGH. Co-present ZWSP (uncarded in this "
         "BOM-scoped battery) MUST still witness -> no-suppression invariant."),
 C(id="B8", cls="dangerous", input="pay%EF%BB%BFpal.com", must_contain=[],
   decoded_input="pay" + BOM + "pal.com", decoded_must_contain=[0xFEFF],
   ctx={"-"}, risk={"-"}, verdict={"pass"}, witness=set(),
   decoded_ctx={"HOST"}, decoded_risk={"HIGH"}, decoded_verdict={"hold_pending_review"},
   basis="Stage1 RAW: percent-escaped, no literal U+FEFF -> BOM card must NOT falsely "
         "fire on %EF%BB%BF. Stage2 POST-DECODE: bytes -> U+FEFF -> HOST/HIGH."),
 C(id="B9", cls="controls", input="the byte order mark is U plus FEFF", must_contain=[],
   ctx={"-"}, risk={"-"}, verdict={"pass"}, witness=set(),
   basis="Mention != use: prose ABOUT the BOM with no actual U+FEFF -> pass, no witness."),
 C(id="B10", cls="controls", input="just plain text here", must_contain=[],
   ctx={"-"}, risk={"-"}, verdict={"pass"}, witness=set(),
   basis="Negative control: ordinary text, no BOM -> pass, no witness flood."),
]

assert len(ZWJ_MANIFEST) == 11, "expected 11 ZWJ cases, got %d" % len(ZWJ_MANIFEST)
assert len(BOM_MANIFEST) == 11, "expected 11 BOM cases, got %d" % len(BOM_MANIFEST)
