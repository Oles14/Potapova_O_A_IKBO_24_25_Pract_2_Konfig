
"""Проверки чтения тестовых репозиториев."""

import tempfile
import unittest
from pathlib import Path

from src.test_repo import read_test_repository


class TestRepositoryTests(unittest.TestCase):
    """Проверки формата A: B C."""

    def read_text(self, text: str):
        """Создать временный файл и прочитать его."""
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "repo.txt"
            path.write_text(text, encoding="utf-8")
            return read_test_repository(str(path))

    def test_valid(self) -> None:
        """Проверить правильный файл."""
        graph = self.read_text("A: B\nB:\n")
        self.assertEqual(graph, {"A": ["B"], "B": []})

    def test_cycle(self) -> None:
        """Проверить файл с циклом."""
        graph = self.read_text("A: B\nB: A\n")
        self.assertEqual(graph["B"], ["A"])

    def test_missing_colon(self) -> None:
        """Проверить отсутствие двоеточия."""
        with self.assertRaises(ValueError):
            self.read_text("A B\n")

    def test_invalid_name(self) -> None:
        """Проверить строчную букву в имени."""
        with self.assertRaises(ValueError):
            self.read_text("a: B\nB:\n")

    def test_duplicate(self) -> None:
        """Проверить повторное описание пакета."""
        with self.assertRaises(ValueError):
            self.read_text("A:\nA:\n")

    def test_unknown_node(self) -> None:
        """Проверить неописанную зависимость."""
        with self.assertRaises(ValueError):
            self.read_text("A: Z\n")

    def test_empty(self) -> None:
        """Проверить пустой репозиторий."""
        with self.assertRaises(ValueError):
            self.read_text("\n")


if __name__ == "__main__":
    unittest.main()
