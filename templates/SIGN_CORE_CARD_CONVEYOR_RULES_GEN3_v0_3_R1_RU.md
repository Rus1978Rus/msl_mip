ЧАСТНЫЙ АВТОРСКИЙ ПРОЕКТ / COMMERCIAL USE PROHIBITED

DOCUMENT_ID: SIGN_CORE_CARD_CONVEYOR_RULES_GEN3_v0_3_R1_RU
DOCUMENT_TYPE: CONVEYOR_DISCIPLINE_RULESET
TEMPLATE_LINE: GEN3_v0_3
DOCUMENT_STATUS: WORKINGLY_CLOSED
STATUS: WORKINGLY_CLOSED / NOT_LOCKED / NOT_RUNTIME / NOT_VALIDATOR / NOT_PRODUCTION
AUTHOR_DECISION_REFERENCE: AUTHOR_DECISION_20260621_001_SIGN_CORE_CARD_CONVEYOR_RULES_v0_3_WORKINGLY_CLOSED_RU
AUTHOR: Руслан Малявский
CREATED_AT: 2026-06-21
SUPERSEDES: SIGN_CORE_CARD_TEMPLATE_GEN3_CONVEYOR_v0_2_PLUS_EPOCH (правила конвейера,
  не сам шаблон — шаблон создаётся отдельным документом
  SIGN_CORE_CARD_TEMPLATE_GEN3_v0_3)

============================================================
0. ПРИЧИНА СОЗДАНИЯ ЭТОГО ДОКУМЕНТА
============================================================

Пять карточек знака (DOT, AT, HASH, SKULL, SOLIDUS), прошедшие
конвейер v0_2_PLUS_EPOCH и получившие статус WORKINGLY_CLOSED,
при сквозном построчном аудите показали структурные пробелы.

SOURCE_AUDIT_TABLE (построчная проверка, выполнена автором
  документа лично через прямой grep по первоисточникам,
  AUDIT_DATE: 2026-06-20/21, повторно сверено в ходе внешнего
  конвейерного ревью этого документа):

  CARD: DOT
    CARD_UID_PRESENT: NO
    ZONE_PRESENT: YES (ZONE_1)
    BASE_MODE_PRESENT: YES
    CODEPOINT_FIELD_NAME_USED: UNICODE
    GLYPH_FIELD_NAME_USED: GLYPH

  CARD: AT
    CARD_UID_PRESENT: NO
    ZONE_PRESENT: YES (ZONE_3)
    BASE_MODE_PRESENT: NO
    CODEPOINT_FIELD_NAME_USED: SIGN_UNICODE
    GLYPH_FIELD_NAME_USED: SIGN_GLYPH

  CARD: HASH
    CARD_UID_PRESENT: YES
    ZONE_PRESENT: YES (ZONE_3)
    BASE_MODE_PRESENT: YES
    CODEPOINT_FIELD_NAME_USED: SIGN
    GLYPH_FIELD_NAME_USED: VISIBLE_FORM

  CARD: SKULL
    CARD_UID_PRESENT: YES
    ZONE_PRESENT: YES (ZONE_3)
    BASE_MODE_PRESENT: YES
    CODEPOINT_FIELD_NAME_USED: SIGN
    GLYPH_FIELD_NAME_USED: VISIBLE_FORM

  CARD: SOLIDUS
    CARD_UID_PRESENT: YES
    ZONE_PRESENT: NO (на момент исходного аудита; пропатчено
      впоследствии в обоих языках — ZONE_2 добавлен)
    BASE_MODE_PRESENT: YES
    CODEPOINT_FIELD_NAME_USED: SIGN
    GLYPH_FIELD_NAME_USED: VISIBLE_FORM

SUMMARY_FROM_TABLE:
  CARD_UID отсутствует: 2 из 5 (DOT, AT)
  ZONE отсутствовал: 1 из 5 (SOLIDUS, исправлено патчем)
  BASE_MODE отсутствует: 1 из 5 (AT)
  Имена поля кодпоинта: 3 разных варианта (UNICODE / SIGN_UNICODE / SIGN)
  Имена поля глифа: 3 разных варианта (GLYPH / SIGN_GLYPH / VISIBLE_FORM)

VERIFICATION_NOTE: в ходе внешнего конвейерного ревью этого документа
  один из ревьюеров (Qwen) предложил уточнение "3 из 5 карточек без
  CARD_UID, включая SKULL" — это уточнение было проверено автором
  документа лично через прямой grep по файлу SKULL и ОТКЛОНЕНО как
  неточное: SKULL содержит CARD_UID (подтверждено построчно). Этот
  эпизод сохранён здесь как живая иллюстрация самого правила 8
  (см. раздел 8) — даже явная попытка верификации может содержать
  ошибку, и формальный акт "уточнения" не делает второе утверждение
  автоматически более достоверным, чем первое, без независимой
  проверки против первоисточника.

КОРНЕВАЯ ПРИЧИНА (из таблицы выше): конвейер v0_2_PLUS_EPOCH проверял
КАЧЕСТВО содержимого карточки (MUTATION_CHECK, ADVERSARIAL_EVIDENCE,
MODEL_FAMILY_DIVERSITY), но НЕ проверял ПОЛНОТУ и ЕДИНООБРАЗИЕ
структуры относительно шаблона и относительно других уже
закрытых карточек.

ВТОРАЯ КОРНЕВАЯ ПРИЧИНА: WORKINGLY_CLOSED присваивался по
результатам изолированного ревью текста карточки. Ни одна
карточка не проходила реальное сквозное исполнение через
MODULE_TEMPLATE до получения этого статуса. Структурные дыры
(отсутствие ZONE) обнаруживались только при попытке реально
прогнать карточку через pipeline — то есть после того, как
статус уже был присвоен.

============================================================
1. ПРИНЦИП: WORKINGLY_CLOSED ≠ ГОТОВ К ИСПОЛЬЗОВАНИЮ
============================================================

FORMULA:
  TEXT_REVIEW_PASS ≠ EXECUTABLE
  WORKINGLY_CLOSED (старое значение) ≠ SIMULATION_CONFIRMED
  STRUCTURAL_COMPLETENESS ≠ CONTENT_QUALITY
  (карточка может быть качественной по содержанию и при этом
   неполной по структуре — это два разных измерения проверки)

НОВОЕ ПРАВИЛО:
  Карточка знака получает финальный статус ARTIFACT_CONFIRMED
  только после прохождения SIMULATION_GATE (см. раздел 5).
  WORKINGLY_CLOSED становится промежуточным статусом, не финальным.

STATUS_PROGRESSION (новая цепочка):
  WORKING_DRAFT
    → STRUCTURAL_PREFLIGHT_PASS (новый шаг — проверка наличия всех
        REQUIRED_FIELDS из раздела 2, ДО текстового конвейерного
        ревью; механическая/быстрая проверка, не требует полного
        раунда моделей)
    → CONVEYOR_REVIEW_PASS (текстовое ревью качества содержимого,
        как раньше — MUTATION_CHECK, ADVERSARIAL_EVIDENCE,
        MODEL_FAMILY_DIVERSITY)
    → WORKINGLY_CLOSED (как раньше, но не финал)
    → SIMULATION_GATE_PASSED (новый шаг, см. раздел 5, с градацией
        по TIER в зависимости от ZONE)
    → ARTIFACT_CONFIRMED (новый финальный статус)

  Любой провал на любом шаге → возврат к WORKING_DRAFT с
  открытым списком находок, не молчаливое накопление дыр.

  PATCH_NOTE: исходная версия документа располагала
  STRUCTURAL_COMPLETENESS_VERIFIED после CONVEYOR_REVIEW_PASS —
  это создавало риск тратить полный раунд текстового ревью на
  карточку, у которой структурные пробелы можно обнаружить
  мгновенно. Исправлено по итогам внешнего конвейерного ревью
  (GPT-5.5): структурная проверка теперь предшествует содержательной.

============================================================
2. ОБЯЗАТЕЛЬНЫЕ ПОЛЯ КАРТОЧКИ (REQUIRED_FIELDS)
============================================================

В отличие от v0_2_PLUS_EPOCH, где обязательность полей
выводилась из примера заполнения шаблона (неявно), v0_3
фиксирует явный список. Карточка НЕ МОЖЕТ получить статус
CONVEYOR_REVIEW_PASS без всех полей из этого списка.

REQUIRED_FIELDS_META:
  CARD_UID                  (уникальный идентификатор карточки;
                              ОБЯЗАТЕЛЬНО — отсутствовало у DOT, AT)
  CODEPOINT                  (Unicode codepoint, формат U+XXXX —
                              единственное каноническое имя для
                              этого значения; поле SIGN запрещено
                              как дубликат, см. PATCH_NOTE_v0_3_P1)
  VISIBLE_FORM               (видимый глиф знака)
  UNICODE_NAME               (официальное имя Unicode)
  ZONE                       (ZONE_1 / ZONE_2 / ZONE_3 —
                              ОБЯЗАТЕЛЬНО — отсутствовало у SOLIDUS)
  DOCUMENT_STATUS
  TEMPLATE_LINE
  SOURCE_TEMPLATE
  AUTHOR                     (ОБЯЗАТЕЛЬНО — отсутствовало в
                              исходной версии v0_3, добавлено по
                              итогам внешнего конвейерного ревью)
  CREATED_AT                 (ОБЯЗАТЕЛЬНО)
  VERSION                    (ОБЯЗАТЕЛЬНО)
  AUTHOR_DECISION_REFERENCE  (ОБЯЗАТЕЛЬНО)
  RUN_CARD_REFERENCE         (ОБЯЗАТЕЛЬНО)
  RUN_CARD_STATUS            (ОБЯЗАТЕЛЬНО)

REQUIRED_FIELDS_META_OPTIONAL (добавлено по итогам третьего раунда
  внешнего ревью — Kimi/Grok):
  RUN_CARD_DATE   (опционально; обязательно, только если
                    RUN_CARD_STATUS содержит датированный результат
                    конвейерного прогона; встречается в HASH)
  PATCHED_AT      (опционально; обязательно, только если карта
                    патчилась после CREATED_AT; встречается в HASH)
  DISPLAY_NAME    (опционально; человекочитаемое название знака
                    помимо официального UNICODE_NAME — например,
                    "точка" для FULL STOP; см. также LEGACY_FIELD_MAPPING
                    в разделе 3, где SIGN_NAME из старых карт
                    маппится сюда)

PATCH_NOTE_v0_3_P1: исходная версия документа требовала одновременно
  SIGN (в META) и CODEPOINT (в LAYER_A) для одного и того же значения
  кодпоинта — внутреннее противоречие, найденное внешним ревью
  (GPT-5.5), подтверждённое автором документа построчной проверкой.
  Исправлено: единственное каноническое имя — CODEPOINT, во всех
  секциях документа.

REQUIRED_FIELDS_LAYER_A:
  VISIBLE_FORM
  BASE_MODE                  (категориальное значение, например
                              DATA_ONLY, DATA_ONLY_SEPARATOR —
                              ОБЯЗАТЕЛЬНО — отсутствовало у AT.
                              НЕ заменяется BASE_MODE_FORMULA —
                              это разные поля: BASE_MODE = категория,
                              BASE_MODE_FORMULA = формула)
  BASE_MODE_FORMULA
  SIGN_CATEGORY
  WHAT_THIS_SIGN_IS_NOT       (минимум 10 пунктов)
  BASE_FORMULAS                (минимум 10 формул)

REQUIRED_FIELDS_LAYER_B:
  SAFE_CASES                 (минимум 6)
  RISK_CASES                  (минимум 6)
  CONFUSABLES                 (минимум 5)
  CONTRADICTION_GUARDS        (минимум 6)
  SEQUENCE_LAYER_BOUNDARY     (может быть NOT_APPLICABLE с явным
                              обоснованием, но поле должно
                              присутствовать)
  PHAGO_ENTITY_MIMICRY        (может быть пустым с явным
                              NOTE, но поле должно присутствовать)

REQUIRED_FIELDS_LAYER_C:
  EFFECT_FIELDS (все 10 полей: authority/trust/verification/
    proof/execution/permission/status/role_assignment/runtime/
    existence)
  EFFECT_FIELDS_ALL_NONE
  CLOSED_SCHEMA

OPTIONAL_FIELDS_RELATION (ось «отношение», AUTHOR_DECISION_20260708;
  добавлено ревизией R1 после реализации оси в коде):

  SIGN_RELATIONS — ОПЦИОНАЛЬНЫЙ блок. Заводится ТОЛЬКО когда знак
  является маской (гомоглифом) другого знака, т.е. может визуально
  подменять канон в определённом контексте. Обычные знаки блок НЕ
  имеют (отсутствие блока = нет активных отношений, знак работает как
  самостоятельный; legacy-карточки v0_3 блок НЕ мигрируют — D1).

  КОГДА ЗАВОДИТЬ РЕБРО: знак похож на другой (канон) настолько, что
  может им притворяться в конкретном контексте (URL, домен, путь...).
  Само сходство — НЕ угроза (RELATION_FOUND ≠ THREAT); ребро лишь
  фиксирует связь, риск решает рантайм по контексту. НЕ заводить рёбра
  «на всякий случай» — лишние рёбра порождают ложные срабатывания.

  ПОЛЯ РЕБРА (RELATION_NNN):
    RELATION_TYPE      — CONFUSABLE_OF (визуально путается) /
                         NFKC_MAPS_TO (нормализуется в канон) /
                         VISUAL_MIMIC_OF (визуальная мимикрия)
    TARGET             — канон: кодпоинт или последовательность
                         (напр. U+002F)
    CONTEXT_SCOPE      — где связь активна (одно или несколько через
                         запятую): URL / HOST / PORT / PATH / EMAIL /
                         IDENTIFIER / IDN / CODE / FREE_TEXT / ANY.
                         HOST = доменная часть (главный кейс подмены).
                         ANY = «везде» — применять ОСТОРОЖНО (высокий
                         риск ложных срабатываний); только для
                         контекст-независимых связей. Ребро БЕЗ scope
                         не сработает нигде (кроме ANY) — валидатор
                         выдаёт RELATION_WITHOUT_SCOPE.
    VERIFICATION_STATUS — VERIFIED / CANDIDATE / MANUAL_OVERRIDE.
                         CANDIDATE понижает итоговый риск на ступень.
    RUNTIME_EFFECT     — ВСЕГДА RELATION_ONLY (зашитый инвариант:
                         ребро сообщает о сходстве, НЕ о риске).
    IS_ACTIVE          — опционально; TRUE по умолчанию. FALSE/NO/0/OFF
                         отключает ребро без удаления. Если ВСЕ рёбра
                         выключены — валидатор выдаёт
                         ALL_RELATIONS_INACTIVE (след аудита, не ошибка).

  ГРАНИЦА: риск маски выносит SEQUENCE-слой (ребро + защищённый
  контекст + соседи), НЕ карточка и НЕ single-sign. Карточка лишь
  ОБЪЯВЛЯЕТ связь. Провенанс похожих знаков остаётся в CONFUSABLES
  (человекочитаемый список); рантайм рёбра берёт ТОЛЬКО из
  SIGN_RELATIONS, CONFUSABLES как рёбра НЕ читает.

  ПРИМЕР (маска полноширинного солидуса ／ U+FF0F):
    SIGN_RELATIONS:
      RELATION_001:
        RELATION_TYPE: CONFUSABLE_OF
        TARGET: U+002F
        CONTEXT_SCOPE: URL, HOST, PATH
        VERIFICATION_STATUS: VERIFIED
        RUNTIME_EFFECT: RELATION_ONLY
    → рантайм: ／ в http://gоog／le.com (host) → HIGH;
      в http://ok.com/a／b (path) → MEDIUM; в свободном тексте → NONE.

REQUIRED_FIELDS_SEMANTIC_EPOCH_TRACKER:
  Для ZONE_1: EPOCH_TRACKER: NOT_APPLICABLE с явным NOTE
    почему (полисемия без прецессии)
  Для ZONE_2: EPOCH_TRACKER: CONTEXT_GATE_REQUIRED с явным
    APPLICABILITY и CAPTURE_HISTORY (если применимо)
  Для ZONE_3: EPOCH_TRACKER: REQUIRED с полным CAPTURE_HISTORY,
    ACTIVE_EPOCH, DORMANT_EPOCHS, PRECESSION_ALERT

  ПРАВИЛО: независимо от ZONE, секция SEMANTIC_EPOCH_TRACKER
  ДОЛЖНА присутствовать с явным значением EPOCH_TRACKER.
  Никогда не оставлять подразумеваемым.

REQUIRED_FIELDS_DOCUMENT_LEVEL:
  ADVERSARIAL_COVERAGE (с MIN_TOTAL_VECTORS, ACTUAL_TOTAL_VECTORS,
    COVERAGE_STATUS — все три поля обязательны, не только MIN)
  MUTATION_CHECK (минимум 6 мутаций, каждая с CLAIM/EXPECTED/RESULT)
  KNOWN_OPEN_QUESTIONS (может быть пустым списком с явным
    ALL_OPEN_QUESTIONS_CLOSED: YES)
  PATCH_HISTORY (формат зафиксирован в разделе 4)
  LIMITATION_STATEMENT
  INTEGRATION_INTERFACE_STATUS

============================================================
3. ЕДИНЫЙ ФОРМАТ ИМЕНОВАНИЯ ПОЛЕЙ (NAMING_NORM)
============================================================

НАЙДЕННАЯ ПРОБЛЕМА: одна и та же концепция называлась по-разному
в разных картах:
  Имя знака:    SIGN_NAME (DOT, AT) vs нет отдельного поля (HASH/SKULL/SOLIDUS)
  Кодпоинт:     UNICODE (DOT) vs SIGN_UNICODE (AT) vs SIGN (HASH/SKULL/SOLIDUS)
  Глиф:         GLYPH (DOT) vs SIGN_GLYPH (AT) vs VISIBLE_FORM (HASH/SKULL/SOLIDUS)

КАНОНИЧЕСКОЕ РЕШЕНИЕ (обязательно для всех новых карточек):
  Кодпоинт      → CODEPOINT: U+XXXX
  Глиф          → VISIBLE_FORM: <символ>
  Имя Unicode   → UNICODE_NAME: <официальное название>

  Поле SIGN_NAME / SIGN_UNICODE / SIGN_GLYPH / UNICODE / GLYPH / SIGN
  ЗАПРЕЩЕНЫ в новых карточках. Если нужно человекочитаемое
  название знака помимо UNICODE_NAME — использовать поле
  DISPLAY_NAME как дополнительное, не замену.

REASON_FOR_CHOICE: канон CODEPOINT/VISIBLE_FORM/UNICODE_NAME выбран,
  потому что:
  1. Терминология ближе к официальной номенклатуре Unicode Consortium
  2. Используется в 3 из 5 существующих карточек (HASH, SKULL, SOLIDUS) —
     более позднее и более структурно зрелое поколение карт
  3. Раздельные имена (CODEPOINT vs VISIBLE_FORM) однозначно различают
     "что это технически" от "как это выглядит", в отличие от
     совмещённых вариантов SIGN_UNICODE/SIGN_GLYPH

LEGACY_FIELD_MAPPING (read-only, для совместимости при чтении
  существующих карт, НЕ для создания новых):
  SIGN_NAME       → DISPLAY_NAME (опционально)
  UNICODE         → CODEPOINT
  SIGN_UNICODE    → CODEPOINT
  SIGN            → CODEPOINT
  GLYPH           → VISIBLE_FORM
  SIGN_GLYPH      → VISIBLE_FORM

  Это маппинг для чтения, не требование переименовывать поля в
  legacy-картах. Любой будущий парсер/валидатор обязан поддерживать
  оба набора имён через этот маппинг, до момента (если будет принято
  отдельное решение), когда legacy-карты будут пересозданы под v0_3.

LOCK-ПОЛЯ (КАНОНИЧЕСКОЕ РЕШЕНИЕ):
  Используется раздельный подход (по образцу HASH/SKULL/SOLIDUS,
  не DOT/AT):
    LAYER_A_LOCK: PERMANENT
    LAYER_B_LOCK: REVIEWABLE
    LAYER_C_LOCK: SESSION
    SEMANTIC_EPOCH_TRACKER_LOCK: REVIEWABLE

  Единый блок SCHEMA_LOCK (как у DOT/AT) ЗАПРЕЩЁН в новых
  карточках — раздельные LOCK точнее отражают разную природу
  изменяемости каждого LAYER.

============================================================
4. ЕДИНЫЙ ФОРМАТ PATCH_HISTORY
============================================================

КАНОНИЧЕСКИЙ ФОРМАТ (обязателен для всех новых карточек):

  v0_X_PATCH_NN: <короткое_имя_патча> (<источник_ревью>,
    <дата>) — <описание, что изменено и почему>
    REASON: <если патч исправляет находку предыдущего ревью>
    PATCHES_APPLIED: N
    PATCHES_VERIFIED: N/N

  ЗАПРЕЩЕНО: пропуски в нумерации без явного объяснения
  (прецедент HASH.PATCHES_MISSING: P12 — допустим только
  с объяснением; немотивированные пропуски — находка).

============================================================
5. SIMULATION_GATE — ОБЯЗАТЕЛЬНЫЙ ШАГ ПЕРЕД ARTIFACT_CONFIRMED
============================================================

НОВОЕ ТРЕБОВАНИЕ, отсутствовавшее в v0_2_PLUS_EPOCH:

После получения WORKINGLY_CLOSED (текстовое ревью пройдено,
структура полна по REQUIRED_FIELDS) карточка ОБЯЗАНА пройти
минимум один сквозной симуляционный прогон:

  SIGN_CORE_CARD → MODULE_TEMPLATE → INTEGRATOR_TEMPLATE →
  RUNTIME_ACTION_REQUEST

  Минимум 2 разных контекста для знаков ZONE_2/ZONE_3
  (проверка DIFFERENTIATION_CHECK_MANDATORY — см. правило,
  установленное в SIMULATION_ARTIFACT_FIRST_PIPELINE_DOT_U002E_ZONE1).

  Минимум 1 контекст для знаков ZONE_1 (DIFFERENTIATION_CHECK
  не применим — ZONE_1 по определению не различает контексты).

SIMULATION_GATE_EXIT_CONDITIONS:
  ARCHITECTURE_BUG найден → возврат к WORKING_DRAFT, патч
    карточки ИЛИ патч шаблона (зависит от природы находки),
    повторный прогон с начала
  CARD_DATA_GAP найден (поле требуется pipeline, но отсутствует
    в карточке) → возврат к WORKING_DRAFT
  Все проверки пройдены, 0 ARCHITECTURE_BUG → ARTIFACT_CONFIRMED

SIMULATION_GATE_TIERS (градация по сложности знака, добавлено по
  итогам внешнего конвейерного ревью — единый порог для всех знаков
  создаёт риск bottleneck при масштабировании на десятки карточек):

  TIER_1 (ZONE_1 — стабильные знаки без контекстной вариативности):
    Минимум 1 контекст
    DIFFERENTIATION_CHECK не применяется (ZONE_1 по определению
      не различает контексты)
    Может быть выполнен автором самостоятельно, без обязательного
      внешнего конвейера моделей
    Документируется как упрощённый SIMULATION_ARTIFACT

  TIER_2 (ZONE_2 — контекстно-зависимые знаки):
    Минимум 2 контекста (рекомендуется 3, по образцу SOLIDUS)
    DIFFERENTIATION_CHECK_MANDATORY обязателен
    Минимум 1 независимый внешний ревьюер (не автор)

  TIER_3 (ZONE_3 — знаки с культурной прецессией эпох):
    Минимум 3 контекста, включая минимум 2 разные эпохи
      (DORMANT/ACTIVE) для проверки EPOCH_CONTEXT_INJECTION
    DIFFERENTIATION_CHECK_MANDATORY обязателен
    Минимум 2 независимых внешних ревьюера
    Полный SIMULATION_ARTIFACT документ (RU+EN при необходимости)

  Финальный статус ARTIFACT_CONFIRMED присваивается только после
  прохождения TIER, соответствующего ZONE данной карточки.

ТРЕБОВАНИЕ К ПРОТОКОЛУ СИМУЛЯЦИИ:
  Результат SIMULATION_GATE фиксируется как отдельный документ
  SIMULATION_ARTIFACT_<SIGN_NAME>_<CODEPOINT>, по аналогии с
  SIMULATION_ARTIFACT_FIRST_PIPELINE_DOT_U002E_ZONE1.
  Этот документ — часть пакета карточки, не опциональное
  приложение.

============================================================
6. ПРАВИЛО ИЗОЛИРОВАННОЙ ДОСТАВКИ КОНВЕЙЕРНЫХ ПАКЕТОВ
============================================================

(Перенесено из предыдущего раунда симуляции, формализуется
здесь как часть правил конвейера, не только как урок одного
случая.)

RULE_ID: ISOLATED_PACKET_DELIVERY_MANDATORY

При передаче карточки или симуляционного пакета любой
ревьюирующей модели — модель должна получать ТОЛЬКО
изолированный файл, не историю переписки. Перед каждым
конвейерным раундом координирующая сторона подтверждает это
явно.

============================================================
7. ПРАВИЛО ОБЯЗАТЕЛЬНОЙ ДИФФЕРЕНЦИАЦИИ
============================================================

(Перенесено из предыдущего раунда, формализуется здесь.)

RULE_ID: DIFFERENTIATION_CHECK_MANDATORY

ЕСЛИ один знак тестируется в N разных контекстах И
INTERPRETATION идентична во всех N контекстах ТО
автоматически ARCHITECTURE_BUG. Эта находка не может быть
понижена по дискреции отдельного ревьюера.

============================================================
8. ПРАВИЛО САМОПРОВЕРКИ ПЕРЕД ДОВЕРИЕМ ЧУЖОМУ АНАЛИЗУ
============================================================

(Новое правило, установленное по итогам этого раунда аудита.)

RULE_ID: VERIFY_BEFORE_TRUST_MANDATORY

Если один участник конвейера (модель) предоставляет таблицу
расхождений, диагноз или находку о состоянии файлов — другой
участник, прежде чем действовать на основе этого анализа
(патчить, создавать новые документы, менять архитектуру),
обязан самостоятельно проверить минимум часть заявленных
фактов против первоисточника.

ОБОСНОВАНИЕ: в ходе данного аудита были обнаружены и
исправлены три случая, где предоставленный анализ был неточен
(фактическая ошибка по HASH.BASE_MODE; ожидание наличия
DOT.LAYER_A_LOCK оказалось некорректным, поскольку DOT использует
старую SCHEMA_LOCK-схему той же эпохи шаблона, не раздельные
LAYER_*_LOCK — это пример того, что проверять нужно не только
наличие конкретного поля, но и то, какой поколенческой схеме
документа принадлежит карточка, прежде чем считать отсутствие
поля находкой;
"забегание вперёд" по статусу патча SOLIDUS.RU.ZONE, которого
фактически ещё не было). Цепочка моделей, нарастающая теориями
("STRUCTURAL_DRIFT" → "TEMPLATE_TO_TEMPLATE_INTERFACE_GAP" →
"CROSS_ARTIFACT_AUDIT_TEMPLATE") на основе непроверенного
анализа — это тот же класс риска, что и REVIEWED ≠ VALIDATED.

PATCH_NOTE_v0_3_P2 (третий раунд внешнего ревью — Kimi, Grok):
исходная формулировка примера про DOT.LAYER_A_LOCK была сама
неточна ("заявление о структуре, не подтверждённое при личной
проверке") — это маскировало реальную природу ошибки (ожидание
поля, которого не существует в данной поколенческой схеме
шаблона, а не недостоверное "заявление"). Формулировка исправлена
выше. Сохранено здесь как ещё один живой пример того, что даже
формулировка иллюстрации правила 8 сама прошла не один раунд
уточнения, прежде чем стала точной.

============================================================
ОГРАНИЧЕНИЯ
============================================================

THIS_DOCUMENT ≠ FINAL_TEMPLATE (это правила конвейера;
  сам канонический SIGN_CORE_CARD_TEMPLATE_GEN3_v0_3 создаётся
  отдельным документом на основе этих правил)
RULESET_CREATED ≠ RULESET_VALIDATED (правила сами должны пройти
  конвейерное ревью, прежде чем применяться)
WORKING_DRAFT ≠ WORKINGLY_CLOSED
EXISTING_CARDS_NOT_RETROACTIVELY_INVALIDATED: старые карточки
  (DOT, AT, HASH, SKULL, SOLIDUS под v0_2_PLUS_EPOCH) сохраняют
  свой текущий статус как LEGACY_PRE_v0_3; решение об их
  пересоздании с нуля под v0_3 принимается автором отдельно
  для каждой карточки, не автоматически этим документом

============================================================
END_OF_DOCUMENT
