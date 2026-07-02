ЧАСТНЫЙ АВТОРСКИЙ ПРОЕКТ / COMMERCIAL USE PROHIBITED
DOCUMENT_ID: MODULE_TEMPLATE_SINGLE_SIGN_GEN3_v0_2_PLUS_EPOCH_v0_1_EN
DOCUMENT_TYPE: MODULE_TEMPLATE
TEMPLATE_LINE: GEN3_v0_2_PLUS_EPOCH
DOCUMENT_STATUS: WORKINGLY_CLOSED
STATUS: WORKINGLY_CLOSED / NOT_LOCKED / NOT_RUNTIME / NOT_VALIDATOR / NOT_PRODUCTION
AUTHOR: Ruslan Malyavsky
CREATED_AT: 2026-06-18
VERSION: v0_1
AUTHOR_DECISION_REFERENCE: AUTHOR_DECISION_20260618_006_MODULE_TEMPLATE_WORKINGLY_CLOSED_EN
RUN_CARD_REFERENCE: SIGN_CONVEYOR_RUN_CARD_MODULE_TEMPLATE_SINGLE_SIGN_GEN3_v0_2_PLUS_EPOCH_v0_1_REVIEW_2_EN
RUN_CARD_STATUS: COMPLETED / PASS
============================================================ COMMON_CONVEYOR_DISCIPLINE
CONVEYOR_DISCIPLINE_VERSION: v0_2_PLUS_EPOCH
RUN_CARD_REQUIRED_BEFORE_LOCK: YES
RUN_CARD_TEMPLATE_REFERENCE: SIGN_CONVEYOR_RUN_CARD_TEMPLATE_GEN3_CONVEYOR_v0_2_PLUS_EPOCH_EN
RUN_CARD_STATUS: COMPLETED / PASS
POST_CONVEYOR_STATUS_AUDIT_REQUIRED: YES
AUDIT_TEMPLATE_REFERENCE: ALPHABET_AUDIT_TEMPLATE_GEN3_v0_2_PLUS_EPOCH_EN
LOCKED_WORKING_CORE_SELF_ASSIGNMENT: FORBIDDEN
MODEL_FAMILY_DIVERSITY_REQUIRED: YES
ADVERSARIAL_EVIDENCE_REQUIRED: YES
MUTATION_CHECK_REQUIRED: YES
LIMITATION_STATEMENT_REQUIRED: YES
AFTER_RUN_RESIDUE: FORBIDDEN
LIMITATION_STATEMENT:
THIS_MODULE_TEMPLATE IS A WORKINGLY_CLOSED ARTIFACT
NOT A FINAL_STANDARD
NOT A PARSER
NOT A RUNTIME
NOT A SECURITY_CERTIFICATE
NOT A PRODUCT
NOT A COMMERCIAL_OFFERING
CONVEYOR_PASS ≠ VALIDATION
MODEL_CONSENSUS ≠ TRUTH
INJECTION_TEST_PASS ≠ SECURITY_PROOF
GUARDS_HOLD_FOR_TESTED_CASES ≠ FUTURE_GUARANTEE
NO_ATTACK_FOUND ≠ NO_ATTACK_EXISTS
LOCK_RECOMMENDATION ≠ LOCK
RUN_CARD_RESULT ≠ FINAL_STATUS
WORKINGLY_CLOSED ≠ LOCKED_WORKING_CORE
MODULE_TEMPLATE ≠ MODULE_INSTANCE
MODULE_TEMPLATE ≠ IMPLEMENTATION
MODULE_TEMPLATE ≠ CERTIFICATION
============================================================ 0. UNIVERSALITY
BOUND_TO_TEMPLATE: YES
AFTER_USE_RESIDUE: FORBIDDEN
MODULE_DATA_IS_SESSION_ONLY: YES
============================================================
META
============================================================
MODULE_TEMPLATE_UID: MODULE_TEMPLATE_SINGLE_SIGN_GEN3_v0_2_PLUS_EPOCH_v0_1_EN
MODULE_NAME: SINGLE_SIGN_MODULE_TEMPLATE
MODULE_PURPOSE: Universal template for creating single-sign modules — software components implementing processing of an individual sign according to its SIGN_CORE_CARD
MODULE_SCOPE: Processing of one sign (U+XXXX) in the context of a message/text
MODULE_TYPE: SINGLE_SIGN / UNIVERSAL / CONFIGURATION_DRIVEN
DOCUMENT_STATUS: WORKINGLY_CLOSED
AUTHOR_DECISION_REFERENCE: AUTHOR_DECISION_20260618_006_MODULE_TEMPLATE_WORKINGLY_CLOSED_EN
RUN_CARD_REFERENCE: SIGN_CONVEYOR_RUN_CARD_MODULE_TEMPLATE_SINGLE_SIGN_GEN3_v0_2_PLUS_EPOCH_v0_1_REVIEW_2_EN
RUN_CARD_STATUS: COMPLETED / PASS
SOURCE_TEMPLATE: MODULE_TEMPLATE_GEN3_CONVEYOR_v0_2_PLUS_EPOCH_EN
CROSS_LANGUAGE_NOTE: Technical sections (1–11) retain original RU terminology for project consistency. Formula identifiers, pseudocode, and structural markers are language-agnostic. Descriptive text in META and INTERFACE sections is translated to EN.
============================================================ 1. ARCHITECTURE_PRINCIPLES
CORE_PRINCIPLE: MODULE_TEMPLATE ≠ SIGN_CORE_CARD
  MODULE_TEMPLATE — универсальный шаблон
  SIGN_CORE_CARD — конфигурация для конкретного знака
  MODULE_INSTANCE = MODULE_TEMPLATE + SIGN_CORE_CARD

CORE_PRINCIPLE: MODULE_TEMPLATE ≠ RUNTIME
  MODULE не знает, в какой runtime встраивается
  MODULE выдаёт универсальный результат
  INTEGRATOR адаптирует результат под конкретный runtime

CORE_PRINCIPLE: MODULE_TEMPLATE ≠ PARSER
  MODULE не парсит текст (это задача upstream-системы)
  MODULE получает уже выделенный знак + контекст
  MODULE принимает решение об интерпретации

CONFIGURATION_DRIVEN:
  Логика MODULE не hardcoded для конкретного знака
  Логика читается из SIGN_CORE_CARD во время инициализации
  Изменение знака = подключение другой карточки, не переписывание MODULE

ZONE_AWARENESS:
  MODULE должен учитывать ZONE знака при выборе алгоритма
  ZONE_1 (STABLE): минимальный контекстный анализ
  ZONE_2 (CONTEXT_DEPENDENT): CONTEXT_GATE анализ
  ZONE_3 (PRECESSIONAL): EPOCH-aware анализ

EPOCH_AWARENESS:
  ZONE_3 знаки требуют EPOCH-detection в MODULE
  MODULE должен определять ACTIVE_EPOCH по контексту
  MODULE должен уметь переключаться между EPOCH в зависимости от SUBSTRATE
============================================================ 2. INTERFACE_SPECIFICATION
INPUT_INTERFACE:
  INPUT_SIGN: U+XXXX (кодпоинт обрабатываемого знака)
  INPUT_CONTEXT: текстовый фрагмент, содержащий знак (минимум: строка, максимум: документ)
  INPUT_SIGN_OCCURRENCE:
    SIGN_OFFSET_START: integer (позиция начала знака в контексте)
    SIGN_OFFSET_END: integer (позиция конца знака в контексте)
    OCCURRENCE_ID: optional string (идентификатор вхождения)
    NEIGHBORING_SIGNS: optional list (соседние знаки в последовательности)
    SEQUENCE_CONTEXT: optional string (контекст последовательности)
  RULE: MODULE analyzes the specified occurrence of the sign, not every identical sign in the context.

INPUT_METADATA:
    PLATFORM: идентификатор платформы (Discord, TikTok, LinkedIn, etc.)
    SENDER_COHORT: возрастная/поколенческая когорта отправителя (Gen Z, Millennial, Boomer, etc.)
    CONVERSATION_HISTORY: предыдущие сообщения (опционально, для behavioral analysis)
    DOMAIN: профессиональный домен (medical, legal, educational, etc.)
    TIMESTAMP: временная метка сообщения (для EPOCH-drift detection)
  INPUT_SIGN_CORE_CARD: ссылка на SIGN_CORE_CARD (конфигурация)

OUTPUT_INTERFACE:
  OUTPUT_STATUS: структурированный результат обработки
    FIELDS:
      SIGN_CODEPOINT: U+XXXX (повтор входного кода для трассировки)
      SIGN_OFFSET_START: integer (PATCH_NOTE v0_1_PATCH_27,
        ПРИМЕНЕНО, верифицировано 5/5 единогласно) — повтор входного
        INPUT_SIGN_OCCURRENCE.SIGN_OFFSET_START для трассировки.
        НАХОДКА, мотивировавшая патч: это поле уже присутствует
        на ВХОДЕ MODULE_TEMPLATE (раздел INPUT_SIGN_OCCURRENCE),
        но никогда не возвращалось обратно в OUTPUT_STATUS —
        из-за этого SEQUENCE_MODULE_TEMPLATE не может восстановить
        реальные текстовые позиции знаков в последовательности
        (SOURCE_OCCURRENCE_LIST вынужденно равен NOT_AVAILABLE,
        см. SEQUENCE_MODULE_TEMPLATE PATCH_25/QUESTION_6).
      SIGN_OFFSET_END: integer (PATCH_NOTE v0_1_PATCH_27,
        ПРИМЕНЕНО) — аналогично, повтор
        INPUT_SIGN_OCCURRENCE.SIGN_OFFSET_END.
      CARD_VERSION: string (версия/UID загруженной SIGN_CORE_CARD для трассировки)
      ACTIVE_EPOCH: идентификатор активной эпохи (для ZONE_3) / NOT_APPLICABLE (для ZONE_1/2)
      INTERPRETATION: семантическая интерпретация знака в данном контексте
      RISK_LEVEL: NONE / LOW / MEDIUM / HIGH / CRITICAL
      RISK_CASES_TRIGGERED: список сработавших RISK_CASE (по ID из SIGN_CORE_CARD)
      GUARDS_TRIGGERED: список сработавших GUARD (по ID из SIGN_CORE_CARD)
      CONFIDENCE_SCORE: 0.0–1.0 (уверенность в интерпретации)
      AMBIGUITY_FLAG: YES / NO (признак неоднозначности, требующей human_review)
      RECOMMENDED_ACTION: INFO / MONITOR / FLAG_FOR_REVIEW / HUMAN_REVIEW / ESCALATE_TO_INTEGRATOR
FORBIDDEN_ACTION: MODULE_MUST_NOT_BLOCK_DIRECTLY
NOTE: BLOCK, DELETE, BAN, EXECUTE, ENFORCE are runtime/integrator actions, not MODULE_TEMPLATE outputs.
      EFFECT_FIELDS_STATUS: все EFFECT_FIELDS = NONE (проверка по LAYER_C)
      LAYER_ANOMALY_FLAG: YES / NO (передаётся из SIGN_CORE_CARD LAYER_A, если ABSENT_PHYSICAL_LAYER аномалия присутствует)
      OUTPUT_WARNINGS: список нефатальных предупреждений (например, DRIFTING обнаружена, но не критична; конфузибл найден, но не отклонён)
  OUTPUT_ERRORS: структура ошибок (если MODULE не смог обработать)

ERROR_INTERFACE:
  ERROR_TYPE:
    CARD_NOT_FOUND: SIGN_CORE_CARD не найдена для данного U+XXXX
    CARD_INVALID: SIGN_CORE_CARD повреждена или не соответствует TEMPLATE_LINE
    CONFUSABLE_DETECTED_REJECTED: входной знак является конфузиблом (визуально похож, но другой кодпоинт)
    ZONE_MISMATCH: ZONE знака не распознан или не поддерживается MODULE
    EPOCH_DETECTION_FAILED: не удалось определить ACTIVE_EPOCH для ZONE_3 знака
    CONTEXT_INSUFFICIENT: входной контекст недостаточен для анализа
    GUARD_EVALUATION_ERROR: ошибка оценки GUARD / advisory rule-check
    INTERNAL_ERROR: внутренняя ошибка MODULE
  ERROR_RESPONSE: MODULE должен вернуть ERROR_STATUS вместо OUTPUT_STATUS
  ERROR_LOGGING: ошибка должна логироваться с трассировкой для аудита
============================================================ 3. PROCESSING_PIPELINE
PIPELINE_STAGES: 8 этапов обработки (STAGE_1–8, включая STAGE_8 AFTER_RUN_CLEANUP)

STAGE_1: CARD_LOADING
  INPUT: U+XXXX
  ACTION: загрузка SIGN_CORE_CARD для данного кодпоинта
  CHECK: CARD_UID совпадает с запрошенным U+XXXX
  CHECK: DOCUMENT_STATUS = WORKINGLY_CLOSED или выше
  CHECK: TEMPLATE_LINE совместим с MODULE_TEMPLATE
  OUTPUT: загруженная карточка в память MODULE
  FAILURE: ERROR_TYPE = CARD_NOT_FOUND или CARD_INVALID

STAGE_2: ZONE_DETECTION + CONFUSABLE_CHECK
  INPUT: загруженная SIGN_CORE_CARD + INPUT_SIGN (U+XXXX)
  SUB_STAGE_2a: CONFUSABLE_CHECK
    ACTION: проверка, что входной U+XXXX совпадает с CODEPOINT в карточке
    CHECK: если входной знак визуально нормализуется в целевой, но имеет другой кодпоинт (например, U+FF03 ＃ вместо U+0023 #)
    OUTPUT: если конфузибл обнаружен → ERROR_TYPE = CONFUSABLE_DETECTED_REJECTED
    NOTE: это ранняя отбраковка до семантического анализа
  SUB_STAGE_2b: ZONE_DETECTION
    ACTION: чтение ZONE из LAYER_A
    VALUES: ZONE_1 / ZONE_2 / ZONE_3
    OUTPUT: определённый ZONE
    ROUTING: ZONE определяет дальнейший путь обработки
    ZONE_1 → STAGE_3a (STABLE_PROCESSING)
    ZONE_2 → STAGE_3b (CONTEXT_PROCESSING)
    ZONE_3 → STAGE_3c (EPOCH_PROCESSING)

STAGE_3a: STABLE_PROCESSING (ZONE_1)
  INPUT: SIGN_CORE_CARD (ZONE_1)
  ACTION: применение BASE_FORMULA из LAYER_A
  LOGIC: семантика не зависит от контекста и времени
  CHECK: WHAT_THIS_SIGN_IS_NOT — проверка на ложные эффекты
  CHECK: SAFE_CASES — соответствует ли контекст безопасному сценарию
  CHECK: RISK_CASES — соответствует ли контекст рисковому сценарию
    (PATCH_NOTE v0_1_PATCH_22: добавлено — ZONE_1 ≠ "риска нет",
    ZONE_1 означает только "семантика не зависит от эпохи/контекста
    выбора алгоритма"; RISK_CASES всё равно должны сверяться)
  OUTPUT: INTERPRETATION = BASE_MODE (например, DATA_ONLY для DOT)
  RISK_LEVEL: определяется матчингом против RISK_CASES, не
    хардкодом (см. PATCH_NOTE выше); по умолчанию NONE при
    отсутствии срабатывания
  SKIP: CONTEXT_GATE, EPOCH_DETECTION не требуются

STAGE_3b: CONTEXT_PROCESSING (ZONE_2)
  INPUT: SIGN_CORE_CARD (ZONE_2) + INPUT_CONTEXT + INPUT_METADATA
  ACTION: анализ контекста для определения активного SUBSTRATE
  LOGIC: CONTEXT_GATE — определение, какой контекст активен
    Примеры: math vs path vs URL vs date для SOLIDUS

  CHECK: SAFE_CASES — соответствует ли контекст безопасному сценарию
  CHECK: RISK_CASES — соответствует ли контекст рисковому сценарию
  CHECK: CONFUSABLES — не является ли знак конфузиблом
  OUTPUT: INTERPRETATION + RISK_LEVEL + CONFIDENCE_SCORE
  OPTIONAL: SEMANTIC_EPOCH_TRACKER (если присутствует в карточке как OPTIONAL_BLOCK)

STAGE_3c: EPOCH_PROCESSING (ZONE_3)
  INPUT: SIGN_CORE_CARD (ZONE_3) + INPUT_CONTEXT + INPUT_METADATA
  ACTION: определение ACTIVE_EPOCH по контексту
  SUB-STAGES:
    SUB_3c_0: CONTEXT_GATE_RESOLUTION (только для ACTIVE_EPOCH_TYPE: CONTEXT_GATE_REQUIRED)
      ACTION: определение активного контекста из INPUT_METADATA (PLATFORM, DOMAIN, SENDER_COHORT)
      LOGIC: использование CONTEXT_ACTIVE_EPOCH_MAP из SIGN_CORE_CARD для выбора эпохи по контексту
      OUTPUT: предварительный ACTIVE_EPOCH для дальнейшего уточнения
    SUB_3c_1: SUBSTRATE_ANALYSIS — определение платформы/поколения/домена
    SUB_3c_2: COHORT_DETECTION — анализ SENDER_COHORT
    SUB_3c_3: PLATFORM_NORM_CHECK — проверка норм платформы
    SUB_3c_4: EPOCH_MATCHING — сопоставление контекста с CAPTURE_HISTORY
      TIMESTAMP_USAGE: INPUT_METADATA.TIMESTAMP используется для сопоставления даты отправки с DATE_RANGE эпох
      LOGIC: если TIMESTAMP попадает в DATE_RANGE эпохи → повышается MATCH_SCORE
      BRANCHING: если ACTIVE_EPOCH_TYPE == CONTEXT_GATE_REQUIRED → использовать результат SUB_3c_0 как базу
      BRANCHING: если ACTIVE_EPOCH_TYPE == GLOBAL → использовать полный CAPTURE_HISTORY
    SUB_3c_5: PRECESSION_ALERT_CHECK — проверка DRIFTING тенденций
      TIMESTAMP_USAGE: INPUT_METADATA.TIMESTAMP используется для определения, наблюдается ли DRIFTING в текущий момент
      OUTPUT_WARNINGS: если DRIFTING обнаружена, но не критична → добавить в OUTPUT_WARNINGS (не повышать RISK_LEVEL)
  CHECK: DORMANT_EPOCHS — может ли контекст реактивировать старую эпоху
  CHECK: Higher_epoch_suppresses_lower — доминирует ли новая эпоха
  OUTPUT: ACTIVE_EPOCH + INTERPRETATION + RISK_LEVEL + CONFIDENCE_SCORE
  AMBIGUITY_LOGIC:
    AMBIGUITY_FLAG = YES если:
      (CONFIDENCE_SCORE < CONFIDENCE_THRESHOLD) ИЛИ
      (несколько ACTIVE_EPOCH с MATCH_SCORE разницей < 0.2)
    AMBIGUITY_FLAG = NO если:
      (CONFIDENCE_SCORE ≥ CONFIDENCE_THRESHOLD) И
      (одна доминирующая ACTIVE_EPOCH с MATCH_SCORE ≥ 0.8)

STAGE_4: GUARD_EVALUATION
  INPUT: результат STAGE_3 + SIGN_CORE_CARD (LAYER_B)
  ACTION: последовательная оценка всех GUARD из карточки как advisory rules
  GUARD_TYPES:
    CONTRADICTION_GUARDS (CG): проверка конкретных ложных утверждений
    SEQUENCE_LAYER_BOUNDARY: фиксация факта нахождения знака в последовательности (решение о multi-sign обработке передаётся INTEGRATOR)
    PHAGO_ENTITY_MIMICRY: проверка PHAGO-подобных атак (для эмодзи)
  LOGIC: каждый GUARD — advisory rule-check (PASS / FAIL), не математическое доказательство
  OUTPUT:
    GUARDS_TRIGGERED: список FAIL
    GUARDS_PASSED: список PASS
    GUARD_CONFIDENCE: уверенность в оценке
    GUARD_LIMITATION_NOTE: GUARD_PASS ≠ SECURITY_PROOF, GUARD_FAIL ≠ FINAL_VERDICT
  EFFECT: если GUARD FAIL → корректировка INTERPRETATION или повышение RISK_LEVEL
  LIMITATION: GUARD_PASS ≠ SECURITY_PROOF, GUARD_FAIL ≠ FINAL_VERDICT

STAGE_5: RISK_ASSESSMENT
  INPUT: результаты STAGE_3 + STAGE_4
  ACTION: агрегация рисков
  LOGIC:
    RISK_LEVEL = MAX(RISK_CASES_TRIGGERED)
    Если GUARD FAIL → RISK_LEVEL может повыситься
    Если AMBIGUITY_FLAG = YES → RISK_LEVEL ≥ MEDIUM
    Если EFFECT_FIELDS не все NONE → критическая ошибка (карточка нарушена)
  CHECK: LIMITATION_STATEMENT карточки — MODULE не должен превышать ограничения
  OUTPUT: финальный RISK_LEVEL + RECOMMENDED_ACTION

STAGE_6: EFFECT_VALIDATION
  INPUT: SIGN_CORE_CARD (LAYER_C) + текущая INTERPRETATION
  ACTION: проверка, что MODULE не приписал знаку эффектов
  CHECK: EFFECT_FIELDS_ALL_NONE = YES (для DATA_ONLY знаков)
  CHECK: CLOSED_SCHEMA = YES (нет неизвестных полей)
  OUTPUT: EFFECT_FIELDS_STATUS (VALID / INVALID)
  FAILURE: если EFFECT_FIELDS не NONE → ERROR_TYPE = INTERNAL_ERROR (нарушение архитектуры)

STAGE_7: OUTPUT_ASSEMBLY
  INPUT: все результаты STAGE_1–6
  ACTION: сборка финального OUTPUT_STATUS
  STRUCTURE: см. OUTPUT_INTERFACE
  VALIDATION: проверка полноты всех полей
  RETURN: OUTPUT_STATUS или ERROR_STATUS

STAGE_8: AFTER_RUN_CLEANUP
  INPUT: OUTPUT_STATUS или ERROR_STATUS
  ACTION: проверка отсутствия остатков (AFTER_RUN_RESIDUE: FORBIDDEN)
  CHECK: временные данные очищены
  CHECK: кэш сессии очищен (RULE_5: SESSION_ONLY)
  CHECK: логи переданы интегратору (если требуется)
  OUTPUT: CLEANUP_CONFIRMATION
  NOTE: STAGE_8 не изменяет OUTPUT_STATUS, только гарантирует отсутствие остатков
============================================================ 4. ZONE-SPECIFIC_ALGORITHMS
ZONE_1_ALGORITHM (STABLE):
  COMPLEXITY: O(1) — константная
  CONTEXT_REQUIRED: NO (или минимальный)
  EPOCH_REQUIRED: NO
  GUARD_COUNT: минимальный (обычно 0–2)
  EXAMPLE: DOT — всегда DATA_ONLY, всегда NONE эффектов (LAYER_C),
    но RISK_LEVEL (LAYER_B) при этом не обязан быть всегда NONE —
    у ZONE_1-знака могут быть нетривиальные RISK_CASES (например,
    DOT: RISK_CASE_002, HIGH, фишинговый домен)
  PSEUDO_CODE:
    LOAD CARD
    READ BASE_MODE
    MATCH INPUT_CONTEXT against SAFE_CASES / RISK_CASES
    RETURN BASE_MODE + матчинговый RISK_LEVEL + CONFIDENCE=1.0
  NOTE: "стабильность" ZONE_1 означает, что семантика знака не
    зависит от эпохи/контекстного гейта (в отличие от ZONE_2/3) —
    это НЕ означает, что у знака нет риск-кейсов. EFFECT_FIELDS
    (LAYER_C) для ZONE_1 действительно всегда NONE, но RISK_CASES
    (LAYER_B) должны сверяться так же, как в ZONE_2_ALGORITHM ниже.
  PATCH_NOTE (v0_1_PATCH_22, координатор/автор, 2026-06-23,
    TYPE_F fix-patch): найдено при TIER_1 SIMULATION_GATE карточки
    SIGN_CORE_CARD_DOT_U002E_GEN3_v0_3_RU — псевдокод жёстко
    возвращал NONE_RISK без сверки с RISK_CASES, из-за чего
    RISK_CASE_002 (HIGH) карточки DOT не мог сработать ни при каких
    условиях. Исправлено по аналогии с ZONE_2_ALGORITHM.
    STATUS: CONVEYOR_VERIFIED (2026-06-24) — узкий раунд
    CONVEYOR_RUN_PACKET_MODULE_TEMPLATE_PATCH22_VERIFICATION_v0_1,
    4 ревьюера (Kimi, Gemini, GPT-5.5, Grok), VERDICT: ACCEPT 4/4,
    0 CRITICAL, 0 MAJOR, 0 MINOR. Координатор лично проверил
    главное заявление ревьюеров (отсутствие "третьих мест" со
    старым поведением) прямым поиском NONE_RISK по файлу —
    оставшиеся два упоминания относятся только к PATCH_NOTE и
    PATCH_HISTORY (описание прошлого состояния), не к действующей
    логике. AUTHOR_DECISION для MODULE_TEMPLATE — отдельным шагом,
    не присваивается автоматически этим патчем.

ZONE_2_ALGORITHM (CONTEXT_DEPENDENT):
  COMPLEXITY: O(n) — линейная по длине контекста
  CONTEXT_REQUIRED: YES
  EPOCH_REQUIRED: OPTIONAL (если SEMANTIC_EPOCH_TRACKER присутствует)
  GUARD_COUNT: средний (3–6)
  EXAMPLE: SOLIDUS — определение math vs path vs URL
  PSEUDO_CODE:
    LOAD CARD
    EXTRACT CONTEXT_SUBSTRATE
    MATCH SUBSTRATE against SAFE_CASES / RISK_CASES
    APPLY CONTEXT_GATE
    RETURN INTERPRETATION + RISK + CONFIDENCE

ZONE_3_ALGORITHM (PRECESSIONAL):
  COMPLEXITY: O(n × m) — линейная по контексту × количество эпох
  CONTEXT_REQUIRED: YES
  EPOCH_REQUIRED: YES (обязательно)
  GUARD_COUNT: высокий (6–12)
  EXAMPLE: SKULL — определение EPOCH_1 vs EPOCH_2 vs EPOCH_3
  PSEUDO_CODE:
    LOAD CARD
    READ ACTIVE_EPOCH_TYPE (GLOBAL / CONTEXT_GATE_REQUIRED / NONE)
    IF ACTIVE_EPOCH_TYPE == CONTEXT_GATE_REQUIRED:
      EXTRACT CONTEXT (platform, domain, cohort)
      USE CONTEXT_ACTIVE_EPOCH_MAP to select base EPOCH
    ELSE:
      EXTRACT SUBSTRATE (platform, cohort, domain)
    FOR EACH EPOCH in CAPTURE_HISTORY:
      MATCH SUBSTRATE against EPOCH.SUBSTRATE
      CALCULATE MATCH_SCORE
    SELECT ACTIVE_EPOCH = MAX(MATCH_SCORE)
    CHECK DORMANT_EPOCHS for reactivation triggers
    APPLY GUARDS (generational, platform, domain)
    RETURN INTERPRETATION + RISK + CONFIDENCE + AMBIGUITY_FLAG
============================================================ 5. CONFIGURATION_INTERFACE
CONFIGURATION_INPUT:
  SIGN_CORE_CARD_PATH: путь к файлу карточки (или реестр карточек)
  CARD_REGISTRY: централизованный реестр всех WORKINGLY_CLOSED карточек (абстрактный интерфейс, формат определяется реализацией: файловая система, БД, REST API)
  MODULE_PARAMETERS:
    CONFIDENCE_THRESHOLD: 0.0–1.0 (порог для AMBIGUITY_FLAG)
    RISK_ESCALATION_RULES: правила повышения риска при GUARD FAIL
    EPOCH_DETECTION_MODEL: модель/алгоритм для определения эпохи (по умолчанию: rule-based)
    CONTEXT_WINDOW_SIZE: размер окна контекста (в символах или токенах)
    COHORT_ANALYSIS_ENABLED: YES / NO (включён ли анализ поколений)
    PLATFORM_NORM_DB: база норм платформ (опционально)

LOGGING_INTERFACE:
  LOG_FORMAT: структурированный лог (JSON)
  REQUIRED_FIELDS:
    TIMESTAMP: временная метка события
    MODULE_UID: идентификатор экземпляра модуля
    CARD_UID: UID загруженной SIGN_CORE_CARD
    ERROR_TYPE: тип ошибки (если применимо)
    CONTEXT_HASH: хеш контекста (для приватности, без хранения полного текста)
    SESSION_ID: идентификатор сессии
  POLICY: логирование согласно audit policy интегратора, persistent logging не требуется MODULE_TEMPLATE
  LIMITATION: если AFTER_RUN_RESIDUE: FORBIDDEN — логи не должны сохраняться между сессиями

CONFIGURATION_RULES:
  RULE_1: MODULE не может работать без загруженной SIGN_CORE_CARD
  RULE_2: MODULE не может использовать карточку со статусом ниже WORKINGLY_CLOSED
  RULE_3: MODULE должен проверять TEMPLATE_LINE совместимость
  RULE_4: MODULE должен передавать все ERROR_STATUS в LOGGING_INTERFACE текущей сессии. Persistent logging не требуется MODULE_TEMPLATE и определяется INTEGRATOR audit policy.
  RULE_5: MODULE не должен кэшировать SIGN_CORE_CARD между сессиями (SESSION_ONLY)
  RULE_6: MODULE_INSTANCE может поддерживать hot-reload при получении нового патча карточки, но MODULE_TEMPLATE не предписывает конкретный механизм. Если hot-reload включён, он должен работать в рамках текущей сессии (не нарушая RULE_5: SESSION_ONLY) и сохранять audit rules.
============================================================ 6. ADVERSARIAL_COVERAGE — RUN CARD SEED
MIN_TOTAL_VECTORS: 12 (6 categories A-F, 2 per category)
CATEGORY_A: CARD_MANIPULATION (3)
  A1: Подмена CARD_UID — MODULE загружает карточку для другого знака
  A2: Повреждённая карточка — MODULE получает карточку без обязательных секций
  A3: Карточка со статусом WORKING_DRAFT — MODULE получает карточку, не прошедшую конвейер (должен вернуть CARD_INVALID)
CATEGORY_B: ZONE_MISMATCH (2)
  B1: ZONE_3 знак обрабатывается как ZONE_1 (пропуск EPOCH_DETECTION)
  B2: ZONE_1 знак обрабатывается как ZONE_3 (ложный EPOCH_DETECTION)
CATEGORY_C: CONTEXT_INJECTION (2)
  C1: Контекст манипулирован для активации неправильной эпохи
  C2: Метаданные подделаны (ложная когорта, ложная платформа)
CATEGORY_D: GUARD_BYPASS (3)
  D1: Входные данные сконструированы для обхода CONTRADICTION_GUARDS
  D2: SEQUENCE_LAYER_BOUNDARY игнорируется (знак в последовательности обрабатывается как одиночный)
  D3: Межсессионное кэширование — MODULE кэширует SIGN_CORE_CARD между сессиями (нарушение RULE_5: SESSION_ONLY)
CATEGORY_E: EFFECT_INJECTION (2)
  E1: MODULE приписывает знаку эффект, которого нет в карточке
  E2: MODULE игнорирует EFFECT_FIELDS_ALL_NONE = YES
CATEGORY_F: EPOCH_DRIFT_EXPLOITATION (2)
  F1: Контекст манипулирован для активации DORMANT_EPOCH вместо ACTIVE_EPOCH
  F2: DRIFTING тенденция эксплуатируется до подтверждения как EPOCH
ACTUAL_TOTAL_VECTORS: 14
COVERAGE_STATUS: SUFFICIENT (14 ≥ 12)
============================================================ 7. MUTATION_CHECK
MUTATION_01:
  CLAIM: MODULE может работать без SIGN_CORE_CARD
  EXPECTED: FAIL — MODULE_TEMPLATE без карточки = ERROR_TYPE = CARD_NOT_FOUND
  RESULT: FAIL
MUTATION_02:
  CLAIM: MODULE может использовать карточку со статусом WORKING_DRAFT
  EXPECTED: FAIL — RULE_2: только WORKINGLY_CLOSED и выше
  RESULT: FAIL
MUTATION_03:
  CLAIM: MODULE может приписать знаку authority_effect
  EXPECTED: FAIL — LAYER_C гарантирует EFFECT_FIELDS_ALL_NONE = YES для DATA_ONLY
  RESULT: FAIL
MUTATION_04:
  CLAIM: ZONE_3 MODULE может пропустить EPOCH_DETECTION
  EXPECTED: FAIL — STAGE_2 routing обязателен
  RESULT: FAIL
MUTATION_05:
  CLAIM: MODULE может кэшировать карточку между сессиями
  EXPECTED: FAIL — RULE_5: SESSION_ONLY
  RESULT: FAIL
MUTATION_06:
  CLAIM: MODULE может игнорировать GUARD FAIL
  EXPECTED: FAIL — STAGE_4 обязателен, GUARD FAIL влияет на RISK_LEVEL
  RESULT: FAIL
============================================================ 8. KNOWN_OPEN_QUESTIONS
OQ1:
  QUESTION: Какой алгоритм EPOCH_DETECTION использовать по умолчанию (rule-based vs ML-based)?
  STATUS: CLOSED_AS_DELEGATED_TO_IMPLEMENTER
  BLOCKS_WORKINGLY_CLOSED: NO
  NOTE: MODULE_TEMPLATE не предписывает конкретный алгоритм. Выбор алгоритма — задача разработчика MODULE_INSTANCE. Шаблон определяет интерфейс и требования, не реализацию.

OQ2:
  QUESTION: Должен ли MODULE поддерживать hot-reload карточек во время работы?
  STATUS: CLOSED_AS_DELEGATED_TO_IMPLEMENTER
  BLOCKS_WORKINGLY_CLOSED: NO
  NOTE: RULE_6 допускает hot-reload, но не предписывает. Конкретная реализация зависит от runtime / implementer.

OQ3:
  QUESTION: Какой формат CARD_REGISTRY (файловая система, БД, REST API)?
  STATUS: CLOSED_AS_DELEGATED_TO_IMPLEMENTER
  BLOCKS_WORKINGLY_CLOSED: NO
  NOTE: MODULE_TEMPLATE определяет интерфейс CONFIGURATION_INPUT, не хранилище.

ALL_OPEN_QUESTIONS_CLOSED: YES
============================================================ 9. LIMITATION_STATEMENT
LIMITATION_STATEMENT:
THIS_MODULE_TEMPLATE IS A WORKINGLY_CLOSED ARTIFACT
NOT A FINAL_STANDARD
NOT A PARSER
NOT A RUNTIME
NOT A SECURITY_CERTIFICATE
NOT A PRODUCT
NOT A COMMERCIAL_OFFERING
MODULE_TEMPLATE ≠ MODULE_INSTANCE
MODULE_TEMPLATE ≠ IMPLEMENTATION
MODULE_TEMPLATE ≠ CERTIFICATION
CONVEYOR_PASS ≠ VALIDATION
RUN_CARD_RESULT ≠ FINAL_STATUS
WORKINGLY_CLOSED ≠ LOCKED_WORKING_CORE
============================================================ 10. INTEGRATION_INTERFACE_STATUS
INTEGRATION_INTERFACE_STATUS:
STATUS: READY_PENDING_CONCRETE_INTEGRATOR
ATTACHED_INTEGRATOR_UID: NONE_CURRENTLY_ATTACHED
ACTIVE_MODULES_COUNT: 0
RUNTIME_ATTACHMENT: NONE
PERMANENT_BINDING: NO
SESSION_ONLY_BINDING: YES
AFTER_RUN_RESIDUE: FORBIDDEN
============================================================ 11. PATCH_HISTORY
PATCH_HISTORY:
v0_1: initial WORKING_DRAFT for MODULE_TEMPLATE_SINGLE_SIGN
v0_1_PATCH_01: INTERFACE_SPECIFICATION filled — P1
v0_1_PATCH_02: PROCESSING_PIPELINE filled (7 stages) — P2
v0_1_PATCH_03: ZONE-SPECIFIC_ALGORITHMS filled — P3
v0_1_PATCH_04: CONFIGURATION_INTERFACE filled — P4
v0_1_PATCH_05: ADVERSARIAL_COVERAGE filled (12 vectors) — P5
v0_1_PATCH_06: MUTATION_CHECK filled (6×FAIL) — P6
v0_1_PATCH_07: KNOWN_OPEN_QUESTIONS closed (all delegated to implementer) — P7
v0_1_PATCH_08: LIMITATION_STATEMENT and INTEGRATION_INTERFACE_STATUS filled — P8
v0_1_PATCH_09: CRIT-01 fix — LIMITATION_STATEMENT WORKINGLY_CLOSED → WORKING_DRAFT — TYPE_F (fix-patch)
v0_1_PATCH_10: M1/M5 — RECOMMENDED_ACTION BLOCK removed, GUARD_EXECUTION → GUARD_EVALUATION — TYPE_F (fix-patch)
v0_1_PATCH_11: M4 — INPUT_SIGN_OCCURRENCE added — TYPE_P (content-patch)
v0_1_PATCH_12: MAJ-02/03 — TIMESTAMP usage, AMBIGUITY_FLAG logic — TYPE_F (fix-patch)
v0_1_PATCH_13: FINDING_1/2 — CONFUSABLE_CHECK, LAYER_ANOMALY_FLAG — TYPE_P (content-patch)
v0_1_PATCH_14: M2/M3/W1 — CONTEXT_GATE_RESOLUTION, OUTPUT_WARNINGS, ZONE_3 pseudocode — TYPE_P (content-patch)
v0_1_PATCH_15: MIN-01/02/W1 — RULE_6 clarified, A3 vector, D3 vector — TYPE_N (clarification-patch) + TYPE_P (content-patch)
v0_1_PATCH_16: AFTER_RUN_CLEANUP (STAGE_8), LOGGING_INTERFACE, CARD_REGISTRY format — TYPE_P (content-patch)
v0_1_PATCH_17: m1 — GUARD_EXECUTION_ERROR → GUARD_EVALUATION_ERROR — TYPE_F (fix-patch)
v0_1_PATCH_18: m2/MAJ-N1 — RULE_4 смягчён: логирование через session LOGGING_INTERFACE, persistent logging не требуется — TYPE_N (clarification-patch)
v0_1_PATCH_19: m3 — OQ2 "рекомендует" → "допускает" — TYPE_N (clarification-patch)
v0_1_PATCH_20: MIN-N1 — PIPELINE_STAGES формулировка исправлена — TYPE_F (fix-patch)
v0_1_PATCH_21: MIN-N2 — NOTE про DOT из STAGE_3b удалён — TYPE_F (fix-patch)
v0_1_PATCH_22: ZONE_1_ALGORITHM — добавлена сверка с SAFE_CASES/
  RISK_CASES вместо жёсткого NONE_RISK (координатор/автор,
  2026-06-23, по находке TIER_1 SIMULATION_GATE карточки DOT) —
  TYPE_F (fix-patch)
v0_1_PATCH_23: SIGN_OFFSET_PROPAGATION — добавлены поля
  SIGN_OFFSET_START и SIGN_OFFSET_END в OUTPUT_STATUS (раздел 2,
  OUTPUT_INTERFACE), повторяющие соответствующие значения из
  входного INPUT_SIGN_OCCURRENCE. НАХОДКА, мотивировавшая патч:
  эти данные уже присутствовали на ВХОДЕ MODULE_TEMPLATE, но
  никогда не возвращались на выход — из-за этого
  SEQUENCE_MODULE_TEMPLATE не мог заполнить SOURCE_OCCURRENCE_LIST
  реальными позициями (оставался NOT_AVAILABLE, см.
  SEQUENCE_MODULE_TEMPLATE PATCH_25/QUESTION_6). По прямому
  указанию автора ("закрыть дыры сейчас, не хочу, чтобы они через
  год полезли") патч применён, несмотря на то что трогает
  документ, уже трижды подтверждённый независимыми TIER-
  симуляциями (DOT TIER_1, SOLIDUS TIER_2, SKULL TIER_3, все три —
  в ПРЕЖНЕМ виде интерфейса, 22/22).
  ОСОБЫЙ ХАРАКТЕР ВЕРИФИКАЦИИ (TYPE_P, аддитивное расширение
  интерфейса WORKINGLY_CLOSED документа, ранее подтверждённого
  тремя TIER): текст патча верифицирован конвейером ДО применения
  (CONVEYOR_RUN_PACKET_SEQUENCE_TECH_DEBT_CLOSURE_v0_1,
  2026-06-26): 5/5 (Kimi, Gemini, GPT-5.5, Grok, Qwen) —
  APPROVE_FOR_APPLICATION единогласно. Явно проверен
  REGRESSION_CHECK на конкретных TIER-сценариях, выбранных
  РАЗНЫМИ ревьюерами независимо (GPT-5.5 — DOT TIER_1 "Версия
  3.14 выпущена.", Grok — DOT TIER_1 "paypal.com.security-
  check.ru" фишинговый сценарий, Qwen — концептуально все три
  SIMULATION_ARTIFACT). Все подтвердили: STAGE_1-6 не используют
  SIGN_OFFSET ни для чего, поля копируются из INPUT_SIGN_OCCURRENCE
  только на STAGE_7 (OUTPUT_ASSEMBLY), RISK_LEVEL/INTERPRETATION/
  CONFIDENCE_SCORE/AMBIGUITY_FLAG не меняются ни для одного из
  проверенных сценариев. Это чисто аддитивное расширение, не
  модифицирующее ни один из 22 существующих патчей.
  РЕКОМЕНДАЦИЯ Qwen (зафиксирована, не исполнена автоматически):
  "Требуется отдельное AUTHOR_DECISION для подтверждения
  применения PATCH_27 [текущий номер 23], так как это изменение
  уже валидированного документа" — оставлено на решение автора
  отдельно от факта применения патча.
  TYPE: TYPE_P (content-patch, аддитивное расширение
  OUTPUT_INTERFACE, не меняет логику STAGE_1-6)
PATCHES_APPLIED: 23
PATCHES_VERIFIED: 23/23
  v0_1_PATCH_22: VERIFIED_BY: CONVEYOR (2026-06-24) —
    CONVEYOR_RUN_PACKET_MODULE_TEMPLATE_PATCH22_VERIFICATION_v0_1,
    4 ревьюера (Kimi, Gemini, GPT-5.5, Grok), VERDICT: ACCEPT 4/4,
    0 CRITICAL/MAJOR/MINOR. Координатор лично проверил ключевое
    заявление (отсутствие "третьих мест" со старым NONE_RISK)
    прямым grep по файлу.
  v0_1_PATCH_23: VERIFIED_BY: CONVEYOR (2026-06-26) —
    CONVEYOR_RUN_PACKET_SEQUENCE_TECH_DEBT_CLOSURE_v0_1, 5
    ревьюеров (Kimi, Gemini, GPT-5.5, Grok, Qwen), VERDICT:
    APPROVE_FOR_APPLICATION 5/5, явный REGRESSION_CHECK на разных
    TIER-сценариях независимо выбранными ревьюерами, 0 регрессий
    найдено.
  AUTHOR_DECISION_NOTE: данный счётчик отражает конвейерную
    верификацию содержания патчей. Формальный AUTHOR_DECISION,
    переподтверждающий статус документа в целом (WORKINGLY_CLOSED)
    с учётом этих патчей — отдельный шаг, не присвоен
    автоматически. Для PATCH_23 это особенно актуально (см.
    рекомендацию Qwen выше) — документ ранее служил основой для
    трёх TIER-подтверждений (DOT/SOLIDUS/SKULL), и формальное
    переподтверждение их валидности с учётом нового интерфейса не
    выполнялось отдельно.
============================================================
END_OF_DOCUMENT