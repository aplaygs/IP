"""Модуль работы с постоянным хранилищем данных в формате JSON.

Обеспечивает загрузку и сохранение списков ярмарок, продавцов и заявок
с использованием контекстных менеджеров и надежной обработкой исключений.
"""

import json
import os
from typing import Any, List, Union


DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
FAIRS_FILE = os.path.join(DATA_DIR, "fairs.json")
VENDORS_FILE = os.path.join(DATA_DIR, "vendors.json")
APPLICATIONS_FILE = os.path.join(DATA_DIR, "applications.json")


def load_json_file(filepath: str, default: Union[list, dict]) -> Any:
    """Загружает данные из JSON-файла с обработкой исключений.

    Параметры:
        filepath: путь к JSON-файлу.
        default: значение по умолчанию, возвращаемое при ошибках.

    Возвращает:
        Десериализованные данные или значение по умолчанию.
    """
    if not os.path.exists(filepath):
        return default

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError) as error:
        print(f"[Предупреждение]: ошибка при чтении {filepath}: {error}. "
              f"Использованы данные по умолчанию.")
        return default


def save_json_file(filepath: str, data: Any) -> bool:
    """Сохраняет данные в JSON-файл с использованием контекстного менеджера.

    Параметры:
        filepath: путь к JSON-файлу.
        data: структура данных для сериализации.

    Возвращает:
        True при успешной записи, иначе False.
    """
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        return True
    except OSError as error:
        print(f"[Ошибка]: не удалось сохранить данные в {filepath}: {error}")
        return False


def load_fairs() -> List[dict]:
    """Загружает список ярмарок из файла fairs.json."""
    return load_json_file(FAIRS_FILE, default=[])


def save_fairs(fairs: List[dict]) -> bool:
    """Сохраняет список ярмарок в файл fairs.json."""
    return save_json_file(FAIRS_FILE, fairs)


def load_vendors() -> List[dict]:
    """Загружает список продавцов из файла vendors.json."""
    return load_json_file(VENDORS_FILE, default=[])


def save_vendors(vendors: List[dict]) -> bool:
    """Сохраняет список продавцов в файл vendors.json."""
    return save_json_file(VENDORS_FILE, vendors)


def load_applications() -> List[dict]:
    """Загружает список заявок из файла applications.json."""
    return load_json_file(APPLICATIONS_FILE, default=[])


def save_applications(applications: List[dict]) -> bool:
    """Сохраняет список заявок в файл applications.json."""
    return save_json_file(APPLICATIONS_FILE, applications)
