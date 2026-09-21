"""Автоматические тесты для ООП-моделей (Vendor, Application, ПР3)."""

import pytest
from models.applications import (
    Application,
    calculate_fair_statistics,
    cancel_application,
    create_application,
    get_occupied_space,
)
from models.fairs import Fair
from models.vendors import (
    CraftVendor,
    FoodVendor,
    SouvenirVendor,
    Vendor,
)


def test_vendor_oop_validation():
    """Проверка инкапсулированной валидации в классе Vendor."""
    with pytest.raises(ValueError):
        Vendor(0, "Имя", "7701234567", "Категория", True)

    with pytest.raises(ValueError):
        Vendor(1, "", "7701234567", "Категория", True)

    with pytest.raises(ValueError):
        Vendor(1, "Имя", "123", "Категория", True)

    with pytest.raises(ValueError):
        Vendor(1, "Имя", "7701234567", "Категория", False)

    with pytest.raises(ValueError):
        Vendor(1, "Имя", "7701234567", "Категория", True, -1)


def test_vendor_polymorphism():
    """Проверка полиморфизма тарифов и строкового представления подклассов."""
    craft = CraftVendor(1, "Гончар", "7701234567", True, 4)
    food = FoodVendor(2, "Фермер", "7702222222", True, 2)
    souvenir = SouvenirVendor(3, "Сувенирщик", "7703333333", True, 1)
    general = Vendor(4, "Универсал", "7704444444", "Разное", True, 0)

    assert craft.get_category_coefficient() == 1.0
    assert food.get_category_coefficient() == 1.3
    assert souvenir.get_category_coefficient() == 1.1
    assert general.get_category_coefficient() == 1.2

    assert "[Ремесленник]" in str(craft)
    assert "[Фермер/Гастрономия]" in str(food)
    assert "[Сувениры]" in str(souvenir)


def test_vendor_factory_from_dict():
    """Проверка создания экземпляров соответствующих классов фабрикой."""
    data_craft = {
        "id": 1,
        "name": "Кузница",
        "inn": "7701234567",
        "category": "Ремесла",
        "has_documents": True,
        "experience_years": 5,
    }
    obj_craft = Vendor.from_dict(data_craft)
    assert isinstance(obj_craft, CraftVendor)
    assert obj_craft.get_category_coefficient() == 1.0

    data_food = {
        "id": 2,
        "name": "Сыроварня",
        "inn": "7702222222",
        "category": "Продукты питания",
        "has_documents": True,
        "experience_years": 2,
    }
    obj_food = Vendor.from_dict(data_food)
    assert isinstance(obj_food, FoodVendor)
    assert obj_food.get_category_coefficient() == 1.3

    exported = obj_food.to_dict()
    assert exported["id"] == 2
    assert exported["category"] == "Продукты питания"


def test_application_oop_model():
    """Проверка объектной модели Application и прямых ссылок."""
    fair = Fair(1, "Ярмарка мастеров", "ВДНХ", "2026-10-15", 1500.0, 100.0)
    vendor = CraftVendor(1, "Мастер Иван", "7701234567", True, 3)

    app = Application(
        application_id=1,
        vendor=vendor,
        fair=fair,
        requested_space=10.0,
    )
    assert app.vendor is vendor
    assert app.fair is fair
    assert app.vendor.name == "Мастер Иван"
    assert app.fair.total_space == 100.0

    fee_discount = app.calculate_fee(is_first_time=True)
    assert fee_discount == 12750.0
    assert app.fee == 12750.0

    card = app.generate_card()
    assert "Мастер Иван" in card
    assert "15.10.2026" in card
    assert "12 750.00 руб." in card

    assert not app.is_cancelled
    app.cancel()
    assert app.is_cancelled
    assert "Отменена" in app.status


def test_application_oop_validation():
    """Проверка валидации при создании экземпляра Application."""
    fair = Fair(1, "Ярмарка", "Локация", "2026-10-15", 1000.0, 50.0)
    vendor = Vendor(1, "Продавец", "7701234567", "Категория", True)

    with pytest.raises(ValueError):
        Application(0, vendor, fair, 10.0)

    with pytest.raises(ValueError):
        Application(1, vendor, fair, -2.0)


def test_application_oop_lifecycle():
    """Интеграционный тест жизненного цикла заявки на уровне объектов."""
    fair = Fair(10, "Фестиваль урожая", "Сокольники", "2026-09-30", 2000.0, 50)
    farmer = FoodVendor(20, "Эко-ферма", "7709876543", True, 4)
    apps = []

    app = create_application(
        applications=apps,
        vendor=farmer,
        fair=fair,
        requested_space=20.0,
        is_first_time=False,
        is_paid=True,
    )
    assert len(apps) == 1
    assert app.fee == 52000.0
    assert get_occupied_space(apps, fair.id) == 20.0

    stats = calculate_fair_statistics(apps, fair)
    assert stats["occupied_space"] == 20.0
    assert stats["free_space"] == 30.0
    assert stats["total_revenue"] == 52000.0

    res = cancel_application(apps, app.id)
    assert res is True
    assert app.is_cancelled
    assert get_occupied_space(apps, fair.id) == 0.0
