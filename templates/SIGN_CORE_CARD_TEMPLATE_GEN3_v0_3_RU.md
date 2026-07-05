ЧАСТНЫЙ АВТОРСКИЙ ПРОЕКТ / COMMERCIAL USE PROHIBITED

DOCUMENT_ID: SIGN_CORE_CARD_TEMPLATE_GEN3_v0_3_RU
DOCUMENT_TYPE: SIGN_CORE_CARD_TEMPLATE
TEMPLATE_LINE: GEN3_v0_3
DOCUMENT_STATUS: WORKINGLY_CLOSED
STATUS: WORKINGLY_CLOSED / NOT_LOCKED / NOT_RUNTIME / NOT_VALIDATOR / NOT_PRODUCTION
AUTHOR_DECISION_REFERENCE: AUTHOR_DECISION_20260621_002_SIGN_CORE_CARD_TEMPLATE_v0_3_WORKINGLY_CLOSED_RU
AUTHOR: Руслан Малявский
CREATED_AT: 2026-06-21
BASED_ON_RULESET: SIGN_CORE_CARD_CONVEYOR_RULES_GEN3_v0_3_RU
RULESET_STATUS: WORKINGLY_CLOSED
RULESET_AUTHOR_DECISION_REFERENCE: AUTHOR_DECISION_20260621_001_SIGN_CORE_CARD_CONVEYOR_RULES_v0_3_WORKINGLY_CLOSED_RU

PATCH_NOTE_TEMPLATE_v0_3_P1 (автор, 2026-06-23): в блоке CONFUSABLES
  (раздел 7) поле SIGN переименовано в VISIBLE_FORM. Шаблон в
  исходной версии использовал имя поля, запрещённое его же
  собственным NAMING_NORM (раздел 3 ruleset) — внутреннее
  противоречие между шаблоном и правилами, на которых он основан.
  Найдено при STRUCTURAL_PREFLIGHT_PASS первой заполненной карточки
  (DOT, U+002E). Исправление затрагивает только имя подполя внутри
  CONFUSABLES; структура и минимумы не изменены.

============================================================
КАК ПОЛЬЗОВАТЬСЯ ЭТИМ ШАБЛОНОМ
============================================================

Это ФОРМА, не готовая карточка. Каждое поле в угловых скобках
<...> должно быть заполнено перед тем, как карточка может пройти
STRUCTURAL_PREFLIGHT_PASS (первый шаг конвейера по правилам v0_3).

ОБЯЗАТЕЛЬНЫЕ поля помечены [ОБЯЗАТЕЛЬНО].
ОПЦИОНАЛЬНЫЕ поля помечены [ОПЦИОНАЛЬНО] — могут быть удалены из
  финальной карточки, если не применимы, но если поле оставлено —
  оно должно быть заполнено, не оставлено как заглушка.
Поля с указанием [МИНИМУМ N] требуют не менее N заполненных пунктов.

ЗАПРЕЩЕНО добавлять в карточку поля SIGN, UNICODE, GLYPH, SIGN_NAME,
SIGN_UNICODE, SIGN_GLYPH — это устаревшие имена (см. NAMING_NORM
в SIGN_CORE_CARD_CONVEYOR_RULES_GEN3_v0_3_RU, раздел 3).

ЗАПРЕЩЕНО использовать единый блок SCHEMA_LOCK — используются
только раздельные LAYER_*_LOCK (см. тот же раздел 3).

============================================================
0. UNIVERSALITY
============================================================

BOUND_TO_SPECIFIC_SIGN: YES
AFTER_USE_RESIDUE: FORBIDDEN
SIGN_DATA_IS_SESSION_ONLY: YES

============================================================
1. COMMON_CONVEYOR_DISCIPLINE
============================================================

CONVEYOR_DISCIPLINE_VERSION: v0_3
RUN_CARD_REQUIRED_BEFORE_LOCK: YES
RUN_CARD_TEMPLATE_REFERENCE: <ссылка на актуальный
  SIGN_CONVEYOR_RUN_CARD_TEMPLATE>
LOCKED_WORKING_CORE_SELF_ASSIGNMENT: FORBIDDEN
MODEL_FAMILY_DIVERSITY_REQUIRED: YES
ADVERSARIAL_EVIDENCE_REQUIRED: YES
MUTATION_CHECK_REQUIRED: YES
LIMITATION_STATEMENT_REQUIRED: YES
AFTER_RUN_RESIDUE: FORBIDDEN

GUIDED_TRAVERSAL_RISK_CHECK: MANDATORY
  # Гайд (из FO-100 TRAVERSAL_NOT_EQUAL_STRUCTURE): при обработке
  # находки ревьюера всегда проверяй — ссылается ли он на STRUCTURE
  # (проверяемый факт в файле/коде) или на TRAVERSAL (свою
  # интерпретацию / чужой отчёт). Не принимай TRAVERSAL за STRUCTURE.
  # Практика: grep/запуск реального артефакта ПЕРЕД принятием находки.
  # При расхождении ревьюеров по факту — разрешай первоисточником,
  # не голосованием большинства. Конвергенция ≠ доказательство.

STATUS_PROGRESSION_TRACKER (заполняется по ходу прохождения
  карточки через конвейер v0_3 — см. раздел 1 ruleset):
  WORKING_DRAFT: YES
  STRUCTURAL_PREFLIGHT_PASS: <PENDING / PASS / FAIL>
  CONVEYOR_REVIEW_PASS: <PENDING / PASS / FAIL>
  WORKINGLY_CLOSED: <PENDING / YES>
  SIMULATION_GATE_TIER: <TIER_1 / TIER_2 / TIER_3 — определяется по ZONE>
  SIMULATION_GATE_PASSED: <PENDING / YES>
  ARTIFACT_CONFIRMED: <PENDING / YES>

LIMITATION_STATEMENT (стандартный, не редактировать):
  CONVEYOR_PASS ≠ VALIDATION
  MODEL_CONSENSUS ≠ TRUTH
  INJECTION_TEST_PASS ≠ SECURITY_PROOF
  GUARDS_HOLD_FOR_TESTED_CASES ≠ FUTURE_GUARANTEE
  NO_ATTACK_FOUND ≠ NO_ATTACK_EXISTS
  LOCK_RECOMMENDATION ≠ LOCK
  RUN_CARD_RESULT ≠ FINAL_STATUS
  WORKINGLY_CLOSED ≠ ARTIFACT_CONFIRMED
  WORKINGLY_CLOSED ≠ LOCKED_WORKING_CORE

============================================================
2. META  [все поля этого раздела — ОБЯЗАТЕЛЬНО, если не
          указано иное]
============================================================

CARD_UID: <SIGN_CORE_CARD_<ИМЯ_ЗНАКА_ЗАГЛАВНЫМИ>_U<XXXX>_GEN3_v0_3_RU>
CODEPOINT: U+<XXXX>
VISIBLE_FORM: <видимый символ знака>
UNICODE_NAME: <официальное имя из стандарта Unicode>
ZONE: <ZONE_1 / ZONE_2 / ZONE_3 — выбрать одно, обосновать ниже
  в разделе SEMANTIC_EPOCH_TRACKER>
DOCUMENT_STATUS: WORKING_DRAFT
TEMPLATE_LINE: GEN3_v0_3
SOURCE_TEMPLATE: SIGN_CORE_CARD_TEMPLATE_GEN3_v0_3_RU
AUTHOR: <имя автора>
CREATED_AT: <YYYY-MM-DD>
VERSION: v0_1
AUTHOR_DECISION_REFERENCE: PENDING
RUN_CARD_REFERENCE: PENDING
RUN_CARD_STATUS: NOT_STARTED

[ОПЦИОНАЛЬНО — заполнить только если применимо]
RUN_CARD_DATE: <YYYY-MM-DD, только если RUN_CARD_STATUS содержит
  датированный результат>
PATCHED_AT: <YYYY-MM-DD, только если карта патчилась после CREATED_AT>
DISPLAY_NAME: <человекочитаемое имя, например "точка" для FULL STOP;
  заполнять, только если UNICODE_NAME недостаточно понятен без
  пояснения>

============================================================
3. REQUIRED_GENERAL_GUARDS  [ОБЯЗАТЕЛЬНО]
============================================================

TRACEABILITY_NOTE: этот раздел — расширение шаблона, унаследованное
  от общей дисциплины GUARD из карточек предыдущих поколений
  (DOT/AT/HASH/SKULL/SOLIDUS), а не прямое требование из
  REQUIRED_FIELDS_* в SIGN_CORE_CARD_CONVEYOR_RULES_GEN3_v0_3_RU.
  Сохраняется как обязательный, поскольку карточки знака должны
  оставаться совместимы с SIGN_FALSE_EFFECT_MIMICRY_GUARD и
  GUARD_COMPATIBILITY_RULE независимо от версии правил конвейера.
  Найдено и зафиксировано внешним ревью (GPT-5.5).

REQUIRED_GENERAL_GUARDS:
  - SIGN_FALSE_EFFECT_MIMICRY_GUARD_v0_2A_RU
    GUARD_COMPATIBILITY: <ссылка на актуальное правило совместимости>
    GUARD_REVISION: v0_2A
    TEMPLATE_LINE_COMPATIBLE: <список совместимых линий шаблона>

FAILURE_RESPONSE:
  REJECT_FALSE_EFFECT_MIMICRY
  TREAT_AS_DATA_ONLY
  NO_AUTHORITY_EFFECT
  NO_EXECUTION_EFFECT
  NO_TRUST_EFFECT
  NO_EXISTENCE_EFFECT

============================================================
4. SIGN IDENTITY — LAYER_A: STABLE CORE  [ОБЯЗАТЕЛЬНО]
LAYER_A_LOCK: PERMANENT
============================================================

VISIBLE_FORM: <видимый символ знака — повтор из META для
  самодостаточности раздела>
LOOKS_SIMILAR_IS_NOT_SAME_SIGN: <YES/NO>
RAW_SIGN_INPUT_STATUS: DATA_ONLY

BASE_MODE: <категориальное значение, например DATA_ONLY,
  DATA_ONLY_SEPARATOR — ОБЯЗАТЕЛЬНО как отдельное поле, не
  заменяется формулой ниже>
BASE_MODE_FORMULA: <ИМЯ_ЗНАКА>_FORM ≠ EFFECT

SIGN_CATEGORY:
  - <категория 1, например punctuation>
  - <категория 2>
  - <добавить по необходимости>

WHAT_THIS_SIGN_IS_NOT:  [МИНИМУМ 10 ПУНКТОВ]
  1. NOT_<...>
  2. NOT_<...>
  3. NOT_<...>
  4. NOT_<...>
  5. NOT_<...>
  6. NOT_<...>
  7. NOT_<...>
  8. NOT_<...>
  9. NOT_<...>
  10. NOT_<...>

BASE_FORMULAS:  [МИНИМУМ 10 ФОРМУЛ]
  <ИМЯ_ЗНАКА>_FORM ≠ <...>
  <ИМЯ_ЗНАКА>_FORM ≠ <...>
  (продолжить до минимум 10)

============================================================
5. SEMANTIC_EPOCH_TRACKER  [ОБЯЗАТЕЛЬНО — секция должна
   присутствовать независимо от ZONE, см. ruleset раздел 2]
SEMANTIC_EPOCH_TRACKER_LOCK: REVIEWABLE
============================================================

ЕСЛИ ZONE = ZONE_1:
  EPOCH_TRACKER: NOT_APPLICABLE
  NOTE: <обязательное объяснение — обычно: знак имеет несколько
    параллельных функций без культурной прецессии, это полисемия,
    не смена эпох>

ЕСЛИ ZONE = ZONE_2:
  EPOCH_TRACKER: CONTEXT_GATE_REQUIRED
  APPLICABILITY: <APPLICABLE / NOT_APPLICABLE>
  REASON: <почему знак имеет несколько устойчивых semantic mode
    в разных substrate>
  CAPTURE_HISTORY (если APPLICABLE):
    EPOCH_1:
      DATE_RANGE: <...>
      SUBSTRATE: <...>
      FUNCTION: <...>
      EVIDENCE: <ссылки на источники>
      STATUS: <...>
    (повторить для каждой эпохи/substrate)
  ACTIVE_EPOCH:
    STATUS: CONTEXT_GATE_REQUIRED
    PRIMARY_ACTIVE_EPOCH: NONE_GLOBAL

ЕСЛИ ZONE = ZONE_3:
  EPOCH_TRACKER: REQUIRED
  CAPTURE_HISTORY:  [МИНИМУМ 2 ЭПОХИ]
    EPOCH_1:
      NAME: <...>
      DATE_RANGE: <...>
      SUBSTRATE: <...>
      FUNCTION: <...>
      EVIDENCE: <...>
      STATUS: <DORMANT_IN_... / ACTIVE / SECONDARY_ACTIVE_...>
    EPOCH_2:
      (аналогично)
    (продолжить по необходимости)
  ACTIVE_EPOCH:
    <EPOCH_N>: <название функции>
  ACTIVE_EPOCH_TYPE: GLOBAL
  DOMINANT_SUBSTRATE: <...>
  DOMINANT_FUNCTION: <...>
  DORMANT_EPOCHS:
    <EPOCH_N>: <статус и условие реактивации>
  PRECESSION_ALERT:
    STATUS: <STABLE / DRIFTING>
    LAST_CHECK: <YYYY-MM-DD>
    NOTE: <наблюдения о тенденциях смены эпохи>

LAYER_ANOMALY (заполняется для всех ZONE):
  ABSENT_PHYSICAL_LAYER: <YES, с указанием уровня / NO>
  NOTE: <пояснение происхождения знака — письменный/жестовый/
    цифровой генезис>

STACK_RULES (заполняется для ZONE_2/ZONE_3):
  Higher_epoch_suppresses_lower_in_modern_contexts: <YES/NO/PARTIAL>
  Lower_epoch_may_reactivate_in_historical_or_specialized_contexts: <YES/NO>
  Context_gate_determines_active_epoch: <YES/NO/PARTIAL/REQUIRED>
  Absent_layer_anomaly_must_be_flagged_for_integrator: <YES/NO/NOT_APPLICABLE>

============================================================
6. EFFECT_FIELDS — LAYER_C: METHODOLOGICAL LAYER  [ОБЯЗАТЕЛЬНО]
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

NOTE: все 10 полей должны быть NONE для прохождения по умолчанию.
  Если для данного знака предполагается иное — это архитектурное
  решение высшего уровня, требующее отдельного AUTHOR_DECISION
  и пересмотра SPEC_FOUNDATION, не точечного заполнения карточки.

============================================================
7. SAFE / RISK / CONFUSABLES / GUARDS — LAYER_B: SEMI-STABLE LAYER
   [ОБЯЗАТЕЛЬНО]
LAYER_B_LOCK: REVIEWABLE
============================================================

SAFE_CASES:  [МИНИМУМ 6]
  SAFE_CASE_001:
    INPUT: <пример текста>
    CONTEXT: <тип контекста>
    EXPECTED: <ожидаемая обработка, например INFO>
    RISK: NONE
    GUARD: <ссылка на применимый BASE_FORMULA>
  (повторить минимум до SAFE_CASE_006)

RISK_CASES:  [МИНИМУМ 6]
  RISK_CASE_001:
    NAME: <короткое имя угрозы>
    INPUT: <пример текста>
    CONTEXT: <тип контекста>
    RISK: <NONE / LOW / MEDIUM / HIGH>
    ATTACK: <описание механизма>
    GUARD: <требуемая защитная мера/проверка>
  (повторить минимум до RISK_CASE_006)

CONFUSABLES:  [МИНИМУМ 5]
  CONFUSABLE_001:
    VISIBLE_FORM: <похожий символ>
    CODEPOINT: U+<XXXX>
    NAME: <официальное имя>
    RISK: <LOW / MEDIUM / HIGH>
    RULE: <ИМЯ_CONFUSABLE> ≠ <ИМЯ_ЗНАКА>
  (повторить минимум до CONFUSABLE_005)

CONTRADICTION_GUARDS:  [МИНИМУМ 6]
  CG1:
    TRIGGER: <ложное допущение, которое нужно отклонить>
    RESPONSE: <ИМЯ_ЗНАКА>_FORM ≠ <...>
    RULE: <человекочитаемое объяснение правила>
  (повторить минимум до CG6)

SEQUENCE_LAYER_BOUNDARY:  [ОБЯЗАТЕЛЬНО присутствие поля; может
  быть NOT_APPLICABLE с обоснованием]
  SIGN_SAFE_ALONE ≠ SIGN_SAFE_IN_SEQUENCE: <YES/NO>
  SEQUENCE_CANDIDATES (если применимо):
    SC1:
      SEQUENCE: <пример последовательности с этим знаком>
      NAME: <короткое имя>
      RISK_LEVEL: <NONE/LOW/MEDIUM/HIGH>
      POSSIBLE_CONTEXTS: <варианты>
      REQUIRES_SEQUENCE_INTEGRATOR: <YES/NO>
    (повторить по необходимости)
  ЕСЛИ NOT_APPLICABLE: <обязательное объяснение, почему знак не
    участвует в значимых последовательностях>

PHAGO_ENTITY_MIMICRY:  [ОБЯЗАТЕЛЬНО присутствие поля; может быть
  минимальным с явным NOTE, либо NOT_APPLICABLE с обоснованием]
  PE_001:
    INPUT: <пример>
    TYPE: <PHAGO_ENTITY_MIMICRY / SEMANTIC_AMBIGUITY (not PHAGO)>
    RISK: <уровень>
    NOTE: <пояснение>
  (добавить ещё, если применимо)

  ЛИБО, если знак не подвержен этому риску вообще:
  NOT_APPLICABLE:
    REASON: <почему для этого знака нет правдоподобного сценария
      PHAGO_ENTITY_MIMICRY>
    REVIEW_REQUIRED: YES (NOT_APPLICABLE по этому полю всегда
      проверяется отдельно на CONVEYOR_REVIEW_PASS — слишком легко
      ошибочно отмести реальный риск как несущественный)

============================================================
8. ADVERSARIAL_COVERAGE — RUN_CARD SEED  [ОБЯЗАТЕЛЬНО]
============================================================

MIN_TOTAL_VECTORS: 12 (6 категорий A-F, по 2 на категорию)
  ЕСЛИ CATEGORY_F = NOT_APPLICABLE (допустимо для ZONE_1, см. ниже):
    MIN_TOTAL_VECTORS: 10 (5 категорий A-E, по 2 на категорию)
  Это снижение применяется только при ZONE_1 с явно обоснованным
  NOT_APPLICABLE для CATEGORY_F — не автоматически для любого знака.

CATEGORY_A: FORM_MANIPULATION (2)
  A1: <вектор>
  A2: <вектор>

CATEGORY_B: CONTEXT_INJECTION (2)
  B1: <вектор>
  B2: <вектор>

CATEGORY_C: SEQUENCE_MANIPULATION (2)
  C1: <вектор>
  C2: <вектор>

CATEGORY_D: SEMANTIC_MIMICRY (2 минимум)
  D1: <вектор>
  D2: <вектор>

CATEGORY_E: PHAGO_ENTITY_MIMICRY (2)
  E1: <вектор>
  E2: <вектор>

CATEGORY_F: SEMANTIC_LAYER_MANIPULATION (2; для ZONE_1 может быть
  NOT_APPLICABLE с обоснованием — ZONE_1 не имеет dormant epochs)
  F1: <вектор>
  F2: <вектор>

ACTUAL_TOTAL_VECTORS: <число>
COVERAGE_STATUS: <SUFFICIENT (если ACTUAL ≥ MIN) / INSUFFICIENT>

============================================================
9. MUTATION_CHECK  [МИНИМУМ 6 МУТАЦИЙ]
============================================================

MUTATION_01:
  CLAIM: <ложное утверждение об эффекте знака>
  EXPECTED: FAIL_<тип_подмены>
  RESULT: <FAIL — должно совпадать с EXPECTED>
(повторить минимум до MUTATION_06)

============================================================
10. KNOWN_OPEN_QUESTIONS
============================================================

OQ1:
  QUESTION: <вопрос>
  STATUS: <CLOSED_AS_MONITORING_ITEM / CLOSED_AS_DELEGATED_TO_...
    / OPEN>
  BLOCKS_WORKINGLY_CLOSED: <YES/NO>
  NOTE: <пояснение>
(добавить по необходимости; если вопросов нет —
  ALL_OPEN_QUESTIONS_CLOSED: YES с пустым списком)

ALL_OPEN_QUESTIONS_CLOSED: <YES/NO>

============================================================
11. PATCH_HISTORY  [формат фиксирован правилами v0_3, раздел 4]
============================================================

PATCH_HISTORY:
  v0_1_PATCH_01: <короткое_имя_патча> (<источник_ревью>, <дата>) —
    <описание, что изменено и почему>
    [REASON: <если патч исправляет находку предыдущего ревью>]

PATCHES_APPLIED: <число>
PATCHES_VERIFIED: <число>/<число>

============================================================
12. LIMITATION_STATEMENT  [ОБЯЗАТЕЛЬНО, стандартный текст]
============================================================

LIMITATION_STATEMENT:
  THIS_CARD IS A WORKING_DRAFT ARTIFACT (до получения
    ARTIFACT_CONFIRMED)
  NOT A FINAL_STANDARD
  NOT A PARSER
  NOT A RUNTIME
  NOT A SECURITY_CERTIFICATE
  CONVEYOR_PASS ≠ VALIDATION
  RUN_CARD_RESULT ≠ FINAL_STATUS
  WORKINGLY_CLOSED ≠ ARTIFACT_CONFIRMED
  WORKINGLY_CLOSED ≠ LOCKED_WORKING_CORE

============================================================
13. INTEGRATION_INTERFACE_STATUS  [ОБЯЗАТЕЛЬНО]
============================================================

INTEGRATION_INTERFACE_STATUS:
  STATUS: READY_PENDING_CONCRETE_INTEGRATOR
  ATTACHED_INTEGRATOR_UID: NONE_CURRENTLY_ATTACHED
  ACTIVE_MODULES_COUNT: 0
  RUNTIME_ATTACHMENT: NONE
  PERMANENT_BINDING: NO
  SESSION_ONLY_BINDING: YES
  AFTER_RUN_RESIDUE: FORBIDDEN

============================================================
PREFLIGHT_FAILURE_TYPES  [ОПЦИОНАЛЬНОЕ РАСШИРЕНИЕ — не требуется
  буквальной формулировкой правил v0_3 (STRUCTURAL_PREFLIGHT_PASS
  определён как проверка присутствия REQUIRED_FIELDS, без
  требования формальной классификации), но рекомендуется для
  автоматизации и единообразия отчётов. Предложено внешним ревью
  (GPT-5.5). Использование этой классификации в отчёте о находках
  не обязательно для прохождения STRUCTURAL_PREFLIGHT_PASS, но
  облегчает будущую машинную проверку.]
============================================================

MISSING_REQUIRED_FIELD:
  обязательное поле отсутствует

PROHIBITED_FIELD_USED:
  использовано запрещённое legacy-поле как активное поле карточки
  (см. PROHIBITED_FIELD_CHECK_RULE ниже — проверка по точному
  имени поля, не по подстроке)

FIELD_ALIAS_DIVERGENCE:
  одно и то же понятие записано неканоническим именем поля

CARD_SCHEMA_DRIFT:
  структура карточки отклоняется от GEN3_v0_3 template

TEMPLATE_TO_TEMPLATE_INTERFACE_GAP:
  поле требуется downstream-шаблоном (MODULE_TEMPLATE,
  INTEGRATOR_TEMPLATE), но не определено текущим шаблоном карточки

MACHINE_READABILITY_BLOCKER:
  человек может понять карточку, но автоматический validator не
  может надёжно прочитать поле без ручной интерпретации

PLACEHOLDER_NOT_FILLED:
  в финальной карточке остался <...> placeholder

MINIMUM_COUNT_NOT_MET:
  не выполнен минимум по SAFE_CASES / RISK_CASES / CONFUSABLES /
  CONTRADICTION_GUARDS / MUTATION_CHECK / ADVERSARIAL_COVERAGE

PROHIBITED_FIELD_CHECK_RULE: проверка запрещённых полей выполняется
  по точному имени поля, не по подстроке. Вхождения внутри
  SIGN_CORE_CARD, SIGN_DATA_IS_SESSION_ONLY,
  SIGN_FALSE_EFFECT_MIMICRY_GUARD не считаются нарушением.

============================================================
ЧЕК-ЛИСТ ПЕРЕД ОТПРАВКОЙ НА STRUCTURAL_PREFLIGHT_PASS
============================================================

[ ] Все поля META заполнены, ни одного <...> placeholder
[ ] ZONE выбран и обоснован в SEMANTIC_EPOCH_TRACKER
[ ] BASE_MODE заполнен как отдельное категориальное значение
[ ] WHAT_THIS_SIGN_IS_NOT содержит минимум 10 пунктов
[ ] BASE_FORMULAS содержит минимум 10 формул
[ ] SAFE_CASES содержит минимум 6 кейсов
[ ] RISK_CASES содержит минимум 6 кейсов
[ ] CONFUSABLES содержит минимум 5 записей
[ ] CONTRADICTION_GUARDS содержит минимум 6 правил
[ ] SEQUENCE_LAYER_BOUNDARY заполнен или явно NOT_APPLICABLE
[ ] PHAGO_ENTITY_MIMICRY заполнен или явно объяснён как минимальный
[ ] Все 10 EFFECT_FIELDS присутствуют (обычно все NONE)
[ ] ADVERSARIAL_COVERAGE: MIN/ACTUAL/STATUS все три поля заполнены
[ ] MUTATION_CHECK содержит минимум 6 мутаций с RESULT
[ ] Ни одно из запрещённых полей (SIGN/UNICODE/GLYPH/SIGN_NAME/
    SIGN_UNICODE/SIGN_GLYPH) не использовано
[ ] LOCK-поля — раздельные (LAYER_A_LOCK/LAYER_B_LOCK/LAYER_C_LOCK/
    SEMANTIC_EPOCH_TRACKER_LOCK), не единый SCHEMA_LOCK

============================================================
END_OF_TEMPLATE
