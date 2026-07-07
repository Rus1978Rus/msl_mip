#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIMULATION_GATE для SOLIDUS_SCHEME_PATCH — постоянный набор.
Расширен по SIMULATION_GATE_REVIEW (6 ревьюеров, NEEDS_MORE_TESTS,
2026-07-07): добавлены классы краевых случаев (регистр схемы, схема с
+/-/., тройной слэш, невалидная схема, граница idx, комбинации,
класс "не падает").

Запуск: python3 gate_solidus_scheme.py
"""
import subprocess, sys, os

# кросс-платформенный запуск: рантайм выводит UTF-8 (кириллица в interp,
# эмодзи ☠), но Windows по умолчанию декодирует subprocess в cp1251 →
# вердикт не находится в битой строке. Форсируем UTF-8 всюду.
_ENV = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")

def _run(text):
    return subprocess.run(
        [sys.executable, "msl_mip_runtime.py", text],
        capture_output=True, text=True,
        encoding="utf-8", errors="replace", env=_ENV,
    )

# (вход, ожидаемый_вердикт, комментарий)
# вердикт: PASS | HOLD  (HOLD = HOLD_PENDING_REVIEW)
CASES = [
    # --- базовые: цель патча (шум схемы убран) ---
    ("http://example.com/page", "PASS", "чистый URL — шум // убран"),
    ("https://github.com/user/repo", "PASS", "https чистый"),
    ("ftp://server/file", "PASS", "ftp схема"),
    # --- @ различитель не сломан ---
    ("http://paypal.com@evil.ru", "HOLD", "фишинг @ со схемой"),
    ("подпишись на @user@mastodon.social", "PASS", "федеративный handle"),
    ("ivan@example.com", "PASS", "обычная почта"),
    ("https://secure-paypal.com@192.168.1.5/verify", "HOLD", "brand+IP @"),
    ("http://evil.ru@paypal.com", "HOLD", "@ HIGH — флаг НЕ понизил соседа"),
    # --- // без валидной схемы = HIGH (path-traversal сохранён) ---
    ("a//b", "HOLD", "// без схемы = HIGH"),
    (":://evil.com", "HOLD", "Q1: псевдосхема (нет буквы) НЕ понижена"),
    ("://evil.com", "HOLD", "':// в начале — idx граница, не падает, HIGH"),
    ("1http://example", "HOLD", "схема с цифры невалидна (RFC) → HIGH"),
    # --- Q4: enum-агрегация, множественные // не падают ---
    ("http://a//b", "HOLD", "Q4: схема // + path // — enum max без краха"),
    ("http:///path", "HOLD", "тройной слэш — второй // без схемы HIGH"),
    # --- регистр и спецсимволы схемы (RFC 3986 §3.1) ---
    ("HTTP://evil.com", "PASS", "схема верхний регистр (case-insensitive)"),
    ("HtTp://evil.com", "PASS", "смешанный регистр схемы"),
    ("coap+tcp://host/path", "PASS", "схема с '+' валидна"),
    ("view-source://example", "PASS", "схема с '-' валидна"),
    # --- комбинации @ + точка + // ---
    ("http://paypal.com.security-check.ru/verify", "HOLD", "схема + точка-подмена"),
    ("paypal.com.security-check.ru/verify", "HOLD", "точка-подмена без схемы (регрессия)"),
    # --- контроль: другие знаки целы ---
    ("я тебя отравлю ☠", "HOLD", "☠ угроза — контроль"),
]

# класс "не падает" (Q4) — только проверка отсутствия исключений
NO_CRASH = ["http://a//b//c", "scheme://///", ":////", "http://a//b//c//d",
            "://", "//", ":"]

def verdict_of(out):
    if "HOLD_PENDING_REVIEW" in out: return "HOLD"
    if "QUEUE" in out: return "QUEUE"
    if "PASS" in out: return "PASS"
    return "?"

def main():
    ok = 0
    print("=== SOLIDUS_SCHEME_PATCH gate ===")
    for text, exp, note in CASES:
        r = _run(text)
        got = verdict_of(r.stdout)
        mark = "✓" if got == exp else "✗"
        if got == exp: ok += 1
        print(f"  {mark} [{got:4}/{exp:4}] {note}")
    print(f"\n  вердикты: {ok}/{len(CASES)}")

    print("\n=== класс 'не падает' (Q4) ===")
    nc_ok = 0
    for text in NO_CRASH:
        r = _run(text)
        crash = "Traceback" in r.stderr or "Error" in r.stderr
        mark = "✓" if not crash else "✗ КРАШ"
        if not crash: nc_ok += 1
        print(f"  {mark} {text!r}")
    print(f"\n  без краха: {nc_ok}/{len(NO_CRASH)}")

    total = ok + nc_ok
    grand = len(CASES) + len(NO_CRASH)
    print(f"\n=== ИТОГО: {total}/{grand} ===")
    sys.exit(0 if total == grand else 1)

if __name__ == "__main__":
    main()
