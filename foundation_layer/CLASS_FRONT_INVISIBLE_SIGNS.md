ЧАСТНЫЙ АВТОРСКИЙ ПРОЕКТ / COMMERCIAL USE PROHIBITED

DOCUMENT_ID: CLASS_FRONT_INVISIBLE_SIGNS
DOCUMENT_TYPE: CLASS_FRONT_REGISTER
CREATED_AT: 2026-07-13
AUTHOR: Руслан Малявский
BASIS: AUTHOR_DECISION_20260713_D-ZWSP-STATUS (Q2)
PROJECT: MSL/MIP Sign Alphabet

НАЗНАЧЕНИЕ: реестр КЛАССОВЫХ зависимостей класса «невидимые знаки» —
  обязательств уровня КЛАССА, которые НЕ должны блокировать отдельную карточку
  как её дефект. Держит их видимыми, чтобы не потерялись, но и не превращались
  в тупик курицы-яйца для первого образца.

============================================================
CLASS_DEPENDENCY: INVISIBLE_DEFAULT_IGNORABLE_GUARD
============================================================
STATUS: NOT_YET_BUILT
PROMISED_BY: ARCH_DECISION_INVISIBLE_SIGNS_HYBRID_C
NATURE: классовый ПОЛИТИЧЕСКИЙ слой (policy) для ВСЕХ невидимых —
  единая реализация классовых свойств: невидимость, неудаляемость
  нормализацией (NFC/NFD/NFKC/NFKD), strip/flag/log/canonicalize; выполняется
  ПЕРВЫМ, отдаёт per-card matcher канонический поток + метаданные; основа для
  тонких карточек невидимых.
BUILD_CONDITION: из >=3 РАЗНЫХ невидимых образцов (НЕ строить на N=1 —
  переобучение под один знак, риск сломать легитимные ZWJ/ZWNJ; принцип «не
  обобщай с одного»).
THEN: ре-валидировать ВСЕ карточки класса на построенном гарде.
PARTIAL_COVERAGE_TODAY: регистратор незнакомых невидимых (INVISIBLE_UNCARDED_
  REGISTRAR, msl_mip_runtime) ЧАСТИЧНО покрывает под-обещание гарда «незнакомое
  не проходит МОЛЧА» (witness). НО witness ≠ policy: регистратор свидетельствует
  присутствие, не оценивает риск и не канонизирует поток. Проверено:
  goog<U+2063>le.com → PASS + witness, НЕ HOST/HIGH. Гард всё равно нужен.

BLOCKS:
  - НЕ блокирует WORKINGLY_CLOSED отдельной карточки (класс-front, не дефект карточки).
  - Блокирует ARTIFACT_CONFIRMED карточек класса (нужна ре-валидация на гарде).

============================================================
SPECIMENS (образцы класса)
============================================================
- ZWSP (U+200B) — METHOD_REFERENCE_SPECIMEN, первый; проведён строгим
  инструментом (two-legged simulation + mutation-adequacy 5/5 + reconcile).
  Статус карточки: WORKINGLY_CLOSED_PENDING_CLASS_GUARD (AUTHOR_DECISION
  D-ZWSP-WORKINGLY-CLOSED 45986d1; прежний VALIDATED_BY_TOOL/PENDING_CONVEYOR_REVIEW
  устарел — конвейер-ревью пройден).
- (нужны ещё >=2 разных: кандидаты — ZWJ/ZWNJ join-control, VS16 variation
  selector, BOM/WJ format — чтобы гард увидел РАЗБРОС класса, а не один ZWSP.)

============================================================
RULE_REFERENCE
============================================================
- PHAGO-применимость для невидимых (и всех знаков): см.
  foundation_layer/RULE_PHAGO_APPLICABILITY_v0_1.md.

END_OF_CLASS_FRONT_REGISTER
