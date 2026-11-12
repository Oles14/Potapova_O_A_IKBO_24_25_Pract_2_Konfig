
"""Тесты получения зависимостей apk."""

import io
import tarfile
import unittest
from unittest.mock import patch

from src.apk_index import (
    download_index,
    find_package,
    get_direct_dependencies,
    parse_index,
)


SAMPLE_INDEX = """P:curl
V:8.14.1-r2
D:libcurl so:libc.musl-x86_64.so.1

P:libcurl
V:8.14.1-r2
D:ca-certificates so:libssl.so.3

P:empty
V:1.0-r0

P:curl
V:8.13.0-r0
D:older-library
"""


def make_archive(content: str) -> bytes:
    """Создать тестовый архив APKINDEX."""
    data = content.encode("utf-8")
    buffer = io.BytesIO()

    with tarfile.open(fileobj=buffer, mode="w:gz") as archive:
        info = tarfile.TarInfo(name="APKINDEX")
        info.size = len(data)
        archive.addfile(info, io.BytesIO(data))

    return buffer.getvalue()


class ApkIndexTests(unittest.TestCase):
    """Проверки второго этапа."""

    def test_parse_index(self) -> None:
        """Проверить чтение записей индекса."""
        packages = parse_index(SAMPLE_INDEX)
        self.assertEqual(len(packages), 4)

    def test_package_name(self) -> None:
        """Проверить имя найденного пакета."""
        packages = parse_index(SAMPLE_INDEX)
        package = find_package(
            packages, "curl", "8.14.1-r2"
        )
        self.assertEqual(package.name, "curl")

    def test_exact_version(self) -> None:
        """Проверить точное совпадение версии."""
        packages = parse_index(SAMPLE_INDEX)
        package = find_package(
            packages, "curl", "8.13.0-r0"
        )
        self.assertEqual(
            package.dependencies, ["older-library"]
        )

    def test_dependencies(self) -> None:
        """Проверить прямые зависимости."""
        packages = parse_index(SAMPLE_INDEX)
        package = find_package(
            packages, "curl", "8.14.1-r2"
        )
        self.assertEqual(
            package.dependencies,
            ["libcurl", "so:libc.musl-x86_64.so.1"]
        )

    def test_empty_dependencies(self) -> None:
        """Проверить пакет без зависимостей."""
        packages = parse_index(SAMPLE_INDEX)
        package = find_package(
            packages, "empty", "1.0-r0"
        )
        self.assertEqual(package.dependencies, [])

    def test_missing_package(self) -> None:
        """Проверить отсутствующий пакет."""
        packages = parse_index(SAMPLE_INDEX)
        with self.assertRaises(ValueError):
            find_package(packages, "unknown", "1.0-r0")

    def test_download_index(self) -> None:
        """Проверить скачивание и распаковку."""
        archive = make_archive(SAMPLE_INDEX)

        with patch("src.apk_index.urlopen") as mock:
            mock.return_value.__enter__.return_value.read.return_value = archive
            text = download_index("https://example.com/repo")

        self.assertEqual(text, SAMPLE_INDEX)
        self.assertTrue(mock.called)

    def test_invalid_archive(self) -> None:
        """Проверить повреждённый архив."""
        with patch("src.apk_index.urlopen") as mock:
            mock.return_value.__enter__.return_value.read.return_value = b"bad"
            with self.assertRaises(ValueError):
                download_index("https://example.com/repo")

    def test_full_dependency_flow(self) -> None:
        """Проверить весь процесс получения зависимостей."""
        with patch(
            "src.apk_index.download_index",
            return_value=SAMPLE_INDEX
        ):
            dependencies = get_direct_dependencies(
                "https://example.com/repo",
                "curl",
                "8.14.1-r2",
            )

        self.assertEqual(
            dependencies,
            ["libcurl", "so:libc.musl-x86_64.so.1"]
        )


if __name__ == "__main__":
    unittest.main()
