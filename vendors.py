"""Модуль управления реестром продавцов и участников ярмарок.

Реализует операции добавления, поиска, фильтрации с использованием генераторов
и сортировки с применением lambda-функций в соответствии с требованиями ПР2.
"""

from typing import Dict, Generator, List, Optional


def validate_inn(inn: str) -> bool:
    """Проверяет корректность формата индивидуального номера налогоплательщика.

    Параметры:
        inn: строка ИНН (должна состоять из 10 или 12 цифр).

    Возвращает:
        True, если ИНН валиден, иначе False.
    """
    clean_inn = inn.strip()
    return clean_inn.isdigit() and (
        len(clean_inn) == 10 or len(clean_inn) == 12
    )


def add_vendor(
    vendors: List[Dict],
    name: str,
    inn: str,
    category: str,
    has_documents: bool,
    experience_years: int = 0,
) -> Dict:
    """Добавляет нового продавца в реестр с валидацией реквизитов.

    Параметры:
        vendors: список словарей продавцов.
        name: наименование бренда или ФИО мастера.
        inn: индивидуальный номер налогоплательщика.
        category: категория реализуемых изделий.
        has_documents: факт наличия обязательных документов.
        experience_years: стаж участия в ярмарочной торговле.

    Возвращает:
        Словарь с данными добавленного продавца.

    Исключения:
        ValueError: при ошибках в имени, ИНН или отсутствии документов.
    """
    clean_name = name.strip()
    if not clean_name:
        raise ValueError("Наименование продавца не может быть пустым.")

    if not validate_inn(inn):
        raise ValueError(
            f"Некорректный формат ИНН '{inn}'. Ожидается 10 или 12 цифр."
        )

    if not has_documents:
        raise ValueError("Регистрация невозможна без пакета документов.")

    if experience_years < 0:
        raise ValueError("Стаж участия не может быть отрицательным числом.")

    # Проверка уникальности ИНН
    for existing in vendors:
        if existing.get("inn") == inn.strip():
            raise ValueError(
                f"Продавец с ИНН '{inn}' уже зарегистрирован в системе."
            )

    # Генерация следующего идентификатора
    next_id = max((item["id"] for item in vendors), default=0) + 1

    new_vendor = {
        "id": next_id,
        "name": clean_name,
        "inn": inn.strip(),
        "category": category.strip(),
        "has_documents": has_documents,
        "experience_years": experience_years,
    }
    vendors.append(new_vendor)
    return new_vendor


def get_vendor_by_id(vendors: List[Dict], vendor_id: int) -> Optional[Dict]:
    """Возвращает продавца по уникальному идентификатору.

    Параметры:
        vendors: список продавцов.
        vendor_id: идентификатор искомого продавца.

    Возвращает:
        Словарь продавца или None при отсутствии.
    """
    for vendor in vendors:
        if vendor.get("id") == vendor_id:
            return vendor
    return None


def find_vendor_by_name(vendors: List[Dict], query: str) -> List[Dict]:
    """Выполняет поиск продавцов по нечувствительной к регистру подстроке.

    Параметры:
        vendors: список продавцов.
        query: поисковая подстрока.

    Возвращает:
        Список найденных продавцов.
    """
    search_query = query.strip().lower()
    if not search_query:
        return list(vendors)

    return [
        vendor for vendor in vendors
        if search_query in vendor.get("name", "").lower()
    ]


def filter_vendors_by_category(
    vendors: List[Dict],
    category: str,
) -> Generator[Dict, None, None]:
    """Генератор поэлементного отбора продавцов заданной категории товаров.

    Демонстрирует применение генераторов (yield) для эффективной обработки.

    Параметры:
        vendors: список продавцов.
        category: целевая категория товаров.

    Возвращает:
        Итератор/генератор подходящих продавцов.
    """
    normalized_target = category.strip().lower()
    for vendor in vendors:
        if vendor.get("category", "").strip().lower() == normalized_target:
            yield vendor


def sort_vendors(
    vendors: List[Dict],
    sort_by: str = "name",
    reverse: bool = False,
) -> List[Dict]:
    """Сортирует продавцов с использованием lambda-функции в качестве ключа.

    Параметры:
        vendors: список продавцов.
        sort_by: критерий сортировки ('name', 'experience', 'id').
        reverse: флаг обратного порядка сортировки.

    Возвращает:
        Отсортированный список продавцов.
    """
    if sort_by == "experience":
        key_function = lambda v: v.get("experience_years", 0)  # noqa: E731
    elif sort_by == "id":
        key_function = lambda v: v.get("id", 0)  # noqa: E731
    else:
        key_function = lambda v: v.get("name", "").lower()  # noqa: E731

    return sorted(vendors, key=key_function, reverse=reverse)
