"""
Матчер для SKULL (U+1F480, ZONE_3).

Ключевые слова для detect_epoch взяты из реальных полей FUNCTION
карточки (EPOCH_1: "маркер смерти, яда, опасности, Хэллоуина";
EPOCH_2: "я устал/я мёртв внутри/переутомление/поражение";
EPOCH_3: замена LOL/LMAO/ROFL — истерический смех/абсурдистский
юмор) — НЕ изобретённые отдельно категории (см. урок предыдущего
runtime, который придумал отдельные EPOCH_HALLOWEEN/EPOCH_GAMING,
не существующие в реальной карточке: Halloween — это часть FUNCTION
EPOCH_1, не отдельная эпоха).

ЧЕСТНО ЧАСТИЧНО МЕТАДАННЫЕ-ЗАВИСИМО: RISK_CASE_003
(GENERATIONAL_MISINTERPRETATION), RISK_CASE_006 (MEDICAL_MISREAD),
RISK_CASE_008 (CROSS_PLATFORM_EPOCH_MISMATCH) принципиально требуют
INPUT_METADATA (SENDER_COHORT/DOMAIN/PLATFORM) — это не текстовый
паттерн, это явно предусмотрено самой архитектурой MODULE_TEMPLATE
(раздел INPUT_METADATA). Без метаданных эти кейсы не детектируются —
это не пробел реализации, а честное отражение того, что искать в
тексте то, чего там нет, было бы тем же классом ошибки, что уже
ловили раньше.
RISK_CASE_001 (ALGORITHMIC_FALSE_POSITIVE_BAN), RISK_CASE_005
(SECOND_HAND_EMBARRASSMENT_DRIFT) — не реализованы: первый описывает
поведение ВНЕШНЕЙ системы модерации (мета-уровень, не свойство
текста), второй — размытая культурная тенденция без чёткого сигнала.
RISK_CASE_007 (EMOJI_SEQUENCE_INJECTION) — относится к SEQUENCE_MODULE
(несколько черепов подряд), не к одиночному знаку, обрабатывается
sequence_engine.py, не здесь.
"""

import re


def _contains_word(text_lower: str, phrase: str) -> bool:
    """Поиск ЦЕЛОГО слова/фразы по границам слов, не подстроки.
    ИСПРАВЛЕНО по итогам код-ревью (Gemini, 2026-06-28): простой
    `phrase in text` ловил 'kill' внутри 'skill', 'die' внутри
    'diet' — ложные EPOCH_1 срабатывания на безобидных словах."""
    pattern = r"\b" + re.escape(phrase) + r"\b"
    return re.search(pattern, text_lower) is not None


EPOCH_1_KEYWORDS = (
    "смерть", "смерти", "умер", "умереть", "убить", "убийство",
    "опасность", "опасно", "гибель", "яд", "ядовито", "хэллоуин",
    "halloween", "death", "dead", "die", "died", "kill", "killed",
    "poison", "toxic", "danger", "dangerous",
)

EPOCH_2_KEYWORDS = (
    "устал", "устала", "выгорел", "не могу", "сдался", "поражение",
    "проиграл", "tired", "exhausted", "burnout", "defeat", "defeated",
    "give up", "failed", "failure",
)

EPOCH_3_KEYWORDS = (
    "lol", "lmao", "rofl", "хаха", "ахах", "смешно", "ржака", "мем",
    "funny", "hilarious", "laugh", "joke", "cringe", "lit", "based",
)

# RISK_CASE_002: REAL_THREAT_OBFUSCATION — явная угрозная фраза рядом
_THREAT_PHRASES = (
    "найду тебя", "i will find you", "убью", "kill you", "i'll kill",
)

# RISK_CASE_004: CANCEL_CULTURE_OSTRACISM — фраза социального "вычёркивания"
_CANCEL_PHRASES = (
    "мёртв для нас", "dead to us", "he is dead to us",
)


def detect_epoch(text: str) -> str:
    """ACTIVE_EPOCH (GLOBAL) — доминирует EPOCH_3, но реактивируется
    EPOCH_1/EPOCH_2 при явном текстовом сигнале (DORMANT_EPOCHS
    reactivation, см. карточку). Использует поиск по границам слов
    (см. _contains_word) — substring-поиск ловил 'kill' в 'skill'."""
    t = text.lower()
    if any(_contains_word(t, kw) for kw in EPOCH_1_KEYWORDS):
        return "EPOCH_1"
    if any(_contains_word(t, kw) for kw in EPOCH_2_KEYWORDS):
        return "EPOCH_2"
    if any(_contains_word(t, kw) for kw in EPOCH_3_KEYWORDS):
        return "EPOCH_3"
    return "EPOCH_3"  # ACTIVE_EPOCH по умолчанию (GLOBAL, доминирует у Gen Z)


_EPOCH_INTERPRETATION = {
    "EPOCH_1": "literal_death",
    "EPOCH_2": "ironic_exhaustion",
    "EPOCH_3": "humor_marker",
}


_HALLOWEEN_KEYWORDS = ("halloween", "хэллоуин", "🎃")
_MEDICAL_KEYWORDS = ("анатоми", "медицин", "лекция", "слайде")


def _safe_case_for_epoch(text_lower: str, epoch: str) -> list:
    """ИСПРАВЛЕНО по итогам код-ревью (2026-06-28, находка независимого
    анализа карточки): прежний код слепо назначал SAFE_CASE_003 любому
    не-EPOCH_3 случаю. По реальной карточке SAFE_CASE_003 —
    ИМЕННО Halloween (holiday greetings, seasonal decoration), не
    "усталость" и не "смерть в целом". Теперь сопоставление точное:
      SAFE_CASE_001 = EPOCH_3 humor (Gen Z social media)
      SAFE_CASE_002 = EPOCH_2 exhaustion (student messaging)
      SAFE_CASE_003 = явный Halloween-контекст (любая эпоха)
      SAFE_CASE_006 = явный медицинский/академический контекст
    Если EPOCH_1 без Halloween/медицинского контекста — честно
    оставляем без SAFE_CASE (нет точного соответствия в карточке для
    обобщённого "смерть/опасность без уточнения контекста"), не
    подменяем приблизительной меткой."""
    if any(kw in text_lower for kw in _HALLOWEEN_KEYWORDS):
        return ["SAFE_CASE_003"]
    if any(kw in text_lower for kw in _MEDICAL_KEYWORDS):
        return ["SAFE_CASE_006"]
    if epoch == "EPOCH_3":
        return ["SAFE_CASE_001"]
    if epoch == "EPOCH_2":
        return ["SAFE_CASE_002"]
    return []


def match(text: str, offset: int, metadata: dict = None):
    """Возвращает (safe_ids, risk_ids, active_epoch, interpretation).

    ИСПРАВЛЕНО по итогам код-ревью (CONVEYOR_RUN_PACKET_MSL_MIP_CODE_
    SINGLE_SIGN_v0_1, 2026-06-28): "He is dead to us 💀" раньше давал
    interpretation="literal_death" ОДНОВРЕМЕННО с risk=RISK_CASE_004
    (CANCEL_CULTURE_OSTRACISM) — большинство ревьюеров (Kimi, Grok,
    GPT-5.5, Qwen) сочли это реальным конфликтом меток, не просто
    "наложением сигналов" (минority: Gemini/Copilot сочли это
    приемлемой синергией). Принято решение большинства: если
    сработала фраза-риск (cancel/threat), её интерпретация
    ЗАМЕЩАЕТ epoch-based интерпретацию, не сосуществует с ней —
    downstream-потребитель INTERPRETATION не должен получать
    "literal_death" для текста, который на деле про социальное
    вычёркивание, а не буквальную смерть."""
    safe, risk = [], []
    metadata = metadata or {}
    t = text.lower()

    # Фразы-риски проверяются ПЕРВЫМИ — они переопределяют epoch-based
    # интерпретацию, если сработали (см. docstring)
    if any(_contains_word(t, p) for p in _THREAT_PHRASES):
        risk.append("RISK_CASE_002")
        epoch = detect_epoch(text)  # эпоха всё равно вычисляется для аудита
        interp = "threat_obfuscated_as_humor"
    elif any(_contains_word(t, p) for p in _CANCEL_PHRASES):
        risk.append("RISK_CASE_004")
        epoch = detect_epoch(text)
        interp = "social_ostracism_marker"
    else:
        epoch = detect_epoch(text)
        interp = _EPOCH_INTERPRETATION[epoch]
        safe.extend(_safe_case_for_epoch(t, epoch))

    # Метаданные-зависимые кейсы — детектируются ТОЛЬКО если метаданные
    # реально переданы (не угадываются из текста)
    sender_cohort = metadata.get("SENDER_COHORT")
    if sender_cohort in ("Boomer", "Millennial") and epoch == "EPOCH_3":
        risk.append("RISK_CASE_003")  # GENERATIONAL_MISINTERPRETATION

    domain = metadata.get("DOMAIN")
    if domain == "medical":
        risk.append("RISK_CASE_006")  # MEDICAL_MISREAD

    platform_history = metadata.get("PLATFORM_ORIGIN")
    platform_current = metadata.get("PLATFORM")
    if platform_history and platform_current and platform_history != platform_current:
        risk.append("RISK_CASE_008")  # CROSS_PLATFORM_EPOCH_MISMATCH

    return safe, risk, epoch, interp
