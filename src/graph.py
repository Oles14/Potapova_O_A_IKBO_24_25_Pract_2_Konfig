
"""Построение графа зависимостей рекурсивным DFS."""

import re

from src.apk_index import download_index, find_package, parse_index


Graph = dict[str, list[str]]


def build_graph(start: str, dependencies: Graph) -> Graph:
    """Обойти зависимости в глубину, сохраняя все рёбра."""
    result: Graph = {}
    visited: set[str] = set()

    def dfs(package: str) -> None:
        """Рекурсивно исследовать один пакет."""
        if package in visited:
            return

        visited.add(package)
        children = dependencies.get(package, [])
        result[package] = list(children)

        for child in children:
            dfs(child)

    dfs(start)
    return result


def dependency_name(requirement: str) -> str:
    """Выделить имя из простого требования apk."""
    return re.split(r"[<>=~]", requirement, maxsplit=1)[0]


def build_apk_graph(
    repository: str, name: str, version: str
) -> Graph:
    """Построить граф по одному индексу Alpine Linux."""
    packages = parse_index(download_index(repository))
    root = find_package(packages, name, version)
    by_name = {package.name: package for package in packages}
    by_name[name] = root
    dependencies: Graph = {}

    for package in by_name.values():
        children = []
        for requirement in package.dependencies:
            candidate = dependency_name(requirement)
            if candidate in by_name and not requirement.startswith("!"):
                children.append(candidate)
            else:
                children.append(requirement)
        dependencies[package.name] = children

    return build_graph(name, dependencies)
