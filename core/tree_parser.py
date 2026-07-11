"""
Universal parser for MSL/MIP project markdown documents
(SIGN_CORE_CARD, and later MODULE_TEMPLATE/INTEGRATOR_TEMPLATE).

APPROACH: build an indentation tree, no per-card regexes.
DOT/SOLIDUS/SKULL cards diverge in details (e.g. SOLIDUS epochs
lack the NAME field while SKULL has it; RISK is sometimes composite:
"LOW / CONTEXT_DEPENDENT") — a single structural parser is robust
to these differences, unlike per-card line regexes.


PARSING RULES:
  - a line "<indent><KEY>: <value>" is a KEY node with that value
    (may be empty when the node has children)
  - a line without that pattern is a CONTINUATION of the value of the
    last open node (a long value wrapped onto the next line with a
    larger indent), regardless of the exact continuation indent
  - empty lines are ignored
  - KEY is a sequence of UPPERCASE latin letters/digits/'_' starting
    with a letter (so it is not confused with numbered headers like
    "5. SEMANTIC_EPOCH_TRACKER" and the preamble)
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
        """First child node with the given key, or None."""
        for c in self.children:
            if c.key == key:
                return c
        return None

    def children_with_prefix(self, prefix: str) -> list:
        """All child nodes whose key starts with prefix (e.g. all
        'SAFE_CASE_001', 'SAFE_CASE_002', ... under SAFE_CASES)."""
        return [c for c in self.children if c.key and c.key.startswith(prefix)]

    def text(self) -> str:
        return self.value.strip()


def parse_indented_tree(raw_text: str) -> Node:
    """Builds the indentation node tree. Returns the root node
    (key=None) whose children are the document top-level nodes."""

    root = Node(key=None)
    stack: list = [(-1, root)]  # (indent, node)

    for raw_line in raw_text.splitlines():
        if not raw_line.strip():
            continue  # empty lines do not affect structure

        stripped = raw_line.strip()

        # skip purely decorative "===...===" separators
        if re.fullmatch(r"=+", stripped):
            continue

        indent = len(raw_line) - len(raw_line.lstrip(" "))
        m = _KEY_LINE_RE.match(stripped)

        if m:
            key, value = m.group(1), m.group(2)
            # pop the stack until the top has an indent < current
            while stack and stack[-1][0] >= indent:
                stack.pop()
            parent = stack[-1][1]
            node = Node(key=key, value=value)
            parent.children.append(node)
            stack.append((indent, node))
        else:
            # continuation of the deepest open node value,
            # regardless of the exact continuation indent (see docstring)
            if stack[-1][1] is not root:
                deepest = stack[-1][1]
                deepest.value = (deepest.value + " " + stripped).strip()
            # if stack[-1][1] is root — junk line outside any node
            # (document preamble etc.), silently ignored

    return root


def find_section(root: Node, key: str) -> Optional[Node]:
    """Finds a top-level node by key (e.g. 'SAFE_CASES')."""
    return root.child(key)
