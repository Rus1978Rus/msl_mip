"""
SEQUENCE_INTEGRATOR_TEMPLATE engine.

Takes SequenceOutput (from sequence_engine) and produces the runtime
decision for sequences. Implements the resolution policy, including
PATCH_24 (optional SEQUENCE_CANDIDATE_MATCH in INPUT_INTERFACE +
CHECK_7 — correct presence/absence handling).

KEY PRINCIPLE (ENUM_GUARD / RULE_3A at the integrator level):
enum risks resolve via DEFAULT_ACTION_MAP (as in the single-sign
integrator), while NON-enum risks ('intensity-dependent', 'combined
idiom', 'spam-like' etc.) are NEVER compared with enums nor
maximised — they get a separate NON_ENUM_ACTION_MAP because their
semantics are contextual, not ordinal. If a string has no table
entry — an honest queue_for_review fallback (we do not guess the
level).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from sign_core_card import RiskLevel
from sequence_output import SequenceOutput


# enum risks — the same demo policy as the single-sign integrator
DEFAULT_ACTION_MAP = {
    RiskLevel.NONE: "pass",
    RiskLevel.LOW: "log_only",
    RiskLevel.MEDIUM: "queue_for_review",
    RiskLevel.HIGH: "hold_pending_review",
    RiskLevel.CRITICAL: "escalate_to_human",
}

# NON-enum SKULL.SC* risks are contextual strings. The action is
# assigned by the string meaning, NOT by deriving a numeric level.
# Values are a demo-policy engineering decision; replace with the
# prescribed ones if the card/INTEGRATOR_TEMPLATE specifies them.
NON_ENUM_ACTION_MAP = {
    "intensity-dependent": "queue_for_review",   # 💀💀💀 — tone-dependent
    "combined idiom": "log_only",                # 💀😭 — a stable idiom
    "epoch_mismatch": "queue_for_review",        # 💀☠️ — epoch mixing
    "seasonal_context": "pass",                  # 💀🎃 — seasonal context
    "spam-like": "hold_pending_review",          # 💀💀💀💀💀 — a spam pattern
}

# action priority for picking the strictest among several
_ACTION_SEVERITY = {
    "pass": 0,
    "log_only": 1,
    "queue_for_review": 2,
    "hold_pending_review": 3,
    "escalate_to_human": 4,
}


@dataclass
class SequenceRuntimeDecision:
    runtime_action: str
    action_rationale: str
    enum_risk: str
    non_enum_risks: list = field(default_factory=list)
    matched_sequences: list = field(default_factory=list)
    check_unavailable_handled: bool = False

    def as_dict(self) -> dict:
        return {
            "RUNTIME_ACTION_REQUEST": self.runtime_action,
            "ACTION_RATIONALE": self.action_rationale,
            "AGGREGATE_ENUM_RISK": self.enum_risk,
            "NON_ENUM_RISKS": list(self.non_enum_risks),
            "MATCHED_SEQUENCES": list(self.matched_sequences),
            "CHECK_UNAVAILABLE_HANDLED": "YES" if self.check_unavailable_handled else "NO",
        }


def _most_severe(actions: list) -> str:
    if not actions:
        return "pass"
    return max(actions, key=lambda a: _ACTION_SEVERITY.get(a, 0))


def process_sequence_output(seq_out: SequenceOutput,
                            action_map: dict = None,
                            non_enum_map: dict = None) -> SequenceRuntimeDecision:
    """STAGE_1-3 SEQUENCE_INTEGRATOR."""
    action_map = action_map or DEFAULT_ACTION_MAP
    non_enum_map = non_enum_map or NON_ENUM_ACTION_MAP

    # --- STAGE_1: INPUT_VALIDATION + CHECK_7 (PATCH_24) ---
    # CHECK_UNAVAILABLE / no matches is handled softly:
    # no SEQUENCE_CANDIDATE_MATCH is a legitimate case (single signs
    # without sequences), not an error.
    if seq_out.check_unavailable:
        return SequenceRuntimeDecision(
            runtime_action="pass",
            action_rationale="check_unavailable=" + ";".join(seq_out.warnings or ["true"]),
            enum_risk="NONE",
            check_unavailable_handled=True,
        )

    if not seq_out.matches:
        return SequenceRuntimeDecision(
            runtime_action="pass",
            action_rationale="no_sequence_candidate_match (single signs only)",
            enum_risk="NONE",
            check_unavailable_handled=True,
        )

    # --- STAGE_2: RISK_RESOLUTION (ENUM_GUARD) ---
    enum_risk, non_enum_risks = seq_out.aggregate_risk()

    candidate_actions = [action_map.get(enum_risk, "pass")]
    rationale_parts = [f"enum_risk={enum_risk.value}"]

    for ner in non_enum_risks:
        act = non_enum_map.get(ner, "queue_for_review")  # honest fallback
        candidate_actions.append(act)
        if ner not in non_enum_map:
            rationale_parts.append(f"non_enum[{ner}]=UNKNOWN->queue_for_review")
        else:
            rationale_parts.append(f"non_enum[{ner}]={act}")

    final_action = _most_severe(candidate_actions)

    matched = [f"{m.sc_id}:{m.sequence}({m.candidate_source_card})"
               for m in seq_out.matches]
    if seq_out.multiple_matches:
        rationale_parts.append("MULTIPLE_MATCHES")

    # --- STAGE_3: OUTPUT_ASSEMBLY ---
    return SequenceRuntimeDecision(
        runtime_action=final_action,
        action_rationale="; ".join(rationale_parts),
        enum_risk=enum_risk.value,
        non_enum_risks=non_enum_risks,
        matched_sequences=matched,
    )
