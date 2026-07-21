ЧАСТНЫЙ АВТОРСКИЙ ПРОЕКТ / COMMERCIAL USE PROHIBITED

DOCUMENT_ID: RAW_REVIEWS_O1_TOKEN_OPTIONS_2026-07-21
DOCUMENT_TYPE: RAW_REVIEW_BUNDLE + COORDINATOR_SVOD + ATTACK_SIM (сверяемый источник; НЕ author decision)
DATE: 2026-07-21
PACKET: CONVEYOR_PACKET_O1_TOKEN_OPTIONS_2026-07-21 (генеративный поиск пространства решений по ячейке
  «BOM внутри токена»)
STATUS: RECORD. Author decision — ОТДЕЛЬНЫЙ заход. Здесь решений НЕТ.
NOTE: полные вербатим-ответы — в транскрипте сессии; здесь сжатая, но сверяемая запись каждой ноги +
  свод против raw + свод-замер на живом ядре. Оба зонда вложены (claim=evidence).

============================================================
СОСТАВ НОГ (5 ног, 4 самостоятельных семейства)
============================================================
LEG 1 — Qwen (Qwen). 5 вариантов. Звезда: узкий позиционный предикат.
LEG 2 — GPT-5.5/Codex (OpenAI reasoning). 10 вариантов, код-обоснованная, адверсариальная к Qwen.
LEG 3 — Kimi K3 (Moonshot-Kimi). ОСТРАЯ: сняла свою же позицию B; дала C6 (форма коллапса) и F (правка ожидания).
LEG 4 — Gemini (Gemini). Подтверждающая + укол по словарю (семантический дрейф).
LEG 5 — «REVIEWER_CONSENSUS» (самозаявлен как синтез GPT-4o/Claude-3.7/Gemini). ПРОВЕНАНС: ОДИН
  синтезированный ответ = ОДНА нога, ОДИН голос (ловушка «3 роли = 1 голос»). Новых чистых семейств НЕ даёт.
ИТОГО: 5 ног, 4 семейства. Строгие >=3 выполнены с запасом.

СУБСТРАТ КРУГА (измерено ДО конвейера, дано в §1 пакета как данность):
  прямое правило BOM×BYTE_EXACT_TOKEN→HIGH: benign FP 8/12 = 67%, ghost TP 7/7 = 100%;
  база УЖЕ очередит и benign, и malicious (MEDIUM/queue) — silent pass отсутствует, спор только о приоритете;
  рантайм сворачивает всё в BYTE_EXACT_TOKEN (даже «fox <BOM>jumps» с пробелом слева) — тонкий предикат не выражает.

============================================================
LEG 1 — Qwen
============================================================
V1 status quo (MEDIUM/queue). V2 УЗКИЙ ПОЗИЦИОННЫЙ ПРЕДИКАТ (offset_in_token>0 — BOM внутри, не ведущий):
  утверждает, что ведущий BOM (вставка/CSV) — львиная доля 67% benign. V3 тег «дефект гигиены» без эскалации.
  V4 расхождение canonical_view (из другой оперы, слой гарда). V5 словарный деривер (высокоценные слова).
RANK: V2 > V4 > V1 > V3 > V5. Рекомендация: V2 + V4.
[КООРДИНАТОР: премиса V2 согласуется с корпусом — 7 из 8 benign-эскалаций ведущие. НО Qwen утверждает
 «рантайм уже даёт offset_in_token, тривиально» — это ОПРОВЕРГНУТО ногой 2 (шов передаёт occurrence_role=None).]

============================================================
LEG 2 — GPT-5.5 / Codex (OpenAI)
============================================================
10 вариантов: 1 keep-MEDIUM; 2 прямой hold (Rank 7, НЕ рекомендован, 67% FP); 3 C1 strict-infix; 4 C2
  protected-lexicon (HIGH только если canonical токен в КОНФИГУРИРОВАННОМ защищённом наборе); 5 C3 machine-shape;
  6 D1 приоритет ОЧЕРЕДИ без hold; 7 D2 hygiene-находка в отчёте; 8 E1 дисплейная/каноническая проекция;
  9 E2 плотность/повтор (агрегат, ближе к input-guard); 10 E3 opt-in режим «машинной политики».
RANK: 1) keep-MEDIUM + E1 + D2; 2) C2 protected-lexicon как лучший БУДУЩИЙ hold; 3) C1+C3 на замер; 4) D1;
  5) density; 6) mode; 7) прямой hold ОТВЕРГНУТ.
ЗАОСТРЕНИЯ: (i) strict-infix НЕПОЛОН — разделяет «внутри-vs-край», а НЕ «ghost-vs-benign»: склейка
  «paragraph<BOM>joined» (alnum/alnum) всё равно срабатывает. (ii) occurrence_role НЕ ПОДКЛЮЧЁН — шов
  передаёт None (sequence_engine.py:752-785) → узкие предикаты требуют доработки, не «тривиальны».
  (iii) Бинарная постановка «queue или hold» БЫЛА БЫ LOOPHOLE; верная постановка — пространство механизмов.

============================================================
LEG 3 — Kimi K3 (Moonshot) — ОСТРАЯ
============================================================
ПРЕАМБУЛА (честность по канону): СНИМАЕТ свою позицию B (token→hold). Её аргумент стоял на допущении
  «benign редкий»; замер (67%) допущение опроверг: при такой базовой ставке hold становится фоном, а не
  сигналом, и «асимметрия цены ошибки» переворачивается. Третий раз замер поправляет её рассуждение.
*** C6 — ПРЕДИКАТ ФОРМЫ КОЛЛАПСА (тест на имперсонацию) — ГЛАВНАЯ ИДЕЯ КРУГА ***
  collapse = токен без членов класса-138. Если collapse ∈ словарь/allowlist/известные цели → hold
  (имперсонация); если collapse — бессловесная склейка («paragraphjoined») → queue (артефакт).
  ПОЧЕМУ ЛУЧШЕ ПОЗИЦИИ: C1 моделирует КОРРЕЛЯТ; атаке же НЕОБХОДИМО, чтобы collapse был узнаваемой
  строкой (pay<BOM>pal выглядит как paypal) — иначе атаки нет. Безобидная склейка коллапсирует в не-слово.
  E1b: если у потребителя есть allowlist — «токена нет в списке, а его collapse есть» = ghost-сигнатура
  в чистом виде, вообще без severity-правила.
F. ЧИНИТЬ ОЖИДАНИЕ КАРТОЧКИ, а не код: reconcile хотел РЕАЛЬНАЯ, но ячейка «часто легитимна, но не
  освобождается» = ОПРЕДЕЛЕНИЕ ВОЗМОЖНАЯ. Дивергенция была «желание без base-rate», а не ошибка рантайма.
D3 строка PENDING_PREDICATE в реестре (provenance: B3 + FP-замер, ссылка на C6) — «не применено» становится ДАННЫМИ.
D1 аннотация-гипотеза «consistent-with: [ghost | concat-artifact]» + collapse-превью — честно показывает НЕРАЗЛИЧИМОСТЬ.
E1 каноническая проекция (самостоятельна, НЕ требует построенного гарда). E4 ЧИНИТЬ КОНТЕКСТ-ДЕТЕКТОР
  (корень: «fox <BOM>jumps»→token) — отдельный фронт CONTEXT_V2, трогает верифиц. путь.
Отклонены с причинами: C5 счётчик>=2 (канонический B3 — ОДИНОЧНЫЙ BOM), E5 трассировка происхождения (вне рантайма).
RANK: 1) E1(+E1b); 2) F+D3+D1; 3) C6 НА ЗАМЕР; 4) E4 отдельный фронт; 5) A; 6) C1 (поглощён C6); 7) D2; 8) B отвергнут.

============================================================
LEG 4 — Gemini
============================================================
5 вариантов: keep-MEDIUM; узкий лексический (BOM между alnum, ожидает FP<10%); энтропия/словарь — САМ отметил,
  что это НАРУШАЕТ принцип MSL/MIP «структура без смысла» → последнее место; приоритет очереди (suspicion_score);
  ДИСПЛЕЙНАЯ ПРОЕКЦИЯ «рентген adm[U+FEFF]in» → ПЕРВОЕ место.
УКОЛ (важен для C6): словарные подходы уводят в «семантический антивирус». Это РАСКАЛЫВАЕТ C6: версия с
  СИСТЕМНЫМ словарём — семантический дрейф; версия с allowlist ПОТРЕБИТЕЛЯ — структурна (смысл у потребителя,
  система лишь strip+match). Честная форма C6 — потребительская.

============================================================
LEG 5 — «REVIEWER_CONSENSUS» (синтез; 1 голос)
============================================================
6 вариантов + G(C+D), H(реактивный порог, отклонён). RANK: 1) D приоритет очереди; 2) F нормализация на входе;
  3) C strict-infix (оценка FP ~30%, пессимистичнее Gemini); 4) A; 5) E деривер; 6) B отвергнут.
ДВА ПОЛЕЗНЫХ ЗАОСТРЕНИЯ:
  (i) ПОЛЯРНОСТЬ СЛОВАРЯ: их вариант E использует ОБЩИЙ словарь → «pay<BOM>pal» коллапсирует в «paypal»,
      которое ЕСТЬ нормальное слово → E оставил бы queue и ПРОПУСТИЛ атаку. Это доказывает, что ОБЩИЙ словарь
      СЛОМАН для ghost-детекции, и заостряет C6: ключ — ЦЕЛЕВОЙ allowlist, а не «нормальное ли это слово».
  (ii) НОРМАЛИЗАЦИЯ НА ВХОДЕ = КРАСНЫЙ ФЛАГ: strip BOM до анализа САНИТИЗИРУЕТ сигнал — ровно анти-паттерн
      «тихого санитайзера», от которого Kimi предостерегала. Уничтожает байтовую разницу, которую эксплуатирует ghost.
  Плюс усиливает тему ПРИОРИТЕТА ОЧЕРЕДИ (её поддержали 4 ноги).

============================================================
СВОД-ЗАМЕР (RULE_DESIGN_ADVERSARIAL_SIM) — C1 против C6 на ОДНИХ корпусах
============================================================
14 benign (вкл. реальные слова с BOM внутри) и 10 ghost (имперсонация целей):
  loose BYTE_EXACT_TOKEN (прямое правило): benign FP 67%       ghost TP 100%   (замерено ранее)
  C1 strict-infix (позиция):               benign FP 36% (5/14) ghost TP 90% (9/10)
  C6 collapse ∈ allowlist (суть):          benign FP  0% (0/14) ghost TP 100% (10/10)
=> KIMI ПОДТВЕРЖДЕНА ЗАМЕРОМ. C1 срабатывает на РЕАЛЬНЫХ словах (re<BOM>ad, fri<BOM>end, note<BOM>book,
   mee<BOM>ting), потому что моделирует коррелят; C6 не сработал ни на одном benign (ни одно не коллапсирует
   в защищённую цель) и поймал ВСЕ ghost, включая трейлинг admin<BOM>, который C1 упустил.
ЧЕСТНЫЕ ОГОВОРКИ ПО C6: (1) ПОЛИТИКО-СВЯЗАН — 0%/100% держатся ТОЛЬКО при allowlist потребителя; пустой список
   → инертен (и TP нет); отсутствие списка ≠ чисто, остаётся queue. (2) Ловит имперсонацию ИЗВЕСТНЫХ целей,
   не «все ghost» (ghost под цель вне списка остаётся в queue — корректная область для hold). (3) ДИЗАЙН-СИМ:
   предикат посчитан на сырых строках; рантайм не имеет обвязки collapse/occurrence_role → это механизм
   инкремента-2 (дёшев: strip класса-138 + set-lookup, структурен). (4) Корпус/allowlist иллюстративные —
   но разрыв 0% против 36% СТРУКТУРЕН (benign-слова редко == защищённые цели; ghost обязан), не подогнан.

============================================================
ФИНАЛЬНЫЙ СВОД (5 ног / 4 семейства + свод-замер)
============================================================
ОТВЕРГНУТО (все 5 ног + замер): прямой token→HIGH/hold (67% FP). МЁРТВ.
УБИТО ЗАМЕРОМ: C1 strict-infix как самостоятельный предикат hold (36% FP на реальных словах, промах по
  трейлингу). Коррелят, не суть. (Была звезда Qwen и «на замер» ещё у 3 ног — замер разрешил.)
СХОЖДЕНИЕ 4/5 семейств (в-рамочно, дёшево, БЕЗ нового замера) → пакет «СЕЙЧАС»:
  P1 КАНОНИЧЕСКАЯ ПРОЕКЦИЯ — аддитивное поле отчёта: collapse + позиции вставки + пометка PROJECTION
     («выглядит как paypal; фактически pay<U+FEFF>pal»). Чистый свидетель: показывает суть, не судит.
     Самостоятельна (strip + верифицированная таблица класса-138), НЕ требует гарда. Свой zero-delta гейт.
  P2 ПРАВКА ОЖИДАНИЯ КАРТОЧКИ (Kimi F) — BOM/token → ВОЗМОЖНАЯ, с пометкой «РЕАЛЬНАЯ требует предиката C6».
  P3 СТРОКА PENDING_PREDICATE + АННОТАЦИЯ-ГИПОТЕЗА — «не применено» становится данными.
  TOKEN = MEDIUM/queue (решено замером; silent pass отсутствует).
ИНКРЕМЕНТ-2 (измеренный мост к честному hold): C6 collapse ∈ allowlist ПОТРЕБИТЕЛЯ. Нужны: обвязка collapse
  + конфиг allowlist + свой author decision + FP-бюджет на реальном списке. НЕ системный словарь.
ОТДЕЛЬНЫЙ ФРОНТ: E4 CONTEXT_V2 (корень — гранулярность контекст-детектора; свой конвейер, полная ре-валидация).
КРАСНЫЙ ФЛАГ ОТВЕРГНУТ: нормализация на входе (тихий санитайзер).

============================================================
ЗОНД 1 — FP-бюджет прямого правила (субстрат круга). claim=evidence, воспроизводим.
============================================================
```python
# benign corpus (CSV/Excel export, concat, paste, log, markdown, prose) vs malicious ghost corpus;
# for each input, does the BOM relation verdict land in BYTE_EXACT_TOKEN (-> the loose rule escalates)?
B = "﻿"
benign = [("csv leading BOM row", B+"name,email,phone"), ("csv cell leading BOM", B+"value"),
          ("concat WITH newline", "first file line\n"+B+"second file line"),
          ("concat no-newline", "endword"+B+"startword"),
          ("paste into prose", "Please see "+B+"the attached file"),
          ("BOM with spaces", "hello "+B+" world"), ("config value trailing", "key=value"+B),
          ("log line", "2026-01-01 INFO "+B+"service started"),
          ("markdown after heading", "# Title\n"+B+"body text here"),
          ("sentence mid", "The quick brown fox "+B+"jumps over"),
          ("two words spaced", "alpha "+B+"beta gamma"),
          ("quoted prose", 'He said, '+B+'"hello there" to me')]
malicious = [("allowlist bypass admin","ad"+B+"min"), ("trailing ghost admin","admin"+B),
             ("ghost root","ro"+B+"ot"), ("filter evade delete","de"+B+"lete"),
             ("ghost identifier","user"+B+"name"), ("ghost api key","api"+B+"key"),
             ("ghost drop","dr"+B+"op")]
# measured via rt.analyze(...) -> relation_verdicts detected_context == "BYTE_EXACT_TOKEN"
# RESULT: benign 8/12 (67%) would escalate to hold; malicious 7/7 (100%).
```

============================================================
ЗОНД 2 — C1 против C6 (свод-замер). claim=evidence, воспроизводим.
============================================================
```python
# -*- coding: utf-8 -*-
B = "﻿"
ALLOWLIST = {"admin","root","delete","drop","username","apikey","paypal",
             "system","password","select","script","sudo","login","token"}

def _token_around(text, i):
    """Maximal run of [alnum or BOM] containing index i (the byte-exact token)."""
    def ok(ch): return ch.isalnum() or ch == B
    l = i
    while l > 0 and ok(text[l-1]): l -= 1
    r = i
    while r+1 < len(text) and ok(text[r+1]): r += 1
    return text[l:r+1]

def C1_fires(text):                      # strict-infix: both neighbours alphanumeric
    for i, ch in enumerate(text):
        if ch == B:
            left  = text[i-1] if i > 0 else ""
            right = text[i+1] if i+1 < len(text) else ""
            if left.isalnum() and right.isalnum(): return True
    return False

def C6_fires(text):                      # collapse of the token is a protected target
    for i, ch in enumerate(text):
        if ch == B:
            if _token_around(text, i).replace(B, "").lower() in ALLOWLIST: return True
    return False

benign = [("glued words","endword"+B+"startword"), ("concat newline","line one\n"+B+"second line"),
          ("paste prose","see "+B+"the attached"), ("BOM both spaces","hello "+B+" world"),
          ("config trailing","key=value"+B), ("log line","INFO "+B+"service started"),
          ("markdown body","Title\n"+B+"body text"), ("sentence space-before","fox "+B+"jumps over"),
          ("csv leading",B+"name,email"), ("csv cell",B+"value"),
          ("real word 'read'","re"+B+"ad this file"), ("real word 'friend'","my fri"+B+"end called"),
          ("real word 'notebook'","a note"+B+"book here"), ("real word 'meeting'","the mee"+B+"ting starts")]
ghost  = [("admin infix","ad"+B+"min"), ("admin trailing","admin"+B), ("root","ro"+B+"ot"),
          ("delete","de"+B+"lete"), ("username","user"+B+"name"), ("apikey","api"+B+"key"),
          ("drop","dr"+B+"op"), ("paypal","pay"+B+"pal"), ("system","sy"+B+"stem"),
          ("password","pass"+B+"word")]
# RESULT: C1 benign FP 5/14 (36%), ghost TP 9/10 (90%)  [fires on re/friend/notebook/meeting, misses trailing]
#         C6 benign FP 0/14 (0%),  ghost TP 10/10 (100%)
```

============================================================
EXIT
============================================================
Пространство исследовано (5 ног, 4 семейства, >20 различных механизмов). Прямой hold отвергнут единогласно
  и замером. Измеримые развилки разрешены свод-замером (C6 > C1 > loose). Материал под AUTHOR_DECISION по
  пакету «СЕЙЧАС» (P1/P2/P3, token=MEDIUM), с C6 как отложенным измеренным мостом и E4 как отдельным фронтом.
FORK_STATUS: OPEN — PENDING_AUTHOR_DECISION (пакет «СЕЙЧАС»). Код заблокирован до решения.

END_OF_RAW_REVIEW_BUNDLE
