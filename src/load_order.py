
"""Определение порядка загрузки зависимостей."""

from src.graph import Graph


def get_load_order(graph: Graph, start: str) -> list[str]:
    """Определить порядок: зависимости раньше пакета."""
    if start not in graph:
        raise ValueError(
            f"Начальный пакет {start} отсутствует в графе."
        )

    order: list[str] = []
    active: set[str] = set()
    completed: set[str] = set()
    path: list[str] = []

    def dfs(package: str) -> None:
        """Рекурсивно обработать пакет и его зависимости."""
        if package in active:
            position = path.index(package)
            cycle = path[position:] + [package]
            raise ValueError(
                "Обнаружен цикл: " + " -> ".join(cycle)
            )

        if package in completed:
            return

        active.add(package)
        path.append(package)

        for dependency in graph.get(package, []):
            dfs(dependency)

        path.pop()
        active.remove(package)
        completed.add(package)
        order.append(package)

    dfs(start)
    return order
