ЧАСТНЫЙ АВТОРСКИЙ ПРОЕКТ / COMMERCIAL USE PROHIBITED

DOCUMENT_ID: RAW_REVIEWS_SUBSTITUTION_OP_COMPOSITION_2026-07-17
DOCUMENT_TYPE: RAW_REVIEW_BUNDLE (сверяемый источник — НЕ свод)
DATE: 2026-07-17
PACKET: CONVEYOR_PACKET_SUBSTITUTION_OP_COMPOSITION_2026-07-17 (O2b — состав набора)

СЧЁТ: прислано 5 блоков (НЕ 7). Реальных op-вердиктов = 4 (R1,R2,R3⚠,R4) + 1 мета (R5).
Семейств названо 3 (OpenAI, Gemini, Qwen); R3 без семейства (фантом-ссылка на файл).

============================================================
R1 — GPT-5.6 Thinking / OpenAI GPT — ВЕРДИКТ
============================================================
МИНИМАЛЬНЫЙ НАБОР = 5: C1 IDNA-processing-profile (домены), C6 identifier-comparison-
  profile (логины), C4 explicit-zero-width-filter (наивные), C3 tag-witness-and-strip
  (LLM), C2 bidi-control-detection (код). Из них 4 порождают substitution-рёбра
  (C1,C3,C4,C6); C2 — MANDATORY ADJACENT DETECTION, GENERATES_SUBSTITUTION_EDGES: NO.
РЕЗЕРВ: C5 maximal-class-strip (test only), C8 TARGET_PIPELINE_REPLAY (новый, high-fidelity).
CUT: C7 NFC, C7 NFKC (согласен с отводом 0/138). Исключение: toNFKC_Casefold ≠ NFKC —
  удаляет default-ignorable, остаётся ВНУТРИ C6.
OP-1: KEEP как explicit versioned target profile, НЕ как universal default, НЕ как
  расплывчатая zero-width-эвристика (точный список кодпоинтов).
IDNA: KEEP mandatory, ПЕРЕИМЕНОВАТЬ IDNA-mapping → IDNA-processing-profile; это
  versioned pipeline (valid/mapped/ignored/deviation/disallowed), НЕ strip. Дал
  per-codepoint UTS-46 статусы (200B ignored, 200C/D deviation, 200E/F disallowed,
  теги disallowed) — reviewer-claimed.
АРХИТЕКТУРНАЯ НАХОДКА (VERIFIED): op разного ТИПА — equivalence-transform /
  validation-profile / detection-profile. CO_REJECTED ≠ SUBSTITUTABLE;
  CO_DETECTED ≠ SUBSTITUTABLE. Без типизированного вывода (STATUS/CANONICAL_KEY/
  WITNESS/REASON) C1 и C2 породят ЛОЖНЫЙ полный граф.
NFC/NFKC отведены: YES. bidi detection-ось: YES (в registry, но не считать edge). C6: mandatory.

============================================================
R2 — Gemini / Gemini — ВЕРДИКТ
============================================================
МИНИМАЛЬНЫЙ НАБОР = 4: op_idna (C1, домены), op_bidi (C2, код), op_tag_strip (C3, LLM),
  op_naive_zw (C4, наивные; ядро ~ZWSP/ZWNJ/ZWJ/WJ/BOM). Рекомендует «подсчёт графа
  рёбер для каждой из 4» — т.е. считает bidi полноправным edge-членом.
РЕЗЕРВ: C6 UAX-31 (добавить позже, если naive_zw неточен). C5 Cf-strip — убрать из
  default (шум 9453), оставить опциональным тестом.
CUT: C7 NFC/NFKC полностью (0/138, «NFKC сворачивает совместимые формы, но Cf/DI не трогает»).
OP-1: ДЕРЖАТЬ с хардкод-списком SUBSET_NAIVE_ZW.
bidi detection в одном наборе со strip: YES (гетерогенность отражает реальность).
Рекомендует FORK_STATUS CLOSED (advisory).

============================================================
R3 — UNNAMED (нет REVIEWER/FAMILY; фантом-ссылка sandbox://…) — LOW_RELIABILITY, ВЕРДИКТ
============================================================
[Провенанс слабый: тот же фантом-отпечаток, что в прошлом круге. По ФАКТАМ в этот раз
 чисто (класс-числа верны). Вес снижен за провенанс, не за содержание.]
DEFAULT (3): C4 zero-width (граница PURE/BN=23), C2 bidi-detect (DETECTION не STRIP),
  C3 tag-strip.
РЕЗЕРВ (2): C5 Cf-strip; C1 IDNA — ДЕМОТИРОВАЛ в резерв («требует run-verification,
  VALIDATION не STRIP»).
CUT: C6 UAX-31 (дублирует OP-1/OP-2), C7 NFC/NFKC (0/138), UTS-39 (визуальная ось).
Итого 3 default + 2 резерв. OP-1 держать. NFC/NFKC отведены YES. bidi detection-ось YES.
[РАСХОЖДЕНИЕ: единственный демотировал IDNA в резерв.]

============================================================
R4 — Qwen / Qwen — ВЕРДИКТ
============================================================
ОБЯЗАТЕЛЬНЫЕ = 4: C1 IDNA (домены), C2 bidi-detect (код), C3 tag (LLM), C4 zero-width
  (наивные). C4 — SURVIVES_WITH_SPEC: явный список из 6: {U+00AD,U+200B,U+200C,U+200D,
  U+2060,U+FEFF}. bidi трактует как edge-генератор («пары с одинаковым визуальным
  порядком при разном логическом»).
СТРОГИЙ ПРОФИЛЬ: C5 Cf-strip (upper bound/тест, не default).
CUT: C6 UAX-31 («политика, сводится к C4/C5», не op), C7 NFC/NFKC (0/138), UTS-39.
NFC/NFKC отведены YES для class-internal; ⚠ добавил: значимы CROSS-CLASS (пример
  U+FF0F → U+002F под NFKC) — вне набора-138, на будущее.
Итого 4 обязат. + 1 строгий = 5. OP-1 держать (6-list). bidi detection-ось YES.

============================================================
R5 — (нет REVIEWER/FAMILY) — META_ASSESSMENT (НЕ вердикт)
============================================================
Оценивает готовность пакета к раздаче («ASSESSMENT FOR DISPATCH», «READY TO SEND TO
≥3 REVIEWERS?»), раздел «PREDICTED REVIEWER FINDINGS» — предсказывает ревьюеров.
ПОЗИЦИЯ (извлечена): минимальный набор {C1 IDNA, C3 tag, C4 OP-1} + C5 тест;
  ⚠ УБРАТЬ C2 (bidi) в отдельный framework (единственный за «вынести совсем»);
  C6 → merge в C4; NFC/NFKC вон.
Три loophole-вопроса (мета): C2 substitution vs detection-framework; C1 IDNA как
  equivalence-class; граница OP-1 (кто фиксирует). Новый кандидат: OP-X контекстная/
  позиционная strip (начало/середина/конец строки). → не равноправный вердикт.

============================================================
ВЕРИФИКАЦИЯ ПРОГОНОМ (Claude Code, scratchpad verify_reviewers_composition.py)
============================================================
- IDNA UTS-46 (пакет idna) НЕ установлен → per-codepoint статусы R1 НЕ run-verified.
- IDNA2003/stringprep (stdlib, прокси): по классу 138 — REMOVED(map-to-nothing) 6 (все
  PURE); PROHIBITED(bidi, C.8) 13 (7 DIR + 6 DEP); прочее 119. Вывод: IDNA гетерогенна
  (remove/prohibit/pass), НЕ чистый strip; как edge-op ТОНКАЯ (~6 removed). Поддерживает
  R1 CO_REJECTED≠SUBSTITUTABLE (13 prohibited = ошибки, не общий ключ).
- Qwen OP-1 6-list: все 6 в классе, gc=Cf, bidi=BN — валиден.
- Qwen cross-class U+FF0F: NFKC='/'; gc=Po; в классе-138 НЕТ — пример корректен, вне набора.
- R1 toNFKC_Casefold: stdlib-приближение ZWSP НЕ убирает → не воспроизводимо в stdlib,
  reviewer-claimed.
- Бакеты 23/12/97/6 переподтверждены.

END_OF_RAW_BUNDLE
