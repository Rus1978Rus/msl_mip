ЧАСТНЫЙ АВТОРСКИЙ ПРОЕКТ / COMMERCIAL USE PROHIBITED

DOCUMENT_ID: CONVEYOR_PACKET_O1_IMPL_PLAN_2026-07-21
DOCUMENT_TYPE: CONVEYOR_PACKET
PACKET_TYPE: REVIEW / PACKET_SUBTYPE: IMPLEMENTATION_PLAN (судится ПЛАН РЕАЛИЗАЦИИ O1 —
  код ещё не писан)
DATE: 2026-07-21
PROJECT: MSL/MIP
AUTHOR: Руслан Малявский (AUTHOR_DECISION_STATUS_AUTHORITY)

РАМКА ПРОЕКТА: система ОПОВЕЩЕНИЯ, не антивирус. Машина свидетель, не судья. Уровень —
  рекомендация человеку. Судим ПЛАН реализации O1 ДО кода — O1 задевает верифицированный
  ZWSP-путь (батарея 21/21) и вердикты ZWJ/BOM.

============================================================
§1. ФАКТ (не на ревью — данные в теле)
============================================================
ЧТО РЕШЕНО (не пересматривать; AUTHOR_DECISION_20260721_D-O1-DESIGN APPROVED):
- O1 = CONTEXTUAL_SEVERITY_POLICY_LAYER: отдельный АДДИТИВНЫЙ per-occurrence слой НАД
  картой; общий `_SCOPE_RISK`/гейт741 НЕ редактируются; combine МОНОТОННЫЙ max(base,overlay);
  спарс-реестр (только карточные знаки, provenance, без wildcard/класс-дефолта, ZWSP-ключи
  невыразимы); РЕАЛЬНАЯ=HIGH→hold; предикат occurrence_role ЖИВЁТ В КАРТОЧКЕ; guard-cap раздельно.
- ВХОДЫ (RECONCILE_BYSPEC_ZWJ_BOM): BOM token/ident/email/ведущий-домен → РЕАЛЬНАЯ; ZWJ
  free-text → ВОЗМОЖНАЯ; Z4/B3.

ТОЧКА ИНТЕГРАЦИИ (из исходника — субстрат, не на ревью):
- Вердикт формируется в `_assess_relation_risk` (sequence_engine.py:706); dict вердикта
  (стр.751-767) несёт {visible_form, at_offset, detected_context, risk_level=risk.value(763),
  relation_type, runtime_role}. RiskLevel→action — sequence_integrator_engine.py:29.
- O1-overlay встаёт МЕЖДУ вычислением base-risk (763) и маппингом в action: final=max(base, overlay).

DELTA-CENSUS СУБСТРАТ (готов, commit 9bc9083): ZWSP 21/21 (sim_bycode_v2) + ZWJ/BOM 11/11
  (zwj_bom_battery) + mutation-adequacy 5/5 каждая. Против них строится «меняются РОВНО
  авторизованные ячейки».

КРИТИЧЕСКИЙ ФАКТ (центральная имплементационная дыра — ПОЧЕМУ план судится ДО кода):
- Дизайн говорит «occurrence_role из карточки». Но на шве вердикта рантайм имеет
  `detected_context` (HOST/EMAIL/FREE_TEXT/BYTE_EXACT_TOKEN/…), а НЕ occurrence_role.
- ZWJ PER_OCCURRENCE_BOUNDARY (functional vs redundant): карточка САМА признаёт, что
  различить их БЕЗ script-контекста рантайм НЕ МОЖЕТ (честная граница MAY_QUEUE до v0.5).
  Значит эскалацию Z5 (free-text ZWJ → ВОЗМОЖНАЯ) чисто реализовать НЕЛЬЗЯ: либо плоское
  правило (все free-text ZWJ → ВОЗМОЖНАЯ — то, что дизайн ОТВЕРГ, будит арабское письмо),
  либо предикат, которого у рантайма нет.
- BOM OBSERVATION_LEVEL (transport vs application): ЧАСТИЧНО контекст-выводим — leading+json
  измеряется FREE_TEXT (транспорт→ЧИСТО), leading+text = BYTE_EXACT_TOKEN (приложение→ВОЗМОЖНАЯ).
  То есть BOM occurrence_role МОЖЕТ быть выводим из контекста, ZWJ — нет. Асимметрия — ядро плана.

============================================================
§2. ВОПРОС РЕВЬЮЕРАМ (двигатель круга — план, «где дыра / чем обходится»)
============================================================
Спланировать реализацию O1 так, чтобы: доставить эскалации reconcile ТАМ, где рантайм МОЖЕТ
вычислить occurrence_role; НЕ сломать верифицированное (ZWSP 21/21 + ZWJ/BOM 11/11 через
delta-census); остаться в witness-рамке (монотонно, РЕАЛЬНАЯ→hold); не растить g; и ЧЕСТНО
назвать, что откладывается (ZWJ functional/redundant без script-контекста). По КАЖДОМУ
измерению I1-I7 — план + «где дыра».

============================================================
§3. ИЗМЕРЕНИЯ ПЛАНА (на ревью)
============================================================
I1. ШОВ ИНТЕГРАЦИИ. Хук на dict вердикта (после risk.value:763, до action-маппинга),
    final=max(base, overlay). Точно где, и как НЕ звать хотспот `_detect_context_at` повторно
    (overlay читает уже готовые detected_context/at_offset/visible_form)?

I2. OCCURRENCE_ROLE — ЯДРО. Кандидаты (не ограничивать):
    I2a. BOM: occurrence_role ВЫВОДИМ из detected_context (json/FREE_TEXT→transport→ЧИСТО;
         text/token→application→ВОЗМОЖНАЯ; mid-host→application→РЕАЛЬНАЯ). ZWJ: ОТЛОЖИТЬ
         эскалацию Z5 до script-контекста (v0.5) — free-text ZWJ остаётся как сейчас,
         честно помечено PENDING. Инкремент-1 = только контекст-выводимые ячейки.
    I2b. Плоское правило ZWJ×free-text→ВОЗМОЖНАЯ — ОТВЕРГНУто дизайном (будит арабское). CUT?
    I2c. Дешёвый script-proxy (доли скрипта видимого фона, как в input-guard) как приближение
         functional/redundant — реализуемо ли БЕЗ хотспота, и не та же ли это ловушка?
    Что доставляет доказанные ячейки, не выдумывая предикат, которого нет?

I3. ПОЛИТИКА-ТАБЛИЦА: схема (sign_id, context[, occurrence_role]) → target_level + provenance_id;
    линт (ключи ⊆ author-set; ZWSP невыразим; CRITICAL запрещён; класс-ключи запрещены; строка
    без provenance = FAIL); diff-тест «карточка↔таблица» в CI. Где растит g / где дыра линта?

I4. DELTA-CENSUS ГЕЙТ. Как ПОСТРОИТЬ доказательство «меняются РОВНО авторизованные ячейки»
    на ZWSP 21/21 + ZWJ/BOM 11/11: батареи прогоняются с O1 ВКЛ; ZWSP — БЕЗ изменений
    (нет ZWSP-ключей); ZWJ/BOM — меняются ТОЛЬКО авторизованные ячейки (обновить их ACCEPTABLE),
    всё прочее идентично; любое изменение вне авторизованных = FAIL. + mutation-adequacy обеих.

I5. МОНОТОННОСТЬ + INTEGRITY. O1 в вердикт-пути (меняет effective_action), но raise-only.
    Как overlay сожительствует с finish-line safeguard/`_integrity_check` (conservation-of-
    severity)? Поднятие уровня — не «under-escalation», но проверить, что integrity-слой не
    считает O1-поднятие нарушением.

I6. ОТЧЁТ/АУДИТ: поле report {base_level, final_level, rule_id, provenance}; вердикт-путь его
    читает (в отличие от report-only class_guard). Где грань «O1 меняет вердикт» vs «аудит-поле»?

I7. ЭТАПНОСТЬ. Инкремент-1 = только ячейки, где occurrence_role ВЫЧИСЛИМ (BOM контекст-выводимые);
    ZWJ functional/redundant + Z5 — инкремент-2 при script-контексте. Что минимально-полезно?

I-OTHER: измерение вне I1-I7. Если план как идея неверен (напр. O1 не место рантайма-шва) —
    сказать прямо (LOOPHOLE).

============================================================
§4. КРИТЕРИИ ОЦЕНКИ (по каждому измерению)
============================================================
(а) НЕ ЛОМАЕТ ВЕРИФИЦИРОВАННОЕ — ZWSP 21/21 + ZWJ/BOM 11/11 + mutation переприйдут через delta-census.
(б) ДОСТАВЛЯЕТ ДОКАЗАННЫЕ ЭСКАЛАЦИИ — где occurrence_role вычислим; отложенное честно названо.
(в) r>g — overlay дёшев, реестр спарс, без роста g на знак.
(г) WITNESS-РАМКА — монотонно, РЕАЛЬНАЯ→hold, не авто-блок.
(д) РЕАЛИЗУЕМ — детерминированно, gated; delta-census строится.
(е) НЕ СОЗДАЁТ ПОВЕРХНОСТИ — не выдумывать предикат (плоское правило будит письменности);
    не звать хотспот; overlay не понижает.
Ревьюер: по каждому измерению 6 отметок + BASIS; для I2 (occurrence_role) и I7 (этапность) —
явный выбор; RANKED_OUTCOME; RECOMMENDATION (скелет плана); явно — план верен или LOOPHOLE.

============================================================
§5. ГРАНИЦЫ
============================================================
- Судим ПЛАН реализации O1. НЕ пересматриваем: дизайн O1 (APPROVED), класс 138, трёхуровневый
  принцип, witness-рамку, батареи.
- КОД НЕ ПИШЕМ до author decision по плану. ZWSP НЕ ТРОГАЕМ (план говорит КАК ре-валидировать).
- НЕ смешивать с input-guard (бюджет входа) и O(n²)-фиксом (перф) — другие фронты.
- Закрытие карточек ZWJ/BOM — ПОСЛЕ O1 (финальное поведение), отдельный заход.

============================================================
§6. ДИСЦИПЛИНА (приложена)
============================================================
- AUTHOR_DECISION_20260721_D-O1-DESIGN — дизайн (BASIS, не на ревью);
- RECONCILE_BYSPEC_ZWJ_BOM_2026-07-18 — входы (эскалации);
- cards ZWJ (PER_OCCURRENCE_BOUNDARY) / BOM (OBSERVATION_LEVEL) — предикаты + честная граница;
- tests/sim_bycode_v2 (ZWSP 21/21) + tests/zwj_bom_battery (ZWJ/BOM 11/11) — delta-census субстрат;
- sequence_engine._assess_relation_risk (шов) / sequence_integrator (action) — точка кода;
- CONVEYOR_PACKET_GUARD_IMPL_PLAN (прецедент: план нашёл дыру гейта №1) — план ловит реальное;
- FOUNDATION_CONCEPT_PIKETTY_R_G — r>g; RULE_DESIGN_ADVERSARIAL_SIM — атака-симуляция до решения.

============================================================
DELIVERABLE_FORMAT
============================================================
REVIEW_RESULT: REVIEWER / MODEL_FAMILY (семейств >=3); по КАЖДОМУ измерению I1-I7 (+OTHER) —
  отметки (а)-(е) + BASIS; для I2 и I7 — явный выбор; RANKED_OUTCOME; RECOMMENDATION (скелет
  плана) как рекомендация, не статус; явно — план верен или LOOPHOLE.
СЛЕПОТА: план-круг; шов кода и измеренная асимметрия ZWJ/BOM в §1 — СУБСТРАТ, дан законно.
EXIT: план сходится → AUTHOR_DECISION по плану → ТОЛЬКО ПОТОМ код + delta-census-гейт; расходятся
  → материал для AUTHOR_DECISION; план неверен → LOOPHOLE, пере-собрать.

FORK_STATUS: OPEN — PENDING_CONVEYOR + AUTHOR_DECISION (план реализации O1). Код заблокирован.

END_OF_CONVEYOR_PACKET
