ЧАСТНЫЙ АВТОРСКИЙ ПРОЕКТ / COMMERCIAL USE PROHIBITED

DOCUMENT_ID: RAW_REVIEWS_O1_IMPL_SCOPE_2026-07-21
DOCUMENT_TYPE: RAW_REVIEW_BUNDLE + COORDINATOR_SVOD + ATTACK_SIM (сверяемый источник; НЕ author decision)
DATE: 2026-07-21
PACKET: CONVEYOR_PACKET_O1_IMPL_SCOPE_2026-07-21 (объём и этапность инкремента-1 O1 ДО кода)
STATUS: RECORD. Author decision по объёму — ОТДЕЛЬНЫЙ заход. Здесь решений НЕТ.
NOTE: полные вербатим-ответы ног — в транскрипте сессии; здесь сжатая, но сверяемая запись каждой
  ноги + свод против raw + две атака-симуляции на живом ядре (per RULE_DESIGN_ADVERSARIAL_SIM).
  ПОРЯДОК КАНОНА СОБЛЮДЁН: независимый зонд B прогнан ДО конвейера (16:44), пакет ушёл в конвейер
  (16:49) уже на измеренном грунте; опорный зонд M1 — на своде (16:59). Замер до И после голосов.

============================================================
СОСТАВ НОГ (4 ноги, 3 самостоятельных семейства; строгие >=3 выполнено)
============================================================
LEG 1 — GPT-5.5 / Codex (OpenAI reasoning). Код-обоснованная (file:line). «3 роли» = ОДИН голос.
LEG 2 — GPT-5.6 Thinking (OpenAI GPT). ТО ЖЕ семейство, что нога 1. Строже: даже email не активен.
LEG 3 — Qwen (Qwen). ИНОЕ семейство (2-е). Подтверждающая; инкремент-0-only; новых дыр нет.
LEG 4 — Kimi K3 (Moonshot-Kimi). ИНОЕ семейство (3-е). ОСТРАЯ: оспорила консенсус из witness-рамки;
        сняла собственную позицию прошлого круга под давлением ФАКТА-1.
Rule provenance: OpenAI x2 = ОДНО семейство (схождение != независимость); Qwen; Moonshot-Kimi.

СУБСТРАТ КРУГА (измерено зондом B ДО конвейера — данные, не на голосование):
  ФАКТ-1: легит персидские слова с серединным ZWJ → BYTE_EXACT_TOKEN (как ASCII-токены) → ZWJ отложить.
  ФАКТ-2: база БЕЗ O1 уже: BOM mid-host → HIGH/hold; token/email → MEDIUM/queue. Host = O1 no-op.
  ФАКТ-3: concat-BOM между не-пробельными → BYTE_EXACT_TOKEN/MEDIUM (безобидный путь в эскалируемый ctx).

============================================================
LEG 1 — GPT-5.5 / Codex (OpenAI reasoning)
============================================================
VERDICT: ACCEPT_WITH_NARROWING. O1-идея + шов ВЕРНЫ (не LOOPHOLE). Исходный token+email = LOOPHOLE
  по token. Рекомендация: INCREMENT-0 (пустой движок + zero-delta) → INCREMENT-1 = ТОЛЬКО BOM×EMAIL→HIGH
  (если автор примет, что split email-local-part структурен и достоин hold) + email FP-бюджет.
CONFIRMS субстрат B статическим чтением репо (не доверяя зонду):
  _SCOPE_RISK: HOST=HIGH, EMAIL=MEDIUM, BYTE_EXACT_TOKEN=MEDIUM, FREE_TEXT=NONE (sequence_engine.py:653-670);
  манифест B2 host HIGH/hold, B3 email MEDIUM/queue, B4 token MEDIUM/queue (zwj_bom_manifests.py:95-107);
  комментарий BYTE_EXACT_TOKEN «no-space word, can't tell keyword vs identifier» (653-657);
  ZWJ PER_OCCURRENCE_BOUNDARY + манифест запрещает hold для персидского Z3 (36-42).
ПО ИЗМЕРЕНИЯМ: C1 инкремент-0 first → email-only (token+email blanket валит r>g); C2 host base HIGH/
  O1 no-op, email можно поднять узко, token НЕ поднимать; C3 шов верен, НЕ интегратор (теряет per-
  occurrence), НЕ карта (_SCOPE_RISK не править); C4 инкремент-0 ДА; C5 confluence — предусловие-гейт.
  C-OTHER-1: линт должен ЛОВИТЬ no-op правила (host как «победа» без дельты = обман учёта).
  C-OTHER-2: отсутствие правила = applied=false/NO_ACTIVE_RULE_DEFERRED, НЕ clean. C-OTHER-3: token —
  только с дискриминатором (machine token vs concat vs identifier vs слово), не голосом.

============================================================
LEG 2 — GPT-5.6 Thinking (OpenAI GPT; ТО ЖЕ семейство)
============================================================
VERDICT: SCOPE_SURVIVES_ONLY_AFTER_BEHAVIORAL_REDUCTION. Дизайн VALID, NO LOOPHOLE. SELECT_C1 =
  OPTION_B (движок, отложить ВСЕ поведенческие правила). FIRST_CODE = INCREMENT_0. ACTIVE_RULES = NONE.
DELTA к ноге 1 (строже по email): нога 1 — email опционально-активен; нога 2 — email КАНДИДАТ, не
  активен, до отдельного benign-path аудита. Ключевая строка: «отсутствие показанного benign-примера
  != доказательство, что его нет» → активировать email лишь потому, что я не показал benign — необоснованно.
  (Это ровно новая измеримая развилка, что я пометил после ноги 1; нога 2 сделала её БЛОКЕРОМ активации.)
ПО ИЗМЕРЕНИЯМ: host CUT (base=overlay=final=HIGH, растит реестр/desync/аудит без r); token→hold NO
  (concat-коллизия; «anomalous != almost certainly harmful»); email→hold NOT YET (нужен полный
  benign-path аудит: валид/невалид Unicode local-parts, copy-from-doc, CSV-импорт, BOM-after-decode,
  валидатор vs runtime-context, точная дельта queue→hold). Шов назвать RELATION_PATH_O1_HOOK_v0_1, не
  заявлять all-paths-covered. C5 — машинно-проверяемый TARGET_SIGN_RISK_PATH_CENSUS (CI ломается при
  изменении без одобренного confluence-манифеста). MINIMUM_USEFUL_DELTA_RULE (6 условий активации):
  host FAILS #1,#2 (CUT); token FAILS #3 (DEFER); email #3 не установлен (CANDIDATE); ZWJ FAILS #3.
  POLICY_CANDIDATE реестр с честными блокерами: BOM_HOST=NOT_NEEDED; BOM_TOKEN=DEFERRED_PREDICATE_
  COLLISION; BOM_EMAIL=EVIDENCE_REQUIRED_BENIGN_PATH_AUDIT; ZWJ=DEFERRED_SCRIPT_ROLE.

============================================================
LEG 3 — Qwen (Qwen; ИНОЕ семейство, 2-е)
============================================================
VERDICT: план объёма VERIFIED (с коррекцией на инкремент-0), NOT LOOPHOLE. SELECT_C1 = (b) Нет —
  отложить правила инкремента-1; минимально-полезное = ИНКРЕМЕНТ-0. Все шесть критериев по каждому
  измерению — VERIFIED. Иное семейство НЕЗАВИСИМО пришло к инкременту-0-only.
СХОДИТСЯ с ногой 2: отложить token И email; ноль активных правил; host CUT (уже HIGH); шов верен;
  confluence — предусловие-гейт (single_sign_risky>0). C2: token+email = ПЕРЕ-эскалация, оставить
  MEDIUM/queue («MEDIUM = посмотри при случае, идеально для редкого безобидного артефакта»; против
  alarm fatigue). Host безопасен (склейку в имя хоста не вставить).
ПРИМЕЧАНИЕ: Qwen НЕ заострил email benign-path (ход ноги 2) — просто отложил email вместе с token.
  Подтверждающий вес, не новый зонд. (Манера Qwen: в input-guard круге был выбросом G3c, тут — в мейнстриме.)

============================================================
LEG 4 — Kimi K3 (Moonshot-Kimi; ИНОЕ семейство, 3-е) — ОСТРЫЙ НОЖ
============================================================
ПРЕАМБУЛА (честность по канону): Kimi СНИМАЕТ своё расширение прошлого круга (ZWJ×{token,email}).
  ФАКТ-1 опроверг её «машинная строка = контекст сам предикат»: персидские слова схлопнуты в тот же
  BYTE_EXACT_TOKEN. «Замер бьёт голос — включая мой.» Принимает ZWJ отложенным. (Самокоррекция усиливает доверие.)
VERDICT: план объёма VERIFIED, NOT LOOPHOLE. Но C1 = (a) ДА С ПРАВИЛАМИ, не инкремент-0-only.
  Инкремент-1 = BOM×{BYTE_EXACT_TOKEN, EMAIL}→HIGH (+ведущий домен R3 после замера его контекста), НА
  шве инкремента-0. (b) инкремент-0-only = runner-up, НЕ cut. (c) email-only = CUT (режет token — первичную поверхность).

*** РАСКОЛ (та самая развилка, ради которой конвейер) ***
  3 ноги (OpenAI x2 + Qwen) → инкремент-0-only, отложить token И email. Рамка: token/email→hold =
    ПЕРЕ-эскалация, потому что concat-BOM — безобидный путь.
  Kimi → инкремент-0, ПОТОМ правила token+email. Рамка: безобидный concat-BOM, дошедший до HOLD — НЕ
    ложная тревога. Назвать его «FP» можно только в АНТИВИРУСНОЙ рамке (тревога=обвинение). В witness-
    рамке тревога = ПОКАЗ ФАКТА С ПРИОРИТЕТОМ. Безобидный concat-BOM ИНФОРМАТИВЕН («ваша склейка тащит
    невидимку в токен — дефект гигиены конвейера»), а не шум.
  АРГУМЕНТЫ KIMI (острые, из рамки проекта):
    - queue vs hold = ПРИОРИТЕТ внимания человека, не «сейчас vs никогда». «Человек и так смотрит»
      путает очередь-на-потом (атака лежит ВЕЧНО) с очередью-по-приоритету.
    - АСИММЕТРИЯ ЦЕНЫ: ложный hold = ОДИН взгляд (не блок — witness, последнее слово за человеком).
      Недо-тревога на ИЗВЕСТНОМ векторе (ghost-токен, обход allowlist, filter evasion = reconcile B3)
      = атака в очереди бессрочно. Недо-тревога для свидетеля хуже. (То же направление ошибки, что I2c.)
    - token — ПЕРВИЧНАЯ поверхность (ghost-токены/allowlist). Резать её ради редкого информативного FP
      = «кастрация инкремента». Цена слоя одноразовая (APPROVED), цена СТРОКИ — данные.
  МЕХАНИЗМ ЧЕСТНОСТИ: KNOWN_FP в provenance строки; FP-бюджет на benign-корпусе С concat-кейсами;
    аудит-поля дают будущему deriver'у (энтропия/словарь) уточнить ячейку без переделки слоя. email→hold:
    benign-путь не измерен, помечен «plausible, unmeasured» (concat контакт-листов контекстно-слеп).
  C4 инкремент-0: ДА (КОНТРОЛЬНЫЙ ОПЫТ — атрибутирует дельту инкремента-1 СТРОКАМ, не шву).
  C5 confluence: предусловие через ROW-LIVENESS (её план-круг I3): строка обязана СРАБОТАТЬ на своём
    reconcile-входе; знак, чей риск минует шов → liveness FAIL громко. Покрытие ПО-ЗНАКОВО при добавлении
    строки, не оптом. Ноль g сверх уже запланированного. (Kimi УТОЧНЯЕТ свой план-круг I1 замером — опять самокоррекция.)
  C7 честность отсутствия: «правило применено и не сработало» != «правила нет». ZWJ = NOT_APPLIED
    (PENDING_SCRIPT_CONTEXT), не clean.
  R3 ведущий домен: HIGH только после замера его контекста. [КООРДИНАТОР: план-круг F2 УЖЕ измерил его =
    HIDDEN_BOUNDARY_PADDING, НЕ BYTE_EXACT_TOKEN → R3 в R1 НЕ сворачивается, отдельная отложенная ячейка.]

============================================================
СВОД-ЗАМЕР (RULE_DESIGN_ADVERSARIAL_SIM) — на своде, живое ядро. Разрешает опорную развилку.
============================================================
M1 — BOM×EMAIL ИМЕЕТ ЧАСТЫЙ безобидный путь (РЕШАЮЩЕЕ): 6/6 правдоподобно-безобидных email-входов →
  EMAIL/MEDIUM (paste-from-doc, склейка двух адресов, CSV-ячейка ведущий/внутренний BOM, mailto в прозе,
  блок подписи). Правило «BOM×EMAIL→HIGH» подняло бы ВСЕ ШЕСТЬ в hold. И это не экзотика: CSV/Excel-
  экспорты штатно несут BOM. => email benign-путь ЧАСТЫЙ (не редкий). (a) опровергает ногу 1 «email чист»;
  (b) подтверждает ноги 2+Qwen «отложить email»; (c) подрезает Kimi (её «частота ниже token» ложна).
  => ПРАВИЛО EMAIL — ВОН ПО ЗАМЕРУ.
M3 — ведущий домен BOM = HIDDEN_BOUNDARY_PADDING (оба кейса), MEDIUM. Не BYTE_EXACT_TOKEN. => R3 в R1 не
  сворачивается, отдельная отложенная ячейка (совпадает с F2). Ведущий домен — не в инкременте-1.
M2 — частота concat-BOM для TOKEN: НЕ измерена (нужен корпус). ФАКТ-3 показал СУЩЕСТВОВАНИЕ; «редко»
  Kimi для token — ДОПУЩЕНИЕ, не мой замер. Для email M1 показал: benign частый → «редкость» Kimi для
  email ложна, для token держится слабо.

============================================================
ФИНАЛЬНЫЙ СВОД (4 ноги, 3 семейства + свод-замер). 5 ячеек свернулись до ОДНОГО авторского решения.
============================================================
РЕШЕНО (замер + схождение — НЕ открыто):
  - ИНКРЕМЕНТ-0 первым (пустой шов + zero-delta гейт): ЕДИНОГЛАСНО 4/4. Делать в любом случае.
  - HOST: правила нет — база уже HIGH (ФАКТ-2), правило = no-op. Единогласно + замер. CUT.
  - EMAIL (R2): ВОН ПО ЗАМЕРУ — M1 показал частый безобидный путь (6/6).
  - ZWJ: отложить целиком — ФАКТ-1. Единогласно + замер + Kimi сняла своё расширение. NOT_APPLIED, не clean.
  - ВЕДУЩИЙ ДОМЕН: отдельная отложенная ячейка (HIDDEN_BOUNDARY_PADDING, M3/F2).
  - CONFLUENCE: предусловие-ГЕЙТ (не полный аудит, single_sign_risky=0), через ROW-LIVENESS (заточка Kimi).
  - ШОВ: _assess_relation_risk после base_risk-enum, до сериализации. Единогласно, не LOOPHOLE.
    Имя RELATION_PATH_O1_HOOK_v0_1, без заявки all-paths-covered.
  - ЧЕСТНОСТЬ-ПЛУМБИНГ (принять): MINIMUM_USEFUL_DELTA_RULE (нога 2); линт no-op правил (нога 2);
    отсутствие=NOT_APPLIED не clean (нога 2+Kimi C7); KNOWN_FP в provenance (Kimi).

ЕДИНСТВЕННОЕ НЕСВОДИМОЕ АВТОРСКОЕ РЕШЕНИЕ (замер информировал, решить не может):
  TOKEN: BOM×BYTE_EXACT_TOKEN → HIGH/hold — ДА (Kimi) или НЕТ/оставить MEDIUM (OpenAI x2 + Qwen)?
  - Ценностный вопрос о witness-рамке, не факт рантайма: безобидно-аномальный BOM в hold — это FP, которого
    надо избегать (alarm-fatigue), или ИНФОРМАТИВНАЯ находка, показанная по приоритету?
  - Замер сузил: token benign-путь (concat) РЕЖЕ, чем email (M1 убил email; token выжил, т.к. concat-mid-
    word нечаст). Аргумент Kimi «редкий информативный FP» применим ИМЕННО к token — там, где после замера ещё жив.
  - Стержень — ЗНАНИЕ АВТОРА: queue_for_review — живая очередь-на-разбор (тогда MEDIUM уже свидетельствует
    → оставить MEDIUM, OpenAI/Qwen) или свалка, где атака лежит вечно (тогда «в очереди навсегда» Kimi → hold
    даёт приоритет)? Модели этого не знают — Руслан знает. Потому решение ЕГО.
  - ЗАПАСНОЙ у ОБЕИХ сторон: если token отложить, инкремент-1 = инкремент-0-only (движок+гейт, ноль правил) —
    когерентное, честное, отгружаемое состояние (runner-up (b) Kimi = (a) трёх ног).

РЕКОМЕНДАЦИЯ КООРДИНАТОРА (честно): замер закрыл 4 из 5 ячеек и оба процессных вопроса. Инкремент-0 —
  единогласен, СТАРТ С НЕГО в любом случае. Token — единственная живая развилка, упирается в «очередь —
  приоритет или свалка». Если неясно → отгрузить инкремент-0-only, token решить ПОСЛЕ доказанно-инертного шва
  + замеренного token FP-бюджета на benign-корпусе. Откладывает трудный вызов до момента дешевле/информативнее.

============================================================
ЗОНД B (независимый; прогнан ДО конвейера — субстрат §1 пакета). claim=evidence, воспроизводим.
============================================================
```python
# -*- coding: utf-8 -*-
# INDEPENDENT re-verification of the O1-IMPL Q1 measurement (claim=evidence).
# V1: legit medial-ZWJ Persian words vs ASCII token -> same context? (multiple words, not a fluke)
# V2: concat-BOM (legit transport artifact mid-buffer) -> which context?
# V3: the 3 increment-1 contexts (internal BOM token/email/mid-host) -> NOT FREE_TEXT?
import os, sys, io, contextlib
os.environ["MSL_MIP_HERMETIC_TLD"] = "1"
BASE = r"C:\Users\malya\OneDrive\Desktop\msl_mip_final"
for p in ("core", "single_sign", "sequence"):
    sys.path.insert(0, os.path.join(BASE, p))
sys.path.insert(0, BASE)
import msl_mip_runtime as rt
from load_card import load_card
from sequence_engine import _force_tld_state_for_test
_force_tld_state_for_test(frozenset({"com","org","net","ru","io","dev","xn--p1ai"}), False)
CARD = lambda n: load_card(os.path.join(BASE, "cards", n))
MASK  = CARD("SIGN_CORE_CARD_FULLWIDTH_SOLIDUS_UFF0F_GEN3_v0_3_RU.md")
ZWJ_C = CARD("SIGN_CORE_CARD_ZERO_WIDTH_JOINER_U200D_GEN3_v0_1_RU.md")
BOM_C = CARD("SIGN_CORE_CARD_BYTE_ORDER_MARK_UFEFF_GEN3_v0_1_RU.md")
ZWJ = "‍"; BOM = "﻿"
def ctx_of(text, sign, cards):
    with contextlib.redirect_stdout(io.StringIO()):
        rep = rt.analyze(text, cards)
    vs = [v for v in rep["sequence_output"].relation_verdicts if v["visible_form"] == sign]
    return sorted({v["detected_context"] for v in vs}), sorted({str(v["risk_level"]) for v in vs}), rep["effective_action"]
# V1
ZC = [ZWJ_C, MASK]
for w in ["می"+ZWJ+"خواهم", "نمی"+ZWJ+"دانم", "می"+ZWJ+"روم"]:
    print("persian", ctx_of(w, ZWJ, ZC)[:2])
for t in ["user"+ZWJ+"name", "api"+ZWJ+"key", "id"+ZWJ+"42"]:
    print("ascii  ", ctx_of(t, ZWJ, ZC)[:2])
# V2 concat-BOM
BC = [BOM_C, MASK]
print("concat ", ctx_of("first file line one\nsecond paragraph"+BOM+"joined file starts here", BOM, BC))
# V3
for nm, t in [("token","bad"+BOM+"word"), ("email","us"+BOM+"er@example.com"), ("host","pay"+BOM+"pal.com")]:
    print(nm, ctx_of(t, BOM, BC))
```
РЕЗУЛЬТАТ B: V1 persian и ascii ОБА → BYTE_EXACT_TOKEN (ФАКТ-1 подтверждён 3 словами); V2 concat →
  BYTE_EXACT_TOKEN/MEDIUM (ФАКТ-3); V3 token→BYTE_EXACT_TOKEN/MEDIUM, email→EMAIL/MEDIUM, host→HOST/HIGH (ФАКТ-2).

============================================================
ЗОНД M1/M3 (свод; опорная email-развилка). claim=evidence, воспроизводим.
============================================================
```python
# -*- coding: utf-8 -*-
# SVOD attack-sim: does BOM x EMAIL have a BENIGN path (like token's concat)? + M3 leading-domain ctx.
import os, sys, io, contextlib
os.environ["MSL_MIP_HERMETIC_TLD"] = "1"
BASE = r"C:\Users\malya\OneDrive\Desktop\msl_mip_final"
for p in ("core", "single_sign", "sequence"):
    sys.path.insert(0, os.path.join(BASE, p))
sys.path.insert(0, BASE)
import msl_mip_runtime as rt
from load_card import load_card
from sequence_engine import _force_tld_state_for_test
_force_tld_state_for_test(frozenset({"com","org","net","ru","io","dev","xn--p1ai"}), False)
CARD = lambda n: load_card(os.path.join(BASE, "cards", n))
MASK  = CARD("SIGN_CORE_CARD_FULLWIDTH_SOLIDUS_UFF0F_GEN3_v0_3_RU.md")
BOM_C = CARD("SIGN_CORE_CARD_BYTE_ORDER_MARK_UFEFF_GEN3_v0_1_RU.md")
BOM = "﻿"; BC = [BOM_C, MASK]
def probe(text):
    with contextlib.redirect_stdout(io.StringIO()):
        rep = rt.analyze(text, BC)
    vs = [v for v in rep["sequence_output"].relation_verdicts if v["visible_form"] == BOM]
    return [(v["detected_context"], str(v["risk_level"]), v.get("at_offset")) for v in vs], rep["effective_action"]
# M1 benign email-ish inputs with internal/adjacent BOM
for nm, t in [("paste-from-doc","Contact: us"+BOM+"er@example.com"),
              ("csv-concat","alice@example.com"+BOM+"bob@example.org"),
              ("csv-leading",BOM+"bob@example.com"),
              ("csv-internal","bo"+BOM+"b@example.com"),
              ("mailto-prose","write me"+BOM+"@example.com"),
              ("signature","Jane Doe\nj"+BOM+"doe@example.org")]:
    print(nm, probe(t))
# M3 leading-domain
for t in [BOM+"paypal.com", BOM+"example.org"]:
    print("leading", probe(t))
```
РЕЗУЛЬТАТ M1: 6/6 безобидных → EMAIL/MEDIUM (эскалация в hold задела бы все). M3: ведущий домен →
  HIDDEN_BOUNDARY_PADDING/MEDIUM (не BYTE_EXACT_TOKEN).

============================================================
EXIT
============================================================
Объём сошёлся на инкременте-0 (единогласно). Развилки email/host/ZWJ/ведущий/confluence разрешены
  замером+схождением. ЕДИНСТВЕННОЕ открытое — token (hold vs MEDIUM), ценностное, за автором.
  Материал под AUTHOR_DECISION по объёму. КОД ЗАБЛОКИРОВАН до решения. ZWSP не трогать.
FORK_STATUS: OPEN — PENDING_AUTHOR_DECISION (объём инкремента-1: token hold/MEDIUM; инкремент-0 в любом случае).

END_OF_RAW_REVIEW_BUNDLE
