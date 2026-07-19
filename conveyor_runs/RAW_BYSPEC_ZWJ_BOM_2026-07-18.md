ЧАСТНЫЙ АВТОРСКИЙ ПРОЕКТ / COMMERCIAL USE PROHIBITED

DOCUMENT_ID: RAW_BYSPEC_ZWJ_BOM_2026-07-18
DOCUMENT_TYPE: RAW_REVIEW_BUNDLE (сверяемый источник — НЕ свод)
DATE: 2026-07-18
PACKET: SIM_PACKET_BYSPEC_ZWJ_BOM_2026-07-18 (двуногая симуляция, слепая нога)

СОСТАВ (по self-заявленному LEAKAGE_STATUS):
  BLIND (полностью): Copilot (Microsoft), Qwen, DeepSeek (reasoning), Gemini.
  BLIND частично: Kimi (Moonshot) — ZWJ BLIND; BOM B1/B5 НЕЗАВИСИМ; BOM B2/B3/B4 COMPROMISED
    (видел BOM THREE_LEVEL_DIVERGENCE в guard-пакете §1).
  CONTROL (self-COMPROMISED, не в счёт слепых): GPT-5.6 (OpenAI) — видел измеренную BOM-раскладку.
  META (оценка метода + предсказания, не боевой REVIEW_RESULT, нет LEAKAGE_STATUS): блок-1.
  Claude self-leg по BY_SPEC в этом круге НЕ подавался (только пакет + логи).
  Слепых ног: ZWJ = 5; BOM B1/B5 = 5 (Kimi независим); BOM B2/B3/B4 = 4 (Kimi контам.).

============================================================
ПРЕДСКАЗАНИЯ ПО КОНТЕКСТАМ (по raw; Ч=ЧИСТО В=ВОЗМОЖНАЯ Р=РЕАЛЬНАЯ)
============================================================
Ctx | Copilot | Qwen | DeepSeek | Gemini | Kimi | (GPT control)
Z1  |  Ч      |  Ч   |   Ч      |  Ч     |  Ч   |  Ч
Z2  |  Р      |  Р   |   Р      |  Р     |  Р   |  Р
Z3  |  Ч/В*   |  Ч   |   Ч      |  Ч/В*  |  Ч(alt В)* | Ч
Z4  |  В      |  В   |   В      |  Р     |  Р(alt В)* | В
Z5  |  Ч/В(низ)* | В |   Ч      |  В     |  В   |  В
B1  |  Ч      |  Ч   |   Ч      |  Ч     |  Ч[indep] |  Ч
B2  |  Р      |  Р   |   Р      |  Р     |  Р[contam] |  Р
B3  |  В      |  В   |   Р      |  Р     |  В[contam] |  Р
B4  |  В      |  В   |   Р      |  В     |  Р(alt В)[part-contam] | В
B5  |  Р      |  Р   |   Р      |  Р     |  Р[indep] |  Р
  * = ревьюер дал оговорку/альтернативу (не плоский уровень).

============================================================
BY_CODE (измерено прогоном 2026-07-18, штатный analyze; маппинг hold↔Р/queue↔В/pass↔Ч)
============================================================
  Z1 emoji            pass   -> ЧИСТО
  Z2 latin host       hold   -> РЕАЛЬНАЯ
  Z3 persian word     queue  -> ВОЗМОЖНАЯ
  Z4 token/ident      queue  -> ВОЗМОЖНАЯ
  Z5 free text        pass   -> ЧИСТО
  B1 leading+text     queue  -> ВОЗМОЖНАЯ   [B1' leading+json: pass -> ЧИСТО — B1 КОНТЕКСТ-ЗАВИСИМ]
  B2 mid-host         hold   -> РЕАЛЬНАЯ
  B3 mid-email/token  queue  -> ВОЗМОЖНАЯ
  B4 leading+domain   queue  -> ВОЗМОЖНАЯ
  B5 parser-desync    PENDING (рантайм не наблюдает рассинхрон из одной строки; карточка RISK_CASE PENDING)

============================================================
ПРОЦЕССНАЯ НАХОДКА (утечка BOM-раскладки)
============================================================
3 независимых указания на утечку: (1) Kimi — BOM THREE_LEVEL_DIVERGENCE протекла из
guard-пакета §1, пометил B2/B3/B4 COMPROMISED; (2) GPT — сам объявил COMPROMISED от той же
раскладки; (3) META-блок — предупредил о leakage-риске. ВЫВОД: межпакетные ссылки на
ИЗМЕРЕННЫЕ вердикты (как THREE_LEVEL_DIVERGENCE, как §5/§6 reader-прогона) фильтровать
ПЕРЕД раздачей слепой ноги.

END_OF_RAW_BUNDLE
