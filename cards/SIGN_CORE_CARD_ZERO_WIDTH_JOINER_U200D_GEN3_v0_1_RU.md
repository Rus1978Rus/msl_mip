ЧАСТНЫЙ АВТОРСКИЙ ПРОЕКТ / COMMERCIAL USE PROHIBITED

CARD_UID: SIGN_CORE_CARD_ZERO_WIDTH_JOINER_U200D_GEN3_v0_1_RU
CODEPOINT: U+200D
VISIBLE_FORM: ‍
INSPECTION_LABEL: ⟦ZWJ U+200D⟧
  [поле-метка для чтения глазами: VISIBLE_FORM выше содержит ЛИТЕРАЛЬНЫЙ
   невидимый U+200D (рантайм сканит text по нему). Прочитать VISIBLE_FORM
   человек не может — INSPECTION_LABEL закрывает трещину пробы.]
UNICODE_NAME: ZERO WIDTH JOINER
ZONE: ZONE_2
DOCUMENT_STATUS: WORKING_DRAFT
LIFECYCLE_STATUS: WORKING_DRAFT
  [РЕАЛЬНАЯ позиция: карточка №2 поднадзорного класса невидимых, только что
   создана из образца. НЕ прошла ни STRUCTURAL_PREFLIGHT, ни конвейер — это
   честный WORKING_DRAFT. Содержание слоёв B/RISK/RELATIONS — на ИЗМЕРЕННОМ
   прогоне штатного analyze() (проба 2026-07-17, ENGINE-verified), не на догадке;
   но полной двуногой TIER_2-батареи (как у ZWSP) ещё нет — см. RUN_CARD_STATUS.]
VALIDATION_METHOD: SINGLE_LEG_ENGINE_PROBE (BY_CODE, штатный analyze; двуногой BY_SPEC нет)
CLASS_ROLE: CLASS_SPREAD_SPECIMEN
  [второй знак класса; даёт классу ПОВЕДЕНЧЕСКИЙ РАЗБРОС — ZWSP РВЁТ (break),
   ZWJ СКЛЕИВАЕТ (join, Join_Control=YES). Для будущего классового гарда нужна
   именно эта разница: невидимки не однородны.]
TEMPLATE_LINE: GEN3_v0_3
SOURCE_TEMPLATE: SIGN_CORE_CARD_ZERO_WIDTH_SPACE_U200B_GEN3_v0_3_RU (образец-эталон метода)
AUTHOR: Руслан Малявский
CREATED_AT: 2026-07-17
VERSION: v0_1
AUTHOR_DECISION_REFERENCE: foundation_layer/AUTHOR_DECISION_20260712_INVISIBLE_SIGNS_D-INV-1_2_3.md
AUTHOR_DECISION_REFERENCE_CLASS: foundation_layer/AUTHOR_DECISION_20260716_D-NEIGHBORS-BORDER-138.md
  (ZWJ ∈ поднадзорный класс 138 = Cf∧Default_Ignorable; один из 5 образцов карточки ZWSP)
RUN_CARD_REFERENCE: scratchpad-проба 2026-07-17 (zwj_context_probe.py / zwj_probe2.py) —
  ЭФЕМЕРНАЯ; персистентный артефакт будет при постройке ZWJ-батареи.
RUN_CARD_STATUS: PROBE_DONE (штатный analyze, 11 кейсов: атаки ловятся, эмодзи чисты,
  персидское соединение = MAY_QUEUE честная граница). НЕ полная TIER_2-батарея — двуногой
  BY_SPEC+reconcile+mutation-adequacy для ZWJ ещё нет; не выдаётся за ARTIFACT.
BY_SPEC_STATUS: NOT_AVAILABLE (ноги BY_SPEC нет; двуногость/reconcile НЕ утверждаются)
PATH_TO_ARTIFACT:
  1. WORKING_DRAFT — ДОСТИГНУТО (эта карточка, на измеренной пробе).
  2. STRUCTURAL_PREFLIGHT_PASS + CONVEYOR_REVIEW — PENDING.
  3. персистентная ZWJ-батарея (двуногая) + mutation-adequacy — PENDING.
  4. INVISIBLE_DEFAULT_IGNORABLE_GUARD (из >=3 знаков: ZWSP+ZWJ+BOM) — CLASS_FRONT.
  5. → WORKINGLY_CLOSED → ARTIFACT_CONFIRMED.
DISPLAY_NAME: невидимый соединитель нулевой ширины (zero width joiner)

============================================================
1. UNIVERSALITY / CONVEYOR_DISCIPLINE
============================================================
BOUND_TO_SPECIFIC_SIGN: YES
AFTER_USE_RESIDUE: FORBIDDEN
SIGN_DATA_IS_SESSION_ONLY: YES
STATUS_PROGRESSION_TRACKER:
  WORKING_DRAFT: YES (создана 2026-07-17 из образца; не прошла preflight/конвейер)
  STRUCTURAL_PREFLIGHT_PASS: PENDING
  CONVEYOR_REVIEW_PASS: PENDING
  WORKINGLY_CLOSED: PENDING
  SIMULATION_GATE_TIER: TIER_2 (ZONE_2)
  SIMULATION_GATE_PASSED: PROBE_ONLY (штатный analyze, не полная батарея)
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
    [ОТКРЫТЫЙ ФРОНТ: классовый гард невидимых. ZWJ — второй из >=3 знаков,
     нужных для его постройки без переобучения. Ссылка = маркер незакрытой
     классовой зависимости, НЕ дефект этой карточки.]
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
VISIBLE_FORM: ‍  (литеральный U+200D; см. INSPECTION_LABEL выше)
LOOKS_SIMILAR_IS_NOT_SAME_SIGN: NO
  [знак невидим — «похожесть» неприменима; отношения ниже строятся НЕ на
   визуальном сходстве, а на разрыве границы / классе фильтра / отсутствии]
RAW_SIGN_INPUT_STATUS: DATA_ONLY
BASE_MODE: DATA_ONLY_INVISIBLE_CONTROL
BASE_MODE_FORMULA: ZWJ_FORM ≠ EFFECT
SIGN_CATEGORY:
  - format_control (Unicode Cf)
  - invisible / zero-advance-width
  - default_ignorable_code_point
  - join_control (Join_Control=YES — ОТЛИЧИЕ от ZWSP, у которого NO)
WHAT_THIS_SIGN_IS_NOT:
  1. NOT_SPACE (U+0020 — имеет ширину и рендерится)
  2. NOT_A_CANON_IT_MIMICS (не изображает никакой видимый знак)
  3. NOT_REMOVABLE_BY_NFC_NFD_NFKC_NFKD (переживает всю нормализацию)
  4. NOT_A_VISIBLE_GLYPH (нулевая ширина, читателю не виден)
  5. NOT_A_BREAK_OPPORTUNITY (это ZWSP U+200B — ПРОТИВОПОЛОЖНАЯ функция; ZWJ СКЛЕИВАЕТ)
  6. NOT_SEMANTIC_CONTENT сам по себе (управляет соединением соседей, не несёт текст)
  7. NOT_A_NON_JOINER (это ZWNJ U+200C — ПОДАВЛЯЕТ соединение; ZWJ его ТРЕБУЕТ)
  8. NOT_A_WORD_JOINER_OR_BOM (U+2060 запрещает разрыв, U+FEFF — маркер BOM; иные функции)
  9. NOT_SAFE_TO_DELETE (несёт смысл: эмодзи-секвенции, арабское/индийское соединение)
  10. NOT_AN_AUTHORITY_OR_EXECUTION_BEARER
BASE_FORMULAS:
  ZWJ_FORM ≠ EFFECT
  ZWJ_FORM ≠ SPACE
  INVISIBLE ≠ ABSENT
  ZWJ_FORM ≠ CANON
  NFKC_SURVIVAL ≠ LEGITIMACY
  JOIN_CONTROL ≠ SAFE_TO_DELETE
  ZWJ ≠ AUTHORITY
  PRESENCE_IN_TOKEN ≠ TOKEN_STRUCTURE
  ZWJ_FORM ≠ VISUAL_MIMICRY
  ZWJ_JOINING ≠ WORD_BOUNDARY_MEANING

============================================================
5. SEMANTIC_EPOCH_TRACKER  (ZONE_2)
SEMANTIC_EPOCH_TRACKER_LOCK: REVIEWABLE
============================================================
EPOCH_TRACKER: CONTEXT_GATE_REQUIRED
APPLICABILITY: APPLICABLE
REASON: у знака ТРИ устойчивых substrate: письменный (соединение форм в арабском/
  индийских письменностях), эмодзи (композиция секвенций), машинный (диверсия
  точного совпадения — как у ZWSP).
CAPTURE_HISTORY:
  EPOCH_1:
    DATE_RANGE: ~1993 (Unicode 1.1) — настоящее время
    SUBSTRATE: письменность с соединением (арабское, индийские шрифты)
    FUNCTION: ТРЕБОВАНИЕ соединённой формы там, где иначе её бы не было
      (cursive joining, Join_Control)
    EVIDENCE: Unicode Standard, UAX#31/UAX#44 (Join_Control)
    STATUS: ACTIVE_IN_SCRIPT
  EPOCH_2:
    DATE_RANGE: ~2015 (эмодзи ZWJ-секвенции) — настоящее время
    SUBSTRATE: эмодзи-композиция (семья 👨‍👩‍👧, профессии, флаги)
    FUNCTION: склейка нескольких эмодзи в один составной глиф
    EVIDENCE: Unicode Emoji (UTS#51 ZWJ sequences)
    STATUS: ACTIVE_IN_TYPOGRAPHY
  EPOCH_3:
    DATE_RANGE: ~2000-е — настоящее время (эпоха фильтр-эвазии)
    SUBSTRATE: латинские машинные строки (домены, идентификаторы, код)
    FUNCTION: невидимая ДИВЕРСИЯ точного совпадения — разрыв токена/домена
      (латиница НЕ соединяется, поэтому ZWJ там = чистая вставка-диверсия)
    EVIDENCE: практика фильтр-эвазии; проба детектора 2026-07-17
    STATUS: ACTIVE_ATTACK
ACTIVE_EPOCH:
  STATUS: CONTEXT_GATE_REQUIRED
  PRIMARY_ACTIVE_EPOCH: NONE_GLOBAL
LAYER_ANOMALY:
  ABSENT_PHYSICAL_LAYER: YES (цифровой генезис; управляющий символ; глифа
    не было НИКОГДА — только эффект на соседей)
  NOTE: чистый цифровой контроль; в письменности проявляется ЧЕРЕЗ соседей, сам глифа не имеет
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
    INPUT: эмодзи-секвенция 👨‍👩‍👧 (семья через ZWJ)
    CONTEXT: свободный текст / эмодзи
    EXPECTED: INFO
    RISK: NONE
    GUARD: ZWJ_JOINING ≠ WORD_BOUNDARY_MEANING
    SEMANTIC_STATUS: LEGITIMATE_USE
    RUNTIME_VERIFIED: YES [проба 2026-07-17: эмодзи-позиции → FREE_TEXT → NONE.
      FP на эмодзи НЕТ — детектор классифицирует их как свободный текст.]
  SAFE_CASE_002:
    INPUT: арабское/персидское соединение می‍خواهم (ZWJ внутри слова)
    CONTEXT: письменность с соединением
    EXPECTED: INFO
    RISK: NONE
    GUARD: JOIN_CONTROL ≠ SAFE_TO_DELETE
    SEMANTIC_STATUS: LEGITIMATE_USE
    IMPLEMENTATION_STATUS: NOT_RECOGNIZED_WITHOUT_EXTERNAL_SCRIPT_CONTEXT
      [детектор НЕ различает арабское соединение (легитимно) от латинской вставки
       (диверсия) без внешнего script-контекста. Чинить кодом нельзя — эвристика
       «арабский=безопасно» откроет пропуск маски в АРАБСКОМ ДОМЕНЕ
       (gоog<ZWJ>le.伊朗 / арабский TLD). Честность карточки, не эвристика —
       зеркалит прецедент ZWSP↔CJK (конвейер 5/5).]
    CURRENT_RUNTIME_EXPECTATION: MAY_QUEUE
      [персидское слово с ZWJ схлопывается в BYTE_EXACT_TOKEN → детектор МОЖЕТ
       дать MEDIUM/QUEUE (проба 2026-07-17: می<ZWJ>خواهم → queue). Карточка НЕ
       обещает авто-PASS, которого код не даёт (claim=evidence). НЕ баг — честная
       граница до script-контекста (v0.5). Со знаком препинания рядом → FREE_TEXT/NONE.]
  SAFE_CASE_003:
    INPUT: «символ ZWJ имеет кодпоинт U+200D» (упоминание знака)
    CONTEXT: учебный/цитирование
    EXPECTED: INFO
    RISK: NONE
    GUARD: mention ≠ use
  SAFE_CASE_004:
    INPUT: намеренный ZWJ в строковом литерале кода (тест-фикстура эмодзи)
    CONTEXT: исходный код с явным намерением
    EXPECTED: INFO
    RISK: NONE
    GUARD: ZWJ_FORM ≠ EFFECT
RISK_CASES:
  [RISK_CASE_RUNTIME_STATUS: VERIFIED — кейс РЕАЛЬНО срабатывает прогоном
   (проба 2026-07-17); уровень RISK = то, что ВЫДАЁТ детектор. Контексты:
   HOST/EMAIL/BYTE_EXACT_TOKEN/HIDDEN_BOUNDARY_PADDING/FREE_TEXT; CODE/IDENTIFIER
   отдельно НЕ различаются — схлопываются в BYTE_EXACT_TOKEN (OQ4, как у ZWSP).]
  RISK_CASE_001:
    NAME: DOMAIN_LABEL_JOIN_EVASION
    INPUT: goog‍le.com (невидимая вставка в метку)
    CONTEXT: HOST
    RISK: HIGH
    RUNTIME_STATUS: VERIFIED [проба: goog<ZWJ>le.com → HOST / hold_pending_review]
    ATTACK: невидимая вставка рвёт точное совпадение — byte-exact блоклист
      промахивается мимо домена (латиница не соединяется — ZWJ здесь чистая диверсия)
    GUARD: ось «отношение», ребро BOUNDARY_DISRUPTOR, scope HOST
  RISK_CASE_002:
    NAME: HOST_TLD_JOIN_EVASION
    INPUT: paypal‍.com (ZWJ между меткой и TLD)
    CONTEXT: HOST
    RISK: HIGH
    RUNTIME_STATUS: VERIFIED [проба: paypal<ZWJ>.com → HOST / hold_pending_review]
    ATTACK: разрыв на границе метка/TLD
    GUARD: BOUNDARY_DISRUPTOR, scope HOST
  RISK_CASE_003:
    NAME: KEYWORD_SPLIT_EVASION
    INPUT: bad‍word (разрыв ключевого слова)
    CONTEXT: BYTE_EXACT_TOKEN
    RISK: MEDIUM
    RUNTIME_STATUS: VERIFIED [проба: bad<ZWJ>word → BYTE_EXACT_TOKEN / queue_for_review]
    ATTACK: разрыв ключевого слова/идентификатора обходит policy точного совпадения
    GUARD: BOUNDARY_DISRUPTOR, scope BYTE_EXACT_TOKEN
  RISK_CASE_004:
    NAME: EMAIL_LOCAL_SPLIT
    INPUT: us‍er@example.com (ZWJ в локальной части)
    CONTEXT: EMAIL
    RISK: MEDIUM
    RUNTIME_STATUS: VERIFIED [проба: us<ZWJ>er@example.com → EMAIL / queue_for_review]
    ATTACK: split локальной части email
    GUARD: BOUNDARY_DISRUPTOR, scope EMAIL
  RISK_CASE_005:
    NAME: LEADING_HIDDEN_PADDING
    INPUT: ‍paypal.com (ведущий ZWJ у целого домена)
    CONTEXT: HIDDEN_BOUNDARY_PADDING
    RISK: MEDIUM
    RUNTIME_STATUS: VERIFIED [проба: <ZWJ>paypal.com → HIDDEN_BOUNDARY_PADDING / queue]
    ATTACK: невидимый ведущий паддинг — не разрыв метки, но и не молчаливый PASS
    GUARD: BOUNDARY_DISRUPTOR, scope HIDDEN_BOUNDARY_PADDING
  RISK_CASE_006:
    NAME: INVISIBLE_CLASS_FILTER_BYPASS
    INPUT: ZWJ там, где грубый фильтр «разрешает zero-width» ожидая другой невидимый
    CONTEXT: BYTE_EXACT_TOKEN
    RISK: NONE
    RUNTIME_STATUS: PENDING
      [ЧЕСТНО: ребро INVISIBLE_CLASS_COLLISION — TAXONOMY_ONLY: поведение ВНЕШНЕГО
       грубого фильтра не наблюдаемо из входной строки, рантайм-проверки нет,
       риска не эмитит. Тип описан, за работающий контракт не выдаётся.]
    ATTACK: невидимый проходит по разрешению класса в грубом классификаторе
    GUARD: ребро INVISIBLE_CLASS_COLLISION (TARGET_KIND: CLASS)
CONFUSABLES:
  NOT_APPLICABLE:
    REASON: у невидимого знака НЕТ визуальных двойников — «спутать ПО ВИДУ» нельзя
      то, что не видно. Рантайм читает только SIGN_RELATIONS ниже.
    REVIEW_REQUIRED: YES
  FUNCTIONAL_NEIGHBORS:
    [ТЕРМИН (канон 2026-07-16): ZWJ — ОБРАЗЕЦ поднадзорного класса (Cf∧DI=138,
     D-NEIGHBORS-BORDER-138). Поле FUNCTIONAL_NEIGHBORS СТРУКТУРНОЕ (шаблон);
     справочный блок для человека, рантайм риск по нему НЕ считает.]
    NEIGHBOR_001:
      CODEPOINT: U+200B
      NAME: ZERO WIDTH SPACE (ZWSP)
      FUNCTION_DIFF: ZWSP даёт ВОЗМОЖНОСТЬ разрыва — ПРОТИВОПОЛОЖНОСТЬ склейке ZWJ
    NEIGHBOR_002:
      CODEPOINT: U+200C
      NAME: ZERO WIDTH NON-JOINER (ZWNJ)
      FUNCTION_DIFF: ZWNJ ПОДАВЛЯЕТ соединение; ZWJ его ТРЕБУЕТ — прямая пара-антипод
    NEIGHBOR_003:
      CODEPOINT: U+2060
      NAME: WORD JOINER (WJ)
      FUNCTION_DIFF: WJ запрещает РАЗРЫВ (не склеивает формы); Join_Control=NO
    NEIGHBOR_004:
      CODEPOINT: U+FEFF
      NAME: ZERO WIDTH NO-BREAK SPACE / BOM
      FUNCTION_DIFF: BOM — маркер порядка байт / no-break, не соединитель форм

SIGN_RELATIONS:
  [ИСТОЧНИК ИСТИНЫ ДЛЯ РАНТАЙМА. RELATION_TYPE_RUNTIME_STATUS — тип это КОНТРАКТ:
   поле говорит, что тип РЕАЛЬНО делает в рантайме (карта _RELATION_RUNTIME_ROLE).]
  RELATION_001:
    RELATION_TYPE: BOUNDARY_DISRUPTOR
    RELATION_TYPE_RUNTIME_STATUS: PRIMARY
      [рвёт границу точного совпадения (латиница не соединяется → ZWJ = чистая
       вставка-диверсия); ЕДИНСТВЕННЫЙ самостоятельный вердикт, VERIFIED пробой
       на goog<ZWJ>le.com → HOST/HIGH]
    TARGET_KIND: EMPTY_SEQUENCE
    CONTEXT_SCOPE: HOST, EMAIL, BYTE_EXACT_TOKEN, HIDDEN_BOUNDARY_PADDING, PATH, QUERY_VALUE, FRAGMENT, USERINFO
    VERIFICATION_STATUS: VERIFIED
    RUNTIME_EFFECT: RELATION_ONLY
  RELATION_002:
    RELATION_TYPE: INVISIBLE_CLASS_COLLISION
    RELATION_TYPE_RUNTIME_STATUS: TAXONOMY_ONLY
      [проходит по разрешению класса в ГРУБОМ внешнем фильтре; поведение фильтра
       НЕ наблюдаемо из входа → рантайм-проверки НЕТ, риска не эмитит. Честно.]
    TARGET_KIND: CLASS
    TARGET: zero-width-allowed (грубый классификатор, НЕ Unicode-функция)
    CONTEXT_SCOPE: BYTE_EXACT_TOKEN
    VERIFICATION_STATUS: CANDIDATE
    RUNTIME_EFFECT: RELATION_ONLY
  RELATION_003:
    RELATION_TYPE: ABSENCE_CONFUSABLE
    RELATION_TYPE_RUNTIME_STATUS: SUPPORTING_FACET
      [неотличим от отсутствия знака; ЭВИДЕНЦИЯ при первичном вердикте, НЕ
       самостоятельный второй HIGH. Риска не эмитит.]
    TARGET_KIND: EMPTY_SEQUENCE
    CONTEXT_SCOPE: HOST, EMAIL, BYTE_EXACT_TOKEN
    VERIFICATION_STATUS: VERIFIED
    RUNTIME_EFFECT: RELATION_ONLY

CONTRADICTION_GUARDS:
  CG1:
    TRIGGER: «ZWJ невидим, значит его нет»
    RESPONSE: INVISIBLE ≠ ABSENT
    RULE: невидимость — не отсутствие; знак присутствует в потоке байт
  CG2:
    TRIGGER: «ZWJ — это пробел/разрыв»
    RESPONSE: ZWJ СКЛЕИВАЕТ, НЕ разрывает и НЕ пробел
    RULE: Join_Control; противоположен ZWSP (break) и ZWNJ (non-join)
  CG3:
    TRIGGER: «нормализация уберёт ZWJ»
    RESPONSE: NFKC_SURVIVAL ≠ LEGITIMACY
    RULE: невидимые переживают NFC/NFD/NFKC/NFKD — остаются в строке
  CG4:
    TRIGGER: «RELATION_FOUND значит угроза»
    RESPONSE: RELATION_FOUND ≠ THREAT
    RULE: ребро — «рвёт границу в scope», риск выносит sequence-слой; контекст гейтит
  CG5:
    TRIGGER: «все невидимые можно слепо удалить»
    RESPONSE: JOIN_CONTROL ≠ SAFE_TO_DELETE
    RULE: удаление ZWJ ломает эмодзи-секвенции и арабское/индийское соединение
  CG6:
    TRIGGER: «нет видимого канона — нет отношения»
    RESPONSE: NO_CODEPOINT_CANON ≠ NO_RELATION
    RULE: отношение к границе/классу/пустоте есть без визуального канона

SEQUENCE_LAYER_BOUNDARY:
  SIGN_SAFE_ALONE ≠ SIGN_SAFE_IN_SEQUENCE: YES
  SEQUENCE_CANDIDATES: NOT_APPLICABLE
    [межзнаковое поведение (ZWJ между метками/буквами) оценивается через ось
     «отношение», как у ZWSP, а не через литеральный кандидат последовательности.
     ЛЕГИТИМНАЯ секвенция (эмодзи) — обратный случай: там ZWJ несёт смысл, детектор
     видит FREE_TEXT и риска не эмитит.]

PHAGO_ENTITY_MIMICRY:
  NOT_APPLICABLE
  PHAGO_REVIEW: INHERITED_FROM_METHOD (правило RULE_PHAGO_APPLICABILITY_v0_1; отдельного
    ZWJ-прогона фаго ещё нет — помечено честно, к конвейеру)
  PHAGO_BASIS: ZWJ СВОЕЙ ФУНКЦИЕЙ (вставка/склейка) НЕ создаёт ложную принадлежность
    к сущности. Как и у ZWSP, мимикрия при участии ZWJ эмерджентна на уровне
    ПОСЛЕДОВАТЕЛЬНОСТИ, не свойство одиночного знака. Тест: убрать ZWJ — целевая
    сущность (paypal, administrator) существует без него.
  PHAGO_INTERACTION_ROLE: ENABLER_ONLY
  PHAGO_APPLICABILITY_RULE: каноничный источник —
    foundation_layer/RULE_PHAGO_APPLICABILITY_v0_1.md (здесь НЕ дублируется).

============================================================
8. ADVERSARIAL_COVERAGE — RUN_CARD SEED
============================================================
MIN_TOTAL_VECTORS: 10
CATEGORY_A: FORM_MANIPULATION
  A1: ZWJ между каждой парой символов домена
  A2: несколько ZWJ подряд
CATEGORY_B: CONTEXT_INJECTION
  B1: ZWJ в host-части URL без схемы
  B2: ZWJ в email локальной части
CATEGORY_C: SEQUENCE_MANIPULATION
  C1: ZWJ между меткой и TLD (paypal‍.com)
  C2: ведущий/хвостовой ZWJ у целого домена (HIDDEN_BOUNDARY_PADDING)
CATEGORY_D: LEGITIMATE_LAYER_STRESS
  [УНИКАЛЬНО для ZWJ: сильный легитимный слой — проверить, что он НЕ даёт FP]
  D1: эмодзи-секвенция 👨‍👩‍👧 → должна быть чиста (VERIFIED: FREE_TEXT/NONE)
  D2: арабское/персидское соединение → честная граница MAY_QUEUE (VERIFIED)
CATEGORY_E: SEMANTIC_LAYER_MANIPULATION
  E1: подача ZWJ в эмодзи-обрамлении для сокрытия машинного риска
  E2: смена активной эпохи гейтом контекста (письменность → машинная)
ACTUAL_TOTAL_VECTORS: 10
COVERAGE_STATUS: PROBE_LEVEL
COVERAGE_SUFFICIENCY: PROBE_LEVEL_NOT_FULL_BATTERY
  [ПРОГНАНО: штатный analyze() на 11 кейсах (атаки VERIFIED, эмодзи чисты,
   персидское = MAY_QUEUE). НЕ двуногая батарея с reconcile+mutation-adequacy —
   та PENDING (см. PATH_TO_ARTIFACT). Не выдаётся за полное покрытие.]

============================================================
9. MUTATION_CHECK
============================================================
MUTATION_01:
  CLAIM: ZWJ даёт authority_effect
  EXPECTED: FAIL_FALSE_AUTHORITY
  RESULT: FAIL
MUTATION_02:
  CLAIM: ZWJ исполняется/запускает
  EXPECTED: FAIL_FALSE_EXECUTION
  RESULT: FAIL
MUTATION_03:
  CLAIM: ZWJ безопасно удаляется всегда
  EXPECTED: FAIL_FALSE_SAFE_DELETE (ломает эмодзи/арабское соединение)
  RESULT: FAIL
MUTATION_04:
  CLAIM: ZWJ эквивалентен ZWSP (разрыв)
  EXPECTED: FAIL_FALSE_EQUIVALENCE (ZWJ склеивает, Join_Control=YES)
  RESULT: FAIL
MUTATION_05:
  CLAIM: невидимость = отсутствие в потоке
  EXPECTED: FAIL_FALSE_ABSENCE
  RESULT: FAIL
MUTATION_CHECK_RUNTIME:
  STATUS: PENDING [engine-verified мутации кодпоинта/контекста/scope (как 6 у ZWSP)
    будут при постройке персистентной ZWJ-батареи; сейчас — семантические выше]

============================================================
10. KNOWN_OPEN_QUESTIONS
============================================================
OQ1:
  QUESTION: классовый INVISIBLE_DEFAULT_IGNORABLE_GUARD не построен
  STATUS: CLASS_FRONT_DEPENDENCY (как у ZWSP)
  BLOCKS_WORKINGLY_CLOSED: NO
  NOTE: ZWJ — 2-й из >=3 знаков для гарда. Разброс ZWSP(рвёт)/ZWJ(склеивает) —
    материал, ради которого карточка и пишется.
OQ2:
  QUESTION: детектор не различает арабское/индийское СОЕДИНЕНИЕ (легитимно) от
    латинской ВСТАВКИ (диверсия) — оба BYTE_EXACT_TOKEN. Script-контекст не читается.
  STATUS: OPEN (honest boundary; зеркалит ZWSP↔CJK)
  BLOCKS_WORKINGLY_CLOSED: NO
  NOTE: SAFE_CASE_002 = MAY_QUEUE. Эвристика «арабский=безопасно» откроет пропуск
    маски в арабском домене — чинить нельзя кодом, только честностью карточки.
OQ3:
  QUESTION: детектор _demask НЕ должен слепо удалять ZWJ (сломает эмодзи/персидское)
  STATUS: OPEN
  BLOCKS_WORKINGLY_CLOSED: NO
  NOTE: JOIN_CONTROL ≠ SAFE_TO_DELETE; для ZWJ в машинном ЛАТИНСКОМ домене demask
    реконструирует канон, но в письменности/эмодзи удаление исказит смысл. Граница
    ДЕТЕКТОРА, не карточки.
OQ4:
  QUESTION: детектор не различает CODE/IDENTIFIER/policy — схлопываются в BYTE_EXACT_TOKEN
  STATUS: OPEN (унаследовано, как у ZWSP)
  BLOCKS_WORKINGLY_CLOSED: NO
ALL_OPEN_QUESTIONS_CLOSED: NO

============================================================
11. PATCH_HISTORY
============================================================
PATCH_HISTORY:
  v0_1_PATCH_00: initial creation (2026-07-17). Вторая карточка невидимого класса,
    из образца ZWSP. Содержание слоёв — на ИЗМЕРЕННОЙ пробе штатного analyze()
    (zwj_context_probe / zwj_probe2, 2026-07-17): эмодзи→FREE_TEXT/NONE (FP нет),
    персидское→BYTE_EXACT_TOKEN→MAY_QUEUE (честная граница ZWSP↔CJK), атаки
    host/token/email/pad — VERIFIED. Персонализация: Join_Control=YES, EPOCH эмодзи,
    антипод ZWNJ. Одним пакетом с подключением в CARD_FILENAMES + обновлением
    oracle K1 (ZWJ теперь карточный → маршрут не witness).
PATCHES_APPLIED: 1
PATCHES_VERIFIED: PROBE (штатный analyze 11 кейсов; полная батарея — PENDING)

============================================================
12. LIMITATION_STATEMENT
============================================================
LIMITATION_STATEMENT:
  THIS_CARD IS A WORKING_DRAFT ARTIFACT (ранняя ступень; не WORKINGLY_CLOSED)
  NOT A FINAL_STANDARD / NOT A PARSER / NOT A RUNTIME / NOT A SECURITY_CERTIFICATE
  PROBE ≠ FULL_BATTERY (двуногой BY_SPEC+reconcile+mutation-adequacy для ZWJ ещё нет)
  DETECTOR_BOUNDARY_NOTE: JOIN_CONTROL ≠ SAFE_TO_DELETE — _demask детектора НЕ должен
    слепо удалять ZWJ: удаление ломает эмодзи-секвенции и арабское/индийское
    соединение. Для ZWJ в машинном ЛАТИНСКОМ контексте demask корректен. Граница
    ДЕТЕКТОРА, реализуется в детекторе, не в карточке.
  RUNTIME_REALITY (обещания=реальность, проба 2026-07-17): система РЕАЛЬНО производит
    по ZWJ: HOST→HIGH(hold); EMAIL→MEDIUM(queue); BYTE_EXACT_TOKEN→MEDIUM(queue);
    HIDDEN_BOUNDARY_PADDING→MEDIUM(queue); FREE_TEXT→NONE(pass). Эмодзи-секвенции →
    FREE_TEXT/NONE (легитимны, FP нет). Персидское/арабское соединение → BYTE_EXACT_
    TOKEN → MAY_QUEUE (честная граница, детектор без script-контекста не отличает от
    диверсии). Единственный самостоятельный вердикт — ребро BOUNDARY_DISRUPTOR
    (PRIMARY); INVISIBLE_CLASS_COLLISION (TAXONOMY_ONLY) и ABSENCE_CONFUSABLE
    (SUPPORTING_FACET) риска НЕ эмитят. Это НЕ антивирус: вердикт (PASS/QUEUE/HOLD) —
    РЕКОМЕНДАЦИЯ человеку, ничего не режется. Невидимый БЕЗ карточки — витнес
    UNVERIFIABLE.

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
