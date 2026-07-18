ЧАСТНЫЙ АВТОРСКИЙ ПРОЕКТ / COMMERCIAL USE PROHIBITED

DOCUMENT_ID: AUTHOR_DECISION_20260718_D-GUARD-IMPL-PLAN
DOCUMENT_TYPE: AUTHOR_DECISION
DECISION_ID: D-GUARD-IMPL-PLAN
STATUS: DRAFT — план реализации инкремента-1 на реальном раскладе конвейера. КОД НЕ
  ПИСАН. Ждёт финального author decision. ZWSP не трогать до ЗЕЛЁНОГО гейта (гейт теперь
  = verdict-identity + shadow-оракул + robustness-кейсы).
DATE: 2026-07-18
AUTHOR: Руслан Малявский (AUTHOR_DECISION_STATUS_AUTHORITY)
PROJECT: MSL/MIP Sign Alphabet
SCOPE: ПЛАН реализации INVISIBLE_DEFAULT_IGNORABLE_GUARD, инкремент 1 (shadow-аннотатор).
  Продолжение D-GUARD-DESIGN (скелет APPROVED). Код — только после этого решения.

РАМКА ПРОЕКТА: система ОПОВЕЩЕНИЯ, не антивирус. Машина свидетель, не судья.

============================================================
РЕШЕНИЕ (кратко)
============================================================
План инкремента-1 ПРИНЯТ С ОБЯЗАТЕЛЬНЫМИ ПОПРАВКАМИ. Ядро (shadow-аннотатор → новое
поле class_guard, вердикт не трогается, acceptance-гейт обязателен) — принято всеми
7/7 ног, LOOPHOLE 0/7, дрейфа нет. НО гейт как написан ДОКАЗУЕМО недостаточен: он не
может валидировать shadow-поле, которое вердикт-путь не читает. Обязательные поправки
ниже смыкают доказательство не-контаминации.

============================================================
ПРОВЕНАНС (расклад конвейера — честно, по raw)
============================================================
Конвейер по CONVEYOR_PACKET_GUARD_IMPL_PLAN_2026-07-18. Перепроверка по raw (Claude
Code, RAW_REVIEWS_GUARD_IMPL_PLAN_2026-07-18.md).

НОГ: 6 ВНЕШНИХ вердиктов (GPT/OpenAI, Gemini, Kimi/Moonshot, DeepSeek, Qwen,
  Copilot/Microsoft) + 1 self-leg (Claude/Anthropic) = 7. Семейств 7. ИСКЛЮЧЁН: 1
  META_ASSESSMENT (предсказывал ревьюеров + ФАБРИКАЦИЯ кода — выдуманные сниппеты как
  «цитаты репо»; verification фейковая). Не в счёте.

РАСКЛАД ПО ГЛУБИНЕ:
  - SURVIVES С ПОПРАВКАМИ (patch-first): 5 — Claude, GPT, Kimi, Qwen, Copilot.
  - CLEAN SURVIVES (code-now): 2 — Gemini, DeepSeek. ⚠ ОБА пропустили реальные дефекты
    (scope-138, биекцию, дыру гейта); DeepSeek назвал гейт «исчерпывающ» — ОПРОВЕРГНУТО
    логикой (см. ДЫРА №1). Раскол НЕ равноценен: строгие правы, мягкие ошиблись.
  - LOOPHOLE / «ломает ZWSP»: 0/7. Ядро (shadow+поле+гейт+reuse+детект-до-нормализации+
    охват-138): ПРИНЯТО 7/7.

ЧЕСТНО: нога Claude была МЯГКА на гейте (нашла дыру, но не структурную причину) — Kimi/
  GPT дожали. Записано, не защищается.

============================================================
ДЫРА ГЕЙТА №1 — ПОДТВЕРЖДЕНА ЛОГИКОЙ (не гипотеза)
============================================================
Гейт ассертит идентичность полей ВЕРДИКТ-ПУТИ. class_guard — shadow, вердикт-путём НЕ
читается → его порча (кривая карта позиций, битые members) НЕ меняет вердикт/witness/
позиции → verdict-identity зелен при БИТОМ class_guard. Тест, проверяющий только X, не
ловит порчу в Y, которое ничто наблюдаемое не читает. ЛОГИЧЕСКИЙ ФАКТ.
ПОДДЕРЖКА 5/7 (Kimi+WHY, GPT guard-oracle+set-138, Qwen bijectivity-assert, Copilot
  formal-bijectivity, Claude guard-self-asserts); Gemini частично; DeepSeek против(ошибочно).
СЛЕДСТВИЕ: гейт ОБЯЗАН включать ОТДЕЛЬНЫЙ property-оракул для class_guard, не только
  verdict-identity.

============================================================
РЕШЕНИЕ — ЧТО ПРИНЯТО (ядро, 7/7)
============================================================
1. ИНКРЕМЕНТ 1 = SHADOW-АННОТАТОР: чистая функция → новое поле отчёта class_guard;
   вердикт-путь (single_actions/relation_actions/semantic_action/effective_action) НЕ
   трогается; вердикт не меняется. Принято 7/7.
2. ACCEPTANCE-ГЕЙТ ОБЯЗАТЕЛЕН: без зелёного — мержа нет. Принято 7/7.
3. REUSE _invisible_candidate (r>g, не параллельный расходящийся сканер); детект/annotate
   ДО нормализации; охват всех 138 сразу (карточные включены). Принято 7/7.

============================================================
ОБЯЗАТЕЛЬНЫЕ ПОПРАВКИ (условие перед кодом; со счётом поддержки)
============================================================
P1. SHADOW-ОРАКУЛ для class_guard (ДЫРА №1, 5/7 — ЛОГИЧЕСКИ ОБЯЗАТЕЛЕН): гейт = verdict-
    identity + property-оракул class_guard. Property-тесты: биективность/согласованность
    карты (∀i canon[i]==orig[map[i]]), CENSUS-138 (строка со всеми членами → ровно 138 с
    верными кодпоинтами/бакетами), canonical_view==reference-strip (дифференциальный
    оракул), identity-on-clean, идемпотентность.
P2. ТРИ УСЛОВИЯ НЕ-КОНТАМИНАЦИИ — в требования инкремента-1:
    (i) PURITY предиката _invisible_candidate (referential transparency; reuse=ВЫЗОВ, не
        копипаст) — 2/7. Тесты CALL_TWICE/CALL_ORDER/PARALLEL.
    (ii) EXCEPTION containment (fail-open РАНТАЙМ): ошибка гарда → class_guard={status:
        GUARD_FAILURE}, конвейер продолжает бит-в-бит — 3/7. + fail-CLOSED на МЕРЖЕ
        (аномалия → reject merge, Copilot) — комплементарно.
    (iii) RESOURCE bound: кап members[] + TRACE_TRUNCATED ПЕРЕНЕСТИ в инкремент-1 (батарея
        21/21 не флудит → OOM не ловит) — 4/7. Robustness-кейсы: флуд 1M невидимых, битый
        UTF-8/одиночные суррогаты (GUARD_FAILURE), астральные границы.
P3. МУТАЦИИ переписать под инкремент-1 — 4/7: MUT-G3/G4/G6 (strip/safe_to_delete/overflow)
    невыразимы в инкр-1 → перенести в свои инкременты; добавить MUT-G8 (card_mask flip),
    MUT-G9 (detect-после-нормализации, урок F-NEW-1), MUT-G10 (offset-drift codepoint vs
    UTF-16 астральные), + original-modified, non-bijective, schema_version-mismatch.
P4. SCOPE-138-ONLY предикат — 2/7 (но факт кода): _invisible_candidate ШИРЕ 138 (VS/
    braille/whitespace); ввести отдельный is_monitored_control_138 (Cf∧DI из pinned UCD),
    не приравнивать reuse к «ровно 138». Инвариант: членство только из pinned Unicode-
    свойств, не из рендера/эвристики/контекста/имени family.
P5. SPAN-TRACE вместо БИЕКЦИИ как КОНТРАКТ — 1/7 (логически верно): биекция есть только
    1:1; будущая канонизация даёт one-to-many/collapse → биекции нет. Контракт = span-based
    position_trace (transform_kind IDENTITY/REMOVED/REPLACED/EXPANDED/COLLAPSED/REORDERED);
    в инкременте-1 — canonical_view=identity, trace=identity (тогда карта тотальна, Kimi P7).
P6. CANONICAL_VIEW identity-only в инкр-1 + ИЗОЛЯЦИЯ — 2/7: не проектировать нетривиальную
    канонизацию сейчас; API-запрет читать canonical_view в вердикт-пути до гейта.
P7. FULL-DIFFERENTIAL гейт — 3-4/7: явный список идентичных полей (verdict, effective_/
    semantic_action, single_/relation_actions, context, witness, witness_count/order,
    original_positions, uncarded_invisibles, oracle_tuple, exception_status); единственная
    дельта = +поле class_guard; guard_disabled == текущий release baseline; deep (не shallow)
    сравнение; пин сериализационной дельты (ровно +1 ключ). Герметичность (pinned UCD/версия/
    locale/no-network/детерминизм).
P8. ИНТЕГРАЦИЯ с _demask/sequence_engine incl F-NEW-1 — 1-2/7: тест demask→guard→matcher→
    verify, no silent bypass.
P9. PROVENANCE явно (ucd_version, table_hash) + определения bucket/family в schema_version +
    документированный GuardResult API — 4/7.

============================================================
РЕКОМЕНДУЕМЫЙ ИНКРЕМЕНТ-1 (после патчей — материал к коду)
============================================================
class_guard_annotate(text, ucd_snapshot) -> GuardResult:
  schema_version, ucd_version, original_text (входная строка analyze, НЕ «байты» —
    P5/GPT: str = кодпоинты), members[] {codepoint, unicode_name, original_offset(codepoint
    index), class_bucket (PURE/DIR/TAG/DEP), family, card_mask, provenance}, canonical_view
    (IDENTITY only), position_trace (identity spans), status.
  Вставка в analyze() как ТОЛЬКО-отчётное поле class_guard; не менять сканер/матчеры/
    action-списки/context/witness/вердикт. Детект ДО нормализации.
Гейт мержа: full-differential + shadow-property-оракул + census-138 + robustness + guard-
  мутации (инкр-1 набор) + purity/determinism. Мерж только при 0 запрещённых дельт.

============================================================
OPEN / ГРАНИЦА
============================================================
- КОД пишется ТОЛЬКО после этого author decision по плану-с-поправками.
- ZWSP НЕ ТРОГАТЬ до ЗЕЛЁНОГО гейта (гейт = verdict-identity + shadow-оракул + robustness).
- ИНКРЕМЕНТ 2 (поглощение регистратора, sequence-поля, policy-strip) + рантайм-ремэппинг
  (O1) — отдельные заходы; каждый со своим гейтом.
- НЕ пересматривает: скелет D-GUARD-DESIGN, класс 138, HYBRID_C.

============================================================
FORK_STATUS
============================================================
FORK_STATUS: PARTIAL —
  ПЛАН ИНКРЕМЕНТА-1 (ядро 7/7) + ОБЯЗАТЕЛЬНЫЕ ПОПРАВКИ P1-P9: готов как материал к
    AUTHOR_DECISION. Ядро принято, дыра гейта №1 подтверждена логикой, патч-сет сведён.
  КОД + зелёный гейт (verdict-identity + shadow-оракул + robustness) + инкремент 2 + O1:
    OPEN — PENDING. Реализация только ПОСЛЕ author decision, с зелёным гейтом.

============================================================
СВЯЗЬ
============================================================
- foundation_layer/AUTHOR_DECISION_20260718_D-GUARD-DESIGN.md — APPROVED скелет (BASIS);
- conveyor_runs/CONVEYOR_PACKET_GUARD_IMPL_PLAN_2026-07-18.md — пакет;
- conveyor_runs/RAW_REVIEWS_GUARD_IMPL_PLAN_2026-07-18.md — 7 raw (сверяемо);
- tests/sim_bycode_v2.py + tests/zwsp_oracle_manifest.py — батарея 21/21 (часть гейта);
- msl_mip_runtime.py (_invisible_candidate/scan_uncarded_invisibles/analyze),
  sequence_engine.py (_demask/F-NEW-1) — точки интеграции.

END_OF_AUTHOR_DECISION
