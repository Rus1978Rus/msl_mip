"""
Движок INTEGRATOR_TEMPLATE (одиночный знак).

ОГОВОРКА: реализовано по общей архитектуре, подтверждённой на
SEQUENCE_INTEGRATOR_TEMPLATE в этом же проекте (демо-политика
ACTION_MAP: NONE/LOW/MEDIUM/HIGH/CRITICAL → конкретное runtime-
действие), а не как буквальная копия текста INTEGRATOR_TEMPLATE_
SINGLE_SIGN — этот документ я помню менее точно, чем MODULE_TEMPLATE.
Если у автора есть точный текст документа — логику можно поправить
под него позже, интерфейс (вход/выход) для этого не изменится.

Принцип (MODULE_MUST_NOT_BLOCK_DIRECTLY): MODULE_TEMPLATE сам не
решает, "блокировать" или нет — он только классифицирует риск и
даёт RECOMMENDED_ACTION как совет. Конкретное runtime-решение —
исключительно работа интегратора, на основе ПОЛИТИКИ, не встроенной
в сам знак.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from sign_core_card import RiskLevel
from output_status import OutputStatus


# Демо-политика, по аналогии с уже подтверждённой
# SEQUENCE_INTEGRATOR_POLICY (см. SEQUENCE_PIPELINE_*_RUN раунды)
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
    """STAGE_1 (валидация входа) + STAGE_2 (выбор действия по политике)
    + STAGE_3 (сборка RUNTIME_ACTION_REQUEST)."""

    action_map = action_map or DEFAULT_ACTION_MAP

    # STAGE_1: INPUT_VALIDATION — OUTPUT_STATUS должен быть валиден
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

    # AMBIGUITY: если контекст неоднозначен (AMBIGUITY_FLAG=YES),
    # действие не понижается ниже queue_for_review, даже если
    # RISK_LEVEL сам по себе NONE/LOW (advisory escalation)
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
