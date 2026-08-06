# MSL/MIP Sign Alphabet

**A structural threat analyzer that asks not "what is this?" but "what does this sign do in this context?"**

*Status: WORKING_DRAFT · Authoritative language: Russian · Author: Ruslan Malyavsky*
*PRIVATE AUTHORED PROJECT / COMMERCIAL USE PROHIBITED*
*NOT A FINAL STANDARD · NOT A SECURITY CERTIFICATE · NOT A PRODUCTION VALIDATOR*

---

## What is this?

MSL/MIP analyzes text character by character to detect potential threats — phishing, injections, path traversal, brand mimicry. Unlike systems that rely on word lists or domain reputation databases, MSL/MIP works purely with **structure**: it treats each sign (`.`, `/`, 💀, ☠) as an object with a history, a function, and a context, and evaluates what that sign *does* in the surrounding text.

For the full philosophy, see [`MANIFEST.md`](MANIFEST.md) (available in 9 languages).

---

## Quick Start

**Requirements:** Python 3.7 or newer. No external dependencies — only the standard library.
**Runs offline by default:** the IANA TLD registry and the Public Suffix List ship as vendored,
sha256-pinned snapshots in `data/net/`, so a fresh clone analyses domains with no network access.
Set `MSL_MIP_ALLOW_NETWORK=1` to fetch fresher registries at runtime. Whenever the system falls
back to its built-in remnant instead of a full registry, it reports itself as **degraded** —
provenance travels with the data rather than being inferred from the entry count.

**1. Check Python is installed:**
```
python --version     (Windows)
python3 --version    (Mac/Linux)
```
If not installed, download from [python.org](https://python.org). On Windows, check "Add Python to PATH" during install.

**2. Run the analyzer** (from inside the project folder):
```
python msl_mip_runtime.py "paypal.com.security-check.ru/verify"
```
Windows uses `py` instead of `python`.

**3. Or run in interactive mode** (no argument):
```
python msl_mip_runtime.py
```
It will prompt you for text to analyze.

**Example output:**
```
TEXT: 'paypal.com.security-check.ru/verify'
--- SINGLE SIGNS ---
  [6]  U+002E interp=domain_separator risk=HIGH -> action=hold_pending_review
  ...
FINAL VERDICT: HOLD_PENDING_REVIEW
```

The verdict is one of: `PASS` → `QUEUE_FOR_REVIEW` → `HOLD_PENDING_REVIEW` (increasing severity).

---

## Project Structure

```
msl_mip_runtime.py      Entry point — run this
MANIFEST.md             Conceptual manifesto (9 languages)
core/                   Card parser, data model, and the analysis axes
  load_card.py            Reads sign cards from disk
  sign_core_card.py       Data structures
  tree_parser.py          Indentation parser
  public_suffix.py        3-tier domain data (PSL + IANA)
  unicode_tables.py       Pinned UCD/UTS#39 loaders (sha256-verified)
  confusable_axis.py      Visible lookalikes (skeleton + mixed script)
  tag_axis.py             Tag-block covert text
  variation_registry.py   Variation-selector payloads
  uax9.py                 Conformant UAX#9 bidi algorithm
  bidi_axis.py            Reordering: logical vs visual order
  zw_bits.py              Zero-width carrier streams
  sni_oracle.py           Script-native functional positions
single_sign/            Single-sign analysis layer
  module_engine.py        Sign dispatcher (by codepoint)
  integrator_engine.py    Verdict for one sign
  matchers/               One matcher per sign (dot, solidus, skull...)
sequence/               Sequence analysis layer
  sequence_engine.py      Cross-sign patterns (../,  //, etc.)
cards/                  Sign definitions (the knowledge base)
data/unicode/           Pinned Unicode tables + PIN_MANIFEST.md
data/net/               Vendored IANA TLD + Public Suffix List snapshots
tests/                  Gate suite — every behaviour has a guard cell
scripts/                run_gates.py (whole suite), analyze_file.py (any file)
templates/              Templates for extending the system
```

---

## How It Works (three layers)

1. **Single Sign** — each sign is analyzed on its own: which substrate (URL, filesystem, math), which epoch (historical function), what risk level. A sign is judged only by its immediate context.

2. **Sequence** — signs combine into candidates. Cross-sign patterns emerge here: `../../../` (path traversal), `//` (protocol injection), `💀☠` (epoch mismatch). A sequence only counts if all its signs were validated by layer 1.

   The sequence layer also decides **mask (homoglyph) verdicts** (the relation axis): a sign declared as a mask of a canon (e.g. fullwidth `／` U+FF0F masking `/` U+002F) gets its risk from *context*, not from the sign itself — HIGH inside a host, MEDIUM in a URL path, NONE in free text, and only when the relation scope covers that context. A relation alone is never a threat (RELATION_FOUND != THREAT).

3. **Integration** — the final graded verdict, preserving space for human judgment. The system flags; humans decide.

---

## The Axes (four kinds of structural threat)

Beyond the three layers, the runtime carries independent **axes**. Each is additive,
raise-only and fail-open: an axis can add a signal, never remove another one's, and a
broken axis reports its own failure instead of silently passing. The final level is the
maximum across contributors, and every report says *which* axis contributed.

| Threat kind | Axis | What it answers |
|---|---|---|
| **Substitution** | `confusable_axis` | is this character a lookalike of another (mixed-script, skeleton collision)? |
| **Concealment** | `tag_axis`, `variation_registry`, `zw_bits` | is invisible data riding in tag characters, variation selectors, or zero-width carriers? |
| **Reordering** | `bidi_axis` + `uax9` | does the visible order differ from the stored order? (`invoice[RLO]gpj.exe` renders as `invoiceexe.jpg`) |
| **Break** | card layer + input guard | does an invisible character break a host, a token, or a byte-exact comparison? |

Two design rules run through all of them:

- **Pinned data, never "latest".** Script, Line_Break, InCB, Joining_Type, confusables,
  bidi brackets and the variation registries are frozen files verified by sha256
  (`data/unicode/PIN_MANIFEST.md`). A hash mismatch disables the affected rule
  *visibly* rather than changing behaviour silently.
- **The function of the position, not the writing system.** The same invisible character
  is normal orthography in one script and an anomaly in another. Khmer separates words
  with a zero-width space; Persian writes a half-space before enclitics; Devanagari joins
  conjuncts with a virama. The oracles judge whether *this occurrence* does a normative
  job (`Line_Break=SA` neighbours, `InCB=Linker`, joining type) — and machine contexts
  (host, e-mail, URL, path, identifier) are never softened, whatever the script.

---

## How to Add a New Sign

The system is designed to be extended. To add a sign you need three things, all with templates in [`templates/`](templates/):

1. **A Sign Card** (`cards/`) — define the sign's codepoint, epochs, safe cases, risk cases, and sequence candidates where applicable. Template: `SIGN_CORE_CARD_TEMPLATE_GEN3_v0_3_R1_RU.md` / `_EN.md`. Filling rules: `SIGN_CORE_CARD_CONVEYOR_RULES_GEN3_v0_3_R1`.

2. **A Matcher** (`single_sign/matchers/`) — the code that reads context and returns interpretation + risk. Template: `MODULE_TEMPLATE_SINGLE_SIGN_GEN3_v0_2_PLUS_EPOCH_v0_1_EN.md`

3. **Register it** — add one line to the `_MATCHER_REGISTRY` in `single_sign/module_engine.py`.

**Mask signs (homoglyphs) take a shorter path.** If the sign can act as a visual mask of another sign in a protected context (e.g. `／` masking `/`), you do NOT write a matcher. Declare a `SIGN_RELATIONS` block in the card (relation type, canon target, `CONTEXT_SCOPE`) — see the `OPTIONAL_FIELDS_RELATION` section of the conveyor rules. The runtime emits relation candidates automatically and the sequence layer decides the risk from context.

For sequence-level behavior, see the `SEQUENCE_MODULE_TEMPLATE` and `SEQUENCE_INTEGRATOR_TEMPLATE` in `templates/`.

---

## The Conveyor Discipline

This project uses a multi-model review methodology called the **conveyor**. No change enters the system without independent review by multiple AI models, and every claim is verified by running the actual code — never by logical tracing alone.

Core rules (full text: [`templates/SIGN_CORE_CARD_CONVEYOR_RULES_GEN3_v0_3_RU.md`](templates/SIGN_CORE_CARD_CONVEYOR_RULES_GEN3_v0_3_RU.md)):
- **VERIFY_BEFORE_TRUST** — verify by execution, not by assumption
- **AUTHOR_DECISION_STATUS_AUTHORITY** — only the author assigns final status
- **NO_EXCEPTIONS** — every code change goes through the conveyor, regardless of size

To submit a change for review, use the packet template: `templates/CONVEYOR_RUN_PACKET_TEMPLATE_v0_1_RU.md`

---

## Limitations & Status

- **WORKING_DRAFT** — this is an active research project, not production software.
- The system works with **structure only**. It does not know "PayPal" is a brand. It knows that `com` in a non-final position of a domain chain is a structural signal of mimicry.
- **Brand-lookalike domains with a single dot** (e.g. `paypai.com`) currently pass — that requires a separate reputation/typosquatting layer, which is future work.
- **Nine sign cards are currently loaded.** Five are `ARTIFACT_CONFIRMED` (`.` U+002E, `/` U+002F, `💀` U+1F480, `☠` U+2620, `@` U+0040). The fullwidth solidus `／` (U+FF0F) — the **relation/mask axis**, no matcher, relations only — is loaded as `WORKING_DRAFT`. Three cards of the invisible *supervised class* (Cf ∧ Default_Ignorable) are also loaded: zero-width space (U+200B, `WORKINGLY_CLOSED`, battery 21/21), zero-width joiner (U+200D) and byte order mark (U+FEFF) as `WORKING_DRAFT`. The runtime prints a `CARD_NOT_CONVEYOR_REVIEWED` warning for every `WORKING_DRAFT` card, so a draft result is never passed off as reliable.
- **The gate suite is the contract: 41 gates, all green** (`py -3 scripts/run_gates.py`). Every decision has guard cells for both halves — the attack it must catch and the legitimate text it must not wake on. Included are 862k official Unicode bidi conformance cases with zero mismatches.
- **Known blindness is pinned, not hidden.** A single-carrier presence/absence scheme sitting on functionally valid positions is indistinguishable from ordinary orthography *in principle* — two different histories produce the identical byte string, so no deterministic rule can separate them. That limit is named (`LIMIT-ZW-SINGLE-CARRIER-FUNCTIONAL`, `REGRESSION_CARD_ZWSP_NATIVE`), pinned by test cells, and stated in the report rather than papered over. Roughly thirty such residuals are registered across the axes; each names its own bypass.
- **Measured, not assumed.** Field measurements on live Khmer text (Wikipedia, Tatoeba, Telegram and Facebook comments) are recorded in `conveyor_runs/SNI_FIELD_MEASURE_*`, including a controlled probe showing that Facebook strips zero-width spaces from comments while Telegram preserves them and injects bidi isolates of its own — carriers are transformed differently by every transport.
- Sign cards are written in Russian (the project's authoritative language). Code output is in English.

## Standards Alignment

MSL/MIP was designed independently, but its architecture lines up with
several established security frameworks. These are **structural
correspondences in spirit**, not certified mappings — framework
crosswalks are rarely one-to-one, and none of the below has been
formally audited by a standards body.

- **NIST SP 800-53 Rev 5 — SI-10 (Information Input Validation).**
  SI-10 calls for checking the syntax and semantics of inputs to
  prevent injection and cross-site-scripting attacks. MSL/MIP's three
  layers (single-sign validation → sequence anchoring → contradiction
  guards) are a structural input-validation pipeline in this spirit.
- **NIST SP 800-53 Rev 5 — AU (Audit and Accountability) family.**
  Every verdict carries an `action_rationale` (e.g.
  `risk_level=HIGH; risk_cases=RISK_CASE_002; guards=CG3`), giving an
  auditable, traceable record of why each decision was made rather
  than an opaque score.
- **OWASP Top 10:2025 / CVE-grounded roadmap.** The Sign Priority
  Registry ranks candidate signs against documented attack classes
  (XSS, SQL injection, Trojan Source / CVE-2021-42574 bidi controls),
  keeping development tied to the real-world threat landscape.
- **MITRE ATT&CK / ATLAS (potential, not claimed).** The runtime emits
  structured, RISK_CASE-tagged output that could in principle feed an
  ATT&CK-mapping or ATLAS (AI-threat) workflow. We deliberately do
  **not** assert specific technique IDs here: an external analysis
  proposed some (e.g. T1592 for the solidus PHAGO case), but T1592 is a
  reconnaissance technique ("Gather Victim Host Information") and does
  not match brand-impersonation — a reminder that technique-level
  mappings need per-case verification before being claimed.

This section is descriptive, for readers placing MSL/MIP in a broader
context. It is not a compliance claim.

---
---

# MSL/MIP Sign Alphabet (Русский)

**Структурный анализатор угроз, который спрашивает не «что это?», а «что делает этот знак в этом контексте?»**

*Статус: WORKING_DRAFT · Авторитетный язык: русский · Автор: Руслан Малявский*
*ЧАСТНЫЙ АВТОРСКИЙ ПРОЕКТ / COMMERCIAL USE PROHIBITED*
*НЕ ФИНАЛЬНЫЙ СТАНДАРТ · НЕ СЕРТИФИКАТ БЕЗОПАСНОСТИ · НЕ PRODUCTION-ВАЛИДАТОР*

---

## Что это?

MSL/MIP анализирует текст знак за знаком для выявления потенциальных угроз — фишинга, инъекций, path traversal, имитации брендов. В отличие от систем, полагающихся на списки слов или базы репутации доменов, MSL/MIP работает исключительно со **структурой**: он рассматривает каждый знак (`.`, `/`, 💀, ☠) как объект с историей, функцией и контекстом, и оценивает, что этот знак *делает* в окружающем тексте.

Полная философия — в [`MANIFEST.md`](MANIFEST.md) (на 9 языках).

---

## Быстрый старт

**Требования:** Python 3.7 или новее. Никаких внешних зависимостей — только стандартная библиотека.
**Работает офлайн по умолчанию:** реестр IANA TLD и Public Suffix List лежат в репозитории как
вендоренные снапшоты с sha256-пином (`data/net/`), поэтому свежий клон разбирает домены без сети.
Переменная `MSL_MIP_ALLOW_NETWORK=1` включает подтягивание свежих реестров в рантайме. Если
система откатывается на встроенный огрызок вместо полного реестра, она сообщает о себе
**degraded** — происхождение едет вместе с данными, а не угадывается по числу записей.

**1. Проверьте, установлен ли Python:**
```
python --version     (Windows)
python3 --version    (Mac/Linux)
```
Если нет — скачайте с [python.org](https://python.org). На Windows поставьте галочку «Add Python to PATH» при установке.

**2. Запустите анализатор** (находясь внутри папки проекта):
```
python msl_mip_runtime.py "paypal.com.security-check.ru/verify"
```
На Windows используйте `py` вместо `python`.

**3. Или в интерактивном режиме** (без аргумента):
```
python msl_mip_runtime.py
```
Программа спросит текст для анализа.

**Пример вывода:**
```
TEXT: 'paypal.com.security-check.ru/verify'
--- SINGLE SIGNS ---
  [6]  U+002E interp=domain_separator risk=HIGH -> action=hold_pending_review
  ...
FINAL VERDICT: HOLD_PENDING_REVIEW
```

Вердикт — один из: `PASS` → `QUEUE_FOR_REVIEW` → `HOLD_PENDING_REVIEW` (по возрастанию серьёзности).

---

## Структура проекта

```
msl_mip_runtime.py      Точка входа — запускать это
MANIFEST.md             Концептуальный манифест (9 языков)
core/                   Парсер карточек, модель данных и оси анализа
  load_card.py            Читает карточки знаков с диска
  sign_core_card.py       Структуры данных
  tree_parser.py          Парсер отступов
  public_suffix.py        3-уровневые доменные данные (PSL + IANA)
  unicode_tables.py       Загрузчики запиненных таблиц UCD/UTS#39 (sha256)
  confusable_axis.py      Видимые двойники (скелет + смешение письменностей)
  tag_axis.py             Скрытый текст в TAG-блоке
  variation_registry.py   Нагрузка в вариационных селекторах
  uax9.py                 Конформный алгоритм UAX#9 (bidi)
  bidi_axis.py            Переупорядочивание: логический порядок против видимого
  zw_bits.py              Потоки носителей нулевой ширины
  sni_oracle.py           Штатные позиции родных письменностей
single_sign/            Слой анализа одиночных знаков
  module_engine.py        Диспетчер знаков (по кодпоинту)
  integrator_engine.py    Вердикт для одного знака
  matchers/               По одному матчеру на знак
sequence/               Слой анализа последовательностей
  sequence_engine.py      Межзнаковые паттерны (../, //) + вердикты масок (отношения)
cards/                  Определения знаков (база знаний)
data/unicode/           Запиненные таблицы Unicode + PIN_MANIFEST.md
data/net/               Вендоренные снапшоты реестра IANA TLD и PSL
tests/                  Свод гейтов — у каждого поведения есть ячейка-страж
scripts/                run_gates.py (весь свод), analyze_file.py (любой файл)
templates/              Шаблоны для расширения системы
```

---

## Как это работает (три слоя)

1. **Одиночный знак** — каждый знак анализируется отдельно: какой субстрат (URL, файловая система, математика), какая эпоха (историческая функция), какой уровень риска. Знак судится только по непосредственному контексту.

2. **Последовательность** — знаки объединяются в кандидаты. Здесь возникают межзнаковые паттерны: `../../../` (path traversal), `//` (protocol injection), `💀☠` (конфликт эпох). Последовательность засчитывается, только если все её знаки прошли валидацию на первом слое.

   Sequence-слой также выносит **вердикты по маскам (гомоглифам)** — ось «отношение»: знак, объявленный маской канона (например, полноширинный `／` U+FF0F, маскирующий `/` U+002F), получает риск из *контекста*, а не из самого знака — HIGH внутри host-части, MEDIUM в пути URL, NONE в свободном тексте, и только когда scope отношения покрывает этот контекст. Само отношение — никогда не угроза (RELATION_FOUND ≠ THREAT).

3. **Интеграция** — финальный градуированный вердикт, сохраняющий место для человеческого суждения. Система отмечает; человек решает.

---

## Оси (четыре рода структурной угрозы)

Помимо трёх слоёв рантайм несёт независимые **оси**. Каждая аддитивна, работает только
на повышение и fail-open: ось может добавить сигнал, но не может погасить чужой, а
сломанная ось сообщает о собственной поломке вместо тихого пропуска. Итоговый уровень —
максимум по вкладчикам, и отчёт всегда называет, *какая* ось его дала.

| Род угрозы | Ось | На какой вопрос отвечает |
|---|---|---|
| **Подмена** | `confusable_axis` | не двойник ли этот знак другого (смешение письменностей, совпадение скелетов)? |
| **Сокрытие** | `tag_axis`, `variation_registry`, `zw_bits` | не едут ли невидимые данные в TAG-знаках, вариационных селекторах или носителях нулевой ширины? |
| **Переупорядочивание** | `bidi_axis` + `uax9` | отличается ли видимый порядок от хранимого? (`invoice[RLO]gpj.exe` показывается как `invoiceexe.jpg`) |
| **Разрыв** | карточный слой + input guard | не разрывает ли невидимка хост, токен или побайтовое сравнение? |

Через все оси проходят два правила:

- **Запиненные данные, никогда «latest».** Scripts, Line_Break, InCB, Joining_Type,
  confusables, bidi-скобки и реестры вариаций — замороженные файлы, проверяемые по
  sha256 (`data/unicode/PIN_MANIFEST.md`). Несовпадение хэша **видимо** выключает
  соответствующее правило, а не меняет поведение молча.
- **Судится функция позиции, а не письменность.** Один и тот же невидимый знак — норма
  орфографии в одной письменности и аномалия в другой. Кхмерский разделяет слова
  пробелом нулевой ширины, персидский ставит полупробел перед энклитиками, деванагари
  соединяет конъюнкты вирамой. Оракулы решают, выполняет ли *данное вхождение* штатную
  работу (соседи с `Line_Break=SA`, `InCB=Linker`, тип соединения) — а машинные контексты
  (хост, почта, URL, путь, идентификатор) не смягчаются никогда, в любой письменности.

---

## Как добавить новый знак

Система спроектирована для расширения. Чтобы добавить знак, нужны три вещи, все с шаблонами в [`templates/`](templates/):

1. **Карточка знака** (`cards/`) — определите кодпоинт, эпохи, безопасные случаи, рисковые случаи и кандидаты-последовательности (где применимо). Шаблон: `SIGN_CORE_CARD_TEMPLATE_GEN3_v0_3_R1_RU.md` / `_EN.md`. Правила заполнения: `SIGN_CORE_CARD_CONVEYOR_RULES_GEN3_v0_3_R1`.

2. **Матчер** (`single_sign/matchers/`) — код, который читает контекст и возвращает интерпретацию + риск. Шаблон: `MODULE_TEMPLATE_SINGLE_SIGN_GEN3_v0_2_PLUS_EPOCH_v0_1_EN.md`

3. **Зарегистрировать** — добавьте одну строку в `_MATCHER_REGISTRY` в `single_sign/module_engine.py`.

**Знаки-маски (гомоглифы) идут коротким путём.** Если знак может выступать визуальной маской другого знака в защищённом контексте (например, `／` маскирует `/`), матчер писать НЕ нужно. Объявите блок `SIGN_RELATIONS` в карточке (тип отношения, канон-цель, `CONTEXT_SCOPE`) — см. раздел `OPTIONAL_FIELDS_RELATION` в правилах конвейера. Рантайм эмитит кандидатов отношения автоматически, а sequence-слой выносит риск из контекста.

Для поведения на уровне последовательностей см. `SEQUENCE_MODULE_TEMPLATE` и `SEQUENCE_INTEGRATOR_TEMPLATE` в `templates/`.

---

## Конвейерная дисциплина

Проект использует методологию мульти-модельного ревью — **конвейер**. Ни одно изменение не входит в систему без независимого ревью несколькими ИИ-моделями, и каждое утверждение проверяется запуском реального кода — никогда только логической трассировкой.

Основные правила (полный текст: [`templates/SIGN_CORE_CARD_CONVEYOR_RULES_GEN3_v0_3_RU.md`](templates/SIGN_CORE_CARD_CONVEYOR_RULES_GEN3_v0_3_RU.md)):
- **VERIFY_BEFORE_TRUST** — проверять запуском, не предположением
- **AUTHOR_DECISION_STATUS_AUTHORITY** — только автор присваивает финальный статус
- **NO_EXCEPTIONS** — любое изменение кода проходит конвейер, независимо от размера

Для отправки изменения на ревью используйте шаблон пакета: `templates/CONVEYOR_RUN_PACKET_TEMPLATE_v0_1_RU.md`

---

## Ограничения и статус

- **WORKING_DRAFT** — это активный исследовательский проект, не production-софт.
- Система работает **только со структурой**. Она не знает, что «PayPal» — это бренд. Она знает, что `com` в непоследней позиции доменной цепочки — структурный сигнал имитации.
- **Домены-двойники брендов с одной точкой** (например `paypai.com`) сейчас проходят — для них нужен отдельный слой репутации/детекции typosquatting, это будущая работа.
- **Сейчас загружены девять карточек знаков.** Пять — `ARTIFACT_CONFIRMED` (`.` U+002E, `/` U+002F, `💀` U+1F480, `☠` U+2620, `@` U+0040). Полноширинный солидус `／` (U+FF0F) — **ось «отношение»/маска**, без матчера, только отношения — загружен как `WORKING_DRAFT`. Также загружены три карточки невидимого *поднадзорного класса* (Cf ∧ Default_Ignorable): пробел нулевой ширины (U+200B, `WORKINGLY_CLOSED`, батарея 21/21), соединитель нулевой ширины (U+200D) и маркер порядка байт (U+FEFF) как `WORKING_DRAFT`. Рантайм печатает предупреждение `CARD_NOT_CONVEYOR_REVIEWED` для каждой `WORKING_DRAFT`-карточки, поэтому черновой результат никогда не выдаётся за надёжный.
- **Свод гейтов — это контракт: 41 гейт, все зелёные** (`py -3 scripts/run_gates.py`). У каждого решения есть ячейки-стражи на обе половины: атака, которую обязаны поймать, и легитимный текст, на котором обязаны молчать. В своде — 862 тысячи официальных конформных случаев Unicode по bidi с нулём расхождений.
- **Известная слепота запинена, а не спрятана.** Однознаковая схема «есть/нет», стоящая на функционально верных позициях, неотличима от обычной орфографии **принципиально**: две разные истории дают одну и ту же строку байтов, и никакое детерминированное правило их не разделит. Этот предел назван (`LIMIT-ZW-SINGLE-CARRIER-FUNCTIONAL`, `REGRESSION_CARD_ZWSP_NATIVE`), закреплён тестовыми ячейками и выводится в отчёт, а не заминается. Всего по осям зарегистрировано около тридцати таких остатков, и каждый называет собственный обход.
- **Измерено, а не предположено.** Полевые замеры на живом кхмерском (Википедия, Tatoeba, комментарии Telegram и Facebook) записаны в `conveyor_runs/SNI_FIELD_MEASURE_*` — включая контрольную пробу, показавшую, что Facebook вырезает пробелы нулевой ширины из комментариев, а Telegram их сохраняет и добавляет собственные bidi-изоляты: каждый транспорт преобразует носители по-своему.
- Карточки знаков написаны на русском (авторитетный язык проекта). Вывод программы — на английском.

## Соответствие стандартам

MSL/MIP разрабатывался независимо, но его архитектура совпадает с
несколькими признанными фреймворками безопасности. Это **структурные
соответствия по духу**, а не сертифицированные маппинги — кросс-связи
между фреймворками редко бывают один-к-одному, и ничто из
нижеперечисленного не проходило формального аудита органом
стандартизации.

- **NIST SP 800-53 Rev 5 — SI-10 (Information Input Validation).**
  SI-10 требует проверки синтаксиса и семантики входных данных для
  предотвращения инъекций и XSS. Три слоя MSL/MIP (проверка одиночного
  знака → якорение последовательностей → contradiction guards) — это
  конвейер валидации входа в том же духе.
- **NIST SP 800-53 Rev 5 — семейство AU (Audit and Accountability).**
  Каждый вердикт несёт `action_rationale` (например
  `risk_level=HIGH; risk_cases=RISK_CASE_002; guards=CG3`), давая
  аудируемую, трассируемую запись причины каждого решения вместо
  непрозрачной оценки.
- **OWASP Top 10:2025 / привязка к CVE.** Реестр приоритетов знаков
  ранжирует знаки-кандидаты относительно документированных классов
  атак (XSS, SQL-инъекции, Trojan Source / bidi-контролы
  CVE-2021-42574), удерживая разработку привязанной к реальному
  ландшафту угроз.
- **MITRE ATT&CK / ATLAS (потенциально, не заявляется).** Runtime
  выдаёт структурированный вывод с тегами RISK_CASE, который в принципе
  мог бы питать ATT&CK-маппинг или ATLAS (угрозы ИИ). Мы намеренно
  **не** указываем конкретные ID техник: внешний анализ предложил
  некоторые (например, T1592 для PHAGO-случая солидуса), но T1592 —
  техника разведки («Gather Victim Host Information») и не соответствует
  имитации бренда — напоминание, что маппинги на уровне техник требуют
  покейсовой проверки, прежде чем их заявлять.

Этот раздел — описательный, для читателей, помещающих MSL/MIP в более
широкий контекст. Это не заявление о соответствии требованиям.
