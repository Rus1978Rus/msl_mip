#!/usr/bin/env python3
"""
msl_mip_runtime.py — рабочая программа MSL/MIP.

Принимает текст (аргументом командной строки или интерактивно),
прогоняет его через весь конвейер:

  1. сканирует текст, находит позиции знаков, для которых есть
     загруженная SIGN_CORE_CARD (сейчас: DOT, SOLIDUS, SKULL)
  2. для каждого знака — module_engine.process_sign (single-sign слой)
  3. для каждого результата — integrator_engine.process_output
     (решение по одиночному знаку)
  4. sequence_engine.process_sequence по всему тексту с полным
     known_signs реестром (CARD_SET_COMPLETENESS — см. код-ревью)
  5. sequence_integrator_engine.process_sequence_output (решение по
     найденным последовательностям)
  6. итоговый вердикт = самое строгое действие среди всех уровней

ЗАПУСК:
    python3 msl_mip_runtime.py "текст для анализа"
    python3 msl_mip_runtime.py        (без аргумента — спросит текст)
"""

from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "core"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "single_sign"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "sequence"))

from load_card import load_card
from module_engine import process_sign
from integrator_engine import process_output
from sequence_engine import process_sequence
from sequence_integrator_engine import process_sequence_output
from matchers import dot_matcher


# Порядок строгости действий — общий для single-sign и sequence решений
_SEVERITY = {
    "pass": 0,
    "log_only": 1,
    "queue_for_review": 2,
    "hold_pending_review": 3,
    "escalate_to_human": 4,
}

CARDS_DIR_CANDIDATES = [
    os.path.join(os.path.dirname(__file__), "cards"),
    "/mnt/user-data/uploads",
]

# Реальные имена файлов карточек (ARTIFACT_CONFIRMED), как они лежат
# в проекте. Если файл не найден — карточка просто не загрузится,
# рантайм продолжит работать с тем, что есть (явный warning).
CARD_FILENAMES = [
    "SIGN_CORE_CARD_DOT_U002E_GEN3_v0_3_RU__2_.md",
    "SIGN_CORE_CARD_SOLIDUS_U002F_GEN3_v0_3_RU__1_.md",
    "SIGN_CORE_CARD_SKULL_U1F480_GEN3_v0_3_RU__1_.md",
    "SIGN_CORE_CARD_SKULL_CROSSBONES_U2620_TEST_v0_1_RU.md",
]


def _find_card_file(filename: str) -> str:
    for d in CARDS_DIR_CANDIDATES:
        path = os.path.join(d, filename)
        if os.path.exists(path):
            return path
    return None


def load_all_cards() -> list:
    """Загружает все доступные карточки. Печатает предупреждение,
    если какая-то не найдена, но не падает."""
    cards = []
    for fname in CARD_FILENAMES:
        path = _find_card_file(fname)
        if path is None:
            print(f"[WARNING] Card not found: {fname} — sign will not be recognized")
            continue
        try:
            cards.append(load_card(path))
        except Exception as e:
            print(f"[WARNING] Failed to load {fname}: {e}")
    return cards


def scan_signs(text: str, cards: list) -> list:
    """STAGE: находит в тексте все позиции знаков, для которых есть
    загруженная карточка, и прогоняет каждую через module_engine."""
    sign_chars = {c.visible_form: c for c in cards}
    statuses = []
    for i, ch in enumerate(text):
        if ch in sign_chars:
            try:
                statuses.append(process_sign(sign_chars[ch], text, i))
            except Exception as e:
                print(f"[WARNING] Error processing sign {ch!r} at position {i}: {e}")
    return statuses


def most_severe(actions: list) -> str:
    if not actions:
        return "pass"
    return max(actions, key=lambda a: _SEVERITY.get(a, 0))


def analyze(text: str, cards: list) -> dict:
    """Полный прогон текста через все слои. Возвращает структуру
    отчёта для печати (и для возможного программного использования)."""
    known_signs = {c.visible_form for c in cards}

    # --- Single-sign слой ---
    sign_statuses = scan_signs(text, cards)
    single_sign_results = []
    single_actions = []
    for st in sign_statuses:
        decision = process_output(st)
        single_sign_results.append((st, decision))
        single_actions.append(decision.runtime_action)

    # --- Sequence слой ---
    seq_out = process_sequence(text, cards, sign_statuses=sign_statuses,
                               known_signs=known_signs)
    seq_decision = process_sequence_output(seq_out)

    # --- Итоговый вердикт ---
    final_action = most_severe(single_actions + [seq_decision.runtime_action])

    return {
        "text": text,
        "sign_statuses": sign_statuses,
        "single_sign_results": single_sign_results,
        "sequence_output": seq_out,
        "sequence_decision": seq_decision,
        "final_action": final_action,
    }


def print_report(report: dict) -> None:
    text = report["text"]
    print("=" * 60)
    print(f"TEXT: {text!r}")
    print("=" * 60)

    print("\n--- SINGLE SIGNS ---")
    if not report["single_sign_results"]:
        print("  (no signs from loaded cards found)")
    for st, decision in report["single_sign_results"]:
        print(f"  [{st.sign_offset_start}] {st.sign_codepoint} "
              f"interp={st.interpretation} risk={st.risk_level.value} "
              f"-> action={decision.runtime_action}")
        if st.risk_cases_triggered:
            print(f"        cases={st.risk_cases_triggered}")
        for w in st.output_warnings:
            print(f"        [!] {w}")

    print("\n--- SEQUENCES ---")
    seq_out = report["sequence_output"]
    if not seq_out.matches:
        print("  (no sequences found)")
    for m in seq_out.matches:
        rl = m.risk_level.value if hasattr(m.risk_level, "value") else m.risk_level
        print(f"  [{m.match_start}:{m.match_end}] {m.sc_id} {m.sequence!r} "
              f"risk={rl} card={m.candidate_source_card}")
    seq_dec = report["sequence_decision"]
    print(f"  -> action={seq_dec.runtime_action} ({seq_dec.action_rationale})")
    for w in seq_out.warnings:
        print(f"  [!] {w}")

    print("\n" + "=" * 60)
    print(f"FINAL VERDICT: {report['final_action'].upper()}")
    print("=" * 60)


def main():
    cards = load_all_cards()
    if not cards:
        print("[ERROR] No cards loaded — analysis impossible.")
        sys.exit(1)
    print(f"Cards loaded: {len(cards)} ({', '.join(c.codepoint for c in cards)})")

    suffix_source = dot_matcher.get_compound_suffix_source()
    if suffix_source == "LIVE_FETCH":
        print("Compound suffix list (PSL): up to date (just fetched)")
    elif suffix_source.startswith("CACHE_FROM_"):
        cached_at = suffix_source.replace("CACHE_FROM_", "")
        print(f"[!] Compound suffix list (PSL): could not update, "
              f"using cached copy from {cached_at}")
    else:
        print("[!] Compound suffix list (PSL): no network and no cached copy — "
              "using built-in minimal list (may not know "
              "about rare compound zones)")

    # ИСПРАВЛЕНО (MAJOR, найдено GPT-5.5, 2026-06-29): раньше источник
    # одиночных TLD (реестр IANA) не раскрывался вообще
    tld_source = dot_matcher.get_single_tld_source()
    if tld_source == "LIVE_FETCH":
        print("Single TLD list (IANA): up to date (just fetched)")
    elif tld_source.startswith("CACHE_FROM_"):
        cached_at = tld_source.replace("CACHE_FROM_", "")
        print(f"[!] Single TLD list (IANA): could not update, "
              f"using cached copy from {cached_at}")
    else:
        print("[!] Single TLD list (IANA): no network and no cached copy — "
              "using built-in minimal list (may not know "
              "about rare TLDs)")
    print()

    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
        report = analyze(text, cards)
        print_report(report)
    else:
        print("Enter text to analyze (Ctrl+C to exit):")
        while True:
            try:
                text = input("> ")
            except (EOFError, KeyboardInterrupt):
                print("\nExiting.")
                break
            if not text.strip():
                continue
            report = analyze(text, cards)
            print_report(report)
            print()


if __name__ == "__main__":
    main()
