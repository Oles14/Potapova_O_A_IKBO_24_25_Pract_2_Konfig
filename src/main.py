
"""Главный модуль анализатора зависимостей."""

from src.config import Config, parse_config
from src.graph import Graph, build_apk_graph, build_graph
from src.load_order import get_load_order
from src.test_repo import read_test_repository


def display_graph(graph: Graph, config: Config) -> None:
    """Вывести граф в виде списка рёбер."""
    print(f"Пакет: {config.package}")
    if not config.test_mode:
        print(f"Версия: {config.version}")
    print("Граф зависимостей:")

    for package, children in graph.items():
        if not children:
            print(f"{package}: нет зависимостей")
        for child in children:
            print(f"{package} -> {child}")


def display_load_order(
    order: list[str], config: Config
) -> None:
    """Вывести порядок загрузки пакетов."""
    print(f"Пакет: {config.package}")
    if not config.test_mode:
        print(f"Версия: {config.version}")
    print("Порядок загрузки зависимостей:")

    for number, package in enumerate(order, start=1):
        print(f"{number}. {package}")


def get_graph(config: Config) -> Graph:
    """Получить граф из выбранного источника."""
    if config.test_mode:
        dependencies = read_test_repository(config.repository)
        if config.package not in dependencies:
            raise ValueError(
                "Начальный пакет отсутствует в файле."
            )
        return build_graph(config.package, dependencies)

    return build_apk_graph(
        config.repository, config.package, config.version
    )


def main() -> None:
    """Запустить анализ зависимостей пакетов."""
    config = parse_config()

    try:
        graph = get_graph(config)

        if config.load_order:
            order = get_load_order(graph, config.package)
            display_load_order(order, config)
        else:
            display_graph(graph, config)

    except (ValueError, OSError) as error:
        raise SystemExit(f"Ошибка: {error}") from error


if __name__ == "__main__":
    main()
