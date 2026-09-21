"""Модульные тесты для проверки функций ПР1 (Сервис регистрации продавцов)."""

from datetime import date
from main import (
    validate_vendor_data,
    calculate_participation_fee,
    determine_application_status,
    generate_registration_card,
)


def test_validate_vendor_data_success():
    """Проверка успешной валидации корректных данных."""
    assert validate_vendor_data("ИП Иванов", "770123456789", True) is True
    assert validate_vendor_data("ООО Ремесла", "7701234567", True) is True


def test_validate_vendor_data_invalid():
    """Проверка выявления некорректных данных."""
    # Пустое имя
    assert validate_vendor_data("", "770123456789", True) is False
    # Неверный ИНН (буквы)
    assert validate_vendor_data("ИП Иванов", "77012345678A", True) is False
    # Неверная длина ИНН (9 цифр)
    assert validate_vendor_data("ИП Иванов", "123456789", True) is False
    # Отсутствуют документы
    assert validate_vendor_data("ИП Иванов", "770123456789", False) is False


def test_calculate_participation_fee():
    """Проверка расчета стоимости участия с учетом категорий и скидок."""
    # Ремесла: 1000 руб/кв.м * 10 кв.м * 1.0 = 10000 руб (без скидки)
    fee_crafts = calculate_participation_fee(
        1000.0, "Ремесленные изделия", 10.0, False
    )
    assert fee_crafts == 10000.0

    # Ремесла со скидкой новичка (15%): 10000 - 1500 = 8500 руб
    fee_newcomer = calculate_participation_fee(1000.0, "Ремесла", 10.0, True)
    assert fee_newcomer == 8500.0

    # Продукты питания: 1000 * 10 * 1.3 = 13000 руб
    fee_food = calculate_participation_fee(
        1000.0, "Продукты питания", 10.0, False
    )
    assert fee_food == 13000.0


def test_determine_application_status():
    """Проверка определения статусов заявки."""
    # Все условия выполнены -> одобрено
    status_ok = determine_application_status(True, 10.0, 50.0, True)
    assert "Одобрена" in status_ok

    # Ошибки в документах -> отклонено
    status_doc_err = determine_application_status(False, 10.0, 50.0, True)
    assert "ошибки" in status_doc_err.lower()

    # Запрошено больше доступного места -> отклонено
    status_space_err = determine_application_status(True, 60.0, 50.0, True)
    assert "недостаточно" in status_space_err.lower()

    # Не оплачено -> ожидает оплаты
    status_wait_pay = determine_application_status(True, 10.0, 50.0, False)
    assert "ожидается оплата" in status_wait_pay.lower()


def test_generate_registration_card():
    """Проверка генерации карточки участника."""
    card = generate_registration_card(
        app_id=1,
        vendor_name="Мастерская",
        inn="770123456789",
        fair_name="Ярмарка",
        fair_date_value=date(2026, 10, 15),
        category="Ремесла",
        space_sqm=10.0,
        total_fee=8500.0,
        status="Одобрена",
    )
    assert "КАРТОЧКА РЕГИСТРАЦИИ" in card
    assert "770123456789" in card
    assert "15.10.2026" in card
