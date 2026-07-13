ЧАСТНЫЙ АВТОРСКИЙ ПРОЕКТ / COMMERCIAL USE PROHIBITED

DOCUMENT_ID: SIMULATION_ARTIFACT_ZERO_WIDTH_SPACE_U200B_TIER2_v0_1_RU
DOCUMENT_TYPE: SIMULATION_ARTIFACT (RUN_CARD)
PACKET_TYPE: SIMULATION
PACKET_SUBTYPE: TIER_2_SIMULATION_GATE
TEMPLATE_LINE: GEN3_v0_3
FORMAT_SOURCE: CONVEYOR_RUN_PACKET_TEMPLATE_v0_1_RU (Часть C, SIMULATION_RESULT)
   + формат честного провала по образцу черепа
     (SIGN_CORE_CARD_SKULL_CROSSBONES_U2620: honest fail 5/14 → патч → PASS 12/12)
TARGET_CARD: SIGN_CORE_CARD_ZERO_WIDTH_SPACE_U200B_GEN3_v0_3_RU (commit 68e1a47)
AUTHOR: Руслан Малявский
CREATED_AT: 2026-07-13
STATUS: ACTIVE_ARTIFACT / NOT_LOCKED / NOT_RUNTIME
RUN_CARD_STATUS_BEFORE: NOT_STARTED (пропущенный обязательный барьер)
RUN_CARD_STATUS_AFTER:  HONEST_FAIL (см. VERDICT) — требует патч-цикла и re-run

============================================================
B.1 СТАТУС СИМУЛЯЦИИ
============================================================
SIMULATION_ID: ZWSP_TIER2_2026-07-13
SIMULATION_STATUS: LIVE_SELF_RUN (не внешнее ревью — прогон на машине автора
  через настоящий движок msl_mip_runtime.analyze; регистратор через
  msl_mip_runtime.scan_uncarded_invisibles)
REVIEWER: LIVE_SELF_RUN (machine), не модель-ревьюер
SIMULATION_GATE_TIER: TIER_2 (знак ZONE_2 — контекст выбирает субстрат;
  соответствует SIMULATION_GATE_TIER: TIER_2 в карточке)
FORMULAS:
  SIMULATION_RUN ≠ VALIDATION
  MEASURE_ONLY ≠ FIX (эта симуляция только МЕРЯЕТ; чинить — по карте провалов)
  ATTACK_CAUGHT = «человеку дан верный сигнал», не «поймал/заблокировал»
  FALSE_ALARM   = «система соврала человеку, подорвала доверие к HOLD»
  МЕТРИКА — ВЕРНОСТЬ СОВЕТА, не бинарное поймал/пропустил

============================================================
B.2 ВХОДНЫЕ ДАННЫЕ / PARSER_SCOPE
============================================================
SOURCE_CARDS_USED (полные файлы, не snapshot):
  - SIGN_CORE_CARD_ZERO_WIDTH_SPACE_U200B_GEN3_v0_3_RU.md
  - SIGN_CORE_CARD_FULLWIDTH_SOLIDUS_UFF0F_GEN3_v0_3_RU.md  (маска ／, для ZWSP+маска)
PARSER_SCOPE: загружены ТОЛЬКО ZWSP + маска ／ — это минимальный набор, при
  котором ось «отношение» ZWSP жива, и он не конфликтует с матчерами других
  знаков (@, ., ☠). Заявлено явно: другие карточки в этот прогон не грузились,
  чтобы вердикт по ZWSP не смешивался с их вердиктами.
TLD_STATE: HERMETIC, закреплённый набор {com,org,net,ru,io,dev,xn--p1ai}.
BATTERY: 33 живых входа, три класса (ATAKA / МИРНОЕ / НЕЗНАКОМОЕ) + отдельный
  зонд границ регистратора (14 кодпоинтов).

RULE_REMINDER: DIFFERENTIATION_CHECK_MANDATORY — один знак (ZWSP) прогнан в
  N контекстах; если бы результат был идентичен во всех — авто ARCHITECTURE_BUG.
  Результат см. ниже (DIFFERENTIATION_CHECK: YES, но с оговоркой F2).

============================================================
B.3 БАТАРЕЯ — СЫРОЙ ИЗМЕРЕННЫЙ ВЫВОД
(CTX/ZRISK — вердикт ребра ZWSP BOUNDARY_DISRUPTOR; VERDICT — effective_action
 всего движка; WITNESS — записи регистратора; CASE — прошёл ли кейс критерий
 своего класса)
============================================================
ID   CLASS   INPUT (codepoints)                           CTX              ZRISK  VERDICT              WITNESS   CASE
A01  ATTACK  goog<U+200B>le.com                           HOST             HIGH   hold_pending_review  -         PASS
A02  ATTACK  g<U+043E>og<U+200B>le.com                    HOST             HIGH   hold_pending_review  -         PASS
A03  ATTACK  goog<U+200B><U+FF0F>le.com                   HOST             HIGH   hold_pending_review  -         PASS
A04  ATTACK  google<U+200B>.com                           HOST             HIGH   hold_pending_review  -         PASS
A05  ATTACK  https://example.com/ad<U+200B>min            PATH             MEDIUM queue_for_review     -         PASS
A06  ATTACK  user<U+200B>name@example.com                 EMAIL            MEDIUM queue_for_review     -         PASS
A07  ATTACK  admin@exam<U+200B>ple.com                    EMAIL            MEDIUM queue_for_review     -         PASS
A08  ATTACK  bad<U+200B>word                              BYTE_EXACT_TOKEN MEDIUM queue_for_review     -         PASS
A09  ATTACK  user<U+200B>name                             BYTE_EXACT_TOKEN MEDIUM queue_for_review     -         PASS
A10  ATTACK  g<U+200B>o<U+200B>o<U+200B>g<U+200B>le.com   HOST             HIGH   hold_pending_review  -         PASS
A11  ATTACK  <U+200B>google.com                           HOST             HIGH   hold_pending_review  -         PASS
A12  ATTACK  google.com<U+200B>                           HOST             HIGH   hold_pending_review  -         PASS
A13  ATTACK  import o<U+200B>s                            BYTE_EXACT_TOKEN MEDIUM queue_for_review     -         PASS
P01  PEACE   東京<U+200B>都では                                BYTE_EXACT_TOKEN MEDIUM queue_for_review     -         FAIL(soft)
P02  PEACE   สวัส<U+200B>ดี                               FREE_TEXT        NONE   pass                 -         PASS
P03  PEACE   the word<U+200B> ends here                   BYTE_EXACT_TOKEN MEDIUM queue_for_review     -         FAIL(soft)
P04  PEACE   https://example.com/docs/very<U+200B>long    PATH             MEDIUM queue_for_review     -         FAIL(soft)
P05  PEACE   release v1.2<U+200B>.3 shipped               FREE_TEXT        NONE   pass                 -         PASS
P06  PEACE   ZWSP is U+200B                               -                -      pass                 -         PASS
R8a  PEACE   docs.example.com/guide/very-long<U+200B>-sec HOST             HIGH   hold_pending_review  -         FAIL(HARD)
R8b  PEACE   api.github.com/repos/user/very<U+200B>long   HOST             HIGH   hold_pending_review  -         FAIL(HARD)
R8c  PEACE   cdn.example.org/assets/js/main<U+200B>.min   HOST             HIGH   hold_pending_review  -         FAIL(HARD)
R8d  PEACE   example.com/a/b/c/d<U+200B>e                 HOST             HIGH   hold_pending_review  -         FAIL(HARD)
U01  UNKNOWN goog<U+2062>le.com                           -                -      pass                 U+2062    PASS
U02  UNKNOWN goog<U+2063>le.com                           -                -      pass                 U+2063    PASS
U03  UNKNOWN <U+FEFF>google.com                           -                -      pass                 U+FEFF    PASS
U04  UNKNOWN goog<U+2060>le.com                           -                -      pass                 U+2060    PASS
U05  UNKNOWN 👨<U+200D>👩<U+200D>👧                          -                -      pass                 U+200D×2  PASS
U06  UNKNOWN می<U+200C><U+200C>روم                        -                -      pass                 U+200C×2  PASS
U07  UNKNOWN abc<U+202E>def                               -                -      pass                 U+202E    PASS
U08  UNKNOWN a<U+FE0F>b                                   -                -      pass                 U+FE0F    PASS
U09  UNKNOWN abc<U+E0041>def                              -                -      pass                 U+E0041   PASS
U10  UNKNOWN go<U+200B>og<U+2062>le                       FREE_TEXT        NONE   pass                 U+2062    PASS

------------------------------------------------------------
B.3b ЗОНД ГРАНИЦ РЕГИСТРАТОРА (ловит / молча пропускает)
------------------------------------------------------------
U+00A0 Zs  no   NO-BREAK SPACE            <- молча пропущен
U+2007 Zs  no   FIGURE SPACE             <- молча пропущен
U+202F Zs  no   NARROW NBSP              <- молча пропущен
U+3000 Zs  no   IDEOGRAPHIC SPACE        <- молча пропущен
U+2028 Zl  no   LINE SEPARATOR           <- молча пропущен
U+2029 Zp  no   PARAGRAPH SEPARATOR      <- молча пропущен
U+2800 So  no   BRAILLE PATTERN BLANK    <- молча пропущен (рендерится пусто!)
U+00AD Cf  YES  SOFT HYPHEN
U+180E Cf  YES  MONGOLIAN VOWEL SEPARATOR
U+115F Lo  YES  HANGUL CHOSEONG FILLER
U+3164 Lo  YES  HANGUL FILLER
U+FEFF Cf  YES  BOM
U+061C Cf  YES  ARABIC LETTER MARK
U+200B Cf  no   ZERO WIDTH SPACE — КОРРЕКТНО исключён (карточка есть)

============================================================
B.4 ЧЕСТНЫЙ СЧЁТ (honest fail, по образцу черепа)
============================================================
  ATTACK  : 13/13 pass   (0 fail)  — ни одной пропущенной атаки
  PEACE   :  3/10 pass   (7 fail)  — 4 ЖЁСТКИХ ложняка + 3 мягких
  UNKNOWN : 10/10 pass   (0 fail)  — регистратор свидетельствует, вердикт не трогает
  --------------------------------------------------
  TOTAL   : 26/33

  ATTACK пропущено: НЕТ.
  PEACE жёсткий ложняк (HOLD на легитимном — подрыв доверия): R8a R8b R8c R8d.
  PEACE мягкий ложняк (QUEUE на легитимном — шум): P01 P03 P04.
  R8-класс ложный HOST/HIGH: 4 из 4 (100% — СИСТЕМАТИЧНО, не случайно).
  UNKNOWN регистратор молча пропустил: НЕТ (в пределах Cf∪bidi∪default-ignorable);
    НО за пределами предиката молча пропускает Zs/Zl/Zp/So (см. B.3b, F5).

DIFFERENTIATION_CHECK: YES — результат РАЗЛИЧАЕТСЯ по контекстам
  (HOST/HIGH vs EMAIL/MEDIUM vs BYTE_EXACT_TOKEN/MEDIUM vs FREE_TEXT/NONE vs
  PATH/MEDIUM), значит это НЕ «одинаково везде» = НЕ ARCHITECTURE_BUG.
  ОГОВОРКА: различение CJK vs тайского (P01 vs P02) НЕ принципиальное, а
  случайное — см. F2.

============================================================
B.5 НАХОДКИ (классификация по шаблону; FINDING_STATUS/BASIS обязательны)
============================================================

F1 — CONTEXT_CLASSIFIER_FALSE_POSITIVE (ЖЁСТКИЙ, подрыв доверия) [HEADLINE]
  ЧТО: schemeless-домен + ZWSP глубоко в ПУТИ → ложно HOST/HIGH/HOLD.
    R8a-R8d: 4 из 4 вариантов дали ложный HOLD. Систематично.
  FINDING_STATUS: VERIFIED
  FINDING_BASIS:
    METHOD: живой прогон msl_mip_runtime.analyze на 4 входах R8a-d.
    TARGET: sequence_engine._detect_context_at, ветка «маска внутри домена»
      (_domain_prefix терпит хвост-путь у left_part+right_part).
    OBSERVED: docs.example.com/guide/very-long<ZWSP>-section → CTX=HOST,
      ZRISK=HIGH, VERDICT=hold_pending_review, хотя ZWSP в пути, не в хосте.
    EXPECTED: PATH/MEDIUM/queue (как тот же вход СО СХЕМОЙ — P04).
  СВЯЗЬ: это уже заведённый OQ5 (NEXT_SESSION_FIX). Симуляция ДОКАЗАЛА, что
    это не единичный R8, а СИСТЕМАТИЧЕСКИЙ класс (100% R8-вариантов).
  РАМКА: для системы ОПОВЕЩЕНИЯ это худший вид провала — HOLD на честном URL
    учит человека не доверять HOLD.

F2 — CARD_PROMISE_VS_DETECTOR_GAP (SAFE_CASE_002 не держится на живом вводе)
  ЧТО: карточка SAFE_CASE_002 обещает CJK/тайскую ZWSP-сегментацию как
    RISK: NONE. Живьём CJK «東京<ZWSP>都では» → BYTE_EXACT_TOKEN/MEDIUM/queue.
    Тайский «สวัส<ZWSP>ดี» проходит (NONE) — но СЛУЧАЙНО.
  FINDING_STATUS: VERIFIED
  FINDING_BASIS:
    METHOD: живой прогон P01 (CJK) и P02 (тайский).
    TARGET: sequence_engine._is_byte_exact_token — требует все символы
      alnum/-/_; CJK-иероглифы isalnum()=True → байт-токен; тайские гласные-
      знаки (combining Mn, напр. U+0E31) isalnum()=False → тайский НЕ байт-
      токен → FREE_TEXT/NONE.
    OBSERVED: CJK→MEDIUM (FAIL обещания), тайский→NONE (проходит, но по
      несвязанной причине — combining mark, не по замыслу).
    EXPECTED (по карточке): оба → NONE.
  ВЫВОД: обещание карточки (NONE для CJK/тайской сегментации) на живом вводе
    держится ЧАСТИЧНО и по случайности. Различение CJK vs тайский — не
    принципиальное. НОВАЯ находка, ранее в карте не отражена.

F3 — TRACE_ONLY_NOTE (мягкий ложняк ПО ЗАМЫСЛУ, не дефект)
  ЧТО: P04 — отображаемый URL СО СХЕМОЙ, soft-wrap ZWSP в пути →
    PATH/MEDIUM/queue.
  FINDING_STATUS: VERIFIED (поведение), REJECTED (как дефект)
  FINDING_BASIS: карточка (раздел RUNTIME_REALITY + _SCOPE_RISK) СОЗНАТЕЛЬНО
    ставит PATH=MEDIUM: из строки нельзя отличить показанный перенос от
    машинного пути. Это заявленный компромисс, не сбой. По строгому критерию
    PEACE=PASS засчитан как мягкий ложняк, но чинить тут нечего без
    display-vs-machine сигнала, которого у движка нет.

F4 — TRACE_ONLY_NOTE (пограничный мягкий ложняк)
  ЧТО: P03 — одиночное слово с хвостовым ZWSP в прозе → BYTE_EXACT_TOKEN/
    MEDIUM/queue.
  FINDING_STATUS: VERIFIED
  FINDING_BASIS: живой прогон P03. ZWSP внутри/на хвосте alnum-слова
    действительно аномален; MEDIUM/queue («глянь») — защитимый совет, не
    жёсткий стоп. Оставлено как заметка, не как блокер.

F5 — REGISTRAR_COVERAGE_GAP (регистратор молча пропускает часть невидимого)
  ЧТО: регистратор ловит Cf ∪ bidi ∪ (курированный default-ignorable). За
    этим предикатом он МОЛЧА пропускает: Zs-пробелы нулевой/узкой видимости
    (NBSP U+00A0, FIGURE SPACE, NARROW NBSP, IDEOGRAPHIC SPACE U+3000),
    Zl/Zp (U+2028 LINE / U+2029 PARAGRAPH SEPARATOR) и U+2800 BRAILLE PATTERN
    BLANK (рендерится ПУСТО, известный приём сокрытия).
  FINDING_STATUS: VERIFIED
  FINDING_BASIS:
    METHOD: зонд B.3b — scan_uncarded_invisibles на 14 кодпоинтах.
    TARGET: msl_mip_runtime._invisible_reason (предикат Cf/bidi/DI-extra).
    OBSERVED: 7 из 14 «пробел/сепаратор/пусто» кодпоинтов → CAUGHT=no,
      запись witness НЕ создана.
    EXPECTED: для СВИДЕТЕЛЯ хотя бы U+2800 и NBSP-семейство стоит освещать
      (или явно объявить вне scope). Сейчас — тихий пропуск.
  РАМКА: свидетель, который молча не замечает пустой браль-символ, даёт
    человеку ложное чувство «здесь ничего невидимого нет».

============================================================
B.6 VERDICT
============================================================
SIMULATION_VERDICT: HONEST_FAIL — 26/33

  ПОЧЕМУ НЕ PASS: класс МИРНОЕ провалил 7/10, из них 4 ЖЁСТКИХ ложняка (HOLD
  на легитимном). Как у черепа первый прогон честно упал 5/14 — так и здесь:
  симуляция поймала дыру, которую конвейер (первый круг) пропустил. RUN_CARD
  переходит из NOT_STARTED в HONEST_FAIL, а не в PASS.

  ЧТО ДЕРЖИТСЯ:
    - ATTACK 13/13 — детектор не пропускает ни одной атаки во всех контекстах.
    - UNKNOWN 10/10 — регистратор свидетельствует и НЕ меняет вердикт
      (в пределах своего предиката).
    - Рамка «оповещение, не антивирус» держится: ни один вердикт ничего не
      режет/не удаляет, всё выносится человеку.

  ЧТО УПАЛО (карта провалов для патч-цикла — ЧИНИТЬ, не в этом заходе):
    F1  R8-класс, ложный HOST/HIGH, 4/4 систематично  [HARD, = OQ5 NEXT_SESSION_FIX]
    F2  SAFE_CASE_002 (CJK) не держится → ложный MEDIUM [SOFT, новая находка]
    F5  регистратор молча пропускает Zs/Zl/Zp/So       [WITNESS_GAP, новая находка]
    F3  P04 PATH=MEDIUM на показанном URL              [ПО ЗАМЫСЛУ — не чинить]
    F4  P03 хвостовой ZWSP в слове                     [пограничное — заметка]

CONVEYOR_EXIT_CONDITION: HONEST_FAIL → патч-цикл перед re-run TIER_2.
  DIFFERENTIATION достигнут (не ARCHITECTURE_BUG). Блокеров-архбагов нет —
  все провалы это ложные тревоги/пробелы покрытия, а не непроходимость pipeline.

NEXT_STEP: карта провалов (F1/F2/F5) уходит в патч-цикл следующим заходом;
  F1 сливается с уже заведённым OQ5. После патчей — повторный TIER_2 на этой
  же батарее (+ можно расширить), цель — закрыть 4 жёстких ложняка (R8) в ноль
  и решить по F2/F5 (чинить или явно объявить вне scope). НЕ ЧИНИМ ЗДЕСЬ —
  симуляция только измерила.

END_OF_SIMULATION_ARTIFACT
