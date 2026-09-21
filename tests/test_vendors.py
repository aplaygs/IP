"""Автоматические тесты для модуля vendors (управление продавцами)."""

import pytest
from vendors import (
    add_vendor,
    filter_vendors_by_category,
    find_vendor_by_name,
    get_vendor_by_id,
    sort_vendors,
    validate_inn,
)


def test_validate_inn():
    """Проверка валидатора ИНН."""
    assert validate_inn("7701234567") is True  # 10 цифр
    assert validate_inn("770123456789") is True  # 12 цифр
    assert validate_inn("123456789") is False  # 9 цифр
    assert validate_inn("77012345678A") is False  # содержит букву


def test_add_vendor_success():
    """Проверка успешного добавления продавца в список."""
    vendors = []
    vendor = add_vendor(
        vendors=vendors,
        name="Мастерская",
        inn="770123456789",
        category="Ремесла",
        has_documents=True,
        experience_years=3,
    )
    assert len(vendors) == 1
    assert vendor["id"] == 1
    assert vendor["name"] == "Мастерская"


def test_add_vendor_duplicate_inn_forbidden():
    """Проверка запрета добавления продавца с дублирующимся ИНН."""
    vendors = []
    add_vendor(vendors, "Мастерская 1", "770123456789", "Ремесла", True, 2)
    with pytest.raises(ValueError) as excinfo:
        add_vendor(
            vendors, "Мастерская 2", "770123456789", "Сувениры", True, 1
        )
    assert "уже зарегистрирован" in str(excinfo.value)


def test_find_vendor_by_name():
    """Проверка поиска продавца по подстроке."""
    vendors = [
        {"id": 1, "name": "Гончарная лавка"},
        {"id": 2, "name": "Кузнечный двор"},
    ]
    results = find_vendor_by_name(vendors, "гончар")
    assert len(results) == 1
    assert results[0]["id"] == 1


def test_filter_vendors_by_category_generator():
    """Проверка фильтрации продавцов через генератор yield."""
    vendors = [
        {"id": 1, "name": "Мёд", "category": "Продукты питания"},
        {"id": 2, "name": "Глина", "category": "Ремесла"},
        {"id": 3, "name": "Сыр", "category": "Продукты питания"},
    ]
    food_gen = filter_vendors_by_category(vendors, "Продукты питания")
    food_list = list(food_gen)
    assert len(food_list) == 2
    assert food_list[0]["name"] == "Мёд"
    assert food_list[1]["name"] == "Сыр"


def test_sort_vendors_lambda():
    """Проверка сортировки продавцов через lambda по стажу."""
    vendors = [
        {"id": 1, "name": "Новичок", "experience_years": 1},
        {"id": 2, "name": "Опытный", "experience_years": 10},
        {"id": 3, "name": "Средний", "experience_years": 5},
    ]
    sorted_vendors = sort_vendors(vendors, sort_by="experience", reverse=True)
    assert sorted_vendors[0]["name"] == "Опытный"
    assert sorted_vendors[-1]["name"] == "Новичок"


def test_get_vendor_by_id():
    """Проверка поиска продавца по ID."""
    vendors = [{"id": 10, "name": "Тест"}]
    assert get_vendor_by_id(vendors, 10) is not None
    assert get_vendor_by_id(vendors, 99) is None
