import unittest
from pathlib import Path
import sys

# Добавляем папку src в путь поиска модулей, чтобы можно было импортировать Try (или ваш скрипт)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

# Импортируем функции из вашего скрипта (замените Try на фактическое имя файла, если оно изменится, например Try_2)
from Try import validate_config, load_config


class TestConfigValidation(unittest.TestCase):

    def setUp(self):
        """Базовый корректный словарь конфигурации для тестов."""
        self.valid_config = {
            "package_name": "test_package",
            "repo_url": "https://github.com/example/test",
            "repo_mode": "online",
            "package_version": "1.0.0",
            "output_image": "output.png",
            "max_depth": 3,
        }

    def test_validate_config_success(self):
        """Тест на успешную валидацию корректного конфига."""
        try:
            validate_config(self.valid_config)
        except Exception as e:
            self.fail(f"validate_config вызвал исключение на корректных данных: {e}")

    def test_missing_field(self):
        """Тест: ошибка при отсутствии обязательного поля."""
        invalid_config = self.valid_config.copy()
        del invalid_config["package_name"]

        with self.assertRaises(KeyError):
            validate_config(invalid_config)

    def test_invalid_type(self):
        """Тест: ошибка при неверном типе данных (например, строка вместо int для max_depth)."""
        invalid_config = self.valid_config.copy()
        invalid_config["max_depth"] = "three"  # Ожидается int

        with self.assertRaises(TypeError):
            validate_config(invalid_config)

    def test_bool_as_int(self):
        """Тест: boolean не должен проходить валидацию, если ожидается int."""
        invalid_config = self.valid_config.copy()
        invalid_config["max_depth"] = True  # В Python bool является подклассом int, проверяем обработку

        with self.assertRaises(TypeError):
            validate_config(invalid_config)

    def test_negative_max_depth(self):
        """Тест: ошибка, если max_depth меньше 0."""
        invalid_config = self.valid_config.copy()
        invalid_config["max_depth"] = -1

        with self.assertRaises(ValueError):
            validate_config(invalid_config)

    def test_invalid_repo_mode(self):
        """Тест: ошибка при недопустимом значении repo_mode."""
        invalid_config = self.valid_config.copy()
        invalid_config["repo_mode"] = "super_mode"

        with self.assertRaises(ValueError):
            validate_config(invalid_config)

    def test_file_not_found(self):
        """Тест: ошибка, если конфигурационный файл не существует."""
        with self.assertRaises(FileNotFoundError):
            load_config("non_existent_config_file_12345.toml")


if __name__ == "__main__":
    unittest.main()