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

3. **Integration** — the final graded verdict, preserving space for human judgment. The system flags; humans decide.

---

## How to Add a New Sign

The system is designed to be extended. To add a sign you need three things, all with templates in [`templates/`](templates/):

1. **A Sign Card** (`cards/`) — define the sign's codepoint, epochs, safe cases, risk cases, and sequence candidates. Template: `SIGN_CORE_CARD_TEMPLATE_GEN3_v0_3_RU.md`

2. **A Matcher** (`single_sign/matchers/`) — the code that reads context and returns interpretation + risk. Template: `MODULE_TEMPLATE_SINGLE_SIGN_GEN3_v0_2_PLUS_EPOCH_v0_1_EN.md`

3. **Register it** — add one line to the `_MATCHER_REGISTRY` in `single_sign/module_engine.py`.

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
- Card `☠` (U+2620) is a **test card** (WORKING_DRAFT), created to validate cross-card sequence logic. The other three cards are confirmed.
- Sign cards are written in Russian (the project's authoritative language). Code output is in English.

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
  sequence_engine.py      Межзнаковые паттерны (../,  //, и т.д.)
cards/                  Определения знаков (база знаний)
templates/              Шаблоны для расширения системы
```

---

## Как это работает (три слоя)

1. **Одиночный знак** — каждый знак анализируется отдельно: какой субстрат (URL, файловая система, математика), какая эпоха (историческая функция), какой уровень риска. Знак судится только по непосредственному контексту.

2. **Последовательность** — знаки объединяются в кандидаты. Здесь возникают межзнаковые паттерны: `../../../` (path traversal), `//` (protocol injection), `💀☠` (конфликт эпох). Последовательность засчитывается, только если все её знаки прошли валидацию на первом слое.

3. **Интеграция** — финальный градуированный вердикт, сохраняющий место для человеческого суждения. Система отмечает; человек решает.

---

## Как добавить новый знак

Система спроектирована для расширения. Чтобы добавить знак, нужны три вещи, все с шаблонами в [`templates/`](templates/):

1. **Карточка знака** (`cards/`) — определите кодпоинт, эпохи, безопасные случаи, рисковые случаи и кандидаты-последовательности. Шаблон: `SIGN_CORE_CARD_TEMPLATE_GEN3_v0_3_RU.md`

2. **Матчер** (`single_sign/matchers/`) — код, который читает контекст и возвращает интерпретацию + риск. Шаблон: `MODULE_TEMPLATE_SINGLE_SIGN_GEN3_v0_2_PLUS_EPOCH_v0_1_EN.md`

3. **Зарегистрировать** — добавьте одну строку в `_MATCHER_REGISTRY` в `single_sign/module_engine.py`.

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
- Карточка `☠` (U+2620) — **тестовая** (WORKING_DRAFT), создана для проверки межкарточной последовательной логики. Остальные три карточки подтверждены.
- Карточки знаков написаны на русском (авторитетный язык проекта). Вывод программы — на английском.
