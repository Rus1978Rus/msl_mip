# AUTHOR_DECISION: O(n²)-ФИКС RELATION-ТРОПЫ (G3b) — ZERO-DELTA, ДИЗАЙН РАТИФИЦИРОВАН

**Статус:** AUTHOR_DECISION (принято; КОД — под acceptance-гейтом, ZWSP не трогать без зелёного)
**Дата:** 2026-07-26
**Автор решения:** Руслан Малявский (AUTHOR_DECISION_STATUS_AUTHORITY) — «go» на решение+код
**Тип:** алгоритмическая правка производительности (НЕ поведение), инвариант ZERO-DELTA
**Основание:** CONVEYOR_PACKET_ONSQ_FIX_2026-07-26; конвейер 4 РАЗНЫХ семейства
  (OpenAI/GPT-5.6, DeepSeek-R1, Google/Gemini, Moonshot/Kimi). §1 подтверждён ДВУМЯ
  независимыми перемерами (координатор + Kimi; формулы кратностей сошлись точно).
  Выделен как OPEN G3b в AUTHOR_DECISION_20260721_D-INPUT-GUARD-MODE-A-DESIGN.

РАМКА: система оповещения, свидетель не судья. Этот круг НЕ меняет ни одного вердикта —
  делает ту же тропу near-linear. Изменение любого вердикта/офсета/reason = ПРОВАЛ круга.

## §1 ФАКТ (измерено, подтверждено 2×)
ZWSP-бег O(n²): 2000→~24–42с (×4/удвоение). Доминанта — `_is_domain_label_invisible` (315),
  вызывается O(m²) из `_detect_context_at` (512), который пересчитывает strip/domain-scan всего
  токена на КАЖДОМ вхождении. Контекст offset-СПЕЦИФИЧЕН (замер: HOST/PATH/USERINFO различаются
  по позиции в одном токене) — общие только ФАКТЫ токена.

## ПРИНЯТЫЕ РЕШЕНИЯ (D1–D6)

**D1 — V1 = (C) свип-реструктура на субстрате (B); (A) мемо-в-одиночку НЕДОСТАТОЧНА (замерено
  Kimi: остаток ×2.9–3.5).** Факты токена (границы, demasked+stripped проекция, domain-shape
  ВСЕХ префиксов/суффиксов одним O(token)-проходом, alnum-массивы, host-span, EMAIL/byte-exact
  константы, structural-stop позиции) считаются ОДИН раз на токен; на вхождение — O(1)-чтение.
  Границы токена БИТ-В-БИТ те же (whitespace-скан; lead=min(lead0,rel); had_leading_structural).
  Точный медленный путь сохранён для краёв (rel<lead0; kept-rel — сегодня недостижим). Прототип
  Kimi: ×2.0–2.25/удвоение, 2000-бег 0.088с (было 42с).

**D2 — V1: старый `_detect_context_at` ОСТАЁТСЯ REFERENCE-ORACLE.** Переименовать в
  `_detect_context_at_reference` (test-only), новый свип = `_detect_context_at`; гейт доказывает
  new == reference на корпусе. Никаких рукописных snapshot, никакого авто-обновления при расхождении.

**D3 — V2 = оба per-cp кэша (`_is_domain_label_invisible`, combining-предикат), обязательно, но
  ВТОРИЧНО.** Чистые функции от кодпоинта → lru_cache доказуемо эквивалентен. V2-в-одиночку
  оставляет O(n²) (малая константа); минимальный комплект = V1(C)+V2. Counter-benchmark на
  много-РАЗНЫХ кодпоинтах обязателен (кэш не должен маскировать O(n²) на низкоэнтропийном ZWSP).

**D4 — V4 differential-гейт = ОБЯЗАТЕЛЬНЫЙ предмерж-артефакт.** Побайтовое сравнение ПОЛНОГО
  отчёта analyze() (verdict/effective/witness/uncarded/reasons/offsets/ordering/projection/
  сериализация/None-vs-omitted/enum/exception) new vs reference. Корпус: батарейные манифесты
  (ZWSP/ZWJ/BOM) + ручные края (scheme/userinfo/host/path/query/fragment, leading-structural,
  combining, multi-mask, padding, email, метки 63/64, fullwidth-точки, IDN .рф/xn--) + seeded-fuzz
  + флуд-формы. Плюс СТРУКТУРНЫЕ counters (Unicode-классификаций ≤ C1·m+C2; strip НЕ из per-offset
  цикла) + scaling T(2n)/T(n) ≤ 2.5 и 2000-бег < 0.5с. Kimi исполнил на прототипе: ZERO-DELTA
  613/613 + ZWSP 21/21 + ZWJ/BOM + mutation 5/5×3 С патчем.

**D5 — V5: порядок отчёта НЕ менять** (обход по-вхождению слева-направо; предвычисление =
  lookup-only, не переупорядочивает reasons/verdicts). source-офсеты публичны, projected — внутри.

**D6 — V6: в этом круге ТОЛЬКО доминанта (V1-C + V2). `claimed` (143) O(m²) + `_attach_source_offsets`
  O(m×s) — СЛЕДУЮЩИЙ отдельный круг.** Замер: slash-флуд O(m²) (12000→14.6с; после V1+V2 доминанта
  = claimed 2.29с + offsets 2.34с на slash×6000). Причина отдельного круга: `claimed`-семантика
  «содержится в ОДНОМ интервале» ≠ слияние интервалов (контрпример: (0,5),(4,10) ⊇ (2,8)? нет по
  одиночным, да по слитым) → нужна структура sorted-starts+max-end online в priority-порядке, своё
  доказательство. Монотонный указатель НЕ эквивалентен (интервалы приходят в порядке приоритета
  кандидатов, не source). slash-DoS ещё круг прикрыт рубежом Mode A. Координатор пересмотрел раннее
  «чинить оба» — замерная нога перевесила: подмешивание V3 добавляет риск тихой дельты к чистой правке.

## GATE — КОД в этом круге только при:
ZERO-DELTA differential (new==reference на корпусе) + ZWSP 21/21 + ZWJ/BOM 11/11 + mutation +
  ВСЕ существующие гейты зелёные + профиль до/после (near-linear ×≤2.5/удвоение) + counter-benchmark
  (много-разных-кодпоинтов) + spy (strip НЕ из per-offset цикла). Без зелёного — мержа нет.

## OPEN — следующий круг
V3: `claimed` (143) + `_attach_source_offsets` (180) — отдельный конвейерный круг со своим
  differential (безопасная интервальная структура, не монотонный указатель).

## СВЯЗЬ
CONVEYOR_PACKET_ONSQ_FIX_2026-07-26 · свод scratchpad/onsq_fix_conveyor_legs.md · профиль
  scratchpad (cProfile-атрибуция) · AUTHOR_DECISION_20260721_D-INPUT-GUARD-MODE-A-DESIGN (G3b) ·
  kimi-methodological-audit-2026-07-26 (W1) · RULE_DESIGN_ADVERSARIAL_SIM · батареи sim_bycode_v2/zwj_bom.

END_OF_AUTHOR_DECISION
