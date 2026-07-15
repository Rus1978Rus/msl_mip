ЧАСТНЫЙ АВТОРСКИЙ ПРОЕКТ / COMMERCIAL USE PROHIBITED

# MSL/MIP — ПРОЦЕДУРА И СМЫСЛ СИМУЛЯЦИИ

**DOCUMENT_ID:** `MSL_MIP_SIMULATION_PROCEDURE_v0_1_RU`  
**STATUS:** `PROCEDURE_DRAFT / FOR_AUTHOR_DECISION`  
**AUTHOR:** Руслан Малявский  
**PURPOSE:** проверка соответствия между обещаниями карточки и фактическим поведением системы

---

## 1. ЧТО ТАКОЕ СИМУЛЯЦИЯ

Симуляция — это управляемый прогон заранее подготовленной батареи входов через правила карточки и через реальную систему.

Симуляция отвечает на вопрос:

```text
ДЕЛАЕТ ЛИ СИСТЕМА ТО,
ЧТО ОБЕЩАЕТ КАРТОЧКА?
```

Основная формула:

```text
CARD_DECLARED
vs
DETECTOR_PRODUCED
```

Симуляция не является обычным чтением документа и не является мнением ревьюера.

В симуляции карточка рассматривается как исполняемая спецификация:

```text
INPUT
→ CARD RULES
→ EXPECTED OUTPUT
```

А затем тот же вход подаётся в реальный код:

```text
INPUT
→ LIVE ENGINE
→ ACTUAL OUTPUT
```

Расхождение между ожидаемым и фактическим результатом является находкой.

---

## 2. ЗАЧЕМ НУЖНА СИМУЛЯЦИЯ

Обычный conveyor review проверяет:

- логичность карточки;
- полноту структуры;
- отсутствие внутренних противоречий;
- корректность формулировок;
- качество модели знака.

Но документ может быть логичным, а код — работать иначе.

```text
GOOD SPECIFICATION
≠
CORRECT IMPLEMENTATION
```

```text
REVIEW PASSED
≠
RUNTIME BEHAVIOUR VERIFIED
```

```text
CODE RUNS
≠
CODE FOLLOWS CARD
```

Симуляция закрывает промежуток между замыслом и исполнением.

---

## 3. ЧТО ИМЕННО ИЗМЕРЯЕТСЯ

Сравнивается не только итоговый verdict.

Для каждого входа сравнивается полный кортеж:

```text
SIGN_DETECTED
CODEPOINT
SIGN_OFFSET
CONTEXT
RELATION_TYPE
RUNTIME_ROLE
PROTECTED_SCOPE
RISK_LEVEL
RECOMMENDED_ACTION
FINAL_VERDICT
WITNESS_RECORDS
INTEGRITY_STATUS
FINDING_BASIS
```

Основной принцип:

```text
SAME_VERDICT
≠
SAME_BEHAVIOUR
```

Например:

```text
BY_SPEC:
  CONTEXT = QUERY
  RISK = MEDIUM

BY_CODE:
  CONTEXT = PATH
  RISK = MEDIUM
```

Итоговый уровень совпал, но система сообщила человеку неправильный контекст. Это считается провалом симуляции.

---

## 4. ДВЕ НОГИ СИМУЛЯЦИИ

### 4.1. BY_SPEC — ручной прогон по карточке

Независимые модели или проверяющие работают как процессоры. Они не оценивают качество правила, а исполняют его буквально:

```text
INPUT
→ CARD FIELD
→ CARD FORMULA
→ EXPECTED CONTEXT
→ EXPECTED RISK
→ EXPECTED ACTION
```

Результат BY_SPEC фиксируется до просмотра выхода реального кода. Это предотвращает подгонку ожидания под фактический результат.

### 4.2. BY_CODE — прогон через живой движок

Та же самая строка, без изменений, подаётся в рабочую систему.

Фиксируется фактический результат:

```text
ACTUAL SIGN
ACTUAL CONTEXT
ACTUAL RELATION
ACTUAL RISK
ACTUAL ACTION
ACTUAL WITNESS
ACTUAL INTEGRITY STATUS
```

BY_CODE является фактом исполнения, но не автоматически правильным ответом.

```text
ACTUAL OUTPUT
≠
CORRECT OUTPUT
```

---

## 5. ORACLE — ОЖИДАЕМЫЙ ЭТАЛОН

Для каждого входа должен существовать заранее записанный oracle — эталон ожидаемого результата.

```text
CASE_ID: P5

INPUT:
  docs.example.com/guide/very-long<U+200B>-section

EXPECTED:
  SIGN: U+200B
  CONTEXT: PATH
  RISK: MEDIUM
  ACTION: QUEUE_FOR_REVIEW
  WITNESS: NONE
```

Oracle должен быть:

- создан до запуска кода;
- привязан к конкретной версии карточки;
- проверяемым;
- машинно-читаемым;
- не изменяемым молча после получения результата.

Если oracle меняется, должна быть указана причина:

```text
ORACLE_PATCH
AUTHOR_DECISION
NEW_EVIDENCE
```

---

## 6. БАТАРЕЯ СИМУЛЯЦИИ

Батарея — это не случайный набор примеров. Она должна содержать разные классы входов.

### 6.1. ATTACK CASES

Строки, где система обязана предупредить:

```text
невидимый знак внутри host
разрыв защищённого токена
комбинация нескольких масок
userinfo deception
query manipulation
path manipulation
```

Главный вопрос:

```text
НЕ ПРОМОЛЧАЛА ЛИ СИСТЕМА?
```

### 6.2. PEACE / SAFE CASES

Легитимные случаи:

```text
типографика
учебное упоминание
test fixture
свободный текст
законная языковая функция
обычные пробелы и разделители
```

Главный вопрос:

```text
НЕ СОЗДАЛА ЛИ СИСТЕМА ЛОЖНУЮ ТРЕВОГУ?
```

Для системы оповещения ложная тревога особенно опасна, потому что обучает человека игнорировать последующие предупреждения.

### 6.3. UNKNOWN CASES

Незнакомые знаки без карточек.

Проверяется:

```text
сработал ли registrar;
указан ли codepoint;
указано ли отсутствие карточки;
не выдуман ли риск;
не потерян ли witness.
```

Ожидаемая формула:

```text
UNKNOWN SIGN
→ WITNESS
→ UNVERIFIABLE
→ VERDICT UNCHANGED
```

### 6.4. BOUNDARY CASES

Знак помещается:

```text
в начало;
в конец;
перед разделителем;
после разделителя;
в host;
в path;
в query;
в userinfo;
в email local-part;
на границе компонентов.
```

Эти случаи проверяют правильность определения позиции, а не только наличие знака.

### 6.5. COMBINATION CASES

Проверяются:

```text
известный + известный;
известный + неизвестный;
неизвестный + известный;
несколько одинаковых знаков;
несколько разных невидимых знаков.
```

Главный вопрос:

```text
НЕ ПОТЕРЯЛАСЬ ЛИ ОДНА НАХОДКА
ИЗ-ЗА БОЛЕЕ СИЛЬНОЙ ДРУГОЙ?
```

---

## 7. ПОДГОТОВКА ВХОДОВ

Каждый вход должен быть сохранён буквально.

Обязательные поля:

```text
CASE_ID
INPUT_LITERAL
CODEPOINT_SEQUENCE
UTF8_HEX
INPUT_LENGTH
SIGN_OFFSETS
NORMALIZATION_FORM
EXPECTED_OUTPUT
```

Для невидимых символов текстового изображения недостаточно. Нужно фиксировать кодпоинты, иначе знак может потеряться при копировании.

```text
DECLARED_CODEPOINTS
=
ACTUAL_CODEPOINTS
```

---

## 8. ПРОЦЕДУРА СИМУЛЯЦИИ

### ЭТАП 1. ЗАФИКСИРОВАТЬ ВЕРСИИ

```text
CARD_VERSION
CARD_HASH
ENGINE_VERSION
ENGINE_COMMIT
ORACLE_VERSION
BATTERY_VERSION
UNICODE_VERSION
MUTATION_SET_VERSION
```

Без этого результат нельзя воспроизвести.

### ЭТАП 2. СОБРАТЬ БАТАРЕЮ

Для каждого правила карточки должен существовать хотя бы один положительный и один отрицательный вход.

Батарея должна проверять не количество строк, а разные ветви поведения.

### ЭТАП 3. СОЗДАТЬ ORACLE

До запуска кода записать ожидаемый полный кортеж каждого case.

### ЭТАП 4. ВЫПОЛНИТЬ BY_SPEC

Каждый процессор получает карточку, конкретный вход и форму ожидаемого ответа.

Процессору запрещено:

- критиковать правило;
- улучшать его;
- угадывать намерение автора;
- смотреть BY_CODE заранее;
- подгонять ответ под здравый смысл.

Он обязан выполнить карточку буквально.

### ЭТАП 5. ВЫПОЛНИТЬ BY_CODE

Каждый вход прогоняется через живой движок. Сохраняется полный raw output, а не только человекочитаемое резюме.

### ЭТАП 6. RECONCILE — СОПОСТАВИТЬ ДВЕ НОГИ

Для каждого поля выполняется сравнение:

```text
EXPECTED
ACTUAL
MATCH / MISMATCH
```

### ЭТАП 7. КЛАССИФИЦИРОВАТЬ НАХОДКУ

```text
FALSE_NEGATIVE
FALSE_POSITIVE
CONTEXT_MISMATCH
RISK_OVERSTATEMENT
RISK_UNDERSTATEMENT
WITNESS_MISSING
WITNESS_FLOOD
RELATION_TYPE_MISMATCH
SCOPE_MISMATCH
INTEGRITY_FAILURE
SPEC_IMPLEMENTATION_DRIFT
ORACLE_DEFECT
BATTERY_DEFECT
```

### ЭТАП 8. НАЙТИ КОРЕНЬ

Нельзя считать каждый неудачный вход отдельным багом.

```text
один корень
→ сколько симптомов
```

Патч должен закрывать корень, а не один пример.

### ЭТАП 9. ПРОВЕРИТЬ РЕГРЕССИЮ

После исправления повторно запускаются:

```text
исходный упавший case;
соседние cases;
старые карточки, использующие тот же detector;
общая regression battery.
```

```text
FIXED ONE CASE
≠
FIXED THE SYSTEM
```

### ЭТАП 10. MUTATION ADEQUACY

В систему намеренно вносятся контролируемые дефекты:

```text
отключить witness;
поменять HOST на PATH;
поменять PRIMARY на SUPPORTING_FACET;
удалить scope;
отключить регистрацию codepoint;
разрешить неизвестный RELATION_TYPE;
сломать aggregation.
```

Батарея должна обнаружить каждую мутацию.

```text
MUTATION_KILLED
→ тест действительно способен увидеть дефект

MUTATION_SURVIVED
→ слепая зона батареи или oracle
```

Mutation adequacy проверяет не систему, а качество самой проверки.

### ЭТАП 11. ПОВТОРНЫЙ ПОЛНЫЙ ПРОГОН

После патча повторяется вся батарея, а не только упавший case.

Фиксируется:

```text
BEFORE
AFTER
NEW_FAILURES
CLOSED_FAILURES
UNCHANGED_BOUNDARIES
```

### ЭТАП 12. AUTHOR DECISION

Симуляция не присваивает окончательный статус карточке. Она выдаёт доказательства для решения автора:

```text
SIMULATION_RESULT:
  PASS
  PASS_WITH_BOUNDARIES
  HONEST_FAIL
  INVALID_BATTERY
  INVALID_ORACLE
```

```text
SIMULATION_RESULT
≠
AUTHOR_DECISION
```

---

## 9. КАК СЧИТАТЬ РЕЗУЛЬТАТ

Одного числа недостаточно.

Нужно разделять:

```text
ATTACK:
  passed / total

PEACE:
  passed / total

UNKNOWN:
  witnessed / total

CONTEXT:
  matched / total

MUTATIONS:
  killed / total
```

Дополнительно:

```text
FALSE_NEGATIVES
FALSE_POSITIVE_QUEUE
FALSE_POSITIVE_HOLD
WITNESS_MISSES
CONTEXT_MISMATCHES
SAME_VERDICT_DIFFERENT_REASON
```

---

## 10. ПРИОРИТЕТ ПРОВАЛОВ

Для системы оповещения:

```text
1. FALSE_NEGATIVE:
   система промолчала при угрозе.

2. WITNESS_MISSING:
   неизвестный знак прошёл незамеченным.

3. FALSE_POSITIVE_ON_LEGITIMATE_USE:
   система подрывает доверие нормальными случаями.

4. FALSE_HIGH/HOLD:
   система чрезмерно останавливает человека.

5. CONTEXT_MISMATCH:
   уровень совпал, но объяснение ложно.

6. TRACE OR DOCUMENTATION MISMATCH.
```

---

## 11. ЧТО СИМУЛЯЦИЯ НЕ ДОКАЗЫВАЕТ

Симуляция не доказывает:

```text
что батарея охватывает все возможные Unicode-строки;
что карточка философски или логически безошибочна;
что одинаковые BY_SPEC и BY_CODE являются истинными;
что намерение пользователя определено правильно;
что отсутствуют ошибки в шрифтах и rendering engines;
что система безопасна в production;
что один successful run является validation навсегда.
```

Если обе ноги ошибаются одинаково:

```text
BY_SPEC = WRONG
BY_CODE = SAME WRONG
```

reconcile не увидит проблему. Поэтому необходим независимый oracle и внешний conveyor review.

---

## 12. СМЫСЛ СИМУЛЯЦИИ ДЛЯ ПРОЕКТА

Симуляция переводит карточку из режима:

```text
«описание кажется логичным»
```

в режим:

```text
«описание предъявило проверяемые обещания,
система была вынуждена их выполнить,
расхождения обнаружены и воспроизведены».
```

Главная ценность не в получении зелёного результата.

Главная ценность — принудительное обнаружение расхождений:

```text
ОБЕЩАНО
≠
ИСПОЛНЕНО
```

Симуляция делает ошибку видимой раньше, чем карточка станет каноном.

---

## 13. КАНОНИЧЕСКАЯ ФОРМУЛА

```text
CARD
→ DECLARED BEHAVIOUR

BATTERY
→ CONTROLLED INPUTS

BY_SPEC
→ EXPECTED BEHAVIOUR

BY_CODE
→ ACTUAL BEHAVIOUR

RECONCILE
→ DIFFERENCES

MUTATION
→ TEST OF THE TEST

ROOT ANALYSIS
→ PATCH TARGET

REGRESSION RUN
→ PATCH VERIFICATION

AUTHOR_DECISION
→ STATUS
```

---

## 14. КРАТКОЕ ОПРЕДЕЛЕНИЕ

```text
СИМУЛЯЦИЯ MSL/MIP —
это воспроизводимая процедура,
в которой одинаковая батарея входов
исполняется по карточке и по живому коду,
после чего сравнивается полный кортеж результатов,
проверяется способность теста ловить намеренные мутации,
а обнаруженные расхождения классифицируются
как дефекты карточки, кода, oracle или батареи.
```

---

## 15. ГЛАВНЫЙ ИНВАРИАНТ

```text
ПРОЙТИ СИМУЛЯЦИЮ
≠
НЕ ИМЕТЬ ОШИБОК
```

```text
ПРОЙТИ СИМУЛЯЦИЮ
=
НЕ ИМЕТЬ НЕОБЪЯСНЁННЫХ РАСХОЖДЕНИЙ
ВНУТРИ ЗАЯВЛЕННОЙ БАТАРЕИ
```

---

## 16. ЛИФЕЦИКЛ И СТАТУС

```text
SIMULATION PROCEDURE
→ GENERAL PROJECT PROCEDURE

CARD
→ REFERENCES PROCEDURE

RUN ARTIFACT
→ STORES BATTERY, ORACLE, RAW OUTPUT, RECONCILE, MUTATIONS

AUTHOR_DECISION
→ ASSIGNS FINAL STATUS
```

Сама процедура не является доказательством конкретной карточки.

```text
PROCEDURE EXISTS
≠
CARD PASSED PROCEDURE
```

---

## СВЯЗЬ

Перекрёстные ссылки на родственные документы проекта (добавлено при заведении файла
в foundation_layer; тело выше — авторское, не изменялось):

- `foundation_layer/drafts/DRAFT_CONVEYOR_PROCEDURE_2026-07-15.md` — процедура
  конвейера; симуляция — барьер ВНУТРИ общего потока card → конвейер → симуляция → код.
- `foundation_layer/RULE_WHEN_CONVEYOR_REQUIRED_v0_1.md` — когда конвейер обязателен.
- `foundation_layer/drafts/DRAFT_PHAGO_LAYER_AND_SIMULATION_GATE_2026-07-13.md` —
  симуляция как обязательный барьер (исходный замысел).
- `foundation_layer/drafts/DRAFT_PRINCIPLE_AI_IN_THE_LOOP_2026-07-13.md` — BY_CODE
  как не-галлюцинирующий якорь; одна нога = консенсус галлюцинаций.
- `conveyor_runs/ORACLE_ZWSP_NEIGHBORS_2026-07-15.md` — пример oracle-манифеста,
  заведён по этой процедуре.
- `foundation_layer/OPEN_NODE_CONVEYOR_REVIEW_FORMAT.md` — формат ревью открыт;
  согласовать при закрытии.

---

**END_OF_DOCUMENT**
