
"""Проверки рекурсивного обхода графа."""

import unittest
from unittest.mock import patch

from src.graph import build_apk_graph, build_graph


class GraphTests(unittest.TestCase):
    """Тесты графов разных типов."""

    def test_chain(self) -> None:
        """Проверить цепочку зависимостей."""
        data = {"A": ["B"], "B": ["C"], "C": []}
        graph = build_graph("A", data)
        self.assertEqual(list(graph), ["A", "B", "C"])

    def test_branching(self) -> None:
        """Проверить разветвление графа."""
        data = {"A": ["B", "C"], "B": [], "C": []}
        graph = build_graph("A", data)
        self.assertEqual(graph["A"], ["B", "C"])

    def test_diamond(self) -> None:
        """Проверить общую зависимость двух пакетов."""
        data = {
            "A": ["B", "C"],
            "B": ["D"],
            "C": ["D"],
            "D": []
        }
        graph = build_graph("A", data)
        self.assertEqual(len(graph), 4)
        self.assertEqual(graph["C"], ["D"])

    def test_cycle(self) -> None:
        """Проверить циклические зависимости."""
        data = {
            "A": ["B"],
            "B": ["C"],
            "C": ["A"]
        }
        graph = build_graph("A", data)
        self.assertEqual(graph["C"], ["A"])
        self.assertEqual(len(graph), 3)

    def test_self_loop(self) -> None:
        """Проверить зависимость пакета от самого себя."""
        data = {"A": ["A"]}
        graph = build_graph("A", data)
        self.assertEqual(graph, {"A": ["A"]})

    def test_unreachable(self) -> None:
        """Проверить недостижимую вершину."""
        data = {"A": [], "Z": []}
        graph = build_graph("A", data)
        self.assertNotIn("Z", graph)

    def test_apk_graph(self) -> None:
        """Проверить транзитивные зависимости apk."""
        text = (
            "P:A\nV:1.0-r0\nD:B\n\n"
            "P:B\nV:2.0-r0\nD:C\n\n"
            "P:C\nV:3.0-r0\n"
        )
        with patch(
            "src.graph.download_index", return_value=text
        ):
            graph = build_apk_graph(
                "https://example.com", "A", "1.0-r0"
            )

        self.assertEqual(graph["A"], ["B"])
        self.assertEqual(graph["B"], ["C"])

    def test_unresolved_virtual(self) -> None:
        """Проверить виртуальную зависимость apk."""
        text = "P:A\nV:1.0-r0\nD:so:libc.so.1\n"

        with patch(
            "src.graph.download_index", return_value=text
        ):
            graph = build_apk_graph(
                "https://example.com", "A", "1.0-r0"
            )

        self.assertEqual(graph["so:libc.so.1"], [])


if __name__ == "__main__":
    unittest.main()
