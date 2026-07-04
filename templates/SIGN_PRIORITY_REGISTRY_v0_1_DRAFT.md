PRIVATE AUTHORED PROJECT / COMMERCIAL USE PROHIBITED
DOCUMENT_ID: SIGN_PRIORITY_REGISTRY_v0_1
DOCUMENT_TYPE: PRIORITY_REGISTRY
STATUS: WORKING_DRAFT — conveyor round 1 applied (2026-07-03)
AUTHOR: Ruslan Malyavsky
CREATED_AT: 2026-07-03

============================================================
# Sign Priority Registry — 50 Most Dangerous Signs
# Реестр приоритетов знаков — 50 самых опасных знаков
============================================================

## Purpose / Назначение

EN: This registry ranks candidate signs for MSL/MIP by threat
potential. It is a roadmap, not a set of artifacts — it says which
signs to build next and why. Sources: OWASP Top 10:2025 (Injection),
Unicode Security (UTS #39), CVE databases, and 2025-2026 research on
LLM prompt injection.

RU: Этот реестр ранжирует знаки-кандидаты для MSL/MIP по потенциалу
угрозы. Это дорожная карта, не набор артефактов — он говорит, какие
знаки делать следующими и почему. Источники: OWASP Top 10:2025
(инъекции), Unicode Security (UTS #39), базы CVE и исследования
2025-2026 по промпт-инъекциям в LLM.

## Categories / Категории

- **PH** = Phishing / social engineering (обман людей)
- **INJ** = Injection / technical attacks (обман машин)
- **LLM** = LLM bypass / prompt injection (обман ИИ)

## PHAGO dimension / Измерение PHAGO

PHAGO_ENTITY_MIMICRY is a **separate, orthogonal dimension** from the
PH/INJ/LLM category. A sign can belong to any category AND still carry
(or not carry) PHAGO potential. PHAGO measures whether a sign is used
to mimic the *existence of a verified entity* (a brand, an organization,
an official account/subproject) — not merely to obfuscate structure.

PHAGO_ENTITY_MIMICRY — это **отдельное, ортогональное измерение**
относительно категории PH/INJ/LLM. Знак может принадлежать любой
категории И при этом нести (или не нести) PHAGO-потенциал. PHAGO
измеряет, используется ли знак для имитации *существования проверенной
сущности* (бренда, организации, официального аккаунта/подпроекта), а не
просто для маскировки структуры.

PHAGO flag values / Значения флага PHAGO:
- **●** = strong PHAGO carrier (direct entity-existence mimicry) /
  сильный носитель PHAGO (прямая имитация существования сущности)
- **○** = partial / adapted PHAGO (domain-specific, e.g. emoji
  astroturfing) / частичный / адаптированный PHAGO
- **—** = not a PHAGO carrier (structure masking only, no entity
  mimicry) / не носитель PHAGO (только маскировка структуры)

This dimension is confirmed at the card level (SOLIDUS = ●,
DOT = —, SKULL = ○) and is flagged here so that the roadmap can
prioritize signs strong in brand/entity mimicry, which commercial
defenses often miss. Это измерение подтверждается на уровне карточки и
отмечается здесь, чтобы дорожная карта могла приоритизировать знаки,
сильные в имитации бренда/сущности.

## Status values / Значения статуса

- **DONE** — card confirmed (ARTIFACT_CONFIRMED)
- **TEST** — test card (WORKING_DRAFT)
- **NEXT** — selected for next build round
- **CANDIDATE** — in the queue, not yet started

## Priority / Приоритет

- **CRITICAL** — active exploitation, high impact, weak existing defenses
- **HIGH** — common attack vector, well-documented
- **MEDIUM** — situational or lower-impact vector

============================================================
## TIER 0 — DONE (already in the system / уже в системе)
============================================================

| # | Sign | Codepoint | Cat | Vector (EN / RU) | Priority | Status |
|---|------|-----------|-----|------------------|----------|--------|
| 1 | `.` | U+002E | PH | Domain mimicry via subdomain chains / имитация домена через поддомены | CRITICAL | DONE |
| 2 | `/` | U+002F | INJ | Path traversal, protocol boundary / обход пути, граница протокола | CRITICAL | DONE |
| 3 | 💀 | U+1F480 | LLM | Epoch-mismatch, semantic overload / конфликт эпох, семантическая перегрузка | MEDIUM | DONE |
| 4 | ☠ | U+2620 | LLM | Cross-card sequence test / тест межкарточной последовательности | MEDIUM | TEST |

============================================================
## TIER 1 — NEXT (selected for next round / выбрано на следующий раунд)
============================================================

| # | Sign | Codepoint | Cat | Vector (EN / RU) | Priority | Status |
|---|------|-----------|-----|------------------|----------|--------|
| 5 | `@` | U+0040 | PH | URL userinfo spoofing (paypal.com@evil.ru) / подмена домена через userinfo | CRITICAL | NEXT |
| 6 | `-` | U+002D | PH | Typosquatting, fake compound brands (paypal-secure.com) / typosquatting, фейковые составные бренды | HIGH | NEXT |
| 7 | `<` | U+003C | INJ | XSS tag opening (<script>) / открытие тега XSS | CRITICAL | NEXT |
| 8 | `'` | U+0027 | INJ | SQL injection string break (' OR '1'='1) / разрыв строки SQL-инъекции | CRITICAL | NEXT |
| 9 | U+FE0F | VS16 | LLM | Invisible emoji modifier — bypasses commercial guardrails / невидимый модификатор, обходит коммерческие защиты | CRITICAL | NEXT |
| 10 | U+200D | ZWJ | LLM | Zero-width joiner — hides arbitrary-length payload / скрывает полезную нагрузку произвольной длины | CRITICAL | NEXT |

============================================================
## TIER 2 — CANDIDATE (queue / очередь)
============================================================

### Phishing / social engineering (PH)

| # | Sign | Codepoint | Vector (EN / RU) | Priority |
|---|------|-----------|------------------|----------|
| 11 | `:` | U+003A | Port/protocol confusion, URL parsing / путаница порта-протокола | HIGH |
| 12 | `%` | U+0025 | URL-encoding obfuscation (%2F, %00) / обфускация через URL-кодирование | HIGH |
| 13 | `?` | U+003F | Query-string boundary, param smuggling / граница query, контрабанда параметров | MEDIUM |
| 14 | `#` | U+0023 | Fragment hiding, URL truncation trick / скрытие фрагмента, обрезка URL | MEDIUM |
| 15 | `_` | U+005F | Fake subdomains, lookalike separators / фейковые поддомены | MEDIUM |
| 16 | `~` | U+007E | Home-dir paths, tilde expansion in URLs / пути домашних директорий | MEDIUM |
| 17 | `а` | U+0430 | Cyrillic homoglyph of Latin 'a' (аpple.com) / кириллический гомоглиф | CRITICAL |
| 18 | `ο` | U+03BF | Greek omicron homoglyph of 'o' / греческий гомоглиф 'o' | HIGH |
| 19 | `ⅼ` | U+217C | Roman numeral lookalike of 'l' / римская цифра-двойник 'l' | MEDIUM |
| 20 | `‐` | U+2010 | Unicode hyphen vs ASCII hyphen confusion / путаница Unicode-дефиса | MEDIUM |

### Injection / technical (INJ)

| # | Sign | Codepoint | Vector (EN / RU) | Priority |
|---|------|-----------|------------------|----------|
| 21 | `>` | U+003E | XSS tag closing / закрытие тега XSS | CRITICAL |
| 22 | `"` | U+0022 | Attribute break in HTML/SQL / разрыв атрибута в HTML/SQL | CRITICAL |
| 23 | `;` | U+003B | Command chaining, SQL statement end / цепочка команд, конец SQL | CRITICAL |
| 24 | `|` | U+007C | Shell pipe, command injection / shell-пайп, инъекция команд | CRITICAL |
| 25 | `&` | U+0026 | Command background/chaining, HTML entity / фоновая команда, HTML-сущность | HIGH |
| 26 | `` ` `` | U+0060 | Shell command substitution / подстановка shell-команды | HIGH |
| 27 | `$` | U+0024 | Variable expansion, template injection / раскрытие переменной, инъекция шаблона | HIGH |
| 28 | `\` | U+005C | Escape sequences, path confusion / escape-последовательности | HIGH |
| 29 | `(` | U+0028 | Function call, LDAP/regex injection / вызов функции, LDAP/regex-инъекция | MEDIUM |
| 30 | `)` | U+0029 | Closing paren in injection payloads / закрытие скобки в нагрузке | MEDIUM |
| 31 | `{` | U+007B | Template/expression injection ({{7*7}}) / инъекция шаблона | HIGH |
| 32 | `}` | U+007D | Template close / закрытие шаблона | MEDIUM |
| 33 | `*` | U+002A | Wildcard, LDAP injection, SQL comment / wildcard, LDAP-инъекция | MEDIUM |
| 34 | `=` | U+003D | Assignment, param pollution / присваивание, загрязнение параметров | MEDIUM |
| 35 | `[` | U+005B | Array/index injection, NoSQL / инъекция массива, NoSQL | MEDIUM |
| 36 | `]` | U+005D | Array close / закрытие массива | MEDIUM |
| 37 | `!` | U+0021 | History expansion, NoSQL negation / раскрытие истории, NoSQL-отрицание | MEDIUM |
| 38 | `+` | U+002B | URL space encoding, SQL concat / кодирование пробела, SQL-конкатенация | MEDIUM |
| 39 | U+000A | LF | HTTP response splitting, log injection / расщепление HTTP-ответа | HIGH |
| 40 | U+000D | CR | Carriage return, CRLF injection / возврат каретки, CRLF-инъекция | HIGH |

### LLM bypass / prompt injection (LLM)

| # | Sign | Codepoint | Vector (EN / RU) | Priority |
|---|------|-----------|------------------|----------|
| 41 | U+200B | ZWSP | Zero-width space, invisible token splitting / невидимое разбиение токенов | CRITICAL |
| 42 | U+200C | ZWNJ | Zero-width non-joiner, hidden payload / скрытая нагрузка | HIGH |
| 43 | U+2060 | WJ | Word joiner, invisible concatenation / невидимая конкатенация | HIGH |
| 44 | U+FEFF | BOM/ZWNBSP | Byte-order mark abuse, invisible prefix / злоупотребление BOM | HIGH |
| 45 | U+202E | RLO | Right-to-left override, filename spoofing (exe→txt) / переворот текста | CRITICAL |
| 46 | U+202D | LRO | Left-to-right override / переопределение направления | MEDIUM |
| 46a | U+202A | LRE | Left-to-right embedding, bidi spoofing / вложение bidi, спуфинг | MEDIUM |
| 46b | U+202B | RLE | Right-to-left embedding / вложение справа налево | MEDIUM |
| 46c | U+2066 | LRI | Left-to-right isolate (Trojan Source attack) / изолят (атака Trojan Source) | HIGH |
| 46d | U+2069 | PDI | Pop directional isolate / завершение изолята | MEDIUM |
| 47 | U+00A0 | NBSP | Non-breaking space, filter bypass / обход фильтра через неразрывный пробел | MEDIUM |
| 48 | U+180E | MVS | Mongolian vowel separator — NO LONGER whitespace since Unicode 6.3 (2013), Zs→Cf; legacy filter-bypass only / больше НЕ пробел с Unicode 6.3, только обход устаревших фильтров | LOW |
| 49 | U+E0001 | TAG | Unicode tag characters, hidden instructions / скрытые инструкции через tag-символы | CRITICAL |
| 50 | U+2028 | LSEP | Line separator — breaks JS string literals, log injection, JSON / разрыв строковых литералов JS, log-инъекция, JSON | HIGH |
| 51 | U+2029 | PSEP | Paragraph separator — same JS/JSON break as U+2028 / тот же разрыв JS/JSON, что U+2028 | HIGH |
| 52 | U+0000 | NUL | Null byte — string truncation, path/filter bypass (file.php%00.jpg) / нулевой байт, обрезка строки, обход фильтра | CRITICAL |
| 53 | U+0009 | TAB | Tab — filter bypass, CSV/TSV injection, indentation confusion / обход фильтра, инъекция CSV/TSV | MEDIUM |

============================================================
## Notes / Примечания
============================================================

EN:
- Homoglyphs (17-19, 45) are the highest-value phishing additions
  after the TIER 1 set — Cyrillic 'а' in "аpple.com" is visually
  identical to Latin 'a' and actively exploited.
- Invisible characters (41-50) are the fastest-growing LLM attack
  surface per 2025-2026 research; existing commercial guardrails
  largely fail against them.
- Bidi controls (45-46d) enable the "Trojan Source" attack (CVE-2021-42574):
  source code that reads one way to a human and another to a compiler.
  U+2066/U+2069 (isolates) are the modern vector, RLO/LRO the classic one.
- CR/LF (39-40) and RLO (45) are cross-category — they serve both
  classic injection and modern LLM/filename attacks.
- This registry is a DRAFT. Priorities and category assignments
  require conveyor review before being treated as authoritative.

RU:
- Гомоглифы (17-19, 45) — самое ценное фишинговое пополнение после
  набора TIER 1: кириллическая 'а' в "аpple.com" визуально идентична
  латинской 'a' и активно эксплуатируется.
- Невидимые символы (41-50) — быстрее всего растущая поверхность
  атак на LLM по данным 2025-2026; существующие коммерческие защиты
  против них в основном не работают.
- Bidi-контролы (45-46d) реализуют атаку "Trojan Source" (CVE-2021-42574):
  исходный код читается человеком одним образом, компилятором — другим.
  U+2066/U+2069 (изоляты) — современный вектор, RLO/LRO — классический.
- CR/LF (39-40) и RLO (45) — межкатегорийные: служат и классической
  инъекции, и современным атакам на LLM/имена файлов.
- Этот реестр — ЧЕРНОВИК. Приоритеты и категории требуют
  конвейерного ревью, прежде чем считаться авторитетными.

============================================================
## PHAGO-RELEVANT SIGNS — SUMMARY / СВОДКА ПО PHAGO
============================================================

Signs flagged for PHAGO_ENTITY_MIMICRY potential (the orthogonal
dimension defined above). CONFIRMED = verified at the card level;
HYPOTHESIS = flagged for review, not yet card-confirmed.

Знаки с PHAGO-потенциалом (ортогональное измерение, определённое выше).
CONFIRMED = подтверждено на уровне карточки; HYPOTHESIS = помечено для
ревью, ещё не подтверждено карточкой.

| Sign | Codepoint | PHAGO | Basis (EN / RU) | Source |
|------|-----------|-------|-----------------|--------|
| `/` | U+002F | ● | Brand path mimicry (OpenAI/VerifiedProjectX) / имитация принадлежности бренду | CONFIRMED (SOLIDUS card, RISK_CASE_007) |
| 💀 | U+1F480 | ○ | Emoji astroturfing, quasi-entity edginess / эмодзи-астротурфинг | CONFIRMED (SKULL card, PE_001/002) |
| `.` | U+002E | — | Domain masking only, no entity mimicry / только маскировка домена | CONFIRMED (DOT card, NOT_APPLICABLE) |
| `@` | U+0040 | ● | userinfo spoofing implies a verified account (paypal.com@evil.ru) / подмена аккаунта | HYPOTHESIS (TIER 1) |
| `-` | U+002D | ● | Fake compound brand (paypal-secure.com) implies affiliated entity / фейковый составной бренд | HYPOTHESIS (TIER 1) |
| `а` | U+0430 | ● | Cyrillic homoglyph mimics the real brand name itself (аpple.com) / гомоглиф имитирует само имя бренда | HYPOTHESIS (TIER 2) |
| `ο` | U+03BF | ● | Greek homoglyph, same brand-name mimicry / греческий гомоглиф, та же имитация | HYPOTHESIS (TIER 2) |
| `_` | U+005F | ○ | Fake subdomains may imply an official sub-entity / фейковые поддомены | HYPOTHESIS (TIER 2) |

NOTE: The `@`, `-`, and homoglyph signs are strong PHAGO candidates
because they mimic not just structure but the *identity of a specific
verified brand*. This is a priority signal for the roadmap: PHAGO
carriers are exactly the class that commercial reputation/lookalike
defenses most often miss. To be confirmed per-card during each sign's
own conveyor pass.

ПРИМЕЧАНИЕ: знаки `@`, `-` и гомоглифы — сильные кандидаты в PHAGO,
потому что имитируют не просто структуру, а *идентичность конкретного
проверенного бренда*. Это приоритетный сигнал для дорожной карты:
носители PHAGO — именно тот класс, который коммерческие защиты от
подделок чаще всего пропускают. Подтверждается покарточно во время
конвейерного прохода каждого знака.

END_OF_DOCUMENT
