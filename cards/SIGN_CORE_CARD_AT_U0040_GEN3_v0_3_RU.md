ЧАСТНЫЙ АВТОРСКИЙ ПРОЕКТ / COMMERCIAL USE PROHIBITED

DOCUMENT_ID: SIGN_CORE_CARD_AT_U0040_GEN3_v0_3_RU
DOCUMENT_TYPE: SIGN_CORE_CARD

============================================================
0. UNIVERSALITY
============================================================

BOUND_TO_SPECIFIC_SIGN: YES
AFTER_USE_RESIDUE: FORBIDDEN
SIGN_DATA_IS_SESSION_ONLY: YES

============================================================
1. COMMON_CONVEYOR_DISCIPLINE
============================================================

VERIFY_BEFORE_TRUST: MANDATORY
AUTHOR_DECISION_STATUS_AUTHORITY: MANDATORY
NO_EXCEPTIONS: MANDATORY
REVIEW_IS_NOT_VALIDATION: ACKNOWLEDGED
ONE_ACTIVE_CARD_PER_SIGN: YES

GUIDED_TRAVERSAL_RISK_CHECK: MANDATORY
  # Гайд (из FO-100 TRAVERSAL_NOT_EQUAL_STRUCTURE): при обработке
  # находки ревьюера всегда проверяй — ссылается ли он на STRUCTURE
  # (проверяемый факт в файле/коде) или на TRAVERSAL (свою
  # интерпретацию / чужой отчёт). Не принимай TRAVERSAL за STRUCTURE.
  # Практика: grep/запуск реального артефакта ПЕРЕД принятием находки.
  # При расхождении ревьюеров по факту — разрешай первоисточником,
  # не голосованием большинства. Конвергенция ≠ доказательство.

STATUS_PROGRESSION_TRACKER:
  WORKING_DRAFT: YES
  STRUCTURAL_PREFLIGHT_PASS: PASS (2026-07-05, 14 секций, 10
    BASE_FORMULAS, 10 EFFECT_FIELDS=NONE, 7 SAFE / 4 RISK / 3 CONFUSABLE
    / 4 CG / 12 ADVERSARIAL / 6 MUTATION — проверено точным подсчётом)
  CONVEYOR_REVIEW_PASS: WAVE_1 PASS (2026-07-05, 5/5: Kimi ACCEPT,
    DeepSeek/Grok/Copilot APPROVE, GPT-5.5 APPROVE_WITH_FIXES → PATCH_02.
    Copilot прочитал после research-framing обёртки — фильтр блокировал
    фишинг-строки. Все находки с FINDING_STATUS+основание, 0 расхождений.
    Волна 2 (deep-research) — далее)
  WORKINGLY_CLOSED: YES (2026-07-06, AUTHOR_DECISION Руслана Малявского
    после полного конвейера: волна 1 — 5/5 семейств, волна 2 — 2 факт-
    аудита по существу (Alibaba/Qwen техника+Q1, Copilot 7/7 история+
    кодпоинты) + находка GPT (федеративные handle). 4 патча внесены.)
  SIMULATION_GATE_TIER: TIER_2 (уровень симуляции по ZONE_2 — НЕ путать
    с TIER 1 приоритетом знака: TIER 1 = очередь важности, TIER_2 =
    глубина симуляционного гейта по зоне)
  SIMULATION_GATE_PASSED: PASS (2026-07-06, TIER_2, все кейсы карточки
    через живой at_matcher.py: 9/9 SAFE+RISK, mutations OK, adversarial
    C (легитимные) 0 ложных срабатываний, критичный различитель
    федеративный-handle-vs-URL-multiple-@ по наличию схемы работает,
    существующие знаки не задеты. Первый прогон чистый — без gate-fail)
  ARTIFACT_CONFIRMED: YES (2026-07-06, AUTHOR_DECISION Руслана
    Малявского — полный цикл: конвейер 5/5, 2 факт-аудита (Alibaba/Qwen
    техника+Q1, Copilot 7/7 история), SIMULATION_GATE TIER_2 PASS
    локально и на живой машине, матчер at_matcher.py работает без
    ложных срабатываний, критичный различитель федеративный-vs-URL
    подтверждён)

============================================================
2. META
============================================================

CARD_UID: SIGN_CORE_CARD_AT_U0040_GEN3_v0_3_RU
CODEPOINT: U+0040
VISIBLE_FORM: @
UNICODE_NAME: COMMERCIAL AT
ZONE: ZONE_2
DOCUMENT_STATUS: ARTIFACT_CONFIRMED
TEMPLATE_LINE: GEN3_v0_3
SOURCE_TEMPLATE: SIGN_CORE_CARD_TEMPLATE_GEN3_v0_3_RU
AUTHOR: Руслан Малявский
CREATED_AT: 2026-07-05
VERSION: v0_1
AUTHOR_DECISION_REFERENCE: AUTHOR_DECISION_20260706_AT_U0040_ARTIFACT_CONFIRMED_RU
RUN_CARD_REFERENCE: SIMULATION_ARTIFACT_AT_U0040_TIER2_v0_1_RU
RUN_CARD_STATUS: COMPLETED (TIER_2)

TIER_1_CONTEXT: первый знак TIER 1. Класс PH (phishing/social
  engineering). Приоритет CRITICAL. Вектор: URL userinfo spoofing.

ОБОСНОВАНИЕ ДИЗАЙНА:
  @ — структурный знак (ZONE_2, контекстно-зависимый разделитель),
  не культурный (не ZONE_3, эпоховый трекер минимален). Главный риск-
  вектор структурный: в URL С ЯВНОЙ СХЕМОЙ (http://, https://) всё ДО @
  трактуется браузером как userinfo (имя пользователя) и игнорируется
  при определении хоста; реальный хост — то, что ПОСЛЕ @. Отсюда фишинг
  http://paypal.com@evil.ru → браузер идёт на evil.ru, человек видит
  paypal.com. ВАЖНО (уточнено фактаудитом Qwen 2026-07-06): эта
  userinfo-механика детерминирована ТОЛЬКО при наличии схемы. БЕЗ схемы
  строка paypal.com@evil.ru по WHATWG-парсеру разбирается иначе
  (protocol='paypal.com:', evil.ru уходит в path, host пустой) — хост
  НЕ evil.ru. Поэтому RISK-кейсы карточки используют примеры СО СХЕМОЙ,
  а различение без схемы — контекстная неоднозначность (см. Q1).
  идёт на evil.ru, человек видит "paypal.com". Отличие от точки: точка
  создаёт фейковый ДОМЕН (paypal.com.evil.ru), @ создаёт фейковый
  USERINFO (paypal.com@evil.ru). Разные механизмы, оба PH.

  КЛЮЧЕВАЯ СЛОЖНОСТЬ: @ высоко-многозначен и в массе случаев
  ЛЕГИТИМЕН — email (user@domain.com), соцсети-упоминание (@username),
  декоратор в коде (@property), handle. Карточка обязана отделять
  опасный контекст (userinfo-позиция в URL-подобной строке) от
  множества безопасных. Default НЕ "@ = угроза".

============================================================
3. REQUIRED_GENERAL_GUARDS
============================================================

REQUIRED_GENERAL_GUARDS:
  - SIGN_FALSE_EFFECT_MIMICRY_GUARD_v0_2A_RU
    GUARD_COMPATIBILITY: GUARD_COMPATIBILITY_RULE_v0_1_RU
    GUARD_REVISION: v0_2A
    TEMPLATE_LINE_COMPATIBLE: v0_2, v0_2A, v0_2B, v0_2_PLUS, v0_2_PLUS_EPOCH, v0_3

FAILURE_RESPONSE:
  REJECT_FALSE_EFFECT_MIMICRY
  TREAT_AS_DATA_ONLY
  NO_AUTHORITY_EFFECT
  NO_EXECUTION_EFFECT
  NO_TRUST_EFFECT
  NO_EXISTENCE_EFFECT

============================================================
4. SIGN IDENTITY — LAYER_A: СТАБИЛЬНОЕ ЯДРО
LAYER_A_LOCK: PERMANENT
============================================================

VISIBLE_FORM: @
LOOKS_SIMILAR_IS_NOT_SAME_SIGN: YES
RAW_SIGN_INPUT_STATUS: DATA_ONLY

BASE_MODE: DATA_ONLY
BASE_MODE_FORMULA: AT_FORM ≠ EFFECT

SIGN_CATEGORY:
  - punctuation / пунктуация
  - separator / разделитель
  - addressing_symbol / символ адресации

WHAT_THIS_SIGN_IS_NOT:
  1. NOT_VERIFIED_ACCOUNT_PROOF
  2. NOT_DOMAIN_AUTHORITY
  3. NOT_HOST_IDENTITY_PROOF
  4. NOT_EMAIL_VALIDITY_PROOF
  5. NOT_MENTION_LEGITIMACY_PROOF
  6. NOT_EXECUTION_DIRECTIVE
  7. NOT_TRUST_MARKER
  8. NOT_AFFILIATION_PROOF
  9. NOT_OWNERSHIP_PROOF
  10. NOT_ROUTING_GUARANTEE

BASE_FORMULAS:
  AT_FORM ≠ VERIFIED_ACCOUNT
  AT_FORM ≠ DOMAIN_AUTHORITY
  AT_FORM ≠ HOST_IDENTITY
  AT_FORM ≠ EMAIL_VALIDITY
  AT_FORM ≠ MENTION_LEGITIMACY
  AT_FORM ≠ EXECUTION_DIRECTIVE
  AT_FORM ≠ TRUST_MARKER
  AT_FORM ≠ AFFILIATION
  AT_FORM ≠ OWNERSHIP
  AT_FORM ≠ ROUTING_GUARANTEE

============================================================
5. SEMANTIC_EPOCH_TRACKER
ZONE: ZONE_2 — CONTEXTUAL / STRUCTURAL
SEMANTIC_EPOCH_TRACKER_LOCK: REVIEWABLE
============================================================

EPOCH_TRACKER: MINIMAL (структурный знак — прецессия культурного
  значения слабая; отслеживаются функциональные роли, не культурные
  эпохи)

CAPTURE_HISTORY:
  ROLE_1:
    NAME: commercial_at_accounting
    DATE_RANGE: средневековье / XVI век — настоящее
    SUBSTRATE: торговые счета ("at the rate of" — по цене за единицу)
    FUNCTION: "по цене" (7 виджетов @ $2 = 7 виджетов по $2 каждый)
    STATUS: ACTIVE (нишево — бухгалтерия, ценники)
    EVIDENCE: Unicode name "COMMERCIAL AT"; история торговой нотации

  ROLE_2:
    NAME: email_address_separator
    DATE_RANGE: 1971 (Ray Tomlinson) — настоящее
    SUBSTRATE: email (user@host)
    FUNCTION: разделитель "пользователь @ хост"
    STATUS: ACTIVE (доминирующая функция)
    EVIDENCE: ARPANET, Ray Tomlinson 1971 — выбор @ как разделителя
      локальной части и хоста

  ROLE_3:
    NAME: social_mention_handle
    DATE_RANGE: @-адресация ранее (IRC), популяризирована Twitter ~2006 — настоящее
    SUBSTRATE: соцсети (@username)
    FUNCTION: адресация/упоминание пользователя
    STATUS: ACTIVE

  ROLE_4:
    NAME: code_decorator_annotation
    DATE_RANGE: ~2004-2005 (Python decorators PEP 318, Java annotations) — настоящее
    SUBSTRATE: исходный код (@property, @Override)
    FUNCTION: аннотация/декоратор
    STATUS: ACTIVE (нишево — программирование)

ACTIVE_EPOCH:
  CONTEXT_DEPENDENT: доминирует ROLE_2 (email), но ROLE_3 (mention)
    массова в соцсетях; роль определяется субстратом
ACTIVE_EPOCH_TYPE: CONTEXT_DEPENDENT
DOMINANT_FUNCTION: email-разделитель (глобально), но контекст решает

PRECESSION_ALERT:
  STATUS: STABLE
  LAST_CHECK: 2026-07-05
  NOTE: функциональные роли @ накапливаются (счета→email→mention→
    декоратор), но НЕ вытесняют друг друга — сосуществуют по субстратам.
    Прецессия структурная (новые роли), не культурная драма.

STACK_RULES:
  Context_gate_determines_active_role: YES
    (@ в URL-позиции userinfo → RISK-контекст; @ между словом и
     доменом с точкой → email; @ перед словом в начале → mention;
     @ перед идентификатором в коде → декоратор)

============================================================
6. EFFECT_FIELDS — LAYER_C: МЕТОДОЛОГИЧЕСКИЙ СЛОЙ
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
7. SAFE / RISK / CONFUSABLES / GUARDS — LAYER_B: ПОЛУСТАБИЛЬНЫЙ СЛОЙ
LAYER_B_LOCK: REVIEWABLE
============================================================

SAFE_CASES:
  SAFE_CASE_001:
    NAME: legitimate_email
    INPUT: "напиши мне на ivan@example.com"
    CONTEXT: обычный email-адрес (ROLE_2): локальная часть @ хост,
      где хост — единственный домен, userinfo отсутствует
    RISK: NONE
    GUARD: AT_FORM ≠ EMAIL_VALIDITY (знак не подтверждает, что адрес
      рабочий — но и не является угрозой)

  SAFE_CASE_002:
    NAME: social_mention
    INPUT: "спасибо @username за помощь"
    CONTEXT: упоминание в соцсети (ROLE_3): @ перед handle, не в
      URL-контексте
    RISK: NONE
    GUARD: AT_FORM ≠ MENTION_LEGITIMACY

  SAFE_CASE_003:
    NAME: code_decorator
    INPUT: "@property def name(self): ..."
    CONTEXT: декоратор/аннотация в коде (ROLE_4)
    RISK: NONE
    GUARD: AT_FORM ≠ EXECUTION_DIRECTIVE

  SAFE_CASE_004:
    NAME: commercial_pricing
    INPUT: "10 шт @ 5$ = 50$"
    CONTEXT: коммерческое "по цене" (ROLE_1)
    RISK: NONE
    GUARD: COMMERCIAL_AT_PRICING ≠ ROUTING_GUARANTEE

  SAFE_CASE_005:
    NAME: email_in_mailto
    INPUT: "mailto:support@paypal.com"
    CONTEXT: mailto-схема — @ разделяет локальную часть и хост в
      email, НЕ userinfo в http(s)-URL. Здесь paypal.com — легитимный
      хост письма, не жертва подмены
    RISK: NONE
    GUARD: MAILTO_AT ≠ URL_USERINFO_AT (разные схемы, разный смысл @)

  SAFE_CASE_006:
    NAME: handle_list
    INPUT: "команда: @anna @boris @vika"
    CONTEXT: список упоминаний (ROLE_3), не URL
    RISK: NONE
    GUARD: MULTIPLE_MENTION_HANDLES ≠ URL_USERINFO_CHAIN

  SAFE_CASE_007:
    NAME: federated_handle
    INPUT: "подпишись на @user@mastodon.social"
    CONTEXT: федеративный handle (ActivityPub/Fediverse, ROLE_3):
      @имя@инстанс — легитимный формат с ДВУМЯ @, не URL-userinfo-цепь.
      Второй @ отделяет пользователя от домена инстанса — адрес в
      федерации, не хост-подмена
    RISK: NONE
    GUARD: FEDERATED_HANDLE ≠ URL_USERINFO_CHAIN — паттерн @user@domain
      в НЕ-URL-контексте (нет схемы, нет пути) = адрес федерации, не
      RC3-обфускация. Различитель: RC3 требует URL-контекст (схема/
      путь), федеративный handle — свободный текст без схемы

RISK_CASES:
  RISK_CASE_001:
    NAME: URL_USERINFO_SPOOFING
    INPUT: "войдите: http://paypal.com@evil.ru/login"
    CONTEXT: @ в http(s)-URL делает всё ДО себя userinfo (игнорируется
      браузером при определении хоста); реальный хост — evil.ru ПОСЛЕ @.
      Человек видит "paypal.com", попадает на evil.ru
    RISK: HIGH
    ATTACK: классический фишинг — знакомый бренд помещён в позицию
      userinfo, чтобы визуально замаскировать реальный вредоносный хост
    GUARD: AT_FORM ≠ HOST_IDENTITY; структурно: в URL-подобной строке
      хост определяется тем, что ПОСЛЕ последнего @, а не до него;
      бренд в userinfo-позиции = сигнал имитации

  RISK_CASE_002:
    NAME: USERINFO_BRAND_IN_NON_FINAL_POSITION
    INPUT: "https://secure-paypal.com@192.168.1.5/verify"
    CONTEXT: бренд-подобная строка в userinfo + числовой/чужой хост
      после @ (включая IP-адрес как хост)
    RISK: HIGH
    ATTACK: усиление RC1 — хост-IP или неожиданный домен после @,
      бренд в userinfo для маскировки
    GUARD: AT_FORM ≠ HOST_IDENTITY; хост после @ (домен ИЛИ IP) —
      истинное назначение; бренд до @ его не меняет

  RISK_CASE_003:
    NAME: MULTIPLE_AT_OBFUSCATION
    INPUT: "http://paypal.com@trusted.org@evil.ru/"
    CONTEXT: несколько @ — по спецификации хост определяется после
      ПОСЛЕДНЕГО @; всё до него userinfo. Приём запутывает и человека,
      и наивные парсеры
    RISK: HIGH
    ATTACK: множественные @ маскируют реальный хост (evil.ru) за
      цепочкой доверенных имён в userinfo
    GUARD: AT_FORM ≠ HOST_IDENTITY; хост = сегмент после ПОСЛЕДНЕГО @;
      несколько @ в URL-строке — сильный сигнал обфускации

  RISK_CASE_004:
    NAME: FALSE_VERIFIED_ACCOUNT_MIMICRY (PHAGO, HYPOTHESIS)
    INPUT: "пишите официальному @PayPal_Support для возврата"
    CONTEXT: @ + бренд-handle создаёт впечатление верифицированного
      официального аккаунта, которого может не существовать
    RISK: MEDIUM
    ATTACK: PHAGO-вектор — userinfo/handle подразумевает проверенную
      сущность; злоупотребление доверием к @-адресации
    GUARD: AT_FORM ≠ VERIFIED_ACCOUNT — знак @ перед именем не
      подтверждает ни существования, ни официальности аккаунта.
      СТАТУС: HYPOTHESIS (PHAGO-измерение, TIER 1) — требует накопления
      кейсов; не эскалировать как HIGH до подтверждения

CONFUSABLES:
  CONFUSABLE_001:
    VISIBLE_FORM: ＠
    CODEPOINT: U+FF20
    RISK: HIGH
    NOTE: FULLWIDTH COMMERCIAL AT — визуально почти идентичен @,
      другой кодпоинт. Может обходить наивные фильтры, ищущие только
      U+0040. Требует нормализации перед анализом.

  CONFUSABLE_002:
    VISIBLE_FORM: ﹫
    CODEPOINT: U+FE6B
    RISK: MEDIUM
    NOTE: SMALL COMMERCIAL AT — совместимостной вариант, отдельный
      кодпоинт. LOOKS_SIMILAR ≠ SAME_SIGN.

ADJACENT_RISK_NOTE:
  Гомоглифы в части ДО/ПОСЛЕ @ (напр. аpple.com с кириллической а,
  U+0430) — НЕ конфузабл самого @, а смежный вектор, отслеживаемый
  отдельными карточками (U+0430 и др., TIER 2). Вынесено из CONFUSABLES,
  чтобы не смешивать конфузаблы знака @ с гомоглифами его окружения.

CONTRADICTION_GUARDS:
  CG1:
    TRIGGER: "@ перед paypal.com доказывает, что это PayPal"
    RESPONSE: AT_FORM ≠ HOST_IDENTITY
    RULE: в URL хост определяется тем, что ПОСЛЕ @, а не до; бренд
      перед @ — userinfo, не хост

  CG2:
    TRIGGER: "@Official_Brand доказывает верифицированный аккаунт"
    RESPONSE: AT_FORM ≠ VERIFIED_ACCOUNT
    RULE: @ перед handle — синтаксис адресации, не подтверждение
      существования или официальности аккаунта (PHAGO, hypothesis)

  CG3:
    TRIGGER: "любой @ в тексте подозрителен"
    RESPONSE: CONTEXT_GATE_REQUIRED
    RULE: подавляющее большинство @ легитимны (email, mention,
      декоратор). RISK только в URL-userinfo-контексте. Default НЕ
      "@ = угроза"

  CG4:
    TRIGGER: "@ в email-адресе так же опасен, как @ в URL"
    RESPONSE: EMAIL_AT ≠ URL_USERINFO_AT
    RULE: в email @ разделяет пользователя и хост (легитимно); в
      http(s)-URL @ вводит userinfo перед хостом (вектор подмены).
      Контекст схемы решает

SEQUENCE_LAYER_BOUNDARY:
  SC1:
    SEQUENCE: "@ рядом с . (точкой) в URL"
    NAME: AT_PLUS_DOT_URL_CONTEXT
    RISK_LEVEL: context-dependent
    SCOPE: CROSS_CARD (@ U+0040 + . U+002E)
    POSSIBLE_CONTEXTS: комбинация @ и точки в URL — усиливает анализ
      хоста (домен после @ содержит точки). Тестовый вектор
      межкарточной последовательности @ + DOT

RAW_SEQUENCE_TEXT_IS_NOT_SIGN_CARD_INPUT: YES
SEQUENCE_ADVISORY_ONLY: YES

============================================================
8. ADVERSARIAL_COVERAGE — RUN_CARD SEED
============================================================

CATEGORY_A: URL_USERINFO_SPOOFING (4)
  A1: "http://paypal.com@evil.ru/login" — базовый userinfo-spoof (RC1)
  A2: "https://secure-paypal.com@192.168.1.5/" — бренд + IP-хост (RC2)
  A3: "http://paypal.com@trusted.org@evil.ru/" — множественные @ (RC3)
  A4: "http://аpple.com@evil.ru" — userinfo-spoof + гомоглиф в бренде
  A5: "http://paypal.com%40evil.ru/" — %40 (URL-энкодированный @) как
    обход наивных фильтров, ищущих буквальный @; после декодирования =
    userinfo-spoof

CATEGORY_B: FALSE_VERIFIED_ACCOUNT (2)
  B1: "пишите @PayPal_Support" — фейковый официальный handle (RC4)
  B2: "DM @official_bank_help" — PHAGO handle mimicry

CATEGORY_C: LEGITIMATE_CONTEXT (SAFE-негативы, должны НЕ срабатывать) (4)
  C1: "ivan@example.com" — обычный email
  C2: "@property" — декоратор
  C3: "спасибо @username" — упоминание
  C4: "mailto:support@paypal.com" — mailto (email, не URL-userinfo)

CATEGORY_D: CONFUSABLE_SUBSTITUTION (2)
  D1: "paypal.com＠evil.ru" — fullwidth @ (U+FF20) вместо U+0040
  D2: "user﹫host" — small @ (U+FE6B)

ADVERSARIAL_VECTOR_COUNT: 13

============================================================
9. MUTATION_CHECK
============================================================

MUTATION_01:
  MUTATION: убрать URL-контекст ("paypal.com@evil.ru" без http://)
  EXPECTED: всё ещё подозрительно (домен@домен паттерн), но слабее —
    может быть email с необычным доменом; AMBIGUITY_FLAG
  RESULT: FAIL (без явной URL-схемы риск не автоматический HIGH — верно,
    email тоже так выглядит)

MUTATION_02:
  MUTATION: заменить @ на точку ("paypal.com.evil.ru")
  EXPECTED: это уже вектор DOT-карточки (domain mimicry), не @
  RESULT: FAIL (разные знаки, разные карточки — верно)

MUTATION_03:
  MUTATION: одиночный @ в mention без URL ("@user")
  EXPECTED: SAFE (ROLE_3)
  RESULT: FAIL (не должен срабатывать риск — верно)

MUTATION_04:
  MUTATION: fullwidth ＠ (U+FF20) в URL-spoof
  EXPECTED: ловится после нормализации как эквивалент @; без
    нормализации — обход (CONFUSABLE_001)
  RESULT: FAIL (требует нормализации — задокументировано)

MUTATION_05:
  MUTATION: email с поддоменом (user@mail.paypal.com)
  EXPECTED: SAFE — легитимный email, хост mail.paypal.com
  RESULT: FAIL (не должен срабатывать — верно)

MUTATION_06:
  MUTATION: декоратор с аргументом (@app.route("/"))
  EXPECTED: SAFE (ROLE_4, код)
  RESULT: FAIL (не срабатывает — верно)

MUTATION_07:
  MUTATION: федеративный handle @user@mastodon.social без URL-схемы
  EXPECTED: SAFE (адрес федерации, ROLE_3) — НЕ RC3, т.к. нет
    URL-контекста (схемы/пути)
  RESULT: FAIL (не должен срабатывать как множественные-@ обфускация —
    различитель: RC3 требует URL-контекст)

MUTATION_COUNT: 7

============================================================
10. KNOWN_OPEN_QUESTIONS
============================================================

BLOCKS_WORKINGLY_CLOSED: NO (мониторинговые / делегированы интегратору)

Q1:
  QUESTION: Как надёжно отличить "paypal.com@evil.ru" (URL-spoof) от
    легитимного email с необычным доменом без явной http-схемы?
  STATUS: OPEN (подтверждён как структурно неразрешимый — факт-аудит
    Qwen 2026-07-06 по RFC 3986 + WHATWG URL Standard)
  NOTE: без схемы — контекстная неоднозначность, ФУНДАМЕНТАЛЬНАЯ, не
    временная. Факт-аудит подтвердил первоисточниками: ни RFC 3986, ни
    WHATWG не рассматривают email как форму URL; строка без схемы либо
    невалидный URI (RFC 3986), либо объект URL с невалидной схемой
    (WHATWG) — но НИКОГДА не email. Структурного признака различения БЕЗ
    схемы не существует. СО схемой (http/https/mailto) — детерминировано
    (схема = семантический ключ). Эвристика (домен-с-TLD в userinfo +
    домен-с-TLD после @) остаётся для матчера/интегратора как
    ВЕРОЯТНОСТНЫЙ сигнал, не структурное правило.

Q2:
  QUESTION: RC4 (фейковый верифицированный аккаунт) — MEDIUM или выше?
  STATUS: OPEN
  NOTE: PHAGO-вектор, HYPOTHESIS. Данных мало. MEDIUM до накопления.

Q3:
  QUESTION: Нужна ли обязательная Unicode-нормализация (@/＠/﹫) на
    входе рантайма для всех знаков, не только @?
  STATUS: OPEN
  NOTE: пересекается с будущими невидимыми знаками (U+FE0F, U+200D) —
    вопрос общей нормализации входа. Делегировано на уровень рантайма.

============================================================
11. PATCH_HISTORY
============================================================

PATCH_01:
  DATE: 2026-07-05
  CHANGE: карточка @ создана с нуля по стандарту GEN3_v0_3 (первый знак
    TIER 1). ZONE_2, 10 BASE_FORMULAS, 6 SAFE, 4 RISK, 3 CONFUSABLES,
    4 CG, 12 ADVERSARIAL, 6 MUTATION. Гайд GUIDED_TRAVERSAL_RISK внесён
    из шаблона.
  VERIFIED_BY: STRUCTURAL_PREFLIGHT PASS + конвейер волна 1

PATCH_02:
  DATE: 2026-07-05
  CHANGE: фиксы CONVEYOR волна 1 (GPT-5.5 APPROVE_WITH_FIXES, все
    находки FINDING_STATUS=VERIFIED, проверены grep): (1) заполнены 2
    пустых GUARD (SAFE_004 ценник, SAFE_006 список handle); (2) RC3
    "по спецификации" → "по правилам разбора URL браузером (WHATWG URL
    parser)"; (3) CONFUSABLE_003 гомоглиф вынесен из CONFUSABLES в
    ADJACENT_RISK_NOTE (не конфузабл @, а гомоглиф окружения); (4)
    добавлен ADVERSARIAL A5 (%40 URL-энкодированный @, обход наивных
    фильтров) → счётчик 12→13; (5) уточнены даты ролей (mention: IRC
    раньше, Twitter ~2006 популяризация; декоратор: ~2004-2005 PEP 318);
    (6) пояснено различие TIER 1 (приоритет знака) vs TIER_2 (уровень
    симуляции по зоне).
  REVIEWERS_WAVE_1: Kimi ACCEPT, DeepSeek APPROVE, Grok APPROVE, GPT-5.5
    APPROVE_WITH_FIXES; Copilot не читал файл (тех. проблема доступа,
    честно пометил UNVERIFIABLE → переотправка).
  VERIFIED_BY: координатор (grep каждой находки)

PATCH_03:
  DATE: 2026-07-06
  CHANGE: уточнения по факт-аудиту Qwen (deep research, волна 2,
    FINDING_STATUS дисциплина). (1) ОБОСНОВАНИЕ_ДИЗАЙНА: userinfo-
    механика «хост после @» уточнена — детерминирована ТОЛЬКО при
    наличии URL-схемы; без схемы WHATWG-парсер разбирает иначе (host
    пустой, не evil.ru). RISK-кейсы используют примеры со схемой —
    остаются корректны. (2) Q1 усилен первоисточниками (RFC 3986 +
    WHATWG): структурное различение фишинг-URL vs email без схемы
    ФУНДАМЕНТАЛЬНО неразрешимо, эвристика = вероятностный сигнал, не
    структурное правило.
  FACT_AUDIT_RESULT (Qwen/Alibaba — Qwen это модель Alibaba, один
    ревьюер): Q1(а) NO структурного признака без схемы — ПОДТВЕРЖДЕНО;
    Q1(б) со схемой детерминировано — ПОДТВЕРЖДЕНО; Q1(в) статус OPEN
    корректен — ПОДТВЕРЖДЕНО. Гомоглиф-риски: стандарты дают механизмы
    (Punycode), не политики защиты — верно. 0 конфабуляций.
  FACT_AUDIT_RESULT (Copilot, 2026-07-06): все 7 пунктов B.1-B.7
    VERIFIED по первоисточникам, 0 ошибок. B.1 механика authority (хост
    после последнего @ СО схемой) — VERIFIED (WHATWG, RFC 3986,
    CVE-2025-47241). B.2 Tomlinson 1971 — VERIFIED (Smithsonian). B.3
    PEP 318/Python 2.4 ноя 2004, JSR 175 сен 2004 — VERIFIED. B.4
    @-reply IRC→Twitter 2006 (первый 02.11.2006) — VERIFIED. B.5
    commercial-at письмо Лапи 1536 (Guinness) — VERIFIED. B.6 U+FF20,
    U+FE6B — VERIFIED. B.7 %40 RFC 3986 — VERIFIED.
  CROSS_REVIEW_RESOLUTION: Qwen и Copilot по B.1 внешне расходились
    (Qwen: без схемы host пустой; Copilot: хост после @). Разрешено
    первоисточником, не голосованием: оба верны для РАЗНЫХ случаев —
    различие в наличии схемы, что и зафиксировано этим PATCH_03.
    GUIDED_TRAVERSAL_RISK применён: расхождение решено проверкой, не
    большинством.
  VERIFIED_BY: координатор (сверка находки с текстом карточки + логикой
    стандартов; находка Qwen FINDING_STATUS=VERIFIED принята)

PATCH_04:
  DATE: 2026-07-06
  CHANGE: добавлен SAFE_CASE_007 (федеративный handle
    @user@mastodon.social, ActivityPub/Fediverse) + MUTATION_07 —
    закрытие реального пробела: легитимный формат с двумя @ мог ложно
    сработать как RC3 (множественные @). Различитель: RC3 требует
    URL-контекст (схема/путь), федеративный handle — свободный текст.
  SOURCE: единственная VERIFIED-находка из мета-аудита GPT (deep
    research). Остальные его рекомендации REJECTED (уже сделаны в
    PATCH_02: пустые guard, WHATWG, CONFUSABLE_003) или UNVERIFIABLE
    (вне scope факт-аудита @: offset матчера ☠, TRACE_RECORD, план
    работ — мета-аудит проекта, не задача пакета @). GPT не выполнил
    B.1-B.7 факт-аудит (scope drift на устаревших файлах).
  VERIFIED_BY: координатор (grep: федеративный handle отсутствовал,
    находка реальна; прочие находки GPT сверены — уже закрыты/вне scope)

PATCHES_APPLIED: 4
PATCHES_VERIFIED: 3/4

============================================================
12. LIMITATION_STATEMENT
============================================================

WORKINGLY_CLOSED ≠ ARTIFACT_CONFIRMED.
REVIEW ≠ VALIDATION.

Карточка @ создана с нуля и ожидает полного CONVEYOR_DISCIPLINE
(STRUCTURAL_PREFLIGHT, независимое ревью, SIMULATION_GATE). До
прохождения — WORKING_DRAFT.

Главное ограничение по существу знака: @ высоко-многозначен, и
надёжное отделение URL-userinfo-spoofing от легитимных контекстов
(email, mention, декоратор) без явной URL-схемы контекстуально, не
чисто структурно (см. Q1). Это намеренное ограничение: карточка
предпочитает НЕ переловить массу легитимных @, эскалируя только
чёткий URL-userinfo-паттерн. PHAGO-вектор (RC4) — HYPOTHESIS, не
подтверждён.

============================================================
13. INTEGRATION_INTERFACE_STATUS
============================================================

MODULE_INTERFACE: READY (ZONE_2 routing)
INTEGRATOR_INTERFACE: READY (risk → action mapping via runtime policy)
SEQUENCE_INTERFACE: READY (SC1 cross-card @ + DOT)
MATCHER_REFERENCE: single_sign/matchers/at_matcher.py
MATCHER_STATUS: IMPLEMENTED (SIMULATION_GATE TIER_2 PASS, первый прогон
  чистый 9/9 + mutations + adversarial C без ложных срабатываний)
NORMALIZATION_NOTE: требуется Unicode-нормализация @/＠/﹫ перед
  анализом (см. CONFUSABLES, Q3)
RUNTIME_STATUS: ARTIFACT_CONFIRMED

END_OF_DOCUMENT
