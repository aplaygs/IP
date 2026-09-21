"""Модуль работы с постоянным хранилищем данных в формате JSON.

Обеспечивает загрузку и сохранение объектов Fair, Vendor и Application
с использованием контекстных менеджеров with open, обработкой исключений
и преобразованием между JSON-структурами и объектами моделей.
"""

import json
import os
from typing import Any, List, Optional, Union

from models.applications import Application
from models.fairs import Fair, find_fair_by_id
from models.vendors import Vendor, find_vendor_by_id

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
        print(
            f"[Предупреждение]: ошибка при чтении {filepath}: {error}. "
            f"Использованы данные по умолчанию."
        )
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


# Алиасы для обратной совместимости
safe_load_json = load_json_file
safe_save_json = save_json_file


def load_fairs() -> List[Fair]:
    """Загружает ярмарки из fairs.json и преобразует их в объекты Fair."""
    raw_data = load_json_file(FAIRS_FILE, default=[])
    fairs: List[Fair] = []
    for item in raw_data:
        try:
            fairs.append(Fair.from_dict(item))
        except (KeyError, ValueError) as err:
            print(f"[Предупреждение]: пропуск поврежденной ярмарки: {err}")
    return fairs


def save_fairs(fairs: List[Any]) -> bool:
    """Сохраняет список объектов Fair в файл fairs.json."""
    serialized = [
        item.to_dict() if hasattr(item, "to_dict") else item
        for item in fairs
    ]
    return save_json_file(FAIRS_FILE, serialized)


def load_vendors() -> List[Vendor]:
    """Загружает продавцов из vendors.json и преобразует в объекты Vendor."""
    raw_data = load_json_file(VENDORS_FILE, default=[])
    vendors: List[Vendor] = []
    for item in raw_data:
        try:
            vendors.append(Vendor.from_dict(item))
        except (KeyError, ValueError) as err:
            print(f"[Предупреждение]: пропуск некорректного продавца: {err}")
    return vendors


def save_vendors(vendors: List[Any]) -> bool:
    """Сохраняет список объектов Vendor в файл vendors.json."""
    serialized = [
        item.to_dict() if hasattr(item, "to_dict") else item
        for item in vendors
    ]
    return save_json_file(VENDORS_FILE, serialized)


def load_applications(
    vendors: Optional[List[Vendor]] = None,
    fairs: Optional[List[Fair]] = None,
) -> List[Application]:
    """Загружает заявки из applications.json и связывает их с объектами.

    Параметры:
        vendors: список объектов продавцов (если None, загружаются из файла).
        fairs: список объектов ярмарок (если None, загружаются из файла).

    Возвращает:
        Список объектов Application со ссылками на объекты Vendor и Fair.
    """
    if vendors is None:
        vendors = load_vendors()
    if fairs is None:
        fairs = load_fairs()

    raw_data = load_json_file(APPLICATIONS_FILE, default=[])
    applications: List[Application] = []

    for item in raw_data:
        v_id = item.get("vendor_id")
        f_id = item.get("fair_id")

        vendor_obj = find_vendor_by_id(vendors, v_id) if v_id else None
        fair_obj = find_fair_by_id(fairs, f_id) if f_id else None

        if not vendor_obj:
            vendor_obj = Vendor(
                vendor_id=v_id or 1,
                name=f"Продавец #{v_id}",
                inn="7700000000",
                category="Общая",
                has_documents=True,
            )

        if not fair_obj:
            fair_obj = Fair(
                fair_id=f_id or 1,
                name=f"Ярмарка #{f_id}",
                location="Городская площадь",
                date="2026-10-01",
                base_rate=1500.0,
                total_space=100.0,
            )

        try:
            app_obj = Application.from_dict(
                item, vendor=vendor_obj, fair=fair_obj
            )
            applications.append(app_obj)
        except (KeyError, ValueError) as err:
            print(f"[Предупреждение]: пропуск поврежденной заявки: {err}")

    return applications


def save_applications(applications: List[Any]) -> bool:
    """Сохраняет список объектов Application в файл applications.json."""
    serialized = [
        item.to_dict() if hasattr(item, "to_dict") else item
        for item in applications
    ]
    return save_json_file(APPLICATIONS_FILE, serialized)
