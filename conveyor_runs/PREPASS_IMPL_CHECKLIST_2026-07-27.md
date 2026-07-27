ЧАСТНЫЙ АВТОРСКИЙ ПРОЕКТ / COMMERCIAL USE PROHIBITED

DOCUMENT_ID: PREPASS_IMPL_CHECKLIST_2026-07-27
DOCUMENT_TYPE: IMPL_CHECKLIST (рабочий чек-лист реализации)
PACKET_TYPE: DESIGN_SPEC (не конвейер-суждение; вход в конвейер)
DATE: 2026-07-27
PROJECT: MSL/MIP
AUTHOR: Руслан Малявский (AUTHOR_DECISION_STATUS_AUTHORITY)
STATUS: WORKING_DRAFT / NOT_LOCKED / NOT_CONVEYOR_REVIEWED / NOT_AUTHOR_DECIDED
BASIS: OBSERVERS_CANONICALIZATION_2026-07-27 (§8) + tools/canon_commutator_demo.py

РАМКА: свидетель, не судья. На неоднозначности — не «пропустить молча», а поднять
  тревогу/удержать (fail-closed). Pre-pass НЕ выносит финальный вердикт — он готовит
  канонический вход для карточек (scan_signs).

---

# CANONICALIZATION_PRE_PASS — рабочий чек-лист

## 1. Цель одной строкой
Привести вход к канонической форме ДО карточек, чтобы маскировки (кодировки, двойники)
свернулись к одному виду; где свернуть однозначно нельзя — пометить и удержать, а не
угадывать.

## 2. Вход / выход
- ВХОД: сырая строка (bytes/str) + `sink_type` (тип приёмника: URL/HOST/HTML/FS/TEXT/UNKNOWN).
- ВЫХОД: либо `canonical_str` (передать в scan_signs), либо `HOLD(reason)` (fail-closed),
  либо флаг `CONTEXT_DEPENDENT` (структура ясна, риск зависит от применения).

## 3. Стадии-декодеры (что декодировать)
Каждая стадия — чистая функция строка→строка, «вскрывающая» один спрятанный слой.

| # | Стадия | Что делает | Гейт (когда применять) |
|---|--------|-----------|------------------------|
| S1 | percent-decode (1 проход) | `%2e`→`.` | всегда |
| S2 | overlong-UTF-8 | `%c0%ae`→`.` ИЛИ reject (C0/C1 — невалидный ведущий байт) | всегда (по умолчанию REJECT) |
| S3 | NFKC / confusable-fold | `．`(FF0E)→`.`, `／`(FF0F)→`/`, гомоглифы→скелет | всегда |
| S4 | zero-width strip + bidi-normalize | убрать ZWSP/ZWJ/BOM; снять RLO/LRO | всегда |
| S5 | entity-decode (1 проход) | `&#46;`→`.`, `&sol;`→`/` | ГЕЙТ: только `sink_type==HTML` |
| S6 | host/IP-normalize | `2130706433`/`0x7f…`/`0177…`→dotted-quad | ГЕЙТ: только позиция хоста |

Правило по умолчанию для S2/S5/S6: **опасный декодер, применяемый не в том контексте,
сам порождает ложные тревоги; неприменённый — пропускает смуггл.** Отсюда §5 (гейт+fail-closed).

## 4. Порядок и остановка (главное — стадии НЕ коммутируют)
Раскодировать нужно ДО совместной неподвижной точки, а не за один проход и не в
произвольном порядке. Практический алгоритм:

```
MAX_PASSES = 16   # защита от decode-loop / decode-bomb

def prepass(raw, sink_type):
    s = raw
    for _ in range(MAX_PASSES):
        prev = s
        s = percent_decode_once(s)          # S1
        s = resolve_or_reject_overlong(s)    # S2 (default: reject invalid)
        s = nfkc_confusable_fold(s)          # S3
        s = strip_zero_width(normalize_bidi(s))  # S4
        if sink_type == HTML:                # S5 gated
            s = entity_decode_once(s)
        if in_host_position(sink_type):      # S6 gated
            s = host_ip_normalize(s)
        if s == prev:
            return s                          # joint fixpoint reached -> в scan_signs
    return HOLD("did not converge in MAX_PASSES — possible decode-bomb")  # fail-closed
```

СТОП-условия:
- **Fixpoint:** за полный проход строка не изменилась → это канон.
- **Лимит проходов:** не сошлось за MAX_PASSES → `HOLD` (не крутить бесконечно).

## 5. Когда говорить «не знаю» и когда удерживать
Два РАЗНЫХ случая — не путать.

**(a) CONTEXT_DEPENDENT (структура ясна, риск зависит от применения).**
После канонизации знак структурно однозначен, но его опасность = функция использования:
- `192.168.0.1` — мишень SSRF или адрес в конфиге?
- `0.0` — делитель (division-by-zero) или просто число?
- `g00gle` — домен (typosquat) или просто токен?
- `..` — атом обхода каталога или пунктуация?
→ НЕ выдавливать риск. Отдать структуру + метку `CONTEXT_DEPENDENT`; решает слой с контекстом.

**(b) FAIL-CLOSED HOLD (не сошлось / гейт неоднозначен).**
- не достигнут fixpoint за MAX_PASSES;
- `sink_type==UNKNOWN`, а гейтируемая стадия (S5/S6) ИЗМЕНИЛА БЫ вердикт (нельзя ни
  применить — ложные тревоги, ни пропустить — смуггл) → `HOLD` с обоими прочтениями;
- остаточная неоднозначность после полной решётки декодеров.

## 6. use vs mention — принципиальная граница (не решается декодером)
`%2f` — настоящий закодированный слэш (**use**) или текст «не пропускай `%2f`» (**mention**)?
Из строки неразрешимо. Правило:
- НЕ декодировать молча (сломаешь mention) и НЕ пропускать молча (пропустишь use);
- пометить как `AMBIGUOUS_USE_MENTION` и отдать карточкам/человеку. Это SAFE_CASE_005.

## 7. Приёмочные тесты (вход → ожидаемое)
Каждый — регресс-кейс. `HIGH` здесь = «структура traversal/NUL однозначна».

| Вход | Ожидаемый канон | Ожидаемый исход |
|------|-----------------|-----------------|
| `%2e%2e%2fetc%2fpasswd` | `../etc/passwd` | traversal (HIGH) |
| `%252e%252e%252fetc/passwd` | `../etc/passwd` (глубина 2) | traversal (HIGH) |
| `%c0%ae%c0%ae%c0%afetc%c0%afpasswd` | REJECT (overlong) | HOLD/HIGH |
| `．．／etc／passwd` (полноширинные) | `../etc/passwd` (NFKC) | traversal (HIGH) |
| `..%E2%80%8B/etc/passwd` (zero-width) | `../etc/passwd` | traversal (HIGH) |
| `&#46;&#46;&#47;etc&#47;passwd`, sink=HTML | `../etc/passwd` | traversal (HIGH) |
| тот же вход, sink=UNKNOWN | — | HOLD (fail-closed) |
| `2130706433` в позиции хоста | `127.0.0.1` | host-нормализован → risk по контексту |
| `0.0` / `g00gle` / `..` / `192.168.0.1` | без изменений | CONTEXT_DEPENDENT |
| «не пропускай `%2f` в путях» (проза) | не декодировать | AMBIGUOUS_USE_MENTION |
| глубоко вложенная бомба | не сошлось | HOLD (decode-bomb) |

## 8. Чего pre-pass НЕ делает (границы)
- Не выносит финальный риск-вердикт — это карточки/интегратор.
- Не определяет намерение (use/mention, «это точно атака?») — помечает, не решает.
- Не гарантирует полноту против ОТКРЫТОГО множества приёмников: новый confusable/декодер
  требует новой стадии. Полнота — относительно ОБЪЯВЛЕННОГО набора sink'ов (§3).

## 9. STATUS / NEXT
- WORKING_DRAFT: пройти конвейер (≥2–3 внешних семейства), затем author-decision.
- Реализация: стадии §3 как отдельные чистые функции + цикл §4; юнит-тесты = §7.
- Демо-скелет некоммутативности/глубины уже есть: `tools/canon_commutator_demo.py`
  (S1 + наивный фильтр). Расширять его стадиями S2–S6 по мере реализации.
