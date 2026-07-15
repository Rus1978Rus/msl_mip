ЧАСТНЫЙ АВТОРСКИЙ ПРОЕКТ / COMMERCIAL USE PROHIBITED

DOCUMENT_ID: SIMULATION_ARTIFACT_ZERO_WIDTH_SPACE_U200B_TIER2_BY_CODE_v0_2_RU
DOCUMENT_TYPE: SIMULATION_ARTIFACT (RUN_CARD) — нога BY_CODE, пересборка v0_2
PACKET_TYPE: SIMULATION / PACKET_SUBTYPE: TIER_2_SIMULATION_GATE
LEG: BY_CODE (живой движок msl_mip_runtime)
PAIR_WITH: BY_SPEC (модели по описанию карточки) → RECONCILE
ORACLE: tests/zwsp_oracle_manifest.md (независимый третий эталон, написан ДО прогона;
  машинный источник — zwsp_oracle_manifest.py)
FORMAT_SOURCE: CONVEYOR_RUN_PACKET_TEMPLATE_v0_1_RU (Часть C) + образец честного
  провала черепа (SKULL_CROSSBONES: honest fail 5/14 → PASS 12/12)
SUPERSEDES: SIMULATION_ARTIFACT_..._BY_CODE_v0_1_RU (17-кейсовая; здесь выверенное
  ядро 21 + правки метода: reconcile-по-кортежу, preflight кодпоинтов, mutation-adequacy)
TARGET_CARD: SIGN_CORE_CARD_ZERO_WIDTH_SPACE_U200B_GEN3_v0_3_RU (commit 68e1a47)
AUTHOR: Руслан Малявский / CREATED_AT: 2026-07-13
STATUS: ACTIVE_ARTIFACT / NOT_LOCKED / NOT_RUNTIME
HISTORICAL_STATUS: SUPERSEDED_PRE_PATCH_HONEST_FAIL_SNAPSHOT (2026-07-15:
  заменён SIMULATION_ARTIFACT_..._BY_CODE_v0_3_RU — проходной прогон 21/21 на
  пост-патчевом коде ENGINE_COMMIT 9963a68; этот файл сохранён как честная
  история «до» и содержательно не менялся)
RUN_CARD_STATUS: HONEST_FAIL (6/21; mutation-adequacy 3/5)

============================================================
B.1 СТАТУС / МЕТОД
============================================================
SIMULATION_ID: ZWSP_TIER2_BY_CODE_v2_2026-07-13
REVIEWER: LIVE_SELF_RUN (machine) — нога BY_CODE
SIMULATION_GATE_TIER: TIER_2 (ZONE_2)
CARDS_USED: [ZWSP U+200B, FULLWIDTH SOLIDUS U+FF0F] (полные файлы) / TLD HERMETIC
FORMULAS: SIMULATION_RUN≠VALIDATION; MEASURE_ONLY≠FIX;
  ATTACK_CAUGHT=верный сигнал; FALSE_ALARM=ложь человеку; МЕТРИКА=верность совета.
ПРАВКИ МЕТОДА (по требованию конвейера):
  1. RECONCILE ПО КОРТЕЖУ, не по вердикту — сверяется весь кортеж
     (CONTEXT, RELATION_ROLE, RISK, VERDICT, WITNESS). SAME_VERDICT≠SAME_SEMANTICS:
     класс CONTEXT_MISMATCH_SAME_VERDICT выделен отдельно (сработал на U1).
  2. PREFLIGHT КОДПОИНТОВ — перед прогоном dump ords+длина и assert must_contain
     (защита от «copy-paste выронил невидимку»). Результат: ALL OK (21/21).
  3. MUTATION-ADEQUACY — 5 мутаций кода, проверка что батарея их УБИВАЕТ.

============================================================
B.2 PREFLIGHT (все входы целы)
============================================================
21/21 ALL OK. Каждый must_contain-кодпоинт присутствует; D4 обе стадии целы
(RAW без литерального U+200B; decoded содержит U+200B). Ни одна невидимка не
потеряна при подготовке батареи.

============================================================
B.3 БАТАРЕЯ — ИЗМЕРЕННЫЙ КОРТЕЖ vs ОРАКУЛ
(CTX/RISK — ребро ZWSP BOUNDARY_DISRUPTOR; VERDICT — effective_action; WIT — witness)
============================================================
ID  CLASS      INPUT (codepoints)                      CTX              RISK   VERDICT              WIT      РЕЗУЛЬТАТ
R1  registrar  goog<U+2800>le.com                      -                -      pass                 -        ОШИБКА WITNESS_LOST(U+2800)
R2  registrar  paypal<U+00A0>.com                      -                -      pass                 -        ОШИБКА WITNESS_LOST(U+00A0)
R3  registrar  admin<U+202F>panel                      -                -      pass                 -        ОШИБКА WITNESS_LOST(U+202F)
R4  registrar  line1<U+2028>line2                      -                -      pass                 -        ОШИБКА WITNESS_LOST(U+2028)
R5  registrar  para<U+2029>break                       -                -      pass                 -        ОШИБКА WITNESS_LOST(U+2029)
R6  registrar  text<U+200B>here                        BYTE_EXACT_TOKEN MEDIUM queue_for_review     -        ВЕРНО
P1  positions  <U+200B>paypal.com                      HOST             HIGH   hold_pending_review  -        ОШИБКА FALSE_POSITIVE_HOLD (ждали BYTE_EXACT/MEDIUM)
P2  positions  paypal.com<U+200B>                      HOST             HIGH   hold_pending_review  -        ОШИБКА FALSE_POSITIVE_HOLD (ждали MEDIUM)
P4  positions  paypal.com<U+200B>/path                 HOST             HIGH   hold_pending_review  -        ОШИБКА FALSE_POSITIVE_HOLD + FORBIDDEN_CTX(HOST)
P5  positions  docs.example.com/...long<U+200B>-sec    HOST             HIGH   hold_pending_review  -        ОШИБКА FALSE_POSITIVE_HOLD + FORBIDDEN_CTX(HOST)  [R8]
K1  combo      goog<U+200B><U+200D>le.com              FREE_TEXT        NONE   pass                 U+200D   ОШИБКА FALSE_NEGATIVE (атака пропущена!)
K3  combo      goog<U+200B><U+2062>le.com              FREE_TEXT        NONE   pass                 U+2062   ОШИБКА FALSE_NEGATIVE (атака пропущена!)
U1  url        https://site.example/?q=bad<U+200B>word PATH             MEDIUM queue_for_review     -        ОШИБКА CONTEXT_MISMATCH_SAME_VERDICT (ждали QUERY_VALUE)
U2  url        us<U+200B>er@example.com                EMAIL            MEDIUM queue_for_review     -        ВЕРНО
D1  dangerous  paypal<U+200B>.com                      HOST             HIGH   hold_pending_review  -        ВЕРНО (+ differential: source⊃U+200B, recon≠raw)
D2  dangerous  http://paypal.com<U+200B>@evil.com      HOST             HIGH   hold_pending_review  -        ОШИБКА FORBIDDEN_CTX(HOST) + NO_HOST_EXTRACTION
D3  dangerous  paypal<U+200B>.com.                     HOST             HIGH   hold_pending_review  -        ВЕРНО
D4  dangerous  paypal%E2%80%8Bl.com                    -                -      pass                 -        ВЕРНО (RAW не сработал ложно)
       └ STAGE2 decoded: paypal<U+200B>l.com → HOST / HIGH / hold_pending_review  (ВЕРНО)
D5  dangerous  goog<U+200B><U+2800>le.com              FREE_TEXT        NONE   pass                 -        ОШИБКА FALSE_NEGATIVE + WITNESS_LOST(U+2800)
T1  controls   日本語<U+200B>のテキスト                       BYTE_EXACT_TOKEN MEDIUM queue_for_review     -        ОШИБКА FALSE_POSITIVE_QUEUE (SAFE_CASE_002)
N1  controls   обычный текст с пробелами (U+0020)      -                -      pass                 -        ВЕРНО (нет witness-flood)

============================================================
B.4 СЧЁТ ПО КЛАССАМ + ОШИБКИ ПО ТИПАМ (раздельно, как требовал конвейер)
============================================================
  registrar : 1/6   (только R6; R1-R5 witness_lost)
  positions : 0/4   (все — ложный HOST/HIGH/HOLD)
  combo     : 0/2   (обе — ПРОПУЩЕННАЯ атака)
  url       : 1/2   (U2 ok; U1 context-mismatch)
  dangerous : 3/5   (D1/D3/D4 ok; D2, D5 упали)
  controls  : 1/2   (N1 ok; T1 F2-регресс)
  --------------------------------
  ИТОГО     : 6/21

  ОШИБКИ ПО ТИПАМ:
    WITNESS_LOST                 : 6   (R1-R5, D5)
    FALSE_POSITIVE_HOLD          : 5   (P1,P2,P4,P5,D2)
    FORBIDDEN_RISK(HIGH)         : 4   (P1,P2,P4,P5)
    FORBIDDEN_VERDICT(HOLD)      : 4   (P1,P2,P4,P5)
    FALSE_NEGATIVE               : 3   (K1,K3,D5)  ← ПРОПУЩЕННЫЕ АТАКИ
    FORBIDDEN_CTX(HOST)          : 3   (P4,P5,D2)
    CONTEXT_MISMATCH_SAME_VERDICT: 1   (U1)
    FALSE_POSITIVE_QUEUE         : 1   (T1)
    NO_HOST_EXTRACTION           : 1   (D2)

============================================================
B.5 MUTATION-ADEQUACY (проверка самой проверки) — 3/5 killed
============================================================
  M1  HOST↔PATH swap          : KILLED   (ломает D1,D3,D4 — ждут HOST/HIGH, получают PATH)
  M2  witness predicate OFF   : SURVIVED — СЛЕПОЕ ПЯТНО (code-masked)
  M3  U+200B scan OFF         : KILLED   (ломает D1,D3,D4,R6,U2 — атаки пропадают)
  M4  facet risk-producing    : SURVIVED — СЛЕПОЕ ПЯТНО (harness-weakness)
  M5  context → FREE_TEXT     : KILLED   (ломает D1,D3,D4,R6,U2 — всё в pass)
  MUTATION_ADEQUACY: 3/5

  СЛЕПОЕ ПЯТНО M2 (witness OFF не пойман): НИ ОДИН baseline-верный кейс не
    держится на живом witness — R1-R5 уже падают (предикат узок), K1/K3
    выдают witness, но падают по FALSE_NEGATIVE, R6 witness не ждёт. Значит
    отключение witness ничего в pass-множестве не меняет. Это ПОСЛЕДСТВИЕ
    других провалов кода: пока предикат сломан, батарея не может проверить
    witness on/off. Закроется, когда R1-R5 начнут проходить (тогда M2 убьётся).
  СЛЕПОЕ ПЯТНО M4 (facet risk-producing не пойман): это слабость ХАРНЕССА, не
    кода. Инвариант facet_leak привязан к runtime_role, а мутация именно роль и
    двигает (ABSENCE_CONFUSABLE→PRIMARY). ПРОВЕРЕНО: на goog<ZWSP>le.com
    ABSENCE_CONFUSABLE baseline=NONE, mutant=HIGH — инвариант, привязанный к
    RELATION_TYPE (а не роли), убил бы M4 (→ было бы 4/5). Фикс харнесса
    известен; в этом заходе НЕ меняю (симуляция только меряет).

============================================================
B.6 НАХОДКИ (severity-порядок для системы ОПОВЕЩЕНИЯ; FINDING_STATUS/BASIS)
============================================================

F-NEW-1 — MISSED_ATTACK: второй невидимый рвёт детекцию ZWSP [K1,K3,D5] ★ ХУДШЕЕ
  ЧТО: невидимый БЕЗ карточки сразу после ZWSP (ZWJ U+200D / U+2062 / U+2800)
    остаётся в реконструкции (демаск снимает ТОЛЬКО mask-chars = U+200B/／),
    _looks_like_domain падает на остаточном невидимом → CONTEXT=FREE_TEXT →
    RISK=NONE → VERDICT=pass. Система МОЛЧИТ на goog<ZWSP><X>le.com.
  FINDING_STATUS: VERIFIED
  FINDING_BASIS: METHOD живой прогон K1/K3/D5; TARGET sequence_engine._detect_
    context_at (демаск run_mask_chars не включает некарточные невидимки);
    OBSERVED ctx=FREE_TEXT, risk=NONE, verdict=pass; EXPECTED HOST/HIGH/HOLD.
  РАМКА: для системы оповещения ПРОПУСК атаки хуже ложной тревоги — человек
    не получает НИКАКОГО сигнала. Тривиальный обход: подставь второй невидимый.
  NB: witness по второму знаку в K1/K3 ЕСТЬ (U+200D/U+2062), но основной
    ZWSP-вердикт схлопнут — witness не компенсирует пропуск атаки.

F-NEW-2 — FALSE_POSITIVE_HOLD: ZWSP рядом с целым доменом → ложный HOST/HIGH
  [P1 leading, P2 trailing, P4 after-domain-before-/, P5 deep-path/R8, D2 userinfo]
  ЧТО: ветка «маска внутри домена» (concat left+right через _domain_prefix)
    принимает любой ведущий домен с хвостом → HOST/HIGH/HOLD, хотя метка НЕ
    разорвана (ZWSP — паддинг/после домена/в пути/в userinfo).
  FINDING_STATUS: VERIFIED
  FINDING_BASIS: METHOD прогон P1/P2/P4/P5/D2; TARGET _detect_context_at строки
    ~499 (concat-host) и scheme-ветка (не парсит userinfo); OBSERVED HOST/HIGH;
    EXPECTED BYTE_EXACT/PATH/MEDIUM (P*), userinfo/MEDIUM (D2).
  ШИРЕ ЧЕМ R8: прежний OQ5 ловил только P5; здесь тот же корень бьёт по 5 кейсам.

F-NEW-3 — WITNESS_LOST: регистратор молча пропускает Zs/Zl/Zp/So [R1-R5,D5]
  ЧТО: предикат Cf∪bidi∪default-ignorable НЕ ловит NBSP(Zs), narrow-NBSP(Zs),
    U+2028(Zl), U+2029(Zp), U+2800 BRAILLE BLANK(So, рендерится пусто).
  FINDING_STATUS: VERIFIED
  FINDING_BASIS: METHOD прогон R1-R5,D5; TARGET msl_mip_runtime._invisible_reason;
    OBSERVED witness пусто; EXPECTED witness={соответствующий кодпоинт}.
  РАМКА: свидетель, молча не видящий пустой браль-символ, даёт ложное «чисто».

F-NEW-4 — CONTEXT_MISMATCH_SAME_VERDICT: нет контекста QUERY_VALUE [U1]
  ЧТО: ZWSP в query (?q=bad<ZWSP>word) классифицирован как PATH. Вердикт
    совпал (MEDIUM/queue), контекст неверен.
  FINDING_STATUS: VERIFIED
  FINDING_BASIS: METHOD прогон U1; scheme-ветка _detect_context_at различает
    только HOST/PATH/URL, QUERY_VALUE-ветки нет; OBSERVED PATH; EXPECTED QUERY_VALUE.
  NB: ровно тот класс, ради которого введена правка метода #1 (reconcile по
    кортежу) — по одному вердикту дыра была бы невидима.

F-NEW-5 — NO_HOST_EXTRACTION: движок не парсит userinfo@host [D2]
  FINDING_STATUS: VERIFIED
  FINDING_BASIS: слой _detect_context_at классифицирует контекст ПОЗИЦИИ, но не
    извлекает host-строку; evil.com как host не подтверждается, userinfo-регион
    трактуется как HOST. Способность отсутствует.

F-KNOWN-6 — F2 CJK: SAFE_CASE_002 не держится [T1]
  日本語<ZWSP>のテキスト → BYTE_EXACT_TOKEN/MEDIUM (карточка обещает NONE).
  FINDING_STATUS: VERIFIED (повтор находки прошлого прогона; контроль T1 её ловит).

F-METHOD-7 — СЛЕПЫЕ ПЯТНА БАТАРЕИ [M2, M4] (см. B.5)
  M2 code-masked (закроется с починкой предиката); M4 harness-weakness
  (инвариант привязать к RELATION_TYPE, не к роли — ПРОВЕРЕНО, убьёт).

============================================================
B.7 ЧТО ДЕРЖИТСЯ
============================================================
  - 6/21 верно: R6, U2, D1, D3, D4, N1.
  - D4 двустадийно ТОЧНО: RAW не сработал ложно на %E2%80%8B; decoded→HOST/HIGH.
  - N1 негативный контроль: обычный U+0020 НЕ даёт witness-flood (важно на
    случай расширения предиката под R1-R5).
  - D1 differential: source⊃U+200B И реконструированный host≠raw.
  - Preflight 21/21 — ни одной потерянной невидимки.
  - DIFFERENTIATION достигнут (контексты различаются) — не архбаг.
  - Рамка держится: ни один вердикт ничего не режет/не удаляет.

============================================================
B.8 ТОЧКИ ДЛЯ RECONCILE (BY_CODE vs BY_SPEC vs ORACLE)
============================================================
  Где нога BY_SPEC (чтение карточки) разойдётся с BY_CODE — там дыра. Заранее
  видно по оракулу, что код НЕ выполняет:
    * P1/P2/P4/P5 — оракул/спека: не HOST/HIGH; код: HOST/HIGH  → код-баг.
    * K1/K3/D5    — оракул: HOST/HIGH+witness; код: pass         → код-баг (пропуск).
    * R1-R5,D5    — оракул: witness; код: молчит                → код-баг (предикат).
    * U1          — оракул: QUERY_VALUE; код: PATH               → код-баг (нет контекста).
    * D2          — оракул: host=evil.com; код: нет извлечения   → код-пробел.
  ОТДЕЛЬНО — где КАРТОЧКА сама переобещает (спека vs оракул):
    * T1 — карточка SAFE_CASE_002 обещает NONE; оракул тоже ждёт NONE; код даёт
      MEDIUM. Карточку тоже надо привести к реальности (F2 в OQ следующего захода).

============================================================
B.9 VERDICT
============================================================
SIMULATION_VERDICT (BY_CODE): HONEST_FAIL — 6/21 ; MUTATION_ADEQUACY 3/5

  Выверенное ядро 21 оказалось куда диагностичнее прежней батареи (было 15/17
  ложно-обнадёживающе). Поймано, помимо известных R8+CJK:
    - ПРОПУСК АТАК (K1/K3/D5) — второй невидимый глушит детекцию ZWSP [★новое, худшее];
    - широкий ложный HOST/HIGH на позициях (P1/P2/P4) — шире R8;
    - систематический witness-пропуск Zs/Zl/Zp/So (R1-R5);
    - отсутствие контекста QUERY_VALUE (U1) — пойман только reconcile-по-кортежу;
    - отсутствие userinfo-парсинга (D2).
  Плюс батарея честно показала ДВА своих слепых пятна (M2 code-masked, M4
  harness-weakness) — 3/5 mutation-adequacy.

  КАРТА ПРОВАЛОВ ДЛЯ ПАТЧ-ЦИКЛА (чинить НЕ здесь):
    P0  F-NEW-1  пропуск атаки при втором невидимом      [MISSED_ATTACK ★]
    P1  F-NEW-2  ложный HOST/HIGH рядом с целым доменом   [включает R8/OQ5]
    P1  F-NEW-3  witness-предикат узок (Zs/Zl/Zp/So)
    P2  F-NEW-4  нет контекста QUERY_VALUE
    P2  F-NEW-5  нет userinfo-парсинга (D2)
    P2  F-KNOWN-6 карточка SAFE_CASE_002 vs код (CJK)
    HARNESS F-METHOD-7 facet-инвариант привязать к RELATION_TYPE; добавить
      witness-положительный проходящий кейс, чтобы M2 стал убиваемым.

CONVEYOR_EXIT_CONDITION: HONEST_FAIL → RECONCILE с BY_SPEC → карта расхождений →
  патч-цикл → повторный TIER_2 на этой же батарее (+ ужесточить харнес до 5/5).
  Архбагов нет, DIFFERENTIATION достигнут. Провалы — пропуски/ложные тревоги/
  пробелы покрытия, не непроходимость pipeline.
NEXT_STEP: НЕ ЧИНИМ ЗДЕСЬ — только измерено. Жду ногу BY_SPEC для сводки.

END_OF_SIMULATION_ARTIFACT
