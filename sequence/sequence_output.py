"""
Result structures of SEQUENCE_MODULE_TEMPLATE.

Mirrors OUTPUT_INTERFACE from SEQUENCE_MODULE_TEMPLATE_GEN3_v0_2_PLUS_
EPOCH_v0_1 with PATCH_24/25/26 applied:
  - PATCH_24: SEQUENCE_CANDIDATE_MATCH (single->sequence bridge)
  - PATCH_25: SOURCE_SIGN_LIST (real data) + SOURCE_OCCURRENCE_
    LIST (honest NOT_AVAILABLE stub until positions are fully done)
  - PATCH_26: CROSS_CARD — CARD_SET, CANDIDATE_POOL (union),
    MULTIPLE_MATCHES, CANDIDATE_SOURCE_CARD

IMPORTANT (ENUM_GUARD / RULE_3A): a candidate risk_level may be
either a RiskLevel (enum) or a descriptive string (ALL SKULL SCs
carry string risks: 'intensity-dependent', 'combined idiom' etc.).
The aggregator must NOT blindly compare/maximise a mix of enums
and strings — see SequenceOutput.aggregate_risk.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from sign_core_card import RiskLevel


@dataclass
class SequenceMatch:
    """One fired SEQUENCE_CANDIDATE match in the text."""
    sc_id: str
    sequence: str
    name: str
    risk_level: object              # RiskLevel | str (ENUM_GUARD!)
    candidate_source_card: str      # owner card CODEPOINT (PATCH_26)
    match_start: int                # match start position in the text
    match_end: int                  # end position (exclusive)
    source_sign_offsets: list = field(default_factory=list)  # PATCH_25
    url_context_flag: bool = False  # SOLIDUS_SCHEME_PATCH: "://" marks URL mode.
                                    # The flag only RAISES downstream scrutiny,
                                    # NEVER lowers risk (CLARIFICATION_1).
    scheme_neutralized: bool = False  # True if "//" was part of a "://" scheme and
                                      # risk was lowered to NONE as a legitimate link

    @property
    def risk_is_enum(self) -> bool:
        return RiskLevel.is_enum_value(self.risk_level)

    def as_dict(self) -> dict:
        rl = self.risk_level.value if isinstance(self.risk_level, RiskLevel) else self.risk_level
        return {
            "SC_ID": self.sc_id,
            "SEQUENCE": self.sequence,
            "NAME": self.name,
            "RISK_LEVEL": rl,
            "RISK_IS_ENUM": "YES" if self.risk_is_enum else "NO",
            "CANDIDATE_SOURCE_CARD": self.candidate_source_card,
            "MATCH_START": self.match_start,
            "MATCH_END": self.match_end,
            "SOURCE_SIGN_OFFSETS": list(self.source_sign_offsets),
            "URL_CONTEXT_FLAG": "YES" if self.url_context_flag else "NO",
            "SCHEME_NEUTRALIZED": "YES" if self.scheme_neutralized else "NO",
        }


@dataclass
class SequenceOutput:
    """SEQUENCE_OUTPUT_STATUS — the result of the whole sequence STAGE_1-7."""
    card_set: list = field(default_factory=list)        # PATCH_26: CODEPOINTs
    matches: list = field(default_factory=list)          # list[SequenceMatch]
    multiple_matches: bool = False                       # PATCH_26
    source_sign_list: list = field(default_factory=list) # PATCH_25 (real)
    source_occurrence_list: str = "NOT_AVAILABLE"        # PATCH_25 (honest stub)
    check_unavailable: bool = False                      # PATCH_24 CHECK_UNAVAILABLE
    warnings: list = field(default_factory=list)
    relation_verdicts: list = field(default_factory=list)  # step 4 of the relation axis: mask verdicts (D-REL-4/6)

    def aggregate_risk(self):
        """Aggregated sequence-layer risk.

        ENUM_GUARD (RULE_3A): max is taken ONLY over matches whose
        risk_level is a real enum. Descriptive strings ('intensity-
        dependent' etc.) do NOT join numeric maximisation — they are
        returned as a separate non_enum_risks list for the integrator,
        which decides by policy, not comparison.

        Returns (enum_risk: RiskLevel, non_enum_risks: list[str])."""
        enum_levels = []
        non_enum = []
        for m in self.matches:
            if m.risk_is_enum:
                lv = m.risk_level if isinstance(m.risk_level, RiskLevel) else RiskLevel(m.risk_level)
                enum_levels.append(lv)
            else:
                non_enum.append(str(m.risk_level))
        enum_risk = RiskLevel.max(*enum_levels) if enum_levels else RiskLevel.NONE
        return enum_risk, non_enum

    def as_dict(self) -> dict:
        enum_risk, non_enum = self.aggregate_risk()
        return {
            "CARD_SET": list(self.card_set),
            "MATCHES": [m.as_dict() for m in self.matches],
            "MULTIPLE_MATCHES": "YES" if self.multiple_matches else "NO",
            "AGGREGATE_ENUM_RISK": enum_risk.value,
            "NON_ENUM_RISKS": non_enum,
            "SOURCE_SIGN_LIST": list(self.source_sign_list),
            "SOURCE_OCCURRENCE_LIST": self.source_occurrence_list,
            "CHECK_UNAVAILABLE": "YES" if self.check_unavailable else "NO",
            "WARNINGS": list(self.warnings),
        }
