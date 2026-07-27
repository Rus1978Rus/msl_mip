#!/usr/bin/env python3
"""Non-commutativity of canonicalization — the 'commutator' [op0, op1], live.

Supporting artifact for conveyor_runs/OBSERVERS_CANONICALIZATION_2026-07-27.md.

Two canonicalization operations on a string:
  op0 = P : percent-decode, ONE pass   ( %2e -> . )
  op1 = F : 'flatten' — delete literal '../'  (a naive traversal filter/guard)

Security verdict: does '../' still reach through after processing?
  DANGER if the result still contains '../', else SAFE.

We apply them in BOTH orders:
  '0и1' = op1(op0(s)) = F(P(s))   (decode, then filter)
  '1и0' = op0(op1(s)) = P(F(s))   (filter, then decode)
When the verdicts DIFFER, the commutator [op0,op1] != 0 — order matters
(the discrete echo of ÂB̂ != B̂Â).

Then the fix: percent-decode to a FIXPOINT first (handles the %252e depth),
which makes the verdict order-INVARIANT again — canonicalization restores
'one verdict regardless of path' = mutation invariance.

Pure standard library. Run:  python3 canon_commutator_demo.py
"""
from urllib.parse import unquote


def P(s: str) -> str:        # op0: one pass of percent-decoding
    return unquote(s)


def F(s: str) -> str:        # op1: naive traversal filter — strip literal '../'
    return s.replace("../", "")


def tag(s: str) -> str:      # the guard's verdict
    return "DANGER" if "../" in s else "SAFE"


def P_fix(s: str, max_depth: int = 10) -> str:   # decode to a fixpoint (depth-aware)
    for _ in range(max_depth):
        d = unquote(s)
        if d == s:
            return s
        s = d
    return s


INPUTS = [
    "safe/report.txt",              # benign
    "../etc/passwd",                # literal traversal
    "%2e%2e/etc/passwd",            # dots percent-encoded
    "%2e%2e%2fetc%2fpasswd",        # dots + slash encoded
    "%252e%252e%252fetc/passwd",    # DOUBLE-encoded (the %252e case, depth)
    "....//etc/passwd",             # filter-bypass ('../' re-forms after one strip)
]


def main() -> None:
    print("=" * 84)
    print("КОММУТАТОР КАНОНИЗАЦИИ: порядок '0и1' vs '1и0' -> разный вердикт")
    print("=" * 84)
    print(f"{'вход':<30} {'0и1 F(P(s))':<12} {'1и0 P(F(s))':<12} {'коммутатор':<12} {'канон':<8}")
    print("-" * 84)
    for s in INPUTS:
        v01 = tag(F(P(s)))          # decode, then filter
        v10 = tag(P(F(s)))          # filter, then decode
        commutes = "= (0)" if v01 == v10 else "!= ЛОМАЕТ"
        canon = tag(P_fix(s))       # correct: decode to fixpoint, then check
        print(f"{s:<30} {v01:<12} {v10:<12} {commutes:<12} {canon:<8}")

    print("-" * 84)
    print("Чтение:")
    print("  * '0и1' и '1и0' расходятся на строках с 'ЛОМАЕТ' — коммутатор [P,F] != 0,")
    print("    порядок операций меняет вердикт (дискретное эхо ÂB̂ != B̂Â).")
    print("  * На %252e... одного прохода декода мало — '../' спрятан на ГЛУБИНЕ 2,")
    print("    наивные порядки видят SAFE, а на деле DANGER.")
    print("  * Столбец 'канон' (декод до неподвижной точки, потом проверка) даёт ОДИН")
    print("    правильный вердикт независимо от порядка — канонизация возвращает")
    print("    инвариантность ('один вердикт при любой маскировке').")

    print("\n" + "=" * 84)
    print("ГЛУБИНА (эхо %252e): один проход декода не вскрывает двойное кодирование")
    print("=" * 84)
    step = "%252e%252e%252fetc/passwd"
    print(f"  вход           : {step}   -> guard: {tag(step)}")
    for i in range(1, 4):
        nxt = unquote(step)
        note = "" if nxt == step else "  (декодировалось)"
        print(f"  декод, проход {i}: {nxt}   -> guard: {tag(nxt)}{note}")
        if nxt == step:
            print("  достигнута неподвижная точка (fixpoint) — дальше не меняется")
            break
        step = nxt


if __name__ == "__main__":
    main()
