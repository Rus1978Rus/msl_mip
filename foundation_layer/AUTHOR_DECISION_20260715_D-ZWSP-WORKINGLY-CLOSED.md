ЧАСТНЫЙ АВТОРСКИЙ ПРОЕКТ / COMMERCIAL USE PROHIBITED

DOCUMENT_ID: AUTHOR_DECISION_20260715_D-ZWSP-WORKINGLY-CLOSED
DOCUMENT_TYPE: AUTHOR_DECISION
DECISION_ID: D-ZWSP-WORKINGLY-CLOSED
DATE: 2026-07-15
AUTHOR: Руслан Малявский (AUTHOR_DECISION_STATUS_AUTHORITY)
PROJECT: MSL/MIP Sign Alphabet
SCOPE: статус первой карточки класса «невидимые знаки» — ZWSP (U+200B):
  подъём до WORKINGLY_CLOSED_PENDING_CLASS_GUARD. Продолжение и закрытие
  шага 2 из PATH_TO_ARTIFACT, заведённого D-ZWSP-STATUS (2026-07-13).

РАМКА ПРОЕКТА: система ОПОВЕЩЕНИЯ, не антивирус (машина свидетель, не судья;
  показывает — человек решает). Вердикт статуса — решение автора, не машины.

============================================================
РЕШЕНИЕ
============================================================
LIFECYCLE_STATUS: WORKINGLY_CLOSED_PENDING_CLASS_GUARD.
DOCUMENT_STATUS (машинное поле): WORKING_DRAFT → WORKINGLY_CLOSED.
FINDING_STATUS: VERIFIED.

Это ровно шаг 2 PATH_TO_ARTIFACT. D-ZWSP-STATUS (Q3) держал карточку ДО
WORKINGLY_CLOSED с ЕДИНСТВЕННЫМ основанием — «внешний конвейер-ревью не пройден,
предупреждение верно». Это основание СНЯТО: ревью пройдено.

============================================================
ОСНОВАНИЕ (всё сошлось — предъявлено, не заявлено)
============================================================
- СИМУЛЯЦИЯ: батарея 21/21, ДВУНОГАЯ (BY_SPEC модели + BY_CODE движок),
  reconcile по кортежу, mutation-adequacy 5/5 killed. Подтверждена ЗАПУСКОМ
  (sim_bycode_v2, hermetic TLD) — не по памяти.
- PREFLIGHT: 35 PASS / 0 FAIL / 1 PRECEDENT (CONFUSABLES-арбитраж для класса
  невидимых) — структурная самопроверка пройдена.
- ВНЕШНЕЕ КОНВЕЙЕР-РЕВЬЮ: 8/8 ACCEPT, VERDICT PASS_WITH_PATCHES, ≥3 семейства
  моделей. Судился ДОКУМЕНТ (карточка), не детектор. Порядок канона
  (card → конвейер → симуляция → код) восстановлен: ревью больше не проскочено.
- BY_CODE-СВЕРКА (2026-07-14): карта и код СОГЛАСОВАНЫ (детектор делает то, что
  заявлено; scope = эмитируемые контексты; obещает-не-производит: [], код-впереди-
  карты: []). Наводки MS Copilot (EMAIL/HOLD, QUERY вне scope) проверены запуском —
  НЕ подтвердились.
- DOC-SYNC (D-ZWSP-STATUS следствие, коммит b8ebfa9): карточка приведена к своим
  доказательствам, 12/12 внутренней консистентности; больше не противоречит сама
  себе. Вскрытый рассинхрон зафиксирован как OPEN_NODE_CARD_SINGLE_SOURCE_OF_TRUTH.
- PHAGO: PHAGO_ENTITY_MIMICRY = NOT_APPLICABLE, VERIFIED (D-ZWSP-STATUS Q1;
  конвейер 9 ревьюеров 8:1 + author decision; CATEGORY_E активно доказан —
  N/A_ACTIVELY_VERIFIED). Каноничный критерий — RULE_PHAGO_APPLICABILITY_v0_1.md.

============================================================
ПОЧЕМУ DOCUMENT_STATUS ФЛИПАЕТСЯ (машинное поле)
============================================================
DOCUMENT_STATUS — MACHINE-GATE поле. Код (single_sign/module_engine.py) определяет
_VALID_STATUSES = {WORKINGLY_CLOSED, ARTIFACT_CONFIRMED} как «прошёл
STRUCTURAL_PREFLIGHT_PASS + CONVEYOR_REVIEW_PASS (несколько независимых ревьюеров)
+ AUTHOR_DECISION». ВСЕ ТРИ условия теперь выполнены (см. ОСНОВАНИЕ) → по
собственному определению кода машинный статус карточки = WORKINGLY_CLOSED.

Держать WORKING_DRAFT дальше НЕЛЬЗЯ: предупреждение CARD_NOT_CONVEYOR_REVIEWED
(«did not pass STRUCTURAL_PREFLIGHT_PASS/CONVEYOR_REVIEW_PASS») стало бы ЛОЖНЫМ —
claim≠reality в ОБРАТНУЮ сторону от той, что фиксировал D-ZWSP-STATUS. Тогда
warning был ВЕРНЫМ (ревью не пройден) и поле держали намеренно; теперь warning
станет ЛОЖНЫМ, и рантайм КОРРЕКТНО перестаёт предупреждать.

Строку "WORKINGLY_CLOSED_PENDING_CLASS_GUARD" код НЕ знает (её нет ни в
_VALID_STATUSES, ни в _DRAFT_STATUSES) — вписать её в DOCUMENT_STATUS = CARD_INVALID.
Поэтому квалификатор _PENDING_CLASS_GUARD живёт в LIFECYCLE_STATUS (свободный текст),
а DOCUMENT_STATUS несёт машинно-допустимое WORKINGLY_CLOSED. Разделение полей —
то же, что заложил D-ZWSP-STATUS.

КОД НЕ ТРОНУТ: меняется только поле КАРТОЧКИ. Изменение вывода рантайма
(warning гаснет) — прямое следствие честного статуса, а не правки движка.

============================================================
ГРАНИЦА РЕШЕНИЯ (что НЕ делаем)
============================================================
- НЕ ARTIFACT_CONFIRMED: остаётся PENDING, blocked классовым гардом
  (INVISIBLE_DEFAULT_IGNORABLE_GUARD, строится из >=3 разных невидимых, затем
  ре-валидация ВСЕХ карточек класса). Гард по D-ZWSP-STATUS Q2 — КЛАССОВАЯ
  зависимость (CLASS_FRONT), НЕ блокер WORKINGLY_CLOSED и НЕ дефект карточки.
- детектор НЕ трогаем (батарея 21/21 подтверждена запуском, код цел);
- структуру шаблона НЕ трогаем (OPEN_NODE_CARD_SINGLE_SOURCE_OF_TRUTH — отдельный
  заход);
- SIMULATION_GATE (формальный) — по пути к ARTIFACT_CONFIRMED, при постройке гарда.

PATH_TO_ARTIFACT после этого решения:
  1. preflight + conveyor review — ПРОЙДЕНЫ.
  2. WORKINGLY_CLOSED_PENDING_CLASS_GUARD — ДОСТИГНУТО (это решение).
  3. построить классовый гард (>=3 невидимых) + ре-валидация  ← следующий шаг.
  4. ARTIFACT_CONFIRMED.

END_OF_AUTHOR_DECISION
