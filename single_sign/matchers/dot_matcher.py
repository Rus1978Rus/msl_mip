"""
Матчер для DOT (U+002E, ZONE_1).

ВАЖНАЯ ОГОВОРКА (не прятать): SAFE_CASES/RISK_CASES в карточке — это
текстовые иллюстрации для людей/ревьюеров (SIMULATION_GATE), не
формальные паттерны. Часть из них (RISK_CASE_001 FAKE_OFFICIAL_
NOTATION, RISK_CASE_003 VERSION_NUMBER_TRUST_INFLATION, RISK_CASE_004
ABBREVIATION_AUTHORITY_MIMICRY, RISK_CASE_005 ELLIPSIS_AS_FALSE_
CONTINUATION_SIGNAL) описывают РИТОРИЧЕСКИЕ паттерны — "текст создаёт
ложное ощущение Х" — это требует семантического понимания, не сводится
к детерминированной проверке символов. Этот матчер их НЕ детектирует
и не имитирует детекцию фейковыми правилами (см. урок dot_module.py —
ровно такая имитация дала false positive на "readme.txt.bak").
Реализованы только структурно проверяемые случаи: decimal/sentence/
abbreviation/file_extension/ellipsis (SAFE) и DOMAIN_LOOKALIKE/
NUMERIC_OBFUSCATION (RISK, оба имеют чёткий структурный сигнал).
"""

import re
from public_suffix import load_compound_suffixes, load_single_tlds

_GENERIC_TLDS = {"com", "org", "net", "info", "biz", "gov", "edu", "io", "app", "dev"}

_compound_suffixes_cache = None
_compound_suffixes_source = None
_single_tlds_cache = None
_single_tlds_source = None


def _get_compound_suffixes():
    """Ленивая загрузка составных доменных окончаний (один раз за
    жизнь процесса) — три уровня защиты, см. public_suffix.py."""
    global _compound_suffixes_cache, _compound_suffixes_source
    if _compound_suffixes_cache is None:
        _compound_suffixes_cache, _compound_suffixes_source = load_compound_suffixes()
    return _compound_suffixes_cache, _compound_suffixes_source


def _get_single_tlds():
    """Ленивая загрузка одиночных TLD (реестр IANA) — та же
    дисциплина трёх уровней. ИСПРАВЛЕНО (2026-06-29, GPT-5.5):
    раньше использовался крошечный ручной _TLDS (20 записей),
    из-за чего реальные TLD типа .shop/.xyz/.site давали false
    negative на domain_mimicry_risk."""
    global _single_tlds_cache, _single_tlds_source
    if _single_tlds_cache is None:
        _single_tlds_cache, _single_tlds_source = load_single_tlds()
    return _single_tlds_cache, _single_tlds_source


def get_compound_suffix_source() -> str:
    """Публичная точка для вызывающего рантайма (msl_mip_runtime.py):
    какой уровень защиты сработал для списка составных TLD —
    'LIVE_FETCH' / 'CACHE_FROM_<дата>' / 'EMBEDDED_FALLBACK'.
    Вызывать ОДИН РАЗ при старте программы, не на каждый матч."""
    _, source = _get_compound_suffixes()
    return source


def get_single_tld_source() -> str:
    """ИСПРАВЛЕНО (MAJOR, найдено GPT-5.5, 2026-06-29): раньше
    источник одиночных TLD (реестр IANA) загружался, но никак не
    раскрывался вызывающему коду — пользователь видел честное
    предупреждение про составные окончания, но не про одиночные
    TLD. Та же дисциплина: вызывать ОДИН РАЗ при старте."""
    _, source = _get_single_tlds()
    return source

# ИСПРАВЛЕНО (2026-06-29): _TLDS (крошечный ручной список из 20
# записей) убран — заменён на _get_single_tlds() (реестр IANA, три
# уровня защиты). См. public_suffix.py.
_EXTS = {
    "md", "txt", "py", "js", "json", "xml", "html", "css", "pdf",
    "doc", "docx", "xls", "png", "jpg", "jpeg", "gif", "zip", "tar",
    "exe", "dll",
}


def _word_at(text: str, start: int, direction: int) -> str:
    """Извлекает слово (алфанумерика) от start в направлении +1/-1."""
    out = []
    i = start
    while 0 <= i < len(text) and text[i].isalnum():
        out.append(text[i])
        i += direction
    if direction < 0:
        out.reverse()
    return "".join(out)


def _is_ipv4_like(s: str) -> bool:
    parts = s.split(".")
    if len(parts) != 4:
        return False
    return all(p.isdigit() and 0 <= int(p) <= 255 for p in parts)


_INTERPRETATION_NAMES = {
    "SAFE_CASE_001": "sentence_terminator",
    "SAFE_CASE_002": "decimal_separator",
    "SAFE_CASE_003": "abbreviation",
    "SAFE_CASE_004": "file_extension",
    "SAFE_CASE_004_DOMAIN": "domain_separator",
    "SAFE_CASE_006_ELLIPSIS": "ellipsis",
    "LEADING_DOT": "leading_dot_token",
}


def match(text: str, offset: int):
    """Возвращает (safe_ids, risk_ids, interpretation) для точки на
    позиции offset. ИСПРАВЛЕНО по итогам конвейерного код-ревью
    (CONVEYOR_RUN_PACKET_MSL_MIP_CODE_SINGLE_SIGN_v0_1, 2026-06-28):
    - interpretation теперь возвращается явно матчером (раньше
      движок брал её из card.context — приводило к утечке прозы
      карточки наружу как "машинного" значения, найдено GPT-5.5);
    - abbreviation больше не перехватывает любое однобуквенное слово
      перед точкой (ломало "x.py", "a.com" — найдено GPT-5.5/
      Copilot/Qwen) — теперь требует либо пробел+заглавная буква
      после точки ("A. Smith"), либо цепочку других однобуквенных
      слов ("к.т.н.");
    - добавлена leading-dot обработка (".env") — найдено Grok/
      Copilot/Qwen/GPT-5.5 как необработанный край."""
    safe, risk = [], []
    if offset < 0 or offset >= len(text) or text[offset] != ".":
        return safe, risk, "unknown"

    left = text[offset - 1] if offset > 0 else ""
    right = text[offset + 1] if offset + 1 < len(text) else ""

    # SAFE_CASE_002: decimal_separator
    if left.isdigit() and right.isdigit():
        safe.append("SAFE_CASE_002")
        chain_start = offset
        while chain_start > 0 and (text[chain_start - 1].isdigit() or text[chain_start - 1] == "."):
            chain_start -= 1
        chain_end = offset
        while chain_end < len(text) - 1 and (text[chain_end + 1].isdigit() or text[chain_end + 1] == "."):
            chain_end += 1
        chain = text[chain_start:chain_end + 1]
        if "." in chain and not _is_ipv4_like(chain) and all(
            p.isdigit() for p in chain.split(".")
        ) and len(chain.split(".")) >= 4:
            risk.append("RISK_CASE_006")
        elif len(chain.split(".")) >= 3:
            # SAFE_CASE_005: version_number — 3+ сегмента, не похоже
            # на обфускацию IP (найдено по итогам код-ревью: реальная
            # карточка содержит этот SAFE_CASE, ранее не помечался
            # отдельно от decimal_separator)
            safe.append("SAFE_CASE_005")
        return safe, risk, _INTERPRETATION_NAMES["SAFE_CASE_002"]

    # ИСПРАВЛЕНО: abbreviation — только если это РЕАЛЬНО похоже на
    # сокращение (пробел+заглавная после точки: "A. Smith"), ИЛИ
    # цепочка однобуквенных слов через точку ("к.т.н."). Простое
    # "одна буква перед точкой" больше не достаточно (ломало x.py,
    # a.com — INTERPRETATION получал bы 'abbreviation', хотя это
    # явно имя файла/домен).
    left_word = _word_at(text, offset - 1, -1)
    if len(left_word) == 1 and left_word.isalpha():
        right_word = _word_at(text, offset + 1, +1)
        space_then_upper = (
            offset + 2 < len(text) and text[offset + 1] == " " and text[offset + 2].isupper()
        )
        chain_abbreviation = len(right_word) == 1 and right_word.isalpha()
        if space_then_upper or chain_abbreviation:
            safe.append("SAFE_CASE_003")
            return safe, risk, _INTERPRETATION_NAMES["SAFE_CASE_003"]
        # иначе — однобуквенное слово, но не похоже на сокращение
        # (x.py, a.com) — падаем дальше, в обычную word.word логику

    # ellipsis
    if text[offset:offset + 3] == "..." or text[max(0, offset - 2):offset + 1] == "...":
        safe.append("SAFE_CASE_006_ELLIPSIS")
        return safe, risk, _INTERPRETATION_NAMES["SAFE_CASE_006_ELLIPSIS"]

    # sentence_terminator
    if (offset == len(text) - 1 or not right.isalnum()) and left.isalpha():
        safe.append("SAFE_CASE_001")
        return safe, risk, _INTERPRETATION_NAMES["SAFE_CASE_001"]

    # ИСПРАВЛЕНО: точка в начале текста (нет left-контекста вовсе) —
    # раньше давала молчаливый unknown, теперь явный случай
    if left == "" and right != "":
        safe.append("LEADING_DOT")
        return safe, risk, _INTERPRETATION_NAMES["LEADING_DOT"]

    if not (left.isalnum() and right.isalnum()):
        return safe, risk, "unknown"

    # ИСПРАВЛЕНО (найдено по итогам код-ревью, 2026-06-28): раньше
    # решение "1 точка vs 2+ точки" принималось по dot_count = text.
    # count(".") — ПО ВСЕМУ ТЕКСТУ. Из-за этого "example.com." (домен
    # + точка конца предложения ПОСЛЕ домена) ложно считался "доменом
    # с 2+ точками" и получал RISK_CASE_002/HIGH, хотя сам домен
    # содержит только одну точку — вторая принадлежит не относящемуся
    # к делу предложению дальше в тексте. Теперь считаем точки только
    # внутри НАЙДЕННОЙ локальной цепочки (содержащей offset).
    local_chain = None
    for m in re.finditer(r"[\w-]+(?:\.[\w-]+)+", text):
        if m.start() <= offset < m.end():
            local_chain = m.group(0)
            break
    right_word = _word_at(text, offset + 1, +1)

    if local_chain is None:
        # одиночная точка без расширяемой цепочки с обеих сторон —
        # на практике не должно происходить здесь (left/right уже
        # alnum), защитный fallback
        local_chain = _word_at(text, offset - 1, -1) + "." + right_word

    local_dot_count = local_chain.count(".")
    single_tlds, _ = _get_single_tlds()
    compound_suffixes, _ = _get_compound_suffixes()

    if local_dot_count == 1:
        # ИСПРАВЛЕНО (MINOR, найдено GPT-5.5, 2026-06-29): для
        # коротких цепочек вида "gov.scot" (всего одна точка) right_
        # word ("scot") сам по себе не входит ни в single_tlds, ни
        # это не помогает — нужно проверять ВСЮ цепочку целиком на
        # совпадение с известным составным окончанием.
        if right_word.lower() in single_tlds or local_chain.lower() in compound_suffixes:
            safe.append("SAFE_CASE_004_DOMAIN")
            return safe, risk, _INTERPRETATION_NAMES["SAFE_CASE_004_DOMAIN"]
        safe.append("SAFE_CASE_004")
        return safe, risk, _INTERPRETATION_NAMES["SAFE_CASE_004"]

    last_segment = local_chain.rsplit(".", 1)[-1].lower()
    is_domain_like = last_segment in single_tlds
    # ИСПРАВЛЕНО (MINOR_01, найдено GPT-5.5, 2026-06-29): составные
    # окончания (gov.scot, com.au) не входят в _TLDS как единый
    # сегмент, поэтому ранее давали верный NONE-риск, но неверную
    # метку file_extension вместо domain_separator. Проверяем
    # последние 2-3 сегмента на совпадение с реальным составным
    # окончанием.
    if not is_domain_like:
        segments_for_suffix_check = local_chain.split(".")
        for k in (2, 3):
            if len(segments_for_suffix_check) >= k:
                candidate_suffix = ".".join(segments_for_suffix_check[-k:]).lower()
                if candidate_suffix in compound_suffixes:
                    is_domain_like = True
                    break

    # ИСПРАВЛЕНО (найдено САМОСТОЯТЕЛЬНО при самопроверке перед
    # отправкой конвейерного пакета, 2026-06-29): domain_mimicry_risk
    # вычислялся БЕЗУСЛОВНО, независимо от is_domain_like. Из-за
    # этого "example.com.bak" (явно файл, не домен — последний
    # сегмент "bak" не TLD и не составной суффикс) всё равно получал
    # RISK_CASE_002, потому что "com" стоит не последним. Семантически
    # бессвязно: SAFE_CASE_004 (файл) + RISK_CASE_002 (имитация
    # ДОМЕНА) одновременно. Теперь проверка имитации выполняется
    # ТОЛЬКО внутри ветки "это похоже на домен" — если последний
    # сегмент не TLD и не составной суффикс, риск имитации домена
    # просто неприменим, какой бы generic-TLD ни был внутри цепочки.
    if is_domain_like:
        safe.append("SAFE_CASE_004_DOMAIN")
        segments = local_chain.split(".")
        domain_mimicry_risk = False
        for i, seg in enumerate(segments[:-1]):
            if seg.lower() in _GENERIC_TLDS:
                remaining = ".".join(segments[i:]).lower()
                if remaining not in compound_suffixes:
                    domain_mimicry_risk = True
                    break
        if domain_mimicry_risk:
            risk.append("RISK_CASE_002")
        return safe, risk, _INTERPRETATION_NAMES["SAFE_CASE_004_DOMAIN"]
    safe.append("SAFE_CASE_004")
    return safe, risk, _INTERPRETATION_NAMES["SAFE_CASE_004"]
