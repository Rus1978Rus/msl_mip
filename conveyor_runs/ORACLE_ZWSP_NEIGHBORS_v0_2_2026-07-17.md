ЧАСТНЫЙ АВТОРСКИЙ ПРОЕКТ / COMMERCIAL USE PROHIBITED

DOCUMENT_ID: ORACLE_ZWSP_NEIGHBORS_v0_2_2026-07-17
DOCUMENT_TYPE: ORACLE_MANIFEST (поднадзорный класс — полный перечень)
DATE: 2026-07-17
PROJECT: MSL/MIP — Malyavsky Syntax Language / Malyavsky Invariant Protocol
SUPERSEDES: ORACLE_ZWSP_NEIGHBORS_2026-07-15 (предикат-22 / strict-40 — SUPERSEDED)
BASIS: foundation_layer/AUTHOR_DECISION_20260716_D-NEIGHBORS-BORDER-138 (a88c234)
  + RULE_NEIGHBORS_CRITERION_v0_2_RU (§1 предикат)
MACHINE_READABLE: conveyor_runs/oracle_class_138_2026-07-17.json
GENERATOR: tests/gen_class138_oracle.py (детерминированный, из unicodedata + pinned DI)

НАЗНАЧЕНИЕ: зафиксировать ПОЛНЫЙ перечень членов ПОДНАДЗОРНОГО КЛАССА (138) —
  эталон для сверки любой ноги/oracle/гарда. Старый oracle перечислял 22 (узкий
  предикат Cf∧BN∧DI∧¬tag∧¬dep); граница расширена автором до Cf∧DI = 138, поэтому
  перечень пересобран машинно на новый предикат.

РАМКА ПРОЕКТА: система ОПОВЕЩЕНИЯ, не антивирус. Эталон — материал для сверки,
  не приговор; расхождение разбирается человеком, не усредняется. Членство в
  классе = witness-охват (кого фиксируем), НЕ разрешение на удаление.

============================================================
ПРЕДИКАТ (дословно из RULE_NEIGHBORS_CRITERION_v0_2 §1)
============================================================
ЧЛЕН КЛАССА ⟺ General_Category = Cf  ∧  Default_Ignorable_Code_Point = True.
  (Условия ¬BN, ¬tag, ¬deprecated из v0_1 УБРАНЫ — были необъявленным сужением.)
TARGET = ZWSP U+200B (сам член класса; «прочих членов» = 137).

============================================================
ПРОВЕНАНС ЭТАЛОНА (машинный, честно по каналам версий)
============================================================
Сгенерирован программно (tests/gen_class138_oracle.py), НЕ набран руками.
  - gc / bidi / name : unicodedata (bundled UCD 16.0.0);
  - Default_Ignorable: pinned tools/sources/17.0.0/DerivedCoreProperties.txt
    через msl_mip_runtime._default_ignorable_set() (тег UCD_17.0.0).
ВЕРСИОННОСТЬ (верифицировано 2026-07-17, прогон): |Cf| = 170 и Cf∧DI = 138
  ИДЕНТИЧНЫ на UCD 16.0 и 17.0 — число версионно-стабильно в этом диапазоне,
  версионный микс рантайма на перечень влияния не даёт (см. блок ВЕРИФИКАЦИЯ в
  AUTHOR_DECISION_20260716_D-NEIGHBORS-BORDER-138). Прежнее ожидание «~120 на 17.0»
  (audit-2) НЕ воспроизведено.

============================================================
ИТОГ (count-инвариант)
============================================================
ПОДНАДЗОРНЫЙ КЛАСС = 138.
  PURE (Cf∧BN∧DI, ¬tag, ¬dep) : 23   (чисто невидимые нулевой ширины, включая ZWSP)
  DIRECTIONAL (bidi ≠ BN)     : 12   (LRM/RLM/ALM/embeddings/overrides/isolates)
  TAG (E0001 + E0020..E007F)  : 97   (language tag + tag-символы)
  DEPRECATED (206A..206F)     :  6
  ------------------------------------ ИТОГО 138.
IN_CARD = 5 образцов карточки ZWSP ⊂ класс (0 лишних): U+200C, U+200D, U+2060,
  U+FEFF, U+00AD. Остальные 133 покрыты КЛАССОМ через предикат, не поимённо.
Сдвиг любого числа (138 / 23 / 12 / 97 / 6 / 5) = ДЕФЕКТ, разбирается.

============================================================
PURE — 23 (bidi = BN, ¬tag, ¬dep)
============================================================
  CODEPOINT  UNICODE_NAME                          FLAG
  ---------- ------------------------------------- ------
  U+00AD     SOFT HYPHEN                           CARD
  U+180E     MONGOLIAN VOWEL SEPARATOR
  U+200B     ZERO WIDTH SPACE                      TARGET
  U+200C     ZERO WIDTH NON-JOINER                 CARD
  U+200D     ZERO WIDTH JOINER                     CARD
  U+2060     WORD JOINER                           CARD
  U+2061     FUNCTION APPLICATION
  U+2062     INVISIBLE TIMES
  U+2063     INVISIBLE SEPARATOR
  U+2064     INVISIBLE PLUS
  U+FEFF     ZERO WIDTH NO-BREAK SPACE             CARD
  U+1BCA0    SHORTHAND FORMAT LETTER OVERLAP
  U+1BCA1    SHORTHAND FORMAT CONTINUING OVERLAP
  U+1BCA2    SHORTHAND FORMAT DOWN STEP
  U+1BCA3    SHORTHAND FORMAT UP STEP
  U+1D173    MUSICAL SYMBOL BEGIN BEAM
  U+1D174    MUSICAL SYMBOL END BEAM
  U+1D175    MUSICAL SYMBOL BEGIN TIE
  U+1D176    MUSICAL SYMBOL END TIE
  U+1D177    MUSICAL SYMBOL BEGIN SLUR
  U+1D178    MUSICAL SYMBOL END SLUR
  U+1D179    MUSICAL SYMBOL BEGIN PHRASE
  U+1D17A    MUSICAL SYMBOL END PHRASE

============================================================
DIRECTIONAL — 12 (bidi ≠ BN — активная угроза, Trojan Source)
============================================================
  CODEPOINT  UNICODE_NAME                          bidi
  ---------- ------------------------------------- ----
  U+061C     ARABIC LETTER MARK                    AL
  U+200E     LEFT-TO-RIGHT MARK                    L
  U+200F     RIGHT-TO-LEFT MARK                    R
  U+202A     LEFT-TO-RIGHT EMBEDDING               LRE
  U+202B     RIGHT-TO-LEFT EMBEDDING               RLE
  U+202C     POP DIRECTIONAL FORMATTING            PDF
  U+202D     LEFT-TO-RIGHT OVERRIDE                LRO
  U+202E     RIGHT-TO-LEFT OVERRIDE                RLO
  U+2066     LEFT-TO-RIGHT ISOLATE                 LRI
  U+2067     RIGHT-TO-LEFT ISOLATE                 RLI
  U+2068     FIRST STRONG ISOLATE                  FSI
  U+2069     POP DIRECTIONAL ISOLATE               PDI

============================================================
TAG — 97 (E0001 + E0020..E007F, все bidi=BN — спящая угроза, LLM-инъекции)
============================================================
Диапазон механический и непрерывный; полный поимённый перечень 97 строк — в
машинном oracle_class_138_2026-07-17.json. Сводка:
  U+E0001              LANGUAGE TAG                               (1)
  U+E0020 .. U+E007F   TAG SPACE .. CANCEL TAG (tag-символы)      (96)
  ------------------------------------------------------------------
  ИТОГО TAG                                                        97
Крайние: U+E0020 TAG SPACE (первый), U+E007F CANCEL TAG (последний). Полнота
перечня гарантируется генератором + JSON, не ручным набором.

============================================================
DEPRECATED — 6 (206A..206F, bidi=BN)
============================================================
  CODEPOINT  UNICODE_NAME
  ---------- -------------------------------------
  U+206A     INHIBIT SYMMETRIC SWAPPING
  U+206B     ACTIVATE SYMMETRIC SWAPPING
  U+206C     INHIBIT ARABIC FORM SHAPING
  U+206D     ACTIVATE ARABIC FORM SHAPING
  U+206E     NATIONAL DIGIT SHAPES
  U+206F     NOMINAL DIGIT SHAPES

============================================================
RECONCILE-КОНТРАКТ (сверка ноги/гарда с эталоном)
============================================================
Любая нога/гард/oracle сверяется с ЭТИМ манифестом (JSON), НЕ друг с другом.
Ключ сверки — КОРТЕЖ на кодпоинт: ( codepoint , gc , bidi , di , bucket , in_card ).
Правила:
  - расхождение ЛЮБОЙ ноги с манифестом = ДЕФЕКТ (ноги ИЛИ манифеста) —
    разбирается человеком, НЕ усредняется, НЕ «голосованием ног»;
  - если ошиблись все одинаково, но манифест верен — расхождение всё равно
    вскрывается (смысл раннего/машинного эталона);
  - count-инвариант: total=138, PURE=23, DIR=12, TAG=97, DEP=6, in_card=5;
    сдвиг любого = дефект.
Пересборка: tests/gen_class138_oracle.py (asserts на 138/23-12-97-6/5 внутри).

============================================================
СВЯЗЬ
============================================================
- foundation_layer/AUTHOR_DECISION_20260716_D-NEIGHBORS-BORDER-138.md (a88c234)
  — решение о границе 138 (BASIS) + блок ВЕРИФИКАЦИЯ (138 стабильно 16.0↔17.0);
- foundation_layer/RULE_NEIGHBORS_CRITERION_v0_2_RU.md — §1 предикат (Cf∧DI);
- conveyor_runs/ORACLE_ZWSP_NEIGHBORS_2026-07-15.md — v0_1 (22/40), SUPERSEDED;
- conveyor_runs/oracle_class_138_2026-07-17.json — машинный перечень (138 кортежей);
- tests/gen_class138_oracle.py — детерминированный генератор эталона;
- cards/SIGN_CORE_CARD_ZERO_WIDTH_SPACE_U200B_GEN3_v0_3_RU.md — 5 образцов ⊂ класс.

END_OF_ORACLE_MANIFEST
