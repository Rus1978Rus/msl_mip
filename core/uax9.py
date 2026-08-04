# -*- coding: utf-8 -*-
"""UAX #9 Unicode Bidirectional Algorithm, revision 50 (Unicode 16.0.0).

Basis: AUTHOR_DECISION_20260804_D-BIDI-REORDER, phase 2. Phase 1 could only say that an
override HOLDS a span; only the real algorithm can say whether the visible order actually
CHANGES, which is what closes residual R5 (a no-op override inside an RTL paragraph
raising a queue it does not deserve) and what lets the human be shown the difference.

A hand-rolled "strip and compare" was explicitly forbidden by the round: it is not
conformant and drifts between implementations. This module therefore implements the
normative rules (P2-P3, X1-X10, W1-W7, N0-N2, I1-I2, L1-L2) and is validated against the
official BidiTest.txt (493502 data lines) and BidiCharacterTest.txt (91707) for 16.0.0 --
see tests/gate_uax9_conformance.py. Character classes come from unicodedata (pinned UCD
16.0.0); only the bracket pairs (rule N0) need a repo artifact, since the stdlib does not
expose Bidi_Paired_Bracket.

The result is the REFERENCE display order under this pinned standard. It is deliberately
NOT called "what the user sees": consumers may apply higher-level protocols, and UAX#9
4.2 even allows conforming systems with no bidi support at all (named residual
BYPASS_CONSUMER_RENDERER).
"""
import os
import unicodedata

MAX_DEPTH = 125

# X9-removed types plus BN.
_REMOVED = frozenset(("RLE", "LRE", "RLO", "LRO", "PDF", "BN"))
_ISOLATE_INITIATORS = frozenset(("LRI", "RLI", "FSI"))
_NEUTRAL_OR_ISOLATE = frozenset(("B", "S", "WS", "ON", "FSI", "LRI", "RLI", "PDI"))
_STRONG = frozenset(("L", "R", "AL"))

_BRACKETS_FILE = "BidiBrackets.txt"
_DEFAULT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "unicode")
_BRACKETS = None            # {cp: (paired_cp, 'o'|'c')}


def _load_brackets(base_dir=None):
    global _BRACKETS
    if _BRACKETS is not None:
        return _BRACKETS
    path = os.path.join(base_dir or _DEFAULT_DIR, _BRACKETS_FILE)
    table = {}
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            for line in f:
                line = line.split("#", 1)[0].strip()
                if not line:
                    continue
                parts = [p.strip() for p in line.split(";")]
                if len(parts) < 3:
                    continue
                table[int(parts[0], 16)] = (int(parts[1], 16), parts[2])
    except OSError:
        table = {}
    _BRACKETS = table
    return table


def _canonical_bracket(cp):
    """BD16 note: brackets are matched under canonical equivalence, which in practice
    means U+2329/U+232A and U+3008/U+3009 must pair with each other."""
    return {0x3008: 0x2329, 0x3009: 0x232A}.get(cp, cp)


def classes_of(text):
    return [unicodedata.bidirectional(ch) or "L" for ch in text]


def _matching_pdi(types, i):
    """BD9: index of the PDI matching the isolate initiator at i, else len(types)."""
    depth = 1
    for j in range(i + 1, len(types)):
        t = types[j]
        if t in _ISOLATE_INITIATORS:
            depth += 1
        elif t == "PDI":
            depth -= 1
            if depth == 0:
                return j
    return len(types)


def paragraph_level(types, start=0, end=None):
    """P2/P3: first strong type, skipping isolate runs."""
    if end is None:
        end = len(types)
    i = start
    while i < end:
        t = types[i]
        if t in _ISOLATE_INITIATORS:
            i = _matching_pdi(types, i)
            if i >= end:
                break
            i += 1
            continue
        if t == "L":
            return 0
        if t in ("R", "AL"):
            return 1
        i += 1
    return 0


def _explicit_levels(types, para_level):
    """X1-X8. Returns (levels, types_after_override) with X9-removed types intact so
    callers can report them as 'x'."""
    n = len(types)
    levels = [para_level] * n
    result = list(types)
    stack = [(para_level, "N", False)]        # (level, override, isolate)
    overflow_isolate = overflow_embedding = valid_isolate = 0

    def next_odd(lvl):
        return lvl + 1 if lvl % 2 == 0 else lvl + 2

    def next_even(lvl):
        return lvl + 2 if lvl % 2 == 0 else lvl + 1

    for i, t in enumerate(types):
        if t in ("RLE", "LRE", "RLO", "LRO"):
            levels[i] = stack[-1][0]          # X9 will drop it; keep for 'x' reporting
            new = next_odd(stack[-1][0]) if t in ("RLE", "RLO") \
                else next_even(stack[-1][0])
            override = "R" if t == "RLO" else ("L" if t == "LRO" else "N")
            if new <= MAX_DEPTH and overflow_isolate == 0 and overflow_embedding == 0:
                stack.append((new, override, False))
            elif overflow_isolate == 0:
                overflow_embedding += 1
        elif t in _ISOLATE_INITIATORS:
            kind = t
            if t == "FSI":
                inner_end = _matching_pdi(types, i)
                kind = "RLI" if paragraph_level(types, i + 1, inner_end) == 1 else "LRI"
            levels[i] = stack[-1][0]
            if stack[-1][1] != "N":
                result[i] = stack[-1][1]
            new = next_odd(stack[-1][0]) if kind == "RLI" else next_even(stack[-1][0])
            if new <= MAX_DEPTH and overflow_isolate == 0 and overflow_embedding == 0:
                valid_isolate += 1
                stack.append((new, "N", True))
            else:
                overflow_isolate += 1
        elif t == "PDI":
            if overflow_isolate > 0:
                overflow_isolate -= 1
            elif valid_isolate:
                overflow_embedding = 0
                while not stack[-1][2]:
                    stack.pop()
                stack.pop()
                valid_isolate -= 1
            levels[i] = stack[-1][0]
            if stack[-1][1] != "N":
                result[i] = stack[-1][1]
        elif t == "PDF":
            levels[i] = stack[-1][0]
            if overflow_isolate > 0:
                pass
            elif overflow_embedding > 0:
                overflow_embedding -= 1
            elif not stack[-1][2] and len(stack) >= 2:
                stack.pop()
        elif t == "B":
            # X8: paragraph separator -- reset to the paragraph level.
            stack = [(para_level, "N", False)]
            overflow_isolate = overflow_embedding = valid_isolate = 0
            levels[i] = para_level
        else:
            levels[i] = stack[-1][0]
            if stack[-1][1] != "N":
                result[i] = stack[-1][1]
    return levels, result


def _isolating_run_sequences(types, levels, para_level):
    """X10/BD13: build isolating run sequences over the X9-filtered indices, with sos/eos."""
    n = len(types)
    kept = [i for i in range(n) if types[i] not in _REMOVED]
    if not kept:
        return []
    # Level runs over kept indices.
    runs = []
    cur = [kept[0]]
    for idx in kept[1:]:
        if levels[idx] == levels[cur[-1]]:
            cur.append(idx)
        else:
            runs.append(cur)
            cur = [idx]
    runs.append(cur)

    run_of = {}
    for r_i, run in enumerate(runs):
        for idx in run:
            run_of[idx] = r_i

    used = [False] * len(runs)
    sequences = []
    for r_i, run in enumerate(runs):
        if used[r_i]:
            continue
        first = run[0]
        # A sequence starts with a run whose first char is not a PDI matching an initiator.
        if types[first] == "PDI":
            # Does it match an initiator? If so, this run continues another sequence.
            matched = False
            depth = 1
            for j in range(first - 1, -1, -1):
                t = types[j]
                if t == "PDI":
                    depth += 1
                elif t in _ISOLATE_INITIATORS:
                    depth -= 1
                    if depth == 0:
                        matched = _matching_pdi(types, j) == first
                        break
            if matched:
                continue
        seq = list(run)
        used[r_i] = True
        while True:
            last = seq[-1]
            if types[last] not in _ISOLATE_INITIATORS:
                break
            pdi = _matching_pdi(types, last)
            if pdi >= n or pdi not in run_of or used[run_of[pdi]]:
                break
            nxt = run_of[pdi]
            seq.extend(runs[nxt])
            used[nxt] = True
        sequences.append(seq)

    out = []
    for seq in sequences:
        level = levels[seq[0]]
        # sos: compare with the previous non-removed character.
        prev = None
        for j in range(seq[0] - 1, -1, -1):
            if types[j] not in _REMOVED:
                prev = j
                break
        prev_level = levels[prev] if prev is not None else para_level
        sos = "R" if max(level, prev_level) % 2 else "L"
        # eos: if the sequence ends with an unmatched isolate initiator, use para level.
        last = seq[-1]
        if types[last] in _ISOLATE_INITIATORS and _matching_pdi(types, last) >= n:
            next_level = para_level
        else:
            nxt = None
            for j in range(last + 1, n):
                if types[j] not in _REMOVED:
                    nxt = j
                    break
            next_level = levels[nxt] if nxt is not None else para_level
        eos = "R" if max(levels[last], next_level) % 2 else "L"
        out.append((seq, sos, eos, level))
    return out


def _resolve_weak_and_neutral(types, seq, sos, eos, level, text=None):
    """W1-W7, N0-N2 over one isolating run sequence (types is mutated in place)."""
    e = "L" if level % 2 == 0 else "R"
    o = "R" if e == "L" else "L"

    # W1: NSM takes the type of the previous character.
    prev = sos
    for idx in seq:
        if types[idx] == "NSM":
            types[idx] = "ON" if prev in _ISOLATE_INITIATORS or prev == "PDI" else prev
        prev = types[idx]

    # W2: EN with last strong AL becomes AN.
    strong = sos
    for idx in seq:
        t = types[idx]
        if t in _STRONG:
            strong = t
        elif t == "EN" and strong == "AL":
            types[idx] = "AN"

    # W3: AL becomes R.
    for idx in seq:
        if types[idx] == "AL":
            types[idx] = "R"

    # W4: single ES between EN, single CS between two numbers of the same type.
    for k in range(1, len(seq) - 1):
        idx, before, after = seq[k], types[seq[k - 1]], types[seq[k + 1]]
        t = types[idx]
        if t == "ES" and before == "EN" and after == "EN":
            types[idx] = "EN"
        elif t == "CS" and before == after and before in ("EN", "AN"):
            types[idx] = before

    # W5: a run of ET adjacent to EN becomes EN.
    k = 0
    while k < len(seq):
        if types[seq[k]] == "ET":
            j = k
            while j < len(seq) and types[seq[j]] == "ET":
                j += 1
            before = types[seq[k - 1]] if k > 0 else sos
            after = types[seq[j]] if j < len(seq) else eos
            if before == "EN" or after == "EN":
                for m in range(k, j):
                    types[seq[m]] = "EN"
            k = j
        else:
            k += 1

    # W6: remaining separators and terminators become ON.
    for idx in seq:
        if types[idx] in ("ET", "ES", "CS"):
            types[idx] = "ON"

    # W7: EN with last strong L becomes L.
    strong = sos
    for idx in seq:
        t = types[idx]
        if t in ("L", "R"):
            strong = t
        elif t == "EN" and strong == "L":
            types[idx] = "L"

    # N0: paired brackets (needs the actual characters).
    if text is not None:
        _resolve_brackets(types, seq, sos, e, o, text)

    # N1: a run of NIs between matching strong directions takes that direction.
    def strong_dir(t):
        if t in ("L",):
            return "L"
        if t in ("R", "EN", "AN"):
            return "R"
        return None

    k = 0
    while k < len(seq):
        if types[seq[k]] in _NEUTRAL_OR_ISOLATE:
            j = k
            while j < len(seq) and types[seq[j]] in _NEUTRAL_OR_ISOLATE:
                j += 1
            before = strong_dir(types[seq[k - 1]]) if k > 0 else sos
            after = strong_dir(types[seq[j]]) if j < len(seq) else eos
            if before is not None and before == after:
                for m in range(k, j):
                    types[seq[m]] = before
            else:
                # N2: otherwise take the embedding direction.
                for m in range(k, j):
                    types[seq[m]] = e
            k = j
        else:
            k += 1


def _resolve_brackets(types, seq, sos, e, o, text):
    """N0/BD16: bracket pairs within the isolating run sequence."""
    brackets = _load_brackets()
    if not brackets:
        return
    stack = []
    pairs = []
    for pos, idx in enumerate(seq):
        if types[idx] != "ON":
            continue
        info = brackets.get(ord(text[idx]))
        if not info:
            continue
        paired, kind = info
        if kind == "o":
            if len(stack) == 63:
                return                       # BD16: stop processing entirely
            stack.append((_canonical_bracket(paired), pos))
        else:
            target = _canonical_bracket(ord(text[idx]))
            for si in range(len(stack) - 1, -1, -1):
                if stack[si][0] == target:
                    pairs.append((stack[si][1], pos))
                    del stack[si:]
                    break
    pairs.sort()

    def strong_of(t):
        if t == "L":
            return "L"
        if t in ("R", "EN", "AN"):
            return "R"
        return None

    for open_pos, close_pos in pairs:
        found_e = found_o = False
        for pos in range(open_pos + 1, close_pos):
            d = strong_of(types[seq[pos]])
            if d == e:
                found_e = True
                break
            if d == o:
                found_o = True
        if found_e:
            new = e
        elif found_o:
            # Check the preceding context.
            context = sos
            for pos in range(open_pos - 1, -1, -1):
                d = strong_of(types[seq[pos]])
                if d is not None:
                    context = d
                    break
            new = o if context == o else e
        else:
            continue
        types[seq[open_pos]] = new
        types[seq[close_pos]] = new
        # Any NSM following a paired bracket that changed takes the same type.
        for pos in (open_pos, close_pos):
            for nxt in range(pos + 1, len(seq)):
                if unicodedata.bidirectional(text[seq[nxt]]) == "NSM":
                    types[seq[nxt]] = new
                else:
                    break


def resolve_levels(types_in, para_level=None, text=None):
    """Full resolution. Returns (levels, types, para_level, removed_flags)."""
    types = list(types_in)
    if para_level is None:
        para_level = paragraph_level(types)
    original = list(types)
    levels, types = _explicit_levels(types, para_level)
    removed = [t in _REMOVED for t in original]

    for seq, sos, eos, level in _isolating_run_sequences(original, levels, para_level):
        _resolve_weak_and_neutral(types, seq, sos, eos, level, text)
        # I1/I2: implicit levels.
        for idx in seq:
            t = types[idx]
            if level % 2 == 0:
                if t == "R":
                    levels[idx] = level + 1
                elif t in ("AN", "EN"):
                    levels[idx] = level + 2
                else:
                    levels[idx] = level
            else:
                if t in ("L", "EN", "AN"):
                    levels[idx] = level + 1
                else:
                    levels[idx] = level

    # L1: reset separators and trailing whitespace to the paragraph level.
    reset = True
    for i in range(len(original) - 1, -1, -1):
        t = original[i]
        if t in ("B", "S"):
            levels[i] = para_level
            reset = True
        elif t in ("WS", "FSI", "LRI", "RLI", "PDI") or t in _REMOVED:
            if reset:
                levels[i] = para_level
        else:
            reset = False
    return levels, types, para_level, removed


def reorder(levels, removed):
    """L2: return the visual order as indices into the original string, X9-removed
    characters omitted."""
    idx = [i for i in range(len(levels)) if not removed[i]]
    if not idx:
        return []
    lv = [levels[i] for i in idx]
    highest = max(lv)
    lowest_odd = min((l for l in lv if l % 2), default=highest + 1)
    order = list(idx)
    level = highest
    while level >= lowest_odd:
        i = 0
        while i < len(order):
            if levels[order[i]] >= level:
                j = i
                while j < len(order) and levels[order[j]] >= level:
                    j += 1
                order[i:j] = order[i:j][::-1]
                i = j
            else:
                i += 1
        level -= 1
    return order


def visual_order(text, para_level=None):
    """Convenience: reference visual order of `text` as a list of original indices."""
    types = classes_of(text)
    levels, _types, _pl, removed = resolve_levels(types, para_level, text)
    return reorder(levels, removed)
