#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
unicode_sources_update.py — обновление Unicode-источников для MSL/MIP.

НАЗНАЧЕНИЕ (узкое, по AUTHOR_DECISION 2026-07-07):
  Снять операционный долг ручного обновления справочников Unicode,
  об который споткнулись оба конвейера (невидимые + цифры).

ЧТО ДЕЛАЕТ:
  1. Качает три канонических файла Unicode.
  2. Кладёт в sources/<UNICODE_VERSION>/ (version pinning).
  3. Сравнивает с текущей зафиксированной версией — показывает diff.
  4. Готовит новое рядом со старым. НЕ применяет автоматически.

ЧЕГО НЕ ДЕЛАЕТ (честная граница):
  - НЕ присваивает знакам risk. Только тянет справочники.
  - НЕ решает, принять ли новую версию — это AUTHOR_DECISION.
  - НЕ валидирует критерий шума на корпусе (это отдельная, ручная
    задача — скрипт снимает механику, не смысловую проверку).
  - НЕ санитайзер и не анализатор. Это вспомогательный tooling.

ДИСЦИПЛИНА:
  flag-only для источников: показывает ЧТО изменилось, решение —
  за автором (VERIFY_BEFORE_TRUST применён к самим справочникам).

ЗАПУСК:
  py unicode_sources_update.py            — проверить и показать diff
  py unicode_sources_update.py --apply    — зафиксировать как current
  py unicode_sources_update.py --only dcp — только DerivedCoreProperties
"""

import sys
import os
import re
import json
import hashlib
import urllib.request
from datetime import datetime, timezone

# ── Источники: первоисточник unicode.org, затем офиц. зеркало на GitHub ──
# Оба канонические (второй — репозиторий Unicode Consortium).
SOURCES = {
    "dcp": {
        "name": "DerivedCoreProperties.txt",
        "purpose": "Default_Ignorable и др. свойства (невидимые знаки)",
        "urls": [
            "https://www.unicode.org/Public/UCD/latest/ucd/DerivedCoreProperties.txt",
            "https://raw.githubusercontent.com/unicode-org/unicodetools/main/unicodetools/data/ucd/dev/DerivedCoreProperties.txt",
        ],
    },
    "udata": {
        "name": "UnicodeData.txt",
        "purpose": "категория/bidi/имя каждого кодпоинта (паспорт знака)",
        "urls": [
            "https://www.unicode.org/Public/UCD/latest/ucd/UnicodeData.txt",
            "https://raw.githubusercontent.com/unicode-org/unicodetools/main/unicodetools/data/ucd/dev/UnicodeData.txt",
        ],
    },
    "confusables": {
        "name": "confusables.txt",
        "purpose": "UTS#39 skeleton — гомоглифы (похожие знаки)",
        "urls": [
            "https://www.unicode.org/Public/security/latest/confusables.txt",
            "https://raw.githubusercontent.com/unicode-org/unicodetools/main/unicodetools/data/security/dev/confusables.txt",
        ],
    },
}

ROOT = os.path.dirname(os.path.abspath(__file__))
SOURCES_DIR = os.path.join(ROOT, "sources")
CURRENT_PTR = os.path.join(SOURCES_DIR, "CURRENT_VERSION.json")

UA = "Mozilla/5.0 (MSL-MIP unicode_sources_update; +local tooling)"


def _fetch(urls):
    """Пробует адреса по порядку. Возвращает (text, url, idx).
    idx=0 — первоисточник (unicode.org, стабильный релиз);
    idx>0 — запасной адрес (напр. github-зеркало /dev/, где может
    лежать ЧЕРНОВИК следующей версии, а не стабильный релиз)."""
    last = None
    for idx, u in enumerate(urls):
        try:
            req = urllib.request.Request(u, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                raw = r.read()
            return raw.decode("utf-8", errors="replace"), u, idx
        except Exception as e:
            last = f"{type(e).__name__}: {str(e)[:80]}"
            continue
    raise RuntimeError(f"все адреса недоступны, последняя ошибка: {last}")


def _sha(text):
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()[:16]


def _parse_version(dcp_text):
    """Вытаскивает версию Unicode из шапки файла (# DerivedCoreProperties-16.0.0.txt)."""
    m = re.search(r"-(\d+\.\d+\.\d+)\.txt", dcp_text[:500])
    if m:
        return m.group(1)
    m = re.search(r"Version:?\s*(\d+\.\d+\.\d+)", dcp_text[:1000])
    return m.group(1) if m else "UNKNOWN"


def _load_current():
    if os.path.exists(CURRENT_PTR):
        with open(CURRENT_PTR, encoding="utf-8") as f:
            return json.load(f)
    return None


def _di_codepoints(dcp_text):
    """Множество кодпоинтов с Default_Ignorable_Code_Point — ядро невидимого guard."""
    di = set()
    for line in dcp_text.splitlines():
        line = line.split("#", 1)[0].strip()
        if not line or "Default_Ignorable_Code_Point" not in line:
            continue
        rng = line.split(";", 1)[0].strip()
        if ".." in rng:
            a, b = rng.split("..")
            di.update(range(int(a, 16), int(b, 16) + 1))
        else:
            di.add(int(rng, 16))
    return di


def main():
    args = set(sys.argv[1:])
    apply = "--apply" in args
    only = None
    for a in list(args):
        if a == "--only":
            # следующий токен
            idx = sys.argv.index("--only")
            if idx + 1 < len(sys.argv):
                only = sys.argv[idx + 1]

    keys = [only] if only in SOURCES else list(SOURCES.keys())

    print("=" * 60)
    print("UNICODE SOURCES UPDATE — MSL/MIP tooling")
    print("режим:", "APPLY (зафиксировать)" if apply else "CHECK (только diff)")
    print("=" * 60)

    os.makedirs(SOURCES_DIR, exist_ok=True)
    current = _load_current()
    cur_ver = current.get("unicode_version") if current else None
    if cur_ver:
        print(f"текущая зафиксированная версия: {cur_ver}")
    else:
        print("текущая версия: НЕТ (первая загрузка)")

    fetched = {}
    new_version = None
    fallback_used = False
    for k in keys:
        src = SOURCES[k]
        print(f"\n── {src['name']} ({src['purpose']}) ──")
        try:
            text, used, idx = _fetch(src["urls"])
        except Exception as e:
            print(f"  ОШИБКА: {e}")
            continue
        sha = _sha(text)
        host = used.split('/')[2]
        print(f"  скачано: {len(text):,} симв | sha {sha} | via {host}")
        if idx > 0:
            fallback_used = True
            print(f"  ⚠️ ВНИМАНИЕ: первоисточник недоступен, взято с ЗАПАСНОГО")
            print(f"     адреса ({host}). Это может быть ветка разработки")
            print(f"     (/dev/) со ЧЕРНОВИКОМ следующей версии, а НЕ")
            print(f"     стабильным релизом. Версию перепроверь вручную.")
        fetched[k] = {"text": text, "sha": sha, "name": src["name"],
                      "source_url": used, "is_fallback": idx > 0}
        if k == "dcp":
            new_version = _parse_version(text)

    if not fetched:
        print("\nничего не скачано. проверь сеть.")
        return 1

    if new_version:
        print(f"\nверсия Unicode из скачанного DerivedCoreProperties: {new_version}")

    # ── DIFF против текущей ──
    print("\n" + "=" * 60)
    print("СРАВНЕНИЕ С ТЕКУЩЕЙ")
    print("=" * 60)
    changed = False
    if current is None:
        print("baseline отсутствует — всё новое (первая фиксация).")
        changed = True
    else:
        old_sha = current.get("files", {})
        for k, info in fetched.items():
            prev = old_sha.get(info["name"], {}).get("sha")
            if prev != info["sha"]:
                changed = True
                print(f"  ИЗМЕНИЛОСЬ: {info['name']}  {prev} -> {info['sha']}")
            else:
                print(f"  без изменений: {info['name']}")
        if new_version and cur_ver and new_version != cur_ver:
            print(f"  ВЕРСИЯ Unicode: {cur_ver} -> {new_version}")

    # содержательный diff для DI (что важно для невидимого guard)
    if "dcp" in fetched:
        new_di = _di_codepoints(fetched["dcp"]["text"])
        print(f"\n  Default_Ignorable кодпоинтов сейчас: {len(new_di)}")
        if current and current.get("di_count"):
            delta = len(new_di) - current["di_count"]
            if delta:
                print(f"  ИЗМЕНЕНИЕ числа DI-кодпоинтов: {delta:+d} "
                      f"(было {current['di_count']})")
                print("  ⚠️ критерий шума невидимого guard мог измениться — "
                      "нужна ручная валидация на корпусе")

    # ── APPLY или остановка ──
    if not changed:
        print("\nВСЁ АКТУАЛЬНО. обновление не требуется.")
        return 0

    if not apply:
        print("\n" + "=" * 60)
        print("НАЙДЕНЫ ИЗМЕНЕНИЯ. НИЧЕГО НЕ ЗАФИКСИРОВАНО.")
        print("Скрипт flag-only: решение принять — за автором.")
        print("Чтобы зафиксировать: py unicode_sources_update.py --apply")
        print("=" * 60)
        return 0

    # ЗАЩИТА: не фиксировать молча версию с ЗАПАСНОГО адреса.
    # Запасной может быть /dev/ веткой с черновиком — это НЕ стабильный
    # релиз. Требуем явного согласия автора (VERIFY_BEFORE_TRUST).
    if fallback_used and "--allow-fallback" not in args:
        print("\n" + "=" * 60)
        print("ФИКСАЦИЯ ОСТАНОВЛЕНА: часть файлов взята с ЗАПАСНОГО адреса.")
        print("Это может быть ветка разработки (черновик след. версии),")
        print("а не стабильный релиз Unicode. Молча фиксировать нельзя.")
        print("Если осознанно принимаешь запасной источник:")
        print("  py unicode_sources_update.py --apply --allow-fallback")
        print("=" * 60)
        return 2

    # APPLY: сохранить в sources/<version>/ и обновить указатель
    ver = new_version or datetime.now(timezone.utc).strftime("snapshot-%Y%m%d")
    vdir = os.path.join(SOURCES_DIR, ver)
    os.makedirs(vdir, exist_ok=True)
    manifest = {
        "unicode_version": ver,
        "fixed_at_utc": datetime.now(timezone.utc).isoformat(),
        "fetched_from_fallback": fallback_used,
        "di_count": len(_di_codepoints(fetched["dcp"]["text"])) if "dcp" in fetched else None,
        "files": {},
    }
    for k, info in fetched.items():
        path = os.path.join(vdir, info["name"])
        with open(path, "w", encoding="utf-8") as f:
            f.write(info["text"])
        manifest["files"][info["name"]] = {
            "sha": info["sha"],
            "path": os.path.relpath(path, ROOT),
            "source_url": info.get("source_url"),
            "is_fallback": info.get("is_fallback", False),
        }
        print(f"  сохранено: {os.path.relpath(path, ROOT)}")
    with open(CURRENT_PTR, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"\nЗАФИКСИРОВАНО как current: версия {ver}")
    if fallback_used:
        print("⚠️ зафиксировано с ЗАПАСНОГО источника (см. манифест)")
    print(f"указатель: {os.path.relpath(CURRENT_PTR, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
