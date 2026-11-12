
"Главный модуль анализатора зависимостей."

from src.config import Config, parse_config


def display_config(config: Config) -> None:
    "Показать все параметры в формате ключ-значение."
    print("Параметры анализатора зависимостей:")
    print(f"package: {config.package}")
    print(f"repository: {config.repository}")
    print(f"test_mode: {config.test_mode}")
    print(f"version: {config.version}")
    print(f"ascii_tree: {config.ascii_tree}")


def main() -> None:
    "Запустить первый этап приложения."
    config = parse_config()
    display_config(config)


if __name__ == "__main__":
    main()
