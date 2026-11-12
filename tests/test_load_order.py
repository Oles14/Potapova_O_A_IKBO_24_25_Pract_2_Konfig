
"""Тесты определения порядка загрузки зависимостей."""

import unittest

from src.graph import build_graph
from src.load_order import get_load_order


class LoadOrderTests(unittest.TestCase):
    """Проверки топологической сортировки."""

    def test_chain(self) -> None:
        """Проверить цепочку зависимостей."""
        data = {"A": ["B"], "B": ["C"], "C": []}
        graph = build_graph("A", data)
        self.assertEqual(
            get_load_order(graph, "A"), ["C", "B", "A"]
        )

    def test_diamond(self) -> None:
        """Проверить граф с общей зависимостью."""
        data = {
            "A": ["B", "C"],
            "B": ["D"],
            "C": ["D"],
            "D": [],
        }
        graph = build_graph("A", data)
        self.assertEqual(
            get_load_order(graph, "A"),
            ["D", "B", "C", "A"]
        )

    def test_branching(self) -> None:
        """Проверить независимые ветви."""
        data = {"A": ["B", "C"], "B": [], "C": []}
        graph = build_graph("A", data)
        self.assertEqual(
            get_load_order(graph, "A"), ["B", "C", "A"]
        )

    def test_single_package(self) -> None:
        """Проверить пакет без зависимостей."""
        graph = {"A": []}
        self.assertEqual(
            get_load_order(graph, "A"), ["A"]
        )

    def test_unreachable(self) -> None:
        """Проверить исключение посторонних пакетов."""
        graph = {"A": ["B"], "B": [], "Z": []}
        self.assertEqual(
            get_load_order(graph, "A"), ["B", "A"]
        )

    def test_cycle(self) -> None:
        """Проверить обнаружение цикла."""
        graph = {
            "A": ["B"], "B": ["C"], "C": ["A"]
        }
        with self.assertRaisesRegex(ValueError, "цикл"):
            get_load_order(graph, "A")

    def test_self_loop(self) -> None:
        """Проверить пакет, зависящий от себя."""
        with self.assertRaises(ValueError):
            get_load_order({"A": ["A"]}, "A")

    def test_missing_start(self) -> None:
        """Проверить отсутствующий начальный пакет."""
        with self.assertRaises(ValueError):
            get_load_order({"A": []}, "Z")

    def test_complex(self) -> None:
        """Проверить сложный граф."""
        data = {
            "A": ["B", "C"],
            "B": ["D", "E"],
            "C": ["E", "F"],
            "D": ["G"],
            "E": ["G"],
            "F": [],
            "G": [],
        }
        graph = build_graph("A", data)
        self.assertEqual(
            get_load_order(graph, "A"),
            ["G", "D", "E", "B", "F", "C", "A"]
        )

    def test_no_duplicates(self) -> None:
        """Проверить отсутствие повторных загрузок."""
        data = {
            "A": ["B", "C"],
            "B": ["D"],
            "C": ["D"],
            "D": [],
        }
        graph = build_graph("A", data)
        order = get_load_order(graph, "A")
        self.assertEqual(len(order), len(set(order)))


if __name__ == "__main__":
    unittest.main()
