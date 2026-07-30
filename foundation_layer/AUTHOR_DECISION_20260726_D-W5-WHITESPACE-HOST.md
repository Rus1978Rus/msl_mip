# AUTHOR_DECISION: whitespace-lookalike host-break ось (W5) — дизайн ратифицирован

**Статус:** AUTHOR_DECISION (дизайн принят; КОД под acceptance-гейтом)
**Дата:** 2026-07-26
**Автор:** Руслан Малявский (AUTHOR_DECISION_STATUS_AUTHORITY) — делегировал координатору «по важности, наименее атакуемый синтез»
**Тип:** новая ось детекции (поведенческая, аддитивная), witness-рамка
**Основание:** CONVEYOR_PACKET_W5_WHITESPACE_HOST_2026-07-26; **4 РАЗНЫХ семейства** (DeepSeek-R1,
  Moonshot/Kimi [замер], OpenAI/GPT-5.6 [аудит кода], Google/Gemini); свод
  scratchpad/w5_whitespace_conveyor_legs.md. §1 подтверждён 2× (Kimi + координатор).

РАМКА: свидетель, не судья. Уровень = рекомендация. Ось только ПОДНИМАЕТ effective_action, witness
  сохраняет, source и canonical-вывод не трогает, карточный вердикт не понижает.

## §1 ФАКТ (измерено)
NBSP/NNBSP/FIGURE/EN-QUAD/IDEOGRAPHIC space = категория Zs, вне класса-138 (Cf∧DI); U+2028=Zl,
  U+2029=Zp; WORD JOINER U+2060=Cf (покрыт). `paypal<NBSP>.com` → pass (макс. witness), карточный
  ZWSP-host → hold. Легит: `Mr.<NBSP>Smith`, french `mot<NNBSP>:` → pass. **NBSP.isspace()==True** →
  текущий whitespace-токенизатор РВЁТ токен на нём. Механика УЖЕ существует: `_reconstructed_context`
  (removal-probe по ASCII-границам, исключает исследуемый non-ASCII пробел) + WHITESPACE witness-семья
  (msl_mip_runtime.py: _NON_ASCII_WS/classify/scan_uncarded), сейчас **witness-only**.

## ПРИНЯТЫЕ РЕШЕНИЯ (D1–D8)

**D1 — КЛАСС: закреплённое свойство `White_Space` МИНУС обычные ASCII-WS** (U+0009/0A/0B/0C/0D/20),
  с подсемействами SPACE_SEPARATOR(Zs)/LINE_SEPARATOR(Zl)/PARAGRAPH_SEPARATOR(Zp)/OTHER (NEL и т.п.).
  По свойству (полно, версионируемо), НЕ голый Zs и НЕ ручной список; пин `unidata_version`. Текущий
  `_NON_ASCII_WS+Zl+Zp` = compat-baseline: сгенерировать property-oracle, сравнить, авторизовать delta
  по-ячеечно, потом заменить. (GPT; Gemini Zs+Zl+Zp — подмножество.)

**D2 — МЕХАНИЗМ: обобщить СУЩЕСТВУЮЩУЮ whitespace witness-семью в аддитивный effective-шов.** НЕ
  расширять класс-138, НЕ трогать `_is_domain_label_invisible` (он намеренно `if ch.isspace(): return
  False`), НЕ звать базовый `_detect_context_at` (рвёт токен на NBSP). Использовать
  `_reconstructed_context` (ASCII-границы + removal-probe). Ось сканирует source НЕЗАВИСИМО от
  карточного статуса (иначе будущая карточка NBSP уберёт знак из uncarded → ось ослепнет). (4/4.)

**D3 — УРОВЕНЬ: host-разрыв → ВОЗМОЖНАЯ (queue), НЕ hold.** Zs И Zl/Zp в host → queue (единый
  уровень). РАЗВИЛКА Zl/Zp (Gemini: hold) РЕШЕНА в queue: host-разрыв Zl/Zp несёт ту же прозаическую
  неоднозначность CONTEXT_V2, что Zs (урок D-INV-GEN — hold на `word.tld`-прозе переалармит), а
  base-rate не измерен. Паритет с uncarded-Cf (queue), не с карточным ZWSP (hold заработан
  карточностью). Условие будущей эскалации назвать заранее (измеренная частота атак > X при FP < Y).
  (queue: DeepSeek/Kimi/GPT; hold: Gemini — 1, конфлатит с line-инъекцией.)

**D4 — FP-ГРАНИЦА: асимметричный host-span предикат на removal-probe.** Эскалировать ТОЛЬКО когда
  удаление whitespace реконструирует ВАЛИДНЫЙ host И позиция разрыва внутри host-span:
  prev=UNICODE-alnum ∧ next∈{alnum,'.'} ∧ (убрать whitespace → `_looks_like_domain`) ∧ в токене есть
  '.'. Наивное «между alnum» ПРОМАХИВАЕТСЯ на `paypal<NBSP>.com` (замер) — отвергнуто. Unicode-alnum,
  не ASCII (иначе IDN-дыра `пэй<NBSP>пал.рф`). Делегация Gemini «штатному FREE_TEXT» отвергнута:
  базовый движок рвёт токен на NBSP (замер). Легит (`Mr.<NBSP>Smith` authoritative, french NNBSP,
  after-dot `pay.<NBSP>pal.com`) → clean (замер).

**D5 — MULTI-WHITESPACE + DEGRADED-TLD.** (а) Одиночное удаление обходится `pay<NBSP><NNBSP>pal.com`
  → удалять ВЕСЬ смежный axis-whitespace-прогон в reconstruction-span (НЕ обычные ASCII-разделители).
  (б) Degraded-TLD FP измерен: `Mr.Smith` → HOST в degraded (alphabetic-TLD fallback). Политика: в
  degraded применять overlay ТОЛЬКО при доп. host-evidence (scheme/authority / typed host / email-домен
  / protected target), иначе witness+DEGRADED без overlay. Не гарантировать одновременно 0-FP и 0-промах
  без TLD-источника — честно.

**D6 — ИНТЕРФЕЙС-СТАБИЛЬНОСТЬ с CONTEXT_V2.** Ось эмитит сигнал «Zs рвёт host-метку»; контекст-детектор
  — внутренний СМЕНЯЕМЫЙ блок, чтобы CONTEXT_V2 заменил эвристику без смены контракта сигнала и без
  повторной ре-валидации батарей. (Kimi.)

**D7 — ПРОИЗВОДИТЕЛЬНОСТЬ.** removal-probe (per-offset boundary-scan + join) = потенциальный НОВЫЙ
  O(n²) на whitespace-флуде — строить факты РАЗ на ASCII-span (source→projection + смежные WS-прогоны),
  per-offset O(1)/O(log). Обязателен scaling-гейт (не вернуть закрытый O(n²)). (GPT.)

**D8 — ОБЛАСТЬ: host-only first-cut.** Отдельными кругами: делимитер-маскарад (`rm<NBSP>-rf`, нужен
  CLI-контекст), STANDALONE line-инъекция Zl/Zp (JSON/log/код — там hold обоснован parser-differential),
  email-домен, generic token. Сырьё Vakhter WHITESPACE_CLASS_DRAFT — только через круг + ре-валидация.

## GATE — КОД только при:
zero-delta для не-whitespace (differential полного отчёта) + ZWSP 21/21 + ZWJ/BOM 11/11 + mutation +
  все гейты + новая whitespace_host_battery (property-генерируемые ячейки: класс × {mid-label,before-dot,
  after-dot,multi} × {атака,легит} + ZWSP-контроль) + degraded/authoritative split + i18n anti-flood
  (french NNBSP/NBSP-проза/числа/CJK — отдельно verdict И attention) + mixed-mechanism (NBSP+ZWSP/…) +
  scaling-гейт (near-linear removal probe). Пин unidata_version в census. Без зелёного — мержа нет.

## OPEN — отдельные круги
delimiter-masquerade (CLI); standalone Zl/Zp line-injection (parser-differential → возможен hold);
  email-домен; property-oracle vs current-set delta authorization.

## СВЯЗЬ
CONVEYOR_PACKET_W5_WHITESPACE_HOST_2026-07-26 · свод w5_whitespace_conveyor_legs.md ·
  AUTHOR_DECISION_20260722_D-INV-GEN (образец аддитивного host-шва; queue-урок) ·
  AUTHOR_DECISION_20260726_D-W4-VS-AXIS (тот же таксон-пробел для Mn) · msl_mip_runtime
  (_reconstructed_context / whitespace witness-семья) · DESIGN_NOTE_E4_CONTEXT_V2 · RULE_DESIGN_ADVERSARIAL_SIM.

END_OF_AUTHOR_DECISION
