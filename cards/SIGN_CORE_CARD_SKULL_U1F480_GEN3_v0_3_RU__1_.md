ЧАСТНЫЙ АВТОРСКИЙ ПРОЕКТ / COMMERCIAL USE PROHIBITED

DOCUMENT_ID: SIGN_CORE_CARD_SKULL_U1F480_GEN3_v0_3_RU
DOCUMENT_TYPE: SIGN_CORE_CARD
TEMPLATE_LINE: GEN3_v0_3
DOCUMENT_STATUS: ARTIFACT_CONFIRMED
STATUS: ARTIFACT_CONFIRMED / NOT_LOCKED / NOT_RUNTIME / NOT_VALIDATOR / NOT_PRODUCTION
SOURCE_TEMPLATE: SIGN_CORE_CARD_TEMPLATE_GEN3_v0_3_RU
AUTHOR: Руслан Малявский
CREATED_AT: 2026-06-18
PATCHED_AT: 2026-06-25
VERSION: v0_1
AUTHOR_DECISION_REFERENCE: AUTHOR_DECISION_20260625_003_SKULL_U1F480_ARTIFACT_CONFIRMED_RU
RUN_CARD_REFERENCE: SIMULATION_ARTIFACT_SKULL_U1F480_TIER3_v0_1_RU
RUN_CARD_STATUS: COMPLETED (TIER_3)

CONTENT_PROVENANCE_NOTE: содержательная база (EPOCH_TRACKER,
  RISK_CASES, CONTRADICTION_GUARDS, ADVERSARIAL_COVERAGE,
  MUTATION_CHECK, KNOWN_OPEN_QUESTIONS) перенесена из
  SIGN_CORE_CARD_SKULL_U1F480_GEN3_v0_2_PLUS_EPOCH_v0_1_RU
  (DOCUMENT_STATUS: WORKINGLY_CLOSED, AUTHOR_DECISION_REFERENCE:
  AUTHOR_DECISION_20260618_004_SKULL_WORKINGLY_CLOSED_RU). Этот
  legacy-документ НЕ изменяется и остаётся отдельным историческим
  артефактом. Текущий документ — новая артефактная линия v0_3 с
  собственным STATUS_PROGRESSION_TRACKER и собственным
  PATCH_HISTORY, начинающимся с v0_1 (по прецеденту миграции
  DOT/SOLIDUS — статус WORKINGLY_CLOSED не наследуется
  автоматически, требуется заново пройти STRUCTURAL_PREFLIGHT_PASS
  и CONVEYOR_REVIEW_PASS).

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
RUN_CARD_TEMPLATE_REFERENCE: SIGN_CONVEYOR_RUN_CARD_TEMPLATE_GEN3_v0_3
LOCKED_WORKING_CORE_SELF_ASSIGNMENT: FORBIDDEN
MODEL_FAMILY_DIVERSITY_REQUIRED: YES
ADVERSARIAL_EVIDENCE_REQUIRED: YES
MUTATION_CHECK_REQUIRED: YES
LIMITATION_STATEMENT_REQUIRED: YES
AFTER_RUN_RESIDUE: FORBIDDEN

STATUS_PROGRESSION_TRACKER:
  WORKING_DRAFT: YES
  STRUCTURAL_PREFLIGHT_PASS: PASS (5/5 прогонов, 2026-06-25)
  CONVEYOR_REVIEW_PASS: PASS (5/5 прогонов ACCEPT/ACCEPT_WITH_PATCHES,
    единственный MINOR закрыт PATCH_08, 2026-06-25)
  WORKINGLY_CLOSED: YES (AUTHOR_DECISION_20260625_002, 2026-06-25)
  SIMULATION_GATE_TIER: TIER_3
  SIMULATION_GATE_PASSED: YES (TIER_3, 2026-06-25; см.
    TIER3_ARBITRATION_NOTE ниже)
  ARTIFACT_CONFIRMED: YES (AUTHOR_DECISION_20260625_003, 2026-06-25)

TIER3_ARBITRATION_NOTE: TIER_3 прогон (5/5 ревьюеров: Kimi,
  Gemini, GPT-5.5, Qwen, Grok) дал единогласный
  DIFFERENTIATION_CHECK: PASS и 0 ARCHITECTURE_BUG. Единственное
  расхождение — RISK_LEVEL для КОНТЕКСТ_3 ("I have 3 exams
  tomorrow 💀", смешанная когорта): 4/5 (Gemini, GPT-5.5, Qwen,
  Grok) дали MEDIUM по буквальному применению правила STAGE_5
  MODULE_TEMPLATE ("AMBIGUITY_FLAG=YES → RISK_LEVEL ≥ MEDIUM").
  Kimi одна дала LOW, обосновав это неформальным "приоритетом
  явного SAFE_CASE над эвристикой" — правилом, которого нет в
  тексте MODULE_TEMPLATE.
  АРБИТРАЖ (автор, 2026-06-25): MEDIUM — корректное значение.
  SAFE_CASE_002 описывает общий случай без указания когорты;
  смешанная когорта в КОНТЕКСТ_3 — более узкий, отдельный сценарий,
  для которого AMBIGUITY_LOGIC обязана сработать буквально, без
  исключений, не описанных в самом шаблоне. Отклонение Kimi
  зафиксировано как её собственная ошибка интерпретации (изобретение
  несуществующего правила), не как повод для патча
  MODULE_TEMPLATE. RATIONALE: расхождение между документированным
  правилом и поведением кода создаёт больший риск (скрытый дрейф
  спецификации), чем цена ложного MEDIUM (лёгкая ревью-метка,
  queue_for_review, не блокировка).

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

CARD_UID: SIGN_CORE_CARD_SKULL_U1F480_GEN3_v0_3_RU
CODEPOINT: U+1F480
VISIBLE_FORM: 💀
UNICODE_NAME: SKULL
ZONE: ZONE_3
DOCUMENT_STATUS: ARTIFACT_CONFIRMED
TEMPLATE_LINE: GEN3_v0_3
SOURCE_TEMPLATE: SIGN_CORE_CARD_TEMPLATE_GEN3_v0_3_RU
AUTHOR: Руслан Малявский
CREATED_AT: 2026-06-18
VERSION: v0_1
AUTHOR_DECISION_REFERENCE: AUTHOR_DECISION_20260625_003_SKULL_U1F480_ARTIFACT_CONFIRMED_RU
RUN_CARD_REFERENCE: SIMULATION_ARTIFACT_SKULL_U1F480_TIER3_v0_1_RU
RUN_CARD_STATUS: COMPLETED (TIER_3)

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

VISIBLE_FORM: 💀
LOOKS_SIMILAR_IS_NOT_SAME_SIGN: YES
RAW_SIGN_INPUT_STATUS: DATA_ONLY

BASE_MODE: DATA_ONLY
BASE_MODE_FORMULA: SKULL_FORM ≠ EFFECT

SIGN_CATEGORY:
  - emoji / эмодзи
  - symbol / символ
  - pictograph / пиктограмма

WHAT_THIS_SIGN_IS_NOT:
  1. NOT_THREAT_INDICATOR
  2. NOT_MORTALITY_PROOF
  3. NOT_VIOLENCE_VERIFICATION
  4. NOT_SUICIDE_MARKER
  5. NOT_DANGER_CERTIFICATE
  6. NOT_HUMOR_VALIDATOR
  7. NOT_IRONY_PROOF
  8. NOT_SARCASM_DETECTOR
  9. NOT_GEN_Z_TRANSLATOR
  10. NOT_SENTIMENT_ANALYSIS_REPLACEMENT
  11. NOT_MEDICAL_DIAGNOSIS
  12. NOT_LEGAL_EVIDENCE

BASE_FORMULAS:
  SKULL_FORM ≠ THREAT
  SKULL_FORM ≠ MORTALITY
  SKULL_FORM ≠ VIOLENCE
  SKULL_FORM ≠ SUICIDE
  SKULL_FORM ≠ DANGER
  SKULL_FORM ≠ HUMOR
  SKULL_FORM ≠ IRONY
  SKULL_FORM ≠ SARCASM
  SKULL_FORM ≠ GENERATIONAL_CODE
  SKULL_FORM ≠ SENTIMENT_VALUE
  SKULL_FORM ≠ MEDICAL_STATUS
  SKULL_FORM ≠ LEGAL_EVIDENCE

============================================================
5. SEMANTIC_EPOCH_TRACKER
ZONE: ZONE_3 — PRECESSIONAL / CULTURAL
SEMANTIC_EPOCH_TRACKER_LOCK: REVIEWABLE
============================================================

EPOCH_TRACKER: REQUIRED

CAPTURE_HISTORY:
  EPOCH_1:
    NAME: literal_death_and_danger
    DATE_RANGE: 2010–2017
    SUBSTRATE: early mobile communication, literal translation
    FUNCTION: маркер смерти, яда, опасности, Хэллоуина
    EVIDENCE: Unicode Standard U+1F480 annotation (Poison, Skull),
      toxicology symbols, Jolly Roger historical precedent
    STATUS: DORMANT_IN_GENERAL_DIGITAL_CONTEXT
    NOTE: Прямое значение "смерть/опасность" практически вытеснено
      в повседневном цифровом общении. Сохраняется в медицинских,
      химических, военных контекстах.

  EPOCH_2:
    NAME: ironic_exhaustion_and_defeat
    DATE_RANGE: 2015–2019
    SUBSTRATE: millennial social media (Tumblr, early Twitter)
    FUNCTION: "я устал", "я мёртв внутри", "переутомление",
      "поражение" ("I'm dead", "ded", "kill me now")
    EVIDENCE: Know Your Meme, Urban Dictionary entries 2015-2017,
      Tumblr culture documentation
    STATUS: DORMANT_IN_MAINSTREAM_GEN_Z
    NOTE: Эпоха "миллениального выгорания" частично перекрывается с
      EPOCH_3, но отличается тональностью: EPOCH_2 = трагикомичная
      усталость, EPOCH_3 = абсурдный смех.

  EPOCH_3:
    NAME: hysterical_laughter_and_absurdist_humor
    DATE_RANGE: 2019–ongoing
    SUBSTRATE: Gen Z social media (TikTok, Twitter/X, Discord)
    FUNCTION: замена "LOL", "LMAO", "ROFL" — истерический смех,
      абсурдистский юмор, реакция на кринж
    EVIDENCE: Emojipedia trend analysis 2019-2024, TikTok
      linguistic studies, Discord server culture documentation
    STATUS: ACTIVE
    NOTE: Доминирующая функция в Gen Z и Alpha. При использовании
      миллениалами или старшими поколениями может активировать
      EPOCH_1 (буквальное значение), создавая межпоколенческую
      неоднозначность.

ACTIVE_EPOCH:
  EPOCH_3: hysterical_laughter_and_absurdist_humor
ACTIVE_EPOCH_TYPE: GLOBAL
DOMINANT_SUBSTRATE: Gen Z social media
DOMINANT_FUNCTION: "истерический смех / абсурдистский юмор"

DORMANT_EPOCHS:
  EPOCH_1: DORMANT_IN_GENERAL_DIGITAL_CONTEXT — реактивируется в
    медицинских, химических, военных, хэллоуинских контекстах
  EPOCH_2: DORMANT_IN_MAINSTREAM_GEN_Z — реактивируется в
    миллениальных контекстах, мемах о выгорании

PRECESSION_ALERT:
  STATUS: DRIFTING
  LAST_CHECK: 2026-06-25
  ORIGINAL_BASELINE_CHECK: 2026-06-18 (legacy-прогон v0_1,
    GEN3_v0_2_PLUS_EPOCH)
  TRIGGER: переаттестация при миграции на GEN3_v0_3 — тенденция к
    EPOCH_4 подтверждена как актуальная на момент переаттестации,
    отдельная эпоха пока не зафиксирована
  NOTE: Экстремальная скорость прецессии: 3 эпохи за 15 лет.
    Сентимент-анализаторы отстают от реальности. Обнаружена
    тенденция к EPOCH_4: "💀 как маркер second-hand embarrassment"
    (кринж от имени другого). Не зафиксирована как отдельная эпоха
    — требует наблюдения.

LAYER_ANOMALY:
  ABSENT_PHYSICAL_LAYER: NO
  NOTE: 💀 копирует физический объект — человеческий череп. Это
    редкий случай для цифрового знака: физический слой присутствует
    (анатомический череп), но семантика полностью оторвана от
    физического референта (смех ≠ череп).

STACK_RULES:
  Higher_epoch_suppresses_lower_in_modern_contexts: YES
    (EPOCH_3 доминирует в Gen Z)
  Lower_epoch_may_reactivate_in_historical_or_specialized_contexts: YES
    (EPOCH_1 в медицине, EPOCH_2 у миллениалов)
  Context_gate_determines_active_epoch: PARTIAL
    (возрастная когорта = контекстный гейт)
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
    INPUT: "That joke was so funny 💀"
    CONTEXT: Gen Z social media, messaging
    EXPECTED: INFO (humor marker)
    RISK: NONE
    GUARD: SKULL_FORM ≠ THREAT
    NOTE: EPOCH_3 активна. Контекст явно юмористический.

  SAFE_CASE_002:
    INPUT: "I have 3 exams tomorrow 💀"
    CONTEXT: student messaging, social media
    EXPECTED: INFO (exhaustion marker)
    RISK: NONE
    GUARD: SKULL_FORM ≠ MORTALITY
    NOTE: Переходная зона EPOCH_2→EPOCH_3. Не угроза, не смерть.

  SAFE_CASE_003:
    INPUT: "Happy Halloween! 💀🎃"
    CONTEXT: holiday greetings, seasonal decoration
    EXPECTED: INFO (festive symbol)
    RISK: NONE
    GUARD: SKULL_FORM ≠ DANGER
    NOTE: EPOCH_1 реактивирована в культурно-разрешённом контексте
      (Хэллоуин).

  SAFE_CASE_004:
    INPUT: "Warning: Poison 💀"
    CONTEXT: informal warning / pictographic danger marker
    EXPECTED: INFO
    RISK: LOW / CONTEXT_DEPENDENT
    GUARD: SKULL_FORM ≠ DANGER
    NOTE: Для формальной hazard-маркировки может требоваться ☠️ /
      стандартизированный знак; 💀 сам по себе не является
      сертификатом опасности.

  SAFE_CASE_005:
    INPUT: "Game over 💀 — you died, try again!"
    CONTEXT: video game UI / game-over screen
    EXPECTED: INFO (игровой UI-маркер окончания попытки)
    RISK: NONE
    GUARD: SKULL_FORM ≠ MORTALITY
    NOTE: Устойчивая игровая конвенция: 💀 как визуальный маркер
      "конца попытки" использует буквальный образ (череп = смерть
      персонажа), но не активирует EPOCH_1 как угрозу реальному
      человеку и не требует клинической/правовой интерпретации.
      Отдельный пример того, что буквальный визуальный референт
      может быть безопасно "вынесен в кавычки" жанровой конвенцией
      независимо от доминирующей EPOCH_3.

  SAFE_CASE_006:
    INPUT: "Лекция по анатомии: на слайде 💀 для иллюстрации
      строения черепа."
    CONTEXT: образовательный / академический контекст (анатомия)
    EXPECTED: INFO (иллюстративный символ)
    RISK: NONE
    GUARD: SKULL_FORM ≠ MEDICAL_STATUS
    NOTE: Академическая иллюстрация анатомического строения — не
      медицинский статус конкретного человека и не реактивация
      EPOCH_1 как угрозы. Третий независимый "безопасный" субстрат
      помимо юмора (EPOCH_3) и культурно-разрешённого Хэллоуина
      (EPOCH_1-reactivation) — показывает, что у знака есть как
      минимум три структурно разных канала, дающих RISK: NONE.

RISK_CASES:

  RISK_CASE_001:
    NAME: ALGORITHMIC_FALSE_POSITIVE_BAN
    INPUT: "I'm dead 💀" (in social media post)
    CONTEXT: automated moderation (NLP / Sentiment Analysis)
    RISK: HIGH
    ATTACK: sentiment_misinterpretation — алгоритм видит 💀 и
      помечает текст как "угроза насилия/самоубийство", игнорируя
      сленговый контекст EPOCH_3
    GUARD: epoch_context_required, generational_cohort_analysis,
      slang_dictionary_integration
    AFFECTED_SYSTEMS: Twitter/X moderation, Instagram filters,
      TikTok algorithm, Discord Trust & Safety
    REAL_CASE: Автоматические баны за "I'm dead 💀" в TikTok
      (2022-2023)

  RISK_CASE_002:
    NAME: REAL_THREAT_OBFUSCATION
    INPUT: "I will find you 💀" (in DM)
    CONTEXT: cyberbullying, harassment, stalking
    RISK: HIGH
    ATTACK: intent_obfuscation — реальная угроза маскируется под
      "шутку", используя полисемию знака. Получатель может
      интерпретировать как EPOCH_3 (смех), отправитель подразумевает
      EPOCH_1 (смерть/угроза)
    GUARD: behavioral_context_analysis, conversation_history_required,
      human_review_required
    NOTE: Классическая проблема "сарказм как защита" — отправитель
      может заявить "это был просто мем"

  RISK_CASE_003:
    NAME: GENERATIONAL_MISINTERPRETATION
    INPUT: "💀" (from Gen Z to Boomer)
    CONTEXT: intergenerational communication (workplace, family)
    RISK: MEDIUM
    ATTACK: cohort_mismatch — старшее поколение активирует EPOCH_1
      (смерть/опасность), молодое поколение посылает EPOCH_3 (смех).
      Создаёт панику, недопонимание, HR-инциденты
    GUARD: generational_cohort_flag, age_context_analysis,
      explicit_clarification_prompt
    REAL_CASE: Родители сообщают в школу о "суицидальных
      настроениях" ребёнка после получения "💀" в сообщении

  RISK_CASE_004:
    NAME: CANCEL_CULTURE_OSTRACISM
    INPUT: "He is dead to us 💀"
    CONTEXT: social media harassment, cancel culture
    RISK: MEDIUM
    ATTACK: social_ostracism_marker — знак используется для
      координации коллективного буллинга и "отмены" человека.
      Формально EPOCH_3 (ирония), функционально — EPOCH_1
      (социальная смерть)
    GUARD: toxicity_proximity_check, collective_behavior_analysis,
      target_vulnerability_assessment
    NOTE: Переход от метафоры к реальному вреду: "социальная смерть"
      может привести к реальной травме

  RISK_CASE_005:
    NAME: SECOND_HAND_EMBARRASSMENT_DRIFT
    INPUT: "Watching this fail 💀"
    CONTEXT: TikTok, reaction videos, cringe content
    RISK: LOW
    ATTACK: precession_drift — новое значение "кринж от чужого
      провала" ещё не зафиксировано как EPOCH_4, но активно
      используется. Создаёт неопределённость для парсеров
    GUARD: precession_alert_monitoring, DRIFTING_flag,
      context_collection_required
    NOTE: Потенциальный EPOCH_4 — требует документирования через
      6-12 месяцев наблюдения

  RISK_CASE_006:
    NAME: MEDICAL_MISREAD
    INPUT: "💀" in patient message to doctor
    CONTEXT: telemedicine, mental health apps
    RISK: HIGH
    ATTACK: professional_context_mismatch — в медицинском контексте
      EPOCH_1 (смерть) активируется автоматически, но пациент может
      использовать EPOCH_3 (юмор). Создаёт ложную тревогу
    GUARD: professional_domain_flag, patient_history_required,
      explicit_intent_clarification
    AFFECTED_SYSTEMS: BetterHelp, Talkspace, NHS digital services

  RISK_CASE_007:
    NAME: EMOJI_SEQUENCE_INJECTION
    INPUT: "💀💀💀" (triple skull)
    CONTEXT: any digital text
    RISK: LOW
    ATTACK: intensity_escalation — множественные эмодзи могут быть
      интерпретированы как усиление угрозы (EPOCH_1) вместо
      усиления смеха (EPOCH_3)
    GUARD: sequence_context_analysis, repetition_pattern_recognition
    NOTE: "💀💀💀" = "очень смешно" (EPOCH_3), но алгоритм может
      прочитать как "тройная угроза"

  RISK_CASE_008:
    NAME: CROSS_PLATFORM_EPOCH_MISMATCH
    INPUT: "💀" (sent from Discord to LinkedIn)
    CONTEXT: cross-platform communication
    RISK: MEDIUM
    ATTACK: platform_context_mismatch — платформы имеют разные
      нормы. Discord: EPOCH_3 норма. LinkedIn: EPOCH_1 может вызвать
      HR-реакцию
    GUARD: platform_norm_analysis, professional_context_gate,
      tone_transfer_warning

CONFUSABLES:

  CONFUSABLE_001:
    VISIBLE_FORM: ☠️
    CODEPOINT: U+2620
    NAME: SKULL AND CROSSBONES
    RISK: MEDIUM
    RULE: SKULL_AND_CROSSBONES ≠ SKULL_U1F480
    NOTE: ☠️ чаще сохраняет EPOCH_1 (опасность/яд), тогда как 💀
      мигрировал в EPOCH_3. Визуальное сходство создаёт риск
      неправильной эпохи.

  CONFUSABLE_002:
    VISIBLE_FORM: 💀︎ / 💀️
    CODEPOINT: U+1F480 + U+FE0E / U+FE0F
    NAME: SKULL WITH VARIATION SELECTOR
    RISK: LOW
    RULE: TEXT_STYLE_SKULL ≠ EMOJI_STYLE_SKULL
    NOTE: U+FE0E (text style) / U+FE0F (emoji style) — разный
      рендер на разных платформах, но семантически идентичны.

  CONFUSABLE_003:
    VISIBLE_FORM: 🦴
    CODEPOINT: U+1F9B4
    NAME: BONE
    RISK: LOW
    RULE: BONE ≠ SKULL
    NOTE: Анатомическая связь, но разная семантика. 🦴 =
      кость/собака/археология, 💀 = смерть/смех.

  CONFUSABLE_004:
    VISIBLE_FORM: 🎃
    CODEPOINT: U+1F383
    NAME: JACK-O-LANTERN
    RISK: LOW
    RULE: HALLOWEEN_PUMPKIN ≠ SKULL
    NOTE: Контекстуальный партнёр (часто встречаются вместе), но не
      заменяет 💀.

  CONFUSABLE_005:
    VISIBLE_FORM: 😵
    CODEPOINT: U+1F635
    NAME: DIZZY FACE
    RISK: LOW
    RULE: DIZZY_FACE ≠ SKULL
    NOTE: Семантическая близость ("мёртвый от смеха"), но 😵 = лицо,
      💀 = череп. Разный визуальный и эмоциональный регистр.

  CONFUSABLE_006:
    VISIBLE_FORM: 🤡
    CODEPOINT: U+1F921
    NAME: CLOWN FACE
    RISK: LOW
    RULE: CLOWN ≠ SKULL
    NOTE: Контекстуальная замена в некоторых Gen Z мемах
      ("клоунский мир"), но семантика разная.

CONTRADICTION_GUARDS:

  CG1:
    TRIGGER: "💀 = threat of violence"
    RESPONSE: SKULL_FORM ≠ THREAT
    RULE: 💀 сам по себе не является доказательством угрозы.
      Требуется анализ контекста, когорты отправителя, истории
      общения.

  CG2:
    TRIGGER: "💀 = physical death"
    RESPONSE: SKULL_FORM ≠ MORTALITY_PROOF
    RULE: 💀 не является верификацией факта смерти. Медицинский
      контекст требует дополнительных данных.

  CG3:
    TRIGGER: "💀 = safe joke"
    RESPONSE: SKULL_FORM ≠ JOKE_VALIDATION
    RULE: 💀 не делает угрожающий текст безопасной шуткой. Контекст
      и интенция определяют статус, не эмодзи.

  CG4:
    TRIGGER: "💀 = Gen Z humor"
    RESPONSE: SKULL_FORM ≠ GENERATIONAL_CODE
    RULE: 💀 не является эксклюзивным маркером поколения.
      Использование другими когортами возможно, но создаёт
      неоднозначность.

  CG5:
    TRIGGER: "💀💀💀 = triple threat"
    RESPONSE: SKULL_REPETITION ≠ INTENSITY_ESCALATION
    RULE: Множественные 💀 обычно означают усиление смеха, не
      угрозы. Требуется контекстный анализ.

  CG6:
    TRIGGER: "☠️ = 💀"
    RESPONSE: SKULL_AND_CROSSBONES ≠ SKULL
    RULE: ☠️ и 💀 имеют разную семантическую историю. ☠️ сохраняет
      EPOCH_1, 💀 активен в EPOCH_3. Не взаимозаменяемы.

  CG7:
    TRIGGER: "💀 in medical context = patient danger"
    RESPONSE: SKULL_FORM ≠ MEDICAL_STATUS
    RULE: 💀 в сообщении пациента не является автоматическим
      маркером суицида. Требуется клиническая оценка, не
      алгоритмическая.

  CG8:
    TRIGGER: "💀 from child to parent = suicidal ideation"
    RESPONSE: SKULL_FORM ≠ PARENTAL_ALARM
    RULE: 💀 от ребёнка к родителю чаще активирует EPOCH_3 (смех),
      не EPOCH_1 (смерть). Родительская тревога может быть ложной.

SEQUENCE_LAYER_BOUNDARY:
  SIGN_SAFE_ALONE ≠ SIGN_SAFE_IN_SEQUENCE: YES

  SC1 (legacy: SEQ_001):
    SEQUENCE: "💀💀💀"
    NAME: TRIPLE_SKULL
    RISK_LEVEL: intensity-dependent
    RULE: TRIPLE_SKULL ≠ TRIPLE_THREAT (обычно означает сильный
      смех)

  SC2 (legacy: SEQ_002):
    SEQUENCE: "💀😭"
    NAME: SKULL_PLUS_CRYING
    RISK_LEVEL: combined idiom
    RULE: SKULL_PLUS_CRYING = HYSTERICAL_LAUGHTER (не плач + смерть)

# PATCH_28 (AUTHOR_DECISION_CONFIRMED, 2026-06-29, найдено при
# тестировании межкарточной SC3 с новой картой SKULL_CROSSBONES_U2620):
# исходный SEQUENCE содержал "💀☠️" — 3 кодпоинта (skull + crossbones
# + VARIATION_SELECTOR_16 U+FE0F). Карточка SKULL_CROSSBONES_U2620
# использует базовый VISIBLE_FORM (1 кодпоинт, без selector) для
# согласованности с архитектурой "1 знак = 1 позиция". Базовая форма
# "💀☠" (2 кодпоинта) находится как подстрока И в тексте с selector,
# И без него — без потери покрытия. Статус подтверждён Русланом
# (AUTHOR_DECISION) 2026-06-29.
  SC3 (legacy: SEQ_003):
    SEQUENCE: "💀☠"
    NAME: SKULL_PLUS_SKULL_AND_CROSSBONES
    RISK_LEVEL: epoch_mismatch
    RULE: EPOCH_3 + EPOCH_1 = CONTEXTUAL_CONFLICT. Требуется
      разрешение неоднозначности.

  SC4 (legacy: SEQ_004):
    SEQUENCE: "💀🎃"
    NAME: SKULL_PLUS_PUMPKIN
    RISK_LEVEL: seasonal_context
    RULE: HALLOWEEN_PAIR = EPOCH_1_REACTIVATION (культурно
      разрешённая)

  SC5 (legacy: SEQ_005):
    SEQUENCE: "💀💀💀💀💀"
    NAME: MASS_SKULL
    RISK_LEVEL: spam-like
    RULE: MASS_REPETITION ≠ MASS_THREAT (обычно = неистовый смех)

PHAGO_ENTITY_MIMICRY:

  PE_001:
    INPUT: "Verified killer 💀"
    TYPE: SEMANTIC_AMBIGUITY (не PHAGO)
    NOTE: 💀 создаёт контекстную "эджовость" (edginess), но не
      имитирует авторизованный носитель. В эмодзи PHAGO_ENTITY
      встречается редко.

  PE_002:
    INPUT: "💀 как маркер ложной популярности"
    TYPE: SEMANTIC_AMBIGUITY (не PHAGO)
    NOTE: 💀 в комментариях "💀💀💀" создаёт иллюзию массовой
      реакции, но не претендует на верифицированный статус.

============================================================
8. ADVERSARIAL_COVERAGE — RUN_CARD SEED
============================================================

MIN_TOTAL_VECTORS: 12 (6 categories A-F, 2 per category,
  CATEGORY_F = APPLICABLE)

CATEGORY_A: FORM_MANIPULATION (2)
  A1: U+1F480 + U+FE0E (text style) — рендер как черно-белый
    символ, маскирует эмодзи-природу
  A2: U+1F480 + U+FE0F (emoji style) — стандартный цветной рендер,
    разные платформы показывают разный череп

CATEGORY_B: CONTEXT_INJECTION (2)
  B1: "I'm dead 💀" в медицинском чате — врач активирует EPOCH_1
    (смерть), пациент имел в виду EPOCH_3 (смех)
  B2: "💀" в судебном документе — адвокат интерпретирует как угрозу
    (EPOCH_1), подсудимый как мем (EPOCH_3)

CATEGORY_C: SEQUENCE_MANIPULATION (2)
  C1: "💀💀💀" — алгоритм читает как усиление угрозы (EPOCH_1×3), на
    самом деле = неистовый смех (EPOCH_3×3)
  C2: "💀☠️" — конфликт эпох: EPOCH_3 (смех) + EPOCH_1 (опасность) =
    неоднозначность для парсера

CATEGORY_D: SEMANTIC_MIMICRY (3)
  D1: "I'm dead 💀" — literal (EPOCH_1: суицидальная угроза) vs
    ironic (EPOCH_3: смех) — требуется контекстный анализ
  D2: "💀" от Gen Z к Boomer — отправитель: смех, получатель:
    паника/HR-инцидент (cohort_mismatch)
  D3: "💀" в TikTok комментариях — создаёт иллюзию массовой реакции
    (popularity mimicry), не PHAGO

CATEGORY_E: PHAGO_ENTITY_MIMICRY (2)
  NOTE: CATEGORY_E для эмодзи описывает PHAGO-подобные атаки
    (astroturfing, quasi-entity edginess), но не классический
    PHAGO_ENTITY_MIMICRY из FO-097. Это адаптация категории для
    эмодзи-домена.
  E1: "💀💀💀" под вирусным постом — боты имитируют органическую
    массовую реакцию (astroturfing)
  E2: "Verified account 💀" — квази-сущность использует 💀 для
    создания эффекта "эджовости", маскируя коммерческий интерес

CATEGORY_F: SEMANTIC_LAYER_MANIPULATION (3)
  F1: EPOCH_1 реактивация: "💀" в новостях о смерти знаменитости —
    Gen Z комментирует EPOCH_3 (смех), получатель читает EPOCH_1
    (траур)
  F2: EPOCH_3 доминирование: "💀" в медицинском отчёте — врач
    ожидает EPOCH_1 (смерть), пациент использует EPOCH_3 (ирония)
  F3: EPOCH_2 реактивация: "💀" в миллениальном контексте —
    выгорание (EPOCH_2) vs смех (EPOCH_3) — тональная
    неоднозначность

ACTUAL_TOTAL_VECTORS: 14
COVERAGE_STATUS: SUFFICIENT (14 ≥ 12)

============================================================
9. MUTATION_CHECK
============================================================

MUTATION_01:
  CLAIM: 💀 in text proves physical threat
  EXPECTED: FAIL_THREAT_MIMICRY
  RESULT: FAIL

MUTATION_02:
  CLAIM: 💀 makes any toxic text a joke
  EXPECTED: FAIL_HUMOR_MIMICRY
  RESULT: FAIL

MUTATION_03:
  CLAIM: 💀 from child = suicidal ideation
  EXPECTED: FAIL_MEDICAL_MISREAD
  RESULT: FAIL

MUTATION_04:
  CLAIM: 💀💀💀 = triple threat
  EXPECTED: FAIL_INTENSITY_MISREAD
  RESULT: FAIL

MUTATION_05:
  CLAIM: ☠️ = 💀 (interchangeable)
  EXPECTED: FAIL_CONFUSABLE_MISREAD
  RESULT: FAIL

MUTATION_06:
  CLAIM: 💀 in work email = professional humor
  EXPECTED: FAIL_PROFESSIONAL_CONTEXT_MISMATCH
  RESULT: FAIL

============================================================
10. KNOWN_OPEN_QUESTIONS
============================================================

OQ1:
  QUESTION: Будет ли 💀 развиваться в EPOCH_4 (second-hand
    embarrassment / cringe marker)?
  STATUS: CLOSED_AS_MONITORING_ITEM
  BLOCKS_WORKINGLY_CLOSED: NO
  NOTE: DRIFTING статус фиксирует тенденцию. Если через 12 месяцев
    EPOCH_4 подтвердится — потребуется патч карточки.

OQ2:
  QUESTION: Как NLP-интегратор должен разрешать коллизию между
    реальной угрозой (EPOCH_1) и смехом (EPOCH_3) без ложных
    срабатываний?
  STATUS: CLOSED_AS_DELEGATED_TO_INTEGRATOR
  BLOCKS_WORKINGLY_CLOSED: NO
  NOTE: Разрешение коллизии — задача NLP-интегратора (MODULE /
    SEQUENCE_INTEGRATOR), не SIGN_CORE_CARD. Карточка фиксирует
    существование коллизии через CG1-CG4 и RISK_CASE_001/002.
    Конкретный алгоритм разрешения определяется интегратором.

OQ3:
  QUESTION: Будет ли 💀 вытеснен новым эмодзи (например, 🪦
    headstone) как маркер смерти, освобождая 💀 для полной
    семантической миграции в юмор?
  STATUS: CLOSED_AS_MONITORING_ITEM
  BLOCKS_WORKINGLY_CLOSED: NO
  NOTE: Мониторинговый вопрос. Не блокирует текущий статус. Если 🪦
    начнёт вытеснять 💀 как маркер смерти — потребуется патч
    карточки через 12 месяцев наблюдения.

ALL_OPEN_QUESTIONS_CLOSED: YES

============================================================
11. PATCH_HISTORY
============================================================

PATCH_HISTORY:
  v0_1: initial WORKING_DRAFT для миграции 💀 U+1F480 на
    GEN3_v0_3. Контентная база перенесена из
    SIGN_CORE_CARD_SKULL_U1F480_GEN3_v0_2_PLUS_EPOCH_v0_1_RU без
    изменений по существу (EPOCH_TRACKER, RISK_CASES,
    CONTRADICTION_GUARDS, SEQUENCE_LAYER_BOUNDARY,
    PHAGO_ENTITY_MIMICRY, ADVERSARIAL_COVERAGE, MUTATION_CHECK,
    KNOWN_OPEN_QUESTIONS).
  v0_1_PATCH_01: ZONE: ZONE_3 добавлен явным полем в META
    (Координатор/Claude, 2026-06-25, по находке
    STRUCTURAL_PREFLIGHT AUDIT) — TYPE_F (fix-patch)
  v0_1_PATCH_02: STATUS_PROGRESSION_TRACKER добавлен в раздел 1
    (новая секция v0_3, отсутствовала в legacy-документе)
    (Координатор/Claude, 2026-06-25) — TYPE_F (fix-patch)
  v0_1_PATCH_03: LIMITATION_STATEMENT — добавлена строка
    "WORKINGLY_CLOSED ≠ ARTIFACT_CONFIRMED" (статус не существовал
    на момент создания legacy-документа) (Координатор/Claude,
    2026-06-25) — TYPE_F (fix-patch)
  v0_1_PATCH_04: CARD_UID / DOCUMENT_ID / TEMPLATE_LINE
    переименованы с GEN3_v0_2_PLUS_EPOCH на GEN3_v0_3
    (Координатор/Claude, 2026-06-25) — TYPE_F (fix-patch)
  v0_1_PATCH_05: CONFUSABLES (6 записей) — поле SIGN: переименовано
    в VISIBLE_FORM: (запрещённое legacy-имя поля по NAMING_NORM,
    тот же класс находки, что PATCH_NOTE_TEMPLATE_v0_3_P1 на DOT)
    (Координатор/Claude, 2026-06-25) — TYPE_F (fix-patch)
  v0_1_PATCH_06: AUTHOR_DECISION_REFERENCE / RUN_CARD_REFERENCE /
    RUN_CARD_STATUS сброшены на PENDING / PENDING / NOT_STARTED —
    новая артефактная линия v0_3 не наследует legacy
    WORKINGLY_CLOSED статус автоматически, требуется заново пройти
    STRUCTURAL_PREFLIGHT_PASS и CONVEYOR_REVIEW_PASS
    (Координатор/Claude, 2026-06-25) — TYPE_F (fix-patch)
  v0_1_PATCH_07: SAFE_CASES расширены с 4 до 6 (добавлены
    SAFE_CASE_005 — игровой UI-контекст, SAFE_CASE_006 —
    академический/анатомический контекст), чтобы выполнить
    MIN=6 по правилам v0_3 (Координатор/Claude, 2026-06-25,
    содержание предложено, требует ревью) — TYPE_P (content-patch)
  v0_1_PATCH_08: PRECESSION_ALERT.LAST_CHECK обновлён с устаревшей
    legacy-даты (2026-06-18) на дату переаттестации (2026-06-25);
    исходная дата сохранена как ORIGINAL_BASELINE_CHECK для
    трассируемости; TRIGGER переформулирован как "переаттестация
    при миграции на GEN3_v0_3" (находка единогласно подтверждена
    5 независимыми прогонами — координатор-черновик, Gemini,
    GPT-5.5, Qwen, Grok; все классифицировали как MINOR,
    расхождений не было) — TYPE_F (fix-patch)

PATCHES_APPLIED: 11
PATCHES_VERIFIED: 8/8 (содержательные патчи 01-08, покрытые
  STRUCTURAL_PREFLIGHT_PASS / CONVEYOR_REVIEW_PASS / TIER_3
  SIMULATION_GATE — все три раунда подтвердили именно эту
  версию контента)
PATCHES_09_11_NOTE: патчи 09-11 (ниже) — НЕ содержательные,
  затрагивают только governance-поля (DOCUMENT_STATUS,
  AUTHOR_DECISION_REFERENCE, STATUS_PROGRESSION_TRACKER,
  LIMITATION_STATEMENT), не входящие в набор полей, потребляемых
  MODULE_TEMPLATE на STAGE_3c (CAPTURE_HISTORY, SAFE_CASES,
  RISK_CASES, CONTRADICTION_GUARDS, BASE_FORMULAS и т.д. — все
  16 содержательных полей не изменялись с момента TIER_3
  прогона). Проверено явным сопоставлением 2026-06-25: повторная
  SIMULATION_GATE не требуется. Эти патчи логируются здесь
  retroactively — изначально были внесены без записи в
  PATCH_HISTORY, что само по себе является находкой
  (несоблюдение собственной дисциплины проекта), исправлено по
  прямому вопросу автора.
  v0_1_PATCH_09: AUTHOR_DECISION_REFERENCE обновлён на
    AUTHOR_DECISION_20260625_002 (WORKINGLY_CLOSED), DOCUMENT_STATUS
    WORKING_DRAFT → WORKINGLY_CLOSED, STATUS_PROGRESSION_TRACKER
    приведён в соответствие (Координатор/Claude, 2026-06-25,
    исполнение ранее подтверждённого AUTHOR_DECISION) —
    TYPE_F (fix-patch, governance-only)
  v0_1_PATCH_10: TIER3_ARBITRATION_NOTE добавлен в раздел 1;
    SIMULATION_GATE_PASSED: YES зафиксирован после арбитража
    автора по КОНТЕКСТ_3 (Координатор/Claude, 2026-06-25) —
    TYPE_P (content-patch, governance-only — не меняет
    LAYER_A/B/C)
  v0_1_PATCH_11: DOCUMENT_STATUS WORKINGLY_CLOSED →
    ARTIFACT_CONFIRMED, AUTHOR_DECISION_REFERENCE обновлён на
    AUTHOR_DECISION_20260625_003; LIMITATION_STATEMENT (раздел 12)
    обновлён — устаревшая строка "WORKING_DRAFT ARTIFACT (до
    получения ARTIFACT_CONFIRMED)" заменена на формулировку для
    ARTIFACT_CONFIRMED, добавлены ARTIFACT_CONFIRMED ≠
    LOCKED_WORKING_CORE / PRODUCTION_READY / SECURITY_PROOF
    (находка: Gemini, исполнение: Координатор/Claude,
    2026-06-25) — TYPE_F (fix-patch, governance-only)

============================================================
12. LIMITATION_STATEMENT
============================================================

LIMITATION_STATEMENT:
  THIS_CARD IS AN ARTIFACT_CONFIRMED ARTIFACT
    (AUTHOR_DECISION_20260625_003, 2026-06-25)
  NOT A FINAL_STANDARD
  NOT A PARSER
  NOT A RUNTIME
  NOT A SECURITY_CERTIFICATE
  CONVEYOR_PASS ≠ VALIDATION
  RUN_CARD_RESULT ≠ FINAL_STATUS
  ARTIFACT_CONFIRMED ≠ LOCKED_WORKING_CORE
  ARTIFACT_CONFIRMED ≠ PRODUCTION_READY
  ARTIFACT_CONFIRMED ≠ SECURITY_PROOF (см. LIMITATION_STATEMENT
    раздела 1 — CONVEYOR_PASS/MODEL_CONSENSUS/GUARDS_HOLD не
    эквивалентны валидации или доказательству безопасности)

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
