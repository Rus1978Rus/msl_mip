ЧАСТНЫЙ АВТОРСКИЙ ПРОЕКТ / COMMERCIAL USE PROHIBITED

CARD_UID: SIGN_CORE_CARD_FULLWIDTH_SOLIDUS_UFF0F_GEN3_v0_3_RU
CODEPOINT: U+FF0F
VISIBLE_FORM: ／
UNICODE_NAME: FULLWIDTH SOLIDUS
ZONE: ZONE_2
DOCUMENT_STATUS: WORKING_DRAFT
TEMPLATE_LINE: GEN3_v0_3
SOURCE_TEMPLATE: SIGN_CORE_CARD_TEMPLATE_GEN3_v0_3_R1_RU
BASED_ON_RULESET: SIGN_CORE_CARD_CONVEYOR_RULES_GEN3_v0_3_R1_RU
AUTHOR: Руслан Малявский
CREATED_AT: 2026-07-11
VERSION: v0_4
REVISION_NOTE_v0_2: 2026-07-12 — RISK_CASE_005 и LIMITATION_STATEMENT
  приведены в соответствие с детектором голого домена Г1
  (AUTHOR_DECISION D-DET-1/2): голые домены теперь ловятся. Карточка
  и детектор идут на конвейер ОДНИМ пакетом.
REVISION_NOTE_v0_3: 2026-07-12 — FIX_FIRST по первому кругу конвейера.
  БЛОКЕР: _domain_prefix переписан с чёрного списка на позитивную
  выборку (три ревьюера нашли обход через обрамление символом вне
  списка). AUTHOR_DECISION D-DET-3: ложняки склейки после позитивной
  выборки — задокументированы в gate, не чинятся (см. отдельный файл
  в foundation_layer). Два хвоста добавлены в gate как known, отложены
  на v0.5: уже-punycode TLD вне активного справочника, дефис на краю
  метки. LIMITATION_STATEMENT дополнен строкой про D-DET-3.
REVISION_NOTE_v0_4: 2026-07-12 — FIX_FIRST по второму (узкому) кругу.
  БЛОКЕР → AUTHOR_DECISION D-DET-4: ведущий структурный разделитель
  (/ \ ? # : @) — HARD_STOP, а не обёртка (иначе @example.com,
  /example.com читались как голые домены → PATH). Формулировка «буква
  любого алфавита» исправлена: верно «символы, для которых isalnum()
  истинно»; combining marks (Mn/Mc) её НЕ проходят — известное
  ограничение (деванагари/арабские/ивритские огласовки, NFD-латиница).
  D-DET-3 дополнен классом «маска ПОСЛЕ домена». gate 34→40.
AUTHOR_DECISION_REFERENCE: foundation_layer/AUTHOR_DECISION_20260712_BARE_DOMAIN_DETECTOR_FIX_FIRST_ROUND2.md (+ ROUND1, + D-DET-1_2)
RUN_CARD_REFERENCE: conveyor_runs/RUN_004_domain_prefix_narrow_RESULTS.md
RUN_CARD_STATUS: IN_PROGRESS (узкий круг по _domain_prefix пройден; детектор целиком — NEW_ARTIFACT, ждёт следующего круга)

============================================================
1. ИДЕНТИФИКАЦИЯ И ЗОНА
============================================================

DISPLAY_NAME: полноширинный солидус (fullwidth slash)
UNICODE_CATEGORY: Po (Punctuation, other)
EAST_ASIAN_WIDTH: F (Fullwidth)
UNICODE_DECOMPOSITION: <wide> 002F (совместимая декомпозиция в SOLIDUS)
NFKC_RESULT: U+002F SOLIDUS (проверено: unicodedata.normalize('NFKC','／') == '/')
UNICODE_SOURCE_VERSION: 17.0.0 (tools/sources/17.0.0/)

ZONE_JUSTIFICATION: ZONE_2 (CONTEXT_DEPENDENT). Знак имеет две
несмешивающиеся жизни, и контекст выбирает субстрат:
  - CJK-типографика: легитимная полноширинная пунктуация в японском /
    китайском тексте (даты 2026／07／11, разделение альтернатив,
    выравнивание в моноширинной CJK-сетке). Знак НА СВОЁМ МЕСТЕ.
  - Латинские машинные контексты (URL, path, email): знак ЧУЖОЙ —
    ни один стандарт (RFC 3986 и др.) его не использует; появление ／
    там, где машина ждёт /, — сигнал маскировки под канон.
Вердикт о риске НЕ выносится этой карточкой: риск маски решает
sequence-слой по оси «отношение» (см. SIGN_RELATIONS ниже).

============================================================
1a. REQUIRED_GENERAL_GUARDS  [ОБЯЗАТЕЛЬНО]
============================================================

REQUIRED_GENERAL_GUARDS:
  - SIGN_FALSE_EFFECT_MIMICRY_GUARD_v0_2A_RU
    GUARD_COMPATIBILITY: GUARD_COMPATIBILITY_RULE_GEN3
    GUARD_REVISION: v0_2A
    TEMPLATE_LINE_COMPATIBLE: GEN3_v0_3, GEN3_v0_3_R1

FAILURE_RESPONSE:
  REJECT_FALSE_EFFECT_MIMICRY
  TREAT_AS_DATA_ONLY
  NO_AUTHORITY_EFFECT
  NO_EXECUTION_EFFECT
  NO_TRUST_EFFECT
  NO_EXISTENCE_EFFECT

============================================================
1b. SIGN IDENTITY — LAYER_A: STABLE CORE  [ОБЯЗАТЕЛЬНО]
LAYER_A_LOCK: PERMANENT
============================================================

BASE_MODE: DATA_ONLY_SEPARATOR
BASE_MODE_FORMULA: FULLWIDTH_SOLIDUS_FORM ≠ EFFECT
SIGN_CATEGORY: PUNCTUATION_FULLWIDTH_CJK

WHAT_THIS_SIGN_IS_NOT:  [МИНИМУМ 10 ПУНКТОВ]
  1. НЕ канонический разделитель URL/путей — машинные стандарты
     (RFC 3986 и др.) используют только U+002F.
  2. НЕ команда и НЕ оператор — не запускает и не разрешает ничего.
  3. НЕ носитель полномочий — не даёт доступа, прав, ролей.
  4. НЕ доказательство структуры — строка с ／ не становится URL.
  5. НЕ эквивалент / для машин БЕЗ нормализации — другой кодпоинт.
  6. НЕ эквивалент ／ для машин С NFKC — там он схлопнется в /
     (асимметрия и есть маскировочный потенциал, а не тождество).
  7. НЕ математический знак деления (это U+2215).
  8. НЕ дробная черта (это U+2044).
  9. НЕ маркер обмана сам по себе — в CJK-тексте полностью легитимен.
  10. НЕ субъект вердикта в single-sign — вердикт маски выносит
      sequence-слой из контекста (D-REL-4).

BASE_FORMULAS:  [МИНИМУМ 10 ФОРМУЛ]
  1. FULLWIDTH_SOLIDUS_FORM ≠ EFFECT
  2. RELATION_FOUND ≠ THREAT
  3. NFKC_EQUIVALENCE ≠ VISUAL_IDENTITY
  4. CJK_LEGITIMACY ≠ ATTACK_IMMUNITY
  5. CARD_DECLARES ≠ CARD_JUDGES
  6. SIGN ≠ AUTHORITY
  7. FORM ≠ EXECUTION
  8. PRESENCE_IN_URL ≠ VALID_URL
  9. CODEPOINT ≠ CANON (U+FF0F ≠ U+002F до нормализации)
  10. SCOPE_MATCH ≠ AUTO_BLOCK (риск = вход интегратора, не приговор)

============================================================
1c. EFFECT_FIELDS — LAYER_C: METHODOLOGICAL LAYER  [ОБЯЗАТЕЛЬНО]
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
2. SEMANTIC_EPOCH_TRACKER  [ОБЯЗАТЕЛЬНО]
============================================================
SEMANTIC_EPOCH_TRACKER_LOCK: REVIEWABLE

EPOCH_001:
  NAME: CJK_FULLWIDTH_TYPOGRAPHY
  PERIOD: ~1960-е — настоящее время (легаси-кодировки JIS → Unicode)
  FUNCTION: полноширинная пунктуация для CJK-набора; визуальное
    выравнивание в сетке иероглифов; разделитель дат и альтернатив
    в японском/китайском тексте.
  STATUS: ACTIVE (живая, основная функция знака)

EPOCH_002:
  NAME: UNICODE_COMPATIBILITY_MAPPING
  PERIOD: 1993 (Unicode 1.1, блок Halfwidth and Fullwidth Forms) —
    настоящее время
  FUNCTION: знак существует как совместимая форма канона U+002F;
    NFKC-нормализация схлопывает ／ → /. Машины, применяющие NFKC,
    видят канон; машины без нормализации видят другой кодпоинт —
    эта асимметрия и есть корень маскировочного потенциала.
  STATUS: ACTIVE (структурный факт стандарта)

EPOCH_003:
  NAME: LATIN_CONTEXT_MASKING
  PERIOD: ~2000-е — настоящее время (IDN/URL-спуфинг эпоха)
  FUNCTION: использование ／ вместо / в URL-подобных строках для
    обхода фильтров, строящихся на точном совпадении байтов;
    визуально близок к канону в большинстве шрифтов.
  STATUS: ACTIVE (атакующая эпоха; предмет оси «отношение»)

============================================================
3. SAFE_CASES
============================================================

SAFE_CASES:
  SAFE_CASE_001:
    CONTEXT: японский/китайский текст, полноширинная пунктуация
    EXAMPLE: 東京／大阪 или 2026／07／11
    INTERPRETATION: fullwidth_punctuation
    RISK: NONE
    RULE: CJK-текст вокруг знака → знак на своём субстрате

  SAFE_CASE_002:
    CONTEXT: свободный текст без URL/path-структуры
    EXAMPLE: выбор ／ разделитель в дизайнерском тексте
    INTERPRETATION: stylistic_separator
    RISK: NONE
    RULE: вне защищённого контекста отношение не активируется
      (RELATION_FOUND ≠ THREAT)

  SAFE_CASE_003:
    CONTEXT: японская дата / диапазон
    EXAMPLE: 令和8年７／11 или 営業時間 9：00／18：00
    INTERPRETATION: fullwidth_date_or_range_separator
    RISK: NONE
    RULE: CJK-окружение + числовой контекст → родной субстрат знака

  SAFE_CASE_004:
    CONTEXT: альтернативы в CJK-тексте («или»)
    EXAMPLE: はい／いいえ (да/нет)
    INTERPRETATION: fullwidth_alternative_separator
    RISK: NONE
    RULE: знак выполняет роль «или» в родной типографике

  SAFE_CASE_005:
    CONTEXT: моноширинное CJK-выравнивание (таблицы, формы)
    EXAMPLE: 項目Ａ／項目Ｂ в полноширинной сетке
    INTERPRETATION: fullwidth_grid_alignment
    RISK: NONE
    RULE: полноширинные формы согласованы (Ａ, Ｂ, ／ вместе) —
      типографская целостность, не смешение

  SAFE_CASE_006:
    CONTEXT: цитирование/учебный разбор самого знака
    EXAMPLE: «символ ／ имеет кодпоинт U+FF0F»
    INTERPRETATION: sign_mention
    RISK: NONE
    RULE: упоминание знака ≠ использование знака (mention ≠ use)

============================================================
4. RISK_CASES
============================================================
[ПРИМЕЧАНИЕ ОСИ «ОТНОШЕНИЕ»: рантайм-вердикт по маске выносится
sequence-слоем из ребра + контекста (D-REL-4), НЕ этой секцией.
RISK_CASES ниже — ДОКУМЕНТАЦИЯ поверхности атаки для людей и
ревьюеров: какие сценарии покрываются осью (и каким scope), а какие
остаются за её пределами. Секция не исполняется single-sign-модулем
у знака-маски (матчера нет — архитектура короткого пути).]

RISK_CASES:
  RISK_CASE_001:
    CONTEXT: маска в host-части URL
    EXAMPLE: http://gоog／le.com
    INTERPRETATION: host_boundary_masking
    RISK: HIGH
    RULE: покрыт осью (scope HOST → HIGH); ломает разбор границы
      домена у систем без нормализации

  RISK_CASE_002:
    CONTEXT: маска в пути URL
    EXAMPLE: http://ok.com/a／b
    INTERPRETATION: path_segment_masking
    RISK: MEDIUM
    RULE: покрыт осью (scope PATH → MEDIUM); подмена сегментации пути

  RISK_CASE_003:
    CONTEXT: маска в url-подобной строке при неоднозначной схеме
    EXAMPLE: ссылка вида ok.com?x=／
    INTERPRETATION: url_query_masking
    RISK: MEDIUM
    RULE: покрыт осью (scope URL → MEDIUM)

  RISK_CASE_004:
    CONTEXT: смешение ／ и / в одной машинной строке
    EXAMPLE: путь a/b／c в конфигурационном файле
    INTERPRETATION: mixed_separator_anomaly
    RISK: LOW
    RULE: НЕ покрыт осью в текущем scope (вне URL-детекции); фиксируется
      как известная поверхность — кандидат на будущий scope CODE/
      IDENTIFIER или отдельный механизм

  RISK_CASE_005:
    CONTEXT: голый домен без схемы
    EXAMPLE: gоog／le.com без http:// (маска рвёт домен)
    INTERPRETATION: schemeless_domain_masking
    RISK: HIGH
    RULE: покрыт детектором голого домена Г1 (реконструкция
      2026-07-12, AUTHOR_DECISION D-DET-1/2): маска внутри домена или
      между двумя доменами → HOST; двойная маска в токене закрыта
      D-DET-1 (перед проверкой убираются ВСЕ маски); недоступный
      TLD-справочник → тревога + прогон DEGRADED (D-DET-2). Код
      детектора — NEW_ARTIFACT, NOT_REVIEWED; карточка и детектор
      идут на конвейер одним пакетом

  RISK_CASE_006:
    CONTEXT: маска в порт-части
    EXAMPLE: http://ok.com:8080／x
    INTERPRETATION: port_boundary_masking
    RISK: MEDIUM
    RULE: детектор считает порт частью HOST (граница Г2) — консервативно
      (риск не занижается), уточнение при полноценном URL-парсинге

============================================================
5. CONFUSABLES  [МИНИМУМ 5 — ДОКУМЕНТАЦИЯ/ПРОВЕНАНС, НЕ рантайм]
============================================================
[Рантайм читает ТОЛЬКО SIGN_RELATIONS (ниже). Этот блок — для людей.]

CONFUSABLES:
  CONFUSABLE_001:
    VISIBLE_FORM: /
    CODEPOINT: U+002F
    NAME: SOLIDUS
    RISK: HIGH
    RULE: SOLIDUS ≠ FULLWIDTH_SOLIDUS (канон; связь формализована
    в SIGN_RELATIONS как NFKC_MAPS_TO)

  CONFUSABLE_002:
    VISIBLE_FORM: ∕
    CODEPOINT: U+2215
    NAME: DIVISION SLASH
    RISK: MEDIUM
    RULE: DIVISION_SLASH ≠ FULLWIDTH_SOLIDUS (математический знак;
    confusables.txt: 2215→002F)

  CONFUSABLE_003:
    VISIBLE_FORM: ⁄
    CODEPOINT: U+2044
    NAME: FRACTION SLASH
    RISK: MEDIUM
    RULE: FRACTION_SLASH ≠ FULLWIDTH_SOLIDUS (дробный знак;
    confusables.txt: 2044→002F)

  CONFUSABLE_004:
    VISIBLE_FORM: ╱
    CODEPOINT: U+2571
    NAME: BOX DRAWINGS LIGHT DIAGONAL UPPER RIGHT TO LOWER LEFT
    RISK: LOW
    RULE: BOX_DIAGONAL ≠ FULLWIDTH_SOLIDUS (псевдографика)

  CONFUSABLE_005:
    VISIBLE_FORM: ⧸
    CODEPOINT: U+29F8
    NAME: BIG SOLIDUS
    RISK: LOW
    RULE: BIG_SOLIDUS ≠ FULLWIDTH_SOLIDUS (математический оператор)

============================================================
6. SIGN_RELATIONS  [ИСТОЧНИК ИСТИНЫ ДЛЯ РАНТАЙМА — ось «отношение»]
============================================================

SIGN_RELATIONS:
  RELATION_001:
    RELATION_TYPE: NFKC_MAPS_TO
    TARGET: U+002F
    CONTEXT_SCOPE: URL, HOST, PATH
    VERIFICATION_STATUS: VERIFIED
    RUNTIME_EFFECT: RELATION_ONLY

RELATION_001_JUSTIFICATION:
  - Тип NFKC_MAPS_TO, а НЕ CONFUSABLE_OF: в confusables.txt Unicode
    17.0.0 ПРЯМОЙ записи FF0F→002F НЕТ; связь идёт через совместимую
    декомпозицию <wide> 002F и NFKC-нормализацию (проверено на
    источниках проекта). Факт стандарта, не «мнение о похожести».
  - VERIFIED: связь — нормативный факт Unicode, воспроизводимый
    (unicodedata.normalize('NFKC','／') == '/').
  - CONTEXT_SCOPE URL, HOST, PATH: машинные латинские контексты, где
    канон / несёт структурную роль и подмена меняет разбор строки.
    EMAIL не включён в первый заход: / в email-адресах не является
    структурным разделителем (у email канон-разделитель @ и .).
  - Вне scope (CJK-текст, свободный текст) ребро не активируется —
    знак живёт своей жизнью (D-REL-3, кейс ＠-паттерн).

============================================================
7. CONTRADICTION_GUARDS  [МИНИМУМ 6]
============================================================

CONTRADICTION_GUARDS:
  CG_001:
    RULE: RELATION_FOUND ≠ THREAT — наличие ребра само по себе не риск.
  CG_002:
    RULE: CJK_LEGITIMACY ≠ ATTACK_IMMUNITY — легитимность в CJK-тексте
      не отменяет маскировочный потенциал в URL.
  CG_003:
    RULE: NFKC_EQUIVALENCE ≠ VISUAL_IDENTITY — машинная эквивалентность
      (после нормализации) и визуальная похожесть — разные основания;
      карточка опирается на первую.
  CG_004:
    RULE: CARD_DECLARES ≠ CARD_JUDGES — карточка объявляет отношение,
      вердикт выносит sequence-слой (D-REL-4).
  CG_005:
    RULE: MASK_WITHOUT_MATCHER — у знака-маски НЕТ собственного
      матчера; это не пробел реализации, а архитектура (короткий путь
      маски, README/правила R1).
  CG_006:
    RULE: SCOPE_LIMITS_VERDICT — вне CONTEXT_SCOPE ребра вердикт не
      выносится, даже если знак стоит рядом с подозрительным.

============================================================
8. SEQUENCE_LAYER_BOUNDARY  [ОБЯЗАТЕЛЬНО]
============================================================

SEQUENCE_LAYER_BOUNDARY: Карточка НЕ содержит SEQUENCE_CANDIDATES.
Межзнаковое поведение маски (позиция в URL, соседство со схемой,
смешение с каноном) оценивается sequence-слоем через
active_relation_candidates (барьер N3) и _assess_relation_risk
(STAGE_6b). Шкала: HOST→HIGH, URL/PATH→MEDIUM, FREE_TEXT→NONE;
CANDIDATE-ребро понижало бы на ступень (здесь VERIFIED — без
понижения). Зонд канона отложен (canon_hypothesis=None).

============================================================
9. LIMITATION_STATEMENT  [ОБЯЗАТЕЛЬНО]
============================================================

- ПОКРЫТО с 2026-07-12 (детектор Г1, AUTHOR_DECISION D-DET-1/2):
  голые домены без схемы (gоog／le.com → HOST), внешняя пунктуация
  вокруг домена, хвосты справа (path/порт/query), IDN/punycode
  (приме／р.рф → HOST), двойная маска в одном токене (D-DET-1),
  деградация TLD-справочника → тревога + прогон DEGRADED (D-DET-2).
  Код детектора: NEW_ARTIFACT, NOT_REVIEWED — карточка и детектор
  идут на конвейер ОДНИМ пакетом.
- ИСПРАВЛЕНО с 2026-07-12 (FIX_FIRST, первый круг конвейера): обрезка
  пунктуации переписана с чёрного списка (_STRIP_OUTER) на позитивную
  выборку домено-подобных символов (символы, для которых isalnum()
  истинно — буквы и цифры Unicode, НЕ «любой алфавит»: см. ниже про
  combining marks — плюс дефис и точка). Три ревьюера нашли обход:
  обрамление домена символом ВНЕ
  чёрного списка (markdown *, тире, тильда, pipe, полноширинная
  кавычка) прилипало к домену → тихий FREE_TEXT. Позитивная выборка
  закрывает весь класс обхода, не по символу.
- ИСПРАВЛЕНО с 2026-07-12 (FIX_FIRST, второй/узкий круг, AUTHOR_DECISION
  D-DET-4): ведущий структурный разделитель (/ \ ? # : @) перед
  доменным блоком — HARD_STOP (позитивная выборка возвращает пустую
  строку), а не пропускаемая обёртка. Без этого @example.com／x,
  /example.com／x читались как голые домены → PATH; теперь → FREE_TEXT
  (структурный символ сохраняет смысл; обёртки *, тире и пр. по-прежнему
  пропускаются). Закрытый список структурных границ ≠ бесконечный чёрный
  список пунктуации.
- ИЗВЕСТНОЕ ОГРАНИЧЕНИЕ combining marks (2026-07-12, второй круг):
  isalnum() ложен для combining marks (Unicode Mn/Mc), поэтому IDN-метка
  с огласовкой/диакритикой (деванагари U+093E DEVANAGARI VOWEL SIGN AA,
  арабские диакритики, ивритские огласовки, NFD-разложенная латиница)
  обрывает позитивную выборку на базовой букве → FREE_TEXT. Это НЕ
  регрессия (старый чёрный список тоже отвергал такую метку проверкой
  isalnum-or-hyphen), но формулировка «любой алфавит» была ложной и
  исправлена. Закрытие требует IDNA/NFC-канонизации кандидата — вне
  scope грубого детектора. Закреплено gate-кейсом (escape-строка).
- ИЗВЕСТНО и НЕ ЧИНИТСЯ (AUTHOR_DECISION D-DET-3, 2026-07-12): сама
  позитивная выборка — эвристика без полного URL-парсера, поэтому
  склейка левой и правой части через маску может дать ложное HOST на
  двух не связанных фрагментах, если результат синтаксически похож на
  домен (my-host／name.com → HOST; example.com,／test → HOST, «test»
  теряется). ДОПОЛНЕНИЕ (второй круг): маска ПОСЛЕ домена тоже читается
  как HOST, а не PATH (gоogle.com*／path → HOST — трейлинг-обёртка
  обрывает run на домене; ／ физически в path-сегменте). Задокументировано
  в gate_bare_domain_detector.py, не считается дефектом — см. файлы
  AUTHOR_DECISION FIX_FIRST_ROUND1/ROUND2 в foundation_layer.
- ОТЛОЖЕНО на v0.5 (известно, не чинится в этом круге): уже-punycode
  TLD-метка, отсутствующая в АКТИВНОМ справочнике (gоog／le.xn--zckzah
  → тихий FREE_TEXT — зависимость от полноты справочника, не
  самостоятельный баг детектора); дефис на краю метки (RFC 952/1035
  запрещает, текущая проверка метки этого не требует —
  -example.com／x → PATH, домен с ведущим дефисом проходит).
- Карточка НЕ ловит: EMAIL-контекст (вне scope первого захода);
  zero-width символы между метками домена (не объявлены масками ни в
  одной карточке — отдельный вектор нормализации, gate показывает
  границу явно); порт как отдельную зону (порт считается частью
  HOST — консервативно, риск не занижается).
- Карточка НЕ решает: агрегацию при будущих нескольких рёбрах,
  различие силы NFKC vs CONFUSABLE (тип ребра пока не влияет на риск
  — открытый вопрос проекта).
- Статус WORKING_DRAFT: до прохождения конвейера и присвоения
  AUTHOR_DECISION результаты по знаку не считаются надёжными
  (рантайм печатает CARD_WARNING — это правильно).

============================================================
10. KNOWN_OPEN_QUESTIONS
============================================================

ALL_OPEN_QUESTIONS_CLOSED: NO

OPEN_QUESTION_001:
  NAME: MASK_BREAKS_NEIGHBOR_CONTEXT
  DATE_RAISED: 2026-07-12
  STATEMENT: маска рвёт контекст СОСЕДНЕМУ ASCII-знаку. Пример:
    src/utils／main.py — ось маски корректно даёт FREE_TEXT/NONE,
    но легаси solidus_matcher теряет path-субстрат у первого «/»
    («src/utils» без продолжения пути) и падает в fallback
    RISK_CASE_008 (path_or_choice_separator, MEDIUM) →
    QUEUE_FOR_REVIEW. Базовая линия: тот же текст целиком в ASCII
    (src/utils/main.py) → filesystem_path, PASS.
  SOURCE: обнаружено 2026-07-12 при FP-прогоне детектора Г1;
    вердикт даёт НЕ ось маски (она чиста), а сосед по токену.
  STATUS: не баг, но неназванный шов. Требует решения:
    уместная настороженность (замаскированный путь ЗАСЛУЖИВАЕТ
    взгляда — маска в машинной строке аномальна сама по себе)
    или ложняк (легитимный CJK-пользователь в path-строке получит
    QUEUE на ровном месте). Решение — AUTHOR_DECISION, не код
    по-тихому: затрагивает и solidus_matcher (single-sign слой),
    и, возможно, будущий канал «маска в токене» → соседним
    матчерам (данные, не вердикт — по образцу D-REL-5).
