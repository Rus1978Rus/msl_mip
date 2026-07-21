ЧАСТНЫЙ АВТОРСКИЙ ПРОЕКТ / COMMERCIAL USE PROHIBITED

DOCUMENT_ID: RAW_REVIEWS_O1_IMPL_PLAN_2026-07-21
DOCUMENT_TYPE: RAW_REVIEW_BUNDLE + COORDINATOR_SVOD + ATTACK_SIM (сверяемый источник; НЕ author decision)
DATE: 2026-07-21
PACKET: CONVEYOR_PACKET_O1_IMPL_PLAN_2026-07-21 (план-круг реализации O1 — код ещё не писан)
STATUS: RECORD. Author decision по ПЛАНУ реализации O1 — ОТДЕЛЬНЫЙ заход. Здесь решений НЕТ.
NOTE: полные вербатим-ответы ног — в транскрипте сессии; здесь сжатая, но сверяемая запись
  каждой ноги + свод против raw + атака-симуляция на живом ядре (per RULE_DESIGN_ADVERSARIAL_SIM).
  Свод и атака-симуляция помечены как синтез/измерение координатора.

============================================================
СОСТАВ НОГ (5 ног, 4 самостоятельных семейства; >=3 выполнено)
============================================================
LEG 1 — GPT-5.6 Thinking (OpenAI GPT) — АДВЕРСАРИАЛЬНО-КОНСТРУКТИВНАЯ; залатала 3 реальные дыры.
LEG 2 — GPT-5.5 / Codex (OpenAI reasoning; ТО ЖЕ семейство, что нога 1). Код-обоснованная (file:line).
        «3 роли A/B/C» = ОДНА модель, ОДИН голос. => 2 ноги, всё ещё ОДНО семейство.
LEG 3 — Kimi K3 (Moonshot-Kimi) — ИНОЕ семейство; РАСШИРИЛА scope + нашла дыру покрытия.
LEG 4 — Grok (xAI/Grok) — 3-е семейство; подтверждающая; BOM-only, не подхватила scope/дыры Kimi.
LEG 5 — Gemini (Gemini) — 4-е семейство; подтверждающая; BOM-only.
Адверсариальных: 2 (GPT нога 1, Kimi). Подтверждающих: 3.

Rule provenance: >=3 РАЗНЫХ семейства — соблюдено (OpenAI x2 = одно; Moonshot; xAI; Gemini).
  Схождение двух OpenAI-ног != независимость (общая слепая зона: обе OVER-DEFER ZWJ, обе прошли
  мимо confluence-дыры). Иное семейство (Kimi) снова сделало работу, что пара OpenAI пропустила.

============================================================
LEG 1 — GPT-5.6 Thinking (OpenAI GPT)
============================================================
VERDICT: APPROVE_WITH_MAJOR_IMPLEMENTATION_PATCHES. План верен, шов верен, NO LOOPHOLE.
  SELECT I2 = I2a, СУЖЕННЫЙ до provably-resolvable ролей. SELECT I7 = BOM-first, ZWJ-deferred.

*** ТРИ РЕАЛЬНЫЕ ДЫРЫ, исправленные в подходе моего пакета ***
  H1 (I1 шов): пакет сказал «хук между risk.value(763) и action-map». НЕВЕРНО — risk.value УЖЕ
     сериализован ("MEDIUM" строка). O1 обязан работать с RiskLevel ENUM ДО сборки вердикт-dict.
     Верный шов: после вычисления base_risk:RiskLevel, ДО сериализации risk.value. Последовательность:
     base_risk -> resolve_occurrence_role -> evaluate_o1_policy -> final=max(base,overlay) ->
     serialize -> map to action.
  H2 (I2 BOM): «BOM контекст-выводим: FREE_TEXT->transport->clean» СЛИШКОМ РЫХЛО. Ведущий BOM на
     offset 0 + FREE_TEXT НЕ доказывает TRANSPORT (рантайм может получить уже декодированную строку;
     U+FEFF может быть реальным сохранённым BOM, литеральным app-префиксом, вставленным юзером или
     ingress-артефактом). FIX: OCCURRENCE_ROLE_STATUS {PROVEN, INFERRED, UNVERIFIABLE}; overlay
     ТОЛЬКО для PROVEN. PROVEN BOM = INTERNAL (offset>0) + BYTE_EXACT_TOKEN/IDENT/EMAIL/HOST (не может
     быть stream-start BOM). Ведущий BOM offset 0 = UNVERIFIABLE без ingress-метаданных -> НЕТ overlay
     (инкремент 2). => даже BOM сужается: инкремент-1 = INTERNAL BOM only, НЕ ведущий-домен.
  H3 (I6 отчёт): не строить report-dict, который вердикт-путь ЧИТАЕТ (делает аудит источником
     контроля -> десинхрон). ОДИН типизированный PolicyDecision -> используется интегратором И
     сериализуется в отчёт. Отчёт ОБЪЯСНЯЕТ решение, никогда не пересчитывает severity.

ДРУГИЕ СИЛЬНЫЕ ПАТЧИ:
  I2 ZWJ: полностью DEFER — Z5 И Z4 remap PENDING до реального script/joining/sequence-context слоя.
    Плоское правило CUT. Script-proxy DEFER (арабский фон != этот ZWJ функционален).
  I3: version-approved allowlist ACTIVE_POLICY_SIGN_SET_v0_1={U+FEFF} (не хардкод «if 200B reject»).
    ЕДИНЫЙ ИСТОЧНИК: КАРТА определяет occurrence-role СЛОВАРЬ + границу; POLICY REGISTRY = единственный
    рантайм-источник severity; НЕ хранить severity и в карте, и в таблице (мой diff-тест был опасен).
    CI: роль политики в объявленных картой ролях; severity только в реестре.
  I4: FROZEN baseline + AUTHORIZED_DELTA_MANIFEST (не просто править ACCEPTABLE — прячет незапланированное).
    Два режима O1 off/on. ZWSP ноль семантических дельт; ZWJ ноль (отложен); BOM меняет ТОЛЬКО
    перечисленные case_ids (только risk_level/action/audit; context/offset/identity фикс). Инвариант:
    AUTHORIZED CONTEXT != AUTHORIZED CASE (авторизуй конкретные ячейки с доказанной ролью, не класс
    контекста). + 10 O1-мутаций (wildcard sign, ZWSP rule, UNVERIFIABLE-role apply, drop context cond,
    max->assign, CRITICAL, no provenance, non-authorized BOM case, ZWJ flat rule, recompute-via-hotspot).
  I5: integrity-формула (final>=base, overlay<=HIGH, no-match->final==base, match->final==max);
    _integrity_check обязан ВИДЕТЬ base+overlay+final и сам проверять монотонность (не доверять O1,
    не считать подъём контаминацией).
  I7 ИНКРЕМЕНТЫ: 0 (ПУСТОЙ engine + zero-delta гейт -> доказывает, что ШОВ сам по себе ничего не
    меняет) -> 1 (PROVEN internal BOM only) -> 2 (ingress-aware ведущий BOM) -> 3 (ZWJ role engine:
    отдельный конвейер+батарея) -> 4 (ZWJ rules). Инкремент-0 zero-delta — сильное добавление.
  I-OTHER-1 UNKNOWN-ROLE: UNVERIFIABLE != CLEAN != REAL; нет overlay, base сохранён, ограничение
    записано (не тихий pass). I-OTHER-2 fail-visible policy-load. I-OTHER-3 perf: O1-no-match ~ O1-off.

============================================================
LEG 2 — GPT-5.5 / Codex (OpenAI reasoning; ТО ЖЕ семейство)
============================================================
VERDICT: ACCEPT_WITH_CONDITIONS. План верен iff I2a + этапный I7; LOOPHOLE только при flat-ZWJ /
  script-proxy / audit-only / _SCOPE_RISK-edit / wildcard-class / O1-over-ZWSP.
СХОДИТСЯ с ногой 1 по: SELECT I2a-narrowed, CUT I2b flat, CUT/DEFER I2c script-proxy, этапный I7
  (BOM-first, ZWJ Z5 отложен), спарс-реестр + линт, tuple-level delta-census + AUTHORIZED_DELTA +
  два режима, raise-only max + integrity видит final risk_level, O1 обязан быть VERDICT-DRIVING
  (не audit-only, т.к. _relation_actions читает v["risk_level"] msl_mip_runtime.py:131-155).
НОВОЕ (сверх ноги 1): I-OTHER-1 SIGN_ID STABILITY — ключ политики по sign_id/идентичности карты, НЕ
  visible_form (display/projection -> случайный кросс-знак матч). I-OTHER-2 нет O1 над _demask.
  I-OTHER-3 mention-vs-use (реестр по реально обнаруженному знаку, не строке "U+FEFF"/"BOM").

НОГА 1 ОСТРЕЕ по 3 пунктам (то же семейство, но нога 1 поймала больше):
  1. ШОВ: нога 1 — НЕ max над сериализованным risk.value (использовать RiskLevel ENUM). Псевдокод
     ноги 2 ВПАДАЕТ ровно в это ("base_level=risk.value; final=max(base,target)" — max над СТРОКАМИ).
     Даже внутри OpenAI нога 1 поймала шов-дыру, что нога 2 пропустила. -> нога 1 права.
  2. I2 BOM FORK (внутрисемейное расхождение, ключевая цель атака-симуляции): нога 1 — только INTERNAL
     BOM PROVEN; ВЕДУЩИЙ offset 0 + FREE_TEXT = UNVERIFIABLE (инкремент 2). Нога 2 — leading-text vs
     leading-JSON уже различены (карта + батарея B1 queue / B1J pass) -> ведущий BOM ВЫВОДИМ в
     инкременте-1. -> ЖИВАЯ РАЗВИЛКА, ИЗМЕРИМА. Атака-симуляция на своде.
  3. ИНКРЕМЕНТ-0 (пустой engine + zero-delta): у ноги 1 есть, нога 2 идёт прямо к BOM. Нога 1 безопаснее.
ОБЕ СОГЛАСНЫ (принять): sign_id-not-visible_form ключевание. Правит МОЙ пакет (там был visible_form).

============================================================
LEG 3 — Kimi K3 (Moonshot-Kimi) — ИНОЕ семейство
============================================================
VERDICT: план верен, NOT LOOPHOLE, VERIFIED (план-уровень). Первое иное семейство — снова сделало
  работу, что пара OpenAI пропустила. 3 ноги / 2 семейства.

*** MAJOR: РАСШИРЯЕТ инкремент-1 (ZWJ machine-string, ни у одной OpenAI-ноги не было) ***
  Обе OpenAI-ноги отложили ВЕСЬ ZWJ. KIMI: ZWJ в МАШИННОЙ СТРОКЕ (token/email/ident) РЕДУНДАНТЕН
  ВСЕГДА — у машинного идентификатора нет арабского/персидского соединения, значит ZWJ там без
  функциональной роли, КОНТЕКСТ САМ — предикат. => Z4/B3 (ZWJ x {token,email}) доставляемы СЕЙЧАС,
  без script-контекста. Только ZWJ x FREE_TEXT нужен script -> UNKNOWN/defer.
  -> инкремент-1 = BOM x4 + ZWJ x2 = 6 из 7 ячеек reconcile; только Z5 честно PENDING.
  [ПРИМЕЧАНИЕ КООРДИНАТОРА: это утверждение ИЗМЕРИМО и оказалось ПЕРЕвёрнуто атака-симуляцией — см. F1.]

BOM FORK — Kimi через ROLE-BY-ABSENCE: json/FREE_TEXT -> transport -> НЕТ строки -> base сохранён
  (pass/CLEAN остаётся ПО ОТСУТСТВИЮ, обходит «нужно доказать transport» ноги 1); token/email/
  измеренный-ведущий-домен -> application -> строка -> HIGH. Клонится к ноге 2 (ведущий доставляем),
  но обрабатывает неоднозначность ноги 1 не-эскалацией FREE_TEXT-случая.

*** НОВАЯ ДЫРА (ни одна OpenAI-нога не отметила): CONFLUENCE COVERAGE ***
  Обе OpenAI-ноги: «хук в _assess_relation_risk». Kimi: есть НЕСКОЛЬКО вердикт-путей (single_actions /
  relation_actions / semantic_action). Хук на ОДНОЙ функции ПРОПУСКАЕТ dict-ы других путей -> ОДИН и
  тот же BOM в ОДНОМ контексте эскалирует или нет в зависимости от пути прихода. FIX: post-pass в
  ТОЧКЕ СЛИЯНИЯ (последняя общая точка перед RiskLevel->action, через которую проходят ВСЕ вердикт-
  dict-ы); план перечисляет все пути + доказывает покрытие каждого. Тест: каждый reconcile-кейс через
  свой путь, эскалация наблюдается (row-liveness).
  [ПРИМЕЧАНИЕ КООРДИНАТОРА: атака-симуляция (F4) показала — для BOM/ZWJ риск только через
   relation_verdicts; хук там покрывает. Тревога Kimi верна КАК ОБЩИЙ ПРИНЦИП плана, но для инкремента-1
   (только BOM) не блокер.]

ДРУГИЕ ЗАТОЧКИ:
  - I1 batch-post-pass o1_apply(verdicts) в точке слияния, НЕ inline-правка на 763 (меньше diff +
    покрывает все пути). dict-only, хотспот не зовётся.
  - I2c script-proxy CUT с ОСТРЕЕ причиной: ошибается в ОПАСНУЮ сторону (UNDER-alarm) — «арабский фон ->
    ZWJ функционален -> CLEAN» УСЫПЛЯЕТ вектор Z3-BYPASS. Для witness-системы молчание на известном
    враждебном векторе хуже ложной тревоги. (OpenAI режут за FP; Kimi за under-alarm — глубже.)
  - I3 ROW-LIVENESS: каждая строка обязана СТРЕЛЯТЬ на своём reconcile-входе (мёртвая строка проходит
    линт, но ничего не доставляет = ТИХАЯ недопоставка). lint + liveness + census — все три.
    + sign_id = CODEPOINT якорь (не имя; алиасы = канал обхода) + row-monotonicity линт.
  - I4 delta-census: OFF-vs-ON DIFF (не single-run-vs-expectations) + exact-match + NEGATIVE SPACE
    (широкий benign-корпус ВНЕ 3 батарей -> ноль изменений вне авторизованных ячеек).
  - I5 порядок overlay -> integrity -> action; integrity ПРОВЕРЯЕТ final==max(base,overlay(rule)).
  - I8 measured-not-intended context keys (ведущий-домен измерен НЕ-HOST -> строка на HOST мимо):
    «divergence -> measured context -> row key» — часть плана.

============================================================
LEG 4 — Grok (xAI/Grok) — 3-е семейство; подтверждающая
============================================================
VERDICT: план верен, NOT LOOPHOLE. SELECT I2a; CUT I2b/I2c; инкремент-1 = BOM ONLY, ZWJ Z5 отложен.
  Скелет конвергентный. I-OTHER: HONEST_PENDING_SURFACE (Z5 pending не должен выглядеть «done»:
  O1_STATUS: PENDING_SCRIPT_CONTEXT в карте; отсутствие rule_id = «политика не применена», не «CLEAN»).
СЛАБЕЕ Kimi по двум пунктам:
  1. OVER-DEFER ZWJ: инкремент-1 = BOM only; весь ZWJ отложен. Не подхватила machine-string Kimi.
     [ПРИМЕЧАНИЕ: атака-симуляция F1 подтвердила — Grok здесь оказался ПРАВ (ZWJ отложить), но по
      правильной причине измерения, а не по разбору аргумента Kimi.]
  2. Ключует ведущий-BOM на HOST: «BOM x HOST (leading) -> HIGH». Но tuple-probe измерил ведущий-домен
     BOM как HIDDEN_BOUNDARY_PADDING, НЕ HOST -> строка Grok = МЁРТВАЯ СТРОКА (row-liveness/measured-
     context-key Kimi поймали бы). Конкретный экземпляр дыры «задуманный-vs-измеренный контекст».
  Не отметила confluence-дыру.

============================================================
LEG 5 — Gemini (Gemini) — 4-е семейство; подтверждающая
============================================================
VERDICT: план верен, NOT LOOPHOLE. SELECT I2a; инкремент-1 = BOM only (контекст-выводимые); ZWJ Z5
  отложен PENDING_SCRIPT_CONTEXT. Всё PASS, конвергентно. Добавляет: пометить эскалированный dict
  (o1_escalated=True), чтобы _integrity_check считал подъём консистентным. Report-поле {base,final,
  rule_id,provenance}. Не подхватила machine-string Kimi, confluence-дыру, measured-context-key.
  Подтверждающая (как другие ноги Gemini — высокоуровнево, не код-обоснованно).

============================================================
СВОД КООРДИНАТОРА против RAW (5 ног, 4 семейства: OpenAI x2, Moonshot, xAI, Gemini)
============================================================
UNANIMOUS SKELETON (5/5): O1 = аддитивный per-occurrence overlay, хук ПОСЛЕ base-risk (RiskLevel enum,
  НЕ сериализованный risk.value — нога 1), ДО action-map; читает ТОЛЬКО готовые поля dict, НИКОГДА не
  зовёт _detect_context_at; монотонный final=max(base,overlay), raise-only, absence=identity; спарс-
  реестр по CODEPOINT sign_id (не имя/visible_form), provenance-ID, линт (ZWSP/wildcard/class/CRITICAL/
  no-provenance/lower/non-computable-role — все FAIL); severity ТОЛЬКО в реестре (карта = словарь ролей);
  РЕАЛЬНАЯ=HIGH->hold (без CRITICAL/escalate); integrity видит final + проверяет final==max(base,
  overlay(rule)) (инвариант объяснимости, маркер O1_RAISE/o1_escalated); audit-поле {base,final,rule_id,
  provenance} ТОЛЬКО если строка сработала, НЕ второй канал решения; delta-census = OFF-vs-ON diff,
  tuple-level, exact-match, ZWSP delta=0, + mutation-adequacy + O1-мутации; I2b flat CUT, I2c script-
  proxy CUT; ZWJ Z5 отложен до script-контекста (v0.5), честно PENDING в карте.
KIMI-UNIQUE, HIGH-VALUE (ни пара OpenAI, ни Grok/Gemini не имели):
  - CONFLUENCE COVERAGE (хук в точке слияния всех вердикт-путей) + ROW-LIVENESS + NEGATIVE SPACE.
  - MEASURED-not-intended context keys.
AUTHOR-OPEN FORKS (ИЗМЕРИМЫ -> атака-симуляция per RULE_DESIGN_ADVERSARIAL_SIM, ДО author decision):
  F1. ZWJ x {token,email} scope: Kimi (1) — доставляемо СЕЙЧАС; OpenAI x2 + Grok + Gemini (4) — отложить.
  F2. BOM ведущий-домен context key: измерен HIDDEN_BOUNDARY_PADDING, не HOST.
  F3. Ведущий-BOM эскалация: нога 1 (UNVERIFIABLE) vs нога 2/Grok/Gemini/Kimi (доставляемо).
  F4. Confluence coverage (Kimi): есть ли вердикт-пути помимо relation_verdicts для BOM/ZWJ?

============================================================
АТАКА-СИМУЛЯЦИЯ (RULE_DESIGN_ADVERSARIAL_SIM) — на живом ядре. РАЗРЕШАЕТ развилки, ПЕРЕВОРАЧИВАЕТ 2 ноги.
Замер бьёт голос. Сам зонд под claim=evidence — исходник зонда вложен ниже, воспроизводим.
============================================================
F1 — ZWJ x token/email (расширение Kimi) -> СРЕЗАНО ЗАМЕРОМ:
  user<ZWJ>name -> BYTE_EXACT_TOKEN; ab<ZWJ>cd_ef -> BYTE_EXACT_TOKEN; us<ZWJ>er@ex.com -> EMAIL;
  *** می<ZWJ>خواهم (легит ПЕРСИДСКОЕ слово, Z3) -> BYTE_EXACT_TOKEN *** (ТОТ ЖЕ контекст, что у ASCII-
  токена); می<ZWJ>خواهم@ex.com (арабский local-part) -> EMAIL.
  => контексты рантайма BYTE_EXACT_TOKEN / EMAIL НЕ различают ASCII машинный идентификатор от легит
  арабского/персидского слова. Правило «ZWJ x BYTE_EXACT_TOKEN -> HIGH» эскалировало бы ЛЕГИТ персидское
  «می‍خواهم» (Z3) = ЛОЖНОЕ СРАБАТЫВАНИЕ. «Machine string = redundant always» Kimi верно в абстракции, но
  НЕВЕРНО про рантайм (он сворачивает арабские слова в тот же token/email контекст). => ZWJ x {token,
  email} НЕ безопасно эскалировать. РАСШИРЕНИЕ KIMI СРЕЗАНО. 4 консервативные ноги ПОДТВЕРЖДЕНЫ замером.
F2 — BOM ведущий-домен context key -> измерен HIDDEN_BOUNDARY_PADDING (НЕ HOST). Строка Grok
  «BOM x HOST(leading)» — МЁРТВАЯ. Ключевать по измеренному контексту (Kimi I8 / GPT правы).
F3 — ведущий-BOM эскалация -> ОТЛОЖИТЬ (нога 1 подтверждена). Ведущий BOM (offset 0) = HIDDEN_BOUNDARY_
  PADDING, и на offset 0 он МОЖЕТ быть легит transport stream-start BOM -> неоднозначно без ingress-
  метаданных. Внутренний BOM (offset>0: mid-host HOST, mid-token/email) ОДНОЗНАЧЕН (BOM никогда не легит
  в середине потока, ЛЮБОЙ script — в отличие от ZWJ, у BOM нет joining-роли). => эскалировать ТОЛЬКО
  внутренний BOM; ведущий-домен BOM отложить в инкремент-2 (ingress-aware, пункт ноги 1).
F4 — confluence coverage -> НИЗКАЯ для этих знаков. BOM/ZWJ: relation_verdicts(sign)=3,
  single_sign_risky(sign)=0 -> риск только через relation_verdicts. Хук в _assess_relation_risk покрывает
  BOM/ZWJ полностью. Тревога Kimi = хорошая ОБЩАЯ заметка плана, но для инкремента-1 хук достаточен.

СКОРРЕКТИРОВАННАЯ РАМКА (замер-обоснованная): occurrence_role выводим из ПРИРОДЫ ЗНАКА + ПОЗИЦИИ, не из
  «контекста». BOM: внутри(offset>0)=всегда application (BOM никогда не легит в середине потока) ->
  эскалация; ведущий(offset 0)=неоднозначный transport -> отложить. ZWJ: НЕ выводим (легит в середине
  арабского; рантайм не отличает арабский от ASCII) -> отложить целиком.

============================================================
ФИНАЛЬНЫЙ СВОД (5 ног, 4 семейства + атака-симуляция). ИНКРЕМЕНТ-1 = ТОЛЬКО ВНУТРЕННИЙ BOM.
============================================================
INCREMENT-1 SCOPE (разрешено атака-симуляцией -> нога 1 подтверждена, НЕ Kimi/нога2/Grok/Gemini):
  = ВНУТРЕННИЙ BOM only (offset>0): BOM x {BYTE_EXACT_TOKEN, EMAIL, HOST(mid)} -> HIGH.
    (3 ячейки reconcile: token, ident, email — все внутренние.)
  ОТЛОЖИТЬ в инкремент-2: BOM ведущий-домен (offset 0, неоднозначный transport, нужны ingress-
    метаданные); ВЕСЬ ZWJ (Z4/B3/Z5 — рантайм не отделяет арабский от машинного); script-контекст (v0.5).
  => инкремент-1 доставляет 3 из 7 ячеек reconcile — ЕДИНСТВЕННЫЕ, что замер доказал безопасными.
  Честно МЕНЬШЕ, чем оценка любой ноги (Kimi 6, нога2/Grok/Gemini 4, нога 1 ~3-4). Замер — это пол.
KEY LESSON (для канона): атака-симуляция ПЕРЕВЕРНУЛА и самую острую адверсариальную ногу (Kimi
  перерасширила ZWJ), И мягкие ноги (перевключили ведущий-BOM), приземлив на консервативную позицию
  ноги 1 — которую доказал только замер. Схождение/острота != правота; арбитр — измерение. Учебный
  RULE_DESIGN_ADVERSARIAL_SIM.
AUTHOR-OPEN (небольшой): (а) подтвердить инкремент-1 = только-внутренний-BOM (форсировано замером);
  (б) общую заметку confluence-coverage — принять как требование плана (хоть для BOM/ZWJ она низкая).

============================================================
ЗОНД АТАКА-СИМУЛЯЦИИ (исходник; claim=evidence — воспроизводим копипастом; НЕ живой тест репо,
  чтобы не тащить кириллицу/арабский в .py под english-only гейт). Прогнан на живом ядре, вывод — выше.
============================================================
```python
# -*- coding: utf-8 -*-
"""Attack-sim the measurable O1-IMPL forks on the live core (RULE_DESIGN_ADVERSARIAL_SIM).
F1: is ZWJ x token machine (Kimi: redundant-always) AND does ZWJ x email risk FP on
    internationalized Arabic local-parts (my caveat: email != always machine)?
F2: leading-domain BOM measured context (HIDDEN_BOUNDARY_PADDING vs HOST for the row key).
F4: for BOM/ZWJ, does risk come ONLY via relation_verdicts (hook there covers) or other paths?
"""
import os, sys, io, contextlib
os.environ["MSL_MIP_HERMETIC_TLD"]="1"
BASE=r"C:\Users\malya\OneDrive\Desktop\msl_mip_final"
for p in ("core","single_sign","sequence"): sys.path.insert(0, os.path.join(BASE,p))
sys.path.insert(0, BASE)
import msl_mip_runtime as rt
from load_card import load_card
from sequence_engine import _force_tld_state_for_test
_force_tld_state_for_test(frozenset({"com","org","net","ru","io","dev","xn--p1ai"}), False)
MASK=load_card(os.path.join(BASE,"cards","SIGN_CORE_CARD_FULLWIDTH_SOLIDUS_UFF0F_GEN3_v0_3_RU.md"))
ZWJ_C=load_card(os.path.join(BASE,"cards","SIGN_CORE_CARD_ZERO_WIDTH_JOINER_U200D_GEN3_v0_1_RU.md"))
BOM_C=load_card(os.path.join(BASE,"cards","SIGN_CORE_CARD_BYTE_ORDER_MARK_UFEFF_GEN3_v0_1_RU.md"))
ZWJ="‍"; BOM="﻿"

def dump(text, sign, cards):
    with contextlib.redirect_stdout(io.StringIO()): rep=rt.analyze(text,cards)
    rv=[v for v in rep["sequence_output"].relation_verdicts if v["visible_form"]==sign
        and v.get("relation_type")=="BOUNDARY_DISRUPTOR"]
    ctx=rv[0]["detected_context"] if rv else "-"
    risk=str(rv[0]["risk_level"]) if rv else "-"
    return ctx, risk, rep["effective_action"], rep.get("semantic_action")

# F1 -- ZWJ x token vs email vs ARABIC email local-part (Kimi machine-string claim)
ZC=[ZWJ_C, MASK]
for nm,t in [("ZWJ ascii-token",  "user"+ZWJ+"name"),
             ("ZWJ ascii-ident",  "ab"+ZWJ+"cd_ef"),
             ("ZWJ ascii-email",  "us"+ZWJ+"er@example.com"),
             ("ZWJ ARABIC-email", "می"+ZWJ+"خواهم@example.com"),
             ("ZWJ ARABIC-token", "می"+ZWJ+"خواهم")]:
    ctx,risk,eff,sem=dump(t,ZWJ,ZC)
    print("  %-18s ctx=%-20s risk=%-6s eff=%s" % (nm,ctx,risk,eff))

# F2 -- BOM leading-domain measured context (row key: HIDDEN_BOUNDARY_PADDING vs HOST)
BC=[BOM_C, MASK]
for nm,t in [("BOM leading+domain", BOM+"paypal.com"),
             ("BOM mid-host",       "pay"+BOM+"pal.com"),
             ("BOM token",          "bad"+BOM+"word"),
             ("BOM email",          "us"+BOM+"er@example.com")]:
    ctx,risk,eff,sem=dump(t,BOM,BC)
    print("  %-18s ctx=%-24s risk=%-6s eff=%s" % (nm,ctx,risk,eff))

# F4 -- does BOM/ZWJ risk come ONLY via relation_verdicts (hook there covers)?
for nm,t,sign,cards in [("BOM mid-host","pay"+BOM+"pal.com",BOM,BC),
                        ("ZWJ latin-host","goog"+ZWJ+"le.com",ZWJ,ZC)]:
    with contextlib.redirect_stdout(io.StringIO()): rep=rt.analyze(t,cards)
    nrel=len([v for v in rep["sequence_output"].relation_verdicts if v["visible_form"]==sign])
    ss_risky=0
    for s in rep.get("single_sign_results", []):
        st = s[0] if isinstance(s,tuple) else s
        try:
            if getattr(st,"sign_codepoint","")==("U+%04X"%ord(sign)) and str(getattr(st,"risk_level",""))!="RiskLevel.NONE":
                ss_risky+=1
        except Exception: pass
    print("  %-16s relation_verdicts(sign)=%d  single_sign_risky(sign)=%d  eff=%s" %
          (nm, nrel, ss_risky, rep["effective_action"]))
```

============================================================
EXIT
============================================================
Скелет плана сошёлся (5/5). Развилки I2/I7 разрешены АТАКА-СИМУЛЯЦИЕЙ (не голосом): инкремент-1 =
  только-внутренний-BOM (3 ячейки). Материал под AUTHOR_DECISION по ПЛАНУ реализации O1. КОД ЗАБЛОКИРОВАН
  до author decision. ZWSP не трогать (план говорит КАК ре-валидировать через delta-census).
FORK_STATUS: OPEN — PENDING_AUTHOR_DECISION (план реализации O1). Два открытых пункта автору (а),(б).

END_OF_RAW_REVIEW_BUNDLE
