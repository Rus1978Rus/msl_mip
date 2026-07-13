"""
MSL/MIP — core data types.

Implements the SIGN_CORE_CARD data structure as Python dataclasses.
Matches SIGN_CORE_CARD_TEMPLATE_GEN3_v0_3 and the three confirmed
(ARTIFACT_CONFIRMED) cards: DOT, SOLIDUS, SKULL.

IMPORTANT: this is an IMPLEMENTATION of the spec, not the spec itself.
If real code diverges from the template text, either revisit the code
or patch the template formally via AUTHOR_DECISION — never silently.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class RiskLevel(Enum):
    """Enumerated risk levels. NOTE: some SEQUENCE_CANDIDATEs in cards
    (e.g. SKULL.SC1) carry a NON-enumerable, descriptive RISK_LEVEL
    ('intensity-dependent') — such cases are stored as a plain string,
    not as a member of this enum (see RULE_3A / ENUM_GUARD
    in sequence_module.py)."""

    NONE = "NONE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

    @classmethod
    def is_enum_value(cls, value) -> bool:
        """ENUM_GUARD: check that a value is a real RiskLevel member,
        not a descriptive string like 'intensity-dependent'."""
        if isinstance(value, RiskLevel):
            return True
        if isinstance(value, str):
            return value in cls._value2member_map_
        return False

    @staticmethod
    def max(*levels: "RiskLevel") -> "RiskLevel":
        order = [RiskLevel.NONE, RiskLevel.LOW, RiskLevel.MEDIUM,
                 RiskLevel.HIGH, RiskLevel.CRITICAL]
        present = [lv for lv in levels if lv is not None]
        if not present:
            return RiskLevel.NONE
        return max(present, key=lambda lv: order.index(lv))


class Zone(Enum):
    """ZONE from the card LAYER_A. Selects the STAGE_3x processing path
    in MODULE_TEMPLATE (see STAGE_2 ZONE_DETECTION)."""

    ZONE_1 = 1  # STABLE — semantics independent of context/epoch
    ZONE_2 = 2  # CONTEXT_DEPENDENT — context selects the SUBSTRATE
    ZONE_3 = 3  # PRECESSIONAL — cultural epochs, EPOCH_MATCHING


@dataclass
class SafeCase:
    case_id: str
    input_example: str
    context: str
    risk: RiskLevel = RiskLevel.NONE
    guard: str = ""
    substrate_hint: Optional[str] = None


@dataclass
class RiskCase:
    case_id: str
    name: str
    input_example: str
    context: str
    risk: RiskLevel
    attack: str = ""
    guard: str = ""
    substrate_hint: Optional[str] = None


@dataclass
class Confusable:
    confusable_id: str
    visible_form: str
    codepoint: str
    name: str
    risk: RiskLevel
    rule: str = ""


@dataclass
class SignRelation:
    """Relation edge between signs (relation axis,
    AUTHOR_DECISION_20260708, D-REL-2). SOURCE OF TRUTH for the runtime.
    An edge by itself is NOT risk: RUNTIME_EFFECT=RELATION_ONLY,
    RELATION_FOUND != THREAT. Mask risk is decided by the sequence layer."""
    relation_id: str
    relation_type: str = ""          # mimicry: CONFUSABLE_OF / NFKC_MAPS_TO / VISUAL_MIMIC_OF; invisible (D-INV-1): BOUNDARY_DISRUPTOR / INVISIBLE_CLASS_COLLISION / ABSENCE_CONFUSABLE
    target: str = ""                 # canon codepoint/sequence; OPTIONAL when target_kind != CODEPOINT (D-INV-3)
    target_kind: str = "CODEPOINT"   # D-INV-3: CODEPOINT / EMPTY_SEQUENCE / CLASS. Explicit enum, never an empty string (empty = "forgot to fill / parser missed it" = a silent pass). Absent in a card -> CODEPOINT (legacy cards unaffected).
    context_scope: list = field(default_factory=list)  # URL/HOST/PORT/PATH/EMAIL/IDENTIFIER/IDN/CODE/FREE_TEXT/ANY
    verification_status: str = ""    # VERIFIED / CANDIDATE / MANUAL_OVERRIDE
    runtime_effect: str = "RELATION_ONLY"  # hard invariant
    is_active: bool = True                  # edge can be disabled without deletion (experiments with "disabled" masks)
    invalid: bool = False                   # Level 3 (Z3-02): a CONTRACT violation (unknown type/kind, CODEPOINT w/o TARGET, EMPTY_SEQUENCE w/ TARGET). An invalid edge is NOT silently activated NOR silently dropped — it is surfaced.
    validation_warnings: list = field(default_factory=list)  # bad edge fields (unknown scope/type, effect != RELATION_ONLY)


@dataclass
class ContradictionGuard:
    guard_id: str
    trigger: str
    response: str
    rule: str = ""


@dataclass
class SequenceCandidate:
    """SC from SEQUENCE_LAYER_BOUNDARY. RISK_LEVEL may be either a
    RiskLevel (enum) or a descriptive string (e.g.
    'intensity-dependent' in SKULL.SC1) — see ENUM_GUARD in STAGE_3.
    SEQUENCE_MODULE."""

    sc_id: str
    sequence: str
    name: str
    risk_level: object  # RiskLevel | str
    possible_contexts: str = ""
    scope: str = ""  # "" (normal) | "UPSTREAM_DEPENDENT" (see SOLIDUS.SC7)


@dataclass
class EpochDefinition:
    """A CAPTURE_HISTORY record for ZONE_3 signs (SEMANTIC_EPOCH_TRACKER).
    Used by EPOCH_MATCHING (STAGE_3c MODULE_TEMPLATE) MATCH_SCORE counting."""

    epoch_id: str
    name: str
    date_range: str
    substrate: str
    function: str
    status: str  # ACTIVE / DORMANT_*
    substrate_keywords: tuple = field(default_factory=tuple)
    function_keywords: tuple = field(default_factory=tuple)


@dataclass
class SignCoreCard:
    """Full sign card — the subset of SIGN_CORE_CARD fields actually
    consumed by MODULE_TEMPLATE / SEQUENCE_MODULE_TEMPLATE
    in their current (patched) form."""

    card_uid: str
    codepoint: str
    visible_form: str
    unicode_name: str
    zone: Zone
    document_status: str

    base_mode: str
    base_mode_formula: str

    safe_cases: list = field(default_factory=list)
    risk_cases: list = field(default_factory=list)
    confusables: list = field(default_factory=list)
    relations: list = field(default_factory=list)  # SignRelation, relation axis (D-REL-2); empty = no active relations (legacy/D1)
    contradiction_guards: list = field(default_factory=list)
    sequence_candidates: list = field(default_factory=list)

    epochs: list = field(default_factory=list)
    active_epoch_type: Optional[str] = None

    def find_sequence_candidate_by_literal(self, text: str):
        """Exact literal SEQUENCE match.
        Used by STAGE_2a SEQUENCE_MODULE (PATCH_24/26)."""
        for sc in self.sequence_candidates:
            if sc.sequence == text:
                return sc
        return None
