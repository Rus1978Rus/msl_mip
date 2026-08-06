ЧАСТНЫЙ АВТОРСКИЙ ПРОЕКТ / COMMERCIAL USE PROHIBITED

# PIN_MANIFEST — запиненные Unicode-таблицы (W7 confusable-ось)

Основание: AUTHOR_DECISION_20260804_D-W7-CONFUSABLE (D5) + SPEC_20260804_W7_BLOCKERS_B1-B8 (S3).
Загрузчик: core/unicode_tables.py (sha256 + unidata_version проверяются при инициализации;
несовпадение -> ось выключена fail-visible). Oracle-гейт: tests/gate_w7_tables_pin.py.

| Файл | Стандарт/версия | sha256 | Источник | Снято |
|---|---|---|---|---|
| confusables.txt | UTS#39 16.0.0 (data 2024-08-14) | 95bd0aad6dced5ebc63436f459c06ab21a8d107cd842fb57f5c3a1e91bca8611 | https://www.unicode.org/Public/security/16.0.0/confusables.txt | 2026-08-04 |
| Scripts.txt | UCD 16.0.0 | 9e88f0a677df47311106340be8ede2ecdacd9c1c931831218d2be6d5508e0039 | https://www.unicode.org/Public/16.0.0/ucd/Scripts.txt | 2026-08-04 |
| ScriptExtensions.txt | UCD 16.0.0 | 049117ce26b9769fe2749b06eef51a50a89faef4a97764dd2d81daa715980700 | https://www.unicode.org/Public/16.0.0/ucd/ScriptExtensions.txt | 2026-08-04 |
| rgi_tag_flags.txt | RGI_Emoji_Tag_Sequence (Emoji 5.0…17.0, неизменен) | f4ff732c21a14f630b32acf9441d5176fb573c22f68d3b12b96fe77671ea89cb | производный от emoji-sequences (3 записи, closed-world) | 2026-08-04 |
| StandardizedVariants.txt | UCD 16.0.0 (1306 пар) | 36e799b2c5d902af094b4dd2cb60622bffc079824bfd0bf62e3a636d698b3fb5 | https://www.unicode.org/Public/16.0.0/ucd/StandardizedVariants.txt | 2026-08-04 |
| emoji-variation-sequences.txt | UCD 16.0.0 (742 пары / 371 база) | 71d93ec015011371a027ba2bc0a63155d381c6e0b94a586c1a88a49400cd6864 | https://www.unicode.org/Public/16.0.0/ucd/emoji/emoji-variation-sequences.txt | 2026-08-04 |
| IVD_Sequences.txt | **IVD release 2022-09-13** (29437 пар / 15290 баз) — НЕ версия UCD | e6168c2ed8e0834d3eccb8a6d43aad004c97c8216e237101f1c2e8347be2b523 | https://www.unicode.org/ivd/data/2022-09-13/IVD_Sequences.txt | 2026-08-04 |
| BidiBrackets.txt | UCD 16.0.0 (правило N0) | b8f32554c6f658821fb0ee742d21c5b1f2086b9bf13071fed04894b022f93d67 | https://www.unicode.org/Public/16.0.0/ucd/BidiBrackets.txt | 2026-08-05 |
| DerivedJoiningType.txt | UCD 16.0.0 (Joining_Type для zero-width оси) | 6bd08b97da66b70ccfdab105a352de2984e02625239ec5695422c99b33d854f0 | https://www.unicode.org/Public/16.0.0/ucd/extracted/DerivedJoiningType.txt | 2026-08-05 |
| conformance/BidiTest.txt | UCD 16.0.0 (770241 кейс) — ТЕСТ-артефакт | 93e5eb9d88ca89dcf895f5576486a3363762ad2aa8f2db2fa56fe60cb82b9520 | https://www.unicode.org/Public/16.0.0/ucd/BidiTest.txt | 2026-08-05 |
| conformance/BidiCharacterTest.txt | UCD 16.0.0 (91707 кейсов) — ТЕСТ-артефакт | d04a51a90052dcd71c4e91ee5b3a9d973ee35c12406b5a99875ac8163c8f2804 | https://www.unicode.org/Public/16.0.0/ucd/BidiCharacterTest.txt | 2026-08-05 |
| LineBreak.txt | UCD 16.0.0 (Line_Break=SA: 757 кодпоинтов, 9 письменностей) | e97e4259d0d20fab150b9c7b4b28abfae5cd78ca97e7f4ac6ed20d685d5f4a7c | https://www.unicode.org/Public/16.0.0/ucd/LineBreak.txt | 2026-08-06 |
| DerivedCoreProperties.txt | UCD 16.0.0 (InCB: Linker=6, Consonant=240) | 39d35161f2954497f69e08bdb9e701493f476a3d30222de20028feda36c1dabd | https://www.unicode.org/Public/16.0.0/ucd/DerivedCoreProperties.txt | 2026-08-06 |

Требуемая среда: `unicodedata.unidata_version == '16.0.0'` (assert в загрузчике).

D6 (активная политика): 4 отложенных source-кодпоинта ИСКЛЮЧЕНЫ из active-карты, данные сохранены
в full-карте: U+0461 (ѡ->w), U+03B7 (η->n+U+0329), U+0561 (ա->w), U+057D (ս->u).
Примечание: официальные прототипы U+0561/U+03B7 отличаются от вахтёровских черновиков — отложение
ключуется по source-кодпоинту, расхождение значения не влияет.

TAG-ось (D-TAG-COVERT-TEXT D2 + спека B2): `rgi_tag_flags.txt` = closed-world whitelist РОВНО из 3
RGI-последовательностей (gbeng/gbsct/gbwls). Обоснование замером (SIM-5): шаблон без списка = канал
25.9–31.0 бит/флаг, широкий CLDR-список (~5000) = 12.29, closed-world-3 = 1.58 бит/флаг. Не-RGI легит
(флаг Техаса `ustx`, будущие RGI) → сигнал by design = именованный остаток R5. Конфликта с пином
unidata 16.0.0 НЕТ: тройка неизменна с Emoji 5.0 (2017), новые флаги не процессятся с 2022.
Несовпадение пина → TAG_VALIDITY_UNVERIFIABLE, легит НЕ освобождается (флаги перестают молчать).

VS-ось (D-VS-STEGO D4 + спека B2): три реестра вариационных последовательностей образуют композит
валидных пар (загрузчик core/variation_registry.py, сборка машинная, один парсер).
**IVD ПИНИТСЯ ДАТОЙ РЕЛИЗА, а НЕ версией UCD** — замер: релизы unicode.org/ivd датированы и
независимы (2014-05-16 … 2022-09-13, 2025-07-14, 2026-07-31, 2026-08-03), «IVD под UCD 16.0.0»
НЕ СУЩЕСТВУЕТ. Взят слепок 2022-09-13 как ровесник нашего пина UCD 16.0.0; регистрации после этой
даты читаются как НЕзарегистрированные до авторского ре-пина (остаток RESIDUAL_POST_PIN).
9 deprecated-пар (PRI 546) ОСТАЮТСЯ в вайтлисте — документы в дикой природе их содержат.
Несовпадение sha256 любого из трёх файлов → PAIR_STATUS=UNVERIFIABLE: исключения продолжают
применяться (иначе возвращается эмодзи-флуд), но факт непроверяемости ВИДИМО выводится в отчёт —
молчаливый pass запрещён.

ZW-BITS ось (D-ZW-BITS D5 + спека B3): `DerivedJoiningType.txt` взят СРАЗУ в фазу 1 — отклонение от
рекомендации круга, обоснованное авторским вопросом «а если на персидском с неправильной орфографией?»:
без этой таблицы нефункциональные позиции ВНУТРИ арабского письма невидимы, и ответ «поймаем» был бы
неправдой. Лежит ПОД СУЩЕСТВУЮЩИМ пином 16.0.0 (40 КБ), не новый версионный трек.
**Загрузчик ОБЯЗАН применять @missing-дефолт файла** (`@missing: 0000..10FFFF; Non_Joining`):
jt(ZWNJ) в файле ОТСУТСТВУЕТ, и загрузчик без дефолтов молча провалится на самом носителе.
`emoji-zwj-sequences.txt` НЕ взят: измерено, что категорийный фолбэк {So,Sk,Sm}+прозрачные Mn гасит
**1468 из 1468 RGI (100%)** ⇒ таблица не нужна ради молчания легита, она сузила бы лишь
не-RGI-байпас (остаток R6). Это поправка к панели, считавшей 1473/1474 от неверного знаменателя.

SNI карточный слой (D-SNI-2, свод SNI_SVOD_AND_SIM 2026-08-06): `LineBreak.txt` +
`DerivedCoreProperties.txt` — две строки ПОД СУЩЕСТВУЮЩИМ пином UCD 16.0.0 (0 новых версионных
треков). Оракул функциональной позиции core/sni_oracle.py: ZWSP — оба значимых соседа с
Line_Break=SA (9 письменностей: Thai/Lao/Khmer/Myanmar/Ahom/New_Tai_Lue/Tai_Le/Tai_Tham/Tai_Viet,
757 кодпоинтов — производная МАШИННАЯ из пина, рукописная константа запрещена: список «4
письменности» уже недополнен против норматива); ZWJ — слева InCB=Linker (6 вирам: Deva/Beng/
Gujr/Orya/Telu/Mlym; включает малаяламский legacy-chillu «вирама+ZWJ в конце слова»). BOM и ZWNJ
исключений НЕ имеют. Диссент D1 круга разрешён в пользу пина: производная требует запиненного
входа. Несовпадение sha256 → SNI_UNVERIFIABLE: исключение НЕ применяется (неизвестность ≠
амнистия), статус видим в отчёте. 0 числовых порогов.

BUMP-ПОЛИТИКА (B6/S6): обновление любой таблицы = ОТДЕЛЬНОЕ AUTHOR_DECISION с diff-отчётом
(добавленные/удалённые/изменённые маппинги + изменённые skeleton), полным прогоном свода гейтов,
delta-census по авторизованному манифесту и обновлением этого файла. Рантайм НИКОГДА не тянет
таблицы из сети; «latest» запрещён.
