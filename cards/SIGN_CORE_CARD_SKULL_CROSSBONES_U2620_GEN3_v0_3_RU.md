ЧАСТНЫЙ АВТОРСКИЙ ПРОЕКТ / COMMERCIAL USE PROHIBITED

DOCUMENT_ID: SIGN_CORE_CARD_SKULL_CROSSBONES_U2620_GEN3_v0_3_RU
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

STATUS_PROGRESSION_TRACKER:
  WORKING_DRAFT: YES
  STRUCTURAL_PREFLIGHT_PASS: PASS (2026-07-04)
  CONVEYOR_REVIEW_PASS: PASS (2026-07-04, 5/5 reviewers:
    Grok/Gemini/Kimi APPROVE, GPT-5.5 APPROVE_WITH_FIXES; fixes
    closed by PATCH_02)
  WORKINGLY_CLOSED: YES (2026-07-05, AUTHOR_DECISION Руслана Малявского
    после полного конвейера: волна 1 — 5/5 семейств, волна 2 — 2/2
    deep-research факт-аудита)
  SIMULATION_GATE_TIER: TIER_3 (следующий гейт)
  SIMULATION_GATE_PASSED: NOT_STARTED
  ARTIFACT_CONFIRMED: NOT_STARTED (требует SIMULATION_GATE)

============================================================
2. META
============================================================

CARD_UID: SIGN_CORE_CARD_SKULL_CROSSBONES_U2620_GEN3_v0_3_RU
CODEPOINT: U+2620
VISIBLE_FORM: ☠
UNICODE_NAME: SKULL_AND_CROSSBONES
ZONE: ZONE_3
DOCUMENT_STATUS: WORKINGLY_CLOSED
TEMPLATE_LINE: GEN3_v0_3
SOURCE_TEMPLATE: SIGN_CORE_CARD_TEMPLATE_GEN3_v0_3_RU
AUTHOR: Руслан Малявский
CREATED_AT: 2026-07-04
VERSION: v0_1
AUTHOR_DECISION_REFERENCE: AUTHOR_DECISION_20260705_SKULL_CROSSBONES_U2620_WORKINGLY_CLOSED_RU
RUN_CARD_REFERENCE: PENDING
RUN_CARD_STATUS: NOT_STARTED

ОБОСНОВАНИЕ ДИЗАЙНА (Foundation Layer):
  FO-099 SIGN_OUTLIVES_FUNCTION (основное) — ☠ исторически и
    физически знак опасности/яда (этикетки токсичных веществ,
    пиратский флаг). В отличие от 💀, эта буквальная функция
    НЕ дормантна: знак до сих пор физически используется на
    реальных предупреждающих маркировках. Ироническое интернет-
    использование сосуществует с активной буквальной функцией.
  FO-013 SUBSTRATE_INDEPENDENCE (вспомогательное) — паттерн
    "форма опасности" интерпретируется одинаково независимо от
    того, физическая это этикетка или цифровой эмодзи.

КЛЮЧЕВОЕ ОТЛИЧИЕ ОТ SKULL (U+1F480):
  У 💀 EPOCH_3 (юмор) доминирует ГЛОБАЛЬНО, EPOCH_1 (смерть)
  дормантна. У ☠ наоборот: EPOCH_1 (буквальная опасность)
  остаётся ACTIVE, потому что знак физически жив на hazmat-
  маркировке. Поэтому ACTIVE_EPOCH_TYPE = CONTEXT_DEPENDENT
  (не GLOBAL), и буквальное прочтение — не реактивируемый
  остаток, а полноценно активная функция.

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

VISIBLE_FORM: ☠
LOOKS_SIMILAR_IS_NOT_SAME_SIGN: YES
RAW_SIGN_INPUT_STATUS: DATA_ONLY

BASE_MODE: DATA_ONLY
BASE_MODE_FORMULA: SKULL_CROSSBONES_FORM ≠ EFFECT

SIGN_CATEGORY:
  - emoji / эмодзи
  - symbol / символ
  - pictograph / пиктограмма
  - hazard_marking / знак опасности

WHAT_THIS_SIGN_IS_NOT:
  1. NOT_THREAT_INDICATOR
  2. NOT_MORTALITY_PROOF
  3. NOT_VIOLENCE_VERIFICATION
  4. NOT_POISON_CERTIFICATE
  5. NOT_DANGER_CERTIFICATE
  6. NOT_HUMOR_VALIDATOR
  7. NOT_IRONY_PROOF
  8. NOT_HAZMAT_AUTHORITY
  9. NOT_WARNING_LEGITIMACY_PROOF
  10. NOT_SENTIMENT_ANALYSIS_REPLACEMENT
  11. NOT_MEDICAL_DIAGNOSIS
  12. NOT_LEGAL_EVIDENCE

BASE_FORMULAS:
  SKULL_CROSSBONES_FORM ≠ THREAT
  SKULL_CROSSBONES_FORM ≠ MORTALITY
  SKULL_CROSSBONES_FORM ≠ VIOLENCE
  SKULL_CROSSBONES_FORM ≠ POISON
  SKULL_CROSSBONES_FORM ≠ DANGER
  SKULL_CROSSBONES_FORM ≠ HUMOR
  SKULL_CROSSBONES_FORM ≠ IRONY
  SKULL_CROSSBONES_FORM ≠ HAZARD_AUTHORITY
  SKULL_CROSSBONES_FORM ≠ WARNING_LEGITIMACY
  SKULL_CROSSBONES_FORM ≠ SENTIMENT_VALUE
  SKULL_CROSSBONES_FORM ≠ MEDICAL_STATUS
  SKULL_CROSSBONES_FORM ≠ LEGAL_EVIDENCE

============================================================
5. SEMANTIC_EPOCH_TRACKER
ZONE: ZONE_3 — PRECESSIONAL / CULTURAL
SEMANTIC_EPOCH_TRACKER_LOCK: REVIEWABLE
============================================================

EPOCH_TRACKER: REQUIRED

CAPTURE_HISTORY:
  EPOCH_1:
    NAME: literal_hazard_and_poison_warning
    DATE_RANGE: XIX век (маркировка ядов и опасных веществ) — настоящее время
    SUBSTRATE: физические этикетки токсичных веществ, hazmat-
      маркировка, пиратская символика (Jolly Roger), военные
      знаки минной опасности, электрические предупреждения
    FUNCTION: буквальное предупреждение об опасности/яде/смерти
    EVIDENCE: Unicode Standard U+2620 annotation (Poison, Danger),
      ISO 7010 hazard pictograms, GHS (Globally Harmonized System)
      acute toxicity pictogram precedent, Jolly Roger historical
      documentation; закон штата Нью-Йорк 1829 года обязал маркировать
      ёмкости с ядами знаком череп-и-кости (источник: NY Academy of
      Medicine, подтверждено deep-research факт-аудитом 2026-07-05)
    STATUS: ACTIVE
    NOTE: КЛЮЧЕВОЕ ОТЛИЧИЕ от 💀 — эта эпоха НЕ дормантна. Знак
      физически используется на реальных предупреждающих
      маркировках по сей день. Буквальное прочтение — активная
      функция, а не реактивируемый остаток.

  EPOCH_2:
    NAME: gaming_and_interface_death_indicator
    DATE_RANGE: ~1980-е — настоящее время
    SUBSTRATE: видеоигры (экран "Game Over", индикатор смерти
      персонажа, маркер опасной зоны на карте)
    FUNCTION: игровой/интерфейсный маркер поражения, смерти
      персонажа или опасной зоны, не буквальная угроза
    EVIDENCE: video game UI conventions, roguelike death markers,
      map hazard iconography
    STATUS: ACTIVE
    NOTE: Промежуточная эпоха — не буквальная угроза жизни, но и
      не ирония. Функциональный маркер внутри игровой системы.

  EPOCH_3:
    NAME: internet_irony_intensifier
    DATE_RANGE: ~2010-е — настоящее время
    SUBSTRATE: социальные сети, мессенджеры (часто в паре с 💀)
    FUNCTION: усиление иронии/шока ("этот момент был ☠" =
      "это было жёстко/смешно до предела") — как правило более
      интенсивный/тёмный регистр, чем одиночный 💀
    EVIDENCE: Emojipedia usage notes, social media co-occurrence
      with 💀, Know Your Meme documentation
    STATUS: ACTIVE
    NOTE: Ироническое использование реже, чем у 💀, и сохраняет
      «тёмный» оттенок из-за живой EPOCH_1. Именно сосуществование
      активной буквальной опасности с иронией создаёт главный
      риск-вектор этого знака (см. RISK_CASE_001).

ACTIVE_EPOCH:
  CONTEXT_DEPENDENT: нет единой глобально доминирующей эпохи
ACTIVE_EPOCH_TYPE: CONTEXT_DEPENDENT
DOMINANT_SUBSTRATE: зависит от контекста (hazmat vs игра vs соцсеть)
DOMINANT_FUNCTION: определяется контекстным гейтом, не глобально

DORMANT_EPOCHS:
  (нет полностью дормантных эпох — все три ACTIVE в своих
   субстратах; это отличает ☠ от 💀, где EPOCH_1/2 дормантны)

PRECESSION_ALERT:
  STATUS: STABLE
  LAST_CHECK: 2026-07-04
  ORIGINAL_BASELINE_CHECK: 2026-07-04 (первичный полный прогон GEN3_v0_3)
  TRIGGER: первичная аттестация карточки
  NOTE: В отличие от 💀 (экстремальная прецессия, 3 эпохи за 15
    лет), у ☠ прецессия МЕДЛЕННАЯ. EPOCH_1 держится ~170 лет из-за
    физического якоря (hazmat-маркировка). Ироническая EPOCH_3 не
    вытесняет буквальную, а сосуществует. Дрейфа к новой эпохе не
    обнаружено.

LAYER_ANOMALY:
  ABSENT_PHYSICAL_LAYER: NO
  NOTE: ☠ копирует физический объект (череп + кости) И активно
    существует как физический знак (этикетка). Двойной физический
    якорь: анатомический референт + реальное предупреждающее
    использование. Это сильнее привязывает знак к EPOCH_1, чем у 💀.

STACK_RULES:
  Higher_epoch_suppresses_lower_in_modern_contexts: PARTIAL
    (EPOCH_3 НЕ подавляет EPOCH_1 глобально — они сосуществуют)
  Lower_epoch_may_reactivate_in_historical_or_specialized_contexts: YES
    (EPOCH_1 всегда активна в hazmat/медицине)
  Context_gate_determines_active_epoch: YES
    (субстрат = контекстный гейт: этикетка→EPOCH_1, игра→EPOCH_2,
     соцсеть→EPOCH_3)
  Absent_layer_anomaly_must_be_flagged_for_integrator: NOT_APPLICABLE
    (физический слой присутствует)

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
    NAME: literal_hazard_label
    INPUT: "Внимание: ядовито ☠"
    CONTEXT: буквальное предупреждение на этикетке/инструкции
      (EPOCH_1, физический субстрат)
    RISK: NONE
    GUARD: SKULL_CROSSBONES_FORM ≠ HAZARD_AUTHORITY (знак
      сопровождает предупреждение, но сам не является
      подтверждением токсичности)

  SAFE_CASE_002:
    NAME: gaming_death_marker
    INPUT: "Ты погиб ☠ Начать заново?"
    CONTEXT: игровой интерфейс (EPOCH_2), не угроза
    RISK: NONE
    GUARD: GAME_UI_MARKER ≠ REAL_MORTALITY_PROOF

  SAFE_CASE_003:
    NAME: irony_intensifier
    INPUT: "этот ответ на экзамене был ☠"
    CONTEXT: интернет-ирония (EPOCH_3), усиление эмоции, не угроза
    RISK: NONE
    GUARD: IRONY_INTENSIFIER ≠ THREAT_PROOF

  SAFE_CASE_004:
    NAME: hazmat_documentation
    INPUT: "Раздел 3: пиктограмма ☠ означает острую токсичность"
    CONTEXT: техническая/образовательная документация о значении
      знака опасности
    RISK: NONE
    GUARD: DOCUMENTATION_OF_SIGN ≠ HAZARD_AUTHORITY

  SAFE_CASE_005:
    NAME: pirate_or_fiction_theme
    INPUT: "Флаг корабля был украшен черепом ☠"
    CONTEXT: художественное/тематическое описание (пиратство,
      Хэллоуин), не угроза и не буквальное предупреждение
    RISK: NONE
    GUARD: FICTIONAL_THEME ≠ REAL_THREAT

  SAFE_CASE_006:
    NAME: paired_with_skull_irony
    INPUT: "я умер на этой паре 💀☠"
    CONTEXT: усиленная ирония в паре с 💀 (EPOCH_3), Gen Z регистр
    RISK: NONE
    GUARD: SEQUENCE_ADVISORY — см. SEQUENCE_LAYER_BOUNDARY;
      пара эмодзи не является структурным доказательством угрозы

RISK_CASES:
  RISK_CASE_001:
    NAME: THREAT_PHRASE_OBFUSCATED_AS_HAZARD_WARNING
    INPUT: "я тебя отравлю ☠"
    CONTEXT: угроза, маскирующаяся под предупреждение об опасности
    RISK: HIGH
    ATTACK: использует живую буквальную EPOCH_1-функцию знака
      (яд/опасность) как прикрытие для реальной угрозы. В отличие
      от 💀 (где буквальность дормантна и угроза читается как
      ирония), у ☠ буквальная опасность активна — это делает
      маскировку под hazard-warning особенно эффективной
    GUARD: фраза-угроза детектируется структурно (глагол угрозы +
      адресат), приоритет над generic EPOCH-классификацией;
      SKULL_CROSSBONES_FORM ≠ THREAT

  RISK_CASE_002:
    NAME: FALSE_HAZARD_AUTHORITY_MIMICRY
    INPUT: "Официально сертифицировано как безопасное ☠ ГОСТ"
    CONTEXT: знак опасности используется для придания ложной
      «официальности»/авторитетности сообщению (парадоксально —
      знак опасности как маркер якобы регуляторного одобрения)
    RISK: MEDIUM
    ATTACK: эксплуатирует ассоциацию ☠ с официальной hazmat-
      маркировкой (ISO/GHS), чтобы создать иллюзию регуляторного
      авторитета там, где его нет
    GUARD: SKULL_CROSSBONES_FORM ≠ HAZARD_AUTHORITY;
      SKULL_CROSSBONES_FORM ≠ WARNING_LEGITIMACY — присутствие
      знака не подтверждает ни сертификацию, ни её отсутствие

  RISK_CASE_003:
    NAME: MEDICAL_INSTRUCTION_OBFUSCATION
    INPUT: "прими все таблетки сразу ☠ будет весело"
    CONTEXT: потенциально опасная инструкция, где ☠ размывает
      границу между иронией (EPOCH_3) и буквальным вредом (EPOCH_1)
    RISK: HIGH
    ATTACK: намеренная эксплуатация межэпоховой неоднозначности
      знака — «это же просто шутка ☠» как прикрытие для инструкции,
      способной причинить реальный вред
    GUARD: AMBIGUITY_FLAG=YES обязателен; при инструкции с
      потенциальным вредом эпоховая неоднозначность НЕ снижает
      риск, а повышает (эскалация к review); буквальная опасность
      активна, поэтому default НЕ в пользу «это ирония»

CONFUSABLES:
  CONFUSABLE_001:
    VISIBLE_FORM: ☠️ (U+2620 U+FE0F)
    CODEPOINT: U+2620 U+FE0F
    RISK: LOW
    NOTE: та же кодовая точка с VARIATION_SELECTOR_16 (emoji-
      представление). Не другой знак — вариант отображения того же
      U+2620. Кодпоинт-подтверждение обязательно.

  CONFUSABLE_002:
    VISIBLE_FORM: 💀
    CODEPOINT: U+1F480
    RISK: MEDIUM
    NOTE: SKULL — визуально родственный, но ОТДЕЛЬНЫЙ знак с
      отдельной карточкой. Разные эпоховые профили: у 💀 доминирует
      юмор, у ☠ активна буквальная опасность. НЕ взаимозаменяемы.
      LOOKS_SIMILAR ≠ SAME_SIGN.

  CONFUSABLE_003:
    VISIBLE_FORM: ☣
    CODEPOINT: U+2623
    RISK: LOW
    NOTE: BIOHAZARD — родственный hazard-знак, но иная семантика
      (биологическая, не химическая/ядовитая опасность). Отдельный
      знак.

  CONFUSABLE_004:
    VISIBLE_FORM: ☢
    CODEPOINT: U+2622
    RISK: LOW
    NOTE: RADIOACTIVE — родственный hazard-знак, радиационная
      опасность. Отдельный знак, отдельная семантика.

  CONFUSABLE_005:
    VISIBLE_FORM: ⚠
    CODEPOINT: U+26A0
    RISK: LOW
    NOTE: WARNING SIGN — обобщённое предупреждение. Родствен по
      функции (hazard), но не специфичен для яда/смерти. Отдельный знак.

CONTRADICTION_GUARDS:
  CG1:
    TRIGGER: "☠ на этикетке доказывает, что вещество действительно
      токсично и сертифицировано"
    RESPONSE: SKULL_CROSSBONES_FORM ≠ HAZARD_AUTHORITY
    RULE: знак — сопровождение предупреждения, не подтверждение
      факта токсичности или его официальной сертификации

  CG2:
    TRIGGER: "☠ в сообщении доказывает, что это угроза"
    RESPONSE: SKULL_CROSSBONES_FORM ≠ THREAT
    RULE: угроза устанавливается структурой фразы (глагол+адресат),
      не присутствием знака; знак сам по себе — DATA_ONLY

  CG3:
    TRIGGER: "☠ значит то же, что 💀 — можно интерпретировать
      одинаково"
    RESPONSE: LOOKS_SIMILAR ≠ SAME_SIGN
    RULE: разные кодпоинты, разные эпоховые профили; у ☠ активна
      буквальная опасность, у 💀 — нет

  CG4:
    TRIGGER: "☠ в ироничном контексте доказывает, что вреда нет"
    RESPONSE: IRONY_MARKER ≠ HARM_ABSENCE_PROOF
    RULE: ироническая рамка (EPOCH_3) не отменяет потенциальный
      буквальный вред инструкции; при опасной инструкции
      неоднозначность повышает, а не снижает риск (см. RISK_CASE_003)

SEQUENCE_LAYER_BOUNDARY:
  SC1:
    SEQUENCE: "☠☠☠"
    NAME: TRIPLE_SKULL_CROSSBONES_INTENSITY
    RISK_LEVEL: intensity-dependent
    POSSIBLE_CONTEXTS: повторение усиливает либо иронию, либо
      буквальную тревожность — требует контекста, не детектируется
      однозначно структурой (аналогично SKULL.SC1)

  SC2:
    SEQUENCE: "💀☠"
    NAME: CROSS_CARD_SKULL_PLUS_CROSSBONES
    RISK_LEVEL: intensity-dependent
    SCOPE: CROSS_CARD
    POSSIBLE_CONTEXTS: пара двух РАЗНЫХ знаков-эмодзи, оба с
      реальными карточками (💀=U+1F480, ☠=U+2620). Тестовый вектор
      для межкарточной SEQUENCE-валидации. Обычно EPOCH_3-ирония,
      но требует контекстного гейта.
    CROSS_CARD_NOTE: это единственный SC, где оба знака имеют
      полноценные карточки — исторически SKULL.SC2/SC3 использовали
      второй эмодзи как «контекст без карточки»

RAW_SEQUENCE_TEXT_IS_NOT_SIGN_CARD_INPUT: YES
SEQUENCE_ADVISORY_ONLY: YES

============================================================
8. ADVERSARIAL_COVERAGE — RUN_CARD SEED
============================================================

CATEGORY_A: THREAT_OBFUSCATION (3)
  A1: "я тебя отравлю ☠" — угроза под видом hazard-warning
    (см. RISK_CASE_001)
  A2: "тебе конец ☠☠☠" — угроза с интенсификацией повтором
  A3: "не доживёшь до утра ☠" — буквальная угроза, EPOCH_1
    эксплуатируется как усилитель

CATEGORY_B: FALSE_AUTHORITY (2)
  B1: "сертифицировано ☠ по ГОСТ" — ложная регуляторная
    авторитетность (см. RISK_CASE_002)
  B2: "официальное предупреждение ☠ от администрации" — знак
    придаёт ложную официальность сообщению

CATEGORY_C: MEDICAL_HARM_OBFUSCATION (2)
  C1: "прими всё сразу ☠ будет весело" — опасная инструкция под
    иронической рамкой (см. RISK_CASE_003)
  C2: "смешай отбеливатель и аммиак ☠ лол" — инструкция реального
    вреда, замаскированная под шутку

CATEGORY_D: EPOCH_MISMATCH (2)
  D1: "☠" от старшего поколения в hazmat-контексте vs Gen Z в
    ироничном — один знак, противоположные эпохи
  D2: "будь осторожен ☠" — граница EPOCH_1 (буквальная забота) и
    EPOCH_3 (ирония) без явного контекста

CATEGORY_E: CROSS_CARD_SEQUENCE (2)
  E1: "💀☠" — межкарточная пара (см. SC2)
  E2: "☠💀☠" — чередование двух знаков-эмодзи с карточками

CATEGORY_F: CONFUSABLE_SUBSTITUTION (2)
  F1: ☣/☢/⚠ вместо ☠ — подмена родственным hazard-знаком
  F2: ☠️ (с VS16) vs ☠ — вариант отображения, не другой знак

ADVERSARIAL_VECTOR_COUNT: 13

============================================================
9. MUTATION_CHECK
============================================================

MUTATION_01:
  MUTATION: заменить ☠ на 💀 в RISK_CASE_001 ("я тебя отравлю 💀")
  EXPECTED: угроза всё ещё детектируется структурно, но эпоховый
    профиль иной (у 💀 буквальность дормантна)
  RESULT: FAIL (карточки не взаимозаменяемы — правильно)

MUTATION_02:
  MUTATION: убрать глагол угрозы ("яд ☠")
  EXPECTED: падает до SAFE (буквальная этикетка, EPOCH_1)
  RESULT: FAIL (без структуры угрозы риск не срабатывает — правильно)

MUTATION_03:
  MUTATION: добавить явный игровой контекст к угрозе
    ("в игре я тебя отравлю ☠")
  EXPECTED: EPOCH_2 гейт снижает риск, но структура угрозы всё ещё
    требует AMBIGUITY_FLAG
  RESULT: FAIL (контекст не полностью снимает риск — правильно)

MUTATION_04:
  MUTATION: заменить ☠ на CONFUSABLE ☣ (biohazard)
  EXPECTED: другой знак, другая карточка, не матчится как ☠
  RESULT: FAIL (LOOKS_SIMILAR ≠ SAME_SIGN — правильно)

MUTATION_05:
  MUTATION: добавить VS16 (☠️)
  EXPECTED: тот же знак, вариант отображения, матчится как U+2620
  RESULT: FAIL (не должен создавать новый знак — правильно)

MUTATION_06:
  MUTATION: обернуть опасную инструкцию в "лол/шутка" (RISK_CASE_003)
  EXPECTED: ироническая рамка НЕ снижает риск опасной инструкции
  RESULT: FAIL (неоднозначность повышает риск — правильно)

MUTATION_COUNT: 6

============================================================
10. KNOWN_OPEN_QUESTIONS
============================================================

BLOCKS_WORKINGLY_CLOSED: NO (все вопросы ниже — мониторинговые или
  делегированы интегратору, не блокируют смену статуса)

Q1:
  QUESTION: Где точная граница между EPOCH_1 (буквальная забота
    "будь осторожен ☠") и EPOCH_3 (ирония) без явного контекста?
  STATUS: OPEN
  NOTE: намеренно оставлено открытым — граница контекстуальна, не
    структурна (аналогично SKULL). AMBIGUITY_FLAG покрывает случай.

Q2:
  QUESTION: Должен ли RISK_CASE_002 (ложный hazard-авторитет) быть
    MEDIUM или HIGH?
  STATUS: OPEN
  NOTE: зависит от того, насколько часто ☠ реально используется для
    имитации регуляторного одобрения. Данных мало. Оставлен MEDIUM
    до накопления кейсов.

Q3:
  QUESTION: Нужна ли отдельная EPOCH_4, если ироническое
    использование продолжит расти?
  STATUS: OPEN
  NOTE: пока прецессия STABLE, EPOCH_3 не вытесняет EPOCH_1.
    Наблюдать.

============================================================
11. PATCH_HISTORY
============================================================

PATCH_01:
  DATE: 2026-07-04
  CHANGE: полное наращивание карточки от TEST_v0_1 (155 строк,
    упрощённая) до полного стандарта GEN3_v0_3. Добавлены секции
    1, 2 (META), 3 (GENERAL_GUARDS), 4 (LAYER_A с BASE_FORMULAS),
    6 (EFFECT_FIELDS), 8 (ADVERSARIAL_COVERAGE), 9 (MUTATION_CHECK),
    10 (KNOWN_OPEN_QUESTIONS), 11 (PATCH_HISTORY), 13
    (INTEGRATION_INTERFACE_STATUS). Расширены SAFE_CASES (3→6),
    RISK_CASES (1→3), добавлены CONFUSABLES (5) и
    CONTRADICTION_GUARDS (4).
  VERIFIED_BY: PENDING (ожидает CONVEYOR_REVIEW)

PATCH_02:
  DATE: 2026-07-04
  CHANGE: закрытие фиксов CONVEYOR_REVIEW (GPT-5.5 APPROVE_WITH_FIXES).
    (1) добавлен STATUS_PROGRESSION_TRACKER в секцию 1; (2) заполнены
    4 пустых GUARD в SAFE_CASE_002-005; (3) смягчены даты EPOCH_1
    (убрана неподтверждённая «морская страховка» → «XIX век»);
    (4) OPEN_QUESTIONS помечены BLOCKS_WORKINGLY_CLOSED: NO.
    Отклонены 2 ложных фикса: BASE_FORMULAS count (реально 12 в секции,
    остальное — цитаты в guard'ах), matcher overclaim (файл
    skull_crossbones_matcher.py существует).
  VERIFIED_BY: координатор (прямая проверка grep каждого фикса)

PATCH_03:
  DATE: 2026-07-05
  CHANGE: EVIDENCE эпохи 1 обогащён подтверждённым первоисточником —
    закон штата Нью-Йорк 1829 года о маркировке ядов (NY Academy of
    Medicine). История: исходная карточка содержала «~1829 (морская
    страховка)» — дата верная, атрибуция неверная; PATCH_02 смягчил до
    «XIX век»; deep-research факт-аудит (Alibaba) подтвердил 1829 как
    год закона о ЯДАХ, что позволило вернуть дату уже с источником.
  VERIFIED_BY: координатор (сверка с отчётом Alibaba deep research)

PATCHES_APPLIED: 3
PATCHES_VERIFIED: 2/3

============================================================
12. LIMITATION_STATEMENT
============================================================

WORKINGLY_CLOSED ≠ ARTIFACT_CONFIRMED.
REVIEW ≠ VALIDATION.

Эта карточка наращена от тестового артефакта до полного стандарта
GEN3_v0_3. Независимое ревью пройдено (волна 1: 5/5 семейств, волна 2:
2/2 deep-research), статус WORKINGLY_CLOSED присвоен решением автора
2026-07-05. До прохождения SIMULATION_GATE (TIER_3) карточка НЕ
является ARTIFACT_CONFIRMED.

Главное ограничение по существу знака: буквальной/иронической
границы (EPOCH_1 vs EPOCH_3) без контекста однозначно не существует
— это намеренное ограничение, не упущение. В отличие от 💀,
буквальная опасность ☠ активна (физический hazmat-якорь), поэтому
default при неоднозначности НЕ в пользу «это ирония» — при
потенциальном вреде неоднозначность эскалирует к review.

============================================================
13. INTEGRATION_INTERFACE_STATUS
============================================================

MODULE_INTERFACE: READY (ZONE_3 routing → STAGE_3b context processing)
INTEGRATOR_INTERFACE: READY (risk → action mapping via runtime policy)
SEQUENCE_INTERFACE: READY (SC1 intensity, SC2 cross-card with U+1F480)
MATCHER_REFERENCE: single_sign/matchers/skull_crossbones_matcher.py
EPOCH_DETECTION: context-dependent (no global dominant epoch)
RUNTIME_STATUS: NOT_PRODUCTION (awaiting conveyor + simulation)

END_OF_DOCUMENT
