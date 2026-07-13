ЧАСТНЫЙ АВТОРСКИЙ ПРОЕКТ / COMMERCIAL USE PROHIBITED

CARD_UID: SIGN_CORE_CARD_ZERO_WIDTH_SPACE_U200B_GEN3_v0_3_RU
CODEPOINT: U+200B
VISIBLE_FORM: ​
INSPECTION_LABEL: ⟦ZWSP U+200B⟧
  [поле-метка для чтения глазами: VISIBLE_FORM выше содержит ЛИТЕРАЛЬНЫЙ
   невидимый U+200B (рантайм сканит text по нему). Прочитать VISIBLE_FORM
   человек не может — INSPECTION_LABEL закрывает трещину пробы.]
UNICODE_NAME: ZERO WIDTH SPACE
ZONE: ZONE_2
DOCUMENT_STATUS: WORKING_DRAFT
TEMPLATE_LINE: GEN3_v0_3
SOURCE_TEMPLATE: SIGN_CORE_CARD_TEMPLATE_GEN3_v0_3_R1_RU
AUTHOR: Руслан Малявский
CREATED_AT: 2026-07-12
VERSION: v0_1
AUTHOR_DECISION_REFERENCE: foundation_layer/AUTHOR_DECISION_20260712_INVISIBLE_SIGNS_D-INV-1_2_3.md
RUN_CARD_REFERENCE: PENDING
RUN_CARD_STATUS: NOT_STARTED
DISPLAY_NAME: невидимый пробел нулевой ширины (zero width space)

============================================================
1. UNIVERSALITY / CONVEYOR_DISCIPLINE
============================================================
BOUND_TO_SPECIFIC_SIGN: YES
AFTER_USE_RESIDUE: FORBIDDEN
SIGN_DATA_IS_SESSION_ONLY: YES
STATUS_PROGRESSION_TRACKER:
  WORKING_DRAFT: YES
  STRUCTURAL_PREFLIGHT_PASS: PENDING
  CONVEYOR_REVIEW_PASS: PENDING
  WORKINGLY_CLOSED: PENDING
  SIMULATION_GATE_TIER: TIER_2 (ZONE_2)
  SIMULATION_GATE_PASSED: PENDING
  ARTIFACT_CONFIRMED: PENDING

============================================================
3. REQUIRED_GENERAL_GUARDS
============================================================
REQUIRED_GENERAL_GUARDS:
  - SIGN_FALSE_EFFECT_MIMICRY_GUARD_v0_2A_RU
    GUARD_COMPATIBILITY: GUARD_COMPATIBILITY_RULE_GEN3
    GUARD_REVISION: v0_2A
    TEMPLATE_LINE_COMPATIBLE: GEN3_v0_3, GEN3_v0_3_R1
  - INVISIBLE_DEFAULT_IGNORABLE_GUARD: NOT_YET_BUILT
    [ОТКРЫТЫЙ ФРОНТ, честно: классовый гард невидимых (невидимость,
     неудаляемость NFKC, strip/flag/log) обещан ARCH_DECISION_INVISIBLE_
     SIGNS_HYBRID_C, но НЕ построен (DRAFT п.4.1). Класс-свойства ZWSP
     объявить пока негде. Ссылка стоит как маркер незакрытой зависимости.]
FAILURE_RESPONSE:
  REJECT_FALSE_EFFECT_MIMICRY
  TREAT_AS_DATA_ONLY
  NO_AUTHORITY_EFFECT
  NO_EXECUTION_EFFECT
  NO_TRUST_EFFECT
  NO_EXISTENCE_EFFECT

============================================================
4. SIGN IDENTITY — LAYER_A
LAYER_A_LOCK: PERMANENT
============================================================
VISIBLE_FORM: ​  (литеральный U+200B; см. INSPECTION_LABEL выше)
LOOKS_SIMILAR_IS_NOT_SAME_SIGN: NO
  [знак невидим — «похожесть» неприменима; отношения ниже строятся НЕ на
   визуальном сходстве, а на разрыве границы / классе фильтра / отсутствии]
RAW_SIGN_INPUT_STATUS: DATA_ONLY
BASE_MODE: DATA_ONLY_INVISIBLE_CONTROL
BASE_MODE_FORMULA: ZWSP_FORM ≠ EFFECT
SIGN_CATEGORY:
  - format_control (Unicode Cf)
  - invisible / zero-advance-width
  - default_ignorable_code_point
WHAT_THIS_SIGN_IS_NOT:
  1. NOT_SPACE (U+0020 — имеет ширину и рендерится)
  2. NOT_A_CANON_IT_MIMICS (не изображает никакой видимый знак)
  3. NOT_REMOVABLE_BY_NFC_NFD_NFKC_NFKD (переживает всю нормализацию)
  4. NOT_A_VISIBLE_GLYPH (нулевая ширина, читателю не виден)
  5. NOT_A_MANDATORY_LINE_BREAK (только ВОЗМОЖНОСТЬ переноса)
  6. NOT_SEMANTIC_CONTENT (читателю ничего не сообщает)
  7. NOT_A_JOINER (это ZWJ U+200D)
  8. NOT_A_NON_JOINER (это ZWNJ U+200C)
  9. NOT_A_WORD_JOINER_OR_BOM (U+2060 / U+FEFF)
  10. NOT_AN_AUTHORITY_OR_EXECUTION_BEARER
BASE_FORMULAS:
  ZWSP_FORM ≠ EFFECT
  ZWSP_FORM ≠ SPACE
  INVISIBLE ≠ ABSENT
  ZWSP_FORM ≠ CANON
  NFKC_SURVIVAL ≠ LEGITIMACY
  BREAK_OPPORTUNITY ≠ BREAK
  ZWSP ≠ AUTHORITY
  PRESENCE_IN_TOKEN ≠ TOKEN_STRUCTURE
  ZWSP_FORM ≠ VISUAL_MIMICRY
  ZWSP_PRESENCE ≠ WORD_BOUNDARY_MEANING

============================================================
5. SEMANTIC_EPOCH_TRACKER  (ZONE_2)
SEMANTIC_EPOCH_TRACKER_LOCK: REVIEWABLE
============================================================
EPOCH_TRACKER: CONTEXT_GATE_REQUIRED
APPLICABILITY: APPLICABLE
REASON: у знака два устойчивых substrate: типографический (перенос) и
  машинный (диверсия точного совпадения).
CAPTURE_HISTORY:
  EPOCH_1:
    DATE_RANGE: ~1991 (Unicode 1.0) — настоящее время
    SUBSTRATE: типографика / раскладка текста
    FUNCTION: невидимая ТОЧКА ПЕРЕНОСА строки без видимого пробела
      (длинные URL, сегментация в тайском/CJK без пробелов)
    EVIDENCE: Unicode Standard, UAX#14 (line breaking)
    STATUS: ACTIVE_IN_TYPOGRAPHY
  EPOCH_2:
    DATE_RANGE: ~2000-е — настоящее время (эпоха фильтр-эвазии)
    SUBSTRATE: латинские машинные строки (домены, идентификаторы, код)
    FUNCTION: невидимая ДИВЕРСИЯ точного совпадения — разрыв токена/
      домена/ключевого слова для обхода byte-exact фильтров
    EVIDENCE: практика фишинга/фильтр-эвазии; проба детектора 2026-07-12
    STATUS: ACTIVE_ATTACK
ACTIVE_EPOCH:
  STATUS: CONTEXT_GATE_REQUIRED
  PRIMARY_ACTIVE_EPOCH: NONE_GLOBAL
LAYER_ANOMALY:
  ABSENT_PHYSICAL_LAYER: YES (цифровой генезис; управляющий символ; глифа
    не было НИКОГДА — ни письменного, ни жестового)
  NOTE: чистый цифровой контроль без физического субстрата
STACK_RULES:
  Higher_epoch_suppresses_lower_in_modern_contexts: PARTIAL
  Lower_epoch_may_reactivate_in_historical_or_specialized_contexts: YES
  Context_gate_determines_active_epoch: REQUIRED
  Absent_layer_anomaly_must_be_flagged_for_integrator: YES

============================================================
6. EFFECT_FIELDS — LAYER_C
LAYER_C_LOCK: SESSION
============================================================
authority_effect: NONE
trust_effect: NONE
verification_effect: NONE
proof_effect: NONE
execution_effect: NONE
permission_effect: NONE
status_effect: NONE
role_assignment_effect: NONE
runtime_effect: NONE
existence_effect: NONE
EFFECT_FIELDS_ALL_NONE: YES
CLOSED_SCHEMA: YES

============================================================
7. LAYER_B
LAYER_B_LOCK: REVIEWABLE
============================================================
SAFE_CASES:
  SAFE_CASE_001:
    INPUT: длинный URL с ZWSP как точкой переноса в вёрстке
    CONTEXT: типографика
    EXPECTED: INFO
    RISK: NONE
    GUARD: BREAK_OPPORTUNITY ≠ BREAK
  SAFE_CASE_002:
    INPUT: тайский/CJK текст с ZWSP как сегментатором слов
    CONTEXT: типографика не-пробельных письменностей
    EXPECTED: INFO
    RISK: NONE
    GUARD: ZWSP_PRESENCE ≠ WORD_BOUNDARY_MEANING
  SAFE_CASE_003:
    INPUT: «символ ZWSP имеет кодпоинт U+200B» (упоминание знака)
    CONTEXT: учебный/цитирование
    EXPECTED: INFO
    RISK: NONE
    GUARD: mention ≠ use
  SAFE_CASE_004:
    INPUT: намеренный ZWSP в строковом литерале кода (тест-фикстура)
    CONTEXT: исходный код с явным намерением
    EXPECTED: INFO
    RISK: NONE
    GUARD: ZWSP_FORM ≠ EFFECT
  SAFE_CASE_005:
    INPUT: одиночный ZWSP в свободном тексте без структуры
    CONTEXT: свободный текст
    EXPECTED: INFO
    RISK: NONE
    GUARD: INVISIBLE ≠ ABSENT (но вне защищённого контекста — не угроза)
  SAFE_CASE_006:
    INPUT: ZWSP в HTML-разметке как soft-wrap подсказка
    CONTEXT: веб-вёрстка
    EXPECTED: INFO
    RISK: NONE
    GUARD: BREAK_OPPORTUNITY ≠ BREAK
RISK_CASES:
  [RISK_CASE_RUNTIME_STATUS (обещания=реальность): VERIFIED — кейс РЕАЛЬНО
   срабатывает прогоном (проба 2026-07-12); PENDING — систему СЕЙЧАС этот
   кейс НЕ производит (контекст даёт NONE, либо тип TAXONOMY_ONLY/
   SUPPORTING_FACET риска не эмитит). Уровень RISK ниже = то, что ВЫДАЁТ
   детектор, не то, что «хотелось бы». Детектор различает контексты
   HOST/EMAIL/PATH/BYTE_EXACT_TOKEN/FREE_TEXT; CODE и IDENTIFIER отдельно
   НЕ различает — см. KNOWN_OPEN OQ4.]
  RISK_CASE_001:
    NAME: DOMAIN_LABEL_BREAK_EVASION
    INPUT: gоog​le.com (невидимый разрыв метки)
    CONTEXT: HOST
    RISK: HIGH
    RUNTIME_STATUS: VERIFIED
    ATTACK: невидимый разрыв точного совпадения — byte-exact блоклист
      промахивается мимо домена
    GUARD: ось «отношение», ребро BOUNDARY_DISRUPTOR, scope HOST
  RISK_CASE_002:
    NAME: KEYWORD_SPLIT_EVASION
    INPUT: bad​word (разрыв ключевого слова)
    CONTEXT: BYTE_EXACT_TOKEN
    RISK: MEDIUM
    RUNTIME_STATUS: VERIFIED
      [РЕАЛЬНОСТЬ: детектор не различает CODE/IDENTIFIER/policy — все
       схлопываются в BYTE_EXACT_TOKEN → MEDIUM (не HIGH). Раньше карта
       обещала HIGH+CODE, чего система не производит; приведено к делу.
       Тонкое различение — KNOWN_OPEN OQ4.]
    ATTACK: разрыв ключевого слова обходит policy-фильтр точного совпадения
    GUARD: ребро BOUNDARY_DISRUPTOR, scope BYTE_EXACT_TOKEN
  RISK_CASE_003:
    NAME: ZWSP_PLUS_MASK_DOMAIN_BREAK
    INPUT: gоog​／le.com (ZWSP + маска рвут домен вместе)
    CONTEXT: HOST
    RISK: HIGH
    RUNTIME_STATUS: VERIFIED
    ATTACK: комбинация невидимого разрыва и полноширинной маски —
      ДОКАЗАНО запуском (проба 2026-07-12, известная открытая дыра)
    GUARD: BOUNDARY_DISRUPTOR + demask собирает домен → HOST
  RISK_CASE_004:
    NAME: INVISIBLE_PADDING_HIDDEN_TEXT
    INPUT: невидимый паддинг между символами для сокрытия/раздувания
    CONTEXT: FREE_TEXT
    RISK: NONE
    RUNTIME_STATUS: PENDING
      [ЧЕСТНО: в FREE_TEXT детектор выдаёт NONE, а ABSENCE_CONFUSABLE теперь
       SUPPORTING_FACET (самостоятельного риска не эмитит). Система СЕЙЧАС
       этот кейс НЕ поднимает — не выдаём за сработавший. Ждёт отдельного
       захода (детекция паддинга/раздувания вне защищённого контекста).]
    ATTACK: скрытый текст / невидимое раздувание длины
    GUARD: ребро ABSENCE_CONFUSABLE (эвиденция, не самостоятельный вердикт)
  RISK_CASE_005:
    NAME: IDENTIFIER_TOKEN_SPLIT
    INPUT: user​name как «другой» идентификатор
    CONTEXT: BYTE_EXACT_TOKEN
    RISK: MEDIUM
    RUNTIME_STATUS: VERIFIED
      [РЕАЛЬНОСТЬ: контекст детектора — BYTE_EXACT_TOKEN (IDENTIFIER/CODE у
       детектора нет); MEDIUM совпал с прогоном.]
    ATTACK: split идентификатора обходит сравнение имён
    GUARD: BOUNDARY_DISRUPTOR, scope BYTE_EXACT_TOKEN
  RISK_CASE_006:
    NAME: INVISIBLE_CLASS_FILTER_BYPASS
    INPUT: ZWSP там, где грубый фильтр «разрешает zero-width» ожидая ZWJ
    CONTEXT: BYTE_EXACT_TOKEN
    RISK: NONE
    RUNTIME_STATUS: PENDING
      [ЧЕСТНО: ребро INVISIBLE_CLASS_COLLISION — TAXONOMY_ONLY: поведение
       ВНЕШНЕГО грубого фильтра не наблюдаемо из входной строки, рантайм-
       проверки нет, риска не эмитит. Тип описан, но за работающий контракт
       не выдаётся. Ждёт отдельного захода по кейсам.]
    ATTACK: невидимый проходит по разрешению ДРУГОГО невидимого в грубом
      классификаторе (класс, не Unicode-функция)
    GUARD: ребро INVISIBLE_CLASS_COLLISION (TARGET_KIND: CLASS)
CONFUSABLES:
  NOT_APPLICABLE:
    REASON: у невидимого знака НЕТ визуальных двойников — «спутать ПО ВИДУ»
      нельзя то, что не видно. Классический механизм CONFUSABLES (визуальная
      мимикрия) к ZWSP неприменим. Рантайм читает только SIGN_RELATIONS ниже.
    REVIEW_REQUIRED: YES
  FUNCTIONAL_NEIGHBORS:
    [НЕ спутываемость ПО ВИДУ, а соседи по КЛАССУ невидимых. Разнесены сюда
     честно: это НЕ CONFUSABLES (различие ФУНКЦИИ, не вида). Справочный блок
     для человека; рантайм риск по ним НЕ считает — ключей CONFUSABLE_ здесь
     нет, парсер их не грузит, и это НАМЕРЕННО.]
    NEIGHBOR_001:
      CODEPOINT: U+200C
      NAME: ZERO WIDTH NON-JOINER (ZWNJ)
      FUNCTION_DIFF: ZWNJ подавляет соединение (персидская орфография);
        несёт смысл — слепое удаление исказит
    NEIGHBOR_002:
      CODEPOINT: U+200D
      NAME: ZERO WIDTH JOINER (ZWJ)
      FUNCTION_DIFF: ZWJ соединяет (эмодзи-секвенции); Join_Control=YES
        (у ZWSP NO); несёт смысл
    NEIGHBOR_003:
      CODEPOINT: U+2060
      NAME: WORD JOINER (WJ)
      FUNCTION_DIFF: WJ ЗАПРЕЩАЕТ разрыв — прямая противоположность ZWSP
    NEIGHBOR_004:
      CODEPOINT: U+FEFF
      NAME: ZERO WIDTH NO-BREAK SPACE / BOM
      FUNCTION_DIFF: BOM — маркер порядка байт / no-break
    NEIGHBOR_005:
      CODEPOINT: U+00AD
      NAME: SOFT HYPHEN (SHY)
      FUNCTION_DIFF: SHY — условный перенос с ВИДИМЫМ дефисом при разрыве

SIGN_RELATIONS:
  [ИСТОЧНИК ИСТИНЫ ДЛЯ РАНТАЙМА. Три ребра по D-INV-1 (минимум типов).
   Честно: без канона-кодпоинта — TARGET_KIND: EMPTY_SEQUENCE (D-INV-3),
   без выдуманного TARGET и без ложного VISUAL_MIMIC_OF.
   RELATION_TYPE_RUNTIME_STATUS (Level 2, находка S-03) — тип это КОНТРАКТ,
   не ярлык; поле говорит, что тип РЕАЛЬНО делает в рантайме, а не только
   описывает. Соответствует карте _RELATION_RUNTIME_ROLE в sequence_engine.]
  RELATION_001:
    RELATION_TYPE: BOUNDARY_DISRUPTOR
    RELATION_TYPE_RUNTIME_STATUS: PRIMARY
      [рвёт границу точного совпадения; ЕДИНСТВЕННЫЙ самостоятельный вердикт
       ZWSP — реальный контракт, VERIFIED прогоном на gоog<ZWSP>／le.com]
    TARGET_KIND: EMPTY_SEQUENCE
    CONTEXT_SCOPE: HOST, EMAIL, BYTE_EXACT_TOKEN, PATH
    VERIFICATION_STATUS: VERIFIED
    RUNTIME_EFFECT: RELATION_ONLY
  RELATION_002:
    RELATION_TYPE: INVISIBLE_CLASS_COLLISION
    RELATION_TYPE_RUNTIME_STATUS: TAXONOMY_ONLY
      [проходит по разрешению другого невидимого в ГРУБОМ внешнем фильтре;
       поведение того фильтра НЕ наблюдаемо из входной строки → рантайм-
       проверки пока НЕТ. Тип описан честно, но НЕ выдаётся за работающий
       контракт: риска не эмитит. Ждёт отдельного захода по кейсам.]
    TARGET_KIND: CLASS
    TARGET: zero-width-allowed (грубый классификатор, НЕ Unicode-функция)
    CONTEXT_SCOPE: BYTE_EXACT_TOKEN
    VERIFICATION_STATUS: CANDIDATE
    RUNTIME_EFFECT: RELATION_ONLY
  RELATION_003:
    RELATION_TYPE: ABSENCE_CONFUSABLE
    RELATION_TYPE_RUNTIME_STATUS: SUPPORTING_FACET
      [неотличим от отсутствия знака; ЭВИДЕНЦИЯ при первичном вердикте, НЕ
       самостоятельный второй HIGH на тот же знак в том же контексте (Z1,
       три ревьюера — дубль убран). Риска не эмитит.]
    TARGET_KIND: EMPTY_SEQUENCE
    CONTEXT_SCOPE: HOST, EMAIL, BYTE_EXACT_TOKEN
    VERIFICATION_STATUS: VERIFIED
    RUNTIME_EFFECT: RELATION_ONLY

CONTRADICTION_GUARDS:
  CG1:
    TRIGGER: «ZWSP невидим, значит его нет»
    RESPONSE: INVISIBLE ≠ ABSENT
    RULE: невидимость — не отсутствие; знак присутствует в потоке байт
  CG2:
    TRIGGER: «ZWSP — это пробел»
    RESPONSE: ZWSP_FORM ≠ SPACE
    RULE: нулевая ширина, не разделитель слов, другой кодпоинт
  CG3:
    TRIGGER: «нормализация уберёт ZWSP»
    RESPONSE: NFKC_SURVIVAL ≠ LEGITIMACY
    RULE: невидимые переживают NFC/NFD/NFKC/NFKD — остаются в строке
  CG4:
    TRIGGER: «RELATION_FOUND значит угроза»
    RESPONSE: RELATION_FOUND ≠ THREAT
    RULE: ребро — «разрывает границу в scope», риск выносит sequence-слой
  CG5:
    TRIGGER: «все невидимые можно слепо удалить»
    RESPONSE: DEFAULT_IGNORABLE ≠ SAFE_TO_DELETE
    RULE: ZWNJ/ZWJ несут смысл (орфография/эмодзи); удаление исказит
  CG6:
    TRIGGER: «нет видимого канона — нет отношения»
    RESPONSE: NO_CODEPOINT_CANON ≠ NO_RELATION
    RULE: отношение к границе/классу/пустоте есть без визуального канона

SEQUENCE_LAYER_BOUNDARY:
  SIGN_SAFE_ALONE ≠ SIGN_SAFE_IN_SEQUENCE: YES
  SEQUENCE_CANDIDATES: NOT_APPLICABLE
    [у ZWSP нет собственных литеральных SEQUENCE_CANDIDATES; межзнаковое
     поведение (ZWSP между метками домена) оценивается через ось
     «отношение» (active_relation_candidates + _assess_relation_risk),
     как у маски ／, а не через литеральный кандидат последовательности]

PHAGO_ENTITY_MIMICRY:
  NOT_APPLICABLE:
    REASON: ZWSP не выдаёт себя за СУЩНОСТЬ (лицо/бренд/систему) — он
      разрывает границу и прячется, механизм — диверсия, не олицетворение
    REVIEW_REQUIRED: YES

============================================================
8. ADVERSARIAL_COVERAGE — RUN_CARD SEED
============================================================
MIN_TOTAL_VECTORS: 12
CATEGORY_A: FORM_MANIPULATION
  A1: ZWSP между каждой парой символов домена
  A2: несколько ZWSP подряд для раздувания длины
CATEGORY_B: CONTEXT_INJECTION
  B1: ZWSP в host-части URL без схемы
  B2: ZWSP в email локальной части
CATEGORY_C: SEQUENCE_MANIPULATION
  C1: ZWSP + полноширинная маска ／ вместе (RISK_CASE_003)
  C2: ZWSP между меткой и TLD (gоogle​.com)
CATEGORY_D: SEMANTIC_MIMICRY
  [МЯГКОЕ ТРЕНИЕ: ZWSP не ИМИТИРУЕТ; векторы сформулированы как ДИВЕРСИЯ]
  D1: ZWSP проходит там, где фильтр «разрешает zero-width» ждёт ZWJ
  D2: ZWSP имитирует ОТСУТСТВИЕ (ABSENCE_CONFUSABLE) — паддинг «как чисто»
CATEGORY_E: PHAGO_ENTITY_MIMICRY
  E1: NOT_APPLICABLE (см. раздел 7; ZWSP не олицетворяет сущность)
  E2: NOT_APPLICABLE
CATEGORY_F: SEMANTIC_LAYER_MANIPULATION
  F1: смена активной эпохи гейтом контекста (типографика → машинная)
  F2: подача ZWSP в типографическом обрамлении для сокрытия машинного риска
ACTUAL_TOTAL_VECTORS: 12
COVERAGE_STATUS: UNVERIFIED
COVERAGE_SUFFICIENCY: UNVERIFIED
  [ЧЕСТНО: RUN_CARD_STATUS=NOT_STARTED — 12 векторов ВЫПИСАНЫ, но не
   ПРОГНАНЫ адверсариально. «Достаточность» нельзя объявить до прогона;
   SUFFICIENT здесь было бы обещанием без дела. Останется UNVERIFIED, пока
   RUN_CARD не отработает.]

============================================================
9. MUTATION_CHECK
============================================================
MUTATION_01:
  CLAIM: ZWSP даёт authority_effect
  EXPECTED: FAIL_FALSE_AUTHORITY
  RESULT: FAIL
MUTATION_02:
  CLAIM: ZWSP исполняется/запускает
  EXPECTED: FAIL_FALSE_EXECUTION
  RESULT: FAIL
MUTATION_03:
  CLAIM: ZWSP — доказательство/верификация
  EXPECTED: FAIL_FALSE_VERIFICATION
  RESULT: FAIL
MUTATION_04:
  CLAIM: ZWSP эквивалентен пробелу U+0020
  EXPECTED: FAIL_FALSE_EQUIVALENCE
  RESULT: FAIL
MUTATION_05:
  CLAIM: ZWSP безопасно удаляется всегда
  EXPECTED: FAIL_FALSE_SAFE_DELETE (ZWNJ/ZWJ несут смысл)
  RESULT: FAIL
MUTATION_06:
  CLAIM: невидимость = отсутствие в потоке
  EXPECTED: FAIL_FALSE_ABSENCE
  RESULT: FAIL

============================================================
10. KNOWN_OPEN_QUESTIONS
============================================================
OQ1:
  QUESTION: классовый INVISIBLE_DEFAULT_IGNORABLE_GUARD не построен —
    класс-свойства ZWSP объявить негде
  STATUS: OPEN
  BLOCKS_WORKINGLY_CLOSED: YES
  NOTE: DRAFT п.4.1; зависимость раздела 3 этой карточки
OQ2:
  QUESTION: D-GUARD-2 слеп к warned-ребру с ненулевым вердиктом
    (кандидат D-GUARD-5)
  STATUS: OPEN
  BLOCKS_WORKINGLY_CLOSED: NO
  NOTE: DRAFT п.4.2; граница сторожа, не карточки
OQ3:
  QUESTION: детектор _demask НЕ должен слепо удалять ZWNJ/ZWJ (сломает
    персидскую орфографию / эмодзи) — это ГРАНИЦА ДЕТЕКТОРА, не карточки
  STATUS: OPEN
  BLOCKS_WORKINGLY_CLOSED: NO
  NOTE: DEFAULT_IGNORABLE ≠ SAFE_TO_DELETE; для ZWSP demask корректен
    (ZWSP в машинном домене — разрыв, удаление реконструирует канон),
    но для ZWNJ/ZWJ демаск-удаление исказит смысл
OQ4:
  QUESTION: детектор НЕ различает CODE vs IDENTIFIER vs policy-фильтр — все
    схлопываются в один контекст BYTE_EXACT_TOKEN (MEDIUM). Тонкое различение
    (ключевое слово policy → HIGH против рядового идентификатора → MEDIUM)
    не выдумывается: детектор пока этого не умеет
  STATUS: OPEN
  BLOCKS_WORKINGLY_CLOSED: NO
  NOTE: RISK_CASE_002/005/006 приведены к реальному BYTE_EXACT_TOKEN; карта
    больше НЕ обещает контекст, которого система не производит
OQ5:
  QUESTION: ЛОЖНАЯ ТРЕВОГА в ОБЩЕМ детекторе (R8): schemeless-домен с маской
    в ПУТИ ложно классифицируется как HOST/HIGH вместо PATH/MEDIUM. Пример:
    docs.example.com/guide/very-long<ZWSP>-section → HOST/HIGH/HOLD, хотя ZWSP
    сидит в ПУТИ, не в хосте. Тот же вход СО СХЕМОЙ отрабатывает верно (PATH/
    MEDIUM). Корень: ветка «маска внутри домена» (_domain_prefix терпит
    хвост-путь); различающий сигнал — до-масочный кусок токена уже содержит
    / ? #.
  STATUS: OPEN
  BLOCKS_WORKINGLY_CLOSED: YES
  SEVERITY: HIGH
    [это СИСТЕМА ОПОВЕЩЕНИЯ: ложная тревога критична — подрывает доверие
     человека к HOLD. Не косметика — чинить, не откладывать бессрочно.]
  SCOPE: ОБЩИЙ детектор — задевает и маску ／ (U+FF0F), и все 55 кейсов
    bare-domain. Фикс требует полного ре-гейта 55 + регрессии на ／, поэтому
    отдельным пакетом, а не внутри этого коммита невидимых.
  RESOLUTION: NEXT_SESSION_FIX (НЕ «отложено навсегда» — чинится следующим
    заходом; заведено здесь, чтобы не потерялось до фикса)
ALL_OPEN_QUESTIONS_CLOSED: NO

============================================================
11. PATCH_HISTORY
============================================================
PATCH_HISTORY:
  v0_1_PATCH_01: initial creation (проба шаблона на ZWSP 2026-07-12 +
    AUTHOR_DECISION D-INV-1/2/3) — первая карточка невидимого знака;
    ось «отношение» расширена типами BOUNDARY_DISRUPTOR /
    INVISIBLE_CLASS_COLLISION / ABSENCE_CONFUSABLE, TARGET_KIND enum.
  v0_1_PATCH_02: FIX_FIRST по первому кругу (2026-07-12) — обещания=реальность.
    RISK_CASE контексты/уровни/RUNTIME_STATUS приведены к тому, что РЕАЛЬНО
    производит детектор (BYTE_EXACT_TOKEN/MEDIUM вместо выдуманного CODE/HIGH;
    004/006 честно PENDING). RELATION_TYPE_RUNTIME_STATUS (Level 2): PRIMARY/
    TAXONOMY_ONLY/SUPPORTING_FACET — убран дубль HIGH. CONFUSABLES →
    NOT_APPLICABLE + FUNCTIONAL_NEIGHBORS. COVERAGE → UNVERIFIED. OQ4
    (CODE/IDENTIFIER не различаются). RUNTIME_REALITY в LIMITATION.
    Реестратор невидимых-без-карточки — в рантайме, не в карте. Найденный
    ложняк R8 (schemeless путь → ложно HOST) заведён как OQ5 NEXT_SESSION_FIX
    (общий детектор, чинится отдельным заходом с ре-гейтом 55).
PATCHES_APPLIED: 2
PATCHES_VERIFIED: 0/2

============================================================
12. LIMITATION_STATEMENT
============================================================
LIMITATION_STATEMENT:
  THIS_CARD IS A WORKING_DRAFT ARTIFACT (до ARTIFACT_CONFIRMED)
  NOT A FINAL_STANDARD
  NOT A PARSER
  NOT A RUNTIME
  NOT A SECURITY_CERTIFICATE
  CONVEYOR_PASS ≠ VALIDATION
  RUN_CARD_RESULT ≠ FINAL_STATUS
  WORKINGLY_CLOSED ≠ ARTIFACT_CONFIRMED
  WORKINGLY_CLOSED ≠ LOCKED_WORKING_CORE
  DETECTOR_BOUNDARY_NOTE: DEFAULT_IGNORABLE ≠ SAFE_TO_DELETE — _demask
    детектора НЕ должен слепо удалять все невидимые: удаление ZWNJ/ZWJ
    исказит смысл (персидская орфография, эмодзи-ZWJ-секвенции), а не
    очистит. Для ZWSP в машинном контексте (домен/идентификатор) demask
    корректен — это граница ДЕТЕКТОРА, фиксируется здесь как ограничение,
    но реализуется в детекторе, не в карточке.
  RUNTIME_REALITY (обещания=реальность): система СЕЙЧАС РЕАЛЬНО производит по
    ZWSP: HOST→HIGH, EMAIL→MEDIUM, PATH→MEDIUM, BYTE_EXACT_TOKEN→MEDIUM,
    FREE_TEXT→NONE. Единственный самостоятельный вердикт даёт ребро
    BOUNDARY_DISRUPTOR (PRIMARY); INVISIBLE_CLASS_COLLISION (TAXONOMY_ONLY) и
    ABSENCE_CONFUSABLE (SUPPORTING_FACET) риска НЕ эмитят — второго
    независимого HIGH на тот же знак они не дают. PATH намеренно MEDIUM, не
    HIGH: из строки нельзя отличить мягкий перенос показанного URL от
    машинного пути. Это НЕ антивирус: вердикт (PASS/QUEUE/HOLD) — РЕКОМЕНДАЦИЯ
    человеку, не команда; ничего не режется и не удаляется, знак только
    выносится на глаза. Невидимый БЕЗ карточки не оценивается вовсе — его
    отдельно ОСВЕЩАЕТ реестратор INVISIBLE_UNCARDED_REGISTRAR статусом
    UNVERIFIABLE (не «опасно», не «безопасно» — «не могу проверить»).

============================================================
13. INTEGRATION_INTERFACE_STATUS
============================================================
INTEGRATION_INTERFACE_STATUS:
  STATUS: READY_PENDING_CONCRETE_INTEGRATOR
  ATTACHED_INTEGRATOR_UID: NONE_CURRENTLY_ATTACHED
  ACTIVE_MODULES_COUNT: 0
  RUNTIME_ATTACHMENT: NONE
  PERMANENT_BINDING: NO
  SESSION_ONLY_BINDING: YES
  AFTER_RUN_RESIDUE: FORBIDDEN

END_OF_CARD
