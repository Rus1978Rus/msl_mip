# Conveyor Runs — Worked Examples / Примеры конвейерных прогонов

This folder answers a common question from external reviewers: "the
CONVEYOR_RUN_PACKET_TEMPLATE exists, but is there a filled-in example
of a real card going through the conveyor?"

Эта папка отвечает на частый вопрос внешних ревьюеров: «шаблон
CONVEYOR_RUN_PACKET есть, но есть ли заполненный пример реальной
карточки, прошедшей конвейер?»

Yes. Each RUN below is a real review round from the project's history.
A run has two parts:

- `RUN_NNN_..._PACKET.md` — the request sent to the reviewer models
  (what to check, materials, deliverable format).
- `RUN_NNN_..._RESULTS.md` — the actual verdicts returned by the
  independent reviewer models (Gemini, GPT-5.5, Kimi, Qwen, Grok),
  plus the coordinator's own direct-verification note.

## The discipline shown here / Показанная дисциплина

These runs demonstrate the project's core rules in action:

- **VERIFY_BEFORE_TRUST** — every reviewer claim is re-checked by the
  coordinator via direct grep/run before being accepted. See RUN_002,
  where an external finding (Alibaba) was verified against the actual
  code before the card was patched.
- **REVIEW ≠ VALIDATION** — an APPROVE verdict is a review signal, not
  a proof of correctness.
- **AUTHOR_DECISION_STATUS_AUTHORITY** — only the author assigns final
  status; reviewer consensus informs but does not decide.
- **MODEL_FAMILY_DIVERSITY** — reviewers are drawn from different model
  families to reduce correlated blind spots.

## Index / Указатель

| Run | Target | Type | Outcome |
|-----|--------|------|---------|
| RUN_001 | DOT card English translation | CARD_TRANSLATION_REVIEW | APPROVE |
| RUN_002 | SOLIDUS RISK_CASE_001 patch | CARD_PATCH_REVIEW | APPROVE (5/5) |
| RUN_003 | PHAGO dimension in registry | REGISTRY_DIMENSION_REVIEW | APPROVE |
| RUN_004 | _domain_prefix rewrite (bare-domain detector G1) | NARROW_CIRCLE_REVIEW | FIX_FIRST — D-DET-4 accepted; 2 voices set aside |

NOTE: These are illustrative examples selected from the project's run
history, not the complete set. They are provided so the conveyor
discipline is visible in the repository itself, not only in the
templates.
