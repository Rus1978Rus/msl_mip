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

END_OF_DOCUMENT
