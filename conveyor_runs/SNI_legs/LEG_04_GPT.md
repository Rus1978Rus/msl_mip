SCRIPT_NATIVE_INVISIBLES CONVEYOR LEG 04
REVIEWER: GPT-5.6 Thinking / MODEL_FAMILY: OpenAI-GPT (ЧЕТВЁРТОЕ семейство)
RECEIVED: 2026-08-06
PACKET: CONVEYOR_PACKET_SCRIPT_NATIVE_INVISIBLES_2026-08-06

VERDICT: DESIGN_SURVIVES_WITH_MAJOR_ARCHITECTURAL_PATCHES. LOOPHOLE: NO.
  CARD_LAYER_MUST_CHANGE: YES, но НЕ ветвлениями внутри карточек.

POSITIONS:
  V1 -> E = A (скрипт соседей) + B (нормативная функция) + C (protected-context gate).
     ***ГЛАВНЫЙ АРХИТЕКТУРНЫЙ ВКЛАД, КОТОРОГО НЕ БЫЛО НИ У КОГО:*** не встраивать скрипт в
     карточки вообще. Ввести ОБЩИЙ СЛОЙ между знаком и карточкой:
       SIGN OCCURRENCE -> FUNCTIONAL_USE_RESOLVER -> FUNCTION_STATUS -> CARD RELATION -> RISK
     Карточка объявляет ДОПУСТИМЫЕ РОЛИ знака (ZWJ: EMOJI_SEQUENCE_JOINER, VIRAMA_CONJUNCT_JOINER,
     JOINING_CONTEXT_JOINER); резолвер вычисляет роль ЭТОГО вхождения из запиненных данных.
     Карточка не обязана знать список письменностей. Слой становится function-aware, а не
     просто script-aware.
     ЧЕТЫРЁХСОСТОЯНИЕ: PROVEN_FUNCTIONAL / PLAUSIBLE_FUNCTIONAL / NONFUNCTIONAL / UNVERIFIABLE.
     ZWSP: одного «оба соседа Khmer» НЕДОСТАТОЧНО (атакующий тоже может окружить кхмерским) ⇒
       максимум PLAUSIBLE, никогда не PROVEN. Line_Break=SA применять к СОСЕДЯМ, а не объявлять
       свойством самого ZWSP. Новый артефакт ZWSP_NATIVE_SCRIPT_PROFILE поверх LineBreak.txt,
       причём сам SA не должен автоматически амнистировать письменность — он ИСТОЧНИК КАНДИДАТОВ.
     ZWJ: для деванагари/малаялам нужен СТРУКТУРНЫЙ предикат вирамы, скрипта мало.
     BOM: ***НИКАКОГО script-исключения*** — его роль транспортная, от письменности не зависит.
     Стоимость ввода: POLICY BASIS / PROVENANCE, но НЕ RUNTIME ORACLE (ядро не видит клавиатуру,
     IME, копирование, историю правки). Совпадает с переформулировкой Qwen, но добавляет явный
     список того, чего ядро не видит.
  V2 -> (ii)+(iv). PROVEN -> pass без внимания; PLAUSIBLE -> pass + ОДИН СВЁРНУТЫЙ witness
     (не 40 записей на 40 границ слов); NONFUNCTIONAL -> карточка без изменений; UNVERIFIABLE ->
     ***неизвестность НЕЛЬЗЯ автоматически превращать в амнистию.*** Четвёртое состояние —
     единственная леги, которая явно закрыла этот путь.
  V3 -> эмодзи-исключение: KEEP, BUT NORMALIZE INTO THE RESOLVER. «Ошибка не в существовании
     эмодзи-исключения. Ошибка в том, что правило применено только к одному хорошо заметному
     классу легитимного использования.» Каждый новый PROVEN-предикат обязан нести:
     rule_id, source artifacts, negative tests, known shelter, residual label, author decision.
  V4 -> ***ЗАПРЕТ НА ПОНИЖЕНИЕ ИТОГА:*** нельзя `if native: final_level = NONE` — это сотрёт
     D-INV-GEN, ZW-BITS, Input-Guard и любую будущую ось. Чинить В ИСТОЧНИКЕ: не порождать
     BOUNDARY_DISRUPTOR, если вхождение выполняет штатную функцию. Composition = max, плюс
     CONTRIBUTOR LEDGER (кто именно дал итоговый queue).
     ФАЗЫ: phase 0 SHADOW (резолвер считает, вердикт не меняется, нулевая семантическая дельта,
     измеряем сколько ячеек сдвинется) -> phase 1 точные функции (эмодзи+вирама) -> phase 2
     профиль ZWSP по письменностям.
  V5 -> AUTHORIZED_SCRIPT_NATIVE_CARD_DELTA_MANIFEST_v0_1 с полями на КАЖДУЮ ячейку. Обязательны
     MIXED-DOCUMENT кейсы (кхмерский абзац + латинский идентификатор; тайская проза + URL;
     персидская проза + config key; смена письменности РОВНО НА невидимом знаке) — смягчение
     применяется ЛОКАЛЬНО К ВХОЖДЕНИЮ, а не ко всему документу. 12 мутаций MUT-SN-01..12,
     каждая ломает отдельный тест. Отдельно: если итоговый queue пришёл от Input-Guard, тест
     НЕ засчитывается как успех ZW-BITS.
  V6 -> пять остатков: NATIVE_SCRIPT_COVER · ORTHOGRAPHIC_CORRECTNESS_UNVERIFIED («PLAUSIBLE
     FUNCTION ≠ CORRECT SPELLING») · SINGLE_CARRIER_NATIVE_SCRIPT_RESIDUAL · MIXED_SCRIPT_
     BOUNDARY_UNVERIFIABLE · INPUT_METHOD_PROVENANCE_UNOBSERVED.
     Запрещённая формулировка: «NATIVE SCRIPTS: SAFE».
  V-OTHER -> чинить в источнике, не гасить сверху. Не C6 целиком: структурные внешние признаки
     (скрипт, joining, вирама, эмодзи, host) УЖЕ есть в ядре, метаданные языка документа —
     будущее внешнее свидетельство, для этой заплаты НЕ требуются.
     ***СПРАВЕДЛИВОСТЬ ВОЗДЕЙСТВИЯ:*** «FORMALLY IDENTICAL RULE ≠ EQUAL IMPACT». Предлагает
     SCRIPT_IMPACT_REGISTER. Исправление — не «ослабление ради языка», а устранение измеренного
     ложного relation: нормальная граница слова была классифицирована как разрушение границы.

=== ЗАМЕР КООРДИНАТОРА #1: РЕЗОЛВЕР, КОТОРЫЙ GPT ПРОСИТ ПОСТРОИТЬ, УЖЕ ПОСТРОЕН ===
GPT ставит Tier-1 пунктами 1 и 2 «Shared FUNCTIONAL_USE_RESOLVER» и «four-state function status».
Проверил живое ядро: `core/zw_bits.py::function_status` возвращает РОВНО ЧЕТЫРЕ состояния с теми
же именами — PROVEN_FUNCTIONAL / PLAUSIBLE_FUNCTIONAL / NONFUNCTIONAL / UNVERIFIABLE — и покрывает
все шесть носителей, включая ZWSP, ZWJ и BOM.
⇒ Tier-1 п.1-2 — это НЕ СТРОЙКА, А ПОДКЛЮЧЕНИЕ. Цена радикально ниже заявленной.

=== ЗАМЕР КООРДИНАТОРА #2 (РЕШАЮЩИЙ): РЕЗОЛВЕР АСИММЕТРИЧЕН, И СЛЕПАЯ ЗОНА — РОВНО ЦЕЛЬ КРУГА ===
Прогнал живой резолвер на векторах круга:
  кхмерский  KH<ZWSP>KH   (ЦЕЛЬ)          -> PLAUSIBLE_FUNCTIONAL
  тайский    TH<ZWSP>TH   (ЦЕЛЬ)          -> PLAUSIBLE_FUNCTIONAL
  лаосский   LO<ZWSP>LO   (ЦЕЛЬ)          -> PLAUSIBLE_FUNCTIONAL
  мьянма     MY<ZWSP>MY   (ЦЕЛЬ)          -> PLAUSIBLE_FUNCTIONAL
  **латиница ab<ZWSP>cd   (АТАКА!)        -> PLAUSIBLE_FUNCTIONAL**
  **граница  KH<ZWSP>lat  (остаток V6-4)  -> PLAUSIBLE_FUNCTIONAL**
  деванагари вирама<ZWJ>  (легит)         -> PROVEN_FUNCTIONAL
  деванагари БЕЗ вирамы<ZWJ>              -> NONFUNCTIONAL
  персидский <ZWNJ>                       -> PROVEN_FUNCTIONAL
⇒ Ветка СОЕДИНИТЕЛЕЙ (ZWJ/ZWNJ) РАЗЛИЧАЮЩАЯ: вирама есть — PROVEN, вирамы нет — NONFUNCTIONAL,
  персидский joining — PROVEN. Tier-2 п.13 GPT («активировать точные вирама/joining предикаты»)
  УЖЕ ВЫПОЛНЕН.
⇒ Ветка ZWSP ПЛОСКАЯ: PLAUSIBLE для ВСЕГО, включая ЛАТИНИЦУ и границу двух письменностей.
  Причина честная: у ZWSP нет позиционного оракула (как у WJ/SHY), для оси битов это корректно.
  НО КАК КАРТОЧНЫЙ ГЕЙТ ОН СЕГОДНЯ НЕПРИГОДЕН: подключить карточку к нему «как есть» = дать
  амнистию латинскому ZWSP, то есть собственноручно реализовать мутацию **MUT-SN-05**.
⇒ ВЫВОД ДЛЯ СВОДА: цена круга РАСПАДАЕТСЯ НА ДВЕ НЕРАВНЫЕ ЧАСТИ.
    ZWJ/ZWNJ — почти бесплатно (подключение существующего различающего предиката).
    ZWSP     — требует ИМЕННО ТОГО, что GPT назвал: нового профиля письменностей.
  Ни одна из первых трёх лег этого разделения не увидела: все говорили «ZWSP/ZWJ» одним пакетом.

=== ЗАМЕР КООРДИНАТОРА #3: ПОДТВЕРЖДЕНЫ ДВА ЧАСТНЫХ УТВЕРЖДЕНИЯ GPT ===
(а) MIXED_SCRIPT_BOUNDARY (V6-4) — субстрат есть:
      KH<ZWSP>KH  -> слева Khmer, справа Khmer  — совпадают
      KH<ZWSP>lat -> слева Khmer, справа Latin  — НЕ совпадают
      lat<ZWSP>KH -> слева Latin, справа Khmer  — НЕ совпадают
      KH<ZWSP>TH  -> слева Khmer, справа Thai   — НЕ совпадают (две РОДНЫЕ, но разные)
    ⇒ формулировка «ОБА соседа в ОДНОЙ письменности» различает эти случаи, а «хотя бы один сосед»
      дала бы амнистию на границе. Выбор слов здесь несёт нагрузку.
(б) Скрипта мало для ZWJ — подтверждено прямым замером: деванагари С вирамой и БЕЗ вирамы имеют
    ОДИНАКОВЫЕ скрипты соседей (Devanagari/Devanagari), различает их только ccc=9 у вирамы.

=== ЗАМЕР КООРДИНАТОРА #4: ЦЕНА НОВОГО ПИНА И PHASE-0 ПЕРЕПИСЬ ===
LineBreak.txt в data/unicode/ ОТСУТСТВУЕТ ⇒ профиль ZWSP = НОВЫЙ пинённый источник (11-й).
  Grok предлагал обойтись КОНСТАНТОЙ (Khmer/Thai/Lao/Myanmar) — расхождение с GPT вынести автору
  как отдельный выбор: константа (дёшево, ручной список) против пина (дорого, воспроизводимо).
PHASE-0 перепись (GPT V4, «измерить сколько ячеек сдвинется» ДО изменения вердиктов) — выполнена:
  gate_bare_domain_detector.py    носители=ZWSP           родные=Devanagari
  gate_combining_mark_demotion.py носители=ZWSP,ZWJ,BOM   родные=Devanagari
  gate_zw_bits.py                 носители=ZWSP,ZWNJ,ZWJ  родные=Devanagari
  reconcile_byspec_probe.py       носители=ZWJ,BOM        родные=Arabic
  zwj_bom_manifests.py            носители=ZWSP,ZWJ,BOM   родные=Arabic
⇒ ПЯТЬ файлов-кандидатов, не один. Утверждение Qwen «0 изменений для старых ячеек» опровергнуто
  вторично и с бОльшим числом: помимо найденной ранее ячейки Z3 затронуты ещё четыре файла.
  Это верхняя граница кандидатов; точный поячеечный список — предмет delta-манифеста.
