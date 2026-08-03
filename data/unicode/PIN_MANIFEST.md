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

Требуемая среда: `unicodedata.unidata_version == '16.0.0'` (assert в загрузчике).

D6 (активная политика): 4 отложенных source-кодпоинта ИСКЛЮЧЕНЫ из active-карты, данные сохранены
в full-карте: U+0461 (ѡ->w), U+03B7 (η->n+U+0329), U+0561 (ա->w), U+057D (ս->u).
Примечание: официальные прототипы U+0561/U+03B7 отличаются от вахтёровских черновиков — отложение
ключуется по source-кодпоинту, расхождение значения не влияет.

BUMP-ПОЛИТИКА (B6/S6): обновление любой таблицы = ОТДЕЛЬНОЕ AUTHOR_DECISION с diff-отчётом
(добавленные/удалённые/изменённые маппинги + изменённые skeleton), полным прогоном свода гейтов,
delta-census по авторизованному манифесту и обновлением этого файла. Рантайм НИКОГДА не тянет
таблицы из сети; «latest» запрещён.
