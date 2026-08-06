ЧАСТНЫЙ АВТОРСКИЙ ПРОЕКТ / COMMERCIAL USE PROHIBITED

# docs/ — process artefacts, not the product

The repository root now holds only what a newcomer needs first: `README.md`,
`MANIFEST.md`, `SECURITY.md`, `LICENSE` and the entry point `msl_mip_runtime.py`.
Everything that documents HOW the work was done lives here, so the product is not
buried under the process that produced it.

## conveyor/

The working papers of the conveyor discipline, moved out of the root on
2026-08-07 (git history preserved — these are renames, not new files):

| File | What it is |
|---|---|
| `CONVEYOR_PACKET_*.txt` | review packets sent to the model panel (July, early rounds) |
| `CONVEYOR_REVIEW_ZWSP_CARD_2026-07-13.txt` | raw review of the ZWSP card |
| `HANDOFF_2026-07-15.md`, `HANDOFF_FOUNDATION_LAYER_2026-07-15.md` | session handover notes |
| `MIGRATION_PACKET_*.md` | migration packets (scheme patch, relation axis, homoglyph relation) |
| `audit_silent_paths_2026-07-12.md` | the silent-paths audit cited by the D-GUARD decisions |
| `РЕЗУЛЬТАТЫ ПРОГОНОВ.txt` | raw run results cited by D-DET-1/2 |

Older documents refer to these by FILENAME rather than by path, so those
references still read correctly — only the location changed.

## Where the rest lives

- `foundation_layer/` — author decisions and specifications. This is the layer
  that carries authority: a decision recorded there is what the code implements.
- `conveyor_runs/` — full rounds: packets, per-family legs, coordinator svods
  with their attack simulations, and field measurements.
- `cards/` — the sign cards themselves (the knowledge base, not documentation).
- `templates/` — templates and the conveyor rules for extending the system.
- `data/unicode/PIN_MANIFEST.md` — which external tables are pinned, at which
  hash, and why each one was taken.

## A note on the nested folder that used to be here

A `msl_mip_final/` directory sat INSIDE the repository root, containing four
author documents from 2026-07-08 (homoglyph-as-relation, card form v0.4). They
were not duplicates — those four decisions existed nowhere else — so they were
moved into `foundation_layer/` where they belong, and the stray folder was
removed. Checked before touching anything: deleting it as "an accidental copy"
would have destroyed unique author decisions.
