import os
from pathlib import Path
import sys
import tomllib

CONFIG_FILE = "config.toml"


def load_config(file_path: str) -> dict:
    """Загружает и парсит TOML файл."""
    curr_dir = Path(__file__).resolve().parent
    config_path = curr_dir / file_path

    if not config_path.exists():
        raise FileNotFoundError(
            f"Файл '{file_path}' не найден."
        )

    try:
        with open(config_path, "rb") as f:
            return tomllib.load(f)
    except tomllib.TOMLDecodeError as e:
        raise ValueError(f"Ошибка синтаксиса TOML: {e}")


def validate_config(config: dict) -> None:
    """Проверяет обязательные параметры."""
    req_fields = {
        "package_name": str,
        "repo_url": str,
        "repo_mode": str,
        "package_version": str,
        "output_image": str,
        "max_depth": int,
    }

    for field, exp_type in req_fields.items():
        if field not in config:
            raise KeyError(
                f"Отсутствует параметр: '{field}'"
            )

        val = config[field]
        is_bool = isinstance(val, bool)
        if not isinstance(val, exp_type) or (
            exp_type is int and is_bool
        ):
            raise TypeError(
                f"Неверный тип '{field}'. "
                f"Ожидался {exp_type.__name__}, "
                f"получен {type(val).__name__}"
            )

    if config["max_depth"] < 0:
        raise ValueError(
            "Параметр 'max_depth' < 0."
        )

    valid_modes = ["online", "offline", "test"]
    if config["repo_mode"] not in valid_modes:
        raise ValueError(
            f"Некорректный режим 'repo_mode': "
            f"'{config['repo_mode']}'"
        )


def main():
    print("=== Инициализация CLI ===")
    try:
        config = load_config(CONFIG_FILE)
        validate_config(config)

        print("\n[Успешно] Конфигурация:")
        for key, value in config.items():
            print(f"  - {key} = {value}")

    except (
        FileNotFoundError,
        ValueError,
        KeyError,
        TypeError,
    ) as e:
        print(
            f"\n[ОШИБКА]: {e}",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()