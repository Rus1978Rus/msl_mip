TAG CONVEYOR LEG 02
REVIEWER: GPT-5.6 Thinking / MODEL_FAMILY: OpenAI GPT
RECEIVED: 2026-08-04
PACKET: CONVEYOR_PACKET_W_TAG_2026-08-04
NOTE: внешняя сверка Unicode 17.0 core-spec ch.23, UTS#51, emoji-sequences 17.0.

VERDICT: APPROVE_WITH_MAJOR_SPEC_PATCHES. дизайн верен, НОВАЯ ОСЬ НУЖНА, LOOPHOLE НЕТ.

POSITIONS:
  V1 MECHANISM  -> ***A + C*** (не B+C как Grok): ЛЮБОЙ назначенный tag-знак ВНЕ валидной emoji tag
                   sequence = событие; максимальные tag-run декодируются в ОТДЕЛЬНЫЙ payload-объект.
                   ***B (порог >=N) CUT как ДЕТЕКТОР***: тривиально обходится -- один знак / разбивка
                   видимыми / несколько односимвольных runs / растяжка по полям. N может влиять на
                   отчёт/приоритет, но НЕ на факт обнаружения. D (плотность) CUT (обход измерен).
                   Декод ТОЛЬКО U+E0020..U+E007E (cp-0xE0000); U+E0001 = маркер, U+E007F = терминатор,
                   unassigned = НЕ декодировать как ASCII.
  V2 LEGIT      -> ***ЧЕТЫРЁХСОСТОЯННЫЙ КЛАССИФИКАТОР ВАЛИДНОСТИ, НЕ "3 RGI-флага"***.
                   ФАКТИЧЕСКАЯ ПОПРАВКА (внешняя сверка): RGI_Emoji_Tag_Sequence в Emoji 17.0 = РОВНО
                   ТРИ (gbeng/gbsct/gbwls), НО UTS#51 допускает ВАЛИДНЫЕ НЕ-RGI последовательности
                   (в спеке показаны California, Ontario, Zurich, Normandy) => правило "молчать только
                   на трёх RGI" БУДИТ стандартно-валидные флаги. [бьёт по LEG_01 Grok "pinned RGI list"]
                   Классы: RGI_VALID -> pass | VALID_NON_RGI (CLDR subdivision ID или 3-значный region
                   subtag, вся последовательность <=32 cp) -> pass + audit | WELL_FORMED_BUT_INVALID
                   (gbxyz) -> queue | ILL_FORMED (run без базы / флаг без CANCEL / чужая база) -> queue
                   | NON_EMOJI_TAG_RUN -> covert. Валидный флаг + хвост ПОСЛЕ CANCEL: префикс CLEAN,
                   хвост QUEUE (легит-префикс НЕ освобождает остаток строки).
                   Артефакт: генерировать компактный VALID_EMOJI_TAG_PROFILE из запиненных
                   emoji-sequences.txt + CLDR validity, НЕ вести список регионов вручную.
                   Fail-visible: VALIDITY_DATA_MISSING/VERSION_MISMATCH -> TAG_VALIDITY_UNVERIFIABLE,
                   НЕ тихое освобождение.
  V3 REVEAL     -> (b) ЭКРАНИРОВАННЫЙ ОГРАНИЧЕННЫЙ СТРУКТУРНЫЙ preview (== Grok, но с жёстким
                   контрактом). Поля: payload_length, escaped_preview, preview_limit(~128), truncated,
                   full_payload_digest, original_start/end, run_count, decoder_version.
                   ЗАПРЕТ (критический): decoded payload НЕ ДОЛЖЕН автоматически: снова входить в
                   analyze(); попадать в LLM-промпт; исполняться; интерпретироваться как разметка;
                   становиться командой. Слой представления обязан применять СВОЁ экранирование
                   (HTML/JSON/Markdown/LLM-как-цитата-недоверенных-данных).
  V4 LEVEL      -> generic non-legit tag -> MEDIUM/QUEUE. ***HOST: остаётся QUEUE, НЕ hold*** (против
                   Grok): HIGH/HOLD только при ДОПОЛНИТЕЛЬНОЙ улике (protected-target collision,
                   parser desync, allowlist bypass по dual-view, trusted machine-field profile,
                   явная авторская политика). ***ОДИНОЧНЫЙ tag-знак -> QUEUE, НЕ pass*** (против Grok
                   и против текущего поведения §1): один невидимый знак уже создаёт скрытую ASCII-букву.
                   ***ЯВНО ОТКЛОНЕНА эвристика "осмысленный ASCII"*** (ignore/send keys/drop tables):
                   ось станет языково-зависимым семантическим фильтром и выйдет за structure-only рамку.
                   U+E0001 -> witness + MEDIUM/QUEUE, decoded_ascii=NONE, event DEPRECATED_LANGUAGE_TAG.
                   Unassigned (U+E0000, E0002..E001F) -> НЕ декодировать, event UNASSIGNED_TAG_BLOCK_
                   CODEPOINT, first-cut = witness/UNVERIFIABLE, БЕЗ претензии "скрытая ASCII-нагрузка".
  V5 BATTERIES  -> frozen baseline: для входов без tag-блока semantic/effective/attention delta = ZERO;
                   повторить ZWSP 21/21, ZWJ/BOM, W4/W5/W7, Input-Guard границы. 14 позитивных ячеек
                   (вкл. прикрытие 120/300/600 -> ВСЁ ЕЩЁ детект; несколько раздельных односимвольных
                   runs; хвост после CANCEL; gbxyz; run без флага; флаг без CANCEL; чужая база;
                   U+E0001; заглавные tag-буквы; несколько payload-runs). Легит-контроли: 3 RGI +
                   валидные не-RGI + чёрный флаг без нагрузки. ***OUTPUT-SAFETY тесты***: payload
                   содержит <script>alert(1)</script>, " } ] `, {{template}}, # heading -> проверка,
                   что не рендерится как активная разметка, не меняет схему отчёта, не становится
                   инструкцией. Граничные: run=1, preview_limit-1/limit/+1, очень длинный под Input-Guard.
                   MUTATION MANIFEST MUT-TAG-01..12 (готовая adversarial-батарея).
  V6 OSTATOK    -> НЕ закрывает 11 каналов (VS-encoding, ZWSP/ZWNJ битовые, combining-mark, bidi,
                   гомоглифы, whitespace-стего, HTML/CSS, метаданные файлов, вложения/бинарь,
                   сжатое/шифрованное внутри ASCII, СБОРКА сообщения из РАЗНЕСЁННЫХ runs).
                   Статус формулировать TAG_CHANNEL_COVERED, НЕ HIDDEN_CONTENT_COVERED.
                   Остающийся обход: payload по многим runs -- детект ДА (каждый run даёт witness),
                   полная реконструкция сообщения = PENDING (tier 2).
  V-OTHER-1     -> АРХИТЕКТУРА: class_guard остаётся источником presence кодпоинтов; TAG-ось ПОТРЕБЛЯЕТ
                   occurrences, группирует последовательности, валидирует emoji-использование,
                   декодирует, выдаёт ОДИН структурный witness. НЕ второй полный сканер текста:
                   "ONE SCAN -> MULTIPLE CONSUMERS". Исключение: 31 unassigned вне класса-138 --
                   объединённый range-check в ТОМ ЖЕ линейном проходе.
  V-OTHER-2     -> детерминированный парсер: сохранять оригинал+offsets; на BLACK FLAG пытаться
                   САМУЮ ДЛИННУЮ валидную последовательность; классифицировать; вне принятой валидной --
                   группировать максимальные runs; декодировать только E0020..E007E; CANCEL = граница,
                   не payload; хвост = отдельное событие; НИКОГДА не вкладывать tag sequences.
                   O(n), память ограничена preview+метаданными, без regex-backtracking.
  V-OTHER-3     -> fail-visible + провенанс в каждом результате (classification, span, raw cps,
                   decoded_length, escaped_preview, digest, emoji_validity_status, rgi_status,
                   UTS51_version, CLDR_version, decoder_version, rule_id).

CONVERGENCE с LEG_01 (Grok): плотность CUT как детектор; декод обязателен; раскрытие = экранированный
  усечённый preview (не raw, не пусто); generic level = queue; TAG != "сокрытие закрыто"; VS/ZW/bidi =
  отдельные оси; ось = достройка/потребитель class-138, не дубль сканера.
ГЕНУИННЫЕ РАЗВИЛКИ (для автора):
  F1 ПОРОГ N: Grok N>=3 как детектор  vs  GPT: ЛЮБОЙ назначенный tag вне валидной последовательности
     (N CUT как тривиально обходимый: односимвольные runs). GPT технически сильнее -- обход измерим.
  F2 ОДИНОЧНЫЙ TAG: Grok pass+presence (сохранить §1)  vs  GPT queue (уже скрытая ASCII-буква).
  F3 HOST-HOLD: Grok hold при "осмысленном ASCII"  vs  GPT queue, hold ТОЛЬКО при доп. улике;
     GPT ЯВНО отвергает семантическую эвристику как выход за structure-only рамку.
  F4 ЛЕГИТ-АРТЕФАКТ: Grok "pinned RGI region list" (3 флага)  vs  GPT "полный validity-классификатор
     (RGI + valid-non-RGI через CLDR subdivision)" -- ФАКТИЧЕСКАЯ поправка: список-из-3 будит валидные
     не-RGI флаги.
COORD-FLAGS (проверить ЗАМЕРОМ на своде):
  * ВЕРСИОННЫЙ КОНФЛИКТ: GPT сверялся с Unicode 17.0 / Emoji 17.0, а наш проект ЗАПИНЕН на
    unidata 16.0.0 (core/unicode_tables.py assert + 3 таблицы). Любой emoji/CLDR-артефакт обязан
    пиниться под 16.0.0, иначе fail-visible сработает на своём же профиле. ИЗМЕРИТЬ.
  * F2/F1 -- измерить цену: сколько ложных queue даст "любой одиночный tag" на легит-корпусе
    (сейчас §1: одиночка -> pass). Это ПОВЫШЕНИЕ шума против текущего поведения.
  * VALID_NON_RGI -- проверить, доступен ли CLDR subdivision-список без нового тяжёлого артефакта
    (r>g): возможно, достаточно СТРУКТУРНОЙ формы (база + 2-6 tag-букв/цифр + CANCEL, <=32 cp).
  * output-safety: проверить, что print_report и report-схема не ломаются на payload с разметкой
    (образец: W7 _reveal экранирует через <U+XXXX NAME>).
