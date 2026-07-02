"""
Матчер для SOLIDUS (U+002F, ZONE_2).

CONTEXT_GATE: солидус не имеет единой активной эпохи — какой
SUBSTRATE активен, определяется контекстом (см. карточку:
ACTIVE_EPOCH_RESOLUTION.PRIMARY_ACTIVE_EPOCH = NONE_GLOBAL).

ЧЕСТНО НЕ РЕАЛИЗОВАНО (семантические, не структурные паттерны,
см. dot_matcher.py docstring для того же класса оговорки):
  RISK_CASE_005 STATUS_CHAIN_MIMICRY, RISK_CASE_006 ROLE_BINDING_
  MIMICRY, RISK_CASE_007 PHAGO_ENTITY_PATH_MIMICRY — требуют
  распознавания "похоже на известный бренд/организацию" или
  "похоже на цепочку статусов", это не структурный признак.
"""


import re


def _word_at(text: str, start: int, direction: int) -> str:
    out = []
    i = start
    allowed = lambda c: c.isalnum() or c in "-_"
    while 0 <= i < len(text) and allowed(text[i]):
        out.append(text[i])
        i += direction
    if direction < 0:
        out.reverse()
    return "".join(out)


_ADMIN_WORDS = {"admin", "root", "execute", "permission", "sudo", "superuser"}
_API_WORDS = {"api", "v1", "v2", "v3"}

# ИСПРАВЛЕНО по итогам код-ревью (CONVEYOR_RUN_PACKET_MSL_MIP_CODE_
# SINGLE_SIGN_v0_1, 2026-06-28, найдено ВСЕМИ 7 ревьюерами): домен-
# подобный сегмент перед солидусом ("trusted.com/verified") должен
# определяться явным regex-поиском по тексту ПЕРЕД offset, а не
# через _word_at (который останавливается на "." и поэтому никогда
# не видит точку — корень бага).
_DOMAIN_BEFORE_SLASH_RE = re.compile(r"[\w-]+\.[A-Za-z]{2,}$")

_INTERPRETATION_NAMES = {
    "SAFE_CASE_001": "path_or_choice_separator",
    "SAFE_CASE_002": "fraction_separator",
    "SAFE_CASE_003": "filesystem_path",
    "SAFE_CASE_004": "url_separator",
    "SAFE_CASE_004_AUTHORITY": "url_authority_separator",
    "SAFE_CASE_005": "date_separator",
}


def detect_substrate(text: str, offset: int) -> str:
    """CONTEXT_GATE: определяет активный субстрат для конкретного
    вхождения солидуса. Возвращает один из:
    MATH / FILESYSTEM / URL / URL_AUTHORITY / DATE / AMBIGUOUS."""

    left = text[offset - 1] if offset > 0 else ""
    right = text[offset + 1] if offset + 1 < len(text) else ""

    if left.isdigit() and right.isdigit():
        window_start = offset
        while window_start > 0 and (text[window_start - 1].isdigit() or text[window_start - 1] == "/"):
            window_start -= 1
        window_end = offset
        while window_end < len(text) - 1 and (text[window_end + 1].isdigit() or text[window_end + 1] == "/"):
            window_end += 1
        chain = text[window_start:window_end + 1]
        parts = chain.split("/")
        if len(parts) == 3 and len(parts[0]) == 4:
            return "DATE"
        return "MATH"

    if text[max(0, offset - 1):offset + 2] == "://" or "://" in text[max(0, offset - 8):offset + 8]:
        return "URL"

    # ИСПРАВЛЕНО (BUG_B, GPT-5.5, 2026-06-28): Windows-путь вида
    # "C:/Users" с ОДНИМ слешем не подхватывался ни одним правилом
    # FILESYSTEM (требовалось 2+ слеша или ведущий "./"/".."),
    # оставался AMBIGUOUS. Явный паттерн "<буква>:/" — диск Windows.
    if offset >= 2 and text[offset - 2].isalpha() and text[offset - 1] == ":":
        return "FILESYSTEM"

    # ИСПРАВЛЕНО: обратный слеш перед солидусом — сигнал escape-
    # последовательности (RISK_CASE_001), без этого ветка FILESYSTEM
    # никогда не достигалась бы для таких входов, и проверка
    # RISK_CASE_001 в match() была бы недостижимым кодом
    if offset > 0 and text[offset - 1] == "\\":
        return "FILESYSTEM"

    # ИСПРАВЛЕНО: домен-подобный сегмент непосредственно перед "/"
    # (без требования "://") — например "trusted.com/verified"
    if _DOMAIN_BEFORE_SLASH_RE.search(text[:offset]):
        return "URL_AUTHORITY"

    if left in "./" or text[max(0, offset - 2):offset] == "..":
        return "FILESYSTEM"
    if text.count("/") >= 2:
        return "FILESYSTEM"

    return "AMBIGUOUS"


def match(text: str, offset: int):
    safe, risk = [], []
    if offset < 0 or offset >= len(text) or text[offset] != "/":
        return safe, risk, "unknown"

    substrate = detect_substrate(text, offset)
    left_word = _word_at(text, offset - 1, -1)
    right_word = _word_at(text, offset + 1, +1)

    if substrate == "MATH":
        safe.append("SAFE_CASE_002")
        return safe, risk, _INTERPRETATION_NAMES["SAFE_CASE_002"]

    if substrate == "DATE":
        safe.append("SAFE_CASE_005")
        return safe, risk, _INTERPRETATION_NAMES["SAFE_CASE_005"]

    if substrate == "URL":
        safe.append("SAFE_CASE_004")
        if "." in left_word and "/" not in left_word:
            risk.append("RISK_CASE_002")
        return safe, risk, _INTERPRETATION_NAMES["SAFE_CASE_004"]

    if substrate == "URL_AUTHORITY":
        # ИСПРАВЛЕНО (AUTHOR_DECISION, 2026-06-29): ранее URL_AUTHORITY
        # безусловно добавлял RISK_CASE_002, что делало ЛЮБУЮ ссылку
        # с доменом источником QUEUE_FOR_REVIEW. Это архитектурно
        # неверно: DOT-слой уже оценивает качество домена (имитация,
        # поддомены и т.п.). Если DOT нашёл риск — финальный вердикт
        # уже будет повышен через DOT. Если не нашёл — домен чист, и
        # SOLIDUS не должен наказывать его повторно только за наличие
        # пути после. SOLIDUS фиксирует ФАКТ (это граница URL-пути),
        # но не добавляет риска самостоятельно.
        # Подтверждено прямым прогоном: paypal.com.security-check.ru
        # даёт HOLD_PENDING_REVIEW через DOT даже без этого риска.
        safe.append("SAFE_CASE_004")
        return safe, risk, _INTERPRETATION_NAMES["SAFE_CASE_004_AUTHORITY"]

    if substrate == "FILESYSTEM":
        safe.append("SAFE_CASE_003")

        # RISK_CASE_001: ESCAPE_SEQUENCE — солидус сразу после
        # обратного слеша (найдено по итогам код-ревью: реальная
        # карточка содержит этот RISK_CASE, ранее не реализован)
        if offset > 0 and text[offset - 1] == "\\":
            risk.append("RISK_CASE_001")

        if text[max(0, offset - 2):offset] == "..":
            risk.append("RISK_CASE_001")

        if left_word.lower() in _ADMIN_WORDS or right_word.lower() in _ADMIN_WORDS:
            risk.append("RISK_CASE_003")

        if left_word.lower() in _API_WORDS or right_word.lower() in _API_WORDS:
            risk.append("RISK_CASE_004")

        return safe, risk, _INTERPRETATION_NAMES["SAFE_CASE_003"]

    safe.append("SAFE_CASE_001")
    risk.append("RISK_CASE_008")
    return safe, risk, _INTERPRETATION_NAMES["SAFE_CASE_001"]
