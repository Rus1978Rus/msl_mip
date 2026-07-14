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
DOCUMENT_STATUS: WORKINGLY_CLOSED
LIFECYCLE_STATUS: WORKINGLY_CLOSED_PENDING_CLASS_GUARD
  [РЕАЛЬНАЯ позиция в жизненном цикле (AUTHOR_DECISION D-ZWSP-WORKINGLY-CLOSED
   2026-07-15; поднято с VALIDATED_BY_TOOL/PENDING_CONVEYOR_REVIEW по D-ZWSP-STATUS
   2026-07-13 — шаг 2 PATH_TO_ARTIFACT закрыт).
   DOCUMENT_STATUS выше поднят WORKING_DRAFT → WORKINGLY_CLOSED — это MACHINE-GATE
   поле (module_engine._VALID_STATUSES). Основание флипа: код определяет
   _VALID_STATUSES как «прошёл STRUCTURAL_PREFLIGHT_PASS + CONVEYOR_REVIEW_PASS
   (несколько независимых ревьюеров) + AUTHOR_DECISION» — ВСЕ ТРИ условия выполнены
   (preflight 35/0/1; внешний конвейер 8/8 ACCEPT; это решение). Держать WORKING_DRAFT
   больше нельзя: предупреждение CARD_NOT_CONVEYOR_REVIEWED («не прошёл preflight/
   conveyor») стало бы ЛОЖНЫМ — claim≠reality в обратную сторону. Рантайм КОРРЕКТНО
   перестаёт предупреждать. Квалификатор _PENDING_CLASS_GUARD живёт здесь, в
   LIFECYCLE_STATUS (код такой строки не знает — в DOCUMENT_STATUS был бы CARD_INVALID);
   классовый гард по D-ZWSP-STATUS Q2 — КЛАССОВАЯ зависимость, НЕ блокер. Код НЕ тронут —
   меняется только поле карточки. ARTIFACT_CONFIRMED остаётся PENDING до постройки
   гарда — см. PATH_TO_ARTIFACT ниже.]
VALIDATION_METHOD: TWO_LEGGED_SIMULATION + MUTATION_ADEQUACY_5/5 + RECONCILE_BY_TUPLE
CLASS_ROLE: METHOD_REFERENCE_SPECIMEN
  [первый невидимый знак класса, проведённый строгим инструментом — эталон метода]
TEMPLATE_LINE: GEN3_v0_3
SOURCE_TEMPLATE: SIGN_CORE_CARD_TEMPLATE_GEN3_v0_3_R1_RU
AUTHOR: Руслан Малявский
CREATED_AT: 2026-07-12
VERSION: v0_1
AUTHOR_DECISION_REFERENCE: foundation_layer/AUTHOR_DECISION_20260712_INVISIBLE_SIGNS_D-INV-1_2_3.md
AUTHOR_DECISION_REFERENCE_STATUS: foundation_layer/AUTHOR_DECISION_20260713_D-ZWSP-STATUS.md; foundation_layer/AUTHOR_DECISION_20260715_D-ZWSP-WORKINGLY-CLOSED.md
RUN_CARD_REFERENCE: conveyor_runs/SIMULATION_ARTIFACT_ZERO_WIDTH_SPACE_U200B_TIER2_BY_CODE_v0_2_RU.md
RUN_CARD_STATUS: SIMULATION_DONE (BATTERY_RESULT: 21/21; BY_CODE, mutation-adequacy 5/5; U1/D2 закрыты F-NEW-4/5)
PATH_TO_ARTIFACT:
  1. STRUCTURAL_PREFLIGHT_PASS + CONVEYOR_REVIEW_PASS — ПРОЙДЕНЫ (preflight 35/0/1;
     внешний конвейер 8/8 ACCEPT, PASS_WITH_PATCHES). Порядок канона восстановлен.
  2. → WORKINGLY_CLOSED_PENDING_CLASS_GUARD — ДОСТИГНУТО (AUTHOR_DECISION
     D-ZWSP-WORKINGLY-CLOSED, 2026-07-15; DOCUMENT_STATUS=WORKINGLY_CLOSED).
  3. построить INVISIBLE_DEFAULT_IGNORABLE_GUARD (из >=3 разных невидимых) + ре-валидация
       ← СЛЕДУЮЩИЙ ШАГ (CLASS_FRONT, не блокер — по D-ZWSP-STATUS Q2)
  4. → ARTIFACT_CONFIRMED
DISPLAY_NAME: невидимый пробел нулевой ширины (zero width space)

============================================================
1. UNIVERSALITY / CONVEYOR_DISCIPLINE
============================================================
BOUND_TO_SPECIFIC_SIGN: YES
AFTER_USE_RESIDUE: FORBIDDEN
SIGN_DATA_IS_SESSION_ONLY: YES
STATUS_PROGRESSION_TRACKER:
  WORKING_DRAFT: NO (superseded — DOCUMENT_STATUS поднят до WORKINGLY_CLOSED, D-ZWSP-WORKINGLY-CLOSED 2026-07-15)
  STRUCTURAL_PREFLIGHT_PASS: PASS (self-check 2026-07-13: 35 PASS / 0 FAIL / 1 PRECEDENT — CONFUSABLES-арбитраж)
  CONVEYOR_REVIEW_PASS: PASS_WITH_PATCHES (2026-07-14, 8/8 ACCEPT; BY_CODE-сверка + doc-sync применены)
  WORKINGLY_CLOSED: DONE (WORKINGLY_CLOSED_PENDING_CLASS_GUARD — AUTHOR_DECISION D-ZWSP-WORKINGLY-CLOSED 2026-07-15; DOCUMENT_STATUS=WORKINGLY_CLOSED)
  SIMULATION_GATE_TIER: TIER_2 (ZONE_2)
  SIMULATION_GATE_PASSED: BY_TOOL_DONE (BY_CODE 21/21; формальный SIMULATION_GATE — по пути к ARTIFACT_CONFIRMED, при постройке гарда)
  ARTIFACT_CONFIRMED: PENDING (blocked ТОЛЬКО классовым гардом — CLASS_FRONT, не дефект карточки)

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
    SEMANTIC_STATUS: LEGITIMATE_USE
      [U+200B — класс переноса строки ZW (UAX#14); в CJK/тайском это законный
       сегментатор слов, семантически безопасен]
    IMPLEMENTATION_STATUS: NOT_RECOGNIZED_WITHOUT_EXTERNAL_TYPOGRAPHY_CONTEXT
      [детектор НЕ различает типографику от машинной строки без внешнего
       typography-контекста; чинить кодом нельзя — эвристика «CJK=безопасно»
       откроет пропуск маски в CJK-ДОМЕНЕ (gоog<ZWSP>le.中国). Честность
       карточки, не эвристика — решение конвейера 5/5.]
    CURRENT_RUNTIME_EXPECTATION: MAY_QUEUE
      [CJK-токен с ZWSP схлопывается в BYTE_EXACT_TOKEN → детектор МОЖЕТ дать
       MEDIUM/QUEUE. Карточка НЕ обещает автоматический PASS, которого код не
       даёт (claim=evidence). НЕ баг — честная граница до typography-контекста
       (v0.5). См. T1 в oracle-манифесте, OQ по typography-контексту.]
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
    CONTEXT_SCOPE: HOST, EMAIL, BYTE_EXACT_TOKEN, PATH, HIDDEN_BOUNDARY_PADDING, QUERY_VALUE, FRAGMENT, USERINFO
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
  NOT_APPLICABLE
  PHAGO_REVIEW: VERIFIED (conveyor 9 reviewers 8:1 + author decision 2026-07-13)
  PHAGO_BASIS: ZWSP СВОЕЙ ФУНКЦИЕЙ (разрыв токена) НЕ создаёт ложную
    принадлежность к сущности. Мимикрия при участии ZWSP эмерджентна на уровне
    ПОСЛЕДОВАТЕЛЬНОСТИ (в связке с гомоглифом/доменом) → относится к
    SEQUENCE/RELATION-слою, не свойство одиночного знака. Согласовано с якорями
    критерия: / U+002F APPLICABLE (функция-разделитель САМА порождает ложную
    иерархию бренда), . U+002E NOT_APPLICABLE (сама не порождает) — ZWSP как точка.
    Тест: убрать ZWSP — целевая сущность (administrator, paypal) существует без него.
  PHAGO_ROBUST: NOT_APPLICABLE держится по ЛЮБОМУ прочтению фаго — вердикт НЕ
    зависит от открытого узла PHAGO_NATURE. ZWSP: (1) НЕ создаёт ложную
    ПРИНАДЛЕЖНОСТЬ к сущности; (2) НЕ ПОГЛОЩАЕТ чужую идентичность (тест
    фагоцитоз-гипотезы); (3) сам НЕ есть сущность-сигнал (невидимый разрыв, не
    лицо/бренд/авторитет). → NOT_APPLICABLE при всех трёх прочтениях.
    См. foundation_layer/OPEN_NODE_PHAGO_NATURE.md.
  PHAGO_INTERACTION_ROLE: ENABLER_ONLY
    [участвует в мимикрии на уровне ПОСЛЕДОВАТЕЛЬНОСТИ, НЕ PHAGO-актор на уровне
     знака. ПРОШЛАЯ граница («своё лицо» / «служит» / «невидим») ОТКАЧЕНА как
     неверная — конфликтовала с / U+002F (APPLICABLE). Верный критерий — в
     foundation_layer/RULE_PHAGO_APPLICABILITY_v0_1.md.]
  PHAGO_APPLICABILITY_RULE: каноничный источник —
    foundation_layer/RULE_PHAGO_APPLICABILITY_v0_1.md (здесь НЕ дублируется во
    избежание дрейфа).

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
CATEGORY_E: PHAGO_ENTITY_MIMICRY — N/A_ACTIVELY_VERIFIED (прогон 2026-07-13)
  [PHAGO=NOT_APPLICABLE, но правило «N/A по фаго проверяется ОТДЕЛЬНО» → это не
   отписка «NOT_APPLICABLE», а 2 АКТИВНЫХ вектора: попытки заставить ZWSP создать
   ложную принадлежность к сущности, которые ПРОВАЛИВАЮТСЯ на движке, подтверждая
   N/A. RESULT = вывод детектора, не догадка.]
  E1: попытка ZWSP как сущность-сигнал РОЛИ — «admin<ZWSP>istrator»
    OBSERVED: детектор → BYTE_EXACT_TOKEN / MEDIUM (разрыв токена), НЕ entity-мимикрия
    RESULT: N/A ПОДТВЕРЖДЁН — роль «administrator» несут ВИДИМЫЕ БУКВЫ (убрать ZWSP →
      «administrator» цел); ZWSP своей функцией ложной принадлежности не создаёт
  E2: попытка ZWSP создать принадлежность к БРЕНДУ — «paypal<ZWSP>.com»
    OBSERVED: детектор → HOST / HIGH (разрыв домена)
    RESULT: N/A ПОДТВЕРЖДЁН — бренд-схожесть «paypal.com» эмерджентна из СТРОКИ
      (видимые буквы), цела без ZWSP; мимикрия (если возникает) на уровне
      ПОСЛЕДОВАТЕЛЬНОСТИ, не одиночного знака (согласовано с PHAGO_BASIS, раздел 7)
CATEGORY_F: SEMANTIC_LAYER_MANIPULATION
  F1: смена активной эпохи гейтом контекста (типографика → машинная)
  F2: подача ZWSP в типографическом обрамлении для сокрытия машинного риска
ACTUAL_TOTAL_VECTORS: 12
COVERAGE_STATUS: SUFFICIENT_FOR_CURRENT_CARD_SCOPE
COVERAGE_SUFFICIENCY: SUFFICIENT_FOR_CURRENT_CARD_SCOPE
  [ПРОГНАНО: BY_CODE-батарея 21/21 (двуногая BY_SPEC+BY_CODE, reconcile по
   кортежу, mutation-adequacy 5/5). НЕ голое SUFFICIENT: покрывает ровно те
   контексты, что детектор РЕАЛЬНО производит (HOST/EMAIL/PATH/BYTE_EXACT_TOKEN/
   QUERY_VALUE/FRAGMENT/USERINFO/HIDDEN_BOUNDARY_PADDING). За scope этой карточки
   (плотностной DoS на впуске, файловый вход) — отдельные фронты, не покрыты и
   честно так помечены.]

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

MUTATION_CHECK_RUNTIME (engine-verified, прогон msl_mip_runtime 2026-07-13 —
  РЕАЛЬНЫЕ мутации кодпоинта/контекста/scope/типа/target_kind; RESULT = вывод
  ДЕТЕКТОРА на прогоне, не предположение; MUTATION_01-06 выше — семантические,
  об EFFECT_FIELDS; эти — рантаймовые, о поведении детектора):
  MR_01_CODEPOINT_BINDING:
    CLAIM: любой невидимый в домене срабатывает как ZWSP
    METHOD: goog<U+2062>le.com (U+2062 вместо U+200B)
    OBSERVED: ZWSP-ребро НЕ сработало; U+2062 → witness (UNVERIFIABLE); verdict pass
    RESULT: FAIL (карта bound к U+200B; чужой невидимый → witness, не ZWSP-вердикт)
  MR_02_CONTEXT_GATING:
    CLAIM: ZWSP даёт фиксированный риск независимо от контекста
    METHOD: goog<ZWSP>le.com / bad<ZWSP>word / «просто <ZWSP> текст»
    OBSERVED: HOST=HIGH, BYTE_EXACT_TOKEN=MEDIUM, FREE_TEXT=NONE
    RESULT: FAIL (риск контекст-зависим — гейтится _detect_context_at)
  MR_03_SCOPE_PROTECTION:
    CLAIM: риск не зависит от CONTEXT_SCOPE ребра
    METHOD: temp-карта без HOST в scope BOUNDARY_DISRUPTOR; goog<ZWSP>le.com
    OBSERVED: ctx=HOST, но protected=False → risk NONE, verdict pass
    RESULT: FAIL (scope гейтит риск; HOST вне scope → NONE)
  MR_04_UNKNOWN_TYPE_SAFETY:
    CLAIM: неизвестный RELATION_TYPE эмитит риск как PRIMARY
    METHOD: temp-карта RELATION_TYPE=FOOBAR_UNKNOWN_TYPE; goog<ZWSP>le.com
    OBSERVED: INVALID_EDGE_NOT_ACTIVATED (1 ребро), исключено, риск не эмитит
    RESULT: FAIL (неизвестный тип → INVALID_EDGE, не PRIMARY-дефолт)
  MR_05_FACET_ROLE_GATING:
    CLAIM: ABSENCE_CONFUSABLE не эмитит риск ни при каком типе
    METHOD: temp-карта ABSENCE_CONFUSABLE→BOUNDARY_DISRUPTOR; goog<ZWSP>le.com
    OBSERVED: как SUPPORTING_FACET → NONE; сменив тип на PRIMARY → HOST/HIGH
    RESULT: FAIL (эмиссия гейтится РОЛЬЮ/типом, не фиксирована — дедуп реален)
  MR_06_TARGET_KIND_ENFORCEMENT:
    CLAIM: TARGET_KIND CODEPOINT без TARGET активируется молча
    METHOD: temp-карта TARGET_KIND EMPTY_SEQUENCE→CODEPOINT (TARGET не добавлен)
    OBSERVED: INVALID_EDGE_NOT_ACTIVATED (1 ребро), surfaced, не активирован
    RESULT: FAIL (CODEPOINT требует TARGET; контракт-нарушение → INVALID_EDGE)
  MUTATION_CHECK_RUNTIME_TOTAL: 6 (все FAIL = движок держит инвариант при мутации)

============================================================
10. KNOWN_OPEN_QUESTIONS
============================================================
OQ1:
  QUESTION: классовый INVISIBLE_DEFAULT_IGNORABLE_GUARD не построен —
    класс-свойства ZWSP объявить негде
  STATUS: RECLASSIFIED (AUTHOR_DECISION D-ZWSP-STATUS 2026-07-13)
  BLOCKS_WORKINGLY_CLOSED: NO  (было YES)
  RECLASSIFIED_AS: CLASS_FRONT_DEPENDENCY
    [гард — КЛАССОВАЯ зависимость, НЕ дефект этой карточки. Строить на N=1 =
     переобучение (нарушает «не обобщай с одного», рискует сломать легитимные
     ZWJ/ZWNJ — DEFAULT_IGNORABLE ≠ SAFE_TO_DELETE). Вынесен в class-front
     register: foundation_layer/CLASS_FRONT_INVISIBLE_SIGNS.md. Регистратор
     (witness) ЧАСТИЧНО покрывает под-обещание «незнакомое не молчит» → снижает
     срочность, но НЕ заменяет (witness ≠ policy: goog<U+2063>le.com →
     PASS+witness, не HOST/HIGH). Гард нужен позже, из >=3 знаков.]
  NOTE: класс-свойства ZWSP объявлены inline (SIGN_CATEGORY +
    WHAT_THIS_SIGN_IS_NOT); общий дом для них — будущий гард на уровне класса.
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
  STATUS: RESOLVED (F-NEW-2 patch, 2026-07-13)
  BLOCKS_WORKINGLY_CLOSED: NO (was YES)
  SEVERITY: HIGH
    [это СИСТЕМА ОПОВЕЩЕНИЯ: ложная тревога критична — подрывает доверие
     человека к HOLD. Не косметика — чинить, не откладывать бессрочно.]
  SCOPE: ОБЩИЙ детектор — задевает и маску ／ (U+FF0F), и все 55 кейсов
    bare-domain. Фикс требует полного ре-гейта 55 + регрессии на ／, поэтому
    отдельным пакетом, а не внутри этого коммита невидимых.
  RESOLUTION: CLOSED by F-NEW-2 root 2B — HOST fires only if the mask index is
    INSIDE the host span (len(left_part) < host_end of the reconstruction);
    past the host -> PATH. NB: the ORIGINAL hypothesis above (pre-mask token
    already contains / ? #) proved INSUFFICIENT — it missed P5-style deep paths;
    the host-span check replaced it. docs.example.com/guide/very-long<ZWSP>-
    section now reads PATH/MEDIUM.
OQ-HBP:
  QUESTION: HIDDEN_BOUNDARY_PADDING — НОВЫЙ контекст (F-NEW-2 root 2A) для
    ведущей/хвостовой невидимки у ЦЕЛОГО домена (<ZWSP>paypal.com,
    paypal.com<ZWSP>): не разрыв метки (не HOST/HIGH), но и не молчаливый PASS
    → MEDIUM/QUEUE как fallback от pass.
  STATUS: OPEN
  BLOCKS_WORKINGLY_CLOSED: NO
  NEEDS: суд конвейера — правильная ли это отдельная сущность-контекст, верен ли
    риск MEDIUM, не плодит ли контексты без нужды (не подвид ли BYTE_EXACT_TOKEN).
    Идёт на конвейер с пачкой F-NEW-3.
  DIRECTION: при РЕВИЗИИ СХЕМЫ рефакторить в POSITION_ROLE, а не top-level
    контекст — по сути это ПОЗИЦИОННАЯ роль знака (в начале/в конце/внутри), не
    отдельный вид контекста наравне с HOST/PATH. Пока НЕ ломать рабочее: живёт
    как контекст до ревизии схемы (v0.5+).
OQ-SOLIDUS-DRIFT:
  QUESTION: детектор ／ (СОЛИДУС, ARTIFACT_CONFIRMED) теперь читает
    example.com,／test и gоogle.com*／path как PATH, а не HOST. Патч карточки
    ZWSP задел зону ГОТОВОГО артефакта — ПЕРВЫЙ подтверждённый ДРЕЙФ.
  STATUS: OPEN
  BLOCKS_WORKINGLY_CLOSED: NO
  SEVERITY: MEDIUM
    [позиционно PATH вернее старого over-read HOST (гейт солидуса сам звал это
     квирком); но изменение поведения ARTIFACT_CONFIRMED-детектора обязано
     пройти ре-валидацию, не тихо.]
  NEEDS: ре-валидация карточки СОЛИДУСА сегодняшним инструментом (BY_CODE),
    как у ZWSP. Связь: ARTIFACT_CONFIRMED привязан к ВЕРСИИ инструмента —
    инструмент изменился → статус солидуса надо переподтвердить. На конвейер
    с пачкой F-NEW-3.
OQ-SHARED-DETECTOR-BOUNDARY:
  QUESTION: в TIER_2-батарее ZWSP два кейса остаются «падающими» — U1
    (?q=bad<ZWSP>word → контекст PATH вместо QUERY_VALUE) и D2
    (paypal.com<ZWSP>@evil.com → нет разбора userinfo, host не извлекается).
  STATUS: RESOLVED (F-NEW-4 + F-NEW-5, 2026-07-13)
    [были НЕ провалами ZWSP: QUERY_VALUE и userinfo-парсинг — свойства ОБЩЕГО
     детектора. Закрыты патчами общего детектора _detect_context_at:
     F-NEW-4 — разбор URL на компоненты (authority/path/QUERY_VALUE/FRAGMENT);
     F-NEW-5 — userinfo (host после ПОСЛЕДНЕГО @ внутри authority, EMAIL не
     сломан — разведён по наличию scheme://). U1 → QUERY_VALUE/MEDIUM,
     D2 → USERINFO/MEDIUM. Батарея ZWSP 19/21 → 21/21.]
  BLOCKS_WORKINGLY_CLOSED: NO (для ZWSP)
  NEEDS: — (закрыто; общий детектор чинился отдельным фронтом, как и планировалось).
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
  v0_1_PATCH_03: F-NEW-3 + T1-честность + D-ZWSP-STATUS (2026-07-13). SAFE_CASE_002
    (CJK) → CURRENT_RUNTIME_EXPECTATION: MAY_QUEUE (не обещать авто-PASS, которого
    код не даёт). Статус-блок: LIFECYCLE_STATUS / VALIDATION_METHOD / CLASS_ROLE.
    OQ1 → CLASS_FRONT_DEPENDENCY (BLOCKS_WORKINGLY_CLOSED: NO). PHAGO: NOT_APPLICABLE
    VERIFIED + PHAGO_ROBUST + ENABLER_ONLY (правило — RULE_PHAGO_APPLICABILITY, узел
    PHAGO_NATURE). Солидус → REVALIDATION_REQUIRED (принцип Q7).
  v0_1_PATCH_04: F-NEW-4/5 (2026-07-13). CONTEXT_SCOPE ребра BOUNDARY_DISRUPTOR +=
    QUERY_VALUE, FRAGMENT, USERINFO (детектор научился разбирать URL на компоненты
    + userinfo по последнему @). OQ-SHARED-DETECTOR-BOUNDARY → RESOLVED. U1/D2
    закрыты → батарея 19/21 → 21/21.
  v0_1_PATCH_05: preflight-pass (2026-07-13). MUTATION_CHECK_RUNTIME — 6 РЕАЛЬНЫХ
    engine-verified мутаций (RESULT = прогон движка). CATEGORY_E → N/A_ACTIVELY_
    VERIFIED (2 активных вектора доказывают фаго-N/A). OPEN_NODE CONVEYOR_REVIEW_FORMAT.
  v0_1_PATCH_06: doc-sync (2026-07-14). Верхние слои приведены к нижним (верным):
    21/21 везде; RUNTIME_REALITY — полный список контекстов = scope ребра; COVERAGE
    → SUFFICIENT_FOR_CURRENT_CARD_SCOPE; RUN_CARD_STATUS/SIMULATION_GATE → 21/21;
    STRUCTURAL_PREFLIGHT → PASS; CONVEYOR_REVIEW_PASS → PASS_WITH_PATCHES (8/8 ACCEPT).
    OPEN_NODE CARD_SINGLE_SOURCE_OF_TRUTH. Триггер: BY_CODE-сверка вскрыла внутренний
    рассинхрон карточки (не карта↔код).
PATCHES_APPLIED: 6
PATCHES_VERIFIED: 6/6 (BY_CODE-батарея 21/21 + preflight 35/0/1 + BY_CODE-сверка 2026-07-14)

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
    ZWSP: HOST→HIGH; EMAIL→MEDIUM; PATH→MEDIUM; BYTE_EXACT_TOKEN→MEDIUM;
    QUERY_VALUE→MEDIUM; FRAGMENT→MEDIUM; USERINFO→MEDIUM;
    HIDDEN_BOUNDARY_PADDING→MEDIUM; FREE_TEXT→NONE. (QUERY_VALUE/FRAGMENT/
    USERINFO — от F-NEW-4/5 разбора URL на компоненты; HIDDEN_BOUNDARY_PADDING —
    от F-NEW-2; этот список ТОЧЬ-В-ТОЧЬ = CONTEXT_SCOPE ребра BOUNDARY_DISRUPTOR,
    сверено BY_CODE 2026-07-14.) Единственный самостоятельный вердикт даёт ребро
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
