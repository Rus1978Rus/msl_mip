ЧАСТНЫЙ АВТОРСКИЙ ПРОЕКТ / COMMERCIAL USE PROHIBITED

DOCUMENT_ID: SIMULATION_ARTIFACT_ZERO_WIDTH_SPACE_U200B_TIER2_BY_CODE_v0_1_RU
DOCUMENT_TYPE: SIMULATION_ARTIFACT (RUN_CARD) — нога BY_CODE
PACKET_TYPE: SIMULATION
PACKET_SUBTYPE: TIER_2_SIMULATION_GATE
LEG: BY_CODE (прогон через настоящий движок msl_mip_runtime)
PAIR_WITH: BY_SPEC (модели гоняют ЭТУ ЖЕ батарею по описанию карточки);
  расхождение BY_CODE vs BY_SPEC = дыра между спекой и кодом
TEMPLATE_LINE: GEN3_v0_3
FORMAT_SOURCE: CONVEYOR_RUN_PACKET_TEMPLATE_v0_1_RU (Часть C, SIMULATION_RESULT)
  + образец честного провала черепа (SKULL_CROSSBONES: honest fail 5/14 → PASS 12/12)
RELATED_ARTIFACT: SIMULATION_ARTIFACT_ZERO_WIDTH_SPACE_U200B_TIER2_v0_1_RU
  (33-кейсовая батарея того же прогона; здесь — ТОЧНАЯ 17-кейсовая батарея
   для сверки один-в-один с моделями)
TARGET_CARD: SIGN_CORE_CARD_ZERO_WIDTH_SPACE_U200B_GEN3_v0_3_RU (commit 68e1a47)
AUTHOR: Руслан Малявский
CREATED_AT: 2026-07-13
STATUS: ACTIVE_ARTIFACT / NOT_LOCKED / NOT_RUNTIME
RUN_CARD_STATUS: HONEST_FAIL (см. VERDICT)

============================================================
B.1 СТАТУС СИМУЛЯЦИИ
============================================================
SIMULATION_ID: ZWSP_TIER2_BY_CODE_2026-07-13
SIMULATION_STATUS: LIVE_SELF_RUN (машина автора, движок msl_mip_runtime.analyze;
  регистратор — msl_mip_runtime.scan_uncarded_invisibles)
REVIEWER: LIVE_SELF_RUN (machine) — нога BY_CODE, не модель-ревьюер
SIMULATION_GATE_TIER: TIER_2 (ZONE_2)
FORMULAS:
  SIMULATION_RUN ≠ VALIDATION
  MEASURE_ONLY ≠ FIX (эта нога только МЕРЯЕТ)
  ATTACK_CAUGHT = верный сигнал человеку; FALSE_ALARM = ложь человеку
  МЕТРИКА — ВЕРНОСТЬ СОВЕТА, не поймал/пропустил
BATTERY_DISCIPLINE: батарея задана автором, прогнана КОДПОИНТ-В-КОДПОИНТ, без
  добавлений и изменений входов — чтобы BY_CODE и BY_SPEC сравнивались 1:1.

============================================================
B.2 ВХОДНЫЕ ДАННЫЕ / PARSER_SCOPE
============================================================
SOURCE_CARDS_USED (полные файлы):
  - SIGN_CORE_CARD_ZERO_WIDTH_SPACE_U200B_GEN3_v0_3_RU.md
  - SIGN_CORE_CARD_FULLWIDTH_SOLIDUS_UFF0F_GEN3_v0_3_RU.md  (маска ／ для A1)
PARSER_SCOPE: только ZWSP + маска ／ (ось «отношение» ZWSP жива, без конфликта
  с матчерами @/./☠). Заявлено явно.
TLD_STATE: HERMETIC, {com,org,net,ru,io,dev,xn--p1ai}.

ТОЧНЫЙ ВВОД ДЛЯ B2/B3 (записаны в батарее как фраза — взяты ЛИТЕРАЛЬНО, целиком;
привожу байты для сверки с моделями, чтобы нога BY_SPEC читала то же самое):
  B2: len=61  repr='very-long-url.example.com с soft-wrap ​ в отображаемом тексте'
       (ZWSP окружён пробелами — одиночный soft-wrap в отображаемой прозе)
  B3: len=22  repr='обычная проза без ZWSP'
       (реального U+200B НЕТ — буквы «ZWSP» это ASCII-текст)

============================================================
B.3 БАТАРЕЯ — СЫРОЙ ИЗМЕРЕННЫЙ ВЫВОД
(CTX/RISK — вердикт ребра ZWSP BOUNDARY_DISRUPTOR; VERDICT — effective_action
 всего движка; WITNESS — записи регистратора; MARK — верно/ошибка по классу)
============================================================
ID  CLASS   INPUT (codepoints)                            CTX              RISK   VERDICT              WIT      MARK
A1  ATTACK  g<U+043E><U+043E>g<U+200B><U+FF0F>le.com      HOST             HIGH   hold_pending_review  -        ВЕРНО
A2  ATTACK  paypa<U+200B>l.com                            HOST             HIGH   hold_pending_review  -        ВЕРНО
A3  ATTACK  user@examp<U+200B>le.com                      EMAIL            MEDIUM queue_for_review     -        ВЕРНО
A4  ATTACK  bad<U+200B>word                               BYTE_EXACT_TOKEN MEDIUM queue_for_review     -        ВЕРНО
A5  ATTACK  admin<U+200B>istrator                         BYTE_EXACT_TOKEN MEDIUM queue_for_review     -        ВЕРНО
A6  ATTACK  https://site.com/ad<U+200B>min/panel          PATH             MEDIUM queue_for_review     -        ВЕРНО
A7  ATTACK  па<U+200B>роль (кириллица)                    BYTE_EXACT_TOKEN MEDIUM queue_for_review     -        ВЕРНО
A8  ATTACK  g<U+043E><U+043E>g<U+200B><U+200B>le.com      HOST             HIGH   hold_pending_review  -        ВЕРНО
B1  PEACE   日本語<U+200B>のテキスト                            BYTE_EXACT_TOKEN MEDIUM queue_for_review     -        ОШИБКА(мягкий ложняк QUEUE)
B2  PEACE   ...soft-wrap <U+200B> в... (см. B.2)          FREE_TEXT        NONE   pass                 -        ВЕРНО
B3  PEACE   обычная проза без ZWSP                        -                -      pass                 -        ВЕРНО
B4  PEACE   src/utils/main.py                             -                -      pass                 -        ВЕРНО
B5  PEACE   docs.example.com/guide/very-long<U+200B>-sec  HOST             HIGH   hold_pending_review  -        ОШИБКА(ЖЁСТКИЙ ложняк HOLD)
B6  PEACE   version v1.2.3 release                        -                -      pass                 -        ВЕРНО
C1  UNKNOWN goog<U+2062>le.com                            -                -      pass                 U+2062   ВЕРНО
C2  UNKNOWN text<U+FEFF>here                              -                -      pass                 U+FEFF   ВЕРНО
C3  UNKNOWN abc<U+202E>def                                -                -      pass                 U+202E   ВЕРНО

============================================================
B.4 ЧЕСТНЫЙ СЧЁТ (honest fail, по образцу черепа)
============================================================
  ATTACK  : 8/8 верно   (0 ошибок)  — ни одной пропущенной атаки
  PEACE   : 4/6 верно   (2 ошибки)  — 1 жёсткий ложняк + 1 мягкий
  UNKNOWN : 3/3 верно   (0 ошибок)  — регистратор свидетельствует, вердикт не трогает
  --------------------------------------------------
  ИТОГО   : 15/17

  ATTACK пропущено: НЕТ.
  PEACE жёсткий ложняк (HOLD на легитимном): B5.
  PEACE мягкий ложняк (QUEUE на легитимном):  B1.
  UNKNOWN молча пропущено: НЕТ.

DIFFERENTIATION_CHECK: YES — результат различается по контекстам
  (HOST/EMAIL/BYTE_EXACT_TOKEN/PATH/FREE_TEXT), не «одинаково везде» = не архбаг.

============================================================
B.5 НАХОДКИ (FINDING_STATUS/BASIS обязательны)
============================================================

F1 — CONTEXT_CLASSIFIER_FALSE_POSITIVE (ЖЁСТКИЙ) — B5 [= R8-класс = OQ5]
  ЧТО: B5 docs.example.com/guide/very-long<ZWSP>-section (schemeless-домен,
    ZWSP глубоко в ПУТИ) → HOST/HIGH/hold_pending_review. ZWSP в пути, не в хосте.
  FINDING_STATUS: VERIFIED
  FINDING_BASIS:
    METHOD: живой прогон B5 через msl_mip_runtime.analyze.
    TARGET: sequence_engine._detect_context_at — ветка «маска внутри домена»
      (_domain_prefix у left_part+right_part принимает домен с хвостом-путём).
    OBSERVED: CTX=HOST, RISK=HIGH, VERDICT=hold_pending_review.
    EXPECTED: PATH/MEDIUM/queue (как A6 — тот же смысл, но СО СХЕМОЙ → верно).
  СВЯЗЬ: подтверждает OQ5 (NEXT_SESSION_FIX) на ТОЧНОМ входе батареи. В
    родственном 33-кейсовом прогоне тот же класс упал 4/4 — систематично.
  РАМКА: HOLD на честном URL подрывает доверие человека к HOLD — худший провал
    для системы оповещения.

F2 — CARD_PROMISE_VS_DETECTOR_GAP (мягкий) — B1 [SAFE_CASE_002 не держится]
  ЧТО: B1 日本語<ZWSP>のテキスト (японская ZWSP-сегментация) →
    BYTE_EXACT_TOKEN/MEDIUM/queue. Карточка SAFE_CASE_002 обещает NONE.
  FINDING_STATUS: VERIFIED
  FINDING_BASIS:
    METHOD: живой прогон B1.
    TARGET: sequence_engine._is_byte_exact_token — CJK/кана isalnum()=True →
      строка классифицируется как байт-токен → MEDIUM.
    OBSERVED: MEDIUM (обещание карточки NONE не выполнено на живом вводе).
    EXPECTED (карточка): NONE.
  СВЯЗЬ: в родственном прогоне CJK «東京<ZWSP>都では» дал тот же MEDIUM; тайский
    прошёл лишь случайно (combining marks). Различение CJK/тайский непринципиально.

ОБЕ ОШИБКИ — ЛОЖНЫЕ ТРЕВОГИ на легитимном (спека обещает молчание, код сигналит).
Ни одной пропущенной атаки; регистратор целен. Это НЕ архбаг — это две дыры
между обещанием карточки и поведением детектора.

============================================================
B.6 VERDICT
============================================================
SIMULATION_VERDICT (BY_CODE): HONEST_FAIL — 15/17

  ПОЧЕМУ НЕ PASS: класс МИРНОЕ упал 4/6 — 1 жёсткий ложняк (B5, HOLD на честном
  URL) + 1 мягкий (B1, QUEUE на японской сегментации). Как у черепа первый
  прогон честно упал 5/14. Батарея, прошедшая бы 100%, была бы подозрительна —
  эта поймала ровно те две дыры, что мы искали (R8 и CJK).

  ЧТО ДЕРЖИТСЯ:
    - ATTACK 8/8 — детектор не пропускает атаки во всех контекстах
      (домен, homoglyph+маска, email, byte-token, идентификатор, путь,
       кириллица, двойной ZWSP).
    - UNKNOWN 3/3 — регистратор свидетельствует (U+2062/BOM/RLO) и НЕ меняет
      вердикт.
    - Рамка «оповещение, не антивирус» держится: ничего не режется/не удаляется.

  КАРТА ПРОВАЛОВ (чинить НЕ в этом заходе — только измерено):
    F1  B5  R8-класс, ложный HOST/HIGH        [HARD, = OQ5 NEXT_SESSION_FIX]
    F2  B1  CJK/SAFE_CASE_002 не держится      [SOFT, новая находка]

  ДЛЯ СВЕРКИ BY_SPEC: если модель по описанию карточки поставит B5 → PATH/MEDIUM
  (как обещает RUNTIME_REALITY) или B1 → NONE (как обещает SAFE_CASE_002), а код
  выдаёт HOST/HIGH и MEDIUM — это и есть точки расхождения спека↔код. Спека
  обещает то, чего код не делает: F1 (карта уже помечена OQ5), F2 (карта ещё
  обещает NONE, код даёт MEDIUM — карту тоже надо привести к реальности).

CONVEYOR_EXIT_CONDITION: HONEST_FAIL → патч-цикл перед re-run. Архбагов нет,
  DIFFERENTIATION достигнут. Провалы — ложные тревоги, не непроходимость pipeline.
NEXT_STEP: сверка с ногой BY_SPEC → карта расхождений → патч-цикл (F1=OQ5, F2) →
  повторный TIER_2 на этой же батарее. НЕ ЧИНИМ ЗДЕСЬ.

END_OF_SIMULATION_ARTIFACT
