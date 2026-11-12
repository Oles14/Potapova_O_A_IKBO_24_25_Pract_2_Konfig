
"Получение зависимостей из индекса Alpine Linux."

import io
import tarfile
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


INDEX_FILENAME = "APKINDEX.tar.gz"
REQUEST_TIMEOUT = 15


@dataclass(frozen=True)
class PackageInfo:
    "Информация о пакете Alpine Linux."

    name: str
    version: str
    dependencies: list[str]


def download_index(repository_url: str) -> str:
    "Скачать и распаковать индекс репозитория."
    url = repository_url.rstrip("/")

    if not url.endswith(INDEX_FILENAME):
        url = f"{url}/{INDEX_FILENAME}"

    try:
        with urlopen(url, timeout=REQUEST_TIMEOUT) as response:
            archive_data = response.read()
    except (HTTPError, URLError, TimeoutError) as error:
        raise ValueError(
            f"Не удалось скачать индекс: {error}"
        ) from error

    try:
        with tarfile.open(
            fileobj=io.BytesIO(archive_data),
            mode="r:gz"
        ) as archive:
            index_file = archive.extractfile("APKINDEX")
            if index_file is None:
                raise ValueError("Файл APKINDEX не найден.")

            return index_file.read().decode("utf-8")
    except (tarfile.TarError, KeyError, UnicodeError) as error:
        raise ValueError(
            "Не удалось прочитать APKINDEX.tar.gz."
        ) from error


def parse_index(index_text: str) -> list[PackageInfo]:
    "Преобразовать текст индекса в список пакетов."
    packages = []
    normalized = index_text.replace("\r\n", "\n")

    for block in normalized.split("\n\n"):
        fields = {}

        for line in block.splitlines():
            if len(line) >= 2 and line[1] == ":":
                fields[line[0]] = line[2:]

        if "P" not in fields or "V" not in fields:
            continue

        dependencies = fields.get("D", "").split()

        packages.append(
            PackageInfo(
                name=fields["P"],
                version=fields["V"],
                dependencies=dependencies,
            )
        )

    return packages


def find_package(
    packages: list[PackageInfo],
    name: str,
    version: str
) -> PackageInfo:
    "Найти пакет с точным совпадением версии."
    for package in packages:
        if package.name == name and package.version == version:
            return package

    raise ValueError(
        f"Пакет {name} версии {version} не найден."
    )


def get_direct_dependencies(
    repository_url: str,
    package_name: str,
    package_version: str
) -> list[str]:
    "Получить прямые зависимости заданного пакета."
    index_text = download_index(repository_url)
    packages = parse_index(index_text)
    package = find_package(
        packages, package_name, package_version
    )

    return package.dependencies
