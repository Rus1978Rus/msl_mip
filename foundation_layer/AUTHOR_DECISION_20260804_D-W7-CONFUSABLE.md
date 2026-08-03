# AUTHOR_DECISION: видимые двойники / mixed-script host-spoof ось (W7) — дизайн ратифицирован

**Статус:** AUTHOR_DECISION (дизайн принят; КОД под acceptance-гейтом + снятием блокеров B1–B8 спекой)
**Дата:** 2026-08-04
**Автор:** Руслан Малявский (AUTHOR_DECISION_STATUS_AUTHORITY) — одобрил синтез координатора по F1–F4 («одобряю»)
**Тип:** новая ось детекции (структурная, аддитивная), witness-рамка, two-tier классовая карточка
**Основание:** CONVEYOR_PACKET_W7_CONFUSABLE_2026-07-26; **4 РАЗНЫХ семейства** (Grok/xAI, Gemini/Google,
  Qwen/Alibaba, GPT-5.6/OpenAI) + 5-й методологический свод (4 стойки SECURITY/FP/VERIFY/REDTEAM, одна
  платформа, самооговорка); координаторский свод + attack-sim: [conveyor_runs/W7_SVOD_AND_SIM_2026-08-04.md];
  леги: conveyor_runs/W7_legs/. §1 подтверждён замером 2× (пакет + координатор).

РАМКА: свидетель, не судья. Уровень = рекомендация человеку. Ось только ПОДНИМАЕТ effective_action,
  witness сохраняет, source и canonical-вывод не трогает, карточный вердикт не понижает. Монотонно/аддитивно.

## §1 ФАКТ (измерено на живом ядре)
ВСЕ видимые двойники сегодня → silent pass, attn=NONE (confusable-карточек нет; 9 карточек = . / ／ / @ /
  💀 / ☠ / ZWSP / ZWJ / BOM). `gоogle.com`(U+043E), `pаypal.com`(U+0430), `paypal．com`(U+FF0E),
  `paypal。com`(U+3002) → pass. Легит `sber.рф`, `α-testing` в прозе → pass. ATTACK-SIM (координатор,
  2026-08-04): `xn--80ak6aa92e.com` → silent pass (нет IDNA-декода); stdlib `unicodedata` НЕ имеет
  Script/Script_Extensions (unidata_version=16.0.0); `analyze(text,cards,protected_targets=None)` уже
  прокинут в O1Context exact-match; `_canon_domain_seps` (sequence_engine.py:540) уже маппит `。．｡`→`.`
  жёстким dict, но МОЛЧА и только для распознавания формы домена вокруг маски.

## КОНВЕРГЕНЦИЯ (устоявшееся — принято как основа, не пере-решается)
V1=C одна КЛАССОВАЯ confusable-ось two-tier (механизм A=mixed-script+skeleton живёт ВНУТРИ карточной оси,
  не нарушает ARCH_DECISION_HOMOGLYPH_VIA_CARD_ONLY); host-only + per-LABEL (не per-host); триггер =
  «латиница ∧ confusable-знак иного скрипта в ОДНОМ label + участвует в фактическом UTS#39-маппинге»,
  НЕ голый «≥2 скрипта» (Common/Inherited не скрипт; CJK Jpan/Kore/Hanb-комбинации легит по UTS#39 §5.2);
  generic → queue; B(81 Vakhter) отклонён как самостоятельный детектор (измеренный α-testing FP), только
  nursery/test-corpus. Отклонено замером: per-host счёт (FP sber.рф) и живой/непиннутый UTS#39.

## ПРИНЯТЫЕ РЕШЕНИЯ (D1–D8)

**D1 — МЕХАНИЗМ (V1=C).** Одна классовая карточка `VISIBLE_CONFUSABLE_RELATION` (two-tier по
  ARCH_DECISION_20260726_TWO_TIER). Держит: версии+sha256 трёх таблиц, skeleton-алгоритм UTS#39
  (NFD→map→NFD), script-профиль, severity-политику, target-контракт. Ядро-механизм A (mixed-script+
  skeleton) — ВНУТРИ карточной оси, не самостоятельный детектор. Пер-обнаружение порождает
  `CONFUSABLE_RELATION_RECORD` (source_cp, position, mapped_prototype, source_script, label_id, skeleton,
  target_collision, relation_status, data_version). Tier-2 тонкие знак-карточки — только где нужно
  (спорные/known-attack/легит-лингвистика/особая severity). НЕ 81 полная карточка.

**D2 — ТРИГГЕР / FP-ГРАНИЦА (V2, патч P1).** CANDIDATE = context==HOST (спека B1) AND per-LABEL (между
  точками) AND label содержит ≥2 resolved explicit script (по запиненной Scripts.txt/ScriptExtensions.txt —
  Common/Inherited НЕ скрипт) AND ≥1 cross-script знак участвует в ФАКТИЧЕСКОМ UTS#39 confusable-маппинге.
  Отвергнут «HAS_LATIN AND HAS_NON_LATIN» как достаточный. CJK-исключения (Han+Kana/Hangul один label = норма).
  `sber.рф` → каждый label моно-скрипт → pass; `α-testing` в прозе → нет host → pass (убивает измеренный
  Vakhter FP без греко-списков). Честный остаток: `α-testing.com` в host → queue (запинено ячейкой, B5).

**D3 — УРОВЕНЬ + ЯРУС (V3/V4, F2 = СЕЙЧАС).** Два яруса:
  • Ярус 1 (безсписочный): mixed-script confusable в host-label БЕЗ target-collision → **queue_for_review**
    (ВОЗМОЖНАЯ; паритет W4/W5/D-INV-GEN; hold при неизмеренной base-rate = приговор без статистики).
  • Ярус 2 (списочный, F2 принят СЕЙЧАС — проводка готова, SIM-4): skeleton(label)==skeleton(caller-target)
    AND raw!=target AND confusable present → **hold_pending_review** (РЕАЛЬНАЯ). Реюз паттерна
    AUTHOR_DECISION_20260721_D-O1-C6-NARROW. SECURITY (P2): targets ТОЛЬКО от доверенного вызывающего слоя;
    пользовательский текст НЕ задаёт targets. target-match = EXACT_LABEL, per-label, не по подстроке (P5).
  Free text → без изменения severity.

**D4 — FULLWIDTH/IDEO-ТОЧКИ (F1 = ОТДЕЛЬНАЯ ОСЬ).** `．。｡` (U+FF0E/U+3002/U+FF61) — НЕ этот
  буквенный фронт, а отдельная ось «разделитель похож на разделитель» (parser-differential) на DOT-пути.
  Канон = UTS#46/IDNA-маппинг (не «NFKC вообще»: U+3002 не имеет NFKC-декомпозиции). Существующий
  `_canon_domain_seps` даёт верный dict, НО молча → обязателен B4 (событие ДО канонизации). Уровень:
  alt-separator в host → queue; collision с protected-доменом → hold. (Grok/FP «внутрь через NFKC» —
  отклонено: смешение осей нарушает §5 и технически неверно для U+3002.)

**D5 — ИСТОЧНИК ТАБЛИЦ (F4).** Skeleton — из ЗАПИНЕННОЙ UTS#39 как ИСТОЧНИКА (версия UCD + sha256), плюс
  author-owned production-поднабор (= полная МИНУС отложенные, D6) с diff-тестом против источника. НЕ живой
  UTS#39 (тихая смена поведения), НЕ ручной без provenance (неполнота/окно перебора). Полная таблица = слой
  ДАННЫХ; курированный поднабор = АКТИВНАЯ политика (P3). ТРИ пиннутых артефакта репо (SIM-3): confusables +
  scripts/scriptext + UTS#46, ver+sha256, assert unidata_version=16.0.0; bump = author decision (B6).

**D6 — 4 СПОРНЫХ МАППИНГА (F3 = ОТЛОЖИТЬ).** ѡ→w, η→n, ա→a, ս→u — данные СОХРАНЕНЫ в источнике, но
  generic-severity ВЫКЛЮЧЕНА; обязательные маркер-ячейки «не срабатывает» (B5) + именованная запись в
  реестре остатка (B8). BASIS: η частотна в научной нотации (прямой FP-генератор), ա/ս армянский легит.
  ДИССЕНТ (SECURITY: включить, они в confusables.txt, witness переносит спорность на человека) —
  зафиксирован; пере-открывается только измеренным корпусом.

**D7 — WHOLE-SCRIPT SPOOF = ОТДЕЛЬНЫЙ ФРОНТ, ЯРЛЫК «БАЙПАСС».** `аррӏе.com` (весь label один не-латинский
  скрипт) mixed-script детект НЕ ловит (тот же single-script тест, что спасает sber.рф). Target-free детекта
  НЕ существует (UTS#39 §4.1). Разрешим только ярусом 2 (список) или отдельным пакетом. Тихое расширение
  этого фронта на whole-script БЕЗ списка = единственный настоящий LOOPHOLE-вектор → ЗАПРЕЩЕНО; фиксируется
  в реестре остатка (B8) как БАЙПАСС, не «отложенный остаток».

**D8 — ИНВАРИАНТЫ.** Ось аддитивна raise-only; witness сохраняет; source и report['text'] = сырой вход
  (не подменять skeleton/IDNA-видом — держать RAW + IDNA_mapped + punycode + skeleton, V-OTHER-1);
  карточный вердикт не понижает; delta-census на FROZEN baseline (B5). Порядок: детект → событие →
  канонизация (B4).

## БЛОКЕРЫ ДО КОДА (снять СПЕКОЙ; код заблокирован пока не закрыты)
- **B1** СПЕКА извлечения host-токена: scheme/authority/userinfo (`p@evil.com`), email local-part
  (`α-user@lab.org` → молчит), видимый-текст vs href. [SIM-5 подтвердил дыру: хелперы есть, спеки нет]
- **B2** IDNA/punycode-декод ДО детекта + пин UTS#46. [SIM-1: `xn--` silent pass]
- **B3** Пин ТРЁХ таблиц (confusables + scripts/scriptext + UTS#46) ver+sha256 + assert unidata_version;
  таблицы = артефакты репо, не рантайм-генерация. [SIM-3]
- **B4** Порядок пайплайна детект→событие→канонизация; тихий ремонт входа запрещён. Переподписать
  §1-строку `paypal．com` (по UTS#46 = легит-канон paypal.com; замер pass — факт, ярлык «spoof» —
  интерпретация; вектор = расхождение парсеров границ, не буква-двойник). [SIM-2]
- **B5** Батарея на FROZEN baseline (старый корпус побайтово + новые ячейки аддитивным отчётом;
  «не-confusable» = ПЕРЕЧИСЛЕНИЕ, не свойство). Обязательные ячейки: позитивы pаypal/gоogle/gοogle/
  gօogle/Ⅽoinbase/paypal．com/paypal。com/смешанный-регистр/xn--после-декода; легит-контроли sber.рф/
  японский-IDN(Han+Kana)/корейский/дефисная-латиница/наука-в-прозе; блокер-ячейки α-testing.com-in-host→
  queue, α-user@lab.org→молчит, моно-скрипт-псевдобренд→не-срабатывает+реестр, 4 отложенных→не-срабатывает.
- **B6** Bump-политика пиннутых таблиц = явное author decision (кто/когда/ре-валидация); обновление =
  миграционное событие с отдельным delta-census, не тихая зависимость от latest.
- **B7** Witness-рендер: punycode/скрипт-аннотация в канале «смотри глазами» (иначе пуст для истинных
  гомоглифов — глаза их не различают).
- **B8** РЕЕСТР ОСТАТКА (именованный): whole-script unlisted = ПОЛНЫЙ БАЙПАСС; 4 отложенных маппинга;
  наука-домены (α-testing.org) = остаточный queue-FP; вне-списочные бренды без яруса-2; ёмкость очереди
  (переполнение = фактический pass); r>g без корпуса — публиковать ИЗМЕРЕННЫЙ FP-набор, не численные претензии.

## ПОРЯДОК РЕАЛИЗАЦИИ (после снятия B1–B8; каждый шаг = свой acceptance-гейт + delta-census)
1. Пин трёх таблиц как артефактов репо + oracle-тесты (B3, D5). 2. host-токен спека + IDNA-декод (B1,B2).
3. Ярус 1 (per-label mixed-script confusable → queue) + frozen батарея (D2,D3,B5). 4. Ярус 2 (caller-target
skeleton-collision → hold, реюз C6-NARROW) (D3). 5. Отдельная separator-ось + событие-до-канонизации (D4,B4).
6. Witness-рендер punycode (B7) + реестр остатка (B8).

**Основание r>g:** поднимает mixed-script spoof из тотального silent pass; host-гейт+per-label гасит
измеренный α-testing FP без списков; классовая ось (не 81 карта) держит g; hold только списочный
(дорогой ложный-hold заперт за caller-target). [[FOUNDATION_CONCEPT_PIKETTY_R_G]]

FORK_STATUS: F1–F4 РЕШЕНЫ. B1–B8 ЗАКРЫТЫ СПЕКОЙ 2026-08-04 →
foundation_layer/SPEC_20260804_W7_BLOCKERS_B1-B8.md (с довызовным замером: userinfo уже покрыт AT-картой;
_looks_like_domain юникодный — субстрат готов). КОД РАЗБЛОКИРОВАН по порядку реализации выше.
