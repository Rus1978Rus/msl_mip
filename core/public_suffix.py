"""
public_suffix.py — трёхуровневая защита для двух списков:
  1. СОСТАВНЫЕ доменные окончания (Public Suffix List, только записи
     с точкой — "co.uk", "com.au", "gov.scot" и т.п.).
  2. ОДИНОЧНЫЕ TLD (реестр IANA, "com", "shop", "xyz" и т.п.).

Оба нужны для корректной детекции domain mimicry в dot_matcher.py:
  - составные — чтобы gov.scot/com.au не считались фишингом
  - одиночные — чтобы paypal.com.verify.shop был пойман как фишинг

УРОВНИ ЗАЩИТЫ (в порядке убывания свежести):
  1. Канонический источник: https://publicsuffix.org/list/public_suffix_list.dat
     Сам файл явно просит тянуть ТОЛЬКО с этого адреса, не с зеркал
     ("Please pull this list from, and only from ..."). Поэтому при
     недоступности сайта мы НЕ ищем альтернативные URL — переходим
     на уровень 2.
  2. Локальный кэш — результат прошлой удачной загрузки уровня 1,
     сохранённый на диск с датой. Переживает временную
     недоступность сайта ИЛИ его полный переезд/исчезновение —
     система просто "застывает" на последней удачной версии.
  3. Встроенный минимальный список — на случай первого запуска без
     интернета вообще (нет ни сети, ни кэша). НЕ претендует на
     полноту — это практичное ядро самых распространённых составных
     окончаний, вручную выбранное из реального списка (не
     придуманное), без редких региональных записей вроде японских
     муниципалитетов.

ЧЕСТНОСТЬ: вызывающий код ДОЛЖЕН получать явный сигнал, какой
уровень защиты сработал — молчаливая деградация до кэша/минимума
недопустима (та же дисциплина, что и WORKING_DRAFT-предупреждения).
"""

from __future__ import annotations

import os
import re
import urllib.request
import urllib.error
from datetime import datetime, timezone

CANONICAL_URL = "https://publicsuffix.org/list/public_suffix_list.dat"
FETCH_TIMEOUT_SECONDS = 3

_CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "cache")
_CACHE_FILE = os.path.join(_CACHE_DIR, "public_suffix_compound_cache.txt")

# ИСПРАВЛЕНО (найдено по итогам код-ревью MINOR01_FIX, 2026-06-29,
# GPT-5.5): "одиночные TLD уже покрыты отдельным списком в dot_
# matcher.py" — оказалось НЕПРАВДОЙ в практическом смысле: тот
# список (_TLDS) был крошечным (20 записей), вручную составленным,
# и НЕ содержал множество реально активных TLD (.shop, .xyz, .site,
# .online, .top и сотни других). Из-за этого domain_mimicry_risk
# (который теперь зависит от is_domain_like) давал false negative на
# реальных фишинг-паттернах вроде "paypal.com.verify.shop". Решение —
# тот же трёхуровневый принцип, но для одиночных TLD, источник —
# официальный реестр IANA (https://data.iana.org/TLD/tlds-alpha-by-
# domain.txt), не менее авторитетный источник, чем сам Public Suffix
# List (PSL частично основан на этом же реестре).
IANA_TLD_URL = "https://data.iana.org/TLD/tlds-alpha-by-domain.txt"
_TLD_CACHE_FILE = os.path.join(_CACHE_DIR, "iana_single_tld_cache.txt")

# Уровень 3: встроенный минимум. Каждая запись реально существует в
# Public Suffix List (проверено прямой загрузкой канонического файла
# 2026-06-29) — это не догадки, а сознательно суженное подмножество:
# самые распространённые составные окончания без редких региональных
# записей (японские муниципалитеты, итальянские провинции и т.п.).
EMBEDDED_FALLBACK = frozenset({
    # Великобритания
    "co.uk", "org.uk", "gov.uk", "ac.uk", "ltd.uk", "plc.uk", "sch.uk", "net.uk", "me.uk",
    # Австралия
    "com.au", "net.au", "org.au", "edu.au", "gov.au", "asn.au", "id.au",
    # Бразилия
    "com.br", "net.br", "org.br", "gov.br", "edu.br",
    # Китай
    "com.cn", "net.cn", "org.cn", "gov.cn", "edu.cn", "ac.cn",
    # Мексика
    "com.mx", "gob.mx", "edu.mx", "net.mx", "org.mx",
    # Новая Зеландия
    "co.nz", "net.nz", "org.nz", "govt.nz",
    # Индия
    "co.in", "net.in", "org.in", "gov.in", "edu.in", "ac.in",
    # Турция
    "com.tr", "gov.tr", "edu.tr",
    # Япония (только организационные типы, без географии)
    "co.jp", "or.jp", "ne.jp", "ac.jp", "go.jp", "gr.jp", "ed.jp", "lg.jp", "ad.jp",
    # Шотландия/Уэльс — найдено в код-ревью как реальный контрпример
    "gov.scot", "gov.wales",
    # Сингапур
    "com.sg", "gov.sg", "edu.sg", "net.sg", "org.sg",
    # ЮАР
    "co.za", "org.za", "gov.za", "net.za",
    # Гонконг
    "com.hk", "net.hk", "org.hk", "edu.hk", "gov.hk",
    # Южная Корея
    "co.kr", "or.kr", "go.kr", "ac.kr", "ne.kr",
    # Аргентина
    "com.ar", "gob.ar", "gov.ar", "net.ar", "org.ar",
    # Колумбия
    "com.co", "edu.co", "gov.co", "net.co", "org.co",
    # Украина
    "com.ua", "gov.ua", "edu.ua", "net.ua", "org.ua",
    # Польша
    "com.pl", "gov.pl", "edu.pl", "net.pl", "org.pl",
    # Индонезия
    "co.id", "go.id", "or.id", "ac.id", "web.id",
    # Вьетнам
    "com.vn", "gov.vn", "edu.vn", "net.vn", "org.vn",
    # Филиппины
    "com.ph", "gov.ph", "edu.ph", "net.ph", "org.ph",
    # Малайзия
    "com.my", "gov.my", "edu.my", "net.my", "org.my",
    # Таиланд
    "co.th", "go.th", "ac.th", "net.th", "org.th",
    # Израиль
    "co.il", "gov.il", "ac.il", "net.il", "org.il",
    # Ирландия
    "gov.ie",
})

# Встроенный минимум ОДИНОЧНЫХ TLD (уровень 3 для IANA root zone).
# Каждая запись реально существует в актуальном реестре IANA
# (проверено прямым поиском, 2026-06-29). Это НЕ полный список (в
# реестре ~1437 TLD) — практичное ядро из gTLD, ccTLD и часто
# злоупотребляемых "свежих" зон (.shop/.xyz/.site/.online/.top и
# т.п., которые особенно релевантны для детекции фишинга, потому что
# дешёвые и нерегулируемые домены чаще используются для подделок).
EMBEDDED_TLD_FALLBACK = frozenset({
    # исходный ручной список (сохранён для совместимости)
    "com", "org", "net", "ru", "io", "dev", "app", "info", "biz",
    "co", "uk", "de", "fr", "ua", "by", "kz", "gov", "edu", "jp", "cn",
    # часто злоупотребляемые "свежие" gTLD в фишинге
    "shop", "xyz", "site", "online", "top", "club", "store", "tech",
    "win", "click", "link", "loan", "work", "live", "world", "space",
    "vip", "icu", "buzz", "rest", "fun", "pro", "name", "mobi",
    "tk", "ml", "ga", "cf", "gq",
    # крупные ccTLD/gTLD, не покрытые исходным списком
    "us", "ca", "au", "nz", "in", "br", "mx", "es", "it", "nl", "se",
    "no", "fi", "dk", "pl", "ch", "at", "be", "pt", "gr", "cz", "hu",
    "ro", "bg", "tr", "il", "sa", "ae", "eg", "za", "ng", "ke", "gh",
    "th", "vn", "id", "ph", "my", "sg", "hk", "tw", "kr", "pk", "bd",
    "lk", "np", "ir", "iq", "sy", "jo", "lb", "kw", "qa", "bh", "om",
    "ye", "ma", "tn", "ly", "sd", "et", "ug", "tz", "zm", "zw", "mw",
    "mz", "ao", "cm", "ci", "sn", "bf", "ne", "gn", "rw",
    "ec", "pe", "ve", "cl", "py", "uy", "bo", "do", "gt",
    "hn", "ni", "pa", "cr", "cu", "ht",
    # инфраструктурные/специальные
    "asia", "eu", "int", "arpa", "cat", "jobs", "mobi", "museum",
    "travel", "coop", "aero", "post",
    # отмечены ревьюерами как пропущенные, фишинг-релевантные
    "zip", "mov", "page", "email", "cloud", "website", "support",
    "services", "finance", "bank", "secure", "download", "review",
})


def _parse_single_tld_entries(raw_text: str) -> frozenset:
    """Извлекает одиночные TLD из IANA tlds-alpha-by-domain.txt.
    Формат: один TLD на строку (UPPERCASE), первая строка —
    комментарий "# Version ... Last Updated ..."."""
    result = set()
    for line in raw_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        result.add(line.lower())
    return frozenset(result)


def _fetch_single_tlds_from_iana() -> frozenset:
    req = urllib.request.Request(IANA_TLD_URL, headers={"User-Agent": "MSL-MIP/1.0"})
    with urllib.request.urlopen(req, timeout=FETCH_TIMEOUT_SECONDS) as resp:
        raw = resp.read().decode("utf-8", errors="replace")
    return _parse_single_tld_entries(raw)


def _save_tld_cache(entries: frozenset) -> None:
    os.makedirs(_CACHE_DIR, exist_ok=True)
    with open(_TLD_CACHE_FILE, "w", encoding="utf-8") as f:
        f.write(f"# CACHED: {datetime.now(timezone.utc).isoformat()}\n")
        for e in sorted(entries):
            f.write(e + "\n")


def _load_tld_cache():
    if not os.path.exists(_TLD_CACHE_FILE):
        return None, None
    with open(_TLD_CACHE_FILE, encoding="utf-8") as f:
        lines = f.readlines()
    if not lines or not lines[0].startswith("# CACHED:"):
        return None, None
    cached_at = lines[0].split("CACHED:", 1)[1].strip()
    entries = frozenset(
        line.strip().lower() for line in lines[1:]
        if line.strip() and not line.startswith("#")
    )
    return entries, cached_at


def load_single_tlds():
    """Аналог load_compound_suffixes(), но для одиночных TLD из IANA
    root zone. Та же дисциплина — три уровня, явный источник
    возвращается вызывающему коду."""
    try:
        entries = _fetch_single_tlds_from_iana()
        if entries:
            _save_tld_cache(entries)
            return entries, "LIVE_FETCH"
    except (urllib.error.URLError, TimeoutError, OSError, ValueError):
        pass

    cached_entries, cached_at = _load_tld_cache()
    if cached_entries:
        return cached_entries, f"CACHE_FROM_{cached_at}"

    return EMBEDDED_TLD_FALLBACK, "EMBEDDED_FALLBACK"


def _parse_compound_entries(raw_text: str) -> frozenset:
    """Извлекает из текста PSL только СОСТАВНЫЕ записи (с точкой),
    пропуская комментарии (//), пустые строки и wildcard-правила
    (*.xx / !exception — редкий случай, не обрабатываем отдельно,
    это известное, осознанное ограничение парсера)."""
    result = set()
    for line in raw_text.splitlines():
        line = line.strip()
        if not line or line.startswith("//") or "*" in line or line.startswith("!"):
            continue
        if "." in line:
            result.add(line.lower())
    return frozenset(result)


def _fetch_from_canonical_source() -> frozenset:
    """Уровень 1. Возвращает frozenset или бросает исключение, если
    скачать не удалось (вызывающий код переходит на уровень 2)."""
    req = urllib.request.Request(CANONICAL_URL, headers={"User-Agent": "MSL-MIP/1.0"})
    with urllib.request.urlopen(req, timeout=FETCH_TIMEOUT_SECONDS) as resp:
        raw = resp.read().decode("utf-8", errors="replace")
    return _parse_compound_entries(raw)


def _save_to_cache(entries: frozenset) -> None:
    os.makedirs(_CACHE_DIR, exist_ok=True)
    with open(_CACHE_FILE, "w", encoding="utf-8") as f:
        f.write(f"# CACHED: {datetime.now(timezone.utc).isoformat()}\n")
        for e in sorted(entries):
            f.write(e + "\n")


def _load_from_cache():
    """Уровень 2. Возвращает (frozenset, дата_кэша) или (None, None),
    если кэша нет."""
    if not os.path.exists(_CACHE_FILE):
        return None, None
    with open(_CACHE_FILE, encoding="utf-8") as f:
        lines = f.readlines()
    if not lines or not lines[0].startswith("# CACHED:"):
        return None, None
    cached_at = lines[0].split("CACHED:", 1)[1].strip()
    entries = frozenset(
        line.strip().lower() for line in lines[1:]
        if line.strip() and not line.startswith("#")
    )
    return entries, cached_at


def load_compound_suffixes():
    """Главная точка входа. Возвращает (frozenset, источник: str)
    где источник — один из 'LIVE_FETCH' / 'CACHE_FROM_<дата>' /
    'EMBEDDED_FALLBACK'. Вызывающий код ОБЯЗАН довести источник до
    пользователя, если это не LIVE_FETCH (см. докстринг модуля,
    раздел ЧЕСТНОСТЬ)."""
    try:
        entries = _fetch_from_canonical_source()
        if entries:
            _save_to_cache(entries)
            return entries, "LIVE_FETCH"
    except (urllib.error.URLError, TimeoutError, OSError, ValueError):
        pass

    cached_entries, cached_at = _load_from_cache()
    if cached_entries:
        return cached_entries, f"CACHE_FROM_{cached_at}"

    return EMBEDDED_FALLBACK, "EMBEDDED_FALLBACK"
