ЧАСТНЫЙ АВТОРСКИЙ ПРОЕКТ / COMMERCIAL USE PROHIBITED

DOCUMENT_ID: SIGN_CORE_CARD_SOLIDUS_U002F_GEN3_v0_3_RU
DOCUMENT_TYPE: SIGN_CORE_CARD
TEMPLATE_LINE: GEN3_v0_3
DOCUMENT_STATUS: ARTIFACT_CONFIRMED
STATUS: ARTIFACT_CONFIRMED / NOT_LOCKED / NOT_RUNTIME / NOT_VALIDATOR / NOT_PRODUCTION
SOURCE_TEMPLATE: SIGN_CORE_CARD_TEMPLATE_GEN3_v0_3_RU
BASED_ON_RULESET: SIGN_CORE_CARD_CONVEYOR_RULES_GEN3_v0_3_RU

MIGRATION_NOTE (автор/координатор, 2026-06-24): содержание
  перенесено из легаси-карточки
  SIGN_CORE_CARD_SOLIDUS_U002F_GEN3_v0_2_PLUS_EPOCH_v0_1_EN
  (WORKINGLY_CLOSED, 2026-06-16) как РЕФЕРЕНС, не прямым копированием
  (LEGACY_REFERENCE_USAGE в исходной карточке: ALLOWED_FOR_EXAMPLES_ONLY).
  Перенесены: 5 эпох с академическими источниками (CAPTURE_HISTORY),
  6 SAFE_CASES, 8 RISK_CASES, 7 CONFUSABLES, 7 CONTRADICTION_GUARDS,
  7 SEQUENCE_CANDIDATES, 12 ADVERSARIAL_COVERAGE векторов (все 6
  категорий A-F применимы), 6 MUTATION_CHECK. Поля переименованы по
  NAMING_NORM v0_3 (SIGN: → VISIBLE_FORM в CONFUSABLES; добавлено
  явное поле ZONE; STATUS_PROGRESSION_TRACKER добавлен).
  Содержательные формулировки не менялись произвольно — где менялось,
  отмечено отдельно ниже.

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
  WORKINGLY_CLOSED: YES (AUTHOR_DECISION_20260624_002_SOLIDUS_U002F_WORKINGLY_CLOSED_RU)
  SIMULATION_GATE_TIER: TIER_2 (ZONE_2 — минимум 2 контекста,
    рекомендуется 3 "по образцу SOLIDUS" — правила v0_3, раздел 5,
    прямо ссылаются на этот знак как эталонный случай TIER_2)
  SIMULATION_GATE_PASSED: YES (4 контекста, консенсус 3/4 — Kimi,
    Qwen, Grok; Gemini отклонён за внутреннее противоречие
    STAGE_5/7 MODULE_TRACE. DIFFERENTIATION_CHECK: PASS, 6/6 пар.
    OPEN_ITEM по номеру guard для RISK_CASE_003 закрыт прямой
    проверкой по первоисточнику — CG1, не CG2/CG3 — см.
    SIMULATION_ARTIFACT_SOLIDUS_U002F_TIER2_v0_1_RU)
  ARTIFACT_CONFIRMED: YES (AUTHOR_DECISION_20260625_001_SOLIDUS_U002F_ARTIFACT_CONFIRMED_RU)

GAP_NOTE (найдено 2026-06-25, по прямому вопросу автора): между
  принятием AUTHOR_DECISION_20260625_001 (ARTIFACT_CONFIRMED) и
  его фактическим отражением в этом документе образовался разрыв
  — решение было объявлено в переписке, но сам файл карточки не
  обновлялся, в работе оставался только SIMULATION_ARTIFACT_
  SOLIDUS_U002F_TIER2_v0_1_RU (отдельный референс-документ).
  Этот файл — первое фактическое применение решения к самой
  карточке. Это более серьёзный случай того же класса находки,
  что и retroactive-логирование патчей у SKULL: там контент не
  менялся, но патчи не записывались; здесь сам файл карточки не
  обновлялся вовсе при уже принятом решении.

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

CARD_UID: SIGN_CORE_CARD_SOLIDUS_U002F_GEN3_v0_3_RU
CODEPOINT: U+002F
VISIBLE_FORM: /
UNICODE_NAME: SOLIDUS
ZONE: ZONE_2
DOCUMENT_STATUS: ARTIFACT_CONFIRMED
TEMPLATE_LINE: GEN3_v0_3
SOURCE_TEMPLATE: SIGN_CORE_CARD_TEMPLATE_GEN3_v0_3_RU
AUTHOR: Руслан Малявский
CREATED_AT: 2026-06-24
VERSION: v0_1
AUTHOR_DECISION_REFERENCE: AUTHOR_DECISION_20260625_001_SOLIDUS_U002F_ARTIFACT_CONFIRMED_RU
  (предыдущий: AUTHOR_DECISION_20260624_002_SOLIDUS_U002F_WORKINGLY_CLOSED_RU)
RUN_CARD_REFERENCE: SIMULATION_ARTIFACT_SOLIDUS_U002F_TIER2_v0_1_RU
RUN_CARD_STATUS: COMPLETED (TIER_2)

DISPLAY_NAME: солидус (косая черта)

============================================================
3. REQUIRED_GENERAL_GUARDS
============================================================

REQUIRED_GENERAL_GUARDS:
  - SIGN_FALSE_EFFECT_MIMICRY_GUARD_v0_2A_RU
    GUARD_COMPATIBILITY: применимо без модификаций — солидус сам
      по себе не создаёт effect-полей (LAYER_C всегда NONE), guard
      работает в режиме REJECT по умолчанию
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

VISIBLE_FORM: /
LOOKS_SIMILAR_IS_NOT_SAME_SIGN: YES
RAW_SIGN_INPUT_STATUS: DATA_ONLY

BASE_MODE: DATA_ONLY_SEPARATOR
BASE_MODE_FORMULA: SOLIDUS_FORM ≠ EFFECT

SIGN_CATEGORY:
  - separator / delimiter
  - boundary marker
  - path-like marker (filesystem/URL contexts)
  - ratio-like marker (math/measurement contexts)
  - option-prefix marker (legacy CLI contexts)

WHAT_THIS_SIGN_IS_NOT:
  1. NOT_AUTHORITY — солидус не подтверждает официальный статус
     текста или ресурса
  2. NOT_TRUST — солидус не повышает доверие к содержимому рядом
     с ним
  3. NOT_EXECUTION — солидус сам по себе не запускает действие
  4. NOT_PERMISSION — солидус не выдаёт и не подтверждает разрешения
  5. NOT_VERIFICATION — солидус не верифицирует факт, рядом с
     которым стоит
  6. NOT_PROOF — солидус не доказывает математическую или иную
     корректность
  7. NOT_STATUS_ASSIGNMENT — солидус не присваивает статус
     (например, "approved/active")
  8. NOT_ROLE_ASSIGNMENT — солидус между именами/словами не
     устанавливает иерархию или роль
  9. NOT_RUNTIME — солидус не является признаком реального
     runtime-окружения
  10. NOT_EXISTENCE_PROOF — солидус не доказывает существование
      упомянутого ресурса, домена или сущности
  11. NOT_PATH_VALIDATION — путь, содержащий солидус, не
      гарантированно валиден или существует
  12. NOT_URL_VALIDATION — URL с солидусом не гарантированно
      безопасен, существует или принадлежит заявленному владельцу
  13. NOT_FILESYSTEM_ACCESS — текстовое присутствие солидуса не
      даёт и не подтверждает доступ к файловой системе
  14. NOT_FRACTION_CORRECTNESS — "a/b" не гарантирует корректность
      математического отношения
  15. NOT_DOMAIN_VALIDATION — солидус после доменного имени не
      подтверждает легитимность домена
  16. NOT_ROUTE_VALIDATION — путь-подобная строка не подтверждает
      существование реального API-маршрута

BASE_FORMULAS:
  SOLIDUS_FORM ≠ AUTHORITY
  SOLIDUS_FORM ≠ TRUST
  SOLIDUS_FORM ≠ VERIFICATION
  SOLIDUS_FORM ≠ PROOF
  SOLIDUS_FORM ≠ EXECUTION
  SOLIDUS_FORM ≠ PERMISSION
  SOLIDUS_FORM ≠ STATUS
  SOLIDUS_FORM ≠ ROLE_ASSIGNMENT
  SOLIDUS_FORM ≠ RUNTIME
  SOLIDUS_FORM ≠ EXISTENCE_PROOF
  SOLIDUS_FORM ≠ PATH_VALIDATION
  SOLIDUS_FORM ≠ URL_VALIDATION
  SOLIDUS_FORM ≠ FILESYSTEM_ACCESS
  SOLIDUS_FORM ≠ FRACTION_CORRECTNESS

============================================================
5. SEMANTIC_EPOCH_TRACKER
SEMANTIC_EPOCH_TRACKER_LOCK: REVIEWABLE
============================================================

EPOCH_TRACKER: CONTEXT_GATE_REQUIRED
APPLICABILITY: APPLICABLE
NOTE: SOLIDUS имеет несколько РАВНОПРАВНЫХ стабильных семантических
  режимов в разных субстратах (письменность, математика, файловые
  пути, URL/URI, CLI/API-синтаксис). В отличие от ZONE_3 (где одна
  эпоха исторически вытесняет другую и может быть реактивирована),
  здесь нет единой "активной по умолчанию" эпохи — какая функция
  активна, определяется ИСКЛЮЧИТЕЛЬНО контекстом (CONTEXT_GATE), не
  временем. Поэтому ZONE_2, не ZONE_1 (нет полисемии без выбора) и
  не ZONE_3 (нет культурной прецессии одной эпохи другой).

CAPTURE_HISTORY:
  EPOCH_1:
    DATE_RANGE: 1450–настоящее время
    SUBSTRATE: письменность / типографика
    FUNCTION: разделитель вариантов, частей записи, альтернативная
      пунктуационная граница ("virgula")
    EVIDENCE:
      - Parkes, M. B. (1992). Pause and Effect: An Introduction to
        the History of Punctuation in the West. Berkeley: University
        of California Press — virgula (/) как подчинённый знак паузы
        в средневековых манускриптах, отдельно от запятой и точки.
      - Gutenberg Bible (Johannes Gutenberg, Mainz, ок. 1454–1455) —
        первая крупная книга, напечатанная в Европе подвижным
        металлическим шрифтом; набор знаков включал virgula/solidus
        как знак цезуры и разделитель.
      - Средневековая латынь "virgula" (веточка) — исходное название
        знака.
    STATUS: DORMANT_IN_DIGITAL_SECURITY_CONTEXT / ACTIVE_IN_TEXTUAL_CONTEXTS

  EPOCH_2:
    DATE_RANGE: 1631–настоящее время
    SUBSTRATE: математика / измерения
    FUNCTION: разделитель дробей, обозначение отношения
    EVIDENCE:
      - Oughtred, W. (1631). Clavis Mathematicae. London: Thomas
        Harper — солидус как разделитель дробей ("3/4").
      - Cajori, F. (1928). A History of Mathematical Notations,
        Vol. 1 — солидус как доминирующий разделитель дробей в
        английских математических текстах с XVII века.
      - ISO 80000-2 (2019). Quantities and units — Part 2:
        Mathematics — солидус стандартизирован как основная
        нотация дробей в современных научных текстах.
    STATUS: ACTIVE_IN_MATH_AND_MEASUREMENT_CONTEXTS

  EPOCH_3:
    DATE_RANGE: 1969–настоящее время
    SUBSTRATE: файловая система / пути
    FUNCTION: разделитель компонентов пути
    EVIDENCE:
      - Ritchie, D. M., & Thompson, K. (1974). "The UNIX
        Time-Sharing System". Communications of the ACM, 17(7) —
        иерархическая файловая система с "/" как разделителем,
        разработана в 1969 в Bell Labs.
      - Конвенция путей Multics (1965) — предшественник UNIX.
    STATUS: ACTIVE_IN_TECHNICAL_CONTEXTS

  EPOCH_4:
    DATE_RANGE: 1994–настоящее время
    SUBSTRATE: URL / URI / веб-адресация
    FUNCTION: разделитель компонентов сетевого ресурса
    EVIDENCE:
      - Berners-Lee, T. (1994). RFC 1630 — формализация "/" как
        разделителя пути в URI.
      - RFC 3986 (2005). Uniform Resource Identifier — подтверждение
        "/" как постоянного компонента синтаксиса URI.
    STATUS: ACTIVE_IN_WEB_CONTEXTS

  EPOCH_5:
    DATE_RANGE: 1979–настоящее время
    SUBSTRATE: CLI / API / config / синтаксис маршрутов
    FUNCTION: маркер опции, путь маршрута, namespace-подобные
      структуры
    EVIDENCE:
      - Конвенция командной строки DOS/CP/M — "/" как префикс опции
        в раннем x86 ПО (86-DOS, MS-DOS 1.x/2.x), унаследовано от
        CP/M (1974).
      - Tim Paterson, 86-DOS (1980–1981) — выбор "/" как префикса
        опции, что впоследствии привело к выбору обратной косой
        черты для путей в DOS 2.0 во избежание неоднозначности.
    STATUS: ACTIVE_IN_SPECIALIZED_TECHNICAL_CONTEXTS

ACTIVE_EPOCH_RESOLUTION:
  PRIMARY_ACTIVE_EPOCH: NONE_GLOBAL
  REASON: для солидуса нет единой современной активной эпохи по
    умолчанию. Веб-контекст активирует EPOCH_4, файловый контекст —
    EPOCH_3, математический — EPOCH_2, CLI/API/config — EPOCH_5.
  RULE: при наличии нескольких равноправных современных субстратов
    ACTIVE_EPOCH определяется через CONTEXT_ACTIVE_EPOCH, не через
    единую глобальную ACTIVE_EPOCH.

DORMANT_EPOCHS:
  EPOCH_1 в современном техническом парсинге, если явно не задан
    текстовый/типографский контекст.
  NOTE: дормантная эпоха может реактивироваться в историческом,
    типографском, архивном или специализированном контексте.

PRECESSION_ALERT:
  STATUS: STABLE_WITH_CONTEXT_COLLISION
  LAST_CHECK: 2026-06-24
  NOTE: новых захватов не обнаружено; архитектурная особенность —
    несколько активных современных эпох требуют CONTEXT_GATE, это
    не баг, а заданное свойство знака.

LAYER_ANOMALY:
  ABSENT_PHYSICAL_LAYER: NO
  NOTE: солидус не воспроизводит отсутствующий физический жест, но
    переносит структуру "разделить / направить / связать" между
    субстратами.

STACK_RULES:
  HIGHER_EPOCH_SUPPRESSES_LOWER_IN_MODERN_CONTEXTS: PARTIAL /
    CONTEXT_DEPENDENT
  LOWER_EPOCH_MAY_REACTIVATE_IN_HISTORICAL_OR_SPECIALIZED_CONTEXTS: YES
  CONTEXT_GATE_DETERMINES_ACTIVE_EPOCH: YES / REQUIRED

EPOCH_LIMITATION:
  EPOCH ≠ VERSION
  EPOCH ≠ EFFECT_FIELD
  EPOCH ≠ GUARD
  EPOCH ≠ VALIDATION
  EPOCH ≠ PROOF_OF_CONTEXT
  CONTEXT_ACTIVE_EPOCH ≠ GLOBAL_ACTIVE_EPOCH

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
NOTE: SEMANTIC_EPOCH_TRACKER помогает интегратору обнаружить
  контекстный риск, но не изменяет EFFECT_FIELDS уровня LAYER_C —
  сам по себе знак не имеет authority/trust/proof/execution/
  permission/status/role_assignment/runtime/verification/existence
  эффекта, независимо от активной эпохи.

============================================================
7. SAFE / RISK / CONFUSABLES / GUARDS — LAYER_B: SEMI-STABLE LAYER
LAYER_B_LOCK: REVIEWABLE
============================================================

SAFE_CASES:
  SAFE_CASE_001:
    INPUT: "и/или"
    CONTEXT: обычный текст
    EXPECTED: INFO
    RISK: NONE
    GUARD: SOLIDUS_FORM ≠ CHOICE_VALIDATION (солидус разделяет
      альтернативы, не подтверждает ни одну из них)

  SAFE_CASE_002:
    INPUT: "1/2"
    CONTEXT: математическая нотация
    EXPECTED: INFO
    RISK: NONE
    GUARD: SOLIDUS_FORM ≠ FRACTION_CORRECTNESS (может обозначать
      дробь, но не верифицирует математическую корректность)

  SAFE_CASE_003:
    INPUT: "/home/user/docs"
    CONTEXT: путь файловой системы в тексте
    EXPECTED: INFO
    RISK: NONE
    GUARD: SOLIDUS_FORM ≠ FILESYSTEM_ACCESS (текстовое вхождение не
      даёт доступа и не подтверждает существование пути)

  SAFE_CASE_004:
    INPUT: "https://example.org/a/b"
    CONTEXT: URL в тексте
    EXPECTED: INFO
    RISK: NONE
    GUARD: SOLIDUS_FORM ≠ URL_VALIDATION (разделяет компоненты URL,
      не подтверждает домен, ресурс, владельца или безопасность)

  SAFE_CASE_005:
    INPUT: "2026/06/24"
    CONTEXT: дата-подобный текст
    EXPECTED: INFO
    RISK: NONE
    GUARD: SOLIDUS_FORM ≠ DATE_PROOF (может разделять компоненты
      даты, не подтверждает формат, календарную корректность или
      существование события)

  SAFE_CASE_006:
    INPUT: "кг/м"
    CONTEXT: измерительный текст
    EXPECTED: INFO
    RISK: NONE
    GUARD: SOLIDUS_FORM ≠ MEASUREMENT_VALIDATION (может обозначать
      отношение/единицу, не подтверждает корректность измерения)

RISK_CASES:
  RISK_CASE_001:
    NAME: FILESYSTEM_TRAVERSAL_OR_ESCAPE_MIMICRY
    INPUT: "../../etc/passwd"
    INPUT_ALT: "http:\\/\\/evil.test"
    CONTEXT: солидус в позиции, характерной для файловой системы —
      два подпаттерна под одним RISK_CASE, так как оба относятся к
      одному семейству "солидус в FILESYSTEM-контексте как признак
      попытки обхода/экранирования":
        (a) PATH_TRAVERSAL: солидус сразу после ".." (../)
        (b) ESCAPE_SEQUENCE: солидус сразу после обратного слеша (\/)
    RISK: HIGH
    ATTACK: визуально узнаваемый паттерн обхода файловой системы
      ИЛИ экранирования; сам по себе текст не даёт доступа, но
      может быть частью реальной попытки обхода/инъекции в системах,
      которые буквально резолвят путь или интерпретируют
      escape-последовательности
    GUARD: SOLIDUS_FORM ≠ FILESYSTEM_ACCESS
    IMPLEMENTATION_NOTE (author, 2026-07-04): код solidus_matcher.py
      реализует ОБА подпаттерна под RISK_CASE_001 (ветка FILESYSTEM:
      проверка text[offset-1]=="\\" для escape, и text[offset-2:offset]
      == ".." для traversal). Оба относятся к одному семейству угроз,
      поэтому объединены под одним RISK_CASE, а не разведены.

  RISK_CASE_002:
    NAME: URL_AUTHORITY_MIMICRY
    INPUT: "trusted.com/verified/project"
    CONTEXT: путь после доверенного домена создаёт иллюзию
      официального статуса ресурса
    RISK: MEDIUM
    ATTACK: разделённый солидусами путь имитирует "верифицированный"
      или официальный статус, хотя сам путь ничего не подтверждает
    GUARD: SOLIDUS_FORM ≠ URL_VALIDATION

  RISK_CASE_003:
    NAME: PERMISSION_PATH_MIMICRY
    INPUT: "/admin/root/execute"
    CONTEXT: путь-подобная структура имитирует повышение привилегий
      или исполняемый маршрут
    RISK: MEDIUM
    ATTACK: визуальное сходство с реальным административным путём
      создаёт иллюзию полномочий, хотя текст — не код и не команда
    GUARD: SOLIDUS_FORM ≠ PERMISSION

  RISK_CASE_004:
    NAME: API_ROUTE_AUTHORITY_MIMICRY
    INPUT: "/api/v1/admin/delete"
    CONTEXT: API-подобный маршрут может быть воспринят как реальная
      возможность или runtime-эндпоинт
    RISK: MEDIUM
    ATTACK: текстовая строка имитирует деструктивный API-вызов,
      хотя сама по себе не является вызовом
    GUARD: SOLIDUS_FORM ≠ RUNTIME

  RISK_CASE_005:
    NAME: STATUS_CHAIN_MIMICRY
    INPUT: "одобрено/активно/верифицировано"
    CONTEXT: цепочка слов-статусов через солидус имитирует
      подтверждённую цепочку проверки
    RISK: LOW
    ATTACK: создаёт ложное ощущение многоступенчатой верификации,
      хотя солидус — просто разделитель слов
    GUARD: SOLIDUS_FORM ≠ STATUS

  RISK_CASE_006:
    NAME: ROLE_BINDING_MIMICRY
    INPUT: "root/admin"
    CONTEXT: парное соединение через солидус намекает на иерархию
      или ролевую привязку
    RISK: LOW
    ATTACK: визуальная близость двух привилегированных слов создаёт
      иллюзию формальной связи между ролями
    GUARD: SOLIDUS_FORM ≠ ROLE_ASSIGNMENT

  RISK_CASE_007:
    NAME: PHAGO_ENTITY_PATH_MIMICRY
    INPUT: "OpenAI/VerifiedProjectX"
    CONTEXT: близость к названию известной организации через
      солидус имитирует официальный подпроект, подразделение или
      аффилированную сущность
    RISK: HIGH
    ATTACK: солидус используется как визуальный "знак принадлежности"
      к проверенному бренду, хотя не подтверждает реальной связи
    GUARD: PATH_PROXIMITY ≠ VERIFIED_CARRIER

  RISK_CASE_008:
    NAME: EPOCH_MISMATCH_ATTACK
    INPUT: "A/B"
    CONTEXT: неоднозначный контекст без явного субстрата
    RISK: MEDIUM
    ATTACK: парсер может принудительно выбрать математическую,
      файловую или текстовую эпоху без реального контекстного
      обоснования, что приведёт к неверной интерпретации
    GUARD: CONTEXT_ACTIVE_EPOCH_REQUIRED (AMBIGUITY_FLAG: YES при
      отсутствии явного контекста)

CONFUSABLES:
  CONFUSABLE_001:
    VISIBLE_FORM: ⁄
    CODEPOINT: U+2044
    NAME: FRACTION SLASH
    RISK: MEDIUM
    RULE: FRACTION_SLASH ≠ SOLIDUS_U002F

  CONFUSABLE_002:
    VISIBLE_FORM: ∕
    CODEPOINT: U+2215
    NAME: DIVISION SLASH
    RISK: MEDIUM
    RULE: DIVISION_SLASH ≠ SOLIDUS_U002F

  CONFUSABLE_003:
    VISIBLE_FORM: ／
    CODEPOINT: U+FF0F
    NAME: FULLWIDTH SOLIDUS
    RISK: MEDIUM
    RULE: FULLWIDTH_SOLIDUS ≠ SOLIDUS_U002F (CJK-контексты,
      потенциальный вектор обхода фильтров по точному кодпоинту)

  CONFUSABLE_004:
    VISIBLE_FORM: ╱
    CODEPOINT: U+2571
    NAME: BOX DRAWINGS LIGHT DIAGONAL UPPER RIGHT TO LOWER LEFT
    RISK: LOW
    RULE: BOX_DRAWING_DIAGONAL ≠ SOLIDUS_U002F

  CONFUSABLE_005:
    VISIBLE_FORM: ⧸
    CODEPOINT: U+29F8
    NAME: BIG SOLIDUS
    RISK: LOW
    RULE: BIG_SOLIDUS ≠ SOLIDUS_U002F

  CONFUSABLE_006:
    VISIBLE_FORM: ⟋
    CODEPOINT: U+27CB
    NAME: MATHEMATICAL RISING DIAGONAL
    RISK: LOW
    RULE: MATHEMATICAL_RISING_DIAGONAL ≠ SOLIDUS_U002F

  CONFUSABLE_007:
    VISIBLE_FORM: \
    CODEPOINT: U+005C
    NAME: REVERSE SOLIDUS (backslash)
    CONFUSABLE_TYPE: FUNCTIONAL (не визуальный гомоглиф — символ
      зеркален, не похож по форме; путаница возникает на уровне
      интерпретации ОС/парсера путей, не зрения)
    RISK: HIGH
    RULE: REVERSE_SOLIDUS ≠ SOLIDUS_U002F (критично в путях — Windows
      использует обратную косую черту как основной разделитель,
      путаница меняет интерпретацию пути целиком)

CONTRADICTION_GUARDS:
  CG1:
    TRIGGER: "солидус сам по себе подтверждает авторитет, доверие,
      верификацию, доказательство, исполнение, разрешение, статус,
      ролевую привязку, runtime или существование чего-либо"
    RESPONSE: SOLIDUS_FORM ≠ AUTHORITY/TRUST/VERIFICATION/PROOF/
      EXECUTION/PERMISSION/STATUS/ROLE_ASSIGNMENT/RUNTIME/EXISTENCE
    RULE: солидус — разделитель, не носитель эффекта любого рода

  CG2:
    TRIGGER: "путь, содержащий солидус, доказывает доступ к
      файловой системе"
    RESPONSE: SOLIDUS_FORM ≠ FILESYSTEM_ACCESS
    RULE: текстовое присутствие пути не равно реальному доступу

  CG3:
    TRIGGER: "URL с солидусами доказывает, что ресурс существует,
      безопасен или принадлежит заявленному владельцу"
    RESPONSE: SOLIDUS_FORM ≠ URL_VALIDATION
    RULE: структура URL не подтверждает ничего о реальном ресурсе —
      это решает DNS/HTTP-запрос, не текстовый паттерн

  CG4:
    TRIGGER: "дробь вида 'a/b' доказывает математическую
      корректность отношения"
    RESPONSE: SOLIDUS_FORM ≠ FRACTION_CORRECTNESS
    RULE: нотация дроби не верифицирует арифметическую правильность

  CG5:
    TRIGGER: "солидус безопасен в одиночном вхождении, значит
      любая последовательность с солидусом тоже безопасна"
    RESPONSE: SIGN_SAFE_ALONE ≠ SIGN_SAFE_IN_SEQUENCE
    RULE: см. раздел 8 — некоторые последовательности солидуса
      требуют отдельной проверки SEQUENCE_INTEGRATOR

  CG6:
    TRIGGER: "близость названия известной организации к
      путь-подобной структуре через солидус подтверждает реальную
      принадлежность/аффилированность"
    RESPONSE: PATH_PROXIMITY ≠ VERIFIED_CARRIER
    RULE: визуальная близость к бренду не равна верифицированной
      связи с этим брендом — см. PHAGO_ENTITY_MIMICRY ниже

  CG7:
    TRIGGER: "у солидуса есть одна правильная активная эпоха,
      применимая независимо от контекста"
    RESPONSE: SOLIDUS_EPOCH ≠ CONTEXT_PROOF
    RULE: активная эпоха определяется ИСКЛЮЧИТЕЛЬНО через
      CONTEXT_GATE (см. раздел 5) — нет глобально верной эпохи по
      умолчанию

SEQUENCE_LAYER_BOUNDARY:
  SIGN_SAFE_ALONE ≠ SIGN_SAFE_IN_SEQUENCE: YES
  SEQUENCE_CANDIDATES:
    SC1:
      SEQUENCE: "//" (двойной солидус)
      NAME: DOUBLE_SOLIDUS
      RISK_LEVEL: HIGH
      POSSIBLE_CONTEXTS: разделитель схемы URL ("https://"),
        маркер комментария в некоторых языках программирования,
        путь-подобный паттерн
      REQUIRES_SEQUENCE_INTEGRATOR: YES
      ADJACENT_CONFUSABLE_NOTE_FF0F: Unicode-слэш ／ (U+FF0F FULLWIDTH
        SOLIDUS) — НЕ ловится SC1 (матчит только ASCII // U+002F). Вскрыто
        SIMULATION_GATE_REVIEW 2026-07-07. Это НЕ баг scheme-патча, а
        смежный confusable — кандидат на отдельную карточку (аналог ＠/﹫
        для @). Не блокирует SOLIDUS-патч, вынесено в бэклог.
      SCHEME_CONTEXT_RULE: SOLIDUS_SCHEME_PATCH (2026-07-07, вариант «б»,
        AUTHOR_DECISION после design-review 6/6). Если "//" непосредственно
        следует за ":" (т.е. это связка схемы "://") — риск понижается до
        NONE (interp=url_scheme_authority_separator) как легитимная схема,
        и выставляется URL_CONTEXT_FLAG. Флаг ТОЛЬКО повышает scrutiny
        нижестоящих знаков (@, точка), НИКОГДА не понижает (CLARIFICATION_1).
        "//" БЕЗ предшествующего ":" остаётся HIGH под анализом
        (path-traversal, CLARIFICATION_2). Различитель — один символ ":".
      SCHEME_PATCH_STATUS: WORKINGLY_CLOSED (AUTHOR_DECISION Руслана
        Малявского 2026-07-07). Полный цикл: design-review 6/6 +
        AUTHOR_DECISION → code-review 6/6 (2 фикса: Q4 enum-баг, Q1
        валидация схемы RFC 3986) → SIMULATION_GATE_REVIEW 6/6 (новая
        дисциплина «симуляции через все ИИ») → gate 28/28 в контейнере
        и на живой машине. Первая правка ЯДРА sequence-движка, прошедшая
        полный цикл. Тесты: tests/gate_solidus_scheme.py.

    SC2:
      SEQUENCE: "./" (точка-солидус)
      NAME: DOT_SOLIDUS
      RISK_LEVEL: MEDIUM
      POSSIBLE_CONTEXTS: относительный путь, командный контекст
      REQUIRES_SEQUENCE_INTEGRATOR: YES

    SC3:
      SEQUENCE: "../" (точка-точка-солидус)
      NAME: DOT_DOT_SOLIDUS
      RISK_LEVEL: HIGH
      POSSIBLE_CONTEXTS: directory traversal, относительный путь
        к родительской директории
      REQUIRES_SEQUENCE_INTEGRATOR: YES

    SC4:
      SEQUENCE: "/=" (солидус-равно)
      RISK_LEVEL: LOW
      NAME: SOLIDUS_EQUALS
      POSSIBLE_CONTEXTS: оператор-подобная последовательность,
        путаница с присваиванием в некоторых нотациях
      REQUIRES_SEQUENCE_INTEGRATOR: NO (достаточно advisory-флага
        на уровне MODULE)

    SC5:
      SEQUENCE: "/*" (солидус-астериск)
      NAME: SOLIDUS_ASTERISK
      RISK_LEVEL: MEDIUM
      POSSIBLE_CONTEXTS: открытие блочного комментария в C-подобных
        языках, wildcard-подобный паттерн
      REQUIRES_SEQUENCE_INTEGRATOR: YES

    SC6:
      SEQUENCE: "*/" (астериск-солидус)
      NAME: ASTERISK_SOLIDUS
      RISK_LEVEL: MEDIUM
      POSSIBLE_CONTEXTS: закрытие блочного комментария в C-подобных
        языках
      REQUIRES_SEQUENCE_INTEGRATOR: YES

# PATCH_27 (AUTHOR_DECISION_CONFIRMED, 2026-06-29, см. CONVEYOR_RUN_PACKET
# MSL_MIP_SEQUENCE_CODE_v0_1 раунд 2): добавлено поле SCOPE к SC7.
# Ведущий символ ":" не является знаком ни одной SIGN_CORE_CARD в
# системе — кандидат структурно зависит от символа, который upstream-
# парсер должен передать как валидированный, прежде чем SEQUENCE-слой
# имеет право его засчитать. Без этого поля ":" в "://" неотличим от
# "*" в SOLIDUS.SC6 "*/" (тот символ тоже вне системы знаков, но НЕ
# должен блокировать кандидат). Найдено по итогам код-ревью
# sequence_engine.py (Ghost Matching / SC6-regression, 2026-06-29).
# Статус подтверждён Русланом (AUTHOR_DECISION) 2026-06-29.
    SC7:
      SEQUENCE: "://" (двоеточие-двойной-солидус)
      NAME: COLON_DOUBLE_SOLIDUS
      RISK_LEVEL: HIGH
      POSSIBLE_CONTEXTS: связка схемы URL ("https://", "ftp://") —
        сильный сигнал, что строка интерпретируется как ссылка
      REQUIRES_SEQUENCE_INTEGRATOR: YES
      SCOPE: UPSTREAM_DEPENDENT

  RAW_SEQUENCE_TEXT_IS_NOT_SIGN_CARD_INPUT: YES
  SOLIDUS_CARD_ALONE_DOES_NOT_VALIDATE_SEQUENCE: YES
  SEQUENCE_ADVISORY_ONLY: YES

PHAGO_ENTITY_MIMICRY:
  APPLICABLE:
    REASON: солидус, в отличие от точки, регулярно участвует в
      паттерне "ИЗВЕСТНЫЙ_БРЕНД/что-то", где визуальная близость к
      названию проверенной организации создаёт иллюзию официального
      подпроекта, подразделения или аффилированной сущности (см.
      RISK_CASE_007). Это прямая мимикрия под существование
      проверенной сущности — именно то, что категория PHAGO_ENTITY_
      MIMICRY проверяет.
    PRIMARY_RULE: EXISTENCE_FORM ≠ VERIFIED_CARRIER
    SOLIDUS_SPECIFIC_RULE: PATH_PROXIMITY ≠ VERIFIED_CARRIER
    GUARD_REFERENCE: CG6 (раздел 7), RISK_CASE_007
    REVIEW_REQUIRED: YES

============================================================
8. ADVERSARIAL_COVERAGE — RUN_CARD SEED
============================================================

MIN_TOTAL_VECTORS: 12 (6 категорий A-F, по 2 на категорию — для
  ZONE_2 категория F ПРИМЕНИМА, в отличие от ZONE_1: у солидуса есть
  CONTEXT_GATE и потенциал принудительного смещения эпохи/субстрата)

CATEGORY_A: FORM_MANIPULATION (2)
  A1: подмена U+002F на CONFUSABLE_001 (FRACTION SLASH, U+2044) в
    URL-подобной строке
  A2: подмена U+002F на CONFUSABLE_003 (FULLWIDTH SOLIDUS, U+FF0F)
    в путь-подобной строке для обхода фильтров по точному кодпоинту

CATEGORY_B: CONTEXT_INJECTION (2)
  B1: "/admin/root/execute" интерпретируется как реальный маршрут
    разрешений (см. RISK_CASE_003)
  B2: "2026/06/24" интерпретируется как подтверждённая дата
    реального события

CATEGORY_C: SEQUENCE_MANIPULATION (2)
  C1: "../secret" — паттерн, похожий на directory traversal (см. SC3)
  C2: "https://trusted.com//verified" — неоднозначность границы из-за
    двойного солидуса (см. SC1, SC7)

CATEGORY_D: SEMANTIC_MIMICRY (2)
  D1: "user/admin" интерпретируется как повышение роли (см.
    RISK_CASE_006)
  D2: "одобрено/активно/верифицировано" интерпретируется как цепочка
    подтверждённых статусов (см. RISK_CASE_005)

CATEGORY_E: PHAGO_ENTITY_MIMICRY (2)
  E1: "OpenAI/VerifiedProjectX" интерпретируется как подтверждённое
    существование подпроекта (см. RISK_CASE_007)
  E2: "ministry/registry/fake-entity" интерпретируется как
    официальный реестр-носитель

CATEGORY_F: SEMANTIC_LAYER_MANIPULATION (2)
  F1: "1/2" принудительно интерпретируется в файловом/путевом
    контексте вместо математического (ложный CONTEXT_GATE выбор)
  F2: "и/или" (типографская альтернатива, EPOCH_1) принудительно
    интерпретируется как исполняемый синтаксис или путь-токен,
    реактивируя дормантный лингвистический слой для обхода
    структурного модуля безопасности

ACTUAL_TOTAL_VECTORS: 12
COVERAGE_STATUS: SUFFICIENT (12 ≥ 12)

============================================================
9. MUTATION_CHECK
============================================================

MUTATION_01:
  CLAIM: солидус создаёт доступ к файловой системе
  EXPECTED: FAIL_PATH_ACCESS_MIMICRY
  RESULT: FAIL

MUTATION_02:
  CLAIM: солидус в URL доказывает, что ресурс существует и безопасен
  EXPECTED: FAIL_URL_VALIDATION_MIMICRY
  RESULT: FAIL

MUTATION_03:
  CLAIM: солидус между названиями ролей присваивает иерархию или
    разрешение
  EXPECTED: FAIL_ROLE_ASSIGNMENT_MIMICRY
  RESULT: FAIL

MUTATION_04:
  CLAIM: солидус в дроби доказывает математическую корректность
  EXPECTED: FAIL_PROOF_MIMICRY
  RESULT: FAIL

MUTATION_05:
  CLAIM: близость к названию через солидус доказывает существование
    верифицированного носителя/подпроекта
  EXPECTED: FAIL_PHAGO_ENTITY_MIMICRY
  RESULT: FAIL

MUTATION_06:
  CLAIM: у солидуса есть одна глобальная активная эпоха независимо
    от контекста
  EXPECTED: FAIL_SEMANTIC_EPOCH_INTEGRITY / CONTEXT_GATE_REQUIRED
  RESULT: FAIL

============================================================
10. KNOWN_OPEN_QUESTIONS
============================================================

ALL_OPEN_QUESTIONS_CLOSED: YES (открытые вопросы легаси-карточки
  v0_2_PLUS_EPOCH — SOLIDUS_ACTIVE_EPOCH_COLLISION, историческая
  доказательная база для эпох 1–2, технические источники для эпох
  3–5 — были закрыты ещё в исходной карточке 2026-06-16 и не
  пересматриваются в рамках миграции на v0_3)

============================================================
11. PATCH_HISTORY
============================================================

PATCH_HISTORY:
  v0_1_PATCH_01: Initial creation under GEN3_v0_3 (Руслан Малявский /
    координатор, 2026-06-24) — карточка заполнена на основе
    легаси-карточки SIGN_CORE_CARD_SOLIDUS_U002F_GEN3_v0_2_PLUS_
    EPOCH_v0_1_EN (WORKINGLY_CLOSED, 2026-06-16) как референс, не
    прямым копированием. Перенесены: 5 эпох CAPTURE_HISTORY с
    академическими источниками, 6 SAFE_CASES, 8 RISK_CASES (RISK_CASE_005
    переименован из DATE_OR_STATUS_MIMICRY в STATUS_CHAIN_MIMICRY —
    исходное название дублировало смысл RISK_CASE про дату, которой
    в финальном INPUT не было), 7 CONFUSABLES (поле SIGN → VISIBLE_FORM
    по NAMING_NORM v0_3), 7 CONTRADICTION_GUARDS, 7 SEQUENCE_CANDIDATES,
    12 ADVERSARIAL_COVERAGE векторов, 6 MUTATION_CHECK.
    PHAGO_ENTITY_MIMICRY явно помечен APPLICABLE (в отличие от DOT,
    где он NOT_APPLICABLE) — у солидуса есть прямой паттерн мимикрии
    под существование сущности (RISK_CASE_007), не просто маскировка
    структуры.
    REASON: первая карточка ZONE_2 под методологией v0_3, эталонный
    случай для TIER_2 SIMULATION_GATE (правила v0_3 раздел 5 прямо
    ссылаются на SOLIDUS).

  v0_1_PATCH_05: RISK_CASE_001 расширен с PATH_TRAVERSAL_MIMICRY до
    FILESYSTEM_TRAVERSAL_OR_ESCAPE_MIMICRY (автор, 2026-07-04) —
    документация догоняет код. Внешнее исследование (Alibaba Qwen
    deep-research по проекту) выявило, что solidus_matcher.py
    реализует под RISK_CASE_001 ДВА подпаттерна (path traversal ".."
    и escape "\"), тогда как карточка описывала только первый.
    AUTHOR_DECISION (вариант B, прагматичный): код работал корректно
    с самого начала — оба подпаттерна принадлежат одному семейству
    "солидус в FILESYSTEM-контексте как признак обхода/экранирования".
    Карточка получает уточнение задним числом БЕЗ понижения статуса
    ARTIFACT_CONFIRMED, так как функциональность кода не менялась —
    менялось только её описание в карточке. Это не дефект артефакта,
    а догоняющая документация.
    REASON: устранение семантического расхождения "спецификация ↔
    реализация", найденного внешним исследованием.
    VERIFICATION: подтверждено прямым grep по solidus_matcher.py
    (строки 148-149 escape, 151-152 traversal) автором лично.

PATCHES_APPLIED: 5
PATCHES_VERIFIED: 3/3 (содержательные патчи 01-02, 05; патчи 03-04 —
  governance-only, см. ниже)
  v0_1_PATCH_01 (само заполнение карточки): VERIFIED_BY: CONVEYOR —
    5 ревьюеров в исходном раунде (Kimi — частично, оборвался на
    Q2 по лимиту длины внешнего чата, не по содержательной
    проблеме; Qwen, Grok, GPT-5.5, Gemini — полные ответы Q1–Q9+B.3).
    0 CRITICAL, 0 MAJOR, кроме одной заявленной MAJOR-находки (Qwen,
    Q5 про CONFUSABLE_007), разобранной ниже.
  v0_1_PATCH_02 (CONFUSABLE_TYPE: FUNCTIONAL): VERIFIED_BY:
    COORDINATOR_DIRECT_FIX при применении, СЕЙЧАС подтверждён
    повторно двумя независимыми ревьюерами на уже патченой версии
    (Kimi и Qwen — Qwen явно отозвал свою исходную MAJOR-находку
    после правки, признав решение координатора корректным). Это
    не формальный отдельный конвейерный раунд с новым пакетом, но
    содержательное подтверждение на актуальной версии документа.

  v0_1_PATCH_02: CONFUSABLE_007 — добавлено поле CONFUSABLE_TYPE:
    FUNCTIONAL (координатор, 2026-06-24, по находкам раунда
    CONVEYOR_RUN_PACKET_SOLIDUS_CONTENT_REVIEW_v0_1) — разногласие
    среди 4 ревьюеров по вопросу Q5: Qwen (1/4) — MAJOR, предлагал
    перенести CONFUSABLE_007 в RISK_CASES целиком, добавить новый
    RISK_CASE_009; Grok (1/4) — без находок, оставить как есть;
    GPT-5.5 и Gemini (2/4) — TRACE_ONLY/MINOR, оставить в CONFUSABLES,
    но явно отметить функциональную (не визуальную) природу путаницы.
    РЕШЕНИЕ КООРДИНАТОРА: не голосование большинством — проверено
    по первоисточнику (SIGN_CORE_CARD_TEMPLATE_GEN3_v0_3_RU,
    SIGN_CORE_CARD_CONVEYOR_RULES_GEN3_v0_3_RU): ни шаблон, ни
    правила НЕ определяют CONFUSABLES как строго визуальную
    категорию (шаблон использует общую формулировку "похожий
    символ"). Перенос Qwen — это реструктуризация без чёткого
    основания в правилах; явная пометка типа путаницы (вариант
    GPT-5.5/Gemini) решает содержательную претензию без
    разрушительного изменения структуры.
    GOVERNANCE_GAP_NOTE (не блокирует, аналогично TEMPLATE_LINE
    несоответствию у DOT): сама формулировка CONFUSABLES в правилах
    v0_3 не уточняет, ограничена ли категория визуальными
    гомоглифами или включает функциональные путаницы — это
    открытый архитектурный вопрос для правил в целом, не для этой
    карточки. CONFUSABLE_007 — первый прецедент такого типа в
    проекте (у DOT все 6 конфузиблов были визуальными).
    VERIFIED_BY: COORDINATOR_DIRECT_FIX — NOT_CONVEYOR_VERIFIED
    (аналогично практике с DOT — тривиальная уточняющая правка,
    не блокирует переход к WORKINGLY_CLOSED).

  v0_1_PATCH_03: DOCUMENT_STATUS WORKINGLY_CLOSED →
    ARTIFACT_CONFIRMED; STATUS_PROGRESSION_TRACKER
    (SIMULATION_GATE_PASSED, ARTIFACT_CONFIRMED) приведён в
    соответствие с уже принятыми решениями
    AUTHOR_DECISION_20260625_001 (Координатор/Claude, 2026-06-25,
    retroactive fix — само решение было принято 2026-06-25 ранее
    в той же сессии, но не было применено к файлу карточки;
    обнаружено по прямому вопросу автора) — TYPE_F (fix-patch,
    governance-only, не затрагивает LAYER_A/B/C)
  v0_1_PATCH_04: LIMITATION_STATEMENT (раздел 12) обновлён —
    устаревшая строка "WORKINGLY_CLOSED ARTIFACT (до получения
    ARTIFACT_CONFIRMED)" заменена на формулировку для
    ARTIFACT_CONFIRMED (Координатор/Claude, 2026-06-25, по тому
    же retroactive fix) — TYPE_F (fix-patch, governance-only)

  GAP_SEVERITY_NOTE: в отличие от аналогичных governance-патчей у
    SKULL (v0_1_PATCH_09-11, где статусные поля были обновлены, но
    не залогированы), здесь сами статусные поля карточки не были
    обновлены вообще — то есть карточка до этого патча формально
    противоречила уже принятому AUTHOR_DECISION. Найдено и
    исправлено только по прямой повторной загрузке файла автором
    и явному вопросу о пропущенных патчах.

============================================================
12. LIMITATION_STATEMENT
============================================================

LIMITATION_STATEMENT:
  THIS_CARD IS AN ARTIFACT_CONFIRMED ARTIFACT
    (AUTHOR_DECISION_20260625_001, 2026-06-25; прошла
    STRUCTURAL_PREFLIGHT_PASS, CONVEYOR_REVIEW_PASS,
    SIMULATION_GATE TIER_2 — финальный статус для методологии
    GEN3_v0_3)
  NOT A FINAL_STANDARD
  NOT A PARSER
  NOT A RUNTIME
  NOT A SECURITY_CERTIFICATE
  NOT PRODUCTION_READY (ARTIFACT_CONFIRMED ≠ PRODUCTION_READY —
    симуляция покрыла 4 контекста, не исчерпывающее тестирование)
  CONVEYOR_PASS ≠ VALIDATION
  RUN_CARD_RESULT ≠ FINAL_STATUS
  ARTIFACT_CONFIRMED ≠ LOCKED_WORKING_CORE
  ARTIFACT_CONFIRMED ≠ SECURITY_PROOF

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
