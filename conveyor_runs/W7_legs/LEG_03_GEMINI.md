W7 CONVEYOR LEG 03
REVIEWER: Gemini / MODEL_FAMILY: Google-Gemini
RECEIVED: 2026-08-03
PACKET: CONVEYOR_PACKET_W7_CONFUSABLE_2026-07-26

VERDICT: дизайн ВЕРЕН, не LOOPHOLE. all (а)-(ж) PASS on every axis.

POSITIONS:
  V1 MECHANISM  -> C: единая КЛАССОВАЯ карточка CONFUSABLE_CLASS_CARD (двухъярусно), агрегирует
                   запиненный UTS#39 skeleton dict + считает mixed-script метрику захваченного
                   токена. B (81 карточка) CUT (раздувает g). A (голый) CUT (нарушает ARCH).
  V2 FP-GRANITSA-> комбо-гейт host-контекст AND ">=2 скрипта в ОДНОМ label":
                   sber.рф pass (каждый label моно-скрипт); alpha-testing pass в прозе (а если
                   ЗАРЕГАН как домен -> структурно аномален, алерт заслужен); проза pass (host-гейт).
  V3 TARGET-LIST-> НЕ требуется для mixed-script: смешение скриптов в ОДНОМ label = строгая
                   структурная аномалия (запрещено ICANN/IDNA2008) -> свидетель вправе подсветить
                   без знания бренда. Список нужен ТОЛЬКО для whole-script spoof (вне first-cut).
  V4 LEVEL/SCOPE-> ВОЗМОЖНАЯ(queue), host/домен-only first-cut. HOLD без списка -> редкие болезненные
                   FP на экзотических легит-IDN. ***DIVERGENCE vs Grok*** fullwidth-точки (．。):
                   ОСТАВИТЬ в ведении parser-desync / NFKC reconstruction ИЛИ DOT-карточки -- НЕ
                   мешать буквенные гомоглифы с разделителями. (Grok LEG_01: наоборот, тянуть их в
                   этот фронт через NFKC/skeleton.)
  V5 BATTERIES  -> классовая карточка + host-гейт математически изолирована от невидимок -> zero-
                   delta ZWSP/ZWJ/BOM гарантирован; новая confusable_battery (spoof/pure-IDN/
                   science/prose); pin UCD/UTS#39 обязателен.
  V6 OSTATOK    -> 4 спорных (ѡ→w, η→n, ա→a, ս→u) отложить; whole-script spoof (аpple.com целиком
                   кириллицей) отложить до системы словарей (target-list) -- без неё атаку от
                   легит-домена не отличить. Честная фиксация остатка.

FIRST-CUT SKELETON (Gemini):
  1) единая CONFUSABLE_CLASS_CARD; 2) статический запиненный dict безопасных маппингов (минус 4
  спорных); 3) триггер: context==HOST AND токен содержит символ из словаря AND в одном label
  (между точками) >=2 различных скрипта; 4) effective_action=QUEUE_FOR_REVIEW; 5) в отчёте честно:
  whole-script и fullwidth-dots в этот инкремент НЕ входят.

CONVERGENCE with LEG_01 Grok (2 семейства согласны):
  V1=C классовая ось; V2 host + ">=2 скрипта в label"; V3 списка НЕ надо для mixed-script;
  V4 queue not hold; V6 4 спорных отложить + whole-script = отдельный фронт (нужен target-list).
DIVERGENCE (fork для автора): fullwidth-точки -- Grok тянет В фронт (NFKC), Gemini ОСТАВЛЯЕТ в
  DOT-карточке/reconstruction. -> отдельная развилка F1.
COORD-FLAGS (проверить замером на живом ядре):
  * оба опираются на "context==HOST" и "label между точками" -- сверить, что _detect_context_at /
    reconstruction реально дают надёжный HOST + label-границы для mixed-script БЕЗ разделителя-масы
    (pаypal в URL без точки-аномалии).
  * "single-script whole-label -> pass" оба подтверждают -> whole-script Cyrillic бренд = ИЗМЕРИТЬ
    и вынести как named остаток (оба вынесли в отдельный фронт).
