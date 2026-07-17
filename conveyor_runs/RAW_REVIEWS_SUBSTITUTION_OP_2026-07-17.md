ЧАСТНЫЙ АВТОРСКИЙ ПРОЕКТ / COMMERCIAL USE PROHIBITED

DOCUMENT_ID: RAW_REVIEWS_SUBSTITUTION_OP_2026-07-17
DOCUMENT_TYPE: RAW_REVIEW_BUNDLE (сверяемый источник — НЕ свод)
DATE: 2026-07-17
PACKET: CONVEYOR_PACKET_SUBSTITUTION_OP_2026-07-17 (O2 — выбор op)
NOTE: 7 присланных блоков. Классификация Claude Code (по факту текста):
  R1 GPT-5.6 (OpenAI)         — реальный вердикт
  R2 Gemini (Gemini-1.5-Pro)  — реальный вердикт
  R3 UNNAMED (нет REVIEWER/FAMILY) — реальный, LOW_RELIABILITY (фантом-файл-ссылка;
     рассуждение содержит debunked-факт «TAG не Cf / вне 138» — на деле TAG=97⊂138)
  R4 DeepSeek-R1 (reasoning)  — реальный вердикт (в этот раунд без фабрикаций)
  R5 (нет заголовка)          — PACKET_ECHO (нет оценки по (а-г), нет своего вердикта)
  R6 (нет заголовка)          — META_ASSESSMENT пакета (предсказывает ревьюеров)
  R7 Gemini (Gemini-1.5-Pro)  — ДУБЛИКАТ R2 дословно (не независим)
Реальных независимых op-вердиктов: 4 (R1,R2,R3-caveated,R4). Семейств названо 3.

============================================================
R1 — GPT-5.6 Thinking / OpenAI GPT
============================================================
RANKED_OUTCOME: OP-4 SURVIVES RANK 1; OP-1 SURVIVES_AS_TARGET_PROFILE RANK 2;
OP-2/OP-3 SURVIVE_AS_EXPLICIT_MAXIMAL_STRIP_PROFILE, NOT_AS_CANONICAL_UNIVERSAL_OP;
OP-OTHER REQUIRED (add IDNA_MAPPING, IDENTIFIER_PROFILE, BIDI_CONTROL_DETECTION,
TAG_STRIP, NFC_PASSWORD_COMPARISON).
RECOMMENDATION: canonical_op should NOT be one destructive transform; should be a
VERSIONED TARGET-PROFILE SET: op(target_profile, stage, version).
OP-2==OP-3 within domain 138: YES (FINDING_STATUS VERIFIED); recommend MERGE as
OP-MAXIMAL-CLASS-STRIP. Difference only when set extends beyond Cf (variation
selectors) — not now.
Per-op: OP-1 realistic YES (after precise profile), completeness LOW_TO_MEDIUM,
false-pos MEDIUM, computable CONDITIONAL; survives as profile, not universal canon.
OP-2/3 realistic YES as strict profile, complete inside 138, false-pos VERY_HIGH,
stable HIGH; survive as MAXIMAL_STRIP_TEST_PROFILE, cut as single canonical meaning.
OP-4 realistic YES, completeness HIGHEST, false-pos CONTROLLABLE, stable if versioned;
STRONG SURVIVOR, RECOMMENDED CANON.
Added ops: OP-5 IDNA_MAPPING (domains, REQUIRED), OP-6 UAX31 IDENTIFIER_PROFILE
(REQUIRED), OP-7 BIDI_CONTROL_DETECTION (source code, REQUIRED), OP-8 TAG_STRIP
(LLM, REQUIRED), OP-9 PASSWORD_NFC (NIST NFC before hashing — NOT strip/NFKC),
OP-10 UTS-39 SKELETON (visual confusables — KEEP_ADJACENT, NOT part of core
invisible op).
LIST_COMPLETENESS: NOT EXHAUSTIVE.
Cites: UTS-46/IDNA2008, UAX-31, NIST NFC, Trojan Source CVE-2021-42574, OWASP
Unicode smuggling / tag characters.
FINAL: accept OP-4 as canonical meta-op with a versioned minimum target-profile set;
form substitution(X,Y,target_profile,stage,unicode_version,profile_version) →
YES/NO/UNVERIFIABLE.

============================================================
R2 — Gemini / Gemini-1.5-Pro
============================================================
OP-1: (а) YES (naive login sanitizers, web regex s/[​-‍﻿]//g, chat
filters); (б) LOW (misses Trojan Source bidi + LLM tags); (в) LOW within PURE subset;
(г) LOW stability ("zero-width" not a single UCD bool). STATUS: CUT (on Б and Г).
OP-2: (а) YES (strict UAX-31 parsers, ML preprocessors, aggressive WAF); (б) MAXIMAL;
(в) CRITICAL — stripping whole 138 makes all 138 mutually substitutable, full graph
138×138, fatal noise (ZWSP↔RLO); (г) absolutely stable. STATUS: CUT (on В).
OP-3: (а)-(г) identical to OP-2. EXPLICIT CONFIRMATION: within fixed 138 (Cf∧DI)
OP-2 and OP-3 mathematically IDENTICAL, both wipe the set, meaningless full graph.
STATUS: CUT (on В).
OP-4: (а) YES (real internet architecture: browsers IDNA, compilers bidi-linters,
DBs NFKC); (б) ABSOLUTE; (в) MINIMAL (substitutability localized per vector); (г)
stable (each op_i on an industrial standard). STATUS: SURVIVES.
OP-OTHER / EXHAUSTIVENESS: §3 algorithmically exhaustive at MACRO level (pure
properties vs combinations) but hides concrete industrial standards. Treat OP-4 as a
container that MUST include: OP-IDNA2008 (domains), OP-NFKC (auth/passwords),
OP-BIDI-STRIP (source code).
RANKED_OUTCOME: SURVIVES OP-4; CUT OP-1, OP-2, OP-3.
RECOMMENDATION: OP-4 (набор). No singular canonical op exists (no single universal
target). Compute dynamically over R = {op_idna, op_nfkc, op_bidi, op_naive_strip};
fits the layered compute-on-demand form.

============================================================
R3 — UNNAMED (нет REVIEWER/MODEL_FAMILY) — LOW_RELIABILITY
============================================================
[Провенанс: без идентификации семейства. Содержит фантом-ссылку
"sandbox:///mnt/agents/output/conveyor_packet_substitution_op_review.txt" +
«Ревью сохранено» — не наш файл, трактуется как несуществующее. В рассуждении
вслух приходит к ЛОЖНОМУ выводу «TAG-символы E0020-E007F — не Cf, вне 138» — на
деле TAG=97 членов класса, все Cf (§1 пакета). BASIS частично на неверной картине.]
Per-op (итоговая таблица): OP-1 (+~+~) SURVIVE; OP-2 (++−+) CUT на (в); OP-3 (=OP-2)
CUT; OP-4 (+++~) SURVIVE; IDNA (++++) SURVIVE для доменов; NFKC (+~++) SURVIVE для
паролей; UTS-39 (−−−−) CUT неприменима к невидимкам; eff.width (−−−−) CUT не
реализовано.
OP-2/3 CUT на (в): полный граф (назвал 18906 пар). OP-1 default для неизвестной мишени.
RECOMMENDATION: канон = НАБОР per-мишень, не одна op; default = OP-1. Набор =
{OP-1, OP-2/Cf-strip, bidi-detect, tag-strip, IDNA-mapping, NFKC}.
OP-2≡OP-3 внутри 138: ДА, тождественны.
LIST_COMPLETENESS: сказал «ДА, исчерпывающий для невидимок» (при этом сам добавил
IDNA/NFKC — внутренне противоречиво).
FORK_STATUS (его): CLOSED (op=набор per-мишень) + OPEN (какие op_i в default; граница
zero-width для OP-1).

============================================================
R4 — DeepSeek-R1 / reasoning-transformer
============================================================
OP-1: (а) YES (наивные санитайзеры логинов/комментов/CMS); (б) НЕ ПОЛНА (пропускает
directional/Trojan Source CVE-2021-42574, теги, deprecated); (в) полный граф на
PURE-ядре ~23; (г) «zero-width» без единого UCD-свойства, задавать списком. ВЕРДИКТ
CUT на (б).
OP-2/OP-3: (а) YES (строгие нормализаторы UAX-31, LLM-защиты); (б) ПОЛНА внутри 138;
(в) ИЗБЫТОЧНА — полный граф C(138,2)=9453 неупорядоченных пары, «всё со всем», шум
для witness; (г) версионно-стабильна. ВЕРДИКТ CUT на (в). OP-2≡OP-3 подтверждено.
OP-4: (а) YES — единственный подход, отражающий реальность (домены IDNA/UTS-46+
RFC5894; код bidi-detect CVE-2021-42574; LLM tag-strip/Cf-strip; логины/пароли
zero-width/NFKC); (б) условно полна; (в) значительно меньше (граф per-мишень
осмыслен); (г) считаема per-op, стабильность варьируется. ВЕРДИКТ SURVIVE по всем.
OP-OTHER: новых op НЕ предлагает — считает §3 исчерпывающим (IDNA/bidi — экземпляры
внутри набора).
RANKED_OUTCOME: SURVIVE OP-4; CUT OP-1 (неполна), OP-2/3 (избыточны).
RECOMMENDATION: принять OP-4 — канон = НАБОР, не одна op. Минимальный набор:
zero-width-strip, Cf-strip, IDNA-mapping, bidi-detect. compute(op) на лету +
SIGN_RELATIONS. Ссылается на архитектуру D-SUBSTITUTION-FORM.
LIST_COMPLETENESS: исчерпывающий. OP-2≡OP-3: подтверждаю.

============================================================
R5 — (нет заголовка) — PACKET_ECHO (НЕ вердикт)
============================================================
Пересказал пакет (суть, факты, предложенные op, критерии, ожидаемый выход, границы),
дал «что требуется от автора/координатора», «риски и замечания», «рекомендацию по
процедуре свода», предложил сделать шаблон-форму/текст рассылки. НЕ оценил ни одну op
по (а)(б)(в)(г); своего RANKED/RECOMMENDATION нет («OP-4 наиболее практичен» — эхо
формулировки пакета). OP-2≡OP-3 не подтвердил сам — переложил «ревьюерам нужно
подтвердить». Нет REVIEWER/FAMILY. → ИСКЛЮЧЁН из счёта вердиктов.

============================================================
R6 — (нет заголовка) — META_ASSESSMENT пакета (не равноправный вердикт)
============================================================
Оценивает КАЧЕСТВО пакета и готовность к раздаче («ASSESSMENT FOR DISPATCH»,
«READY TO SEND TO ≥3 REVIEWERS?»). Раздел «PREDICTED REVIEWER FINDINGS» —
предсказывает, что скажут ревьюеры, а не свой вердикт. Нет REVIEWER/FAMILY.
Содержательная позиция (извлечена): OP-1 как default-канон + OP-4 набор как
framework поверх. OP-2/3 CUT (K₁₃₈=9453 шум). OP-3 CUT как избыточный/менее
стабильный (внутренняя нестыковка: сам признал OP-2≡OP-3). OP-2≡OP-3: подтверждает
(K₁₃₈). LIST: НЕ исчерпывающий — предлагает OP-5 NFKC, OP-6 контекстная-по-позиции,
OP-7 adversarial-meta. Мета-замечание: сделать явным вопрос «single op vs набор
обязателен» (мягкая критика постановки, не hard LOOPHOLE).

============================================================
R7 — Gemini / Gemini-1.5-Pro — ДУБЛИКАТ R2
============================================================
Текст ДОСЛОВНО идентичен R2 (тот же разбор OP-1..4, тот же RANKED SURVIVES OP-4 /
CUT OP-1,2,3, та же RECOMMENDATION, тот же R={op_idna,op_nfkc,op_bidi,op_naive_strip}).
НЕ независимый вердикт. → ИСКЛЮЧЁН из счёта (повтор R2).

END_OF_RAW_BUNDLE
