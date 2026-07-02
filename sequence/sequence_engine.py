"""
Движок SEQUENCE_MODULE_TEMPLATE — STAGE_1-7.

Реализует SEQUENCE_MODULE_TEMPLATE_GEN3_v0_2_PLUS_EPOCH_v0_1 с
PATCH_24/25/26. Слой работает ПОВЕРХ результатов одиночных знаков
(module_engine): берёт исходный текст + список OutputStatus от каждого
обработанного знака, ищет среди известных SEQUENCE_CANDIDATES всех
задействованных карт совпадения, идущие подряд в тексте.

КЛЮЧЕВОЙ ПРИНЦИП adjacency (проверка смежности): кандидат считается
сработавшим, только если его буквальная последовательность реально
присутствует в тексте КАК НЕПРЕРЫВНАЯ подстрока. Это защищает от
ложного "слипания" знаков, стоящих в разных концах текста (например,
две точки в "конец. Начало." не образуют SEQUENCE '..', потому что
между ними есть другие символы).

CROSS-CARD (PATCH_26): CANDIDATE_POOL — объединение SEQUENCE_CANDIDATES
ВСЕХ карт из CARD_SET, а не одной. Это позволяет ловить межкарточные
идиомы вроде '../' (точка+точка+солидус — кандидаты есть и у DOT, и у
SOLIDUS), '://' (SOLIDUS.SC7).
"""

from __future__ import annotations

from sign_core_card import SignCoreCard, RiskLevel
from sequence_output import SequenceMatch, SequenceOutput


def _build_candidate_pool(cards: list) -> list:
    """STAGE_2/2a (PATCH_26): CANDIDATE_POOL = объединение
    SEQUENCE_CANDIDATES всех карт. Каждый элемент — (candidate, card)."""
    pool = []
    for card in cards:
        for sc in card.sequence_candidates:
            pool.append((sc, card))
    # сортируем по убыванию длины последовательности — более длинные
    # (специфичные) кандидаты проверяются первыми, чтобы '../../../'
    # имел приоритет над '..' на том же месте
    pool.sort(key=lambda pair: len(pair[0].sequence), reverse=True)
    return pool


def _find_literal_matches(text: str, pool: list,
                          validated_offsets: set = None,
                          card_signs: set = None,
                          strict: bool = False,
                          known_signs: set = None) -> list:
    """STAGE_3-4: ищет непрерывные буквальные совпадения каждого
    кандидата в тексте. adjacency обеспечивается тем, что str.find
    ищет именно НЕПРЕРЫВНУЮ подстроку.

    ИСПРАВЛЕНО (раунд 2, 2026-06-29): прежнее "правило якоря"
    (ведущий символ ОБЯЗАН быть знаком набора) было опровергнуто
    контрпримером SOLIDUS.SC6 "*/" — ведущий "*" вне набора знаков,
    но кандидат легитимен, если "/" провалидирован. Новое правило:

      (а) ВСЕ символы кандидата, которые являются знаками из CARD_SET
          ИЛИ из known_signs (полного реестра знаков системы, см.
          ниже), обязаны быть провалидированы;
      (б) среди символов кандидата должен быть хотя бы ОДИН знак из
          CARD_SET (защита от полностью "пустых" Ghost-совпадений);
      (в) символы кандидата, которых нет ни в CARD_SET, ни в
          known_signs (истинный контекст — 🎃/😭/☠️ у SKULL, "*" в
          "*/", для которых в системе вообще нет SIGN_CORE_CARD),
          валидации не требуют.

    ИСПРАВЛЕНО (раунд 3, 2026-06-29, CARD_SET_COMPLETENESS, найдено
    по итогам код-ревью): card_signs строится только из ПЕРЕДАННЫХ в
    конкретный вызов карт. Если вызывающий код забыл передать DOT,
    а кандидат SOLIDUS.SC3 "../" содержит точки — точки раньше
    считались "внешним контекстом" (как звёздочка), хотя DOT-карточка
    РЕАЛЬНО существует в системе, просто не была передана в ЭТОТ
    вызов. Это давало Ghost-Matching через невнимательность вызывающего
    кода, не через намеренный дизайн. known_signs — отдельный,
    опциональный параметр: ПОЛНЫЙ реестр знаков, известных системе
    (не только текущему CARD_SET). Если передан — символ из
    known_signs ВСЕГДА требует валидации, даже если его карта не
    входит в card_signs этого вызова. known_signs=None (по умолчанию)
    — сохраняет прежнее поведение (без реестра, для изолированных
    юнит-тестов одной карты).

    UPSTREAM_DEPENDENT (sc.scope) проверяется отдельно и безусловно
    блокирует кандидат в strict-режиме — см. SOLIDUS.SC7 "://".

    strict=False: validated_offsets не переданы → текстовый режим."""
    matches = []
    claimed = []
    card_signs = card_signs or set()
    registry = known_signs if known_signs is not None else card_signs

    def _candidate_validated(sc, idx: int, end: int) -> bool:
        if validated_offsets is None:
            return not strict
        if sc.scope == "UPSTREAM_DEPENDENT":
            # явная пометка из карточки: кандидат структурно зависит
            # от символа вне системы знаков — в strict-режиме
            # недостижим, пока для такого символа нет своей карточки
            return False
        has_card_sign = False
        for pos in range(idx, end):
            ch = text[pos]
            if ch in card_signs:
                has_card_sign = True
            if ch in registry:
                # знак из CARD_SET ИЛИ из полного реестра системы —
                # в обоих случаях обязан быть провалидирован
                if pos not in validated_offsets:
                    return False
        return has_card_sign

    for sc, card in pool:
        seq = sc.sequence
        if not seq:
            continue
        start = 0
        while True:
            idx = text.find(seq, start)
            if idx < 0:
                break
            end = idx + len(seq)
            covered = any(c_start <= idx and end <= c_end for c_start, c_end in claimed)
            if not covered and _candidate_validated(sc, idx, end):
                matches.append(SequenceMatch(
                    sc_id=sc.sc_id,
                    sequence=seq,
                    name=sc.name,
                    risk_level=sc.risk_level,
                    candidate_source_card=card.codepoint,
                    match_start=idx,
                    match_end=end,
                ))
                claimed.append((idx, end))
            start = idx + 1
    matches.sort(key=lambda m: (m.match_start, -(m.match_end - m.match_start)))
    return matches


def _attach_source_offsets(matches: list, sign_statuses: list) -> None:
    """PATCH_25: для каждого совпадения — какие одиночные знаки
    (по их SIGN_OFFSET) попали в диапазон [match_start, match_end).
    Заполняет source_sign_offsets реальными данными (SOURCE_SIGN_LIST),
    что стало возможным благодаря PATCH_23 (offset в OutputStatus)."""
    for m in matches:
        for st in sign_statuses:
            if m.match_start <= st.sign_offset_start < m.match_end:
                m.source_sign_offsets.append(st.sign_offset_start)
        m.source_sign_offsets.sort()


def process_sequence(text: str, cards: list,
                     sign_statuses: list = None,
                     known_signs: set = None) -> SequenceOutput:
    """Полный STAGE_1-7 sequence-слоя.

    text          — исходный текст (тот же, что подавался в module_engine)
    cards          — список SignCoreCard, реально задействованных
                     (CARD_SET, PATCH_26); обычно те карты, чьи знаки
                     присутствуют в тексте
    sign_statuses  — список OutputStatus от module_engine (для
                     SOURCE_SIGN_LIST); опционально
    known_signs    — ПОЛНЫЙ реестр visible_form всех SIGN_CORE_CARD,
                     известных системе (не только переданных в cards).
                     Закрывает CARD_SET_COMPLETENESS пробел (найдено
                     по итогам код-ревью, 2026-06-29): без этого
                     параметра, если вызывающий код передал неполный
                     CARD_SET (например, забыл DOT), точки в
                     SOLIDUS.SC3 "../" ошибочно считались "внешним
                     контекстом" и матчились без валидации. В
                     production-рантайме (msl_mip_runtime.py) сюда
                     следует передавать registry со ВСЕХ загруженных
                     карт системы, а не только cards этого вызова.
                     По умолчанию None — для изолированных юнит-тестов
                     одной карты, сохраняет прежнее поведение.
    """
    sign_statuses = sign_statuses or []

    # --- STAGE_1: INPUT_VALIDATION ---
    if not text:
        return SequenceOutput(check_unavailable=True,
                              warnings=["EMPTY_TEXT"])
    if not cards:
        return SequenceOutput(check_unavailable=True,
                              warnings=["NO_CARDS_IN_SET"])

    # --- STAGE_2: CARD_SET_DETERMINATION (PATCH_26) ---
    card_set = [c.codepoint for c in cards]

    # ИСПРАВЛЕНО (найдено по итогам код-ревью, 2026-06-29, Grok):
    # раньше sequence-слой не проверял document_status карт в
    # CARD_SET вообще — WORKING_DRAFT карточка участвовала в поиске
    # последовательностей молча, без какого-либо сигнала о том, что
    # результат для неё ненадёжен (в отличие от module_engine, где
    # такое предупреждение обязательно). Теперь sequence-слой тоже
    # честно предупреждает, не блокируя работу.
    _CONFIRMED_STATUSES = {"WORKINGLY_CLOSED", "ARTIFACT_CONFIRMED"}
    draft_cards = [
        c for c in cards
        if c.document_status not in _CONFIRMED_STATUSES and c.visible_form in text
    ]
    draft_warnings = [
        f"CARD_NOT_CONVEYOR_REVIEWED: {c.card_uid or c.codepoint} "
        f"(status={c.document_status}) реально встретился в тексте — "
        f"результаты для последовательностей с этим знаком ненадёжны"
        for c in draft_cards
    ]

    # --- STAGE_2a: CANDIDATE_POOL (PATCH_26) ---
    pool = _build_candidate_pool(cards)
    if not pool:
        return SequenceOutput(card_set=card_set, check_unavailable=True,
                              warnings=["EMPTY_CANDIDATE_POOL"])

    # Множество позиций, реально прошедших single-sign валидацию.
    # Каждый OutputStatus покрывает [sign_offset_start, sign_offset_end).
    # Если статусы предоставлены — включаем strict-валидацию совпадений
    # (Ghost Matching fix): кандидат принимается, только если все его
    # позиции провалидированы. Если статусов нет — текстовый режим.
    validated_offsets = None
    strict = False
    if sign_statuses:
        validated_offsets = set()
        for st in sign_statuses:
            for pos in range(st.sign_offset_start, st.sign_offset_end):
                validated_offsets.add(pos)
        strict = True

    # --- STAGE_3-4: MATCHING + adjacency + validation ---
    card_signs = {c.visible_form for c in cards}
    matches = _find_literal_matches(text, pool, validated_offsets, card_signs,
                                    strict, known_signs)

    # --- STAGE_5: SOURCE_SIGN_LIST / SOURCE_OCCURRENCE_LIST (PATCH_25) ---
    _attach_source_offsets(matches, sign_statuses)
    source_sign_list = sorted({st.sign_offset_start for st in sign_statuses})

    # --- STAGE_6: MULTIPLE_MATCHES (PATCH_26) ---
    multiple = len(matches) > 1

    # ИСПРАВЛЕНО (найдено по итогам код-ревью, 2026-06-29, GPT-5.5):
    # проверка "visible_form карты в тексте" пропускает редкий, но
    # реальный случай — WORKING_DRAFT карта объявляет SEQUENCE_
    # CANDIDATE, который сам НЕ содержит visible_form этой карты
    # (например, гипотетическая карта объявляет кандидат "://" без
    # собственного знака внутри него). Такое совпадение реально
    # сработает, но предупреждение по проверке "visible_form in text"
    # не появится. Вторая, независимая проверка: если совпадение
    # пришло от непроверенной карты — предупреждение обязано
    # появиться, независимо от первой проверки.
    draft_codepoints = {c.codepoint for c in cards
                        if c.document_status not in _CONFIRMED_STATUSES}
    matched_draft = {m.candidate_source_card for m in matches
                     if m.candidate_source_card in draft_codepoints}
    already_warned = {c.codepoint for c in draft_cards}
    for cp in matched_draft - already_warned:
        draft_warnings.append(
            f"CARD_NOT_CONVEYOR_REVIEWED_MATCHED_SEQUENCE_SOURCE: "
            f"{cp} — непроверенная карта стала источником совпадения "
            f"в SEQUENCE, хотя её visible_form не найден в тексте напрямую"
        )

    # --- STAGE_7: OUTPUT_ASSEMBLY ---
    return SequenceOutput(
        card_set=card_set,
        matches=matches,
        multiple_matches=multiple,
        source_sign_list=source_sign_list,
        source_occurrence_list="NOT_AVAILABLE",  # честный стаб (PATCH_25)
        check_unavailable=False,
        warnings=draft_warnings,
    )
