"""
Загрузка SignCoreCard из markdown-файла карточки знака.

load_card(path) -> SignCoreCard

Использует tree_parser (структурный парсер по отступам), не регулярки
под конкретный формат карты — устойчив к расхождениям между картами
(подтверждено на практике: SKULL хранит SEQUENCE_CANDIDATES прямо под
SEQUENCE_LAYER_BOUNDARY, без промежуточного узла, в отличие от DOT и
SOLIDUS; эпохи SOLIDUS не имеют поля NAME, у SKULL — есть).
"""

from __future__ import annotations

import re

from sign_core_card import (
    SignCoreCard, SafeCase, RiskCase, Confusable, ContradictionGuard,
    SequenceCandidate, EpochDefinition, RiskLevel, Zone,
)
from tree_parser import parse_indented_tree, Node


def _parse_risk(raw: str):
    """Возвращает RiskLevel, если raw — точное перечислимое значение
    или начинается с него (например, 'LOW / CONTEXT_DEPENDENT' из
    SKULL.SAFE_CASE_004 → RiskLevel.LOW). Если первый токен не входит
    в RiskLevel (например, SEQUENCE_CANDIDATE 'intensity-dependent',
    'combined idiom', 'epoch_mismatch', 'seasonal_context',
    'spam-like') — возвращает исходную строку как есть (ENUM_GUARD
    в sequence_module.py обязан явно проверять это разграничение,
    не считать такие значения сравнимыми с enum)."""

    raw = raw.strip()
    if not raw:
        return RiskLevel.NONE
    first_token = re.split(r"[\s/(]", raw, maxsplit=1)[0]
    if RiskLevel.is_enum_value(first_token):
        return RiskLevel(first_token)
    return raw  # не-перечислимое значение — оставляем строкой


def _parse_zone(raw: str) -> Zone:
    raw = raw.strip().upper()
    return {
        "ZONE_1": Zone.ZONE_1,
        "ZONE_2": Zone.ZONE_2,
        "ZONE_3": Zone.ZONE_3,
    }[raw]


def _extract_safe_cases(root: Node) -> list:
    section = root.child("SAFE_CASES")
    if not section:
        return []
    out = []
    for sc in section.children_with_prefix("SAFE_CASE_"):
        out.append(SafeCase(
            case_id=sc.key,
            input_example=sc.child("INPUT").text() if sc.child("INPUT") else "",
            context=sc.child("CONTEXT").text() if sc.child("CONTEXT") else "",
            risk=_parse_risk(sc.child("RISK").text() if sc.child("RISK") else "NONE"),
            guard=sc.child("GUARD").text() if sc.child("GUARD") else "",
        ))
    return out


def _extract_risk_cases(root: Node) -> list:
    section = root.child("RISK_CASES")
    if not section:
        return []
    out = []
    for rc in section.children_with_prefix("RISK_CASE_"):
        out.append(RiskCase(
            case_id=rc.key,
            name=rc.child("NAME").text() if rc.child("NAME") else "",
            input_example=rc.child("INPUT").text() if rc.child("INPUT") else "",
            context=rc.child("CONTEXT").text() if rc.child("CONTEXT") else "",
            risk=_parse_risk(rc.child("RISK").text() if rc.child("RISK") else "NONE"),
            attack=rc.child("ATTACK").text() if rc.child("ATTACK") else "",
            guard=rc.child("GUARD").text() if rc.child("GUARD") else "",
        ))
    return out


def _extract_confusables(root: Node) -> list:
    section = root.child("CONFUSABLES")
    if not section:
        return []
    out = []
    for cf in section.children_with_prefix("CONFUSABLE_"):
        out.append(Confusable(
            confusable_id=cf.key,
            visible_form=cf.child("VISIBLE_FORM").text() if cf.child("VISIBLE_FORM") else "",
            codepoint=cf.child("CODEPOINT").text() if cf.child("CODEPOINT") else "",
            name=cf.child("NAME").text() if cf.child("NAME") else "",
            risk=_parse_risk(cf.child("RISK").text() if cf.child("RISK") else "NONE"),
            rule=cf.child("RULE").text() if cf.child("RULE") else "",
        ))
    return out


def _extract_contradiction_guards(root: Node) -> list:
    section = root.child("CONTRADICTION_GUARDS")
    if not section:
        return []
    out = []
    for cg in section.children_with_prefix("CG"):
        out.append(ContradictionGuard(
            guard_id=cg.key,
            trigger=cg.child("TRIGGER").text() if cg.child("TRIGGER") else "",
            response=cg.child("RESPONSE").text() if cg.child("RESPONSE") else "",
            rule=cg.child("RULE").text() if cg.child("RULE") else "",
        ))
    return out


def _extract_sequence_candidates(root: Node) -> list:
    seq = root.child("SEQUENCE_LAYER_BOUNDARY")
    if not seq:
        return []
    # DOT/SOLIDUS: вложенный узел SEQUENCE_CANDIDATES
    sc_container = seq.child("SEQUENCE_CANDIDATES")
    sc_nodes = sc_container.children_with_prefix("SC") if sc_container else []
    # SKULL: SC-узлы прямо под SEQUENCE_LAYER_BOUNDARY (расхождение
    # формата, подтверждено структурным парсером — см. docstring модуля)
    if not sc_nodes:
        sc_nodes = seq.children_with_prefix("SC")

    out = []
    for sc in sc_nodes:
        risk_raw = sc.child("RISK_LEVEL").text() if sc.child("RISK_LEVEL") else "NONE"
        out.append(SequenceCandidate(
            sc_id=sc.key,
            sequence=_strip_quotes(sc.child("SEQUENCE").text() if sc.child("SEQUENCE") else ""),
            name=sc.child("NAME").text() if sc.child("NAME") else "",
            risk_level=_parse_risk(risk_raw),
            possible_contexts=(
                sc.child("POSSIBLE_CONTEXTS").text() if sc.child("POSSIBLE_CONTEXTS")
                else (sc.child("RULE").text() if sc.child("RULE") else "")
            ),
            scope=sc.child("SCOPE").text() if sc.child("SCOPE") else "",
        ))
    return out


def _strip_quotes(s: str) -> str:
    """SEQUENCE-поле в карточках записано как '"../" (комментарий)' —
    достаём только буквальную строку в кавычках."""
    m = re.match(r'^"([^"]*)"', s.strip())
    return m.group(1) if m else s.strip()


def _extract_epochs(root: Node) -> list:
    cap = root.child("CAPTURE_HISTORY")
    if not cap:
        return []
    out = []
    for ep in cap.children_with_prefix("EPOCH_"):
        out.append(EpochDefinition(
            epoch_id=ep.key,
            name=ep.child("NAME").text() if ep.child("NAME") else "",
            date_range=ep.child("DATE_RANGE").text() if ep.child("DATE_RANGE") else "",
            substrate=ep.child("SUBSTRATE").text() if ep.child("SUBSTRATE") else "",
            function=ep.child("FUNCTION").text() if ep.child("FUNCTION") else "",
            status=ep.child("STATUS").text() if ep.child("STATUS") else "",
        ))
    return out


def load_card(path: str) -> SignCoreCard:
    text = open(path, encoding="utf-8").read()
    root = parse_indented_tree(text)

    zone = _parse_zone(root.child("ZONE").text())
    active_epoch_type = None
    if zone == Zone.ZONE_3:
        active_epoch_type = (
            root.child("ACTIVE_EPOCH_TYPE").text()
            if root.child("ACTIVE_EPOCH_TYPE") else None
        )
    elif zone == Zone.ZONE_2:
        active_epoch_type = (
            root.child("EPOCH_TRACKER").text()
            if root.child("EPOCH_TRACKER") else None
        )

    return SignCoreCard(
        card_uid=root.child("CARD_UID").text() if root.child("CARD_UID") else "",
        codepoint=root.child("CODEPOINT").text(),
        visible_form=root.child("VISIBLE_FORM").text(),
        unicode_name=root.child("UNICODE_NAME").text() if root.child("UNICODE_NAME") else "",
        zone=zone,
        document_status=root.child("DOCUMENT_STATUS").text(),
        base_mode=root.child("BASE_MODE").text() if root.child("BASE_MODE") else "",
        base_mode_formula=(
            root.child("BASE_MODE_FORMULA").text()
            if root.child("BASE_MODE_FORMULA") else ""
        ),
        safe_cases=_extract_safe_cases(root),
        risk_cases=_extract_risk_cases(root),
        confusables=_extract_confusables(root),
        contradiction_guards=_extract_contradiction_guards(root),
        sequence_candidates=_extract_sequence_candidates(root),
        epochs=_extract_epochs(root),
        active_epoch_type=active_epoch_type,
    )
