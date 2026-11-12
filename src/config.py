
"Чтение и проверка параметров командной строки."

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse


PACKAGE_PATTERN = r"[A-Za-z0-9][A-Za-z0-9._+-]*"
VERSION_PATTERN = r"[A-Za-z0-9][A-Za-z0-9._+~-]*"


@dataclass(frozen=True)
class Config:
    "Настройки анализатора зависимостей."

    package: str
    repository: str
    test_mode: bool
    version: str
    ascii_tree: bool


def create_parser() -> argparse.ArgumentParser:
    "Создать парсер аргументов командной строки."
    parser = argparse.ArgumentParser(
        description="Анализатор зависимостей пакетов Alpine Linux"
    )
    parser.add_argument("--package", required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument(
        "--test-mode", action="store_true"
    )
    parser.add_argument(
        "--ascii-tree", action="store_true"
    )
    return parser


def validate_package(package: str) -> None:
    "Проверить корректность имени пакета."
    if not re.fullmatch(PACKAGE_PATTERN, package):
        raise ValueError(
            "Имя пакета содержит недопустимые символы."
        )


def validate_version(version: str) -> None:
    "Проверить корректность записи версии."
    if not re.fullmatch(VERSION_PATTERN, version):
        raise ValueError(
            "Версия пакета имеет недопустимый формат."
        )


def validate_repository(
    repository: str, test_mode: bool
) -> None:
    "Проверить URL или путь к тестовому файлу."
    if test_mode:
        path = Path(repository)
        if not path.is_file():
            raise ValueError(
                "Файл тестового репозитория не найден."
            )
        return

    parsed_url = urlparse(repository)
    if parsed_url.scheme not in ("http", "https"):
        raise ValueError(
            "URL должен начинаться с http:// или https://."
        )
    if not parsed_url.hostname:
        raise ValueError(
            "URL репозитория не содержит имени сервера."
        )
    try:
        parsed_url.port
    except ValueError as error:
        raise ValueError(
            "URL репозитория содержит неверный порт."
        ) from error


def parse_config(
    args: list[str] | None = None,
) -> Config:
    "Получить проверенную конфигурацию."
    parser = create_parser()
    values = parser.parse_args(args)

    try:
        validate_package(values.package)
        validate_version(values.version)
        validate_repository(
            values.repository, values.test_mode
        )
    except ValueError as error:
        parser.error(str(error))

    return Config(
        package=values.package,
        repository=values.repository,
        test_mode=values.test_mode,
        version=values.version,
        ascii_tree=values.ascii_tree,
    )
