## PRIVATE AUTHOR PROJECT / COMMERCIAL USE PROHIBITED

DOCUMENT_ID: SEQUENCE_MODULE_TEMPLATE_GEN3_v0_2_PLUS_EPOCH_v0_1_EN
VERSION: v0_1
STATUS: WORKINGLY_CLOSED
AUTHOR: Ruslan Malyavsky
DATE: 2026-06-19
BOUND_TO_TEMPLATE: SEQUENCE_MODULE_TEMPLATE_GEN3_CONVEYOR_v0_2_PLUS_EPOCH
PURPOSE: Universal template for creating SEQUENCE_MODULE_INSTANCE — a sign sequence aggregation module
SEQUENCE_MODULE_NAME: UNIVERSAL_SEQUENCE_MODULE_TEMPLATE
SEQUENCE_MODULE_UID: SEQUENCE_MODULE_TEMPLATE_GEN3_v0_2_PLUS_EPOCH_v0_1_EN
SEQUENCE_MODULE_PURPOSE: Aggregation of OUTPUT_STATUS from multiple MODULE_INSTANCE into a single SEQUENCE_OUTPUT for passing to INTEGRATOR_INSTANCE
SEQUENCE_MODULE_SCOPE: Processing of a sign sequence (2..N), forming SEQUENCE_RISK_LEVEL, SEQUENCE_INTERPRETATION, EPOCH_SEQUENCE_CONTEXT
CORE_PRINCIPLE: SEQUENCE_MODULE_TEMPLATE ≠ MODULE_TEMPLATE
CORE_PRINCIPLE: SEQUENCE_MODULE_TEMPLATE ≠ RUNTIME
CORE_PRINCIPLE: SEQUENCE_MODULE_TEMPLATE ≠ PARSER
CORE_PRINCIPLE: SEQUENCE_MODULE_TEMPLATE ≠ FINAL_VERDICT
BOUNDARY: SEQUENCE_MODULE_TEMPLATE ≠ INTEGRATOR_TEMPLATE
BOUNDARY: SEQUENCE_MODULE_TEMPLATE ≠ SIGN_CORE_CARD
BOUNDARY: SEQUENCE_MODULE_TEMPLATE ≠ SEQUENCE_INTEGRATOR_TEMPLATE
DOCUMENT_STATUS: WORKINGLY_CLOSED
STATUS: WORKINGLY_CLOSED / NOT_LOCKED / NOT_RUNTIME / NOT_VALIDATOR / NOT_PRODUCTION

COMMON_CONVEYOR_DISCIPLINE:
  AUTHOR_DECISION_REFERENCE: AUTHOR_DECISION_20260619_008_SEQUENCE_MODULE_TEMPLATE_WORKINGLY_CLOSED_RU
  RUN_CARD_REFERENCE: PENDING
  RUN_CARD_STATUS: NOT_STARTED / PENDING
  CONVEYOR_PASS ≠ VALIDATION
  RUN_CARD_RESULT ≠ FINAL_STATUS
  WORKING_DRAFT ≠ WORKINGLY_CLOSED
  WORKINGLY_CLOSED ≠ LOCKED_WORKING_CORE

CROSS_LANGUAGE_STATUS: BILINGUAL_BRIDGE
CROSS_LANGUAGE_NOTE: Technical sections (1–11) retain original RU terminology for project consistency. Formula identifiers, pseudocode, and structural markers are language-agnostic. Descriptive text in META and header sections is translated to EN.
CROSS_LANGUAGE_NOTE_STATUS: INTENTIONAL_BILINGUAL_BRIDGE
RU_SOURCE_REFERENCE: SEQUENCE_MODULE_TEMPLATE_GEN3_v0_2_PLUS_EPOCH_v0_1_RU
TRANSLATION_SCOPE: HEADER_AND_META_TRANSLATED / TECHNICAL_SECTIONS_RETAIN_RU_FOR_PROJECT_CONSISTENCY
FULL_EN_MIRROR_REQUIRED: DEFERRED
CROSS_LANGUAGE_AUDIT_STATUS: PARTIAL_PASS
PROJECT_NORM: BILINGUAL_BRIDGE is the accepted standard for infrastructure templates (MODULE_TEMPLATE, INTEGRATOR_TEMPLATE, SEQUENCE_MODULE_TEMPLATE). Full EN mirror deferred until EN-native developer requires it.

## 1. ARCHITECTURE_PRINCIPLES

ARCHITECTURE_PRINCIPLES:
  PRINCIPLE_1: SEQUENCE_MODULE получает список OUTPUT_STATUS от MODULE_INSTANCE
  PRINCIPLE_2: SEQUENCE_MODULE агрегирует риски, не переопределяет семантику отдельных знаков
  PRINCIPLE_3: SEQUENCE_MODULE формирует SEQUENCE_OUTPUT, не FINAL_VERDICT
  PRINCIPLE_4: SEQUENCE_MODULE учитывает контекст соседних знаков (EPOCH_SEQUENCE_CONTEXT)
  PRINCIPLE_5: SEQUENCE_MODULE не изменяет INTERPRETATION отдельных знаков
  PRINCIPLE_6: SEQUENCE_MODULE не является runtime — только агрегатор
  PRINCIPLE_7: SEQUENCE_MODULE не устанавливает политику — только агрегирует сигналы
  PRINCIPLE_8: SEQUENCE_MODULE может работать с 2..N знаками (MAX_SEQUENCE_LENGTH определяется конфигурацией)
  PRINCIPLE_9: SEQUENCE_MODULE не обрабатывает знаки вне заданной последовательности
  PRINCIPLE_10: SEQUENCE_MODULE не кэширует результаты между сессиями (SESSION_ONLY)

INTEGRATION_CHAIN:
  INPUT: [MODULE_RESULT_1, MODULE_RESULT_2, ..., MODULE_RESULT_N] от MODULE_INSTANCE
  RULE: OUTPUT_STATUS elements are aggregated into SEQUENCE_OUTPUT.
  RULE: ERROR_STATUS elements are propagated into SEQUENCE_ERROR_STATUS and are not converted into SEQUENCE_INTERPRETATION.
  OUTPUT: SEQUENCE_OUTPUT → INTEGRATOR_INSTANCE
  SEQUENCE_INTEGRATOR: SEQUENCE_MODULE может передавать SEQUENCE_OUTPUT в SEQUENCE_INTEGRATOR_INSTANCE (если есть)
  BOUNDARY: SEQUENCE_MODULE ≠ INTEGRATOR (SEQUENCE_MODULE агрегирует, INTEGRATOR адаптирует)

## 2. INTERFACE_SPECIFICATION

INPUT_INTERFACE:
  SEQUENCE_INPUT:
    TYPE: LIST[MODULE_RESULT]
    SOURCE: MODULE_INSTANCE (один или несколько)
    MIN_LENGTH: 2
    MAX_LENGTH: определяется SEQUENCE_POLICY.MAX_SEQUENCE_LENGTH
    ELEMENT_STRUCTURE: MODULE_RESULT из MODULE_TEMPLATE (OUTPUT_STATUS или ERROR_STATUS)
    MODULE_RESULT:
      TYPE: OUTPUT_STATUS / ERROR_STATUS
      OUTPUT_STATUS: стандартный OUTPUT_STATUS из MODULE_TEMPLATE (RISK_LEVEL, INTERPRETATION, ACTIVE_EPOCH, ZONE, AMBIGUITY_FLAG, EFFECT_FIELDS_STATUS)
      ERROR_STATUS: MODULE_ERROR_STATUS из MODULE_TEMPLATE (ERROR_TYPE, ERROR_MESSAGE, SOURCE_MODULE_UID)
    SEQUENCE_INPUT_VALIDATION:
      CHECK_1: все OUTPUT_STATUS элементы имеют EFFECT_FIELDS_STATUS = VALID
      CHECK_1A: если элемент = ERROR_STATUS → ERROR_TYPE = MODULE_ERROR_IN_SEQUENCE
      CHECK_2: все OUTPUT_STATUS элементы имеют RISK_LEVEL из допустимого набора (NONE, LOW, MEDIUM, HIGH, CRITICAL)
      CHECK_3: для OUTPUT_STATUS элементов — EFFECT_FIELDS_STATUS = VALID
        SKIP: если элемент = ERROR_STATUS → skip EFFECT_FIELDS_STATUS check → route to CHECK_1A
      CHECK_3A: если элемент = ERROR_STATUS → ERROR_TYPE = MODULE_ERROR_IN_SEQUENCE
      CHECK_4: SOURCE_CONTEXT compatibility according to SEQUENCE_POLICY.SOURCE_CONTEXT_MODE
        MODE_STRICT_SAME_TEXT:
          RULE: все элементы должны иметь одинаковый SOURCE_TEXT_ID
          FAILURE: ERROR_TYPE = INCONSISTENT_CONTEXT
        MODE_SAME_THREAD_WINDOW:
          RULE: все элементы должны иметь одинаковый THREAD_ID
          REQUIRE: SEQUENCE_POLICY.THREAD_MODE = YES
          FAILURE_IF_THREAD_MODE_NO: ERROR_TYPE = SEQUENCE_POLICY_INVALID
          FAILURE_IF_DIFFERENT_THREAD: ERROR_TYPE = INCONSISTENT_CONTEXT
          WARNING_IF_RELAXED: SEQUENCE_OUTPUT_WARNING (не ошибка)
        MODE_SAME_SESSION_WINDOW:
          RULE: все элементы должны иметь одинаковый SESSION_ID
          REQUIRE: SEQUENCE_POLICY.SESSION_MODE = YES
          FAILURE_IF_SESSION_MODE_NO: ERROR_TYPE = SEQUENCE_POLICY_INVALID
          FAILURE_IF_DIFFERENT_SESSION: ERROR_TYPE = INCONSISTENT_CONTEXT
          WARNING_IF_RELAXED: SEQUENCE_OUTPUT_WARNING (не ошибка)
        DEFAULT_MODE: STRICT_SAME_TEXT
        NOTE: relaxed modes (SAME_THREAD_WINDOW / SAME_SESSION_WINDOW) требуют явного разрешения в SEQUENCE_POLICY
      CHECK_5: для OUTPUT_STATUS элементов — RISK_LEVEL из допустимого набора
        SKIP: если элемент = ERROR_STATUS → skip RISK_LEVEL check
      CHECK_6: если все элементы = ERROR_STATUS → ERROR_TYPE = ALL_ELEMENTS_ERROR
    MODULE_ERROR_PROPAGATION:
      RULE: если любой элемент = ERROR_STATUS → SEQUENCE_ERROR_TYPE = MODULE_ERROR_IN_SEQUENCE
      RULE: MODULE_ERROR_STATUS не преобразуется в SEQUENCE_INTERPRETATION
      ACTION: propagate MODULE_ERROR_STATUS в SEQUENCE_ERROR_STATUS без семантической переинтерпретации

OUTPUT_INTERFACE:
  SEQUENCE_OUTPUT:
    TYPE: STRUCT
    FIELDS:
      SEQUENCE_RISK_LEVEL: агрегированный риск (NONE, LOW, MEDIUM, HIGH, CRITICAL)
      SEQUENCE_INTERPRETATION: агрегированная интерпретация (STRING)
      SEQUENCE_INTERPRETATION_CONFLICT_FLAG: YES / NO (флаг конфликта интерпретаций)
      SOURCE_INTERPRETATION_LIST: список INTERPRETATION_1..N (неизменённый, для аудита и traceability)
      EPOCH_SEQUENCE_CONTEXT: список ACTIVE_EPOCH для всех знаков в последовательности
      SEQUENCE_AMBIGUITY: агрегированный флаг амбигуитета (YES / NO)
      SEQUENCE_ZONE: максимальная ZONE из последовательности (1, 2, 3)
      SEQUENCE_EFFECT_FIELDS_STATUS: VALID / INVALID (если хотя бы один INVALID → INVALID)
      SEQUENCE_LENGTH: фактическая длина последовательности
      SEQUENCE_CANDIDATE_MATCH: structure / NOT_APPLICABLE / NO_MATCH /
        CHECK_UNAVAILABLE (PATCH_NOTE v0_1_PATCH_24) — результат
        STAGE_2a, передаётся в SEQUENCE_INTEGRATOR для аудита
        источника риска (опциональное поле; SEQUENCE_INTEGRATOR_
        TEMPLATE на момент этого патча не ожидает его явно в своём
        INPUT_INTERFACE — симметричный микро-патч интегратора
        требуется отдельно, не блокирует применение этого патча,
        см. KNOWN_FOLLOW_UP_REQUIRED)
      SOURCE_SIGN_LIST: [SIGN_CODEPOINT_1, ..., SIGN_CODEPOINT_N]
        (PATCH_NOTE v0_1_PATCH_25) — список CODEPOINT в порядке
        следования элементов SEQUENCE_INPUT. Заполняется напрямую
        из SIGN_CODEPOINT, извлечённого в STAGE_2 (см. PATCH_24).
        Подвержен тому же ORDERING_INVARIANT, что и
        SEQUENCE_CONTEXT_TEXT (STAGE_2a) — порядок гарантируется
        порядком списка SEQUENCE_INPUT, не верифицированной
        позицией в тексте.
      SOURCE_OCCURRENCE_LIST: NOT_AVAILABLE
        (PATCH_NOTE v0_1_PATCH_25) — НЕ заполняется этим патчем.
        Реальные текстовые offset недоступны: OUTPUT_STATUS
        одиночного MODULE_TEMPLATE не возвращает SIGN_OFFSET (это
        поле есть только во входном INPUT_SIGN_OCCURRENCE
        одиночного модуля, не возвращается обратно). Заполнение
        фиктивными индексами (0,1,2...) было бы тихой подменой
        данных — не делается сознательно. Закрытие этого поля
        реальными значениями требует отдельного патча
        MODULE_TEMPLATE (другого, уже WORKINGLY_CLOSED документа)
        — добавление SIGN_OFFSET в его OUTPUT_STATUS, вне рамок
        этого патча.
        INTEGRATOR_RULE (по находке Kimi, раунд верификации
        2026-06-26): IF SOURCE_OCCURRENCE_LIST = NOT_AVAILABLE →
        COMBINATION_ANALYSIS и любая иная логика интегратора НЕ
        должны зависеть от позиционных offset — допустимо
        опираться только на порядок элементов SOURCE_SIGN_LIST.
        Проверено по тексту SEQUENCE_INTEGRATOR_TEMPLATE
        (STAGE_2/STAGE_3, раунд верификации): IDIOM_RECOGNITION
        использует точное совпадение последовательности CODEPOINT
        (SOURCE_SIGN_LIST) или INTERPRETATION, не offset — правило
        не нарушает существующую логику.
        NOTE (асимметрия, по находке Kimi): SOURCE_SIGN_LIST.length
        = N (реальные данные), SOURCE_OCCURRENCE_LIST = NOT_AVAILABLE
        (не массив той же длины) — интегратор НЕ должен предполагать
        parallel-array доступ между этими двумя полями. Если в
        будущем SOURCE_OCCURRENCE_LIST станет реальным массивом
        (после патча MODULE_TEMPLATE), оба списка будут иметь
        одинаковую длину и порядок — до этого момента такое
        предположение неверно.
      SOURCE_SEQUENCE: ссылка на входную последовательность
      SEQUENCE_MODULE_UID: идентификатор экземпляра SEQUENCE_MODULE
      SEQUENCE_TIMESTAMP: временная метка агрегации
      SEQUENCE_LIMITATION_NOTE: строка, подтверждающая ограничения SEQUENCE_MODULE

ERROR_INTERFACE:
  SEQUENCE_ERROR_TYPES:
    INVALID_SEQUENCE_INPUT: входная последовательность повреждена или неполна
    EMPTY_SEQUENCE: SEQUENCE_INPUT пуст (0 элементов)
    UNDER_MIN_LENGTH_SEQUENCE: SEQUENCE_INPUT содержит 1 элемент, но MIN_LENGTH = 2
    OVERSIZED_SEQUENCE: SEQUENCE_INPUT превышает MAX_SEQUENCE_LENGTH
    INCONSISTENT_CONTEXT: элементы из разных SOURCE_CONTEXT
    INVALID_ELEMENT: хотя бы один OUTPUT_STATUS элемент имеет EFFECT_FIELDS_STATUS = INVALID
    MODULE_ERROR_IN_SEQUENCE: хотя бы один элемент содержит ERROR_STATUS от MODULE_INSTANCE
    ALL_ELEMENTS_ERROR: все элементы содержат ERROR_STATUS от MODULE_INSTANCE
    SEQUENCE_POLICY_INVALID: SEQUENCE_POLICY содержит недопустимый AGGREGATION_MODE или отсутствуют требуемые карты
    AGGREGATION_ERROR: ошибка при агрегации (например, конфликтующие EPOCH)
    SEQUENCE_INTERNAL_ERROR: внутренняя ошибка SEQUENCE_MODULE
    ERROR_RESPONSE: SEQUENCE_MODULE должен вернуть SEQUENCE_ERROR_STATUS вместо SEQUENCE_OUTPUT

## 3. PROCESSING_PIPELINE

PIPELINE_STAGES: 7 этапов обработки (STAGE_1–7)

STAGE_1: SEQUENCE_INPUT_VALIDATION
  INPUT: SEQUENCE_INPUT + SEQUENCE_POLICY
  ACTION: валидация входной последовательности и SEQUENCE_POLICY
  CHECK_0: SEQUENCE_POLICY_VALIDATION
    RULE_1: если AGGREGATION_MODE = SUM → требуется RISK_NUMERIC_MAP
    RULE_2: если AGGREGATION_MODE = WEIGHTED → требуется WEIGHT_MAP и RISK_NUMERIC_MAP
    RULE_3: если AGGREGATION_MODE = CUMULATIVE → требуется CUMULATIVE_RULES
    RULE_4: если AGGREGATION_MODE = MAX → дополнительные карты не требуются
    RULE_5: если требуемая карта отсутствует → ERROR_TYPE = SEQUENCE_POLICY_INVALID
    RULE_6: если SOURCE_CONTEXT_MODE = SAME_THREAD_WINDOW → требуется THREAD_MODE = YES
    RULE_7: если SOURCE_CONTEXT_MODE = SAME_SESSION_WINDOW → требуется SESSION_MODE = YES
    RULE_8: если требуемый режим не разрешён → ERROR_TYPE = SEQUENCE_POLICY_INVALID
  CHECK_1: SEQUENCE_INPUT длина >= MIN_LENGTH (MIN_LENGTH = 2)
    IF length = 0 → ERROR_TYPE = EMPTY_SEQUENCE
    IF length = 1 → ERROR_TYPE = UNDER_MIN_LENGTH_SEQUENCE
  CHECK_2: SEQUENCE_INPUT не превышает MAX_SEQUENCE_LENGTH
  CHECK_3: для OUTPUT_STATUS элементов — EFFECT_FIELDS_STATUS = VALID (ERROR_STATUS пропускается к CHECK_1A)
  CHECK_3A: если элемент = ERROR_STATUS → ERROR_TYPE = MODULE_ERROR_IN_SEQUENCE
  CHECK_4: SOURCE_CONTEXT compatibility according to SEQUENCE_POLICY.SOURCE_CONTEXT_MODE
  CHECK_5: для OUTPUT_STATUS элементов — RISK_LEVEL из допустимого набора (ERROR_STATUS пропускается)
  CHECK_6: если все элементы = ERROR_STATUS → ERROR_TYPE = ALL_ELEMENTS_ERROR
  CHECK_7 (PATCH_NOTE v0_1_PATCH_26): SIGN_CARD_REGISTRY доступен
    (см. SEQUENCE_CONFIGURATION_INTERFACE) — требуется для
    STAGE_2a. IF недоступен → ERROR_TYPE = SEQUENCE_POLICY_INVALID
    (та же категория ошибки, что и для отсутствующих карт
    AGGREGATION_MODE, CHECK_0 RULE_5/8 — реестр карточек — это
    тоже часть конфигурации, не опциональная зависимость)
  ERROR_PRECEDENCE:
    IF all MODULE_RESULT elements are ERROR_STATUS → ERROR_TYPE = ALL_ELEMENTS_ERROR
    ELSE IF any MODULE_RESULT element is ERROR_STATUS → ERROR_TYPE = MODULE_ERROR_IN_SEQUENCE
    NOTE: ALL_ELEMENTS_ERROR имеет приоритет над MODULE_ERROR_IN_SEQUENCE
  FAILURE: SEQUENCE_ERROR_TYPE = INVALID_SEQUENCE_INPUT / EMPTY_SEQUENCE / UNDER_MIN_LENGTH_SEQUENCE / OVERSIZED_SEQUENCE / ALL_ELEMENTS_ERROR / INCONSISTENT_CONTEXT / INVALID_ELEMENT / MODULE_ERROR_IN_SEQUENCE / SEQUENCE_POLICY_INVALID

STAGE_2: SEQUENCE_ELEMENT_EXTRACTION
  INPUT: валидированная SEQUENCE_INPUT
  ACTION: извлечение ключевых полей из каждого OUTPUT_STATUS элемента
  EXTRACT: RISK_LEVEL, INTERPRETATION, ACTIVE_EPOCH, ZONE,
    AMBIGUITY_FLAG, SIGN_CODEPOINT, CARD_VERSION
  OUTPUT: SEQUENCE_ELEMENT_MAP (индексированный список полей)
  NOTE: SEQUENCE_MODULE не изменяет извлечённые поля — только структурирует
    (PATCH_NOTE v0_1_PATCH_24: добавлены SIGN_CODEPOINT и
    CARD_VERSION в EXTRACT — необходимы для STAGE_2a ниже, оба
    поля уже присутствуют в OUTPUT_STATUS одиночного
    MODULE_TEMPLATE по его OUTPUT_INTERFACE, не новые данные)

STAGE_2a: SEQUENCE_CANDIDATE_CROSS_CARD_CHECK
  (PATCH_NOTE v0_1_PATCH_26: переименован и обобщён из
  SEQUENCE_CANDIDATE_SAME_CARD_CHECK — раньше проверка
  ограничивалась ОДНОЙ картой (CHECK_SAME_CARD), отбрасывая любую
  последовательность из знаков разных карт без анализа
  (SEQUENCE_CANDIDATE_MATCH = NOT_APPLICABLE). Теперь проверка
  обобщена: same-card — частный случай, когда CARD_SET состоит из
  одной карты. НАХОДКА, мотивировавшая обобщение: SOLIDUS.SC3
  буквально содержит SEQUENCE: "../" — то есть карточка SOLIDUS
  САМА описывает межкарточную (DOT+DOT+SOLIDUS) последовательность
  как свой собственный кандидат. Прежний механизм игнорировал это
  полностью при ТЕСТ_3, потому что элементы принадлежали разным
  кодпоинтам. Это не теоретический, а реально найденный по тексту
  карточки случай.)

  INPUT: SEQUENCE_ELEMENT_MAP (после STAGE_2) + CARD_REGISTRY

  SEQUENCE_CONTEXT_TEXT_RECONSTRUCTION:
    ACTION: восстановление буквального текста последовательности
      из элементов SEQUENCE_ELEMENT_MAP
    LOGIC: SEQUENCE_CONTEXT_TEXT = CONCAT(VISIBLE_FORM(элемент_i)
      для i = 1..N, в порядке следования элементов в SEQUENCE_INPUT)
    ORDERING_INVARIANT (ЯВНО ЗАФИКСИРОВАННОЕ ПРЕДПОЛОЖЕНИЕ):
      порядок элементов в списке SEQUENCE_INPUT соответствует
      порядку их следования в исходном тексте. Это предположение
      НЕ проверяется явной позицией (OUTPUT_STATUS одиночного
      MODULE_TEMPLATE не содержит SIGN_OFFSET — это поле есть
      только во входном INPUT_SIGN_OCCURRENCE одиночного модуля,
      не возвращается обратно). Риск ASYMMETRIC: неверный порядок
      может привести к безопасному MISS (пропуску потенциального
      совпадения), но не к ложному HIT (подтверждено раундом 2
      верификации). FOLLOW_UP: см. v0_1_PATCH_27 для
      MODULE_TEMPLATE (отдельный документ) — добавление
      SIGN_OFFSET в OUTPUT_STATUS.
    PRIMARY_PATH: VISIBLE_FORM не входит в OUTPUT_STATUS
      одиночного MODULE_TEMPLATE явно (там есть только
      SIGN_CODEPOINT и CARD_VERSION) — поэтому получение
      VISIBLE_FORM через CARD_REGISTRY lookup по SIGN_CODEPOINT
      каждого элемента является ОСНОВНЫМ путём для ЛЮБОГО
      элемента, не исключительным сценарием отказа.

  CARD_SET_DETERMINATION (НОВОЕ, заменяет CHECK_SAME_CARD):
    ACTION: определить множество УНИКАЛЬНЫХ SIGN_CODEPOINT среди
      элементов SEQUENCE_ELEMENT_MAP
    OUTPUT: CARD_SET = {уникальные SIGN_CODEPOINT_1, ..., _K}
    NOTE: K=1 — частный случай, ранее называвшийся "same-card".
      K>1 — общий случай, ранее полностью игнорировавшийся.

  IF CARD_REGISTRY недоступен для какого-либо CODEPOINT из CARD_SET
    (защитная проверка, не должно происходить штатно):
    OUTPUT: SEQUENCE_CANDIDATE_MATCH = CHECK_UNAVAILABLE
    OUTPUT_WARNING: "CARD_REGISTRY_UNAVAILABLE_FOR_SC_CHECK"
  ELSE:
    FOR EACH card_codepoint IN CARD_SET:
      LOAD карточку SIGN_CORE_CARD для card_codepoint через
        CARD_REGISTRY
      READ SEQUENCE_CANDIDATES (раздел 7, LAYER_B) этой карточки
    CANDIDATE_POOL = UNION всех SEQUENCE_CANDIDATES из ВСЕХ карт
      в CARD_SET (не только "доминирующей" или "первой" карты)
    MATCH SEQUENCE_CONTEXT_TEXT (точное буквальное совпадение
      строки) против SEQUENCE_CANDIDATE.SEQUENCE КАЖДОГО
      кандидата из CANDIDATE_POOL, независимо от того, из какой
      карты он происходит
    IF найдено ровно одно совпадение:
      OUTPUT: SEQUENCE_CANDIDATE_MATCH = {
        CANDIDATE_ID: <SC-номер>,
        CANDIDATE_NAME: <NAME>,
        CANDIDATE_RISK_LEVEL: <RISK_LEVEL из карточки>,
        CANDIDATE_SOURCE_CARD: <CODEPOINT карты-источника кандидата>
          (НОВОЕ поле — для аудита: видно, что найденный
          кандидат может принадлежать карте, не совпадающей с
          большинством элементов последовательности)
      }
    IF найдено НЕСКОЛЬКО совпадений (разные карты дали кандидатов
      с одинаковым буквальным SEQUENCE):
      OUTPUT: SEQUENCE_CANDIDATE_MATCH = {
        MULTIPLE_MATCHES: [список всех найденных кандидатов с их
          CANDIDATE_SOURCE_CARD],
        CANDIDATE_RISK_LEVEL: MAX по всем найденным enum-значениям
          (не-enum значения исключаются из MAX, см. RULE_3A,
          сохраняются в MULTIPLE_MATCHES для делегирования
          интегратору)
      }
      OUTPUT_WARNING: "MULTIPLE_SEQUENCE_CANDIDATES_MATCHED" —
        указывает, что несколько разных карт независимо считают
        этот паттерн своим кандидатом; это TRACE_ONLY информация
        для аудита, не ошибка
    IF совпадений не найдено:
      OUTPUT: SEQUENCE_CANDIDATE_MATCH = NO_MATCH

  LIMITATION (ВАЖНО, НЕ ПУТАТЬ С ИСПРАВЛЕННЫМ ОГРАНИЧЕНИЕМ ВЫШЕ):
    Этот механизм находит кандидата ТОЛЬКО если ВСЕ знаки его
    SEQUENCE реально присутствуют как элементы в SEQUENCE_INPUT.
    Кандидаты, чей SEQUENCE включает знак, для которого upstream-
    система НЕ создала отдельный MODULE_RESULT (например,
    SOLIDUS.SC7 "://" требует элемента для ":", COLON — если
    COLON не передан как элемент SEQUENCE_INPUT вообще, никакой
    cross-card механизм его не найдёт, потому что отсутствующий
    знак невозможно сопоставить). Это НЕ исправлено этим патчем
    и не может быть исправлено на уровне SEQUENCE_MODULE — это
    ответственность upstream-парсера (системы, которая решает,
    какие знаки текста становятся отдельными MODULE_RESULT).
    ПРОВЕРКА ДЛЯ РАЗРАБОТЧИКА: если upstream-парсер не создаёт
    MODULE_RESULT для пунктуационных/служебных знаков типа ":",
    "@", "#" — соответствующие SEQUENCE_CANDIDATES в карточках,
    включающие эти знаки, останутся НЕДОСТИЖИМЫМИ независимо от
    качества SEQUENCE_MODULE.
STAGE_3: SEQUENCE_RISK_AGGREGATION
  INPUT: SEQUENCE_ELEMENT_MAP + SEQUENCE_CANDIDATE_MATCH (из STAGE_2a)
  ACTION: агрегация RISK_LEVEL из всех элементов
  AGGREGATION_RULES:
    RULE_1: MAX_RISK — SEQUENCE_RISK_LEVEL = MAX(RISK_LEVEL всех элементов)
    RULE_2: если хотя бы один элемент = CRITICAL → SEQUENCE_RISK_LEVEL = CRITICAL
    RULE_3: если все элементы = NONE И SEQUENCE_CANDIDATE_MATCH ∈
      {NOT_APPLICABLE, NO_MATCH, CHECK_UNAVAILABLE} →
      SEQUENCE_RISK_LEVEL = NONE
    RULE_3A (PATCH_NOTE v0_1_PATCH_24, обобщено v0_1_PATCH_26): если
      SEQUENCE_CANDIDATE_MATCH содержит CANDIDATE_RISK_LEVEL (один
      кандидат) ИЛИ MULTIPLE_MATCHES (несколько кандидатов из
      разных карт, см. STAGE_2a после PATCH_26):
        ENUM_GUARD: для каждого найденного CANDIDATE_RISK_LEVEL —
          IF значение ∈ {NONE, LOW, MEDIUM, HIGH, CRITICAL}:
            учитывается в MAX
          ELSE (описательная строка, например "intensity-dependent",
            "combined idiom", "epoch_mismatch", "seasonal_context",
            "spam-like"):
            не учитывается в MAX, сохраняется как есть в
            SEQUENCE_CANDIDATE_MATCH для делегирования интегратору
        SEQUENCE_RISK_LEVEL = MAX(SEQUENCE_RISK_LEVEL по RULE_1,
          все enum-значения CANDIDATE_RISK_LEVEL из найденных
          кандидатов — один или несколько)
        Если хотя бы один кандидат не-enum →
          OUTPUT_WARNING: "NON_ENUM_SEQUENCE_CANDIDATE_RISK_DELEGATED"
      RULE_3A применяется ПОСЛЕ RULE_1, ДО переопределения политикой
        (SEQUENCE_POLICY.AGGREGATION_MODE)
      ВЕРИФИЦИРОВАНО раундом 2 (Kimi, GPT-5.5×2, Qwen, Gemini,
        2026-06-26): подтверждено отсутствие регрессии на
        SKULL.SC1 (RISK_LEVEL: "intensity-dependent" не ломает
        MAX, корректно делегируется); подтверждено достижение
        HIGH на "//" через SOLIDUS.SC1 (не SC7, см. LIMITATION в
        STAGE_2a). ПОСЛЕ ОБОБЩЕНИЯ PATCH_26: cross-card случай
        (ранее CHECK_SAME_CARD=FALSE → автоматический skip)
        теперь обрабатывается через CARD_SET-механизм STAGE_2a —
        требует отдельной верификации этим же раундом
        (CONVEYOR_RUN_PACKET_SEQUENCE_TECH_DEBT_CLOSURE_v0_1).
    RULE_4: если есть ZONE_3 элементы → SEQUENCE_ZONE = 3
    RULE_5: агрегация может быть переопределена SEQUENCE_POLICY.AGGREGATION_MODE
      (RULE_3A применяется ДО любого переопределения политикой)
  AGGREGATION_MODES:
    MODE_MAX: максимальный риск (по умолчанию)
    MODE_SUM: суммарный риск (требует числовой шкалы)
    MODE_WEIGHTED: взвешенный риск (требует WEIGHT_MAP)
    MODE_CUMULATIVE: накопительный риск
  DEFAULT_MODE: MODE_MAX
  NOTE: SEQUENCE_MODULE не переопределяет семантику — только агрегирует риск

STAGE_4: EPOCH_SEQUENCE_CONTEXT_BUILDING
  INPUT: SEQUENCE_ELEMENT_MAP + ACTIVE_EPOCH из всех элементов
  ACTION: формирование EPOCH_SEQUENCE_CONTEXT и промежуточных флагов амбигуитета
  LOGIC:
    EPOCH_SEQUENCE_CONTEXT = [ACTIVE_EPOCH_1, ACTIVE_EPOCH_2, ..., ACTIVE_EPOCH_N]
    EPOCH_SEQUENCE_UNIQUE = UNIQUE(EPOCH_SEQUENCE_CONTEXT) - {NOT_APPLICABLE}
    EPOCH_SEQUENCE_COUNT = COUNT(EPOCH_SEQUENCE_UNIQUE)
  EPOCH_AMBIGUITY (промежуточный флаг):
    IF EPOCH_SEQUENCE_COUNT > 1 → EPOCH_AMBIGUITY = YES (разные эпохи в одной последовательности)
    IF EPOCH_SEQUENCE_COUNT = 1 → EPOCH_AMBIGUITY = NO
    IF EPOCH_SEQUENCE_COUNT = 0 → EPOCH_AMBIGUITY = NO (все элементы имеют NOT_APPLICABLE)
  ELEMENT_AMBIGUITY (промежуточный флаг):
    ELEMENT_AMBIGUITY = OR(AMBIGUITY_FLAG_1..N)
    YES — если хотя бы один элемент имеет AMBIGUITY_FLAG = YES
    NO — если все элементы имеют AMBIGUITY_FLAG = NO
  NOTE: SEQUENCE_AMBIGUITY (финальный) вычисляется в STAGE_6 после получения SEQUENCE_INTERPRETATION_CONFLICT_FLAG из STAGE_5
  NOTE: SEQUENCE_MODULE не решает, какая эпоха "правильная" — только документирует контекст
  NOTE: NOT_APPLICABLE исключается из подсчёта EPOCH_SEQUENCE_UNIQUE для предотвращения ложного EPOCH_AMBIGUITY

STAGE_5: SEQUENCE_INTERPRETATION_AGGREGATION
  INPUT: SEQUENCE_ELEMENT_MAP + INTERPRETATION из всех элементов
  ACTION: формирование SEQUENCE_INTERPRETATION и SEQUENCE_INTERPRETATION_CONFLICT_FLAG
  LOGIC:
    SEQUENCE_INTERPRETATION = CONCAT(INTERPRETATION_1, INTERPRETATION_2, ..., INTERPRETATION_N) с разделителями
    SEQUENCE_INTERPRETATION_CONFLICT_FLAG: YES / NO
    CONFLICT_DETECTION:
      IF EPOCH_AMBIGUITY = YES → SEQUENCE_INTERPRETATION_CONFLICT_FLAG = YES (конфликтующие эпохи)
      IF INTERPRETATION_1..N содержат семантически конфликтующие смыслы → SEQUENCE_INTERPRETATION_CONFLICT_FLAG = YES
      ELSE → SEQUENCE_INTERPRETATION_CONFLICT_FLAG = NO
    SEQUENCE_INTERPRETATION_SUMMARY = SUMMARY(INTERPRETATION_1..N) (опционально, если SEQUENCE_POLICY.ENABLE_SUMMARY = YES)
  SOURCE_INTERPRETATION_LIST_LIMIT:
    MAX_OUTPUT_SIZE: определяется SEQUENCE_POLICY.MAX_OUTPUT_SIZE (DEFAULT: 64KB)
    IF SOURCE_INTERPRETATION_LIST exceeds limit:
      preserve hashes/references to source interpretations
      add OUTPUT_WARNING = SOURCE_INTERPRETATION_LIST_TRUNCATED_WITH_REFERENCES
    FORMULA: TRUNCATED_REFERENCE_LIST ≠ SEMANTIC_SUMMARY
  SUMMARY_LIMIT:
    SEQUENCE_SUMMARY ≠ NEW_SEMANTIC_INTERPRETATION
    SEQUENCE_SUMMARY ≠ FINAL_VERDICT
    SOURCE_INTERPRETATION_LIST: неизменённый список INTERPRETATION_1..N
  NOTE: SEQUENCE_MODULE не создаёт новую семантику — только агрегирует существующую
  NOTE: SEQUENCE_INTERPRETATION_CONFLICT_FLAG помечает конфликт, не разрешает его

STAGE_6: SEQUENCE_OUTPUT_ASSEMBLY
  INPUT: все результаты STAGE_1–5
  ACTION: сборка финального SEQUENCE_OUTPUT, включая финальный расчёт SEQUENCE_AMBIGUITY
  SEQUENCE_AMBIGUITY_COMPUTATION (финальный):
    SEQUENCE_AMBIGUITY = YES если (EPOCH_AMBIGUITY = YES) ИЛИ (ELEMENT_AMBIGUITY = YES) ИЛИ (SEQUENCE_INTERPRETATION_CONFLICT_FLAG = YES)
    SEQUENCE_AMBIGUITY = NO если все три флага = NO
  CHECK_1: SEQUENCE_RISK_LEVEL определён
  CHECK_2: SEQUENCE_INTERPRETATION не пуста
  CHECK_3: EPOCH_SEQUENCE_CONTEXT не пуст
  CHECK_4: SEQUENCE_LIMITATION_NOTE присутствует
  CHECK_5: SEQUENCE_INTERPRETATION_CONFLICT_FLAG определён (YES / NO)
  CHECK_6: SEQUENCE_AMBIGUITY определён (YES / NO)
  CHECK_7: SOURCE_INTERPRETATION_LIST присутствует (или ссылки при truncation)
  CHECK_8 (PATCH_NOTE v0_1_PATCH_26): SEQUENCE_CANDIDATE_MATCH
    определён (один из: структура с CANDIDATE_ID, MULTIPLE_MATCHES,
    NOT_APPLICABLE, NO_MATCH, CHECK_UNAVAILABLE)
  CHECK_9 (PATCH_NOTE v0_1_PATCH_26): SOURCE_SIGN_LIST присутствует
    и его длина равна SEQUENCE_LENGTH
  CHECK_10 (PATCH_NOTE v0_1_PATCH_26): SOURCE_OCCURRENCE_LIST
    присутствует (значение NOT_AVAILABLE допустимо)
  RETURN: SEQUENCE_OUTPUT или SEQUENCE_ERROR_STATUS
  NOTE: STAGE_6 не изменяет индивидуальные INTERPRETATION — только собирает агрегированный OUTPUT

STAGE_7: FINALIZATION_CLEANUP_BEFORE_SESSION_CLOSE
  INPUT: SEQUENCE_OUTPUT или SEQUENCE_ERROR_STATUS (собран в STAGE_6)
  ACTION: проверка отсутствия остатков (AFTER_RUN_RESIDUE: FORBIDDEN)
  CHECK_1: временные данные очищены
  CHECK_2: SEQUENCE_INPUT не кэшируется между сессиями (SESSION_ONLY)
  CHECK_3: SEQUENCE_ELEMENT_MAP очищен
  CHECK_4: SEQUENCE_POLICY не кэшируется между сессиями (SESSION_ONLY)
  OUTPUT: CLEANUP_CONFIRMATION
  NOTE: STAGE_7 выполняется после сборки OUTPUT, но перед закрытием сессии
  NOTE: STAGE_7 не изменяет SEQUENCE_OUTPUT
  NOTE: STAGE_7 не влияет на результат, возвращённый в STAGE_6

## 4. SEQUENCE_AGGREGATION_MODEL

SEQUENCE_AGGREGATION_MODEL:
  PURPOSE: определение алгоритмов агрегации для разных типов последовательностей

  RISK_AGGREGATION:
    DEFAULT: MAX_RISK
    ALTERNATIVES:
      SUM_RISK: суммирование числовых значений риска (требует RISK_NUMERIC_MAP)
      WEIGHTED_RISK: взвешенное суммирование (требует WEIGHT_MAP и POSITION_WEIGHTS)
      CUMULATIVE_RISK: накопительный риск (каждый следующий знак увеличивает риск)
    CONFIGURATION: SEQUENCE_POLICY.AGGREGATION_MODE

  INTERPRETATION_AGGREGATION:
    DEFAULT: CONCATENATION
    ALTERNATIVES:
      SUMMARY: краткое резюме (требует SUMMARY_ALGORITHM)
      KEYWORD_EXTRACTION: извлечение ключевых слов
    CONFIGURATION: SEQUENCE_POLICY.INTERPRETATION_MODE

  EPOCH_AGGREGATION:
    DEFAULT: LIST_ALL
    ALTERNATIVES:
      DOMINANT_EPOCH: наиболее частая эпоха
      LATEST_EPOCH: эпоха последнего знака
    CONFIGURATION: SEQUENCE_POLICY.EPOCH_MODE

  AMBIGUITY_AGGREGATION:
    DEFAULT: OR_LOGIC (YES если хотя бы один элемент имеет AMBIGUITY_FLAG = YES)
    ALTERNATIVES:
      AND_LOGIC (YES только если все элементы имеют AMBIGUITY_FLAG = YES)
      THRESHOLD_LOGIC (YES если > N элементов имеют AMBIGUITY_FLAG = YES)
    CONFIGURATION: SEQUENCE_POLICY.AMBIGUITY_MODE
    NOTE: ELEMENT_AMBIGUITY вычисляется в STAGE_4 как промежуточный флаг
    NOTE: SEQUENCE_AMBIGUITY (финальный) = OR(EPOCH_AMBIGUITY, ELEMENT_AMBIGUITY, SEQUENCE_INTERPRETATION_CONFLICT_FLAG) — вычисляется в STAGE_6

  ZONE_AGGREGATION:
    DEFAULT: MAX_ZONE
    ALTERNATIVES: NONE (ZONE всегда максимальная)
    CONFIGURATION: FIXED

  SEQUENCE_POLICY:
    ABSTRACT: SEQUENCE_POLICY определяет параметры агрегации
    STRUCTURE:
      MAX_SEQUENCE_LENGTH: максимальное количество знаков (DEFAULT: 10)
      MAX_OUTPUT_SIZE: максимальный размер SOURCE_INTERPRETATION_LIST (DEFAULT: 64KB)
      AGGREGATION_MODE: MAX / SUM / WEIGHTED / CUMULATIVE
      INTERPRETATION_MODE: CONCAT / SUMMARY / KEYWORDS
      EPOCH_MODE: LIST_ALL / DOMINANT / LATEST
      AMBIGUITY_MODE: OR / AND / THRESHOLD
      ENABLE_SUMMARY: YES / NO
      WEIGHT_MAP: {POSITION: WEIGHT} (опционально)
      DEFAULT_WEIGHT: 0 (для непокрытых позиций)
      RISK_NUMERIC_MAP: {RISK_LEVEL: NUMERIC_VALUE} (опционально)
      CUMULATIVE_RULES: {THRESHOLD, INCREMENT} (опционально)
      SOURCE_CONTEXT_MODE: STRICT_SAME_TEXT / SAME_THREAD_WINDOW / SAME_SESSION_WINDOW (DEFAULT: STRICT_SAME_TEXT)
      THREAD_MODE: YES / NO (разрешить SAME_THREAD_WINDOW)
      SESSION_MODE: YES / NO (разрешить SAME_SESSION_WINDOW)
    SEQUENCE_POLICY_VALIDATION:
      RULE_1: если AGGREGATION_MODE = SUM → требуется RISK_NUMERIC_MAP
      RULE_2: если AGGREGATION_MODE = WEIGHTED → требуется WEIGHT_MAP и RISK_NUMERIC_MAP
      RULE_3: если AGGREGATION_MODE = CUMULATIVE → требуется CUMULATIVE_RULES
      RULE_4: если AGGREGATION_MODE = MAX → дополнительные карты не требуются
      RULE_5: если требуемая карта отсутствует → ERROR_TYPE = SEQUENCE_POLICY_INVALID
      RULE_6: если SOURCE_CONTEXT_MODE = SAME_THREAD_WINDOW → THREAD_MODE = YES обязателен
      RULE_7: если SOURCE_CONTEXT_MODE = SAME_SESSION_WINDOW → SESSION_MODE = YES обязателен
    NOTE: SEQUENCE_POLICY не определяется SEQUENCE_MODULE_TEMPLATE — загружается при инициализации
    NOTE: SEQUENCE_POLICY валидируется при загрузке (STAGE_1 CHECK_0), не при каждой агрегации

## 5. CONFIGURATION_INTERFACE

SEQUENCE_CONFIGURATION_INTERFACE:
  SEQUENCE_POLICY_PATH: путь к файлу политики последовательности
  SEQUENCE_POLICY_REGISTRY: абстрактный реестр SEQUENCE_POLICY
  SIGN_CARD_REGISTRY: абстрактный реестр SIGN_CORE_CARD
    (PATCH_NOTE v0_1_PATCH_26) — REQUIRED для работы STAGE_2a
    (SEQUENCE_CANDIDATE_CROSS_CARD_CHECK). До этого патча
    зависимость от CARD_REGISTRY существовала неявно внутри
    STAGE_2a (введена PATCH_24), но не была формально объявлена
    здесь — разработчик, читающий только CONFIGURATION_INTERFACE,
    мог не заметить эту зависимость. Тот же реестр, что
    используется MODULE_TEMPLATE STAGE_1 (CARD_LOADING) — не
    отдельная инфраструктура.
  DEFAULT_PARAMETERS:
    DEFAULT_MAX_SEQUENCE_LENGTH: 10
    DEFAULT_MAX_OUTPUT_SIZE: 64KB
    DEFAULT_AGGREGATION_MODE: MAX
    DEFAULT_INTERPRETATION_MODE: CONCAT
    DEFAULT_EPOCH_MODE: LIST_ALL
    DEFAULT_AMBIGUITY_MODE: OR
    DEFAULT_ENABLE_SUMMARY: NO

  SEQUENCE_LOGGING_INTERFACE:
    LOG_FORMAT: структурированный лог (JSON)
    FIELDS:
      SEQUENCE_TIMESTAMP: временная метка события
      SESSION_ID: идентификатор сессии
      SEQUENCE_MODULE_UID: идентификатор экземпляра SEQUENCE_MODULE
      SOURCE_SEQUENCE_LENGTH: длина входной последовательности
      SEQUENCE_RISK_LEVEL_AGGREGATED: агрегированный риск
      EPOCH_SEQUENCE_CONTEXT: контекст эпох
      AGGREGATION_MODE_APPLIED: применённый режим агрегации
      SEQUENCE_POLICY_VERSION: версия применённой SEQUENCE_POLICY
    POLICY: логирование согласно audit policy SEQUENCE_OWNER; persistent logging не требуется SEQUENCE_MODULE_TEMPLATE
    LIMITATION: если AFTER_RUN_RESIDUE: FORBIDDEN — логи не сохраняются между сессиями

  SEQUENCE_HARDENING_RULES:
    RULE_1: SEQUENCE_MODULE не может работать без загруженной SEQUENCE_POLICY
    RULE_2: SEQUENCE_MODULE не может обрабатывать SEQUENCE_INPUT с EFFECT_FIELDS_STATUS = INVALID (для OUTPUT_STATUS)
    RULE_3: SEQUENCE_MODULE должен проверять совместимость SEQUENCE_POLICY с SEQUENCE_MODULE_TEMPLATE версией
    RULE_4: SEQUENCE_MODULE не может изменять INTERPRETATION отдельных элементов
    RULE_5: SEQUENCE_MODULE не кэширует SEQUENCE_INPUT между сессиями (SESSION_ONLY)
    RULE_6: SEQUENCE_MODULE не может вынести FINAL_VERDICT — только SEQUENCE_OUTPUT
    RULE_7: SEQUENCE_MODULE не может игнорировать элементы с AMBIGUITY_FLAG = YES — они участвуют в агрегации
    RULE_8: SEQUENCE_MODULE не может добавлять элементы в SEQUENCE_INPUT — только агрегирует заданные

## 6. ADVERSARIAL_COVERAGE

ADVERSARIAL_COVERAGE:
  MIN_TOTAL_VECTORS: 12 (6 categories A-F, 2 per category)

  CATEGORY_A: SEQUENCE_INPUT_MANIPULATION (2)
    A1: Подмена SEQUENCE_INPUT — добавление/удаление элементов без валидации
    A2: Повреждённый элемент в SEQUENCE_INPUT — EFFECT_FIELDS_STATUS = INVALID для одного элемента

  CATEGORY_B: AGGREGATION_BYPASS (2)
    B1: AGGREGATION_MODE подменён — SEQUENCE_POLICY содержит недопустимый режим
    B2: WEIGHT_MAP манипулирован — веса приводят к занижению SEQUENCE_RISK_LEVEL

  CATEGORY_C: EPOCH_SEQUENCE_EXPLOIT (3)
    C1: EPOCH_SEQUENCE_CONTEXT подменён — ACTIVE_EPOCH изменены для снижения риска
    C2: DOMINANT_EPOCH манипуляция — выбор эпохи, минимизирующий SEQUENCE_RISK_LEVEL
    C3: EPOCH_NOT_APPLICABLE_INJECTION — внедрение NOT_APPLICABLE для снижения EPOCH_AMBIGUITY (обход EPOCH_SEQUENCE_COUNT)

  CATEGORY_D: SEQUENCE_LENGTH_ATTACK (2)
    D1: OVERSIZED_SEQUENCE — SEQUENCE_INPUT превышает MAX_SEQUENCE_LENGTH
    D2: EMPTY_SEQUENCE_INJECTION — пустая последовательность передана как валидная

  CATEGORY_E: BOUNDARY_VIOLATION (2)
    E1: SEQUENCE_MODULE изменил INTERPRETATION отдельного элемента — нарушение PRINCIPLE_5
    E2: SEQUENCE_MODULE вынес FINAL_VERDICT — нарушение PRINCIPLE_6

  CATEGORY_F: SESSION_LEAK (2)
    F1: SEQUENCE_INPUT кэширована между сессиями — нарушение RULE_5
    F2: SEQUENCE_OUTPUT одной сессии передана в другую без переинициализации

  ACTUAL_TOTAL_VECTORS: 13
  COVERAGE_STATUS: SUFFICIENT (13 ≥ 12)

## 7. MUTATION_CHECK

MUTATION_CHECK:
  MUTATION_01:
    CLAIM: SEQUENCE_MODULE может работать без SEQUENCE_POLICY
    EXPECTED: FAIL — RULE_1: SEQUENCE_POLICY обязательна
    RESULT: FAIL

  MUTATION_02:
    CLAIM: SEQUENCE_MODULE может принять SEQUENCE_INPUT с EFFECT_FIELDS_STATUS = INVALID
    EXPECTED: FAIL — RULE_2: INVALID элемент → SEQUENCE_ERROR_STATUS
    RESULT: FAIL

  MUTATION_03:
    CLAIM: SEQUENCE_MODULE может изменить INTERPRETATION отдельного элемента
    EXPECTED: FAIL — PRINCIPLE_5: INTERPRETATION не изменяется
    RESULT: FAIL

  MUTATION_04:
    CLAIM: SEQUENCE_MODULE может кэшировать SEQUENCE_INPUT между сессиями
    EXPECTED: FAIL — RULE_5: SESSION_ONLY
    RESULT: FAIL

  MUTATION_05:
    CLAIM: SEQUENCE_MODULE может вынести FINAL_VERDICT
    EXPECTED: FAIL — PRINCIPLE_6: только SEQUENCE_OUTPUT
    RESULT: FAIL

  MUTATION_06:
    CLAIM: SEQUENCE_MODULE может игнорировать элементы с AMBIGUITY_FLAG = YES
    EXPECTED: FAIL — RULE_7: все элементы участвуют в агрегации
    RESULT: FAIL

## 8. KNOWN_OPEN_QUESTIONS

KNOWN_OPEN_QUESTIONS:
  QUESTION_1:
    QUESTION: Как SEQUENCE_MODULE должен обрабатывать вложенные последовательности (sequence внутри sequence)?
    STATUS: CLOSED_AS_DELEGATED_TO_SEQUENCE_INTEGRATOR
    BLOCKS_WORKINGLY_CLOSED: NO
    NOTE: SEQUENCE_MODULE_TEMPLATE описывает плоскую последовательность. Вложенность — задача SEQUENCE_INTEGRATOR или рекурсивного SEQUENCE_MODULE_INSTANCE.

  QUESTION_2:
    QUESTION: Должен ли SEQUENCE_MODULE поддерживать real-time потоковую обработку (знаки приходят по одному, не пакетом)?
    STATUS: CLOSED_AS_DELEGATED_TO_RUNTIME
    BLOCKS_WORKINGLY_CLOSED: NO
    NOTE: SEQUENCE_MODULE_TEMPLATE описывает пакетную обработку. Real-time streaming — задача SEQUENCE_INTEGRATOR или runtime.

  QUESTION_3:
    QUESTION: Как SEQUENCE_MODULE должен обрабатывать частично перекрывающиеся последовательности (sliding window)?
    STATUS: CLOSED_AS_DELEGATED_TO_SEQUENCE_INTEGRATOR
    BLOCKS_WORKINGLY_CLOSED: NO
    NOTE: SEQUENCE_MODULE_TEMPLATE описывает дискретную последовательность. Sliding window — задача SEQUENCE_INTEGRATOR или runtime.

  QUESTION_4:
    QUESTION: Является ли SEQUENCE_INTEGRATOR_TEMPLATE отдельным документом или это INTEGRATOR_TEMPLATE со специализированной SEQUENCE_POLICY?
    STATUS: CLOSED_BY_AUTHOR_DECISION_20260619_008
    BLOCKS_WORKINGLY_CLOSED: NO
    NOTE: Решено — SEQUENCE_INTEGRATOR_TEMPLATE является отдельным документом, не вариантом INTEGRATOR_TEMPLATE. Подтверждено созданием SEQUENCE_INTEGRATOR_TEMPLATE_GEN3_v0_2_PLUS_EPOCH_v0_1A как самостоятельного артефакта. Это исправляет более раннюю формулировку этого вопроса в данном файле, которая предполагала противоположное решение ("отдельный шаблон не создаётся") — та формулировка была преждевременной и не отражает фактическое архитектурное развитие проекта.

  QUESTION_5 (PATCH_NOTE v0_1_PATCH_24, ЗАКРЫТ v0_1_PATCH_26):
    QUESTION: Как SEQUENCE_MODULE должен обрабатывать cross-card
      sequence candidates — последовательности, состоящие из
      знаков РАЗНЫХ карточек (например, DOT+SOLIDUS на "../")?
    STATUS: CLOSED_BY_PATCH_26
    РЕШЕНИЕ: STAGE_2a обобщён из SEQUENCE_CANDIDATE_SAME_CARD_CHECK
      в SEQUENCE_CANDIDATE_CROSS_CARD_CHECK — same-card теперь
      частный случай (CARD_SET из одной карты). Подтверждено по
      тексту карточки SOLIDUS: SC3.SEQUENCE буквально равно "../",
      то есть сама карточка SOLIDUS описывает межкарточную
      последовательность DOT+DOT+SOLIDUS как свой кандидат — это
      и было содержательным основанием для обобщения, не
      гипотетическим расширением. ТРЕБУЕТ ОТДЕЛЬНОЙ ВЕРИФИКАЦИИ
      конвейером перед тем, как считаться полностью подтверждённым
      на практике (см. CONVEYOR_RUN_PACKET_SEQUENCE_TECH_DEBT_
      CLOSURE_v0_1).

  QUESTION_5A (НОВЫЙ, PATCH_NOTE v0_1_PATCH_26 — частично открытый
    остаток QUESTION_5, не закрывается на уровне SEQUENCE_MODULE):
    QUESTION: SOLIDUS.SC7 ("://", COLON_DOUBLE_SOLIDUS) остаётся
      недостижимым даже после обобщения STAGE_2a в cross-card,
      потому что ":" (COLON) физически отсутствует как элемент
      SEQUENCE_INPUT — upstream-парсер (система, формирующая
      список MODULE_RESULT из исходного текста) не передаёт
      пунктуационные/служебные знаки как отдельные MODULE_RESULT
      в текущих тестовых сценариях. Это ограничение НЕ может быть
      закрыто на уровне SEQUENCE_MODULE_TEMPLATE — ответственность
      лежит на upstream-системе разбора текста, вне рамок этого
      документа.
    STATUS: OPEN — CLOSED_AS_OUT_OF_SCOPE_FOR_THIS_DOCUMENT
    BLOCKS_WORKINGLY_CLOSED: NO
    NOTE: это честно зафиксированный остаточный пробел, не скрытый
      и не выданный за решённый. Если в будущем понадобится
      гарантированно покрывать такие кандидаты — нужно либо (а)
      обеспечить, чтобы upstream-парсер создавал MODULE_RESULT для
      ВСЕХ знаков в тексте, включая пунктуацию, либо (б) ввести
      отдельный механизм "частичного буквенного совпадения" с
      учётом недостающих промежуточных знаков — последнее
      потенциально опасно (риск ложных совпадений) и не
      рекомендуется без отдельной архитектурной проработки.

  QUESTION_6 (PATCH_NOTE v0_1_PATCH_25, ПРЕДЛОЖЕНО К ЗАКРЫТИЮ
    v0_1_PATCH_27):
    QUESTION: SOURCE_OCCURRENCE_LIST в OUTPUT_INTERFACE
      зафиксирован как NOT_AVAILABLE, потому что OUTPUT_STATUS
      одиночного MODULE_TEMPLATE не возвращает SIGN_OFFSET. Нужно
      ли добавлять SIGN_OFFSET_START/END в OUTPUT_STATUS
      одиночного MODULE_TEMPLATE (отдельный патч ДРУГОГО,
      WORKINGLY_CLOSED документа), чтобы SOURCE_OCCURRENCE_LIST
      стал реальным массивом, а не заглушкой?
    STATUS: PENDING_VERIFICATION (PATCH_27 предложен для
      MODULE_TEMPLATE, требует отдельного конвейерного
      подтверждения, прежде чем SOURCE_OCCURRENCE_LIST в этом
      документе сможет перестать быть NOT_AVAILABLE)
    BLOCKS_WORKINGLY_CLOSED: NO (текущая логика SEQUENCE_INTEGRATOR
      STAGE_2/STAGE_3 не зависит от offset — использует только
      порядок SOURCE_SIGN_LIST; NOT_AVAILABLE остаётся корректным
      значением до подтверждения PATCH_27)
    NOTE: решение закрыть этот вопрос принято автором 2026-06-26
      ("не хочу, чтобы дыры лезли через год") — приоритет поднят
      с низкого до текущего по прямому указанию, не по
      технической необходимости (текущая логика и так работает с
      NOT_AVAILABLE).

  ALL_OPEN_QUESTIONS_CLOSED: YES (QUESTION_5 закрыт PATCH_26;
    QUESTION_5A зафиксирован как OUT_OF_SCOPE_FOR_THIS_DOCUMENT —
    не блокирует WORKINGLY_CLOSED, но не выдаётся за решённый;
    QUESTION_6 — см. ниже, статус зависит от применения PATCH_27
    к MODULE_TEMPLATE)

## 9. LIMITATION_STATEMENT

LIMITATION_STATEMENT:
  SEQUENCE_MODULE_TEMPLATE:
    IS_NOT: runtime
    IS_NOT: parser
    IS_NOT: final_verdict_system
    IS_NOT: policy_enforcer
    IS_NOT: semantic_interpreter
    IS_NOT: production_ready_without_runtime_policy
    IS_NOT: validator
    IS_NOT: certification
    IS_NOT: locked_working_core
    IS: working_draft_artifact
    IS: template_for_sequence_module_instance
    IS: aggregator
    IS: passthrough_for_individual_semantics
    IS: session_only
    IS: epoch_aware

  FORMULAS:
    CONVEYOR_PASS ≠ VALIDATION
    MODEL_CONSENSUS ≠ TRUTH
    REVIEWED ≠ VALIDATED
    WORKING_DRAFT ≠ WORKINGLY_CLOSED
    WORKINGLY_CLOSED ≠ LOCKED_WORKING_CORE
    SEQUENCE_AGGREGATION ≠ NEW_SEMANTIC_INTERPRETATION
    SEQUENCE_OUTPUT ≠ FINAL_VERDICT
    SEQUENCE_MODULE_TEMPLATE ≠ INTEGRATOR_TEMPLATE
    SEQUENCE_MODULE_TEMPLATE ≠ RUNTIME
    SEQUENCE_SUMMARY ≠ NEW_SEMANTIC_INTERPRETATION
    SEQUENCE_SUMMARY ≠ FINAL_VERDICT

  SEQUENCE_MODULE_LIMITATION:
    SEQUENCE_MODULE_TEMPLATE описывает шаблон агрегации, не конкретный алгоритм.
    Конкретные алгоритмы агрегации (SUM, WEIGHTED, CUMULATIVE) определяются SEQUENCE_POLICY.
    SEQUENCE_MODULE_TEMPLATE не гарантирует оптимальность агрегации для всех типов текстов.
    SEQUENCE_MODULE_TEMPLATE не обрабатывает вложенные или потоковые последовательности.
    SEQUENCE_MODULE_TEMPLATE не определяет MAX_SEQUENCE_LENGTH — это параметр SEQUENCE_POLICY.
    SEQUENCE_MODULE_TEMPLATE не является заменой human review для сложных случаев.

  AFTER_RUN_RESIDUE: FORBIDDEN
  SESSION_ONLY: YES
  SEQUENCE_POLICY_DEPENDENCY: YES
  HUMAN_REVIEW_REQUIRED_FOR: сложные случаи агрегации, не покрытые SEQUENCE_POLICY

## 10. INTEGRATION_INTERFACE_STATUS

INTEGRATION_INTERFACE_STATUS:
  STATUS: READY_PENDING_CONCRETE_SEQUENCE_POLICY
  ATTACHED_SEQUENCE_POLICY: NONE_CURRENTLY_ATTACHED
  ATTACHED_SEQUENCE_INTEGRATOR_UID: NONE_CURRENTLY_ATTACHED
  ACTIVE_INSTANCES_COUNT: 0
  SEQUENCE_POLICY_ATTACHMENT: NONE
  PERMANENT_BINDING: NO
  SESSION_ONLY_BINDING: YES
  NEXT_TEMPLATE_IN_CHAIN: INTEGRATOR_TEMPLATE (или SEQUENCE_INTEGRATOR_TEMPLATE, см. OQ4)
  BOUNDARY: SEQUENCE_MODULE_TEMPLATE ≠ INTEGRATOR_TEMPLATE
  BOUNDARY: SEQUENCE_MODULE_TEMPLATE может передавать SEQUENCE_OUTPUT в SEQUENCE_INTEGRATOR_TEMPLATE (если есть)

## 11. PATCH_HISTORY

PATCH_HISTORY:
  v0_1_PATCH_01: AUTHOR — Initial draft creation — TYPE_I (initial)
  v0_1_PATCH_02: NOT_APPLICABLE excluded from EPOCH_SEQUENCE_UNIQUE — TYPE_F (fix-patch)
  v0_1_PATCH_03: SEQUENCE_INTERPRETATION_CONFLICT_FLAG + SUMMARY_LIMIT added — TYPE_F (fix-patch)
  v0_1_PATCH_04: UNDER_MIN_LENGTH_SEQUENCE error type added — TYPE_F (fix-patch)
  v0_1_PATCH_05: MODULE_ERROR_IN_SEQUENCE propagation added — TYPE_F (fix-patch)
  v0_1_PATCH_06: DEFAULT_WEIGHT = 0 for uncovered positions — TYPE_F (fix-patch)
  v0_1_PATCH_07: STAGE_6 split into STAGE_6 (ASSEMBLY) + STAGE_7 (CLEANUP) — TYPE_F (fix-patch)
  v0_1_PATCH_08: COMMON_CONVEYOR_DISCIPLINE added to header — TYPE_P (content-patch)
  v0_1_PATCH_09: OQ1-OQ3 closed as DELEGATED — TYPE_F (fix-patch)
  v0_1_PATCH_10: SEQUENCE_POLICY_VALIDATION rules added to STAGE_1 CHECK_0 — TYPE_P (content-patch)
  v0_1_PATCH_11: C3 NOT_APPLICABLE_INJECTION adversarial vector added — TYPE_P (content-patch)
  v0_1_PATCH_12: SOURCE_CONTEXT_MODE definition and CHECK_4 logic added — TYPE_P (content-patch)
  v0_1_PATCH_13: CHECK_6 ALL_ELEMENTS_ERROR added to STAGE_1 and ERROR_INTERFACE — TYPE_F (fix-patch)
  v0_1_PATCH_14: CHECK_3 and CHECK_5 restricted to OUTPUT_STATUS only; ERROR_STATUS skip documented — TYPE_F (fix-patch)
  v0_1_PATCH_15: STAGE_7 renamed to FINALIZATION_CLEANUP_BEFORE_SESSION_CLOSE; NOTE updated — TYPE_F (fix-patch)
  v0_1_PATCH_16: RESULT: FAIL added to all 6 MUTATION_CHECK entries — TYPE_N (clarification-patch)
  v0_1_PATCH_17: SOURCE_INTERPRETATION_LIST_LIMIT added to STAGE_5 — TYPE_P (content-patch)
  v0_1_PATCH_18: ATTACHED_SEQUENCE_INTEGRATOR_UID added to INTEGRATION_INTERFACE_STATUS — TYPE_P (content-patch)
  v0_1_PATCH_19: SEQUENCE_MODULE_UID added to META — TYPE_P (content-patch)
  v0_1_PATCH_20: CHECK_3 fixed for ERROR_STATUS skip in INPUT_INTERFACE — TYPE_F (fix-patch)
  v0_1_PATCH_21: MAJ-N1 fix — SEQUENCE_AMBIGUITY moved from STAGE_4 to STAGE_6; STAGE_4 computes intermediate flags only (EPOCH_AMBIGUITY, ELEMENT_AMBIGUITY); STAGE_6 computes final SEQUENCE_AMBIGUITY = OR(EPOCH, ELEMENT, CONFLICT) — TYPE_F (fix-patch)
  v0_1_PATCH_22: OQ4 added (SEQUENCE_INTEGRATOR_TEMPLATE architectural decision pending); NEXT_TEMPLATE_IN_CHAIN updated with reference to OQ4 — TYPE_P (content-patch)
  v0_1_PATCH_23: Final pre-close synchronization — OQ4 closed as AUTHOR_DECISION_DEFERRED; INTEGRATION_CHAIN input changed from OUTPUT_STATUS list to MODULE_RESULT list with routing rules; ERROR_PRECEDENCE added for ALL_ELEMENTS_ERROR vs MODULE_ERROR_IN_SEQUENCE — TYPE_F (fix-patch)
  v0_1_PATCH_24: SAME_CARD_SEQUENCE_CANDIDATE_BRIDGE — добавлен
    STAGE_2a (SEQUENCE_CANDIDATE_SAME_CARD_CHECK) с восстановлением
    SEQUENCE_CONTEXT_TEXT и явным ORDERING_INVARIANT; STAGE_3
    дополнен RULE_3A (ENUM_GUARD — защита MAX() от не-перечислимых
    значений RISK_LEVEL типа "intensity-dependent"); OUTPUT_INTERFACE
    дополнен полем SEQUENCE_CANDIDATE_MATCH; KNOWN_OPEN_QUESTIONS
    дополнен QUESTION_5 (cross-card, осознанно отложено). Закрывает
    ARCHITECTURE_BUG, найденный CONVEYOR_RUN_PACKET_SEQUENCE_
    PIPELINE_FIRST_RUN_v0_1 (5/5 прогонов, 2026-06-25):
    SEQUENCE_CANDIDATE.RISK_LEVEL карточек физически не достигал
    pipeline. Направление утверждено AUTHOR_DECISION_20260625_004
    (Вариант А, сокращённый объём — только same-card). Текст патча
    прошёл ДВА раунда конвейерной верификации ДО применения (по
    уроку предыдущего эпизода PATCH_23 к MODULE_TEMPLATE — патч
    написан, проверен, исправлен по находкам, проверен повторно,
    только потом применён):
      РАУНД 1 (CONVEYOR_RUN_PACKET_..._VERIFICATION_v0_1,
        2026-06-25): найдены 2 блокирующих дефекта в черновике —
        (а) STAGE_2a не определял источник SEQUENCE_CONTEXT_TEXT
        (найдено Qwen, подтверждено координатором прямой
        проверкой INPUT_INTERFACE), (б) RULE_3A пытался MAX(NONE,
        "intensity-dependent") — неопределённая операция, найдено
        Kimi/GPT-5.5/Qwen/Gemini (4/6 ответов), подтверждено
        координатором прямой проверкой карточки SKULL.SC1.
      РАУНД 2 (CONVEYOR_RUN_PACKET_..._VERIFICATION_v0_2,
        2026-06-26): оба дефекта подтверждены закрытыми (5/5:
        Kimi, GPT-5.5×2, Qwen, Gemini — APPROVE_FOR_APPLICATION
        или APPROVE_WITH_CHANGES без блокирующих находок). Найдена
        дополнительная неточность тестового сценария (не текста
        патча): "//" совпадает с SOLIDUS.SC1, не с заявленным SC7
        — оба HIGH в данной карточке, цель теста достигнута, но
        через другой кандидат; это подтвердило более широкую
        LIMITATION (см. STAGE_2a) — кандидаты с буквами/знаками
        других кодпоинтов в SEQUENCE недостижимы same-card
        механизмом в принципе, не только для конкретного "://".
    TYPE: TYPE_P (content-patch, меняет логику STAGE_2/STAGE_3)
  v0_1_PATCH_25: TEMPLATE_TO_TEMPLATE_INTERFACE_GAP CLOSURE —
    добавлены поля SOURCE_SIGN_LIST (реальные данные, из
    SIGN_CODEPOINT) и SOURCE_OCCURRENCE_LIST (NOT_AVAILABLE,
    честная заглушка) в OUTPUT_INTERFACE; добавлен OQ6 про
    будущий SIGN_OFFSET follow-up. Закрывает находку, поднятую
    одним из шести ответов раунда SEQUENCE_PIPELINE_SECOND_RUN
    (GPT-5.5, 2026-06-26) — SEQUENCE_INTEGRATOR_TEMPLATE требует
    эти два поля как mandatory в INPUT_INTERFACE, а
    SEQUENCE_MODULE_TEMPLATE их никогда не производил — пробел
    существовал с самого первого раунда (SEQUENCE_PIPELINE_
    FIRST_RUN), не связан с PATCH_24, пропущен пятью из шести
    предыдущих независимых прогонов. Текст патча верифицирован
    конвейером ДО применения (CONVEYOR_RUN_PACKET_SEQUENCE_
    SOURCE_LISTS_GAP_v0_1, 2026-06-26): 5 ответов (GPT-5.5×2,
    Gemini, Grok — APPROVE_FOR_APPLICATION; Kimi —
    APPROVE_WITH_CHANGES). Проверено и подтверждено явно:
    SEQUENCE_INTEGRATOR STAGE_2/STAGE_3 не использует
    SOURCE_OCCURRENCE_LIST для позиционной логики — только
    SOURCE_SIGN_LIST (порядок CODEPOINT), поэтому NOT_AVAILABLE
    не блокирует существующую логику IDIOM_RECOGNITION. Учтены
    уточнения Kimi: явный INTEGRATOR_RULE про запрет позиционной
    зависимости при NOT_AVAILABLE, явная NOTE про асимметрию
    длин двух списков (запрет parallel-array предположения).
    TYPE: TYPE_F (fix-patch, интерфейс, не меняет логику STAGE)
  v0_1_PATCH_26: CROSS_CARD_GENERALIZATION — STAGE_2a переименован
    и обобщён из SEQUENCE_CANDIDATE_SAME_CARD_CHECK в
    SEQUENCE_CANDIDATE_CROSS_CARD_CHECK. CHECK_SAME_CARD заменён
    на CARD_SET_DETERMINATION (множество уникальных кодпоинтов,
    K≥1, same-card — частный случай K=1). Поиск кандидата теперь
    идёт по объединению SEQUENCE_CANDIDATES ВСЕХ карт в CARD_SET.
    Добавлены поле CANDIDATE_SOURCE_CARD и состояние
    MULTIPLE_MATCHES. RULE_3A (STAGE_3) обновлён для обработки
    MULTIPLE_MATCHES. SIGN_CARD_REGISTRY формализован в
    CONFIGURATION_INTERFACE (CHECK_7 на STAGE_1). Добавлены
    CHECK_8/9/10 на STAGE_6 для аудита новых output-полей. По
    прямому указанию автора ("закрыть дыры сейчас") закрывает
    QUESTION_5 содержательно — найдено по тексту карточки SOLIDUS:
    SC3.SEQUENCE буквально равно "../", то есть сама карточка
    описывает межкарточную (DOT+DOT+SOLIDUS) последовательность
    как свой кандидат. Добавлен честный QUESTION_5A — остаточное
    upstream-ограничение (кандидаты типа SOLIDUS.SC7 "://"
    недостижимы, если знак ":" не передан как элемент
    SEQUENCE_INPUT — это вне рамок этого документа, не решается
    cross-card обобщением). Подтверждено новым ТЕСТ_4
    ("https://trusted.com" с урезанным input) — SC7 остаётся
    недостижимым, что доказывает честность классификации
    QUESTION_5A, не тихое замалчивание. Текст патча верифицирован
    конвейером ДО применения (CONVEYOR_RUN_PACKET_SEQUENCE_TECH_
    DEBT_CLOSURE_v0_1, 2026-06-26): 5/5 (Kimi, Gemini, GPT-5.5,
    Grok, Qwen) — APPROVE_FOR_APPLICATION единогласно. Подтверждено
    отсутствие регрессии для K=1 случаев (ТЕСТ_1, ТЕСТ_2 —
    идентичны PATCH_24/25). Подтверждено для ТЕСТ_3: HIGH теперь
    достигается через SEQUENCE_CANDIDATE (SOLIDUS.SC3, RULE_3A), а
    не только через RULE_1 MAX отдельных элементов — содержательно
    иной механизм при том же числовом результате, зафиксировано
    честно, не скрыто как "ничего не изменилось".
    TYPE: TYPE_P (content-patch, обобщает логику STAGE_2a/STAGE_3)
  PATCHES_APPLIED: 26
  PATCHES_VERIFIED: 26/26 (PATCH_26 верифицирован конвейером ДО
    применения, единогласно 5/5, по дисциплине verify-before-apply)

END_OF_DOCUMENT
