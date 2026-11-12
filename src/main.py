
"""Главный модуль анализатора зависимостей."""

from src.config import Config, parse_config
from src.graph import Graph, build_apk_graph, build_graph
from src.test_repo import read_test_repository


def display_graph(graph: Graph, config: Config) -> None:
    """Вывести найденные зависимости в виде списка рёбер."""
    print(f"Пакет: {config.package}")
    if not config.test_mode:
        print(f"Версия: {config.version}")
    print("Граф зависимостей:")

    for package, children in graph.items():
        if not children:
            print(f"{package}: нет зависимостей")
        for child in children:
            print(f"{package} -> {child}")


def main() -> None:
    """Построить граф по реальному или тестовому источнику."""
    config = parse_config()

    try:
        if config.test_mode:
            dependencies = read_test_repository(config.repository)
            if config.package not in dependencies:
                raise ValueError("Начальный пакет отсутствует в файле.")
            graph = build_graph(config.package, dependencies)
        else:
            graph = build_apk_graph(
                config.repository, config.package, config.version
            )
    except (ValueError, OSError) as error:
        raise SystemExit(f"Ошибка: {error}") from error

    display_graph(graph, config)


if __name__ == "__main__":
    main()
