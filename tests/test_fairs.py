"""Тесты для модуля fairs (объектная модель ярмарки Fair)."""

import pytest
from models.fairs import Fair, find_fair_by_id


def test_fair_creation_success():
    """Проверка успешной инициализации объекта Fair."""
    fair = Fair(
        fair_id=1,
        name="Осенняя ремесленная ярмарка",
        location="Москва, ВДНХ",
        date="2026-10-15",
        base_rate=1500.0,
        total_space=150.0,
    )
    assert fair.id == 1
    assert fair.name == "Осенняя ремесленная ярмарка"
    assert fair.location == "Москва, ВДНХ"
    assert fair.date == "2026-10-15"
    assert fair.base_rate == 1500.0
    assert fair.total_space == 150.0


def test_fair_validation_errors():
    """Проверка валидации параметров при инициализации Fair."""
    with pytest.raises(ValueError):
        Fair(-1, "Ярмарка", "Локация", "2026-10-15", 1000.0, 100.0)

    with pytest.raises(ValueError):
        Fair(1, "", "Локация", "2026-10-15", 1000.0, 100.0)

    with pytest.raises(ValueError):
        Fair(1, "Ярмарка", "Локация", "2026-10-15", -500.0, 100.0)

    with pytest.raises(ValueError):
        Fair(1, "Ярмарка", "Локация", "2026-10-15", 1000.0, 0.0)


def test_fair_space_available():
    """Проверка метода проверки доступности торговой площади."""
    fair = Fair(1, "Ярмарка", "ВДНХ", "2026-10-15", 1500.0, 100.0)

    assert fair.is_space_available(requested_space=20.0, occupied_space=50.0)
    assert fair.is_space_available(requested_space=50.0, occupied_space=50.0)
    assert not fair.is_space_available(
        requested_space=51.0, occupied_space=50.0
    )
    assert not fair.is_space_available(
        requested_space=-5.0, occupied_space=10.0
    )


def test_fair_get_free_space():
    """Проверка расчета свободного пространства на ярмарке."""
    fair = Fair(1, "Ярмарка", "ВДНХ", "2026-10-15", 1500.0, 100.0)
    assert fair.get_free_space(occupied_space=40.0) == 60.0
    assert fair.get_free_space(occupied_space=100.0) == 0.0
    assert fair.get_free_space(occupied_space=120.0) == 0.0


def test_fair_serialization():
    """Проверка сериализации в словарь и десериализации из словаря."""
    data = {
        "id": 5,
        "name": "Зимняя сказка",
        "location": "Парк Горького",
        "date": "2026-12-20",
        "base_rate": 2200.0,
        "total_space": 80.0,
    }
    fair = Fair.from_dict(data)
    assert fair.id == 5
    assert fair.name == "Зимняя сказка"

    exported = fair.to_dict()
    assert exported["id"] == 5
    assert exported["base_rate"] == 2200.0
    assert exported["total_space"] == 80.0


def test_fair_str_and_getitem():
    """Проверка строкового представления и обратной совместимости getitem."""
    fair = Fair(1, "Ярмарка", "ВДНХ", "2026-10-15", 1500.0, 100.0)
    assert "Ярмарка #1" in str(fair)
    assert fair["name"] == "Ярмарка"
    assert "total_space" in fair
    with pytest.raises(KeyError):
        _ = fair["unknown_key"]


def test_find_fair_by_id():
    """Проверка функции поиска ярмарки в коллекции."""
    fair1 = Fair(1, "Ярмарка 1", "Локация 1", "2026-10-15", 1000.0, 50.0)
    fair2 = Fair(2, "Ярмарка 2", "Локация 2", "2026-10-20", 2000.0, 80.0)
    collection = [fair1, fair2]

    assert find_fair_by_id(collection, 2) is fair2
    assert find_fair_by_id(collection, 99) is None
