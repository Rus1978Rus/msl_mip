"""
Матчер для ☠ (U+2620, SKULL_AND_CROSSBONES).

Структура аналогична matchers/skull_matcher.py (тот же ZONE_3,
epoch-зависимая интерпретация). Карточка WORKINGLY_CLOSED; matcher
NOT_PRODUCTION — ожидает финального прогона SIMULATION_GATE и решения
автора об ARTIFACT_CONFIRMED (см. SIGN_CORE_CARD).
"""

import re


def _contains_word(text_lower: str, phrase: str) -> bool:
    """Поиск целого слова/фразы по границам слов, не подстроки (тот
    же приём, что в skull_matcher.py — substring-поиск ловил бы
    'яд' внутри других слов)."""
    pattern = r"\b" + re.escape(phrase) + r"\b"
    return re.search(pattern, text_lower) is not None


EPOCH_1_KEYWORDS = (
    "ядовито", "яд", "токсично", "опасно", "смертельно", "отравлю",
    "отравить", "убью", "убить",
)
EPOCH_2_KEYWORDS = (
    "погиб", "умер в игре", "game over", "начать заново", "респавн",
)
EPOCH_3_KEYWORDS = (
    "жёстко", "жестко", "смешно", "ору", "это было", "экзамен",
)

_THREAT_PHRASES = (
    "я тебя отравлю", "я тебя убью", "ты умрёшь", "ты умрешь",
    # MATCHER_PATCH_01: расширение покрытия RISK_CASE_001 по
    # ADVERSARIAL_COVERAGE полной карточки (A2, A3)
    "не доживёшь", "не доживешь", "тебе конец",
)

# MATCHER_PATCH_01: RISK_CASE_002 FALSE_HAZARD_AUTHORITY_MIMICRY —
# слова-заявки на официальность/сертификацию рядом со знаком опасности
# (карточка: знак не подтверждает регуляторный авторитет)
_FALSE_AUTHORITY_KEYWORDS = (
    "сертифицировано", "сертифицирован", "официально", "официальное",
    "официальный", "гост", "одобрено", "лицензировано",
    "от администрации", "администрация",
)

# MATCHER_PATCH_01: RISK_CASE_003 MEDICAL_INSTRUCTION_OBFUSCATION —
# императив приёма/смешивания + вещество. Структурный паттерн
# потенциально вредной инструкции; ироническая рамка НЕ снижает риск
# (GUARD карточки: неоднозначность эскалирует, default НЕ "это ирония")
_HARM_INSTRUCTION_VERBS = (
    "прими", "примите", "выпей", "выпейте", "проглоти", "проглотите",
    "смешай", "смешайте", "вдохни", "вдохните",
)
_HARM_SUBSTANCE_WORDS = (
    "таблетки", "таблетку", "таблеток", "лекарства", "лекарство",
    "отбеливатель", "аммиак", "хлорку", "хлорка", "уксус",
    "растворитель", "антифриз",
)


def detect_epoch(text: str) -> str:
    """ACTIVE_EPOCH — в отличие от 💀 (где EPOCH_3 доминирует
    глобально), у ☠ EPOCH_1 имеет приоритет при явном ключевом
    слове (знак физически используется как предупреждение об
    опасности до сих пор — см. CAPTURE_HISTORY карточки)."""
    t = text.lower()
    if any(_contains_word(t, kw) for kw in EPOCH_1_KEYWORDS):
        return "EPOCH_1"
    if any(_contains_word(t, kw) for kw in EPOCH_2_KEYWORDS):
        return "EPOCH_2"
    if any(_contains_word(t, kw) for kw in EPOCH_3_KEYWORDS):
        return "EPOCH_3"
    return "EPOCH_3"  # по умолчанию — интернет-ирония, как у 💀


_EPOCH_INTERPRETATION = {
    "EPOCH_1": "literal_hazard_warning",
    "EPOCH_2": "gaming_death_indicator",
    "EPOCH_3": "irony_intensifier",
}


def _sentence_around(text: str, offset: int) -> str:
    """Возвращает предложение, содержащее знак на позиции offset.
    Границы предложения: . ! ? ; и перевод строки. Риск-паттерны
    (угроза/инструкция/ложный авторитет) засчитываются, только если
    триггер и знак — в ОДНОМ предложении (MATCHER_PATCH_03)."""
    boundaries = ".!?;\n"
    start = 0
    for i in range(offset - 1, -1, -1):
        if text[i] in boundaries:
            start = i + 1
            break
    end = len(text)
    for i in range(offset, len(text)):
        if text[i] in boundaries:
            end = i
            break
    return text[start:end]


def match(text: str, offset: int, metadata: dict = None):
    """Возвращает (safe_ids, risk_ids, active_epoch, interpretation).

    Фразы-угрозы проверяются ПЕРВЫМИ и замещают epoch-based
    интерпретацию (тот же принцип, что в skull_matcher.py: "я тебя
    отравлю ☠" не должна получить нейтральную literal_hazard_warning
    интерпретацию рядом с RISK_CASE_001 — угроза важнее)."""
    safe, risk = [], []
    metadata = metadata or {}
    # MATCHER_PATCH_03 (шлифовка после живого прогона): риск-паттерны
    # ищутся в предложении, содержащем знак, а не в окне фикс. радиуса.
    # Живой тест показал: радиус ±80 на коротком сообщении дотягивался
    # до слова из ДРУГОГО предложения ("Официально сообщаем: ... это ☠"
    # ложно давало RC2). Правило "один знак — одно предложение" точнее
    # и не зависит от длины сообщения. detect_epoch по-прежнему смотрит
    # весь текст (эпоха — свойство более широкого контекста).
    t = _sentence_around(text, offset).lower()

    # Приоритет проверок (MATCHER_PATCH_01): RC1 угроза → RC3 вредная
    # инструкция → RC2 ложный авторитет → SAFE по эпохам. Угроза и
    # инструкция вреда — HIGH (важнее эпохи); ложный авторитет — MEDIUM.
    if any(_contains_word(t, p) for p in _THREAT_PHRASES):
        risk.append("RISK_CASE_001")
        epoch = detect_epoch(text)
        interp = "threat_obfuscated_as_hazard_warning"
    elif (any(_contains_word(t, v) for v in _HARM_INSTRUCTION_VERBS)
          and any(_contains_word(t, s) for s in _HARM_SUBSTANCE_WORDS)):
        # RC3: императив + вещество = потенциально вредная инструкция.
        # Ироническая рамка ("лол", "будет весело") риск НЕ снижает —
        # по GUARD карточки неоднозначность эскалирует.
        risk.append("RISK_CASE_003")
        epoch = detect_epoch(text)
        interp = "medical_instruction_obfuscation"
    elif any(_contains_word(t, kw) for kw in _FALSE_AUTHORITY_KEYWORDS):
        # RC2: заявка на официальность/сертификацию рядом со знаком
        # опасности — имитация регуляторного авторитета (MEDIUM).
        risk.append("RISK_CASE_002")
        epoch = detect_epoch(text)
        interp = "false_hazard_authority"
    else:
        epoch = detect_epoch(text)
        interp = _EPOCH_INTERPRETATION[epoch]
        if epoch == "EPOCH_1":
            safe.append("SAFE_CASE_001")
        elif epoch == "EPOCH_2":
            safe.append("SAFE_CASE_002")
        elif epoch == "EPOCH_3":
            safe.append("SAFE_CASE_003")

    return safe, risk, epoch, interp

# MATCHER_PATCH_HISTORY:
#   MATCHER_PATCH_01 (2026-07-05): добавлены RC2 (ложный авторитет) и
#     RC3 (вредная инструкция), расширено покрытие RC1. Закрыл gate-fail
#     5/14 → локально 14/14.
#   MATCHER_PATCH_02 (2026-07-05): фиксы по CODE_PATCH_REVIEW (GPT-5.5
#     APPROVE_WITH_FIXES): (1) offset-окно ±80 для риск-паттернов вместо
#     сканирования всего текста (сужение ложных срабатываний); (2)
#     обновлён устаревший docstring (WORKING_DRAFT → WORKINGLY_CLOSED);
#     карточный ADV_C1 выровнен под структурное правило (императив+вещество).
#     FINDING_03 (default epoch EPOCH_3) оставлен как известное
#     ограничение: риск-кейсы его перекрывают, граница EPOCH_1/3 намеренно
#     открыта (Q1 карточки, non-blocking).
#   MATCHER_PATCH_03 (2026-07-05): шлифовка после живого прогона на
#     машине автора. Фикс offset-окна ±80 → окно ПРЕДЛОЖЕНИЯ: риск-
#     паттерн засчитывается только если триггер и знак в одном
#     предложении (границы . ! ? ; \n). Живой тест выявил, что радиус
#     ±80 на коротком сообщении дотягивался до слова из другого
#     предложения. Правило "один знак — одно предложение" точнее.
#   Отклонена галлюцинация Gemini-ревью: описанные им словари _PIRACY_WORDS/
#     _SATIRE_WORDS/_MEDICAL_WORDS в коде отсутствуют (проверено grep).
