"""
Универсальный парсер для markdown-документов проекта MSL/MIP
(SIGN_CORE_CARD, и в перспективе MODULE_TEMPLATE/INTEGRATOR_TEMPLATE).

ПОДХОД: строим дерево по отступам (indentation tree), не пишем регулярки
под формат конкретной карточки. Карточки DOT/SOLIDUS/SKULL расходятся в
деталях (например, у SOLIDUS эпохи без поля NAME, у SKULL — с ним;
RISK иногда составной: "LOW / CONTEXT_DEPENDENT") — единый
структурный парсер устойчив к этим различиям, в отличие от
построчных регулярок под каждую карту.

ПРАВИЛО ПАРСИНГА:
  - строка вида "<отступ><KEY>: <значение>" — это узел KEY с этим
    значением (может быть пустым, если у узла есть дочерние узлы)
  - строка без такого паттерна — это ПРОДОЛЖЕНИЕ значения последнего
    открытого узла (перенос длинной строки на следующую строку с
    большим отступом), независимо от точного отступа продолжения
  - пустые строки игнорируются
  - KEY — последовательность ЗАГЛАВНЫХ латинских букв/цифр/'_',
    начинающаяся с буквы (так не путается с нумерованными
    заголовками типа "5. SEMANTIC_EPOCH_TRACKER" и преамбулой)
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional


_KEY_LINE_RE = re.compile(r"^([A-Z][A-Z0-9_]*)(?:\s*\([^)]*\))?:\s?(.*)$")


@dataclass
class Node:
    key: Optional[str]
    value: str = ""
    children: list = field(default_factory=list)

    def child(self, key: str) -> Optional["Node"]:
        """Первый дочерний узел с данным key, или None."""
        for c in self.children:
            if c.key == key:
                return c
        return None

    def children_with_prefix(self, prefix: str) -> list:
        """Все дочерние узлы, чей key начинается с prefix (например,
        все 'SAFE_CASE_001', 'SAFE_CASE_002', ... под SAFE_CASES)."""
        return [c for c in self.children if c.key and c.key.startswith(prefix)]

    def text(self) -> str:
        return self.value.strip()


def parse_indented_tree(raw_text: str) -> Node:
    """Строит дерево узлов по отступам. Возвращает корневой узел
    (key=None), дети которого — узлы верхнего уровня документа."""

    root = Node(key=None)
    stack: list = [(-1, root)]  # (indent, node)

    for raw_line in raw_text.splitlines():
        if not raw_line.strip():
            continue  # пустые строки не влияют на структуру

        stripped = raw_line.strip()

        # пропускаем чисто декоративные разделители "===...==="
        if re.fullmatch(r"=+", stripped):
            continue

        indent = len(raw_line) - len(raw_line.lstrip(" "))
        m = _KEY_LINE_RE.match(stripped)

        if m:
            key, value = m.group(1), m.group(2)
            # поднимаемся по стеку, пока вершина не имеет отступ < текущего
            while stack and stack[-1][0] >= indent:
                stack.pop()
            parent = stack[-1][1]
            node = Node(key=key, value=value)
            parent.children.append(node)
            stack.append((indent, node))
        else:
            # продолжение значения самого глубокого открытого узла,
            # независимо от точного отступа продолжения (см. docstring)
            if stack[-1][1] is not root:
                deepest = stack[-1][1]
                deepest.value = (deepest.value + " " + stripped).strip()
            # если stack[-1][1] is root — мусорная строка вне любого
            # узла (преамбула документа и т.п.), молча игнорируем

    return root


def find_section(root: Node, key: str) -> Optional[Node]:
    """Поиск узла верхнего уровня по key (например, 'SAFE_CASES')."""
    return root.child(key)
