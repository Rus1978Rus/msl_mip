ЧАСТНЫЙ АВТОРСКИЙ ПРОЕКТ / COMMERCIAL USE PROHIBITED

DOCUMENT_ID: SIMULATION_ARTIFACT_ZERO_WIDTH_SPACE_U200B_TIER2_BY_CODE_v0_3_RU
DOCUMENT_TYPE: SIMULATION_ARTIFACT (RUN_CARD) — нога BY_CODE, ПРОХОДНОЙ прогон
PACKET_TYPE: SIMULATION / PACKET_SUBTYPE: TIER_2_SIMULATION_GATE
LEG: BY_CODE (живой движок msl_mip_runtime)
PAIR_WITH: BY_SPEC — NOT_AVAILABLE (ноги BY_SPEC не существует; двуногость и
  reconcile ЭТИМ артефактом НЕ утверждаются — см. B.6)
SUPERSEDES: SIMULATION_ARTIFACT_ZERO_WIDTH_SPACE_U200B_TIER2_BY_CODE_v0_2_RU
  (pre-patch снимок HONEST_FAIL 6/21 — сохранён как история «до»)
AUTHOR: Руслан Малявский / CREATED_AT: 2026-07-15
STATUS: ACTIVE_ARTIFACT / NOT_LOCKED / NOT_RUNTIME
RUN_CARD_STATUS: PASS (21/21; mutation-adequacy 5/5; preflight 21/21 ALL OK)

ОСНОВАНИЕ ПЕРЕСБОРКИ: конвейер по развилке RUN-CARD DISCREPANCY (пакет
  conveyor_runs/CONVEYOR_PACKET_ZWSP_RUNCARD_DISCREPANCY_2026-07-15.md, 6
  ревьюеров, консенсус «V3→свежий реальный V1/V2») + перепроверка свода.
  Артефакт сгенерирован ИЗ RAW OUTPUT реального прогона (не из памяти, не из
  строки карточки). RAW приложен целиком в B.3.

============================================================
B.0 ПРОВЕНАНС ПРОГОНА (полная фиксация среды)
============================================================
RUN_ID: ZWSP_TIER2_BY_CODE_v3_2026-07-15
RUN_TIMESTAMP: 2026-07-15 23:57 +03:00 (запуск 2026-07-15, локальная машина автора)
ENGINE_COMMIT: 9963a68503ce534cae22bdba04d26cdc9a92cefb (= origin/main; код движка
  на локальном HEAD b42e9bd идентичен — незапушенные коммиты трогают только .md,
  git diff origin/main..HEAD -- "*.py" пуст; working tree чист)
CARD: cards/SIGN_CORE_CARD_ZERO_WIDTH_SPACE_U200B_GEN3_v0_3_RU.md
CARD_COMMIT: 45986d1 (последний коммит, трогавший карточку до этого захода)
CARD_SHA256: 24C66F7F967383E49416940F405125FD1B9AC15164E15BC56D787D974D53ADD2
  (финальное состояние карточки, коммитится вместе с артефактом; отличие от
   состояния на 45986d1 — только строки RUN_CARD_REFERENCE/BY_SPEC_STATUS в шапке,
   внесённые ЭТИМ заходом. Первичный прогон шёл против карточки sha
   D0E5186BAB48E54FE637363C2F7AF42E206915E53BFF0D604058AD1FC62FDEE0; контрольный
   перепрогон против финального состояния дал БАЙТ-ИДЕНТИЧНЫЙ RAW — шапочные
   строки на детекцию не влияют)
BATTERY_ID: ZWSP_TIER2_CORE21 (те же 21 ID, что в v0_2: R1-R6 P1 P2 P4 P5 K1 K3
  U1 U2 D1-D5 T1 N1 — батарея НЕ менялась; менялся код между v0_2 и v0_3)
HARNESS: tests/sim_bycode_v2.py
HARNESS_SHA256: A0C46E6A21B4B884437AE46AB0074B336FF6A5E6BA33880ED2C1FA5985FD4840
HARNESS_PROVENANCE: перенесён из session-scratchpad (оригинал sha
  A55AF12BEC58750201806C21E69BD1582BFE24B1164CC8E3CD3E83A392D91699); отличие
  ТОЛЬКО в блоке путей (repo-relative вместо абсолютных; 11 строк diff);
  батарея/oracle-импорт/measure/classify/мутации байт-идентичны. Контроль:
  прогон из tests/ дал RAW, байт-идентичный прогону оригинала из scratchpad
  (одинаковый RAW_SHA256 ниже).
ORACLE: tests/zwsp_oracle_manifest.py (машинный, перенесён байт-в-байт)
ORACLE_SHA256: 126B0AF413DA80BDDBDA843DDABF7250D5161371E426399C2C23E4603DA51656
ORACLE_HUMAN_PAIR: tests/zwsp_oracle_manifest.md (человекочитаемый, был в репо)
MUTATION_SET_ID: M1_HOST_PATH_SWAP, M2_WITNESS_OFF, M3_ZWSP_SCAN_OFF,
  M4_FACET_RISK_PRODUCING, M5_CTX_ALWAYS_FREETEXT (5 мутаций, каждая с undo)
UNICODE_VERSION: 16.0.0 (Python 3.14.6, unicodedata)
TLD_DATA_VERSION: HERMETIC, закреплённый набор {com,org,net,ru,io,dev,xn--p1ai}
  (_force_tld_state_for_test, сеть не используется)
ENVIRONMENT: Windows 11; py -3 (Python 3.14.6); MSL_MIP_HERMETIC_TLD=1;
  PYTHONUTF8=1; PYTHONIOENCODING=utf-8
RAW_OUTPUT_SHA256: EBB200255251084FB4DD9668EB7B12752780B7A2E15903F80F09AAC6C7975DEA
CARDS_USED: [ZWSP U+200B, FULLWIDTH SOLIDUS U+FF0F] (как в v0_2)
NB: CARD_WARNING (CARD_NOT_CONVEYOR_REVIEWED) в прогоне ОТСУТСТВУЕТ — карточка
  на момент прогона DOCUMENT_STATUS=WORKINGLY_CLOSED (машинный гейт пройден,
  согласуется с author decision 45986d1).

FORMULAS: SIMULATION_RUN ≠ VALIDATION; MEASURE_ONLY ≠ FIX;
  ATTACK_CAUGHT = верный сигнал человеку; FALSE_ALARM = ложь человеку;
  МЕТРИКА = верность совета.

============================================================
B.1 МЕТОД (унаследован от v0_2 без изменений)
============================================================
1. RECONCILE ПО КОРТЕЖУ, не по вердикту: сверяется (CONTEXT, RELATION_ROLE,
   RISK, VERDICT, WITNESS) против машинного oracle. SAME_VERDICT≠SAME_SEMANTICS.
2. PREFLIGHT КОДПОИНТОВ: dump ords+длина, assert must_contain до прогона.
3. MUTATION-ADEQUACY: 5 намеренных дефектов кода; батарея обязана убить каждый;
   sanity — baseline pass-set стабилен после отката мутаций.
M4-инвариант (введён после v0_2): независимая авторитетная карта
RELATION_TYPE→EXPECTED_ROLE в чекере (не импортируется из рантайма) — ловит
«согласованную ложь», когда мутация двигает и карту ролей, и эмиссию.

============================================================
B.2 РЕЗУЛЬТАТ (из RAW; полный RAW — B.3)
============================================================
PREFLIGHT: 21/21 ALL OK (ни одна невидимка не потеряна при подготовке).
БАТАРЕЯ:  registrar 6/6, positions 4/4, combo 2/2, url 2/2, dangerous 5/5,
          controls 2/2 — ИТОГО 21/21, ошибок по типам: НЕТ.
MUTATION-ADEQUACY: 5/5 KILLED (M1 ломает 8 baseline-верных; M2 — 8; M3 — 14;
          M4 — 15; M5 — 14). Sanity: baseline pass-set стабилен = True.
Против v0_2 (6/21, mutation 3/5) закрыты: R1-R5 (witness Zs/Zl/Zp/So),
P1/P2/P4/P5 (ложный HOST/HIGH), K1/K3/D5 (пропуск атаки при втором невидимом),
U1 (QUERY_VALUE), D2 (USERINFO), T1-контроль соответствует oracle; слепые пятна
M2/M4 устранены (M2 стал убиваемым после починки witness-предиката; M4 — после
привязки инварианта к RELATION_TYPE).

============================================================
B.3 RAW OUTPUT (полный, дословный; sha256 = RAW_OUTPUT_SHA256 из B.0)
============================================================
==================================================================================================================================
ZWSP TIER_2 BY_CODE v2 — verified core 21 (live msl_mip_runtime; cards=[ZWSP,FW-SOLIDUS]; hermetic TLD)
==================================================================================================================================

[PREFLIGHT] codepoint dump + must_contain assertion
  R1  len= 11 must_contain=['U+2800']  OK
  R2  len= 11 must_contain=['U+00A0']  OK
  R3  len= 11 must_contain=['U+202F']  OK
  R4  len= 11 must_contain=['U+2028']  OK
  R5  len= 10 must_contain=['U+2029']  OK
  R6  len=  9 must_contain=['U+200B']  OK
  P1  len= 11 must_contain=['U+200B']  OK
  P2  len= 11 must_contain=['U+200B']  OK
  P4  len= 16 must_contain=['U+200B']  OK
  P5  len= 41 must_contain=['U+200B']  OK
  K1  len= 12 must_contain=['U+200B', 'U+200D']  OK
  K3  len= 12 must_contain=['U+200B', 'U+2062']  OK
  U1  len= 32 must_contain=['U+200B']  OK
  U2  len= 17 must_contain=['U+200B']  OK
  D1  len= 11 must_contain=['U+200B']  OK
  D2  len= 27 must_contain=['U+200B']  OK
  D3  len= 12 must_contain=['U+200B']  OK
  D4  len= 20 must_contain=[]  OK
      decoded len=12 must_contain=['U+200B']  OK
  D5  len= 12 must_contain=['U+200B', 'U+2800']  OK
  T1  len=  9 must_contain=['U+200B']  OK
  N1  len= 25 must_contain=['U+0020']  OK
  PREFLIGHT: ALL OK

[BASELINE] measured tuple vs manifest
ID  CLASS      INPUT                                    CTX              RISK   VERDICT              WIT      RES
----------------------------------------------------------------------------------------------------------------------------------
R1  registrar  goog<U+2800>le.com                       -                -      pass                 U+2800   ВЕРНО
R2  registrar  paypal<U+00A0>.com                       -                -      pass                 U+00A0   ВЕРНО
R3  registrar  admin<U+202F>panel                       -                -      pass                 U+202F   ВЕРНО
R4  registrar  line1<U+2028>line2                       -                -      pass                 U+2028   ВЕРНО
R5  registrar  para<U+2029>break                        -                -      pass                 U+2029   ВЕРНО
R6  registrar  text<U+200B>here                         BYTE_EXACT_TOKEN MEDIUM queue_for_review     -        ВЕРНО
P1  positions  <U+200B>paypal.com                       HIDDEN_BOUNDARY_PADDING MEDIUM queue_for_review     -        ВЕРНО
P2  positions  paypal.com<U+200B>                       HIDDEN_BOUNDARY_PADDING MEDIUM queue_for_review     -        ВЕРНО
P4  positions  paypal.com<U+200B>/path                  PATH             MEDIUM queue_for_review     -        ВЕРНО
P5  positions  docs.example.com/guide/very-long<U+200B> PATH             MEDIUM queue_for_review     -        ВЕРНО
K1  combo      goog<U+200B><U+200D>le.com               HOST             HIGH   hold_pending_review  U+200D   ВЕРНО
K3  combo      goog<U+200B><U+2062>le.com               HOST             HIGH   hold_pending_review  U+2062   ВЕРНО
U1  url        https://site.example/?q=bad<U+200B>word  QUERY_VALUE      MEDIUM queue_for_review     -        ВЕРНО
U2  url        us<U+200B>er@example.com                 EMAIL            MEDIUM queue_for_review     -        ВЕРНО
D1  dangerous  paypal<U+200B>.com                       HOST             HIGH   hold_pending_review  -        ВЕРНО
D2  dangerous  http://paypal.com<U+200B>@evil.com       USERINFO         MEDIUM queue_for_review     -        ВЕРНО
D3  dangerous  paypal<U+200B>.com.                      HOST             HIGH   hold_pending_review  -        ВЕРНО
D4  dangerous  paypal%E2%80%8Bl.com                     -                -      pass                 -        ВЕРНО
        └ STAGE2(decoded): ctx=HOST risk=HIGH verdict=hold_pending_review wit=-
D5  dangerous  goog<U+200B><U+2800>le.com               HOST             HIGH   hold_pending_review  U+2800   ВЕРНО
T1  controls   日本語<U+200B>のテキスト                         BYTE_EXACT_TOKEN MEDIUM queue_for_review     -        ВЕРНО
N1  controls   <U+043E>бычный текст с пр<U+043E>белами  -                -      pass                 -        ВЕРНО

============================================================
СЧЁТ ПО КЛАССАМ
============================================================
  registrar : 6/6 верно  (0 ошибок)
  positions : 4/4 верно  (0 ошибок)
  combo     : 2/2 верно  (0 ошибок)
  url       : 2/2 верно  (0 ошибок)
  dangerous : 5/5 верно  (0 ошибок)
  controls  : 2/2 верно  (0 ошибок)
  ИТОГО     : 21/21

ОШИБКИ ПО ТИПАМ:

============================================================
MUTATION-ADEQUACY (проверка самой проверки)
============================================================
  M1_HOST_PATH_SWAP         : KILLED  (ломает 8 baseline-верных: ['D1', 'D3', 'D4', 'D5', 'K1', 'K3', 'P4', 'P5'])
  M2_WITNESS_OFF            : KILLED  (ломает 8 baseline-верных: ['D5', 'K1', 'K3', 'R1', 'R2', 'R3', 'R4', 'R5'])
  M3_ZWSP_SCAN_OFF          : KILLED  (ломает 14 baseline-верных: ['D1', 'D2', 'D3', 'D4', 'D5', 'K1', 'K3', 'P1'])
  M4_FACET_RISK_PRODUCING   : KILLED  (ломает 15 baseline-верных: ['D1', 'D2', 'D3', 'D4', 'D5', 'K1', 'K3', 'P1'])
  M5_CTX_ALWAYS_FREETEXT    : KILLED  (ломает 14 baseline-верных: ['D1', 'D2', 'D3', 'D4', 'D5', 'K1', 'K3', 'P1'])

  MUTATION_ADEQUACY: 5/5 killed
  (sanity) baseline pass-set stable after mutations: True

============================================================
B.4 ВОСПРОИЗВЕДЕНИЕ
============================================================
  cd <repo>
  set MSL_MIP_HERMETIC_TLD=1 & set PYTHONUTF8=1
  py -3 tests\sim_bycode_v2.py
Ожидаемый выход побайтово совпадает с B.3 (RAW_OUTPUT_SHA256) при том же
ENGINE_COMMIT / CARD_SHA256 / UNICODE_VERSION.

============================================================
B.5 СТАТУС ПРОВАЛОВ v0_2 НА ЭТОМ КОДЕ (по кейсам батареи)
============================================================
Все 15 упавших в v0_2 кейсов на ENGINE_COMMIT 9963a68 проходят против oracle.
Соответствие корней (фикс-коммиты между dd9a944 и 9963a68, ключевой b937911):
  F-NEW-1 (пропуск атаки при 2-м невидимом)  → K1/K3/D5 ВЕРНО (HOST/HIGH + witness)
  F-NEW-2 (ложный HOST/HIGH у целого домена)  → P1/P2/P4/P5 ВЕРНО (PADDING/PATH, MEDIUM)
  F-NEW-3 (witness-предикат узок)             → R1-R5 ВЕРНО (witness Zs/Zl/Zp/So есть)
  F-NEW-4 (нет QUERY_VALUE)                   → U1 ВЕРНО (QUERY_VALUE/MEDIUM)
  F-NEW-5 (нет userinfo)                      → D2 ВЕРНО (USERINFO/MEDIUM)
  F-KNOWN-6 (CJK T1)                          → T1 ВЕРНО против ТЕКУЩЕГО oracle
ЭТО КОНСТАТАЦИЯ ПО БАТАРЕЕ, не ревью фиксов: качество/полнота самих патчей
F-NEW-1..5 этим артефактом НЕ судится (граница пакета развилки).

============================================================
B.6 ЧТО ЭТОТ АРТЕФАКТ НЕ УТВЕРЖДАЕТ (честные границы)
============================================================
- НЕ двуногость: ноги BY_SPEC НЕ СУЩЕСТВУЕТ (BY_SPEC_STATUS: NOT_AVAILABLE).
  Reconcile «BY_SPEC × BY_CODE» не выполнялся и НЕ заявляется — сейчас он свёл
  бы BY_CODE сам с собой. Единственная независимая опора — машинный oracle
  (tests/zwsp_oracle_manifest.py), написанный до прогонов и не выводимый из ног.
- НЕ SIMULATION_GATE_PASSED формально: присвоение статусов — только автор.
- НЕ покрытие за пределами батареи 21 (см. процедуру §11: прохождение = нет
  необъяснённых расхождений ВНУТРИ заявленной батареи, не отсутствие ошибок).
- НЕ ревью корневых патчей F-NEW-1..5 (B.5 — констатация по кейсам).

============================================================
B.7 VERDICT
============================================================
SIMULATION_VERDICT (BY_CODE): PASS — 21/21; MUTATION_ADEQUACY 5/5;
  PREFLIGHT 21/21; baseline стабилен.
Персистентность закрыта: харнесс + машинный oracle внесены в репозиторий вместе
с артефактом; эфемерных зависимостей у артефакта нет.
NEXT (вне этого артефакта, по решению автора): нога BY_SPEC + reconcile-сводка;
формальный SIMULATION_GATE; судьба WORKINGLY_CLOSED-пометки — авторские шаги.

END_OF_SIMULATION_ARTIFACT
