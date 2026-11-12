
"Тесты параметров командной строки."

import unittest

from src.config import parse_config


class ConfigTests(unittest.TestCase):
    "Проверки первого этапа приложения."

    def setUp(self) -> None:
        "Подготовить правильные параметры."
        self.args = [
            "--package", "curl",
            "--repository", "https://example.com/repo",
            "--version", "8.7.1-r0",
        ]

    def test_valid_config(self) -> None:
        "Проверить правильную конфигурацию."
        config = parse_config(self.args)
        self.assertEqual(config.package, "curl")
        self.assertEqual(config.version, "8.7.1-r0")
        self.assertFalse(config.test_mode)
        self.assertFalse(config.ascii_tree)

    def test_missing_package(self) -> None:
        "Проверить отсутствие имени пакета."
        args = self.args[2:]
        with self.assertRaises(SystemExit):
            parse_config(args)

    def test_invalid_package(self) -> None:
        "Проверить неверное имя пакета."
        args = self.args.copy()
        args[1] = "bad package!"
        with self.assertRaises(SystemExit):
            parse_config(args)

    def test_invalid_repository(self) -> None:
        "Проверить неверный URL."
        args = self.args.copy()
        args[3] = "not-a-url"
        with self.assertRaises(SystemExit):
            parse_config(args)

    def test_invalid_version(self) -> None:
        "Проверить неверную версию."
        args = self.args.copy()
        args[5] = "bad version!"
        with self.assertRaises(SystemExit):
            parse_config(args)

    def test_missing_test_file(self) -> None:
        "Проверить отсутствующий тестовый файл."
        args = self.args.copy()
        args[3] = "missing_repository.txt"
        args.append("--test-mode")
        with self.assertRaises(SystemExit):
            parse_config(args)

    def test_invalid_boolean_option(self) -> None:
        "Проверить неизвестное значение флага."
        args = self.args + ["--ascii-tree", "maybe"]
        with self.assertRaises(SystemExit):
            parse_config(args)

    def test_valid_test_mode(self) -> None:
        "Проверить корректный тестовый режим."
        args = self.args.copy()
        args[1] = "A"
        args[3] = "tests/data/sample_repo.txt"
        args.extend(["--test-mode", "--ascii-tree"])
        config = parse_config(args)
        self.assertTrue(config.test_mode)
        self.assertTrue(config.ascii_tree)


if __name__ == "__main__":
    unittest.main()
