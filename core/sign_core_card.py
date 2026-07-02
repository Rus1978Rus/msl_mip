"""
MSL/MIP — базовые типы данных.

Реализует структуру данных SIGN_CORE_CARD в виде Python dataclass-ов.
Соответствует SIGN_CORE_CARD_TEMPLATE_GEN3_v0_3_RU и трём подтверждённым
(ARTIFACT_CONFIRMED) картам: DOT, SOLIDUS, SKULL.

ВАЖНО: это РЕАЛИЗАЦИЯ спецификации, не сама спецификация. Если реальный
код расходится с текстом шаблонов — это повод пересмотреть код или
формально патчить шаблон через AUTHOR_DECISION, не тихо менять поведение.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class RiskLevel(Enum):
    """Перечислимые уровни риска. ВАЖНО: некоторые SEQUENCE_CANDIDATE
    в карточках (например SKULL.SC1) имеют НЕ-перечислимый, описательный
    RISK_LEVEL ('intensity-dependent') — такие случаи представлены как
    обычная строка, не как член этого enum (см. RULE_3A / ENUM_GUARD
    в sequence_module.py)."""

    NONE = "NONE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

    @classmethod
    def is_enum_value(cls, value) -> bool:
        """ENUM_GUARD: проверка, что значение — реальный член RiskLevel,
        а не описательная строка типа 'intensity-dependent'."""
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
    """ZONE из LAYER_A карточки. Определяет, по какому STAGE_3x идёт
    обработка в MODULE_TEMPLATE (см. STAGE_2 ZONE_DETECTION)."""

    ZONE_1 = 1  # STABLE — семантика не зависит от контекста/эпохи
    ZONE_2 = 2  # CONTEXT_DEPENDENT — контекст выбирает SUBSTRATE
    ZONE_3 = 3  # PRECESSIONAL — культурные эпохи, EPOCH_MATCHING


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
class ContradictionGuard:
    guard_id: str
    trigger: str
    response: str
    rule: str = ""


@dataclass
class SequenceCandidate:
    """SC из раздела SEQUENCE_LAYER_BOUNDARY. RISK_LEVEL может быть как
    RiskLevel (enum), так и описательной строкой (например
    'intensity-dependent' у SKULL.SC1) — см. ENUM_GUARD в STAGE_3
    SEQUENCE_MODULE."""

    sc_id: str
    sequence: str
    name: str
    risk_level: object  # RiskLevel | str
    possible_contexts: str = ""
    scope: str = ""  # "" (обычный) | "UPSTREAM_DEPENDENT" (см. SOLIDUS.SC7)


@dataclass
class EpochDefinition:
    """Запись CAPTURE_HISTORY для ZONE_3 знаков (SEMANTIC_EPOCH_TRACKER).
    Используется EPOCH_MATCHING (STAGE_3c MODULE_TEMPLATE) для подсчёта
    MATCH_SCORE."""

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
    """Полная карточка знака — то подмножество полей SIGN_CORE_CARD,
    которое реально потребляется MODULE_TEMPLATE / SEQUENCE_MODULE_TEMPLATE
    в их текущем (патченом) виде."""

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
    contradiction_guards: list = field(default_factory=list)
    sequence_candidates: list = field(default_factory=list)

    epochs: list = field(default_factory=list)
    active_epoch_type: Optional[str] = None

    def find_sequence_candidate_by_literal(self, text: str):
        """Точное буквальное совпадение SEQUENCE.
        Используется STAGE_2a SEQUENCE_MODULE (PATCH_24/26)."""
        for sc in self.sequence_candidates:
            if sc.sequence == text:
                return sc
        return None
