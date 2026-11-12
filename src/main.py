

"Главный модуль анализатора зависимостей."

from src.apk_index import get_direct_dependencies
from src.config import Config, parse_config


def display_dependencies(
    config: Config,
    dependencies: list[str]
) -> None:
    "Вывести прямые зависимости пакета."
    print(f"Пакет: {config.package}")
    print(f"Версия: {config.version}")
    print("Прямые зависимости:")

    if not dependencies:
        print("Зависимости отсутствуют.")
        return

    for dependency in dependencies:
        print(f"- {dependency}")


def main() -> None:
    "Запустить анализ прямых зависимостей."
    config = parse_config()

    if config.test_mode:
        raise SystemExit(
            "Тестовый режим с локальным графом "
            "будет реализован на этапе 3."
        )

    try:
        dependencies = get_direct_dependencies(
            repository_url=config.repository,
            package_name=config.package,
            package_version=config.version,
        )
    except ValueError as error:
        raise SystemExit(f"Ошибка: {error}") from error

    display_dependencies(config, dependencies)


if __name__ == "__main__":
    main()
