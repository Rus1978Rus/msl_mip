#!/usr/bin/env python3
"""Zero-card difficulty verifier — mining written in the MSL/MIP style.

Answers the question: can we run the block hash through a "zero sign card"
plus the module/integrator pipeline to get the required number of leading
zeros?

Mining has two separate roles, and the zero-card fits only one of them:

  * SEARCH  (produce the zeros) — brute-force the nonce and SHA-256 it until
    the hash happens to start with N zeros. ONLY the hash can do this. The
    zero-card is a DETECTOR, not a generator: it recognizes zeros, it cannot
    make them, and a single verdict gives the search no hint which nonce to
    try next. So it can neither drive nor speed up the search.

  * VERIFY  (count the zeros) — given a finished hash, does it start with >= N
    zeros? THIS maps cleanly onto the pipeline, across all three layers:
        single-sign (zero card) -> "is this char a leading zero?"
        sequence layer          -> "a run of leading zeros anchored at offset 0"
        integrator policy       -> PASS (valid block) / HOLD (reject)

So the zero-card replaces the one-line `hash.startswith("0"*N)` check with an
interpretable verdict. It does NOT make mining any easier — every bit of the
work stays in the SHA-256 loop, which is not the pipeline.

Pure standard library. Run:  python3 mining_zero_card.py
"""

from mining_demo import Block, Transaction, COINBASE, BLOCK_SUBSIDY

# --- A minimal "sign card" for the digit zero, in MSL/MIP vocabulary ---
# Honest status: this card never went through the conveyor, so it is a
# WORKING_DRAFT — it illustrates the shape, it is not a reviewed card.
ZERO_CARD = {
    "codepoint": "U+0030",
    "visible_form": "0",
    "document_status": "WORKING_DRAFT",
}


def zero_match(text: str, offset: int):
    """STAGE_3 analog — the single-sign matcher for the zero card.

    Returns (safe_ids, risk_ids, interpretation), like dot_matcher.match.
    A zero is judged only by its immediate context: a zero is a *leading*
    zero iff every character before it is also a zero.
    """
    if offset < 0 or offset >= len(text) or text[offset] != ZERO_CARD["visible_form"]:
        return [], [], "non_zero"
    if all(ch == "0" for ch in text[:offset]):
        return ["SAFE_CASE_LEADING_ZERO"], [], "leading_zero"
    return ["SAFE_CASE_INTERIOR_ZERO"], [], "interior_zero"


def detect_leading_zero_run(hash_hex: str) -> dict:
    """SEQUENCE layer analog.

    The "N leading zeros" difficulty rule is a cross-sign pattern: a run of
    zero-signs anchored at offset 0 — the same shape the sequence layer uses
    for ../ or //. It counts the run by asking the single-sign matcher about
    each position, stopping at the first non-leading-zero.
    """
    run = 0
    for offset in range(len(hash_hex)):
        _, _, interpretation = zero_match(hash_hex, offset)
        if interpretation == "leading_zero":
            run += 1
        else:
            break
    return {"pattern": "LEADING_ZERO_RUN", "anchored_at": 0, "length": run}


def integrate(candidate: dict, difficulty: int) -> dict:
    """INTEGRATOR analog — policy maps the detected run against difficulty.

    Mirrors DEFAULT_ACTION_MAP: a satisfied rule is PASS (accept), an
    unsatisfied one surfaces as HOLD_PENDING_REVIEW (reject the block).
    """
    length = candidate["length"]
    if length >= difficulty:
        return {
            "verdict": "PASS",
            "action": "accept_block",
            "rationale": f"leading-zero run {length} >= difficulty {difficulty}",
        }
    return {
        "verdict": "HOLD_PENDING_REVIEW",
        "action": "reject_block",
        "rationale": f"leading-zero run {length} < difficulty {difficulty}",
    }


def mine_with_zero_card(block: Block, difficulty: int):
    """SEARCH via SHA-256, VERIFY via the zero-card pipeline.

    The loop body makes the split explicit: block.hash() is the search work,
    the pipeline (matcher -> sequence -> integrator) is only the verdict.
    """
    attempts = 0
    while True:
        digest = block.hash()                       # SEARCH: SHA-256 does the work
        candidate = detect_leading_zero_run(digest)  # VERIFY: single-sign + sequence
        verdict = integrate(candidate, difficulty)   # VERIFY: integrator policy
        if verdict["verdict"] == "PASS":
            return digest, attempts, candidate, verdict
        block.nonce += 1
        attempts += 1


def main() -> None:
    difficulty = 4
    print(f"Правило сложности: хеш блока должен начинаться с {difficulty} нулей.")
    print("Роль карточки нуля — ПРОВЕРКА (вердикт), а не ПОИСК.\n")

    def fresh_block():
        # Fixed timestamp -> deterministic, reproducible hashes. This
        # particular value yields a clean, representative run: the first
        # hash to reach the difficulty has exactly 4 leading zeros, found
        # in ~64.7k attempts (the theoretical average for 4 hex zeros is
        # 16**4 = 65536).
        return Block(
            index=1,
            prev_hash="0" * 64,
            transactions=[Transaction(COINBASE, "Майнер", BLOCK_SUBSIDY)],
            timestamp=1_700_000_005.0,
        )

    # --- Почему карточка нуля НЕ помогает искать ---
    print("=== Почему карточка нуля НЕ помогает ИСКАТЬ ===")
    block = fresh_block()
    for n in range(6):
        block.nonce = n
        candidate = detect_leading_zero_run(block.hash())
        print(
            f"  nonce={n}: хеш {block.hash()[:16]}...  ведущих нулей: {candidate['length']}"
        )
    print("  Длина серии скачет случайно — вердикт по одному хешу ничего не говорит")
    print("  о том, какой nonce брать следующим. Поиск ведёт только перебор SHA-256.\n")

    # --- Майним: SHA-256 ищет, модуль + интегратор выносят вердикт ---
    print("=== Майним: SHA-256 ИЩЕТ, модуль + интегратор ПРОВЕРЯЮТ ===")
    block = fresh_block()
    digest, attempts, candidate, verdict = mine_with_zero_card(block, difficulty)
    print(f"  SHA-256 перебрал {attempts} nonce (это ПОИСК, работа не пайплайна)")
    print(f"  найденный хеш: {digest}")
    print(
        f"  single-sign + sequence -> ведущих нулей: {candidate['length']} "
        f"(pattern={candidate['pattern']}, anchored_at={candidate['anchored_at']})"
    )
    print(f"  integrator -> вердикт {verdict['verdict']}, действие {verdict['action']}")
    print(f"    обоснование: {verdict['rationale']}\n")

    # --- Проверка отклоняет недобранный блок ---
    print("=== Тот же пайплайн отклоняет недобранный блок ===")
    block = fresh_block()  # nonce=0, почти наверняка < 4 нулей
    digest0 = block.hash()
    candidate0 = detect_leading_zero_run(digest0)
    verdict0 = integrate(candidate0, difficulty)
    print(f"  хеш при nonce=0: {digest0}")
    print(
        f"  ведущих нулей: {candidate0['length']} < {difficulty} "
        f"-> вердикт {verdict0['verdict']}, действие {verdict0['action']}"
    )
    print(f"    обоснование: {verdict0['rationale']}\n")

    print(
        "Вывод: карточка нуля через модуль/sequence/интегратор — это честный\n"
        "ВАЛИДАТОР сложности (заменяет строку hash.startswith('0'*N) вердиктом\n"
        "PASS/HOLD). Но всю работу по ДОБЫЧЕ нулей делает SHA-256 в цикле выше —\n"
        "пайплайн её не ускоряет и не заменяет. Карточка-детектор нули узнаёт,\n"
        "но не производит."
    )


if __name__ == "__main__":
    main()
