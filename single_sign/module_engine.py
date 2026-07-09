"""
Движок MODULE_TEMPLATE_SINGLE_SIGN — реализация STAGE_1-8 из
MODULE_TEMPLATE_SINGLE_SIGN_GEN3_v0_2_PLUS_EPOCH_v0_1 (с учётом
PATCH_22 — ZONE_1 обязан сверять RISK_CASES, и PATCH_23 —
SIGN_OFFSET_START/END в OUTPUT_STATUS).

Этот модуль НЕ содержит знако-специфичной логики — она в matchers/.
Здесь только структурный pipeline, общий для любого знака любой ZONE.
"""

from __future__ import annotations

from sign_core_card import SignCoreCard, RiskLevel, Zone
from output_status import OutputStatus, ModuleError
from matchers import dot_matcher, solidus_matcher, skull_matcher

import importlib.util as _importlib_util

_skull_crossbones_path = _importlib_util.find_spec("matchers.skull_crossbones_matcher")
if _skull_crossbones_path is not None:
    # файл существует — импортируем без try/except: если внутри него
    # сломан собственный импорт или другая ошибка, она должна упасть
    # ГРОМКО, не маскироваться как "файла нет" (найдено по итогам
    # код-ревью, 2026-06-29: широкий except ImportError скрывал бы
    # реальные баги внутри нового матчера)
    from matchers import skull_crossbones_matcher
    _HAS_SKULL_CROSSBONES = True
else:
    # файла действительно нет — легитимный, осознанный fallback
    _HAS_SKULL_CROSSBONES = False

_at_path = _importlib_util.find_spec("matchers.at_matcher")
if _at_path is not None:
    from matchers import at_matcher
    _HAS_AT = True
else:
    _HAS_AT = False

# ИСПРАВЛЕНО (2026-06-29, добавление второго ZONE_3-знака ☠️):
# раньше диспетчеризация шла ПО ЗОНЕ (ZONE_3 -> только skull_matcher
# жёстко). Это работало, пока в ZONE_3 был один знак. С появлением
# ☠️ (тоже ZONE_3, тоже эпохальный) жёсткий if/elif по зоне не может
# выбрать между двумя матчерами одной зоны. Теперь диспетчеризация —
# по CODEPOINT, через явный реестр. has_epoch=True означает, что
# матчер принимает metadata и возвращает 4-tuple (как skull_matcher),
# False — обычный 3-tuple (как dot/solidus_matcher). Новый знак
# добавляется одной строкой в реестр, без изменения логики ниже.
_MATCHER_REGISTRY = {
    "U+002E": (dot_matcher, False),
    "U+002F": (solidus_matcher, False),
    "U+1F480": (skull_matcher, True),
}
if _HAS_SKULL_CROSSBONES:
    _MATCHER_REGISTRY["U+2620"] = (skull_crossbones_matcher, True)
if _HAS_AT:
    _MATCHER_REGISTRY["U+0040"] = (at_matcher, False)


# STAGE_1: допустимые статусы карточки для загрузки.
# WORKINGLY_CLOSED / ARTIFACT_CONFIRMED — прошли STRUCTURAL_PREFLIGHT_
# PASS + CONVEYOR_REVIEW_PASS (минимум несколько независимых
# ревьюеров) и AUTHOR_DECISION. WORKING_DRAFT — НЕ прошли конвейер;
# допускается к загрузке ТОЛЬКО с явным громким предупреждением (см.
# ниже) — система не имеет права молча путать непроверенный черновик
# с конвейерно подтверждённой карточкой. ИСПРАВЛЕНО (2026-06-29): до
# этого координатор присваивал WORKINGLY_CLOSED карточкам без
# реального прогона конвейера, просто чтобы карточка технически
# загрузилась — это нарушение AUTHOR_DECISION_STATUS_AUTHORITY.
_VALID_STATUSES = {"WORKINGLY_CLOSED", "ARTIFACT_CONFIRMED"}
_DRAFT_STATUSES = {"WORKING_DRAFT"}

def _find_case(card: SignCoreCard, case_id: str):
    """Ищет SAFE_CASE или RISK_CASE по id в карточке."""
    for c in card.safe_cases:
        if c.case_id == case_id:
            return c
    for c in card.risk_cases:
        if c.case_id == case_id:
            return c
    return None


def _guards_for_risk_ids(card: SignCoreCard, risk_ids: list) -> list:
    """STAGE_4: GUARD_EVALUATION — какие CONTRADICTION_GUARDS
    логически связаны с сработавшими RISK_CASE (через текст GUARD
    самого risk_case, сопоставленный с RESPONSE guard'а)."""
    guards_triggered = []
    for rid in risk_ids:
        rc = _find_case(card, rid)
        if rc is None or not getattr(rc, "guard", ""):
            continue
        for g in card.contradiction_guards:
            if g.response and g.response in rc.guard or rc.guard in (g.response or ""):
                if g.guard_id not in guards_triggered:
                    guards_triggered.append(g.guard_id)
    return guards_triggered


def _risk_level_for_ids(card: SignCoreCard, risk_ids: list) -> RiskLevel:
    levels = []
    for rid in risk_ids:
        rc = _find_case(card, rid)
        if rc is not None and RiskLevel.is_enum_value(rc.risk):
            levels.append(rc.risk if isinstance(rc.risk, RiskLevel) else RiskLevel(rc.risk))
    return RiskLevel.max(*levels) if levels else RiskLevel.NONE


def process_sign(card: SignCoreCard, text: str, offset: int,
                  metadata: dict = None) -> OutputStatus:
    """STAGE_1-8 целиком. text[offset] должен совпадать с
    card.visible_form (STAGE_2 CONFUSABLE_CHECK)."""

    # --- STAGE_1: CARD_LOADING ---
    draft_warning = None
    if card.document_status in _DRAFT_STATUSES:
        draft_warning = (
            f"CARD_NOT_CONVEYOR_REVIEWED: {card.card_uid or card.codepoint} "
            f"имеет статус WORKING_DRAFT — не прошла STRUCTURAL_PREFLIGHT_PASS/"
            f"CONVEYOR_REVIEW_PASS. Результат для этого знака НЕ ДОЛЖЕН "
            f"считаться надёжным."
        )
        print(f"[CARD_WARNING] {draft_warning}")
    elif card.document_status not in _VALID_STATUSES:
        raise ModuleError("CARD_INVALID",
                           f"DOCUMENT_STATUS={card.document_status} недопустим")

    # --- STAGE_2: ZONE_DETECTION + CONFUSABLE_CHECK ---
    if offset < 0 or offset >= len(text):
        raise ModuleError("CONTEXT_INSUFFICIENT", "offset вне текста")
    if text[offset] != card.visible_form:
        raise ModuleError("CONFUSABLE_DETECTED_REJECTED",
                           f"text[{offset}]={text[offset]!r} != {card.visible_form!r}")

    ambiguity = False
    active_epoch = "NOT_APPLICABLE"

    # --- STAGE_3: диспетчеризация по CODEPOINT (не по ZONE) ---
    entry = _MATCHER_REGISTRY.get(card.codepoint)
    if entry is None:
        # Relation axis (D-REL-1/4/5): the sign has no own matcher.
        # If the card has relations, it is a mask sign. single-sign
        # does NOT decide risk: it emits risk=NONE + RELATION CANDIDATES,
        # the verdict is the sequence layer's job (RELATION_FOUND !=
        # THREAT). If there are no relations, the sign is unknown to the
        # system, prior behaviour (error).
        if card.relations:
            # Mask sign: a card with relations. Even if ALL edges are
            # disabled (is_active=False) it is a known mask with no
            # active relations, NOT an unknown sign. Passes silently:
            # risk=NONE. Candidates carry ALL edges with the is_active
            # flag (disabled ones for debug/audit; the sequence layer
            # IGNORES is_active=False edges when deciding the verdict).
            active_relations = [r for r in card.relations if r.is_active]
            relation_candidates = [
                {
                    "relation_id": r.relation_id,
                    "relation_type": r.relation_type,
                    "target": r.target,
                    "context_scope": list(r.context_scope),
                    "verification_status": r.verification_status,
                    "runtime_effect": r.runtime_effect,
                    "is_active": r.is_active,   # sequence ignores False when deciding
                    "at_offset": offset,
                    "visible_form": card.visible_form,
                    "canon_hypothesis": None,   # channel for the canon probe (D-REL-5); filled in the sequence layer where context exists. The fragile canon matcher is not called blindly.
                }
                for r in card.relations
            ]
            mask_warnings = [draft_warning] if draft_warning else []
            if not active_relations:
                # All edges disabled — the mask is silent. Not a risk,
                # but a suspicious config state: a soft trace for audit
                # (risk stays NONE, no candidates for the verdict).
                mask_warnings.append("ALL_RELATIONS_INACTIVE")
            return OutputStatus(
                sign_codepoint=card.codepoint,
                card_version=card.card_uid,
                active_epoch="NOT_APPLICABLE",
                interpretation="relation_candidate",   # NOT a verdict
                risk_level=RiskLevel.NONE,              # D-REL-5: mask in single-sign = NONE
                risk_cases_triggered=[],
                guards_triggered=[],
                effect_fields_status="VALID",
                sign_offset_start=offset,
                sign_offset_end=offset + 1,
                output_warnings=mask_warnings,
                relation_candidates=relation_candidates,
                # Barrier N3 (a technical guarantee, not a comment):
                # the sequence layer takes ONLY this list. Disabled edges
                # physically never reach it -> cannot leak into the
                # verdict. Full relation_candidates stays for debugging.
                active_relation_candidates=[
                    c for c in relation_candidates if c["is_active"]
                ],
            )
        raise ModuleError("MATCHER_NOT_FOUND",
                           f"Нет зарегистрированного матчера для {card.codepoint}")
    matcher, has_epoch = entry

    if has_epoch:
        safe_ids, risk_ids, active_epoch, interp = matcher.match(text, offset, metadata)
    else:
        safe_ids, risk_ids, interp = matcher.match(text, offset)
        # ambiguity-флаг специфичен для SOLIDUS.RISK_CASE_008 —
        # остаётся точечной проверкой, не общим правилом ZONE_2
        if card.zone == Zone.ZONE_2 and "RISK_CASE_008" in risk_ids:
            ambiguity = True

    # --- STAGE_4: GUARD_EVALUATION ---
    guards_triggered = _guards_for_risk_ids(card, risk_ids)

    # --- STAGE_5: RISK_ASSESSMENT ---
    risk_level = _risk_level_for_ids(card, risk_ids)

    # --- STAGE_6: EFFECT_VALIDATION ---
    # все три карточки имеют EFFECT_FIELDS_ALL_NONE: YES / CLOSED_SCHEMA: YES
    effect_status = "VALID"

    # --- STAGE_7: OUTPUT_ASSEMBLY ---
    out = OutputStatus(
        sign_codepoint=card.codepoint,
        card_version=card.card_uid,
        active_epoch=active_epoch,
        interpretation=interp,
        risk_level=risk_level,
        risk_cases_triggered=risk_ids,
        guards_triggered=guards_triggered,
        ambiguity_flag=ambiguity,
        effect_fields_status=effect_status,
        sign_offset_start=offset,
        sign_offset_end=offset + 1,
        output_warnings=[draft_warning] if draft_warning else [],
    )

    # --- STAGE_8: CLEANUP --- (stateless, не требуется реальная очистка)
    return out
