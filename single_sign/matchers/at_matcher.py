# -*- coding: utf-8 -*-
"""
Матчер для знака @ (U+0040, COMMERCIAL AT). ZONE_2, класс PH.

Соответствует SIGN_CORE_CARD_AT_U0040_GEN3_v0_3_RU (WORKINGLY_CLOSED).
Возвращает 3-tuple (safe_ids, risk_ids, interpretation) — как
dot/solidus (структурный знак без культурных эпох).

ГЛАВНЫЙ ПРИНЦИП (из карточки): @ в подавляющем большинстве ЛЕГИТИМЕН
(email, mention, декоратор, ценник, федеративный handle). RISK ТОЛЬКО
в URL-userinfo-контексте. Default НЕ "@ = угроза" (CG3).

RISK-механика детерминирована ТОЛЬКО при наличии URL-схемы (PATCH_03,
факт-аудит Alibaba/Copilot по WHATWG + RFC 3986): в http(s)://...@host
хост = сегмент после ПОСЛЕДНЕГО @, всё до — userinfo. БЕЗ схемы строка
paypal.com@evil.ru не даёт host=evil.ru (WHATWG: protocol='paypal.com:',
host пустой) — поэтому без схемы это контекстная неоднозначность (Q1),
не автоматический RISK.

MATCHER_PATCH_HISTORY:
  создан 2026-07-06 под карточку @ (после конвейера 5/5 + 2 факт-аудита).
"""
from __future__ import annotations
import re

# URL-схема перед @ — маркер URL-контекста (RISK-детерминизм только тут)
_URL_SCHEME_RE = re.compile(r'(https?|ftp)://', re.IGNORECASE)
# mailto — email-контекст, @ легитимен (SAFE, не URL-userinfo)
_MAILTO_RE = re.compile(r'mailto:', re.IGNORECASE)

# домен с TLD (для распознавания бренда в userinfo-позиции)
_DOMAIN_RE = re.compile(r'[\w-]+\.[A-Za-z]{2,}')
# IP-адрес как хост (RC2)
_IP_RE = re.compile(r'\d{1,3}(?:\.\d{1,3}){3}')

# декоратор в коде: @ в начале строки/после отступа перед идентификатором
_DECORATOR_RE = re.compile(r'(^|\n)\s*@[A-Za-z_]\w*')

INTERPRETATION = {
    "SAFE_CASE_001": "email_separator",
    "SAFE_CASE_002": "social_mention",
    "SAFE_CASE_003": "code_decorator",
    "SAFE_CASE_004": "commercial_pricing",
    "SAFE_CASE_005": "mailto_email",
    "SAFE_CASE_006": "handle_list",
    "SAFE_CASE_007": "federated_handle",
    "RISK_CASE_001": "url_userinfo_spoofing",
    "RISK_CASE_002": "userinfo_brand_non_final",
    "RISK_CASE_003": "multiple_at_obfuscation",
    "RISK_CASE_004": "false_verified_account",
}


def _url_context_around(text: str, offset: int):
    """Извлекает URL-подобный токен, содержащий @ на позиции offset.
    Токен = непрерывная последовательность без пробелов вокруг offset."""
    start = offset
    while start > 0 and not text[start - 1].isspace():
        start -= 1
    end = offset
    while end < len(text) and not text[end].isspace():
        end += 1
    return text[start:end], start


def match(text: str, offset: int):
    """Возвращает (safe_ids, risk_ids, interpretation).
    @ на позиции offset. RISK только в URL-userinfo-контексте."""
    safe, risk = [], []

    # Проверка: по offset действительно @ (или fullwidth-эквивалент уже
    # нормализован до @ на входе рантайма — см. NORMALIZATION_NOTE)
    if offset < 0 or offset >= len(text) or text[offset] != "@":
        return [], [], None

    token, tok_start = _url_context_around(text, offset)
    tok_lower = token.lower()

    has_scheme = bool(_URL_SCHEME_RE.search(token))
    is_mailto = bool(_MAILTO_RE.search(token))

    # --- SAFE: mailto (email в mailto-схеме, не URL-userinfo) ---
    if is_mailto:
        safe.append("SAFE_CASE_005")
        return safe, risk, INTERPRETATION["SAFE_CASE_005"]

    # --- RISK-ветка: ТОЛЬКО при URL-схеме (PATCH_03 детерминизм) ---
    if has_scheme:
        # часть токена после схемы
        after_scheme = _URL_SCHEME_RE.sub("", token)
        at_count = after_scheme.count("@")
        # хост = после ПОСЛЕДНЕГО @ (WHATWG)
        last_at = after_scheme.rfind("@")
        userinfo = after_scheme[:last_at]
        host_part = after_scheme[last_at + 1:]

        # RC3: множественные @ в URL — обфускация
        if at_count >= 2:
            risk.append("RISK_CASE_003")
            return safe, risk, INTERPRETATION["RISK_CASE_003"]

        # бренд-домен в userinfo (до @) — сигнал имитации
        brand_in_userinfo = bool(_DOMAIN_RE.search(userinfo))
        host_is_ip = bool(_IP_RE.match(host_part))
        host_is_domain = bool(_DOMAIN_RE.match(host_part))

        if brand_in_userinfo and host_is_ip:
            # RC2: бренд в userinfo + IP-хост
            risk.append("RISK_CASE_002")
            return safe, risk, INTERPRETATION["RISK_CASE_002"]
        if brand_in_userinfo and host_is_domain:
            # RC1: базовый userinfo-spoofing (бренд.tld @ другой-домен.tld)
            risk.append("RISK_CASE_001")
            return safe, risk, INTERPRETATION["RISK_CASE_001"]
        # @ в URL, но userinfo без бренд-домена — легитимный userinfo
        # (напр. user@host) — не спуфинг
        safe.append("SAFE_CASE_001")
        return safe, risk, INTERPRETATION["SAFE_CASE_001"]

    # --- БЕЗ схемы: контекстная неоднозначность (Q1) → SAFE-ветвление ---
    # декоратор в коде
    if _DECORATOR_RE.search(text[max(0, offset - 40):offset + 40]):
        safe.append("SAFE_CASE_003")
        return safe, risk, INTERPRETATION["SAFE_CASE_003"]

    # федеративный handle @user@domain (SAFE_CASE_007): два @ БЕЗ схемы
    if token.count("@") >= 2 and _DOMAIN_RE.search(token):
        safe.append("SAFE_CASE_007")
        return safe, risk, INTERPRETATION["SAFE_CASE_007"]

    # email: слово@домен.tld без схемы, один @
    if token.count("@") == 1 and _DOMAIN_RE.search(token[token.find("@"):]):
        safe.append("SAFE_CASE_001")
        return safe, risk, INTERPRETATION["SAFE_CASE_001"]

    # ценник: @ рядом с цифрами/валютой ("10 шт @ 5$")
    around = text[max(0, offset - 10):offset + 10]
    if re.search(r'\d', around) and re.search(r'[$€£\d]', text[offset:offset + 10]):
        safe.append("SAFE_CASE_004")
        return safe, risk, INTERPRETATION["SAFE_CASE_004"]

    # mention: @ перед словом-handle
    if offset + 1 < len(text) and (text[offset + 1].isalnum() or text[offset + 1] == "_"):
        safe.append("SAFE_CASE_002")
        return safe, risk, INTERPRETATION["SAFE_CASE_002"]

    # дефолт: одиночный @ без контекста — DATA_ONLY, безопасно
    safe.append("SAFE_CASE_002")
    return safe, risk, INTERPRETATION["SAFE_CASE_002"]
