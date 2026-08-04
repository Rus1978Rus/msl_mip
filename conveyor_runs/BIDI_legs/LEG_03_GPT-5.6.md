BIDI CONVEYOR LEG 03
REVIEWER: GPT-5.6 Thinking / MODEL_FAMILY: OpenAI GPT
RECEIVED: 2026-08-04
PACKET: CONVEYOR_PACKET_BIDI_2026-08-04
NOTE: внешняя сверка UAX#9 (revision 50 для Unicode 16.0.0), UTS#55, Trojan Source (arXiv 2111.00169).

VERDICT: APPROVE_WITH_MAJOR_ARCHITECTURAL_PATCHES. НОВАЯ ОСЬ, потребляющая occurrence-индекс
  class-guard; D-INV-GEN БЕЗ ИЗМЕНЕНИЙ. LOOPHOLE НЕТ.
Формулы: BIDI CONTROL PRESENT != BIDI ATTACK · BALANCED != SAFE · LOGICAL != REFERENCE DISPLAY ·
  REFERENCE DISPLAY != GUARANTEED CONSUMER RENDERING.

POSITIONS:
  V1 MECHANISM  -> E, ПЯТИСТАДИЙНО: 1) классификация семейства контроля 2) разбор областей и баланса
                   3) ЭТАЛОННЫЙ визуальный порядок 4) поиск сдвинутых участков и пересечённых границ
                   5) контекстная политика.
                   ***«БАЛАНС — УЛИКА, А НЕ РЕШЕНИЕ О БЕЗОПАСНОСТИ»***: сбалансированный RLO..PDF
                   ВСЁ РАВНО переставляет расширение/разделители/код. [бьёт по Gemini, у которой
                   стек-баланс несущий, и закрывает САМО-ПРИЗНАННУЮ дыру Grok]
                   Предикат first-cut (любое из): RLO/LRO в display-sensitive токене · эталонная
                   перестановка пересекает точку/слэш/кавычку/скобку/разделитель комментария/границу
                   токена · невалидная структура инициатор/терминатор в display-sensitive контексте ·
                   override в ASCII-доминантном токене без RTL-обоснования рядом · расхождение границ
                   лексических атомов в профиле SOURCE_CODE.
  V2 LEGIT      -> семейная политика + совместимость скрипта/контекста + баланс + тест пересечения
                   границ. ОТКЛОНЕНО ТРОЙНО: «любой bidi -> queue» · «сбалансировано -> автоматически
                   чисто» · «есть RTL-буква рядом -> автоматически чисто».
                   Метки LRM/RLM/ALM в общем тексте -> PASS + ***СВЁРНУТЫЙ (collapsed) witness***
                   (BIDI_MARK_SUMMARY: total_count, types, first/last positions, collapsed=true) —
                   ЕДИНСТВЕННЫЙ ответ на ИЗМЕРЕННЫЙ линейный рост витнесса §1 (x20 -> 20 записей);
                   ни Grok, ни Gemini этого не адресовали.
                   ***ТАБЛИЦА BIDI_CLASS НУЖНА (против Grok и Gemini, обе сказали «не нужна»):***
                   12 контролей достаточно, чтобы их ОПОЗНАТЬ, но НЕ чтобы выполнить UAX#9 над
                   ОКРУЖАЮЩИМ текстом. Нужен связный bundle: UAX9_REVISION 50 + DerivedBidiClass +
                   BidiBrackets + BidiMirroring + BidiTest + BidiCharacterTest (все 16.0.0).
                   Fail-visible: данных нет / версия не та / conformance-тест упал ->
                   BIDI_PROJECTION_UNVERIFIABLE; НЕ «считать, что перестановки нет» и НЕ «queue весь RTL».
  V3 REVEAL     -> ***БЕЗОПАСНОЕ ДВОЙНОЕ ПРЕДСТАВЛЕНИЕ (против категорического запрета Gemini):***
                   logical_escaped + REFERENCE_VISUAL_ORDER + карта сдвинутых участков + карта областей
                   контролей. Отклонено: сырая bidi-строка в отчёте · «только факт bidi без разницы» ·
                   утверждение точного рендера потребителя.
                   Обоснование: текущий witness говорит «U+202E на позиции N», но НЕ отвечает
                   «что именно переставилось». Для §1-файла человеку нужно:
                   LOGICAL invoice<RLO>gpj.exe / REFERENCE_DISPLAY invoiceexe.jpg / MOVED_REGION 8..14 /
                   BOUNDARY_EFFECT extension-like suffix visually changed.
                   Ключ безопасности: core хранит НЕ готовую активную строку, а ДАННЫЕ (logical_codepoints,
                   control_records, reference_visual_indices, moved_spans, crossed_boundaries,
                   paragraph_direction_profile, uax9_version); контролы рендерятся ТОЛЬКО как инертные
                   ASCII-метки; для смешанного текста обязателен список ИНДЕКСОВ, который терминал
                   переставить не может. Поле renderer_claim = REFERENCE_UAX9_PROJECTION обязательно.
  V4 LEVEL      -> метки/сбалансированные изоляты в прозе -> PASS + свёрнутый witness;
                   override в display-sensitive токене -> MEDIUM/QUEUE; несбалансированный override ->
                   QUEUE при наличии контекстной/граничной улики; host -> ОСТАЁТСЯ существующим QUEUE
                   (ось добавляет witness, НЕ создаёт второй вердикт и НЕ поднимает в HOLD);
                   filename-like перестановка расширения -> QUEUE; расхождение лексических атомов
                   (source code) -> QUEUE; HIGH/HOLD зарезервирован под отдельную потребительскую улику
                   (профиль FILENAME + отображаемый суффикс != логического + политика потребителя).
  V5 BATTERIES  -> AUTHORIZED_BIDI_DELTA_MANIFEST_v0_1, по ячейке: CASE_ID / старый семантический
                   уровень / новый / старое effective / новое / EXPECTED_BIDI_FINDING /
                   ***EXPECTED_CAUSAL_AXIS*** / allowed_changed_fields / author_decision_id.
                   12 позитивных (B1..B12, вкл. сбалансированный RLO..PDF spoof, LRO-аналог, вложенные
                   override/isolate, перестановка через точку/слэш/кавычку, host-случай, контроль в
                   комментарии и в строке кода) + 10 легит-контролей (L1..L10, вкл. измеренные
                   RLM x1/x5/x10/x20 -> PASS и zero-delta на тексте без контролей).
                   ***CAUSALITY-ГЕЙТ (ОБЯЗАТЕЛЕН) — механизация ловушки §1:*** каждый тест хранит
                   CAUSE_LEDGER (вклад каждой оси). Для Trojan-Source-строки: С RLO — находка SOLIDUS
                   может быть, но находка BIDI ОБЯЗАНА существовать НЕЗАВИСИМО; БЕЗ RLO — SOLIDUS
                   остаётся, находка BIDI ОБЯЗАНА ИСЧЕЗНУТЬ. Нельзя засчитывать финальный вердикт как
                   bidi-TP без bidi_rule_id + bidi_occurrence + bidi_reference_divergence.
                   Перед проектной батареей — официальные BidiTest.txt и BidiCharacterTest.txt на
                   запиненном 16.0.0. MUTATION MANIFEST MUT-BIDI-01..14 (в т.ч. MUT-BIDI-08
                   «засчитать SOLIDUS-queue как успех bidi» и MUT-BIDI-14 «алерт на каждый RLM»).
                   Zero-delta по ZWSP/ZWJ/BOM/TAG/VS/W5/W7.
  V6 OSTATOK    -> не закрывается (10 пунктов): естественное bidi-переупорядочивание без контролей ·
                   шрифто/shaping-зависимость · CSS/HTML directionality вне кодпоинтов · paragraph
                   direction потребителя · баги рендереров и нестандартные tailorings · source-code
                   спуф без подключённой грамматики языка · перестановка между разными UI-полями ·
                   копирование после удаления контролей потребителем · скриншот-атаки · гомоглифы/
                   скрытые каналы/пробелы = другие оси.
                   Допустимая формулировка: EXPLICIT_BIDI_CONTROL_REORDERING: COVERED WITH REFERENCE
                   PROJECTION. Запрещённая: BIDI SPOOFING FULLY CLOSED.
  V-OTHER-1     -> НОВАЯ ОСЬ, потребляющая occurrence-индекс class-guard. Разделение: class-guard =
                   «контроль существует, позиции, класс»; D-INV-GEN = «член класса ломает host»;
                   bidi-ось = «области, эталонная перестановка, сдвинутые участки, пересечённые
                   границы, безопасный двойной witness». ONE OCCURRENCE INDEX -> D-INV-GEN -> BIDI AXIS,
                   без второго полного скана.
  V-OTHER-2     -> ТРИ ПРОФИЛЯ: GENERAL_TEXT (метки и сбалансированные изоляты терпимы) ·
                   DISPLAY_SENSITIVE (host/path/filename-like/идентификатор — строже к override) ·
                   SOURCE_CODE (нужен лексический адаптер языка). Источник профиля — ДОВЕРЕННЫЙ
                   caller-context, НИКОГДА не текст атакующего.
  V-OTHER-3     -> ***ДВУХ/ТРЁХФАЗНОЕ ВНЕДРЕНИЕ — СНИМАЕТ СПОР О UAX#9:***
                   ФАЗА 1 (БЕЗ UAX#9): классификация 12 контролей, баланс/вложенность, display-sensitive
                   токены, queue на RLO/LRO в filename-like, свёрнутый witness меток, causal-ledger.
                   УЖЕ поднимает измеренный invoice<RLO>gpj.exe. Витнесс называется
                   REORDERING_CAPABLE_CONTROL, НЕ EXACT_VISIBLE_RESULT.
                   ФАЗА 2: пин UAX9 rev.50 + bidi-артефакты + официальные conformance-тесты + карты
                   индексов + безопасные адаптеры рендера. ФАЗА 3: профиль исходного кода (UTS#55).

CONVERGENCE (3 семейства): новая ось, не достройка D-INV-GEN; метки = белый список, pass; override —
  опасный класс; host не поднимать выше существующего queue; hold не вводить; сырую bidi-строку в
  отчёт НЕ вставлять; delta-манифест обязателен; ловушка §1 принята всеми; остаток = естественный RTL
  + рендерер-зависимость; запрет «bidi закрыт».
РАЗВИЛКИ (уточнены этой легой):
  F1 УСЛОВИЕ НА OVERRIDE: Gemini «любой override -> queue» | Grok «override + (unbalanced OR
     decision-span)» | GPT «override в display-sensitive токене ИЛИ пересечение границы ИЛИ
     ASCII-доминантный токен без RTL-обоснования» — GPT ближе к Grok, но с явным тестом границы.
  F2 БАЛАНС: Gemini — несущий предикат (стек) | GPT — «улика, не решение» (сбалансированный RLO..PDF
     переставляет). ЗАМЕР решает: invoice<RLO>gpj<PDF>.exe.
  F3 ПОКАЗ РАЗНИЦЫ: Gemini запрет НАВСЕГДА | Grok запрет в first-cut, опция v2 | GPT БЕЗОПАСНОЕ
     двойное представление СРАЗУ (данные+индексы, инертные метки).
  F4 ТАБЛИЦА BIDI_CLASS: Grok и Gemini «не нужна, хватит 12 кодпоинтов» (2) | GPT «нужен bundle из
     5-6 артефактов + UAX9 rev.50» (1). ФАКТИЧЕСКИЙ вопрос -> ЗАМЕР.
  F5 ФАЗНОСТЬ: только GPT предложил разделить (фаза 1 без UAX#9 уже закрывает §1-кейс) — снимает
     спор «UAX#9 да/нет», переводя его в «сейчас/потом».

COORD-FLAGS (проверить ЗАМЕРОМ на своде):
  * F4 РЕШАЮЩИЙ ЗАМЕР: в stdlib ЕСТЬ unicodedata.bidirectional() (в отличие от Script, которого не
    было в VS-круге). Проверить, покрывает ли она «RTL-буква рядом» и классы контролей БЕЗ внешних
    таблиц — тогда шестой артефакт нужен только для ПОЛНОГО UAX#9 (фаза 2), а фаза 1 бесплатна.
  * F2 ПРОВЕРИТЬ: invoice<RLO>gpj<PDF>.exe (сбалансированный спуф) — ловится ли предикатом Gemini
    (стек пуст => чисто?) и предикатом Grok (unbalanced=нет, спасает только decision-span).
  * Свёрнутый witness меток — ИЗМЕРИТЬ на §1-наборе (RLM x20): сколько записей станет вместо 20.
  * Размер артефактов фазы 2 (BidiTest.txt/BidiCharacterTest.txt) — они КРУПНЫЕ; посчитать цену r>g.
  * Causality-ledger — проверить, есть ли в отчёте поля, позволяющие атрибутировать вклад оси
    (сейчас вклад осей в effective_action не разделён).
