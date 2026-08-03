W7 CONVEYOR LEG 04
REVIEWER: Qwen / MODEL_FAMILY: Qwen (Alibaba)
RECEIVED: 2026-08-03
PACKET: CONVEYOR_PACKET_W7_CONFUSABLE_2026-07-26

VERDICT: APPROVE_WITH_SCOPE_NARROWING (дизайн верен, сузить область). LOOPHOLE НЕТ.

POSITIONS:
  V1 MECHANISM  -> C классовая ось (Two-Tier) + A mixed-script detect + запиненный UTS#39 skeleton;
                   81 карта CUT (квадратичный долг). Skeleton СТРОГО запинен (ручной набор нарушает
                   VERIFY_BEFORE_TRUST, дрейф).
  V2 FP-GRANITSA-> host-context-gate (субстрат URL_HOST/DOMAIN) + ">=2 скрипта в ОДНОМ DNS label
                   (сегмент между точками)". sber.рф: оба label моно-скрипт -> pass; alpha-testing:
                   субстрат prose -> pass; gоogle.com: label mixed count=2 -> queue. UTS#39
                   Restriction Levels = базис.
  V3 TARGET-LIST-> НЕ нужен для first-cut на уровне queue (сохраняет SUBSTRATE_INDEPENDENCE).
                   Список нужен ТОЛЬКО для эскалации до hold ИЛИ для whole-script spoof.
  V4 LEVEL/SCOPE-> queue_for_review; host/domain-only. ***fullwidth-точки -> В DOT-КАРТОЧКУ***
                   (U+FF0E = конфузабл U+002E, место в SIGN_CORE_CARD_DOT через NFKC; мешать в один
                   фронт нарушает ONE_ACTIVE_CARD_PER_SIGN). [=Gemini, против Grok]
  V5 BATTERIES  -> zero-delta для prose/pure-IDN/science вне host; pin UTS#39 v15.1.0 + UCD v15.1.0.
                   Обязательные ячейки: gоogle.com->queue, pаypal.com->queue, sber.рф->pass,
                   alpha-testing->pass, paypal．com->pass (через DOT-карту, НЕ этот фронт).
  V6 OSTATOK    -> 4 спорных отложить (77 неспорных в v1); whole-script spoof (all-Greek ραуραλ) =
                   отдельный фронт в бэклог (нужен skeleton-всего-домена vs target-list = принципиально
                   другой механизм, Target-List Dependent).
  V-OTHER       -> LOOPHOLE НЕТ: mixed-script в одном DNS label = объективный структурный факт (UTS#39),
                   не требует семантического списка. Корень C6/CONTEXT_V2 обходится сужением области
                   до DNS-субстрата.

CONVERGENCE (теперь 3 семейства: Grok+Gemini+Qwen):
  V1=C классовая ось; V2 host + ">=2 скрипта в label"; V3 списка НЕ надо для mixed-script queue;
  V4 queue not hold, host-only; V6 4 спорных отложить + whole-script = отдельный фронт (target-list).
F1 FORK (fullwidth-точки) COUNT: DOT-карта/reconstruction = Gemini + Qwen (2); в этот фронт via NFKC
  = Grok (1). => склоняется к "делегировать DOT-карте".
COORD-FLAGS (проверить замером -- те же, что по Gemini):
  * все три опёрлись на host-context-gate + "label между точками" -- ИЗМЕРИТЬ, что ядро реально даёт
    надёжный HOST + label-границы для mixed-script без разделителя-аномалии (pаypal в URL).
  * "pаypal．com -> pass через DOT-карту" -- Qwen УТВЕРЖДАЕТ что DOT-карта уже это ловит; §1 показал
    paypal．com -> silent pass (attn=NONE). ЗНАЧИТ DOT-карта fullwidth-точку в host СЕЙЧАС НЕ
    эскалирует. Это надо ПРОВЕРИТЬ и, возможно, вынести как под-развилку F1b (нужна доработка DOT).
