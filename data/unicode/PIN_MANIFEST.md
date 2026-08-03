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

BUMP-ПОЛИТИКА (B6/S6): обновление любой таблицы = ОТДЕЛЬНОЕ AUTHOR_DECISION с diff-отчётом
(добавленные/удалённые/изменённые маппинги + изменённые skeleton), полным прогоном свода гейтов,
delta-census по авторизованному манифесту и обновлением этого файла. Рантайм НИКОГДА не тянет
таблицы из сети; «latest» запрещён.
