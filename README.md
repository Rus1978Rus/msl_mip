# MSL/MIP Sign Alphabet

**A structural threat analyzer that asks not "what is this?" but "what does this sign do in this context?"**

*Status: WORKING_DRAFT · Authoritative language: Russian · Author: Ruslan Malyavsky*
*PRIVATE AUTHORED PROJECT / COMMERCIAL USE PROHIBITED*
*NOT A FINAL STANDARD · NOT A SECURITY CERTIFICATE · NOT A PRODUCTION VALIDATOR*

---

## 🌩 Also in this repo: StormClouds

Alongside the analyzer, this repository hosts **[StormClouds](stormclouds/)** — a
self-contained interactive side-project: a *"code storm"* where clouds carry
Python fragments, wind makes them collide, and lightning **actually executes**
the assembled code (with optional *sky memory*, *coverage*, and *evolution*
toggles). It is unrelated to MSL/MIP and lives entirely in its own folder.

**→ Open the project: [`stormclouds/`](stormclouds/)** — code, docs, and how to run.

---

## What is this?

MSL/MIP analyzes text character by character to detect potential threats — phishing, injections, path traversal, brand mimicry. Unlike systems that rely on word lists or domain reputation databases, MSL/MIP works purely with **structure**: it treats each sign (`.`, `/`, 💀, ☠) as an object with a history, a function, and a context, and evaluates what that sign *does* in the surrounding text.

For the full philosophy, see [`MANIFEST.md`](MANIFEST.md) (available in 9 languages).

---

## Quick Start

**Requirements:** Python 3.7 or newer. No external dependencies — only the standard library.

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
core/                   Card parser and data model
  load_card.py            Reads sign cards from disk
  sign_core_card.py       Data structures
  tree_parser.py          Indentation parser
  public_suffix.py        3-tier domain data (PSL + IANA)
single_sign/            Single-sign analysis layer
  module_engine.py        Sign dispatcher (by codepoint)
  integrator_engine.py    Verdict for one sign
  matchers/               One matcher per sign (dot, solidus, skull...)
sequence/               Sequence analysis layer
  sequence_engine.py      Cross-sign patterns (../,  //, etc.)
cards/                  Sign definitions (the knowledge base)
templates/              Templates for extending the system
```

---

## How It Works (three layers)

1. **Single Sign** — each sign is analyzed on its own: which substrate (URL, filesystem, math), which epoch (historical function), what risk level. A sign is judged only by its immediate context.

2. **Sequence** — signs combine into candidates. Cross-sign patterns emerge here: `../../../` (path traversal), `//` (protocol injection), `💀☠` (epoch mismatch). A sequence only counts if all its signs were validated by layer 1.

   The sequence layer also decides **mask (homoglyph) verdicts** (the relation axis): a sign declared as a mask of a canon (e.g. fullwidth `／` U+FF0F masking `/` U+002F) gets its risk from *context*, not from the sign itself — HIGH inside a host, MEDIUM in a URL path, NONE in free text, and only when the relation scope covers that context. A relation alone is never a threat (RELATION_FOUND != THREAT).

3. **Integration** — the final graded verdict, preserving space for human judgment. The system flags; humans decide.

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
- **Nine sign cards are currently loaded.** Five are `ARTIFACT_CONFIRMED` (`.` U+002E, `/` U+002F, `💀` U+1F480, `☠` U+2620, `@` U+0040). The fullwidth solidus `／` (U+FF0F) — the **relation/mask axis**, no matcher, relations only — is loaded as `WORKING_DRAFT`. Three cards of the invisible *supervised class* (Cf ∧ Default_Ignorable) are also loaded: zero-width space (U+200B, `WORKINGLY_CLOSED`, battery 21/21), zero-width joiner (U+200D) and byte order mark (U+FEFF) as `WORKING_DRAFT`. The runtime prints a `CARD_NOT_CONVEYOR_REVIEWED` warning for every `WORKING_DRAFT` card, so a draft result is never passed off as reliable. The relation axis (mask/homoglyph verdicts) is implemented and gated (step-4 gate 12/12).
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
core/                   Парсер карточек и модель данных
  load_card.py            Читает карточки знаков с диска
  sign_core_card.py       Структуры данных
  tree_parser.py          Парсер отступов
  public_suffix.py        3-уровневые доменные данные (PSL + IANA)
single_sign/            Слой анализа одиночных знаков
  module_engine.py        Диспетчер знаков (по кодпоинту)
  integrator_engine.py    Вердикт для одного знака
  matchers/               По одному матчеру на знак
sequence/               Слой анализа последовательностей
  sequence_engine.py      Межзнаковые паттерны (../, //) + вердикты масок (отношения)
cards/                  Определения знаков (база знаний)
templates/              Шаблоны для расширения системы
```

---

## Как это работает (три слоя)

1. **Одиночный знак** — каждый знак анализируется отдельно: какой субстрат (URL, файловая система, математика), какая эпоха (историческая функция), какой уровень риска. Знак судится только по непосредственному контексту.

2. **Последовательность** — знаки объединяются в кандидаты. Здесь возникают межзнаковые паттерны: `../../../` (path traversal), `//` (protocol injection), `💀☠` (конфликт эпох). Последовательность засчитывается, только если все её знаки прошли валидацию на первом слое.

   Sequence-слой также выносит **вердикты по маскам (гомоглифам)** — ось «отношение»: знак, объявленный маской канона (например, полноширинный `／` U+FF0F, маскирующий `/` U+002F), получает риск из *контекста*, а не из самого знака — HIGH внутри host-части, MEDIUM в пути URL, NONE в свободном тексте, и только когда scope отношения покрывает этот контекст. Само отношение — никогда не угроза (RELATION_FOUND ≠ THREAT).

3. **Интеграция** — финальный градуированный вердикт, сохраняющий место для человеческого суждения. Система отмечает; человек решает.

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
- **Сейчас загружены девять карточек знаков.** Пять — `ARTIFACT_CONFIRMED` (`.` U+002E, `/` U+002F, `💀` U+1F480, `☠` U+2620, `@` U+0040). Полноширинный солидус `／` (U+FF0F) — **ось «отношение»/маска**, без матчера, только отношения — загружен как `WORKING_DRAFT`. Также загружены три карточки невидимого *поднадзорного класса* (Cf ∧ Default_Ignorable): пробел нулевой ширины (U+200B, `WORKINGLY_CLOSED`, батарея 21/21), соединитель нулевой ширины (U+200D) и маркер порядка байт (U+FEFF) как `WORKING_DRAFT`. Рантайм печатает предупреждение `CARD_NOT_CONVEYOR_REVIEWED` для каждой `WORKING_DRAFT`-карточки, поэтому черновой результат никогда не выдаётся за надёжный. Ось «отношение» (вердикты по маскам/гомоглифам) реализована и закрыта gate-тестом (шаг 4: 12/12).
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
