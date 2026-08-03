W7 CONVEYOR LEG 01
REVIEWER: Grok / MODEL_FAMILY: xAI-Grok
RECEIVED: 2026-08-03
PACKET: CONVEYOR_PACKET_W7_CONFUSABLE_2026-07-26

VERDICT: дизайн верен (с поправками). LOOPHOLE не подтверждён.

POSITIONS:
  V1 MECHANISM  -> C: классовая confusable-ось (two-tier), вход через карточный/осевой путь
                   (не хардкод в sequence); предикат ">=2 скрипта в ОДНОМ host-label";
                   skeleton = запиненная UTS#39, версия UCD в CI.
  V2 FP-GRANITSA-> host/label-only gate (alpha-testing вне host -> pass);
                   whole-label single-script -> легит IDN pass; >=2 скрипта в label -> сигнал.
  V3 TARGET-LIST-> first-cut БЕЗ обязательного списка (mixed-script-in-host уже аномалия -> queue);
                   target-list = ОПЦИОНАЛЬНОЕ усиление (upgrade приоритета / hold). Список на
                   старте = рост g без доказанной необходимости.
  V4 LEVEL/SCOPE-> mixed-script-in-host -> ВОЗМОЖНАЯ(queue), паритет W4/W5; hold ТОЛЬКО при
                   target-match (если список дан); host/label-only first-cut;
                   fullwidth/ideographic dots -> в этот фронт через NFKC/skeleton.
  V5 BATTERIES  -> zero-delta на не-confusable входах (ZWSP/ZWJ/BOM/SOLIDUS + mutation);
                   новые ячейки spoof->queue / IDN+science+проза->pass; pin UTS#39+UCD в CI.
  V6 OSTATOK    -> 4 спорных (ѡ→w, η→n, ա→a, ս→u) ОТЛОЖИТЬ; first-cut = КУРИРОВАННЫЙ набор
                   (кириллица/греч высокоувер. + fullwidth separators), не вся UTS#39;
                   whole-script spoof = ОТДЕЛЬНЫЙ фронт (нужен target-list/IDN-политика).
  V-OTHER       -> TARGET_LIST_OPTIONALITY: "аномалия mixed-script в host" (без списка) != "spoof
                   бренда X" (нужен список). Выдавать первое за второе = overclaim; "нельзя ничего
                   без списка" = underclaim. First-cut закрывает silent pass; список = след. слой.

RANKED: 1) классовая ось + host mixed-script + queue (без обяз. списка)  2) +optional target-list
        3) 81 карточка (g растёт)  4) голый mixed-script CUT (нарушает ARCH)  5) обяз. список CUT.

COORD-FLAGS (для свода/сима, проверить на живом ядре):
  * ARCH-констрейнт: ось ДОЛЖНА быть карточкой/осью, не хардкодом в sequence -> сверить, как
    W4/W5-seam реализованы (они additive в analyze(), не карточки) => есть ли уже прецедент
    "осевого" пути, или Grok требует нового карточного носителя.
  * host-label-only gate -- проверить, есть ли в ядре надёжный host/label-детектор для НЕ-точечных
    случаев (mixed-script без разделителя, напр. "pаypal" в прозе vs в URL).
  * "single-script whole-label -> pass" -- измерить: не пропустит ли whole-script Cyrillic-бренд
    (раypal целиком кириллицей) = Grok сам вынес это в отдельный фронт (V6), пометить как остаток.
