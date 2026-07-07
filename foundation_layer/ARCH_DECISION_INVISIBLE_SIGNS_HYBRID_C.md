PRIVATE AUTHORED PROJECT / COMMERCIAL USE PROHIBITED
DOCUMENT_ID: ARCH_DECISION_INVISIBLE_SIGNS_HYBRID_C
DOCUMENT_TYPE: ARCHITECTURE_DECISION
STATUS: AUTHOR_DECISION (Руслан Малявский, 2026-07-07)
AUTHOR: Ruslan Malyavsky

============================================================
# Архитектура невидимых знаков — ГИБРИД (вариант C)
============================================================

## Решение

Невидимые знаки (Default_Ignorable_Code_Point: U+FE0F VS16, U+200D ZWJ,
U+200B ZWSP, U+FEFF BOM, U+202E RLO, U+E0001 TAG и др.) реализуются по
ГИБРИДНОЙ архитектуре:

  СЛОЙ КЛАССА (общий):  INVISIBLE_DEFAULT_IGNORABLE_GUARD
    — единая реализация классовых свойств: невидимость, неудаляемость
      нормализацией, strip/flag/log/canonicalize.
    — подключается через существующий массив REQUIRED_GENERAL_GUARDS
      в шаблоне карточки (Раздел 3), рядом с SIGN_FALSE_EFFECT_MIMICRY_GUARD.

  СЛОЙ ЗНАКА (тонкие карточки):  по одной на знак
    — только УНИКАЛЬНАЯ семантика и матчинг:
        VS16  → emoji-variation-sequence
        ZWJ   → join-control (UAX#29 GB9)
        ZWSP  → word-break
    — НЕ дублируют классовые GUARD.

  КОНТРАКТ: GENERAL_GUARD выполняется ПЕРВЫМ (strip/normalize/flag),
    затем per-card matcher получает канонический поток + метаданные
    (original_positions, removed_chars) для трассируемости.

## Обоснование (из фактов исследования U+FE0F)

- F2 [VERIFIED]: невидимые НЕ удаляются никакой нормализацией (NFC/NFD/
  NFKC/NFKD) — свойство ОБЩЕЕ → в GENERAL_GUARD (не дублировать).
- F3 [VERIFIED]: функции РАЗНЫЕ (ZWJ join / ZWSP break / VS16 selector)
  → тонкие карточки на знак (не сливать в одну).
- F4 [UNVERIFIABLE]: у VS16 нет уникального CVE, угроза классовая →
  классовая защита оправдана.

## Почему не A и не B

- НЕ A (полные отдельные карточки): дублировал бы классовый GUARD в
  10+ карточках невидимых.
- НЕ B (одна общая карточка): потерял бы F3 — разные механизмы требуют
  разных матчеров.
- C берёт лучшее обоих.

## Прецедент в архитектуре (VERIFIED grep 2026-07-07)

REQUIRED_GENERAL_GUARDS уже существует в шаблоне GEN3_v0_3 (строка 128,
140) и работает в карточке @. Вариант C НЕ требует новой архитектуры —
использует существующий механизм. Нужно добавить
INVISIBLE_DEFAULT_IGNORABLE_GUARD_v0_1 в этот массив.

## Риск выбора (честно)

Появляется контракт между GENERAL_GUARD и картой, требующий дисциплины
синхронизации. Управляемо через шаблон REQUIRED_GENERAL_GUARDS.

## Процесс (конвейер)

- Развилка A/B/C прошла ARCHITECTURE_DECISION review — единодушно C.
- Ревьюеры: Gemini, GPT-5.5, Qwen, Copilot, MSL/MIP agents.
- AUTHOR_DECISION: C (Руслан Малявский 2026-07-07).

## Следующие шаги

1. Спроектировать INVISIBLE_DEFAULT_IGNORABLE_GUARD (через конвейер —
   ляжет в основу всех невидимых).
2. На нём построить тонкую карточку VS16 (U+FE0F).
3. Далее ZWJ, ZWSP и остальные — тонкими карточками на том же GUARD.

END_OF_DOCUMENT
