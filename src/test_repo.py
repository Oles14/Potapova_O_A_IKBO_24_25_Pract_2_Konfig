
"""Чтение тестового графа из текстового файла."""

import re
from pathlib import Path

from src.graph import Graph


PACKAGE_NAME = r"[A-Z]+"


def read_test_repository(path: str) -> Graph:
    """Прочитать строки вида A: B C и проверить граф."""
    graph: Graph = {}
    text = Path(path).read_text(encoding="utf-8-sig")

    for number, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        if ":" not in line:
            raise ValueError(f"Строка {number}: пропущено ':'.")

        name, remainder = line.split(":", maxsplit=1)
        name = name.strip()
        children = remainder.split()

        if not re.fullmatch(PACKAGE_NAME, name):
            raise ValueError(f"Строка {number}: неверное имя '{name}'.")
        if any(not re.fullmatch(PACKAGE_NAME, x) for x in children):
            raise ValueError(f"Строка {number}: неверная зависимость.")
        if name in graph:
            raise ValueError(f"Строка {number}: повтор пакета {name}.")
        graph[name] = children

    if not graph:
        raise ValueError("Тестовый репозиторий пуст.")
    missing = set().union(*map(set, graph.values())) - graph.keys()
    if missing:
        raise ValueError("Не описаны пакеты: " + ", ".join(sorted(missing)))
    return graph
