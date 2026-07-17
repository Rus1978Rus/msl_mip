ЧАСТНЫЙ АВТОРСКИЙ ПРОЕКТ / COMMERCIAL USE PROHIBITED

[SUPERSEDED 2026-07-17 — предикат-22 устарел. Граница класса расширена автором до
 Cf∧Default_Ignorable = 138 (AUTHOR_DECISION_20260716_D-NEIGHBORS-BORDER-138).
 АКТУАЛЬНЫЙ эталон: conveyor_runs/ORACLE_ZWSP_NEIGHBORS_v0_2_2026-07-17.md
 (+ машинный oracle_class_138_2026-07-17.json, генератор tests/gen_class138_oracle.py).
 Этот файл (canon 22 / strict 40) сохранён как ИСТОРИЯ; для сверки НЕ использовать.
 Условия ¬BN/¬tag/¬deprecated, дававшие 22, были необъявленным авторским сужением.]

DOCUMENT_ID: ORACLE_ZWSP_NEIGHBORS_2026-07-15
DOCUMENT_TYPE: ORACLE_MANIFEST [SUPERSEDED_BY ORACLE_ZWSP_NEIGHBORS_v0_2_2026-07-17]
DATE: 2026-07-15
PROJECT: MSL/MIP — Malyavsky Syntax Language / Malyavsky Invariant Protocol
BASIS: foundation_layer/AUTHOR_DECISION_20260715_D-NEIGHBORS-CRITERION.md
MACHINE_READABLE: conveyor_runs/oracle_zwsp_neighbors_2026-07-15.json

НАЗНАЧЕНИЕ: зафиксировать ОЖИДАЕМЫЙ список соседей ZWSP ДО прогона ног симуляции
  критерия D-NEIGHBORS-CRITERION. Защита от «обе ноги ошиблись одинаково»: ноги
  сверяются с ЭТИМ эталоном, а не друг с другом. Эталон выведен из предиката
  решения и подтверждён BY_CODE (22 text-bucket / 40 strict).

РАМКА ПРОЕКТА: система ОПОВЕЩЕНИЯ, не антивирус. Эталон — материал для сверки,
  не приговор; расхождение разбирается человеком, не усредняется.

============================================================
ПРЕДИКАТ (дословно из D-NEIGHBORS-CRITERION §1)
============================================================
СОСЕД ⟺ General_Category = Cf
      ∧ Bidi_Class = BN
      ∧ Default_Ignorable_Code_Point = True
      ∧ ¬tag         (не U+E0001, не U+E0020..E007F)
      ∧ ¬deprecated  (не U+206A..206F)

TARGET = ZWSP U+200B (исключается из своих соседей).

============================================================
ОЖИДАЕМЫЙ КАНОН (text-bucket) = 22 кодпоинта
============================================================
Имена — из unicodedata (UCD), не по памяти. Столбец CARD: знак присутствует в
карточке ZWSP как NAMED_SPECIMEN (5 из 22).

  #  CODEPOINT  UNICODE_NAME                          gc  bidi  CARD
  -- ---------- ------------------------------------- --- ----- ----
  01 U+00AD     SOFT HYPHEN (SHY)                     Cf  BN    CARD
  02 U+180E     MONGOLIAN VOWEL SEPARATOR             Cf  BN     +
  03 U+200C     ZERO WIDTH NON-JOINER (ZWNJ)          Cf  BN    CARD
  04 U+200D     ZERO WIDTH JOINER (ZWJ)              Cf  BN    CARD
  05 U+2060     WORD JOINER (WJ)                      Cf  BN    CARD
  06 U+2061     FUNCTION APPLICATION                 Cf  BN     +
  07 U+2062     INVISIBLE TIMES                      Cf  BN     +
  08 U+2063     INVISIBLE SEPARATOR                  Cf  BN     +
  09 U+2064     INVISIBLE PLUS                       Cf  BN     +
  10 U+FEFF     ZERO WIDTH NO-BREAK SPACE (BOM)       Cf  BN    CARD
  11 U+1BCA0    SHORTHAND FORMAT LETTER OVERLAP       Cf  BN     +
  12 U+1BCA1    SHORTHAND FORMAT CONTINUING OVERLAP   Cf  BN     +
  13 U+1BCA2    SHORTHAND FORMAT DOWN STEP            Cf  BN     +
  14 U+1BCA3    SHORTHAND FORMAT UP STEP              Cf  BN     +
  15 U+1D173    MUSICAL SYMBOL BEGIN BEAM             Cf  BN     +
  16 U+1D174    MUSICAL SYMBOL END BEAM               Cf  BN     +
  17 U+1D175    MUSICAL SYMBOL BEGIN TIE              Cf  BN     +
  18 U+1D176    MUSICAL SYMBOL END TIE                Cf  BN     +
  19 U+1D177    MUSICAL SYMBOL BEGIN SLUR             Cf  BN     +
  20 U+1D178    MUSICAL SYMBOL END SLUR               Cf  BN     +
  21 U+1D179    MUSICAL SYMBOL BEGIN PHRASE           Cf  BN     +
  22 U+1D17A    MUSICAL SYMBOL END PHRASE             Cf  BN     +

(U+00AD и U+FEFF имеют канонические имена UCD SOFT HYPHEN / ZERO WIDTH NO-BREAK
 SPACE; SHY / BOM — общеупотребимые алиасы, приведены в скобках.)

============================================================
STRICT-BUCKET = 40 (REFERENCE-ONLY, НЕ КАНОН)
============================================================
Справочный ВЕРХНИЙ ПРЕДЕЛ: text-bucket + directional-форматы (LRM/RLM/встраивания/
изоляты) + deprecated (U+206A..206F). НЕ канон соседства — приведён только как
граница сверху. Reconcile идёт по КАНОНУ = 22.

============================================================
РАЗМЕТКА КАРТОЧКИ
============================================================
Из 22:
  - 5 NAMED_SPECIMENS в карточке ZWSP: U+00AD, U+200C, U+200D, U+2060, U+FEFF
    (in_card=true) — репрезентативная выборка;
  - 17 «сверх карточки» (in_card=false) — в карточке отсутствуют BY DESIGN,
    покрыты КЛАССОМ через предикат, а не поимённо.
NAMED_SPECIMENS ⊂ канон (0 лишних в карточке). Карточка НЕ обязана перечислять все
22 — «кто сосед» решает предикат (D-NEIGHBORS-CRITERION §2).

============================================================
RECONCILE-КОНТРАКТ (двуногая симуляция критерия)
============================================================
BY_SPEC-нога и BY_CODE-нога сверяются с ЭТИМ манифестом, НЕ друг с другом.
Ключ сверки — КОРТЕЖ на каждый кодпоинт:
  ( codepoint , gc , bidi , DI , bucket , in_card )
Правила:
  - расхождение ЛЮБОЙ ноги с манифестом = ДЕФЕКТ (ноги ИЛИ манифеста) — разбирается,
    НЕ усредняется, НЕ «голосованием ног»;
  - если ошиблись ОБЕ ноги одинаково, но манифест верен — расхождение всё равно
    вскрывается (в этом смысл раннего эталона);
  - если верны обе ноги, а манифест неверен — правится манифест с записью провенанса;
  - count-инвариант: canon=22, strict_reference=40; сдвиг любого числа = дефект.
Машинный reconcile берёт эталон из oracle_zwsp_neighbors_2026-07-15.json.

============================================================
ПРОВЕНАНС ЭТАЛОНА
============================================================
BY_CODE, сгенерирован программно из unicodedata по DI_RANGES (UCD
DerivedCoreProperties), НЕ набран руками.
  - UCD 16.0.0 (Claude Code, Python 3.14): canon 22 / strict 40;
  - UCD 15.0.0 (separate env, Python 3.12): идентично (22/40, те же кодпоинты) —
    прогон ДРУГОГО исполнителя, NOT_RE_RUN_HERE (см. D-NEIGHBORS-CRITERION §1
    CROSS_VERSION_UCD_15_0_0).
Устойчивость к версии UCD подтверждена двумя независимыми окружениями.

END_OF_ORACLE_MANIFEST
