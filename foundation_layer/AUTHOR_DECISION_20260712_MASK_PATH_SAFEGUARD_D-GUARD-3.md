ЧАСТНЫЙ АВТОРСКИЙ ПРОЕКТ / COMMERCIAL USE PROHIBITED

DOCUMENT_ID: AUTHOR_DECISION_20260712_MASK_PATH_SAFEGUARD_D-GUARD-3
DOCUMENT_TYPE: AUTHOR_DECISION (принято)
STATUS: ACCEPTED (решение автора)
AUTHOR: Руслан Малявский (AUTHOR_DECISION_STATUS_AUTHORITY)
DATE: 2026-07-12
BASIS: второй круг конвейера по детектору Г1 в сборе. Адверсариальный
       ревьюер (1 из 6) нашёл реальное и воспроизвёл трассировкой; пять
       остальных проглядели. Находка: сторож (D-GUARD-1) ловил только
       «HIGH + финал == pass». Если финал стал log_only или
       queue_for_review, сторож МОЛЧАЛ, хотя HIGH занижен. Это не «закон
       сохранения риска», а «запрет буквального PASS».

════════════════════════════════════════════════════════════════
РЕШЕНИЕ D-GUARD-3 — СРАВНЕНИЕ СЕРЬЁЗНОСТИ, НЕ БУКВАЛЬНЫЙ PASS
════════════════════════════════════════════════════════════════
Сторож сравнивает СЕРЬЁЗНОСТЬ финала с минимумом, требуемым риском
relation-вердикта, а не проверяет равенство «== pass»:

  MEDIUM relation  → минимум queue_for_review
  HIGH relation    → минимум hold_pending_review
  CRITICAL relation→ минимум hold_pending_review
  NONE / LOW       → минимума нет (не проверяется)

Если severity(semantic_action) < severity(минимум для риска) → это
INTEGRITY_VIOLATION (а не только при финале pass). Каждое нарушение
несёт required_action, чтобы D-GUARD-4 мог поднять эффективный вердикт.
Так ловится HIGH→pass, HIGH→log_only, HIGH→queue — весь класс
занижения, а не единственная точка.

УСТОЙЧИВОСТЬ К ФОРМЕ risk_level. Значение нормализуется
str(...).strip().upper(), поэтому "high" / " HIGH " / "High" / enum
сравниваются одинаково. НЕИЗВЕСТНОЕ значение risk_level → CONCERN
(D-GUARD-3-UNKNOWN), НЕ молчаливый пропуск: «не знаю уровень» обязано
быть видимым, а не проглоченным (та же дисциплина, что ACK_GAP_TRIVALENT
UNVERIFIABLE ≠ пропуск).

ПОЧЕМУ ЭТО ВЕРНО ПРИ ИНТАКТНОМ ПУТИ. В целом прогоне MEDIUM relation
даёт действие queue → semantic ≥ queue → нет ложного нарушения; HIGH
даёт hold → semantic ≥ hold → нет нарушения. Сторож срабатывает только
когда путь агрегации ЗАНИЗИЛ риск маски. Проверено chaos-гейтом.

РЕАЛИЗАЦИЯ (msl_mip_runtime.py):
  - _REL_MIN_ACTION = {MEDIUM: queue, HIGH/CRITICAL: hold}.
  - _integrity_check(semantic_action, seq_out, cards): нормализует
    risk_level, сравнивает _SEVERITY[semantic] с _SEVERITY[required];
    ниже минимума → violation с required_action; неизвестный уровень →
    concern.

ГРАНИЦА (честно). Сторож по-прежнему читает relation_verdicts как
источник истины и НЕ ловит их опустошение ДО analyze (та же граница,
что в D-GUARD-1 — отдельный механизм, отложено). D-GUARD-3 усиливает
условие сравнения, а не расширяет область чтения.

ПРОВЕРКА (chaos-гейт tests/gate_safeguard.py, секция [D-GUARD-3]):
HIGH→log_only и HIGH→queue роняют строгий прогон; risk_level "high" /
" HIGH " / "High" дают нарушение; неизвестный уровень → CONCERN, не
молча. gate_safeguard 15→23, герметично, 20/20.

СВЯЗЬ: D-GUARD-1 (инвариант, который усилен), D-GUARD-4 (эффективный
вердикт по required_action), audit_silent_paths_2026-07-12.md.
