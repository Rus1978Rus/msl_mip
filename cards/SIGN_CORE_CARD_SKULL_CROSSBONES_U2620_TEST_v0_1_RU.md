ЧАСТНЫЙ АВТОРСКИЙ ПРОЕКТ / COMMERCIAL USE PROHIBITED

DOCUMENT_ID: SIGN_CORE_CARD_SKULL_CROSSBONES_U2620_TEST_v0_1_RU
DOCUMENT_TYPE: SIGN_CORE_CARD
TEMPLATE_LINE: GEN3_v0_3 (упрощённая версия для тестового знака)
DOCUMENT_STATUS: SUPERSEDED
STATUS: SUPERSEDED_BY_GEN3_v0_3 / NOT_ACTIVE / RETAINED_AS_LEGACY
SUPERSEDED_BY: SIGN_CORE_CARD_SKULL_CROSSBONES_U2620_GEN3_v0_3_RU
SUPERSEDED_AT: 2026-07-04
SUPERSEDED_NOTE: эта упрощённая тестовая карточка наращена до полного
  стандарта GEN3_v0_3. Сохраняется как legacy (правило LEGACY≠DELETE),
  но НЕ активна (правило ONE_ACTIVE_CARD_PER_SIGN). Активная карточка —
  GEN3_v0_3.
AUTHOR: Руслан Малявский (по согласованию, координатор — Claude)
CREATED_AT: 2026-06-29

ЧЕСТНОЕ ПРИМЕЧАНИЕ О СТАТУСЕ: эта карточка СОЗНАТЕЛЬНО не проходила
полный CONVEYOR_DISCIPLINE (нет TIER3-прогона, нет 5 независимых
ревьюеров, нет ADVERSARIAL_COVERAGE/MUTATION_CHECK секций). Создана
как тестовый артефакт для проверки межкарточной SEQUENCE-логики на
ДВУХ знаках-эмодзи, оба с реальными карточками (раньше у SKULL.SC2/
SC3 второй эмодзи всегда был "контекстом без карточки" — это не
давало протестировать настоящую кросс-карточную валидацию). Перед
использованием в production-конвейере требует отдельного полного
прогона по дисциплине GEN3_v0_3, как DOT/SOLIDUS/SKULL.

ОБОСНОВАНИЕ ДИЗАЙНА (Foundation Layer):
  FO-099 SIGN_OUTLIVES_FUNCTION (основное) — ☠ исторически и
    физически — знак опасности/яда (этикетки токсичных веществ,
    пиратский флаг), эта функция сегодня частично дормантна в
    цифровой среде и соседствует с ироническим интернет-
    использованием, похожим на 💀. Структурно то же напряжение,
    что и в кейсах FO-099 (свастика, иероглифы, приветствие).
  FO-013 SUBSTRATE_INDEPENDENCE (вспомогательное) — паттерн
    "форма опасности" интерпретируется одинаково независимо от
    того, физическая это этикетка или цифровой эмодзи.

============================================================
0. UNIVERSALITY
============================================================

BOUND_TO_SPECIFIC_SIGN: YES
AFTER_USE_RESIDUE: FORBIDDEN
SIGN_DATA_IS_SESSION_ONLY: YES

============================================================
4. SIGN_IDENTITY
============================================================

CARD_UID: SIGN_CORE_CARD_SKULL_CROSSBONES_U2620_TEST_v0_1
CODEPOINT: U+2620
VISIBLE_FORM: ☠
UNICODE_NAME: SKULL_AND_CROSSBONES
ZONE: ZONE_3
BASE_MODE: EPOCH_DEPENDENT
BASE_MODE_FORMULA: ACTIVE_EPOCH определяет интерпретацию; см.
  CAPTURE_HISTORY ниже. В отличие от 💀 (где EPOCH_3 юмор доминирует
  глобально), у ☠ EPOCH_1 (буквальная опасность) остаётся активной
  чаще — знак физически используется на реальных предупреждающих
  этикетках до сих пор, не полностью дормантен.

============================================================
5. SEMANTIC_EPOCH_TRACKER (CAPTURE_HISTORY)
============================================================

ACTIVE_EPOCH_TYPE: CONTEXT_DEPENDENT_WITH_EPOCH_1_BIAS

CAPTURE_HISTORY:
  EPOCH_1:
    NAME: literal_hazard_warning
    DATE_RANGE: ~19 век — настоящее время
    SUBSTRATE: физические этикетки (яд, токсичные вещества),
      пиратская символика (Jolly Roger), хазмат-маркировка
    FUNCTION: буквальное предупреждение об опасности/яде/смерти
    STATUS: ACTIVE (не дормантна — знак физически используется по
      сей день на реальных предупреждающих маркировках)

  EPOCH_2:
    NAME: gaming_death_indicator
    DATE_RANGE: ~1980-е — настоящее время
    SUBSTRATE: видеоигры (экран "Game Over", индикатор смерти
      персонажа)
    FUNCTION: игровой маркер поражения/смерти персонажа, не
      буквальная угроза
    STATUS: ACTIVE

  EPOCH_3:
    NAME: internet_irony_intensifier
    DATE_RANGE: ~2010-е — настоящее время
    SUBSTRATE: социальные сети, мессенджеры (часто в паре с 💀)
    FUNCTION: усиление иронии/шока ("этот момент был ☠" =
      "это было жёстко/смешно до предела") — как правило более
      интенсивный регистр, чем одиночный 💀
    STATUS: ACTIVE

============================================================
7. SAFE_CASES / RISK_CASES / SEQUENCE_LAYER_BOUNDARY
============================================================

SAFE_CASES:
  SAFE_CASE_001:
    NAME: literal_hazard_label
    INPUT: "Внимание: ядовито ☠"
    CONTEXT: буквальное предупреждение на этикетке/инструкции
    RISK: NONE
    GUARD: ""

  SAFE_CASE_002:
    NAME: gaming_death_marker
    INPUT: "Ты погиб ☠ Начать заново?"
    CONTEXT: игровой интерфейс, не угроза
    RISK: NONE
    GUARD: ""

  SAFE_CASE_003:
    NAME: irony_intensifier
    INPUT: "этот ответ на экзамене был ☠"
    CONTEXT: интернет-ирония, усиление эмоции, не угроза
    RISK: NONE
    GUARD: ""

RISK_CASES:
  RISK_CASE_001:
    NAME: THREAT_PHRASE_OBFUSCATED_AS_HAZARD_WARNING
    INPUT: "я тебя отравлю ☠"
    CONTEXT: угроза, маскирующаяся под предупреждение об опасности
    RISK: HIGH
    ATTACK: использует буквальную EPOCH_1-функцию знака (опасность)
      как прикрытие для реальной угрозы, не иронии
    GUARD: фраза-угроза детектируется структурно (см. матчер),
      приоритет над generic EPOCH-классификацией

CONFUSABLES: (нет — emoji-форма уникальна в Unicode)

CONTRADICTION_GUARDS: (нет дополнительных сверх общих)

SEQUENCE_LAYER_BOUNDARY:
  SC1:
    SEQUENCE: "☠☠☠"
    NAME: TRIPLE_SKULL_CROSSBONES_SPAM
    RISK_LEVEL: intensity-dependent
    POSSIBLE_CONTEXTS: повторение усиливает либо иронию, либо
      спам-паттерн — требует контекста, не детектируется однозначно
      структурой (аналогично SKULL.SC1/SC5)

RAW_SEQUENCE_TEXT_IS_NOT_SIGN_CARD_INPUT: YES
SEQUENCE_ADVISORY_ONLY: YES

============================================================
12. LIMITATION_STATEMENT
============================================================

Эта карточка — тестовый артефакт, не прошедший полный конвейер
GEN3_v0_3. EPOCH_TRACKER и RISK_CASES основаны на единичном
авторском проходе с опорой на FO-099/FO-013, не на множественном
независимом ревью. RISK_CASE_001 — единственный структурно
проверяемый риск; буквальной/иронической границы (EPOCH_1 vs
EPOCH_3) без контекста однозначно не существует — это намеренное
ограничение, не упущение.

END_OF_DOCUMENT
