ЧАСТНЫЙ АВТОРСКИЙ ПРОЕКТ / COMMERCIAL USE PROHIBITED

CARD_UID: SIGN_CORE_CARD_BYTE_ORDER_MARK_UFEFF_GEN3_v0_1_RU
CODEPOINT: U+FEFF
VISIBLE_FORM: ﻿
INSPECTION_LABEL: ⟦BOM U+FEFF⟧
  [поле-метка для чтения глазами: VISIBLE_FORM выше содержит ЛИТЕРАЛЬНЫЙ
   невидимый U+FEFF (рантайм сканит text по нему). Прочитать VISIBLE_FORM
   человек не может — INSPECTION_LABEL закрывает трещину пробы.]
UNICODE_NAME: ZERO WIDTH NO-BREAK SPACE
COMMON_NAME: BYTE ORDER MARK (BOM) — современная основная роль
ZONE: ZONE_2
DOCUMENT_STATUS: WORKING_DRAFT
LIFECYCLE_STATUS: WORKING_DRAFT
  [РЕАЛЬНАЯ позиция: карточка №3 поднадзорного класса невидимых, создана из образца.
   НЕ прошла ни STRUCTURAL_PREFLIGHT, ни конвейер — честный WORKING_DRAFT. Содержание
   слоёв B/RISK/RELATIONS — на ИЗМЕРЕННОМ прогоне штатного analyze() (проба 2026-07-18,
   ENGINE-verified), не на догадке; полной двуногой TIER_2-батареи ещё нет.]
VALIDATION_METHOD: SINGLE_LEG_ENGINE_PROBE (BY_CODE, штатный analyze; двуногой BY_SPEC нет)
CLASS_ROLE: CLASS_SPREAD_SPECIMEN
  [третий знак класса; даёт классу ТРЕТИЙ, непохожий профиль — ZWSP РВЁТ (break),
   ZWJ СКЛЕИВАЕТ (join), BOM = СЛУЖЕБНЫЙ МАРКЕР потока/файла, легитимность в ПОЗИЦИИ
   (первый символ), а не в функции. Для классового гарда нужен именно этот разброс.]
PRINCIPLE_CARRIER: THREE_LEVEL_SIGNAL_v0 (ПЕРВЫЙ НОСИТЕЛЬ)
  [эта карточка — первое применение принципа ТРЁХУРОВНЕВОЙ СИГНАЛИЗАЦИИ (принят
   автором 2026-07-18): тревога свидетеля = ЧИСТО / ВОЗМОЖНАЯ ОПАСНОСТЬ / РЕАЛЬНАЯ
   ОПАСНОСТЬ, не бинарно. Здесь принцип применён на СУЩЕСТВУЮЩИХ выходах рантайма
   (pass=ЧИСТО / queue=ВОЗМОЖНАЯ / hold=РЕАЛЬНАЯ). Полное закрепление принципа
   (foundation-документ, риск-градация класса 138, рантайм) — ОТДЕЛЬНЫЙ заход.
   См. секцию 7A ниже + THREE_LEVEL_DIVERGENCE.]
TEMPLATE_LINE: GEN3_v0_3
SOURCE_TEMPLATE: SIGN_CORE_CARD_ZERO_WIDTH_JOINER_U200D_GEN3_v0_1_RU (метод-образец №2)
AUTHOR: Руслан Малявский
CREATED_AT: 2026-07-18
VERSION: v0_1
AUTHOR_DECISION_REFERENCE: foundation_layer/AUTHOR_DECISION_20260712_INVISIBLE_SIGNS_D-INV-1_2_3.md
AUTHOR_DECISION_REFERENCE_CLASS: foundation_layer/AUTHOR_DECISION_20260716_D-NEIGHBORS-BORDER-138.md
  (BOM ∈ поднадзорный класс 138 = Cf∧Default_Ignorable; один из 5 образцов карточки ZWSP)
RUN_CARD_REFERENCE: scratchpad-проба 2026-07-18 (bom_probe.py / bom_temp_card_measure.py) —
  ЭФЕМЕРНАЯ; персистентный артефакт будет при постройке BOM-батареи.
RUN_CARD_STATUS: PROBE_DONE (штатный analyze, контексты измерены: mid-host→hold,
  токен/email/ведущий-домен→queue, free-text/json-ведущий→pass). НЕ полная TIER_2-батарея —
  двуногого BY_SPEC+reconcile+mutation-adequacy для BOM ещё нет; не выдаётся за ARTIFACT.
BY_SPEC_STATUS: NOT_AVAILABLE (ноги BY_SPEC нет; двуногость/reconcile НЕ утверждаются)
PATH_TO_ARTIFACT:
  1. WORKING_DRAFT — ДОСТИГНУТО (эта карточка, на измеренной пробе).
  2. STRUCTURAL_PREFLIGHT_PASS + CONVEYOR_REVIEW — PENDING.
  3. персистентная BOM-батарея (двуногая) + mutation-adequacy — PENDING.
  4. INVISIBLE_DEFAULT_IGNORABLE_GUARD (из >=3 знаков: ZWSP+ZWJ+BOM — теперь набор ПОЛОН) — CLASS_FRONT.
  5. → WORKINGLY_CLOSED → ARTIFACT_CONFIRMED.
DISPLAY_NAME: маркер порядка байт (byte order mark)

============================================================
1. UNIVERSALITY / CONVEYOR_DISCIPLINE
============================================================
BOUND_TO_SPECIFIC_SIGN: YES
AFTER_USE_RESIDUE: FORBIDDEN
SIGN_DATA_IS_SESSION_ONLY: YES
STATUS_PROGRESSION_TRACKER:
  WORKING_DRAFT: YES (создана 2026-07-18 из образца; не прошла preflight/конвейер)
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
    [ОТКРЫТЫЙ ФРОНТ: классовый гард невидимых. BOM — ТРЕТИЙ из >=3 знаков, нужных
     для его постройки без переобучения. С ZWSP+ZWJ+BOM набор образцов ПОЛОН (рвёт/
     склеивает/маркер) — можно строить гард. Ссылка = маркер незакрытой зависимости.]
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
VISIBLE_FORM: ﻿  (литеральный U+FEFF; см. INSPECTION_LABEL выше)
LOOKS_SIMILAR_IS_NOT_SAME_SIGN: NO
  [знак невидим — «похожесть» неприменима; отношения ниже строятся НЕ на визуальном
   сходстве, а на разрыве границы / классе фильтра / отсутствии / позиции]
RAW_SIGN_INPUT_STATUS: DATA_ONLY
BASE_MODE: DATA_ONLY_INVISIBLE_CONTROL
BASE_MODE_FORMULA: BOM_FORM ≠ EFFECT
SIGN_CATEGORY:
  - format_control (Unicode Cf)
  - invisible / zero-advance-width
  - default_ignorable_code_point
  - byte_order_mark (основная современная роль: маркер начала файла/потока)
  - join_control: NO (в отличие от ZWJ; и не break-opportunity, в отличие от ZWSP)
WHAT_THIS_SIGN_IS_NOT:
  1. NOT_SPACE (U+0020 — имеет ширину и рендерится)
  2. NOT_A_CANON_IT_MIMICS (не изображает никакой видимый знак)
  3. NOT_REMOVABLE_BY_NFC_NFD_NFKC_NFKD (переживает всю нормализацию)
  4. NOT_A_VISIBLE_GLYPH (нулевая ширина, читателю не виден)
  5. NOT_A_BREAK_OPPORTUNITY (это ZWSP U+200B — иная функция; BOM не даёт разрыв)
  6. NOT_A_JOINER (это ZWJ U+200D; BOM Join_Control=NO, соединения форм не требует)
  7. NOT_A_WORD_JOINER (U+2060 — актуальная замена устаревшей no-break роли BOM с Unicode 3.2)
  8. NOT_SEMANTIC_CONTENT (читателю ничего не сообщает; это маркер потока, не текст)
  9. NOT_SAFE_TO_DELETE_UNCONDITIONALLY (ведущий BOM — легитимный маркер файла; слепое
     удаление может сломать ожидания парсера — но и присутствие в середине подозрительно)
  10. NOT_AN_AUTHORITY_OR_EXECUTION_BEARER
BASE_FORMULAS:
  BOM_FORM ≠ EFFECT
  BOM_FORM ≠ SPACE
  INVISIBLE ≠ ABSENT
  BOM_FORM ≠ CANON
  NFKC_SURVIVAL ≠ LEGITIMACY
  BOM_POSITION_MATTERS (легитимность ПОЗИЦИОННА: первый символ ≠ середина)
  BOM ≠ AUTHORITY
  PRESENCE_IN_TOKEN ≠ TOKEN_STRUCTURE
  BOM_FORM ≠ VISUAL_MIMICRY
  LEADING_BOM ≠ FREE_TO_IGNORE (частый легитимный ≠ безопасный: не освобождается)

============================================================
5. SEMANTIC_EPOCH_TRACKER  (ZONE_2)
SEMANTIC_EPOCH_TRACKER_LOCK: REVIEWABLE
============================================================
EPOCH_TRACKER: CONTEXT_GATE_REQUIRED
APPLICABILITY: APPLICABLE
REASON: у знака три substrate: сигнальный (BOM — маркер порядка байт/кодировки в начале
  потока), устаревший типографический (zero-width no-break space), машинный (диверсия
  точного совпадения / parser-desync — как у ZWSP).
CAPTURE_HISTORY:
  EPOCH_1:
    DATE_RANGE: ~1991 (Unicode 1.0) — настоящее время
    SUBSTRATE: устаревшая типографика (zero-width no-break space)
    FUNCTION: неразрывный пробел нулевой ширины (склейка без разрыва)
    EVIDENCE: Unicode Standard; ДЕПРЕКЕЙТ с Unicode 3.2 в пользу U+2060 WORD JOINER
    STATUS: DEPRECATED
  EPOCH_2:
    DATE_RANGE: ~1996 (Unicode 2.0, UTF-16/UTF-8) — настоящее время
    SUBSTRATE: сигнал кодировки / порядка байт в НАЧАЛЕ файла/потока
    FUNCTION: Byte Order Mark — первый символ помечает UTF-16 BE/LE или UTF-8-поток
    EVIDENCE: Unicode Standard (BOM); практика редакторов/тулчейнов
    STATUS: ACTIVE_LEGITIMATE_AT_STREAM_START
  EPOCH_3:
    DATE_RANGE: ~2000-е — настоящее время (эпоха фильтр-эвазии)
    SUBSTRATE: латинские машинные строки (домены, идентификаторы, код)
    FUNCTION: невидимая ДИВЕРСИЯ точного совпадения В СЕРЕДИНЕ токена + PARSER-DESYNC
      (часть парсеров BOM режут, часть нет → рассинхрон представления)
    EVIDENCE: практика фильтр-эвазии; проба детектора 2026-07-18
    STATUS: ACTIVE_ATTACK
ACTIVE_EPOCH:
  STATUS: CONTEXT_GATE_REQUIRED
  PRIMARY_ACTIVE_EPOCH: NONE_GLOBAL
  POSITION_GATE: LEADING → EPOCH_2 (легитимный маркер); MID_STREAM → EPOCH_3 (диверсия)
LAYER_ANOMALY:
  ABSENT_PHYSICAL_LAYER: YES (цифровой генезис; управляющий символ; глифа не было НИКОГДА)
  NOTE: чистый цифровой контроль; смысл — в ПОЗИЦИИ в потоке, не в форме
STACK_RULES:
  Higher_epoch_suppresses_lower_in_modern_contexts: PARTIAL
  Lower_epoch_may_reactivate_in_historical_or_specialized_contexts: YES
  Context_gate_determines_active_epoch: REQUIRED
  Position_gate_determines_legitimacy: REQUIRED (уникально для BOM)
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
    INPUT: ведущий BOM в начале обычного текстового файла ("﻿hello world")
    CONTEXT: ведущая позиция (маркер файла)
    THREE_LEVEL: ВОЗМОЖНАЯ ОПАСНОСТЬ (не ЧИСТО!)
    EXPECTED: NOTICE (тихо, «посмотри при случае»)
    RISK: POSSIBLE
    GUARD: LEADING_BOM ≠ FREE_TO_IGNORE
    SEMANTIC_STATUS: FREQUENT_LEGITIMATE_BUT_NOT_FREED
      [осознанный авторский выбор: ведущий BOM ЧАСТО легитимен (маркер), НО НЕ
       освобождается — частота = поверхность атаки. Это НЕ «детектор не смог отличить»,
       а «решили не освобождать». Первое применение принципа трёх уровней.]
    OBSERVATION_LEVEL: APPLICATION_STRING_NOT_TRANSPORT_STREAM
      [ключ уровня — УРОВЕНЬ НАБЛЮДЕНИЯ, не только позиция. Прикладная строка ≠
       транспортный поток: легитимный транспортный BOM живёт в НАЧАЛЕ ФАЙЛА/ПОТОКА
       и обязан быть СЪЕДЕН транспортным слоем (декодером) ДО прикладного уровня.
       BOM, ДОЖИВШИЙ до прикладной строки с обычным текстом, — уже наблюдение:
       либо огрех конвейера данных, либо маскировка под «легитимный маркер».
       Поэтому ведущий-BOM-в-тексте = ВОЗМОЖНАЯ, не ЧИСТО. Вывод НЕ выводится из
       голых свойств знака («ведущий = легитимный маркер» даёт ложное ЧИСТО):
       слепая нога BY_SPEC дала ЧИСТО 5/5; уровень наблюдения независимо назвали
       2 ревьюера (GPT, Kimi) — RECONCILE_BYSPEC_ZWJ_BOM_2026-07-18.]
    RUNTIME_VERIFIED: YES [проба 2026-07-18: "﻿hello world" → BYTE_EXACT_TOKEN →
      queue_for_review. queue = уровень ВОЗМОЖНАЯ ОПАСНОСТЬ. Не pass (дыра закрыта),
      не hold (сигнал не топится).]
  SAFE_CASE_002:
    INPUT: ведущий BOM перед JSON/структурой ("﻿{"key":"value"}")
    CONTEXT: ведущая позиция + структурированный текст
    THREE_LEVEL: ЧИСТО [расхождение с ранним желаемым СНЯТО — см. ниже]
    EXPECTED: INFO/pass
    RISK: NONE
    OBSERVATION_LEVEL: TRANSPORT_LIKE_POSITION
      [зеркало SAFE_CASE_001: ведущий BOM непосредственно перед структурой (json/
       файл-поток) читается как ТРАНСПОРТНАЯ позиция — каноническое место легитимного
       маркера кодировки. Здесь «ведущий = легитимный» работает → ЧИСТО.
       Раннее желаемое автора было ВОЗМОЖНАЯ (см. историю в THREE_LEVEL_DIVERGENCE);
       после reconcile BY_SPEC (обоснование «прикладная строка ≠ транспортный поток»,
       2 независимых ревьюера) автор принял контекст-деление кода: текст→ВОЗМОЖНАЯ,
       транспортная структура→ЧИСТО. RECONCILE_BYSPEC_ZWJ_BOM_2026-07-18, точка B1.]
    RUNTIME_VERIFIED: YES [проба: "﻿{...}" → FREE_TEXT → pass = ЧИСТО. Совпадает
      с описанием после уточнения уровня наблюдения.]
  SAFE_CASE_003:
    INPUT: «символ BOM имеет кодпоинт U+FEFF» (упоминание знака)
    CONTEXT: учебный/цитирование
    THREE_LEVEL: ЧИСТО
    EXPECTED: INFO
    RISK: NONE
    GUARD: mention ≠ use
  SAFE_CASE_004:
    INPUT: намеренный BOM в строковом литерале кода (тест-фикстура кодировки)
    CONTEXT: исходный код с явным намерением
    THREE_LEVEL: ЧИСТО (в FREE_TEXT)
    EXPECTED: INFO
    RISK: NONE
    GUARD: BOM_FORM ≠ EFFECT
RISK_CASES:
  [RISK_CASE_RUNTIME_STATUS: VERIFIED — кейс РЕАЛЬНО срабатывает прогоном (проба
   2026-07-18); уровень RISK = то, что ВЫДАЁТ детектор. THREE_LEVEL — уровень принципа,
   измеренный (не желаемый; расхождения желаемое↔измеренное — в THREE_LEVEL_DIVERGENCE).]
  RISK_CASE_001:
    NAME: DOMAIN_LABEL_BOM_EVASION
    INPUT: pay﻿pal.com (BOM в середине метки хоста)
    CONTEXT: HOST
    THREE_LEVEL: РЕАЛЬНАЯ ОПАСНОСТЬ
    RISK: HIGH
    RUNTIME_STATUS: VERIFIED [проба: pay<BOM>pal.com → HOST / hold_pending_review]
    ATTACK: невидимая вставка в метку рвёт точное совпадение — byte-exact блоклист
      промахивается мимо домена (BOM в середине легитимной функции не имеет)
    GUARD: ось «отношение», ребро BOUNDARY_DISRUPTOR, scope HOST
  RISK_CASE_002:
    NAME: HOST_TLD_BOM_EVASION
    INPUT: paypal﻿.com (BOM между меткой и TLD)
    CONTEXT: HOST
    THREE_LEVEL: РЕАЛЬНАЯ ОПАСНОСТЬ
    RISK: HIGH
    RUNTIME_STATUS: VERIFIED [проба: paypal<BOM>.com → HOST / hold_pending_review]
    ATTACK: разрыв на границе метка/TLD
    GUARD: BOUNDARY_DISRUPTOR, scope HOST
  RISK_CASE_003:
    NAME: KEYWORD_TOKEN_BOM_SPLIT
    INPUT: bad﻿word / user﻿name (BOM в токене/идентификаторе)
    CONTEXT: BYTE_EXACT_TOKEN
    THREE_LEVEL: измерено ВОЗМОЖНАЯ; ЖЕЛАЕМО РЕАЛЬНАЯ (см. THREE_LEVEL_DIVERGENCE)
    RISK: MEDIUM (измерено)
    RUNTIME_STATUS: VERIFIED [проба: bad<BOM>word → BYTE_EXACT_TOKEN / queue_for_review]
    ATTACK: разрыв ключевого слова/идентификатора обходит policy точного совпадения
    GUARD: BOUNDARY_DISRUPTOR, scope BYTE_EXACT_TOKEN
    NOTE: автор дизайнил это как РЕАЛЬНАЯ (hold); рантайм даёт queue (ВОЗМОЖНАЯ).
      Эскалация до hold требует рантайм-риск-мэппинга (задевает ZWSP) — OPEN, не тут.
  RISK_CASE_004:
    NAME: EMAIL_LOCAL_BOM_SPLIT
    INPUT: us﻿er@example.com (BOM в локальной части)
    CONTEXT: EMAIL
    THREE_LEVEL: измерено ВОЗМОЖНАЯ; ЖЕЛАЕМО РЕАЛЬНАЯ
    RISK: MEDIUM (измерено)
    RUNTIME_STATUS: VERIFIED [проба: us<BOM>er@example.com → EMAIL / queue_for_review]
    ATTACK: split локальной части email
    GUARD: BOUNDARY_DISRUPTOR, scope EMAIL
  RISK_CASE_005:
    NAME: LEADING_BOM_BEFORE_DOMAIN
    INPUT: ﻿paypal.com (ведущий BOM перед целым доменом)
    CONTEXT: HIDDEN_BOUNDARY_PADDING
    THREE_LEVEL: измерено ВОЗМОЖНАЯ; ЖЕЛАЕМО РЕАЛЬНАЯ
    RISK: MEDIUM (измерено)
    RUNTIME_STATUS: VERIFIED [проба: <BOM>paypal.com → HIDDEN_BOUNDARY_PADDING / queue]
    ATTACK: невидимый ведущий маркер у домена — не разрыв метки, но и не молчаливый PASS
    GUARD: BOUNDARY_DISRUPTOR, scope HIDDEN_BOUNDARY_PADDING
  RISK_CASE_006:
    NAME: PARSER_DESYNC
    INPUT: BOM там, где один парсер его срежет, другой оставит (рассинхрон представления)
    CONTEXT: BYTE_EXACT_TOKEN
    THREE_LEVEL: желаемо РЕАЛЬНАЯ (вектор реален), но РАНТАЙМ-СТАТУС PENDING
    RISK: NONE (измерено — рантайм этот вектор пока не наблюдает)
    RUNTIME_STATUS: PENDING
      [ЧЕСТНО: рассинхрон парсеров — свойство ВНЕШНИХ систем, не наблюдаемо из одной
       входной строки текущим детектором. Вектор описан, за работающий контракт НЕ
       выдаётся; риска не эмитит. Ждёт отдельного захода.]
    ATTACK: BOM вызывает расхождение того, что «видят» разные парсеры одного потока
    GUARD: ребро INVISIBLE_CLASS_COLLISION (TARGET_KIND: CLASS) — кандидат

7A. THREE_LEVEL_SIGNAL — ПРИМЕНЕНИЕ ПРИНЦИПА (первый носитель)
------------------------------------------------------------
Принцип (принят автором 2026-07-18): тревога = ЧИСТО / ВОЗМОЖНАЯ / РЕАЛЬНАЯ.
Применён на СУЩЕСТВУЮЩИХ выходах рантайма (рантайм НЕ менялся):
  ЧИСТО            = pass                 (BOM нет / FREE_TEXT)
  ВОЗМОЖНАЯ ОПАСНОСТЬ = queue_for_review  (тихо, «посмотри»; не дыра, не топит сигнал)
  РЕАЛЬНАЯ ОПАСНОСТЬ  = hold_pending_review (громко, приоритет)
Ключ честности BOM: ведущий BOM (частый легитимный маркер) НЕ уходит в pass (дыра
закрыта) — он в ВОЗМОЖНОЙ ОПАСНОСТИ (queue). Максимально закрыто + сигнал не топится.

THREE_LEVEL_DIVERGENCE (желаемое автором ↔ измеренное рантаймом — честно;
  исходно 5, ОСТАЛОСЬ 4 после reconcile BY_SPEC 2026-07-19):
  Совпало (5): mid-host→РЕАЛЬНАЯ; host/tld→РЕАЛЬНАЯ; free-text→ЧИСТО;
    ведущий-текст→ВОЗМОЖНАЯ; хвостовой→ВОЗМОЖНАЯ.
  РАСХОЖДЕНИЯ (4) — ЖЕЛАЕМО РЕАЛЬНАЯ, ИЗМЕРЕНО ВОЗМОЖНАЯ (queue, не hold):
    токен, идентификатор, email, ведущий-перед-доменом. [остаются OPEN → O1]
  СНЯТО (1): «ведущий BOM перед JSON — желаемо ВОЗМОЖНАЯ, измерено ЧИСТО» — снято
    ПРАВКОЙ ОПИСАНИЯ, не кода: уровень наблюдения (прикладная строка ≠ транспортный
    поток) делает измеренное ЧИСТО корректным для транспортной позиции; см.
    SAFE_CASE_002 / RECONCILE_BYSPEC_ZWJ_BOM_2026-07-18 точка B1.
  ПРИЧИНА: рантайм присваивает уровень по КОНТЕКСТУ (только HOST→hold; BYTE_EXACT_TOKEN/
    EMAIL/HIDDEN_BOUNDARY_PADDING→queue; FREE_TEXT→pass). Карточка гейтит срабатывание
    ребра, но НЕ поднимает серьёзность. Эскалация желаемого требует пересмотра рантайм-
    риск-мэппинга (context→severity) — ЗАДЕВАЕТ ZWSP (те же контексты) → контаминация
    верифицированных 21/21. Поэтому НЕ делается тут.
  СТАТУС: OPEN — привязано к застолблённому вопросу «риск-градация класса 138 +
    нужен ли рантайм-уровень». Карточка фиксирует ИЗМЕРЕННОЕ, желаемое = документированный OPEN.

CONFUSABLES:
  NOT_APPLICABLE:
    REASON: у невидимого знака НЕТ визуальных двойников. Рантайм читает только SIGN_RELATIONS.
    REVIEW_REQUIRED: YES
  FUNCTIONAL_NEIGHBORS:
    [ТЕРМИН (канон 2026-07-16): BOM — ОБРАЗЕЦ поднадзорного класса (Cf∧DI=138,
     D-NEIGHBORS-BORDER-138). Поле СТРУКТУРНОЕ (шаблон); справочный блок для человека,
     рантайм риск по нему НЕ считает.]
    NEIGHBOR_001:
      CODEPOINT: U+200B
      NAME: ZERO WIDTH SPACE (ZWSP)
      FUNCTION_DIFF: ZWSP — ВОЗМОЖНОСТЬ разрыва; BOM — маркер потока, не разрыв
    NEIGHBOR_002:
      CODEPOINT: U+200D
      NAME: ZERO WIDTH JOINER (ZWJ)
      FUNCTION_DIFF: ZWJ склеивает формы (Join_Control=YES); BOM Join_Control=NO
    NEIGHBOR_003:
      CODEPOINT: U+2060
      NAME: WORD JOINER (WJ)
      FUNCTION_DIFF: WJ — АКТУАЛЬНАЯ замена устаревшей no-break роли BOM (с Unicode 3.2)
    NEIGHBOR_004:
      CODEPOINT: U+200C
      NAME: ZERO WIDTH NON-JOINER (ZWNJ)
      FUNCTION_DIFF: ZWNJ подавляет соединение; BOM к соединению отношения не имеет

SIGN_RELATIONS:
  [ИСТОЧНИК ИСТИНЫ ДЛЯ РАНТАЙМА. RELATION_TYPE_RUNTIME_STATUS — тип это КОНТРАКТ
   (карта _RELATION_RUNTIME_ROLE).]
  RELATION_001:
    RELATION_TYPE: BOUNDARY_DISRUPTOR
    RELATION_TYPE_RUNTIME_STATUS: PRIMARY
      [рвёт границу точного совпадения в машинном контексте; ЕДИНСТВЕННЫЙ
       самостоятельный вердикт, VERIFIED пробой на pay<BOM>pal.com → HOST/HIGH]
    TARGET_KIND: EMPTY_SEQUENCE
    CONTEXT_SCOPE: HOST, EMAIL, BYTE_EXACT_TOKEN, HIDDEN_BOUNDARY_PADDING, PATH, QUERY_VALUE, FRAGMENT, USERINFO
    VERIFICATION_STATUS: VERIFIED
    RUNTIME_EFFECT: RELATION_ONLY
  RELATION_002:
    RELATION_TYPE: INVISIBLE_CLASS_COLLISION
    RELATION_TYPE_RUNTIME_STATUS: TAXONOMY_ONLY
      [проходит по разрешению класса в ГРУБОМ внешнем фильтре / parser-desync;
       поведение внешних систем НЕ наблюдаемо из входа → рантайм-проверки НЕТ,
       риска не эмитит. Честно.]
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
    TRIGGER: «BOM невидим, значит его нет»
    RESPONSE: INVISIBLE ≠ ABSENT
    RULE: невидимость — не отсутствие; знак присутствует в потоке байт
  CG2:
    TRIGGER: «BOM — это пробел / разрыв»
    RESPONSE: BOM — МАРКЕР потока, не пробел и не разрыв
    RULE: Join_Control=NO; не break-opportunity (ZWSP); смысл в позиции
  CG3:
    TRIGGER: «нормализация уберёт BOM»
    RESPONSE: NFKC_SURVIVAL ≠ LEGITIMACY
    RULE: невидимые переживают NFC/NFD/NFKC/NFKD — остаются в строке
  CG4:
    TRIGGER: «ведущий BOM легитимен, значит безопасен»
    RESPONSE: LEADING_BOM ≠ FREE_TO_IGNORE
    RULE: частый легитимный ≠ безопасный; не освобождается (ВОЗМОЖНАЯ ОПАСНОСТЬ)
  CG5:
    TRIGGER: «все невидимые можно слепо удалить»
    RESPONSE: DEFAULT_IGNORABLE ≠ SAFE_TO_DELETE
    RULE: удаление ведущего BOM ломает ожидания парсера кодировки; в середине —
      реконструирует канон. Граница детектора, не карточки.
  CG6:
    TRIGGER: «нет видимого канона — нет отношения»
    RESPONSE: NO_CODEPOINT_CANON ≠ NO_RELATION
    RULE: отношение к границе/классу/пустоте/позиции есть без визуального канона

SEQUENCE_LAYER_BOUNDARY:
  SIGN_SAFE_ALONE ≠ SIGN_SAFE_IN_SEQUENCE: YES
  SEQUENCE_CANDIDATES: NOT_APPLICABLE
    [межзнаковое поведение (BOM между метками/буквами) оценивается через ось
     «отношение», как у ZWSP/ZWJ, а не через литеральный кандидат последовательности.]

PHAGO_ENTITY_MIMICRY:
  NOT_APPLICABLE
  PHAGO_REVIEW: INHERITED_FROM_METHOD (правило RULE_PHAGO_APPLICABILITY_v0_1; отдельного
    BOM-прогона фаго ещё нет — помечено честно, к конвейеру)
  PHAGO_BASIS: BOM СВОЕЙ ФУНКЦИЕЙ (маркер/вставка) НЕ создаёт ложную принадлежность к
    сущности. Мимикрия при участии BOM эмерджентна на уровне ПОСЛЕДОВАТЕЛЬНОСТИ, не
    свойство одиночного знака. Тест: убрать BOM — целевая сущность (paypal) цела.
  PHAGO_INTERACTION_ROLE: ENABLER_ONLY
  PHAGO_APPLICABILITY_RULE: каноничный источник —
    foundation_layer/RULE_PHAGO_APPLICABILITY_v0_1.md (здесь НЕ дублируется).

============================================================
8. ADVERSARIAL_COVERAGE — RUN_CARD SEED
============================================================
MIN_TOTAL_VECTORS: 10
CATEGORY_A: FORM_MANIPULATION
  A1: BOM между символами домена
  A2: несколько BOM подряд
CATEGORY_B: CONTEXT_INJECTION
  B1: BOM в host-части URL без схемы
  B2: BOM в email локальной части
CATEGORY_C: POSITION_MANIPULATION
  [УНИКАЛЬНО для BOM: легитимность позиционна — проверить ведущий/середина/хвост]
  C1: ведущий BOM перед доменом (HIDDEN_BOUNDARY_PADDING)
  C2: ведущий BOM перед текстом/json (частый легитимный — ВОЗМОЖНАЯ ОПАСНОСТЬ)
CATEGORY_D: PARSER_DESYNC
  D1: BOM, вызывающий рассинхрон парсеров (RUNTIME_STATUS PENDING — вектор описан)
CATEGORY_E: SEMANTIC_LAYER_MANIPULATION
  E1: подача BOM в файловом обрамлении для сокрытия машинного риска
  E2: смена активной эпохи гейтом позиции (ведущий-маркер → машинная-диверсия)
ACTUAL_TOTAL_VECTORS: 10
COVERAGE_STATUS: PROBE_LEVEL
COVERAGE_SUFFICIENCY: PROBE_LEVEL_NOT_FULL_BATTERY
  [ПРОГНАНО: штатный analyze() на контекстах BOM (mid-host→hold, токен/email/ведущий-
   домен→queue, free-text/json→pass). НЕ двуногая батарея с reconcile+mutation-adequacy —
   та PENDING. Не выдаётся за полное покрытие.]

============================================================
9. MUTATION_CHECK
============================================================
MUTATION_01:
  CLAIM: BOM даёт authority_effect
  EXPECTED: FAIL_FALSE_AUTHORITY
  RESULT: FAIL
MUTATION_02:
  CLAIM: BOM исполняется/запускает
  EXPECTED: FAIL_FALSE_EXECUTION
  RESULT: FAIL
MUTATION_03:
  CLAIM: ведущий BOM безопасен (освобождается в pass)
  EXPECTED: FAIL_FALSE_SAFE (частый легитимный ≠ безопасный; ВОЗМОЖНАЯ ОПАСНОСТЬ)
  RESULT: FAIL
MUTATION_04:
  CLAIM: BOM эквивалентен ZWSP (break) или ZWJ (join)
  EXPECTED: FAIL_FALSE_EQUIVALENCE (BOM — маркер потока, Join_Control=NO, не break)
  RESULT: FAIL
MUTATION_05:
  CLAIM: невидимость = отсутствие в потоке
  EXPECTED: FAIL_FALSE_ABSENCE
  RESULT: FAIL
MUTATION_CHECK_RUNTIME:
  STATUS: PENDING [engine-verified мутации кодпоинта/контекста/scope (как 6 у ZWSP)
    будут при постройке персистентной BOM-батареи; сейчас — семантические выше]

============================================================
10. KNOWN_OPEN_QUESTIONS
============================================================
OQ1:
  QUESTION: классовый INVISIBLE_DEFAULT_IGNORABLE_GUARD не построен
  STATUS: CLASS_FRONT_DEPENDENCY (как у ZWSP/ZWJ)
  BLOCKS_WORKINGLY_CLOSED: NO
  NOTE: BOM — 3-й из >=3 знаков. Набор образцов ПОЛОН (ZWSP рвёт / ZWJ склеивает /
    BOM маркер) — можно строить гард.
OQ2:
  QUESTION: THREE_LEVEL_DIVERGENCE — контексты, где желаемый уровень (РЕАЛЬНАЯ/
    ВОЗМОЖНАЯ) не совпал с измеренным. Эскалация требует рантайм-риск-мэппинга.
  STATUS: OPEN, осталось 4 из исходных 5 (эскалационные: токен/идентификатор/email/
    ведущий-перед-доменом → O1). Пятое (json-ведущий) СНЯТО правкой описания
    (observation-level, RECONCILE_BYSPEC_ZWJ_BOM_2026-07-18 точка B1), не эскалацией.
  BLOCKS_WORKINGLY_CLOSED: NO
  NOTE: задевает ZWSP (общие контексты) → отдельный заход с ре-валидацией, не тут.
OQ3:
  QUESTION: детектор _demask и ведущий BOM — удаление ломает ожидания парсера кодировки
  STATUS: OPEN
  BLOCKS_WORKINGLY_CLOSED: NO
  NOTE: DEFAULT_IGNORABLE ≠ SAFE_TO_DELETE; граница ДЕТЕКТОРА, не карточки
OQ4:
  QUESTION: детектор не различает CODE/IDENTIFIER/policy — схлопываются в BYTE_EXACT_TOKEN
  STATUS: OPEN (унаследовано, как у ZWSP/ZWJ)
  BLOCKS_WORKINGLY_CLOSED: NO
OQ5:
  QUESTION: PARSER_DESYNC-вектор (RISK_CASE_006) рантаймом не наблюдается из одной строки
  STATUS: OPEN
  BLOCKS_WORKINGLY_CLOSED: NO
  NOTE: свойство внешних систем; честно PENDING, за контракт не выдаётся
ALL_OPEN_QUESTIONS_CLOSED: NO

============================================================
11. PATCH_HISTORY
============================================================
PATCH_HISTORY:
  v0_1_PATCH_00: initial creation (2026-07-18). Третья карточка невидимого класса,
    из образца ZWJ. Содержание — на ИЗМЕРЕННОЙ пробе штатного analyze() (bom_probe /
    bom_temp_card_measure, 2026-07-18): mid-host→hold, токен/email/ведущий-домен→queue,
    free-text/json→pass. Персонализация: BOM=byte-order-mark, легитимность позиционна,
    Join_Control=NO, устаревшая no-break роль (→U+2060). ПЕРВЫЙ носитель принципа
    трёхуровневой сигнализации (на существующих выходах; THREE_LEVEL_DIVERGENCE = 5
    OPEN-расхождений желаемое↔измеренное). Подключение в CARD_FILENAMES (9 карт).
    Oracle НЕ тронут (BOM в кейсах нет). Батарея ZWSP не задета (ZWSP-scoped).
  v0_1_PATCH_01: описание B1 доуточнено по reconcile двуногой симуляции (2026-07-19,
    RECONCILE_BYSPEC_ZWJ_BOM_2026-07-18, точка B1). ТОЛЬКО ОПИСАНИЕ, поведение НЕ
    тронуто: (а) SAFE_CASE_001 — добавлен OBSERVATION_LEVEL (прикладная строка ≠
    транспортный поток; BOM, доживший до прикладной строки, = наблюдение → ВОЗМОЖНАЯ;
    из голых свойств не выводится — слепая нога дала ЧИСТО 5/5, уровень наблюдения
    независимо назвали GPT+Kimi); (б) SAFE_CASE_002 — json-ведущий = ЧИСТО
    (TRANSPORT_LIKE_POSITION), раннее желаемое ВОЗМОЖНАЯ снято обоснованием, не кодом;
    (в) THREE_LEVEL_DIVERGENCE/OQ2 пересчитаны: осталось 4 эскалационных (→O1).
    Верификация: вердикты всех контекстов ИДЕНТИЧНЫ до/после (описание ≠ поведение).
PATCHES_APPLIED: 2
PATCHES_VERIFIED: PROBE (штатный analyze; полная батарея — PENDING)

============================================================
12. LIMITATION_STATEMENT
============================================================
LIMITATION_STATEMENT:
  THIS_CARD IS A WORKING_DRAFT ARTIFACT (ранняя ступень; не WORKINGLY_CLOSED)
  NOT A FINAL_STANDARD / NOT A PARSER / NOT A RUNTIME / NOT A SECURITY_CERTIFICATE
  PROBE ≠ FULL_BATTERY (двуногая BY_SPEC+reconcile для BOM ВЫПОЛНЕНА 2026-07-18 —
    RECONCILE_BYSPEC_ZWJ_BOM_2026-07-18: B2/B4 подтверждены, B1 закрыт правкой описания
    PATCH_01; mutation-adequacy для BOM ещё НЕТ)
  THREE_LEVEL_IS_FIRST_APPLICATION: принцип трёх уровней применён здесь ВПЕРВЫЕ, на
    существующих выходах рантайма (pass/queue/hold). Полное закрепление (foundation-
    документ, риск-градация 138, возможный рантайм-уровень) — ОТДЕЛЬНЫЙ заход.
    Оставшиеся 4 расхождения желаемое↔измеренное (после снятия json-ведущего PATCH_01)
    честно вынесены в THREE_LEVEL_DIVERGENCE / OQ2.
  DETECTOR_BOUNDARY_NOTE: DEFAULT_IGNORABLE ≠ SAFE_TO_DELETE — _demask детектора НЕ
    должен слепо удалять ведущий BOM (ломает ожидания парсера кодировки); в машинной
    середине demask реконструирует канон. Граница ДЕТЕКТОРА, не карточки.
  RUNTIME_REALITY (обещания=реальность, проба 2026-07-18): система РЕАЛЬНО производит по
    BOM: HOST→HIGH(hold)=РЕАЛЬНАЯ; EMAIL→MEDIUM(queue)=ВОЗМОЖНАЯ; BYTE_EXACT_TOKEN→
    MEDIUM(queue)=ВОЗМОЖНАЯ; HIDDEN_BOUNDARY_PADDING→MEDIUM(queue)=ВОЗМОЖНАЯ;
    FREE_TEXT→NONE(pass)=ЧИСТО. Единственный самостоятельный вердикт — ребро
    BOUNDARY_DISRUPTOR (PRIMARY); INVISIBLE_CLASS_COLLISION (TAXONOMY_ONLY) и
    ABSENCE_CONFUSABLE (SUPPORTING_FACET) риска НЕ эмитят. Это НЕ антивирус: вердикт
    (PASS/QUEUE/HOLD) — РЕКОМЕНДАЦИЯ человеку, ничего не режется. Невидимый БЕЗ карточки —
    витнес UNVERIFIABLE.

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
