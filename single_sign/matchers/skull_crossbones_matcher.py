"""
Матчер для ☠ (U+2620, SKULL_AND_CROSSBONES).

Структура аналогична matchers/skull_matcher.py (тот же ZONE_3,
epoch-зависимая интерпретация). Тестовый знак — карточка помечена
WORKING_DRAFT, не прошла полный конвейер (см. SIGN_CORE_CARD).
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


def match(text: str, offset: int, metadata: dict = None):
    """Возвращает (safe_ids, risk_ids, active_epoch, interpretation).

    Фразы-угрозы проверяются ПЕРВЫМИ и замещают epoch-based
    интерпретацию (тот же принцип, что в skull_matcher.py: "я тебя
    отравлю ☠" не должна получить нейтральную literal_hazard_warning
    интерпретацию рядом с RISK_CASE_001 — угроза важнее)."""
    safe, risk = [], []
    metadata = metadata or {}
    t = text.lower()

    if any(_contains_word(t, p) for p in _THREAT_PHRASES):
        risk.append("RISK_CASE_001")
        epoch = detect_epoch(text)
        interp = "threat_obfuscated_as_hazard_warning"
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
