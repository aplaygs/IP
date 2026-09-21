"""Автоматические тесты для модуля applications (управление заявками)."""

import pytest
from applications import (
    calculate_fair_statistics,
    calculate_participation_fee,
    cancel_application,
    create_application,
    get_occupied_space,
    is_space_available,
    validate_vendor_data,
)


@pytest.fixture
def sample_fair():
    """Тестовые данные ярмарки."""
    return {
        "id": 1,
        "name": "Ярмарка мастеров",
        "base_rate": 1000.0,
        "total_space": 50.0,
    }


@pytest.fixture
def sample_vendor():
    """Тестовые данные продавца."""
    return {
        "id": 1,
        "name": "Гончар",
        "inn": "770123456789",
        "category": "Ремесла",
        "has_documents": True,
    }


def test_validate_vendor_data():
    """Проверка валидатора данных продавца из ПР1."""
    assert validate_vendor_data("Мастер", "770123456789", True) is True
    assert validate_vendor_data("", "770123456789", True) is False
    assert validate_vendor_data("Мастер", "123", True) is False


def test_calculate_participation_fee():
    """Проверка расчета арендного сбора со скидкой и без."""
    # Ремесла (коэф 1.0), 10 кв.м, без скидки = 10 000 руб
    fee_standard = calculate_participation_fee(1000.0, "Ремесла", 10.0, False)
    assert fee_standard == 10000.0

    # Ремесла (коэф 1.0), 10 кв.м, скидка новичка 15% = 8 500 руб
    fee_discount = calculate_participation_fee(1000.0, "Ремесла", 10.0, True)
    assert fee_discount == 8500.0


def test_is_space_available(sample_fair):
    """Проверка контроля торговой площади ярмарки."""
    applications = []
    # 50 кв.м свободно, запрашиваем 30 -> доступно
    assert is_space_available(applications, sample_fair, 30.0) is True

    # Занимаем 30 кв.м
    applications.append({
        "id": 1,
        "fair_id": sample_fair["id"],
        "requested_space": 30.0,
        "status": "Одобрена",
    })
    # Осталось 20 кв.м. Запрашиваем 25 -> недоступно
    assert is_space_available(applications, sample_fair, 25.0) is False
    # Запрашиваем 15 -> доступно
    assert is_space_available(applications, sample_fair, 15.0) is True


def test_create_application_success(sample_fair, sample_vendor):
    """Проверка успешного создания заявки."""
    applications = []
    app = create_application(
        applications=applications,
        vendor=sample_vendor,
        fair=sample_fair,
        requested_space=10.0,
        is_first_time=True,
        is_paid=True,
    )
    assert len(applications) == 1
    assert app["id"] == 1
    assert app["requested_space"] == 10.0
    assert "Одобрена" in app["status"]


def test_create_application_exceeds_space(sample_fair, sample_vendor):
    """Проверка вызова исключения при превышении лимита площади."""
    applications = []
    with pytest.raises(ValueError) as excinfo:
        create_application(
            applications=applications,
            vendor=sample_vendor,
            fair=sample_fair,
            requested_space=100.0,  # Лимит ярмарки 50 кв.м
            is_first_time=False,
            is_paid=True,
        )
    assert "Недостаточно места" in str(excinfo.value)


def test_cancel_application():
    """Проверка отмены заявки."""
    applications = [
        {"id": 1, "status": "Одобрена"},
        {"id": 2, "status": "На рассмотрении"},
    ]
    assert cancel_application(applications, 1) is True
    assert "Отменена" in applications[0]["status"]
    assert cancel_application(applications, 99) is False


def test_get_occupied_space():
    """Проверка расчета занятой площади."""
    applications = [
        {"id": 1, "fair_id": 1, "requested_space": 12.5, "status": "Одобрена"},
        {"id": 2, "fair_id": 1, "requested_space": 7.5, "status": "Одобрена"},
        {"id": 3, "fair_id": 1, "requested_space": 10.0, "status": "Отменена"},
        {"id": 4, "fair_id": 2, "requested_space": 15.0, "status": "Одобрена"},
    ]
    assert get_occupied_space(applications, 1) == 20.0
    assert get_occupied_space(applications, 2) == 15.0


def test_fair_statistics(sample_fair):
    """Проверка сводной статистики площадки."""
    applications = [
        {
            "id": 1,
            "fair_id": 1,
            "requested_space": 10.0,
            "fee": 10000.0,
            "status": "Одобрена",
        },
        {
            "id": 2,
            "fair_id": 1,
            "requested_space": 20.0,
            "fee": 20000.0,
            "status": "Одобрена",
        },
        {
            "id": 3,
            "fair_id": 1,
            "requested_space": 5.0,
            "fee": 5000.0,
            "status": "Отменена",
        },
    ]
    stats = calculate_fair_statistics(applications, sample_fair)
    assert stats["total_space"] == 50.0
    assert stats["occupied_space"] == 30.0
    assert stats["free_space"] == 20.0
    assert stats["approved_count"] == 2
    assert stats["total_revenue"] == 30000.0
