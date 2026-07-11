"""
INTEGRATOR_TEMPLATE engine (single sign).

CAVEAT: implemented after the general architecture confirmed on
SEQUENCE_INTEGRATOR_TEMPLATE in this project (demo policy
ACTION_MAP: NONE/LOW/MEDIUM/HIGH/CRITICAL -> a concrete runtime
action), not as a literal copy of the INTEGRATOR_TEMPLATE_
SINGLE_SIGN document, which is remembered less precisely.
If the author has the exact document text, the logic can be adjusted
later; the interface (input/output) will not change.

Principle (MODULE_MUST_NOT_BLOCK_DIRECTLY): MODULE_TEMPLATE does not
decide "block or not" — it only classifies risk and offers
RECOMMENDED_ACTION as advice. The concrete runtime decision is
exclusively the integrator job, based on a POLICY not baked into
the sign itself.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from sign_core_card import RiskLevel
from output_status import OutputStatus


# Demo policy, by analogy with the already confirmed
# SEQUENCE_INTEGRATOR_POLICY (see SEQUENCE_PIPELINE_*_RUN rounds)
DEFAULT_ACTION_MAP = {
    RiskLevel.NONE: "pass",
    RiskLevel.LOW: "log_only",
    RiskLevel.MEDIUM: "queue_for_review",
    RiskLevel.HIGH: "hold_pending_review",
    RiskLevel.CRITICAL: "escalate_to_human",
}


@dataclass
class RuntimeActionRequest:
    sign_codepoint: str
    offset_start: int
    offset_end: int
    runtime_action: str
    action_rationale: str
    risk_level: str
    ambiguity_handled: bool = False

    def as_dict(self) -> dict:
        return {
            "SIGN_CODEPOINT": self.sign_codepoint,
            "SIGN_OFFSET_START": self.offset_start,
            "SIGN_OFFSET_END": self.offset_end,
            "RUNTIME_ACTION_REQUEST": self.runtime_action,
            "ACTION_RATIONALE": self.action_rationale,
            "RISK_LEVEL": self.risk_level,
            "AMBIGUITY_HANDLED": "YES" if self.ambiguity_handled else "NO",
        }


def process_output(status: OutputStatus,
                    action_map: dict = None) -> RuntimeActionRequest:
    """STAGE_1 (input validation) + STAGE_2 (policy action selection)
    + STAGE_3 (RUNTIME_ACTION_REQUEST assembly)."""

    action_map = action_map or DEFAULT_ACTION_MAP

    # STAGE_1: INPUT_VALIDATION — OUTPUT_STATUS must be valid
    if status.effect_fields_status != "VALID":
        raise ValueError(
            f"INTEGRATOR_INPUT_INVALID: EFFECT_FIELDS_STATUS={status.effect_fields_status}"
        )

    # STAGE_2: ACTION_SELECTION
    base_action = action_map.get(status.risk_level, "pass")

    rationale_parts = [f"risk_level={status.risk_level.value}"]
    if status.risk_cases_triggered:
        rationale_parts.append(f"risk_cases={','.join(status.risk_cases_triggered)}")
    if status.guards_triggered:
        rationale_parts.append(f"guards={','.join(status.guards_triggered)}")
    if status.ambiguity_flag:
        rationale_parts.append("ambiguity_flag=YES")

    # AMBIGUITY: when context is ambiguous (AMBIGUITY_FLAG=YES),
    # the action is not lowered below queue_for_review even if
    # RISK_LEVEL alone is NONE/LOW (advisory escalation)
    final_action = base_action
    if status.ambiguity_flag and base_action in ("pass", "log_only"):
        final_action = "queue_for_review"
        rationale_parts.append("escalated_due_to_ambiguity")

    # STAGE_3: OUTPUT_ASSEMBLY
    return RuntimeActionRequest(
        sign_codepoint=status.sign_codepoint,
        offset_start=status.sign_offset_start,
        offset_end=status.sign_offset_end,
        runtime_action=final_action,
        action_rationale="; ".join(rationale_parts),
        risk_level=status.risk_level.value,
        ambiguity_handled=status.ambiguity_flag,
    )
