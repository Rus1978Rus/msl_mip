ЧАСТНЫЙ АВТОРСКИЙ ПРОЕКТ / COMMERCIAL USE PROHIBITED

DOCUMENT_ID: PRINCIPLE_GATE_MUST_BE_HERMETIC
LAYER: FOUNDATION_LAYER
DOCUMENT_TYPE: ENGINEERING_PRINCIPLE (дисциплина гейтов)
NAME: GATE_MUST_BE_HERMETIC
STATUS: ACCEPTED
AUTHOR_DECISION: Руслан Малявский, 2026-07-12
BASIS: gate_solidus_scheme дал 27/28, затем дважды 28/28 при НЕИЗМЕННОМ
       коде. Разбор показал не «шум», а недопустимую зависимость гейта
       от внешнего сетевого источника.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ПРИНЦИП
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GATE_MUST_BE_HERMETIC:
  Гейт НЕ имеет права зависеть от внешних источников (сеть, живой
  реестр, изменяемый кэш, часы, случайность). Один и тот же код на одном
  и том же входе обязан давать один и тот же вердикт КАЖДЫЙ раз,
  независимо от того, доступна ли сеть и что она вернула.

  Живой справочник — для РАНТАЙМА. Пришпиленный — для ГЕЙТА.

  Гейт, зависящий от сети, — не гейт: он даст зелёный на СЛОМАННОМ
  коде, если сеть «подсказала» правильный ответ, и красный на РАБОЧЕМ
  коде, если сеть подвела. Это молчаливая деградация, а не тестовый
  сигнал. «Зелёный 20 раз» при живой сети НЕ доказывает корректность —
  доказывает лишь, что сеть в тот момент отвечала.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ДОКАЗАННАЯ ПРИЧИНА (не гипотеза)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Цепочка касания сети:
  gate_solidus_scheme.py спавнит msl_mip_runtime.py на КАЖДЫЙ кейс →
  runtime при старте зовёт dot_matcher.get_compound_suffix_source() и
  get_single_tld_source() → public_suffix.load_compound_suffixes() /
  load_single_tlds() → urllib.request.urlopen(publicsuffix.org /
  data.iana.org, timeout=3). Плюс gate_relation_verdict_step4.py →
  process_sequence → _assess_relation_risk → sequence_engine._tlds() →
  та же load_single_tlds().

Конкретный флип-кейс (измерено, не предположено):
  «paypal.com.security-check.ru» (gate_solidus_scheme, «dot substitution»)
    TLD-набор С 'ru'    → domain_separator + RISK_CASE_002 → HOLD (верно)
    TLD-набор БЕЗ 'ru'  → file_extension, без риска        → PASS (тихий
                          зелёный на том, что должно флагироваться)
  Частичный/битый/протухший ответ IANA, где 'ru' выпал, молча красит
  гейт зелёным. Это и есть молчаливая деградация.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
МЕХАНИЗМ ГЕРМЕТИЗАЦИИ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Флаг окружения MSL_MIP_HERMETIC_TLD (public_suffix.py): при установке
load_compound_suffixes() и load_single_tlds() ПРОПУСКАЮТ сеть и кэш и
возвращают встроенные (in-repo) EMBEDDED-наборы — детерминированный,
offline, пришпиленный источник (source = "EMBEDDED_HERMETIC"). Поведение
по умолчанию (флаг снят) не меняется: live → cache → embedded, как в
проде. Рантайм честно печатает HERMETIC-режим (не врёт про «нет сети»).

Способы пришпиливания по гейтам:
  - подпроцессный гейт (spawns runtime): MSL_MIP_HERMETIC_TLD="1" в env
    подпроцесса (gate_solidus_scheme);
  - in-process гейт: os.environ до первого вызова, ИЛИ прямой пин
    состояния (gate_bare_domain_detector: _force_tld_state_for_test с
    _PINNED_TLDS — ещё жёстче, задаёт конкретный набор);
  - gate_relation_verdict_step4: os.environ в шапке до импортов.

Гейт без внешних источников вовсе (gate_english_only — только чтение
файлов) герметичен по построению, флаг не нужен.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ПОДТВЕРЖДЕНИЕ (воспроизводимость = измерение)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

После герметизации каждый гейт прогнан 20 раз подряд:
  gate_bare_domain_detector  20/20  40 OK / 0 FAIL
  gate_english_only          20/20  CLEAN
  gate_relation_verdict_step4 20/20  12 OK / 0 FAIL
  gate_solidus_scheme        20/20  28/28
Offline-доказательство: под флагом runtime печатает
"EMBEDDED_HERMETIC" (сеть/кэш пропущены), спорный кейс остаётся HOLD.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ПРАВИЛО ДЛЯ БУДУЩИХ ГЕЙТОВ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Новый гейт ОБЯЗАН быть герметичным до включения в набор. Если он
   касается TLD/суффиксов — MSL_MIP_HERMETIC_TLD или прямой пин.
2. Любой новый внешний источник (сеть, БД, часы, случайность) в пути
   гейта требует такого же offline-пришпиливания. Если пришпилить
   нельзя — это не гейт, а мониторинг; выносить отдельно.
3. Приёмка гейта включает прогон N≥20 раз с идентичным результатом.
   Заявление «стабильно» без измерения не принимается (ср.
   ACK_GAP_TRIVALENT: утверждение ≠ доказательство).

СВЯЗЬ: SIGN_CORE_CARD_CONVEYOR_RULES (этап SIMULATION_GATE_PASSED — гейт
должен быть герметичным, чтобы его PASS что-то значил),
CONVEYOR_RUN_PACKET_TEMPLATE (FINDING_BASIS: то же требование измерять,
а не заявлять), public_suffix.py (флаг MSL_MIP_HERMETIC_TLD),
gate_bare_domain_detector.py (_PINNED_TLDS — образец прямого пина).

═══════════════════════════════════
