ЧАСТНЫЙ АВТОРСКИЙ ПРОЕКТ / COMMERCIAL USE PROHIBITED

DOCUMENT_ID: SIGN_CORE_CARD_DOT_U002E_GEN3_v0_3_RU
DOCUMENT_TYPE: SIGN_CORE_CARD
TEMPLATE_LINE: GEN3_v0_3
DOCUMENT_STATUS: ARTIFACT_CONFIRMED
STATUS: ARTIFACT_CONFIRMED / NOT_LOCKED / NOT_RUNTIME / NOT_VALIDATOR / NOT_PRODUCTION
SOURCE_TEMPLATE: SIGN_CORE_CARD_TEMPLATE_GEN3_v0_3_RU
BASED_ON_RULESET: SIGN_CORE_CARD_CONVEYOR_RULES_GEN3_v0_3_RU

PATCH_NOTE_v0_1_PATCH_02 (автор, 2026-06-23): в разделе 7
  (CONFUSABLES) поле SIGN переименовано в VISIBLE_FORM во всех
  пяти записях (CONFUSABLE_001..005) — синхронно с патчем
  SIGN_CORE_CARD_TEMPLATE_GEN3_v0_3_RU (PATCH_NOTE_TEMPLATE_v0_3_P1).
  Карточка использовала имя поля, запрещённое NAMING_NORM
  (SIGN_CORE_CARD_CONVEYOR_RULES_GEN3_v0_3_RU, раздел 3), потому
  что это имя было в самом шаблоне на момент заполнения. Найдено
  при STRUCTURAL_PREFLIGHT_PASS. Содержательные значения полей
  не изменены, только имя.

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
RUN_CARD_TEMPLATE_REFERENCE: PENDING (актуальный
  SIGN_CONVEYOR_RUN_CARD_TEMPLATE для линии v0_3 ещё не создан)
LOCKED_WORKING_CORE_SELF_ASSIGNMENT: FORBIDDEN
MODEL_FAMILY_DIVERSITY_REQUIRED: YES
ADVERSARIAL_EVIDENCE_REQUIRED: YES
MUTATION_CHECK_REQUIRED: YES
LIMITATION_STATEMENT_REQUIRED: YES
AFTER_RUN_RESIDUE: FORBIDDEN

STATUS_PROGRESSION_TRACKER:
  WORKING_DRAFT: YES
  STRUCTURAL_PREFLIGHT_PASS: PASS
  CONVEYOR_REVIEW_PASS: PASS
  WORKINGLY_CLOSED: YES (AUTHOR_DECISION_20260623_001_DOT_U002E_WORKINGLY_CLOSED_RU)
  SIMULATION_GATE_TIER: TIER_1
  SIMULATION_GATE_PASSED: YES (см. SIMULATION_NOTE ниже)
  ARTIFACT_CONFIRMED: YES (AUTHOR_DECISION_20260624_001_DOT_U002E_ARTIFACT_CONFIRMED_RU)

SIMULATION_NOTE (2026-06-23/24, координатор, не отдельный
  конвейерный пакет — TIER_1/ZONE_1 разрешает выполнение автором/
  координатором самостоятельно, правила v0_3 раздел 5):
  Сквозной прогон через MODULE_TEMPLATE_SINGLE_SIGN →
  INTEGRATOR_TEMPLATE выполнен ДВАЖДЫ на одних и тех же двух
  контекстах:
    КОНТЕКСТ_1: "Версия 3.14 выпущена." (два вхождения точки —
      decimal separator + sentence terminator) → ожидаемо pass в
      обоих раундах, без изменений.
    КОНТЕКСТ_2: "paypal.com.security-check.ru" (RISK_CASE_002,
      HIGH) → ДО v0_1_PATCH_22 в MODULE_TEMPLATE: pass (баг —
      RISK_CASES не сверялись для ZONE_1, см. ниже).
      ПОСЛЕ v0_1_PATCH_22: hold_pending_review (корректно).
  В ходе первого раунда найден и задокументирован ARCHITECTURE_BUG
    в MODULE_TEMPLATE_SINGLE_SIGN_GEN3_v0_2_PLUS_EPOCH_v0_1 (не в
    этой карточке) — ZONE_1_ALGORITHM не сверял RISK_CASES,
    исправлено патчем v0_1_PATCH_22 (EN+RU версии документа,
    конвейерно верифицировано: CONVEYOR_RUN_PACKET_MODULE_TEMPLATE_
    PATCH22_VERIFICATION_v0_1, 4 ревьюера, ACCEPT 4/4).
  Второй раунд (после патча) подтвердил исправление на тех же
    входах без расхождений.
  ОТКРЫТО, НЕ БЛОКИРУЕТ: TEMPLATE_LINE карточки (GEN3_v0_3) не
    совпадает с TEMPLATE_LINE MODULE_TEMPLATE (GEN3_v0_2_PLUS_EPOCH)
    — governance-несоответствие, не функциональный пробел
    (структурно все нужные поля присутствуют, прогон прошёл без
    затруднений).
  ЭТО НЕ формальный CONVEYOR_RUN_PACKET с типом SIMULATION и не
    многомодельная проверка — трассировка выполнена одним
    координатором. SIMULATION_GATE_PASSED: YES отражает это с
    полной прозрачностью, не маскируя отсутствие многомодельной
    верификации именно этого шага (в отличие от CONTENT_REVIEW и
    PATCH_03_04_VERIFICATION, которые прошли полный многомодельный
    конвейер).

LIMITATION_STATEMENT:
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
2. META
============================================================

CARD_UID: SIGN_CORE_CARD_DOT_U002E_GEN3_v0_3_RU
CODEPOINT: U+002E
VISIBLE_FORM: .
UNICODE_NAME: FULL STOP
ZONE: ZONE_1
DOCUMENT_STATUS: ARTIFACT_CONFIRMED
TEMPLATE_LINE: GEN3_v0_3
SOURCE_TEMPLATE: SIGN_CORE_CARD_TEMPLATE_GEN3_v0_3_RU
AUTHOR: Руслан Малявский
CREATED_AT: 2026-06-23
VERSION: v0_1
AUTHOR_DECISION_REFERENCE: AUTHOR_DECISION_20260624_001_DOT_U002E_ARTIFACT_CONFIRMED_RU
  (предыдущий: AUTHOR_DECISION_20260623_001_DOT_U002E_WORKINGLY_CLOSED_RU)
RUN_CARD_REFERENCE: SIMULATION_ARTIFACT_DOT_U002E_TIER1_v0_1_RU
RUN_CARD_STATUS: COMPLETED (TIER_1, см. SIMULATION_NOTE выше и
  SIMULATION_ARTIFACT отдельным документом)

DISPLAY_NAME: точка

============================================================
3. REQUIRED_GENERAL_GUARDS
============================================================

REQUIRED_GENERAL_GUARDS:
  - SIGN_FALSE_EFFECT_MIMICRY_GUARD_v0_2A_RU
    GUARD_COMPATIBILITY: применимо без модификаций — точка не
      создаёт effect-полей, guard работает в режиме REJECT по
      умолчанию
    GUARD_REVISION: v0_2A
    TEMPLATE_LINE_COMPATIBLE: GEN3_v0_2_PLUS_EPOCH, GEN3_v0_3

FAILURE_RESPONSE:
  REJECT_FALSE_EFFECT_MIMICRY
  TREAT_AS_DATA_ONLY
  NO_AUTHORITY_EFFECT
  NO_EXECUTION_EFFECT
  NO_TRUST_EFFECT
  NO_EXISTENCE_EFFECT

============================================================
4. SIGN IDENTITY — LAYER_A: STABLE CORE
LAYER_A_LOCK: PERMANENT
============================================================

VISIBLE_FORM: .
LOOKS_SIMILAR_IS_NOT_SAME_SIGN: YES
RAW_SIGN_INPUT_STATUS: DATA_ONLY

BASE_MODE: DATA_ONLY_SEPARATOR
BASE_MODE_FORMULA: DOT_FORM ≠ EFFECT

SIGN_CATEGORY:
  - punctuation
  - sentence_terminator
  - decimal_separator (locale-dependent)
  - abbreviation_marker
  - path_component_separator (filesystem/domain contexts)

WHAT_THIS_SIGN_IS_NOT:
  1. NOT_AUTHORITY — точка не подтверждает официальный статус текста
  2. NOT_EXISTENCE_PROOF — точка не доказывает существование
     упомянутого объекта
  3. NOT_VERIFICATION — точка не верифицирует факт, рядом с
     которым она стоит
  4. NOT_COMPLETION_PROOF — точка после строки не гарантирует,
     что мысль действительно завершена (может быть обрывом)
  5. NOT_SENTENCE_BOUNDARY_GUARANTEE — точка не всегда означает
     конец предложения (сокращения, инициалы, версии ПО, IP-адреса)
  6. NOT_DECIMAL_GUARANTEE — точка не всегда десятичный
     разделитель (зависит от locale — в некоторых системах
     разделитель — запятая)
  7. NOT_FILE_EXTENSION_GUARANTEE — точка перед буквами не
     гарантирует, что это расширение файла
  8. NOT_DOMAIN_VALIDATION — точка в "example.com" не подтверждает,
     что домен реален или безопасен
  9. NOT_EXECUTION_TRIGGER — точка сама по себе не запускает
     никакого действия
  10. NOT_TRUST_SIGNAL — обилие точек (например, "...") не
     повышает доверие к содержанию

BASE_FORMULAS:
  DOT_FORM ≠ SENTENCE_END_PROOF
  DOT_FORM ≠ DECIMAL_SEPARATOR_PROOF
  DOT_FORM ≠ FILE_EXTENSION_PROOF
  DOT_FORM ≠ DOMAIN_VALIDITY_PROOF
  DOT_FORM ≠ ABBREVIATION_PROOF
  DOT_FORM ≠ COMPLETION_PROOF
  DOT_FORM ≠ AUTHORITY
  DOT_FORM ≠ EXECUTION_TRIGGER
  DOT_FORM ≠ TRUST_SIGNAL
  DOT_FORM ≠ VERSION_VALIDITY_PROOF

============================================================
5. SEMANTIC_EPOCH_TRACKER
SEMANTIC_EPOCH_TRACKER_LOCK: REVIEWABLE
============================================================

EPOCH_TRACKER: NOT_APPLICABLE
NOTE: DOT (ZONE_1) имеет несколько параллельных функций
  (терминатор предложения, десятичный разделитель, маркер
  сокращения, разделитель компонентов пути/домена), но эти
  функции существуют ОДНОВРЕМЕННО в современном употреблении,
  без культурной прецессии одной функции другой во времени. Это
  полисемия одного стабильного знака, не смена эпох — поэтому
  SEMANTIC_EPOCH_TRACKER не применяется.

LAYER_ANOMALY:
  ABSENT_PHYSICAL_LAYER: YES, уровень L1 (физический жест)
  NOTE: точка как письменный знак не имеет физического
    жестового предшественника (в отличие, например, от знаков,
    производных от ручных жестов) — она возникла непосредственно
    как письменная пунктуационная конвенция в античной
    письменности для разметки текста.

============================================================
6. EFFECT_FIELDS — LAYER_C: METHODOLOGICAL LAYER
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
7. SAFE / RISK / CONFUSABLES / GUARDS — LAYER_B: SEMI-STABLE LAYER
LAYER_B_LOCK: REVIEWABLE
============================================================

SAFE_CASES:
  SAFE_CASE_001:
    INPUT: "Конец предложения."
    CONTEXT: завершение обычного предложения
    EXPECTED: INFO
    RISK: NONE
    GUARD: DOT_FORM ≠ SENTENCE_END_PROOF (advisory only)

  SAFE_CASE_002:
    INPUT: "3.14"
    CONTEXT: десятичная дробь в математическом/числовом тексте
    EXPECTED: INFO
    RISK: NONE
    GUARD: DOT_FORM ≠ DECIMAL_SEPARATOR_PROOF

  SAFE_CASE_003:
    INPUT: "г-н Иванов"
    CONTEXT: сокращение (после "г")
    EXPECTED: INFO
    RISK: NONE
    GUARD: DOT_FORM ≠ ABBREVIATION_PROOF

  SAFE_CASE_004:
    INPUT: "document.pdf"
    CONTEXT: разделитель имени файла и расширения
    EXPECTED: INFO
    RISK: NONE
    GUARD: DOT_FORM ≠ FILE_EXTENSION_PROOF

  SAFE_CASE_005:
    INPUT: "version 2.5.1"
    CONTEXT: разделитель компонентов номера версии
    EXPECTED: INFO
    RISK: NONE
    GUARD: DOT_FORM ≠ VERSION_VALIDITY_PROOF

  SAFE_CASE_006:
    INPUT: "Подождите..."
    CONTEXT: многоточие (тройная точка) как индикатор
      продолжения/незаконченности мысли
    EXPECTED: INFO
    RISK: NONE
    GUARD: DOT_FORM ≠ COMPLETION_PROOF

RISK_CASES:
  RISK_CASE_001:
    NAME: FAKE_OFFICIAL_NOTATION
    INPUT: "Уведомление №А.1.7-ОФИЦ от руководства."
    CONTEXT: имитация формального/бюрократического стиля через
      обилие точек в номерах и сокращениях
    RISK: LOW
    ATTACK: точки в псевдо-индексах создают иллюзию официального
      документооборота, хотя сама точка не подтверждает
      легитимность источника
    GUARD: DOT_FORM ≠ AUTHORITY

  RISK_CASE_002:
    NAME: DOMAIN_LOOKALIKE_VIA_DOT_PLACEMENT
    INPUT: "paypal.com.security-check.ru"
    CONTEXT: фишинговый URL, где точки создают иллюзию
      поддомена легитимного сервиса
    RISK: HIGH
    ATTACK: размещение точек так, чтобы реальный домен
      ("security-check.ru") был скрыт визуально за похожим на
      легитимный поддоменом
    GUARD: DOT_FORM ≠ DOMAIN_VALIDITY_PROOF

  RISK_CASE_003:
    NAME: VERSION_NUMBER_TRUST_INFLATION
    INPUT: "Проверено в версии 99.9.9.9 — абсолютно безопасно"
    CONTEXT: использование длинной, "технически выглядящей"
      версии с точками для создания иллюзии тщательной проверки
    RISK: LOW
    ATTACK: количество точек/чисел в номере версии не
      коррелирует с реальной надёжностью утверждения
    GUARD: DOT_FORM ≠ VERSION_VALIDITY_PROOF

  RISK_CASE_004:
    NAME: ABBREVIATION_AUTHORITY_MIMICRY
    INPUT: "По заключению к.т.н. и д.э.н. изделие сертифицировано"
    CONTEXT: использование сокращений учёных степеней с точками
      без проверки, что степень реальна
    RISK: MEDIUM
    ATTACK: сокращение с точками выглядит как формальное
      подтверждение квалификации, хотя сама точка не верифицирует
      ни наличие степени, ни личность
    GUARD: DOT_FORM ≠ AUTHORITY

  RISK_CASE_005:
    NAME: ELLIPSIS_AS_FALSE_CONTINUATION_SIGNAL
    INPUT: "Мы гарантируем результат... подробности по запросу"
    CONTEXT: многоточие используется, чтобы намекнуть на
      существование скрытой, более полной информации, которой
      на деле может не быть
    RISK: LOW
    ATTACK: создаёт ложное ощущение, что есть веское продолжение
      аргумента, хотя многоточие — просто пунктуационный приём
    GUARD: DOT_FORM ≠ COMPLETION_PROOF

  RISK_CASE_006:
    NAME: NUMERIC_OBFUSCATION_VIA_DOT_INSERTION
    INPUT: "1.92.168.1.1" (вместо корректного "192.168.1.1")
    CONTEXT: добавление лишней точки в IP-подобную строку, чтобы
      обойти простую валидацию по паттерну или сбить
      автоматический парсер
    RISK: MEDIUM
    ATTACK: нестандартное расположение точек может обмануть
      regex-валидаторы, которые слепо доверяют наличию точек как
      признаку валидного IP-адреса
    GUARD: DOT_FORM ≠ DECIMAL_SEPARATOR_PROOF (в применении к
      сетевым адресам — отдельная advisory-проверка формата)

CONFUSABLES:
  CONFUSABLE_001:
    VISIBLE_FORM: ‧
    CODEPOINT: U+2027
    NAME: HYPHENATION POINT
    RISK: LOW
    RULE: HYPHENATION_POINT ≠ FULL_STOP

  CONFUSABLE_002:
    VISIBLE_FORM: ·
    CODEPOINT: U+00B7
    NAME: MIDDLE DOT
    RISK: MEDIUM
    RULE: MIDDLE_DOT ≠ FULL_STOP

  CONFUSABLE_003:
    VISIBLE_FORM: 。
    CODEPOINT: U+3002
    NAME: IDEOGRAPHIC FULL STOP
    RISK: MEDIUM
    RULE: IDEOGRAPHIC_FULL_STOP ≠ FULL_STOP (визуально похож,
      используется в CJK-текстах, может маскировать домены/строки
      при смешивании со стандартной точкой)

  CONFUSABLE_004:
    VISIBLE_FORM: ٠
    CODEPOINT: U+0660
    NAME: ARABIC-INDIC DIGIT ZERO
    RISK: LOW
    RULE: ARABIC_INDIC_ZERO ≠ FULL_STOP (риск путаницы в
      смешанных RTL/LTR числовых строках)

  CONFUSABLE_005:
    VISIBLE_FORM: ｡
    CODEPOINT: U+FF61
    NAME: HALFWIDTH IDEOGRAPHIC FULL STOP
    RISK: MEDIUM
    RULE: HALFWIDTH_IDEOGRAPHIC_FULL_STOP ≠ FULL_STOP (используется
      в японских/корейских текстах, потенциальный вектор для
      обхода фильтров, ищущих только стандартную точку U+002E)

  CONFUSABLE_006:
    VISIBLE_FORM: ․
    CODEPOINT: U+2024
    NAME: ONE DOT LEADER
    RISK: MEDIUM
    RULE: ONE_DOT_LEADER ≠ FULL_STOP (прямой типографический
      двойник точки, визуально почти неотличим от U+002E в
      большинстве шрифтов — наиболее точный визуальный конфузибл
      из всех перечисленных)

CONTRADICTION_GUARDS:
  CG1:
    TRIGGER: "точка в конце текста подтверждает, что мысль
      полностью завершена"
    RESPONSE: DOT_FORM ≠ COMPLETION_PROOF
    RULE: точка — пунктуационный маркер, не гарантия смысловой
      завершённости

  CG2:
    TRIGGER: "точка как десятичный разделитель означает, что
      число корректно по всем locale"
    RESPONSE: DOT_FORM ≠ DECIMAL_SEPARATOR_PROOF
    RULE: интерпретация точки как десятичного разделителя
      зависит от локали; в некоторых системах эта роль у запятой

  CG3:
    TRIGGER: "домен с точками типа paypal.com.xyz.ru — это
      поддомен paypal.com"
    RESPONSE: DOT_FORM ≠ DOMAIN_VALIDITY_PROOF
    RULE: визуальное наличие точек не определяет реальную
      доменную иерархию — это решает DNS, не текстовый паттерн

  CG4:
    TRIGGER: "сокращение с точкой (например 'д.т.н.') подтверждает
      реальность учёной степени или должности"
    RESPONSE: DOT_FORM ≠ AUTHORITY
    RULE: точка в сокращении — орфографическая конвенция, не
      механизм верификации квалификации

  CG5:
    TRIGGER: "длинный номер версии с множеством точек ('9.9.9.9')
      означает более тщательную проверку или надёжность продукта"
    RESPONSE: DOT_FORM ≠ VERSION_VALIDITY_PROOF
    RULE: количество компонентов номера версии не коррелирует
      с качеством или безопасностью

  CG6:
    TRIGGER: "точка после файла ('document.pdf') гарантирует,
      что файл реально является PDF и безопасен"
    RESPONSE: DOT_FORM ≠ FILE_EXTENSION_PROOF
    RULE: расширение после точки — это заявленный, не
      криптографически подтверждённый тип файла; реальный
      формат может отличаться (например исполняемый файл,
      переименованный с расширением .pdf)

SEQUENCE_LAYER_BOUNDARY:
  SIGN_SAFE_ALONE ≠ SIGN_SAFE_IN_SEQUENCE: YES
  SEQUENCE_CANDIDATES:
    SC1:
      SEQUENCE: ".." (две точки подряд)
      NAME: DOUBLE_DOT
      RISK_LEVEL: MEDIUM
      POSSIBLE_CONTEXTS: путь файловой системы "родительская
        директория" (../), потенциальный directory traversal
        в путях, опечатка
      REQUIRES_SEQUENCE_INTEGRATOR: YES

    SC2:
      SEQUENCE: "..." (три точки, многоточие)
      NAME: ELLIPSIS_SEQUENCE
      RISK_LEVEL: LOW
      POSSIBLE_CONTEXTS: риторический приём незаконченности
        мысли, манипулятивное создание ложного ощущения
        "продолжения" (см. RISK_CASE_005)
      REQUIRES_SEQUENCE_INTEGRATOR: NO (достаточно
        advisory-флага на уровне отдельного MODULE)

    SC3:
      SEQUENCE: "../../../" (множественные двойные точки с
        разделителями пути)
      NAME: PATH_TRAVERSAL_PATTERN
      RISK_LEVEL: HIGH
      POSSIBLE_CONTEXTS: классический паттерн атаки directory
        traversal для выхода за пределы разрешённой директории
      REQUIRES_SEQUENCE_INTEGRATOR: YES

  ЕСЛИ NOT_APPLICABLE: не применимо — последовательности выше
    реальны и значимы.

PHAGO_ENTITY_MIMICRY:
  NOT_APPLICABLE:
    REASON: точка сама по себе не имитирует существование
      проверенной сущности (организации, аккаунта, продукта) —
      в отличие, например, от знака @ (мимикрия под верифицированный
      аккаунт) или # (мимикрия под официальный тег/категорию).
      Риски точки (см. RISK_CASES выше) связаны с маскировкой
      доменов и созданием ложного ощущения формальности, но не
      с прямой имитацией конкретной проверенной сущности.
    REVIEW_REQUIRED: YES

============================================================
8. ADVERSARIAL_COVERAGE — RUN_CARD SEED
============================================================

MIN_TOTAL_VECTORS: 10 (5 категорий A-E, по 2 на категорию;
  CATEGORY_F = NOT_APPLICABLE для ZONE_1, см. ниже)

CATEGORY_A: FORM_MANIPULATION (3)
  A1: подмена U+002E на CONFUSABLE_002 (MIDDLE DOT, U+00B7) в
    доменном имени для визуального обмана
  A2: подмена U+002E на CONFUSABLE_003 (IDEOGRAPHIC FULL STOP,
    U+3002) в смешанном CJK/латинском тексте
  A3: подмена U+002E на CONFUSABLE_006 (ONE DOT LEADER, U+2024)
    в латинском тексте — наиболее точный визуальный двойник из
    всех конфузиблов, наименее заметная подмена для человека

CATEGORY_B: CONTEXT_INJECTION (2)
  B1: вставка точки в число для имитации десятичной дроби там,
    где ожидается целое число (например, цена "100.00" вместо
    "10000" для визуального уменьшения суммы)
  B2: использование точки как разделителя в псевдо-официальном
    номере документа для имитации бюрократической нумерации
    (см. RISK_CASE_001)

CATEGORY_C: SEQUENCE_MANIPULATION (2)
  C1: цепочка ".." в пути для directory traversal (см. SC1, SC3)
  C2: множественные точки "....." как визуальный разделитель,
    маскирующий конец одной семантической единицы и начало
    другой в фишинговом тексте

CATEGORY_D: SEMANTIC_MIMICRY (2 минимум)
  D1: имитация версии ПО с длинным номером через точки для
    создания иллюзии "проверенности" (см. RISK_CASE_003)
  D2: имитация академического сокращения с точками для
    создания иллюзии экспертного подтверждения (см. RISK_CASE_004)

CATEGORY_E: PHAGO_ENTITY_MIMICRY (2)
  E1: точка в "paypal.com.fake-domain.ru" как часть паттерна
    маскировки реального домена под легитимный сервис
    (см. RISK_CASE_002)
  E2: точка как разделитель в имени файла, маскирующая реальное
    расширение (например "invoice.pdf.exe" — точка перед "exe"
    визуально менее заметна после уже знакомого ".pdf")

CATEGORY_F: SEMANTIC_LAYER_MANIPULATION
  NOT_APPLICABLE
  REASON: ZONE_1, точка не имеет dormant/active эпох (см. раздел 5,
    SEMANTIC_EPOCH_TRACKER: NOT_APPLICABLE) — категория F тестирует
    реактивацию устаревшей эпохи знака, что неприменимо к знаку
    без эпох.

ACTUAL_TOTAL_VECTORS: 11
COVERAGE_STATUS: SUFFICIENT (11 ≥ 10)

============================================================
9. MUTATION_CHECK
============================================================

MUTATION_01:
  CLAIM: точка в конце фразы доказывает, что автор закончил мысль
  EXPECTED: FAIL_COMPLETION_MIMICRY
  RESULT: FAIL

MUTATION_02:
  CLAIM: точка как десятичный разделитель действует одинаково
    во всех локалях и системах счисления
  EXPECTED: FAIL_LOCALE_ASSUMPTION_MIMICRY
  RESULT: FAIL

MUTATION_03:
  CLAIM: домен с точками в любом расположении образует
    легитимную поддоменную структуру известного бренда
  EXPECTED: FAIL_DOMAIN_AUTHORITY_MIMICRY
  RESULT: FAIL

MUTATION_04:
  CLAIM: сокращение учёной степени с точками подтверждает
    реальность квалификации указанного лица
  EXPECTED: FAIL_AUTHORITY_MIMICRY
  RESULT: FAIL

MUTATION_05:
  CLAIM: расширение файла после точки гарантирует реальный
    формат и безопасность файла
  EXPECTED: FAIL_FILE_TYPE_TRUST_MIMICRY
  RESULT: FAIL

MUTATION_06:
  CLAIM: последовательность ".." в пути всегда безопасна для
    runtime, поскольку выглядит как обычная пунктуация
  EXPECTED: FAIL_SEQUENCE_SAFETY_MIMICRY
  RESULT: FAIL

============================================================
10. KNOWN_OPEN_QUESTIONS
============================================================

ALL_OPEN_QUESTIONS_CLOSED: YES (открытых вопросов на момент
  заполнения не выявлено)

============================================================
11. PATCH_HISTORY
============================================================

PATCH_HISTORY:
  v0_1_PATCH_01: Initial creation (Руслан Малявский, 2026-06-23) —
    первая заполненная карточка по шаблону SIGN_CORE_CARD_TEMPLATE
    GEN3_v0_3_RU; первый тест нового шаблона на практике.
  v0_1_PATCH_02: SIGN → VISIBLE_FORM in CONFUSABLES (автор,
    2026-06-23) — переименование запрещённого по NAMING_NORM поля
    во всех пяти CONFUSABLE_00X, синхронно с патчем шаблона
    (PATCH_NOTE_TEMPLATE_v0_3_P1).
    REASON: находка STRUCTURAL_PREFLIGHT_PASS — PROHIBITED_FIELD_USED

  v0_1_PATCH_03: CONFUSABLE_006 added — U+2024 ONE DOT LEADER
    (конвейерное ревью CONVEYOR_RUN_PACKET_DOT_CONTENT_REVIEW_v0_1,
    2026-06-23) — добавлен шестой confusable, не входивший в
    исходную карточку.
    REASON: конвергентная находка трёх ревьюеров из разных семейств
    моделей (Kimi, Gemini, GPT-5.5), независимо указавших на этот
    codepoint как пропущенный прямой типографический двойник точки.
    REJECTED_FINDINGS_FROM_THIS_REVIEW_ROUND (проверено координатором
      лично против первоисточника, по правилу
      VERIFY_BEFORE_TRUST_MANDATORY, и отклонено):
      - Qwen m2/m3/m4 (MUTATION_03/05/06 EXPECTED не совпадает
        с именем BASE_FORMULA) — шаблон определяет EXPECTED как
        свободное описание FAIL_<тип_подмены>, требования
        буквального совпадения с именем BASE_FORMULA не существует
        ни в шаблоне, ни в ruleset.
      - GPT-5.5 (U+FF0E "был в карточке, затем пропал") — неверно
        как факт: U+FF0E не встречается ни в одной версии карточки.
      - GPT-5.5 (уточнить формулировку GUARD в RISK_CASE_006 для
        IP-контекста) — уточнение "(в применении к сетевым
        адресам — отдельная advisory-проверка формата)" уже
        присутствует в карточке.
      - Qwen m1 (заменить U+0660 на U+2024) — замещение отклонено,
        U+0660 сохранён: confusable определяется визуальным
        сходством начертания, не категорией символа; U+2024
        добавлен отдельно, не взамен.

  v0_1_PATCH_04: ADVERSARIAL_COVERAGE CATEGORY_A vector A3 added —
    ссылка на CONFUSABLE_006 (Kimi, повторный раунд после
    патча_03, 2026-06-23) — добавлен вектор A3 (подмена U+002E на
    CONFUSABLE_006 в латинском тексте), ACTUAL_TOTAL_VECTORS
    обновлён 10→11.
    REASON: находка Kimi — A1/A2 не упоминали CONFUSABLE_006,
    самый точный визуальный двойник точки из всех конфузиблов,
    подтверждено координатором прямой проверкой файла.

PATCHES_APPLIED: 5
PATCHES_VERIFIED: 2/5
  (v0_1_PATCH_03 и v0_1_PATCH_04 теперь CONVEYOR_VERIFIED — это и
  была цель отдельного раунда PATCH_03_04_VERIFICATION (5 ревьюеров:
  Kimi, Gemini, GPT-5.5, Qwen, Grok), который прямо проверил их содержание
  по вопросам Q1/Q2 и подтвердил независимо. v0_1_PATCH_05 (правка
  заголовка CATEGORY_A) — находка из ТОГО ЖЕ раунда, но сама правка
  применена координатором после раунда и повторно конвейером не
  проверялась; v0_1_PATCH_01/02 не являются конвейерной проверкой
  по определению (создание автором / механическая самопроверка))
  v0_1_PATCH_01: VERIFIED_BY: AUTHOR (initial creation, not a
    conveyor check by definition)
  v0_1_PATCH_02: VERIFIED_BY: COORDINATOR (STRUCTURAL_PREFLIGHT_PASS,
    механическая проверка, не конвейер)
  v0_1_PATCH_03: ORIGINALLY VERIFIED_BY: COORDINATOR_ARBITRATION_ONLY,
    СЕЙЧАС: CONVEYOR_VERIFIED (см. PATCH_03_04_VERIFICATION_ROUND_RESULT
    ниже). На момент применения (2026-06-23, раньше в тот же день)
    патч был результатом разбора расхождений координатором, не
    повторным конвейерным прогоном — никакая внешняя модель его не
    видела. После этого был подготовлен отдельный пакет
    CONVEYOR_RUN_PACKET_DOT_PATCH_03_04_VERIFICATION_v0_1, и 5
    ревьюеров (Kimi, Gemini, GPT-5.5, Qwen, Grok — это полный и
    точный список участников; упоминание "Copilot" как участника в
    одном из более раннего черновика было ошибочным, Copilot ни в
    одном из раундов этого проекта не участвовал) подтвердили
    содержание патча_03 независимо (вопрос Q1 пакета верификации).
  v0_1_PATCH_04: ORIGINALLY VERIFIED_BY: COORDINATOR (находка Kimi
    про CATEGORY_A, подтверждена координатором прямой проверкой
    файла), СЕЙЧАС: CONVEYOR_VERIFIED — тот же раунд
    PATCH_03_04_VERIFICATION подтвердил вектор A3 и пересчитал
    ACTUAL_TOTAL_VECTORS=11 независимо (вопрос Q2 пакета
    верификации), всеми 5 ревьюерами.
  NOTE_ON_PATCHES_APPLIED_VS_VERIFIED_RATIO: формальное правило
    "PATCHES_APPLIED = PATCHES_VERIFIED — обязательное равенство"
    существует в SPEC_MSL_MIP_FOUNDATION (CONVEYOR_PASS_CRITERIA
    для дисциплины v0_2_PLUS_EPOCH), но НЕ зафиксировано как
    обязательное в SIGN_CORE_CARD_CONVEYOR_RULES_GEN3_v0_3_RU
    (раздел 4 v0_3 описывает только формат записи патча, без
    требования сквозного равенства). Эта карточка идёт по
    CONVEYOR_DISCIPLINE_VERSION: v0_3, поэтому текущее соотношение
    2/5 не является нарушением зафиксированного правила — это
    прозрачно задокументированная асимметрия, не блокер.
    (Ревьюер Qwen во втором раунде сослался на это правило как
    на "раздел 4 правил v0_3" — это неверная атрибуция, проверено
    координатором лично grep'ом по обоим документам, и подтверждено
    независимо 5 ревьюерами раунда PATCH_03_04_VERIFICATION,
    вопрос Q5.)
  COORDINATOR_ARBITRATION ≠ CONVEYOR_REVIEW
  CONVEYOR_REVIEW_PASS относится к содержанию карточки на момент
    отправки в пакет (v0_1_PATCH_02), не к патчу, добавленному
    после неё

  v0_1_PATCH_05: CATEGORY_A заголовок "(2)" → "(3)" (Qwen,
    PATCH_03_04_VERIFICATION раунд, 2026-06-23) — заголовок
    CATEGORY_A: FORM_MANIPULATION не был обновлён после добавления
    вектора A3 патчем_04 и продолжал показывать (2) при фактических
    трёх векторах (A1, A2, A3). Проверено координатором по файлу
    напрямую.
    VERIFIED_BY: COORDINATOR (находка Qwen из раунда верификации,
      но сама правка заголовка применена координатором после
      раунда и повторно конвейером не проверялась — аналогично
      исходному статусу патчей 03/04 до их собственной верификации)

  PATCH_03_04_VERIFICATION_ROUND_RESULT (отдельный конвейерный
    раунд, 5 ревьюеров — Kimi, Gemini, GPT-5.5, Qwen, Grok, 2026-06-23):
    ARBITRATION_CONFIRMED: YES по всем четырём пунктам (Q3–Q6) —
      все предыдущие отклонения координатора (несовпадение
      EXPECTED/BASE_FORMULA, "пропавший" U+FF0E, атрибуция правила
      PATCHES_APPLIED=PATCHES_VERIFIED, замена U+0660) подтверждены
      4/4 независимо.
    Q1/Q2 (содержание патчей 03/04): подтверждены 5/5 — это и есть
      основание для пометки этих двух патчей как CONVEYOR_VERIFIED
      выше.
    Единственная новая находка — заголовок CATEGORY_A "(2)" вместо
      "(3)" (Qwen) — патч_05 выше.
    VERDICT: ACCEPT (Kimi, Gemini, GPT-5.5, Grok) /
      ACCEPT_WITH_PATCHES (Qwen, единственная MINOR-находка)

============================================================
12. LIMITATION_STATEMENT
============================================================

LIMITATION_STATEMENT:
  THIS_CARD IS AN ARTIFACT_CONFIRMED ARTIFACT (прошла
    STRUCTURAL_PREFLIGHT_PASS, CONVEYOR_REVIEW_PASS,
    SIMULATION_GATE TIER_1 — финальный статус для методологии
    GEN3_v0_3)
  NOT A FINAL_STANDARD
  NOT A PARSER
  NOT A RUNTIME
  NOT A SECURITY_CERTIFICATE
  NOT PRODUCTION_READY (ARTIFACT_CONFIRMED ≠ PRODUCTION_READY —
    симуляция покрыла 2 контекста, не исчерпывающее тестирование)
  CONVEYOR_PASS ≠ VALIDATION
  RUN_CARD_RESULT ≠ FINAL_STATUS
  WORKINGLY_CLOSED ≠ ARTIFACT_CONFIRMED (пройдено, оба статуса
    последовательно получены)
  WORKINGLY_CLOSED ≠ LOCKED_WORKING_CORE
  ARTIFACT_CONFIRMED ≠ LOCKED_WORKING_CORE
  MODEL_CONSENSUS ≠ TRUTH

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

============================================================
END_OF_DOCUMENT
