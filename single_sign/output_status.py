"""
Структуры результата MODULE_TEMPLATE_SINGLE_SIGN.

Поля OutputStatus соответствуют OUTPUT_INTERFACE.OUTPUT_STATUS из
MODULE_TEMPLATE_SINGLE_SIGN_GEN3_v0_2_PLUS_EPOCH_v0_1, включая
SIGN_OFFSET_START/END, добавленные патчем v0_1_PATCH_23 (закрытие
QUESTION_6 — пробрасывание позиции знака для SEQUENCE_MODULE).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from sign_core_card import RiskLevel


# RECOMMENDED_ACTION mapping — из OUTPUT_INTERFACE MODULE_TEMPLATE
_ACTION_MAP = {
    RiskLevel.NONE: "INFO",
    RiskLevel.LOW: "MONITOR",
    RiskLevel.MEDIUM: "FLAG_FOR_REVIEW",
    RiskLevel.HIGH: "HUMAN_REVIEW",
    RiskLevel.CRITICAL: "ESCALATE_TO_INTEGRATOR",
}


@dataclass
class OutputStatus:
    sign_codepoint: str
    card_version: str
    active_epoch: str  # значение эпохи или "NOT_APPLICABLE"
    interpretation: str
    risk_level: RiskLevel
    risk_cases_triggered: list = field(default_factory=list)
    guards_triggered: list = field(default_factory=list)
    confidence_score: float = 1.0
    ambiguity_flag: bool = False
    effect_fields_status: str = "VALID"
    layer_anomaly_flag: bool = False
    output_warnings: list = field(default_factory=list)
    sign_offset_start: int = 0
    sign_offset_end: int = 0

    @property
    def recommended_action(self) -> str:
        return _ACTION_MAP.get(self.risk_level, "INFO")

    def as_dict(self) -> dict:
        return {
            "SIGN_CODEPOINT": self.sign_codepoint,
            "CARD_VERSION": self.card_version,
            "ACTIVE_EPOCH": self.active_epoch,
            "INTERPRETATION": self.interpretation,
            "RISK_LEVEL": self.risk_level.value,
            "RISK_CASES_TRIGGERED": list(self.risk_cases_triggered),
            "GUARDS_TRIGGERED": list(self.guards_triggered),
            "CONFIDENCE_SCORE": self.confidence_score,
            "AMBIGUITY_FLAG": "YES" if self.ambiguity_flag else "NO",
            "RECOMMENDED_ACTION": self.recommended_action,
            "EFFECT_FIELDS_STATUS": self.effect_fields_status,
            "LAYER_ANOMALY_FLAG": "YES" if self.layer_anomaly_flag else "NO",
            "OUTPUT_WARNINGS": list(self.output_warnings),
            "SIGN_OFFSET_START": self.sign_offset_start,
            "SIGN_OFFSET_END": self.sign_offset_end,
        }


@dataclass
class ErrorStatus:
    """ERROR_INTERFACE MODULE_TEMPLATE."""
    error_type: str
    detail: str = ""

    def as_dict(self) -> dict:
        return {"ERROR_TYPE": self.error_type, "DETAIL": self.detail}


class ModuleError(Exception):
    """Исключение, оборачивающее ERROR_INTERFACE ERROR_TYPE."""

    def __init__(self, error_type: str, detail: str = ""):
        super().__init__(f"{error_type}: {detail}")
        self.error_type = error_type
        self.detail = detail
