ЧАСТНЫЙ АВТОРСКИЙ ПРОЕКТ / COMMERCIAL USE PROHIBITED

DOCUMENT_ID: AUTHOR_DECISION_20260712_MASK_PATH_SAFEGUARD_D-GUARD-4
DOCUMENT_TYPE: AUTHOR_DECISION (принято)
STATUS: ACCEPTED (решение автора)
AUTHOR: Руслан Малявский (AUTHOR_DECISION_STATUS_AUTHORITY)
DATE: 2026-07-12
BASIS: второй круг конвейера. Ревьюер прав: при нарушении вердикт
       оставался pass, а метка ехала ОТДЕЛЬНЫМ полем integrity_status.
       Это ТОТ ЖЕ класс ошибки, против которого весь сторож («потребитель
       не прочитал поле»), просто на новом канале: человек в окне видел
       PASS и мог не заметить integrity_status.

════════════════════════════════════════════════════════════════
РЕШЕНИЕ D-GUARD-4 — ТРИ ПОЛЯ ВЕРДИКТА, ОБА ВИДНЫ В ОКНЕ
════════════════════════════════════════════════════════════════
МАСШТАБ (важно для этого решения). Система — РУЧНОЙ инструмент: человек
вставляет текст в окно, читает вердикт в окне. Нет downstream-
потребителей, потоков, автоблокировки. Поэтому починка направлена на
то, что ВИДИТ ЧЕЛОВЕК, а не на машинный контракт.

Отчёт analyze() разводит три поля:
  semantic_action  — что решил ОСНОВНОЙ путь. Это власть автора; сторож
                     её НЕ меняет (единственная инстанция переопределения
                     вердикта — автор).
  integrity_status — OK / VIOLATION / CONCERN.
  effective_action — при VIOLATION поднимается до безопасного минимума
                     (most_severe(semantic + required_action по каждому
                     нарушению) → HOLD/QUEUE по уровню); иначе равен
                     semantic_action.

В ОКНЕ показываются ОБА (print_report): при нарушении печатается
SEMANTIC VERDICT (main path), строка INTEGRITY со статусом и деталями,
и EFFECTIVE VERDICT (integrity-adjusted). Человек видит «система сказала
X, целостность нарушена → эффективно Y», а не одно слово PASS с тихой
меткой сбоку. При OK печатается один FINAL VERDICT (semantic ==
effective).

СТРОГИЙ РЕЖИМ (гейты, env MSL_MIP_GUARD_STRICT=1) по-прежнему РОНЯЕТ
прогон при нарушении: регрессия, обрывающая/занижающая путь маски, не
проходит в разработке.

ПОЧЕМУ НЕ АВТО-ПЕРЕЗАПИСЬ semantic. Сторож не имеет права переписывать
решение основного пути (AUTHOR_DECISION_STATUS_AUTHORITY). Он поднимает
ОТДЕЛЬНОЕ эффективное действие и делает расхождение видимым; финальное
слово о смене semantic — за автором. Эффективное действие — это то, что
безопасно предъявить человеку СЕЙЧАС, не подменяя запись о том, что
решил основной путь.

РЕАЛИЗАЦИЯ (msl_mip_runtime.py):
  - analyze(): semantic_action = most_severe(...); (violations, concerns)
    = _integrity_check(semantic_action, ...); при violations
    effective_action = most_severe([semantic] + [required_action ...]),
    integrity_status = "VIOLATION"; строгий режим → raise. Отчёт несёт
    semantic_action, effective_action, integrity_status,
    integrity_violations, integrity_concerns (поле final_action убрано —
    заменено парой semantic/effective).
  - print_report(): при статусе != OK печатает оба вердикта явно.

ПРОВЕРКА (chaos-гейт, секция [D-GUARD-4]): при сломанном пути
(non-strict) semantic остаётся pass, effective поднимается до
hold_pending_review, integrity_status = VIOLATION, деталь называет риск
+ semantic + required. gate_safeguard 15→23, герметично, 20/20.

СВЯЗЬ: D-GUARD-1 (гибрид «в бою метка, в строгом падение» — теперь с
явным effective), D-GUARD-3 (required_action, по которому поднимается
effective), audit_silent_paths_2026-07-12.md (класс «потребитель не
прочитал поле»).
