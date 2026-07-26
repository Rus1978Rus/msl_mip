# AUTHOR_DECISION: literal-matcher O(m²)-фикс (круг V3) — ZERO-DELTA, дизайн ратифицирован

**Статус:** AUTHOR_DECISION (дизайн принят; КОД под acceptance-гейтом, как D-ONSQ-FIX)
**Дата:** 2026-07-26
**Автор:** Руслан Малявский (AUTHOR_DECISION_STATUS_AUTHORITY)
**Тип:** алгоритмическая правка производительности, инвариант ZERO-DELTA
**Основание:** CONVEYOR_PACKET_ONSQ_CLAIMED_2026-07-26; 3 РАЗНЫХ семейства (Google/Gemini,
  OpenAI/GPT-5.6, Moonshot/Kimi); Kimi построила differential-проверенные прототипы; свод
  scratchpad/onsq_claimed_conveyor_legs.md. Продолжение D-ONSQ-FIX (V6 вынес этот круг).

РАМКА: круг НЕ меняет вердикты — делает ту же тропу near-linear. Любое изменение набора матчей/
  порядка/отчёта = провал круга.

## §1 ФАКТ (измерено, подтверждено 3×)
slash-флуд O(m²) (12000→14.6с), D-ONSQ-FIX не затронут. Должники: `claimed`-покрытие
  `covered=any(...)` (17.99M вызовов) + `_attach_source_offsets` O(m×s). Семантика `covered` =
  «∃ ПРИНЯТЫЙ интервал, ПОЛНОСТЬЮ содержащий [idx,end]» = `max(end : start≤idx) ≥ end`
  (НЕ union: {(0,5),(4,10)}⊉(2,8) → False). Pool отсортирован по убыванию длины (код L48).

## ПРИНЯТЫЕ РЕШЕНИЯ (D1–D6)

**D1 — CONTAINMENT = PREFIX-MAX.** Заменить O(m) `any(...)` на структуру, отвечающую
  `max(end : start≤idx) ≥ end` за O(log m) ONLINE в priority-порядке. Структура — на выбор
  реализатора, обе zero-delta, обе валидируются ОДНИМ differential:
  (а) FENWICK prefix-max по source-start (GPT) — O(log n) query/update, размер n+1 (координаты
      уже целые 0..n, сжатие НЕ нужно), прямое доказательство из предиката, без edge-кейсов удаления;
  (б) FRONTIER недоминируемых интервалов с ДОКАЗУЕМЫМ удалением (Gemini/Kimi) — Kimi измерила
      прототип: 4.72с→0.11с на slash×12000, ZERO-DELTA 428/428, unit-diff 300 серий = 0.
  Уклон — FENWICK (проще доказательство, нет удаления); допустим FRONTIER (измерен). Union/
  overlap/монотонный-source-указатель ЗАПРЕЩЕНЫ (неэквивалентны).

**D2 — ЧИНИТЬ И `_attach_source_offsets` В ЭТОМ КРУГЕ.** Один отсортированный multiset
  `sign_offset_start` + два `bisect_left` на полуинтервал [start,end). СОХРАНИТЬ: дубли (multiset,
  не set), `extend`+финальный `.sort()` (не replacement), не читать статусы при пустом `matches`
  (exception-эквивалентность). Замер (Kimi): 2.18с→~0.

**D3 — REFERENCE-ORACLE DIFFERENTIAL (обязательный предмерж-артефакт).** Старый
  `_find_literal_matches` + старый attach — оставить test-only оракулами (как
  `_detect_context_at_reference` в D-ONSQ-FIX). Гейт трёхуровневый: unit matcher + unit attach +
  end-to-end побайтовый полный отчёт + структурные counters (Fenwick-шагов ≤ occ·log n; legacy-
  claimed-сканов=0; union-операций 0) + контрпримеры (union {(0,5),(4,10)}⊉(2,8); bridge
  {(0,4),(3,7),(6,10)}⊉(2,9); priority-order) + slash-scaling + fuzz (варьируя pool). Update
  ТОЛЬКО после успешного append принятого матча (exception-before-update). Порядок и финальная
  сортировка `(start,-len)` — не трогать.

**D4 — OUTPUT-SIZE GATE (страховка, из находки GPT OTHER-10).** Замерить суммарный размер
  attached-offsets. Для slash ИЗМЕРЕНО O(n) (matches O(n), off/n=2.0) → полный отчёт O(n),
  near-linear достижим. Оставить output-counter в acceptance: если на ином корпусе выход O(n²),
  честно зафиксировать, что zero-delta ограничивает достижимую сложность материализации.

**D5 — ОБЛАСТЬ: V1(containment)+V2(attach) — этот круг; substrate — КРУГ №4.** Поправка Kimi
  (измерена мной): после снятия claimed+attach slash остаётся O(m²) из-за ТРЕТЬЕГО должника
  `solidus_matcher.detect_substrate` (L93 `_DOMAIN_BEFORE_SLASH_RE.search(text[:offset])` +
  L98 `text.count("/")`, per-offset; изолированно 12000→1.29с ×4.1). Этот круг закрывает
  claimed+attach (измеренная доминанта, near-linear по ним); ПОЛНЫЙ slash near-linear требует
  ещё круга №4 (substrate). Честно: критерий (б) на slash в этом круге достигается ЧАСТИЧНО.

**D6 — ДВА ПОДПАТЧА (атрибуция дельты).** V1 (containment) и V2 (attach) — отдельными
  коммитами, каждый со своим reference-oracle differential + профилем; финальный совместный гейт.

## GATE — КОД только при:
ZERO-DELTA differential (new==reference, unit+end-to-end) + ZWSP 21/21 + ZWJ/BOM 11/11 +
  mutation + все гейты + профиль до/после (claimed+attach near-linear) + counters (legacy-сканов=0) +
  output-size замер + union/bridge/priority-корпус. Без зелёного — мержа нет.

## OPEN — круг №4
`solidus_matcher.detect_substrate` O(m²) (per-text кэш count + alpha-run массив → O(1) prefix-regex).
  Материал Kimi готов (прототип 517/517 + 3689-offset unit-diff). Отдельный конвейер/решение.

## СВЯЗЬ
CONVEYOR_PACKET_ONSQ_CLAIMED_2026-07-26 · свод onsq_claimed_conveyor_legs.md · AUTHOR_DECISION_
  20260726_D-ONSQ-FIX (V6 вынес этот круг; образец reference-oracle+differential) · sequence_engine
  `_find_literal_matches`/`_attach_source_offsets` · solidus_matcher `detect_substrate` (круг 4) ·
  RULE_DESIGN_ADVERSARIAL_SIM · батареи sim_bycode_v2/zwj_bom.

END_OF_AUTHOR_DECISION
