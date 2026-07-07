"""
Структуры результата SEQUENCE_MODULE_TEMPLATE.

Отражает OUTPUT_INTERFACE из SEQUENCE_MODULE_TEMPLATE_GEN3_v0_2_PLUS_
EPOCH_v0_1 с применёнными PATCH_24/25/26:
  - PATCH_24: SEQUENCE_CANDIDATE_MATCH (мост одиночный→sequence)
  - PATCH_25: SOURCE_SIGN_LIST (реальные данные) + SOURCE_OCCURRENCE_
    LIST (честный стаб NOT_AVAILABLE до полной реализации позиций)
  - PATCH_26: CROSS_CARD — CARD_SET, CANDIDATE_POOL (объединение),
    MULTIPLE_MATCHES, CANDIDATE_SOURCE_CARD

ВАЖНО (ENUM_GUARD / RULE_3A): risk_level кандидата может быть как
RiskLevel (enum), так и описательной строкой (у SKULL ВСЕ SC имеют
строковый risk: 'intensity-dependent', 'combined idiom' и т.п.).
Агрегатор НЕ имеет права слепо сравнивать/максимизировать смесь
enum и строк — см. SequenceOutput.aggregate_risk.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from sign_core_card import RiskLevel


@dataclass
class SequenceMatch:
    """Одно сработавшее совпадение SEQUENCE_CANDIDATE в тексте."""
    sc_id: str
    sequence: str
    name: str
    risk_level: object              # RiskLevel | str (ENUM_GUARD!)
    candidate_source_card: str      # CODEPOINT карты-владельца (PATCH_26)
    match_start: int                # позиция начала совпадения в тексте
    match_end: int                  # позиция конца (эксклюзивно)
    source_sign_offsets: list = field(default_factory=list)  # PATCH_25
    url_context_flag: bool = False  # SOLIDUS_SCHEME_PATCH: "://" помечает URL-режим.
                                    # Флаг только ПОВЫШАЕТ scrutiny downstream,
                                    # НИКОГДА не понижает риск (CLARIFICATION_1).
    scheme_neutralized: bool = False  # True если "//" был частью "://" схемы и
                                      # риск понижен до NONE как легитимная связка

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
    """SEQUENCE_OUTPUT_STATUS — результат всего STAGE_1-7 sequence-слоя."""
    card_set: list = field(default_factory=list)        # PATCH_26: CODEPOINTs
    matches: list = field(default_factory=list)          # list[SequenceMatch]
    multiple_matches: bool = False                       # PATCH_26
    source_sign_list: list = field(default_factory=list) # PATCH_25 (реальные)
    source_occurrence_list: str = "NOT_AVAILABLE"        # PATCH_25 (честный стаб)
    check_unavailable: bool = False                      # PATCH_24 CHECK_UNAVAILABLE
    warnings: list = field(default_factory=list)

    def aggregate_risk(self):
        """Агрегированный риск sequence-слоя.

        ENUM_GUARD (RULE_3A): берём max ТОЛЬКО по тем совпадениям, чей
        risk_level — реальный enum. Описательные строки ('intensity-
        dependent' и т.п.) НЕ участвуют в численной максимизации —
        они возвращаются отдельным списком non_enum_risks для
        интегратора, который решает по политике, а не сравнением.

        Возвращает (enum_risk: RiskLevel, non_enum_risks: list[str])."""
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
