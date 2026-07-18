ЧАСТНЫЙ АВТОРСКИЙ ПРОЕКТ / COMMERCIAL USE PROHIBITED

DOCUMENT_ID: RAW_REVIEWS_GUARD_IMPL_PLAN_2026-07-18
DOCUMENT_TYPE: RAW_REVIEW_BUNDLE (сверяемый источник — НЕ свод)
DATE: 2026-07-18
PACKET: CONVEYOR_PACKET_GUARD_IMPL_PLAN_2026-07-18 (план реализации, инкремент 1)

СЧЁТ: 6 ВНЕШНИХ дизайн-вердиктов + 1 self-leg (Claude) = 7 ног. Семейств 7 (Anthropic,
  OpenAI, Gemini, Moonshot, DeepSeek, Qwen, Microsoft). ИСКЛЮЧЁН: 1 META_ASSESSMENT
  (предсказывает ревьюеров; + ФАБРИКАЦИЯ КОДА — привёл выдуманные сниппеты как «цитаты
  из msl_mip_runtime.py»: `_invisible_candidate(ch, ucd_pinned)` — реально `(ch)` один
  арг + unicodedata; verification фейковая, факты чужие из §1 пакета). Не в счёте.

============================================================
РАСКЛАД ПО ГЛУБИНЕ (кто чистый SURVIVES, кто с поправками)
============================================================
CLEAN SURVIVES (code-now, без глубоких поправок): Gemini, DeepSeek = 2.
  ⚠ Оба ПРОПУСТИЛИ реальные дефекты (scope-138, биекция, дыра гейта). DeepSeek прямо
  назвал гейт «исчерпывающ» — опровергнуто логикой (см. ДЫРА №1).
SURVIVES С ПОПРАВКАМИ (patch-first): Claude, GPT, Kimi, Qwen, Copilot = 5.
ПРОТИВ / LOOPHOLE / «ломает ZWSP»: 0/7. Все: план верен, ZWSP безопасен ЕСЛИ гейт пропатчен.
ЯДРО (shadow → новое поле class_guard, вердикт не трогается, acceptance-гейт обязателен,
  reuse _invisible_candidate, детект до нормализации, охват-138-сразу): ПРИНЯТО ВСЕМИ 7/7.

============================================================
ДЫРА ГЕЙТА №1 (Kimi) — СТРУКТУРНАЯ, КРИТИЧНАЯ
============================================================
УТВЕРЖДЕНИЕ: гейт ассертит идентичность ВЕРДИКТОВ/witness/позиций; но class_guard —
  shadow-поле, вердикт-путём НЕ читается → поломка ВНУТРИ поля (кривая карта, MUT-G2)
  для verdict-identity НЕВИДИМА ПО ПОСТРОЕНИЮ. Нужен ОТДЕЛЬНЫЙ property-оракул для
  class_guard (биективность карты, census-138, canonical_view==reference-strip,
  identity-on-clean, идемпотентность).
ЛОГИЧЕСКАЯ ПРОВЕРКА (Claude): ВЕРНО. Тест, проверяющий только поля X, не может обнаружить
  порчу в поле Y, которое ни одно наблюдаемое вычисление не читает. class_guard не
  потребляется → его порча не меняет вердикт/witness/позиции → verdict-identity зелен
  при битом class_guard. Логический факт, не гипотеза.
ПОДДЕРЖКА: Kimi (сформулировал + WHY), GPT (guard-specific oracle GUARD_ORACLE_MANIFEST +
  exact-set-138), Qwen (assert биективности position_map), Copilot (формальные bijectivity-
  проверки: uniqueness/coverage/reversibility), Claude self-leg (guard-self-asserts:
  биективность, покрытие-138, карточные-аннотированы). = 5/7. Gemini частично (deep-compare).
  DeepSeek ПРОТИВ (назвал гейт исчерпывающим — неверно). => 5 за, 1 частично, 1 против(ошибочно).

============================================================
ТРИ УСЛОВИЯ НЕ-КОНТАМИНАЦИИ (Kimi) — каналы В ОБХОД dataflow
============================================================
(i) PURITY предиката _invisible_candidate: зовётся чаще (регистратор+гард); скрытое
    состояние (кэш/дедуп) сдвинет регистратор БЕЗ dataflow-рёбер. Пин referential
    transparency; reuse=вызов. РЕАЛЬНО. Поддержка: Kimi + GPT (pure-function contract,
    CALL_TWICE/CALL_ORDER/PARALLEL) = 2.
(ii) EXCEPTION containment: падение гарда роняет analyze() = контаминация → class_guard=
    {status:GUARD_FAILURE}, конвейер бит-в-бит (fail-open РАНТАЙМ). РЕАЛЬНО. Поддержка:
    Kimi + GPT (GUARD_INTERNAL_ERROR → preserve old + UNVERIFIABLE) + Copilot (fail-closed
    на МЕРЖЕ — комплементарно) = 3.
(iii) RESOURCE bound: members[]=O(#невидимых); флуд ZWSP/TAG → OOM; батарея 21/21 НЕ
    флудит → не ловит. Кап + TRACE_TRUNCATED в инкр-1. РЕАЛЬНО. Поддержка: Kimi + GPT
    (resource-exhaustion O(n)/event-limit/TRACE_TRUNCATED) + Qwen (assert time<2*baseline) +
    Copilot (нагрузочное+resource-limits) = 4.

============================================================
МУТАЦИИ НЕВЫРАЗИМЫ (Kimi) — split под инкремент 1
============================================================
MUT-G3(strip карточного)/G4(safe_to_delete)/G6(overflow) описывают инкремент 2 (в инкр-1
  нет strip/safe_to_delete/overflow-полей) → нечего мутировать. Заменить/добавить:
  MUT-G8 (card_mask flip), MUT-G9 (detect-после-нормализации, урок F-NEW-1), MUT-G10
  (offset-drift codepoint vs UTF-16 астральные). РЕАЛЬНО. Поддержка: Kimi + GPT
  (независимо дал split MUT-I1-01..12) + Qwen (4 дыры: original-mod/non-bijective/schema/
  resource) + Copilot (off-by-one/non-bijective/canonical-length/truncation/provenance) = 4.

============================================================
ДОП. ПАТЧИ (за пределами 3 групп Kimi — свод их не перечислил)
============================================================
- SCOPE-138-ONLY предикат: _invisible_candidate ШИРЕ 138 (VS/braille/whitespace); нужен
  отдельный is_monitored_control_138 (Cf∧DI из pinned UCD). Claude + GPT = 2/7
  (Gemini/DeepSeek/Qwen/Copilot пропустили).
- SPAN-TRACE вместо БИЕКЦИИ: биекция есть только 1:1; будущая канонизация (norm/compose)
  даёт one-to-many/collapse → биекции нет. Заменить на span-based position_trace
  (transform_kind IDENTITY/REMOVED/REPLACED/EXPANDED/COLLAPSED/REORDERED); в инкр-1 —
  identity. GPT = 1/7 (Kimi P7 «биекция тотальна» верно для removal-only инкр-1; остальные
  оставили «bijective»). Логически GPT прав про КОНТРАКТ.
- CANONICAL_VIEW identity-only в инкр-1 + ИЗОЛЯЦИЯ (не читать в вердикт-пути до гейта;
  API-контракт). GPT + Copilot = 2.
- FULL-DIFFERENTIAL гейт (явный список полей: verdict/effective/semantic/single/relation/
  context/witness/witness_count/order/positions/uncarded_invisibles/oracle_tuple/exception;
  guard_disabled==release baseline). GPT + Qwen + Copilot (+ Gemini deep-compare) = 3-4.
- ИНТЕГРАЦИЯ с _demask/sequence_engine incl F-NEW-1 (demask→guard→matcher→verify, no
  silent bypass). Copilot (+ Kimi MUT-G9 частично) = 1-2.
- PROVENANCE/schema_version явно + документированный API. Kimi + GPT + Qwen + Copilot = 4.

============================================================
ВЕРДИКТЫ ПОГОЛОВНО (сжато, по raw)
============================================================
Claude self-leg: SURVIVES + верен скелету; нашёл дыру гейта (guard-self-asserts) + scope-138.
  Run-grounded прототип (bijective_ok, все 138 incl карточные, context-free). Был мягок на
  гейте — GPT/Kimi дожали до структурной причины.
GPT (OpenAI): PLAN_SURVIVES_WITH_MAJOR_PATCHES; LOOPHOLE NO. Инкр-1+гейт «not yet as
  written», после патчей YES для батареи. Патчи: span-trace, canonical-identity-only, full-
  differential, guard-oracle, exact-set-138, mutation-split, scope-138-предикат, fail-visible,
  original-text-vs-bytes, purity/determinism.
Gemini: CLEAN SURVIVES по всем; «начать код немедленно». Один вклад: deep-vs-shallow
  compare. Пропустил scope-138 + биекцию + гейт-дыру.
Kimi (Moonshot): ПРИНЯТЬ С ПОПРАВКАМИ 1-7; LOOPHOLE NO. P8 (бакеты 97/12/6/23 = чистое
  разбиение 138). ДЫРА №1 + три условия (purity/exception/resource) + мутации split
  (G8/G9/G10) + сериализационная дельта + provenance.
DeepSeek: CLEAN SURVIVES по всем; «готов к коду»; гейт «исчерпывающ» (ОШИБОЧНО — опроверг.
  ДЫРА №1). Пропустил scope/биекцию/side-channels.
Qwen: SURVIVES с уточнениями (PATCH-FIRST). 4 дыры мутаций (original/non-bijective/schema/
  resource) + явный список полей гейта + r>g two-scanner concern. Пропустил scope + биекцию-
  обобщение (оставил «bijective»).
Copilot (Microsoft): SURVIVE_WITH_PATCHES (V-PATCH). Full-differential + bijectivity-проверки
  + resource/TRACE_TRUNCATED + canonical-изоляция (API) + ИНТЕГРАЦИЯ с _demask/F-NEW-1 +
  fail-closed-на-мерже + security-review. Пропустил scope + биекцию-обобщение.

END_OF_RAW_BUNDLE
