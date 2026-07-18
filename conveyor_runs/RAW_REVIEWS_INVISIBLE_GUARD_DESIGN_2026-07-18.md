ЧАСТНЫЙ АВТОРСКИЙ ПРОЕКТ / COMMERCIAL USE PROHIBITED

DOCUMENT_ID: RAW_REVIEWS_INVISIBLE_GUARD_DESIGN_2026-07-18
DOCUMENT_TYPE: RAW_REVIEW_BUNDLE (сверяемый источник — НЕ свод)
DATE: 2026-07-18
PACKET: CONVEYOR_PACKET_INVISIBLE_GUARD_DESIGN_2026-07-18

СЧЁТ: прислано 7 блоков. ПОЛНЫХ дизайн-вердиктов = 5 (Claude self-leg, GPT, Gemini,
  DeepSeek, Qwen). ЧАСТИЧНЫЙ = 1 (Kimi — только D1 + эмпирика P1-P7). ИСКЛЮЧЕНЫ:
  блок 5 = PACKET_ECHO (нет оценок по (a-e), нет вердикта); блок 6 = META_ASSESSMENT
  (предсказывает ревьюеров, кластеры, нет своего вердикта); прозаическая часть Kimi =
  ДРУГОЙ пакет (PROSE_READER_RUN, уже SUPERSEDED) + self-declared LEAKED → к гарду
  не относится. Семейств названо 6 (Anthropic, OpenAI, Gemini, DeepSeek, Qwen, Moonshot).

============================================================
ПО ИЗМЕРЕНИЯМ (позиции каждого — по raw)
============================================================
D1 (контракт / артефакты):
  Claude: HYBRID_C верен, «канонический поток» = дыра → view + оригинал + богатые
    метаданные {codepoint, class_bucket, context_at_pos}.
  GPT: single canonical stream CUT → ORIGINAL_VIEW + DERIVED_VIEWS[] + TRACE_LEDGER;
    матчер запрашивает view; default = ORIGINAL; богатый TRACE_EVENT (offset-карта
    one_to_zero/one/many).
  Gemini: дыра = потеря локального контекста → добавить original_context_window
    (срез слева/справа); оригинал + канонизированный (два состояния).
  DeepSeek: дыра = потеря позиции → canonical_map (canon↔orig), removed_chars
    (idx,cp,reason), card_mask.
  Qwen: (в) CONCERN desync → смещения строго относительно ИСХОДНОЙ; аддитивный
    invisible_map (оригинал нетронут + карта).
  Kimi (partial): ДВЕ дыры → два артефакта (original бит-в-бит + canonical_view;
    «поток» = ВИД, не замена) + дыра-2 context-free (ниже).
  => 6/6 (все, кто высказался): «единый поток = дыра → оригинал сохранён + производный
     вид/метаданные». ЕДИНОГЛАСНО.

D2 (канонизация):
  Claude: D2c+D2b (strip в машинных контекстах). [minority]
  GPT: D2c+D2a; D2b CUT как общее правило (только versioned policy_view); D2d только в policy.
  Gemini: D2c (два потока); D2a-одиночный/D2b отверг.
  DeepSeek: D2d гейт по Join_Control (никогда не strip ZWJ/ZWNJ; остальные — strip в машинных).
  Qwen: D2a (никогда не strip по умолчанию, только annotate) + опциональный stripped-view;
    явно CUT D2b И D2d («слишком сложно для класс-гарда»).
  Kimi: D2 не давал; но context-free ⇒ контекст-гейт-strip в гарде невозможен; P4/P5
    доказали, что слепой strip разрушает смысл.
  => 5/5: НИКОГДА не strip вслепую, гард аддитивен, оригинал сохранён. Strip (если есть)
     = опциональный производный вид / policy-слой. D2b (strip-в-ядре-гарда): 1/5 (Claude),
     отвергнут ≥3. D2d (Join_Control-гейт): DeepSeek за, Qwen против, GPT только-в-policy.

D3 (трёхуровневый сигнал):
  Claude: отдельный слой НАД гардом; гард несёт только пол «member-present=POSSIBLE».
  GPT: risk mapping SEPARATE; гард несёт CLASS_PRESENCE (NONE/PRESENT/PRESENT_WITH_
    STRUCTURAL_EFFECT), НЕ CLEAN/POSSIBLE/REAL.
  Gemini: risk-мэппинг отдельным фасадным слоем.
  DeepSeek: отдельный слой; гард даёт только информацию.
  Qwen: отдельно; гард = структура, риск = отдельный слой.
  => 5/5 ЕДИНОГЛАСНО: риск-вердикт НЕ встраивать в гард, отдельным слоем. (гард может
     нести ФАКТИЧЕСКИЙ presence-сигнал, но не risk-вердикт.)

D4 (ре-валидация ZWSP — критично):
  Claude: D4a + D4b (прозрачность для карточных + гейт).
  GPT: D4b + D4c (гейт + аддитивный); D4a только временный shadow, перманентный D4a =
    уязвимость (дифф-пайплайн); GATE-1..8; guard-мутации MUT-G1..G7.
  Gemini: D4c + D4b (аддитивный + acceptance-гейт); D4a отвергнут.
  DeepSeek: D4b + D4a (гейт + прозрачность для карточных).
  Qwen: D4c + D4b (аддитивный + жёсткий CI-гейт); D4a CUT.
  Kimi: D4 не давал; P7 (биективная карта) поддерживает реализуемость.
  => ACCEPTANCE-ГЕЙТ (D4b): 5/5 ЕДИНОГЛАСНО. «Карточный вход не изменён → 21/21
     переприйдут»: суть сходится 5/5 (через аддитивность D4c у 3, через D4a у 2).
     D4a КАК ПЕРМАНЕНТНЫЙ МЕХАНИЗМ (bypass): 2/5 за (Claude, DeepSeek), 3/5 против
     (GPT, Gemini, Qwen — предпочитают D4c аддитивный, bypass = поверхность атаки).

D5 (порядок):
  Claude: detect-before-transform; strip-чтобы-увидеть, не решать; fail-visible.
  GPT: DETECT_BEFORE_TRANSFORM; захват оригинала до любого преобразования; fail-visible.
  Gemini: Flag→Extract-context→Normalize→Strip; детект до стирания.
  DeepSeek: classify→annotate→(strip в stripped-поток)→оба потока; оригинал всегда.
  Qwen: Annotate→Normalize→опциональный Strip; strip-первым теряет позицию.
  Kimi: P6 → детект СТРОГО до нормализации (позиции корёжатся под NFKC).
  => 6/6 ЕДИНОГЛАСНО: детект/annotate ДО любой нормализации/strip. Kimi + эмпирика P6.

D6 (гард vs регистратор):
  Claude/GPT/Gemini/DeepSeek/Qwen: гард ПОГЛОЩАЕТ регистратор (единый сканер; registrar →
    адаптер/дефолт-поведение гарда). GPT + фазовый план shadow→consume→remove.
  => 5/5 ЕДИНОГЛАСНО: поглощает.

D7 (охват/этапность):
  Claude: поэтапно (гард на 3 карточных + witness-пол 135; ре-валидация ZWSP первой).
  GPT: class-wide observation с дня 1 + phased POLICY activation (Phase 0-5).
  Gemini: сразу все 138 (универсальный слой с первого коммита).
  DeepSeek: поэтапно (3 карточных прозрачно + 135 witness; strip позже).
  Qwen: сразу 138 НО консервативный дефолт (annotate-only).
  => РАСКОЛ 3/2: phased-policy (Claude, GPT, DeepSeek) vs all-138-сразу (Gemini, Qwen).
     ПРИМИРЯЕТСЯ: охват/witness на 138 сразу + тяжёлая policy/strip консервативно/поэтапно.

KIMI ДЫРА-2 (context-free):
  Kimi: «выполняется первым» vs контекст = ЦИКЛ → гард КОНТЕКСТ-СВОБОДЕН (detect/
    annotate/derive), контекст входит ВЫШЕ.
  Поддержка-в-духе: GPT (context-engine отдельно), Qwen (гард без семантического
    контекста), Gemini (гард структурный). ПРОТИВОРЕЧИТ: DeepSeek (strip в машинных
    контекстах = context-aware) + Claude D2b. => сильный НОВЫЙ принцип, разводит D2:
    контекст-гейт-strip в гарде НЕЛЬЗЯ; property-based (Join_Control) — можно.

HYBRID_C ФУНДАМЕНТАЛЬНО НЕВЕРЕН (LOOPHOLE)? — 0/6. Все: «верен + патч контракта
  (канонический поток → виды)». LOOPHOLE по архитектуре НЕТ.

D-OTHER (добавленные измерения, никто не отверг):
  GPT: sequence-semantics (ZWJ в эмодзи/tag, BOM-позиция, bidi-спаны; поля
    SEQUENCE_TYPE/VALIDITY); resource-exhaustion (O(n), event-limit, TRACE_TRUNCATED).
  Qwen: metadata schema_version (иначе матчеры молча сломаются при смене формата).
  Block-6 meta: связность D1-D7 → когерентные кластеры (structural insight).

============================================================
ЗАМЕТКА (гигиена, НЕ в свод гарда): протечка reader-прогона прозы
============================================================
Kimi во ВТОРОЙ части блока 7 ответил на ДРУГОЙ пакет — CONVEYOR_PACKET_PROSE_READER_
RUN_2026-07-17 (уже SUPERSEDED: проза = EXPLANATORY_ONLY, reader-прогон не долг,
a0e046b). Kimi САМ пометил LEAKAGE_STATUS: STIMULUS_COMPROMISED (получил пакет целиком
с §5/§6 → не слепой; голос не в счёт REQUIRED_REVIEWERS) и дал координатору hygiene-
находку: «вырезать §5/§6, раздавать только §1». Это ПОДТВЕРЖДАЕТ ранее найденную
протечку reader-батча (тот же дефект раздачи). Независимый машинный счёт Kimi = 138
(UCD 15.0+16.0) совпал с верифицированным предикатом — но моот (пакет закрыт). К
дизайну гарда ОТНОШЕНИЯ НЕ ИМЕЕТ.

============================================================
ВЕРИФИКАЦИЯ (self-leg run-grounded + Kimi эмпирика)
============================================================
- Claude self-leg на реальном коде: `_demask()` (стрип carded-масок «never hardcoded»)
  + F-NEW-1 (шрам D5-бага: второй невидимый пережил demask → молча пропущенный хост;
  урок «strip чтобы УВИДЕТЬ, не решать» уже в коде). Registrar витнесит бескарточные.
- Kimi P1-P7 (прогон UCD 16.0.0): P1 все 138 переживают NFC/NFD/NFKC/NFKD (0/138);
  P4 эмодзи-семья при слепом strip распадается (DEFAULT_IGNORABLE≠SAFE_TO_DELETE на
  данных); P5 арабское+ведущий-BOM гибнут; P6 детект строго до нормализации; P7
  биективная карта orig↔canon тотально конструируема (снимает desync-CONCERN Qwen).

END_OF_RAW_BUNDLE
