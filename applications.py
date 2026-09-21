"""Модуль управления заявками на участие в ярмарках.

Реэкспортирует класс Application и сопутствующие функции обработки
заявок и аналитики из models.applications для обеспечения совместимости.
"""

from models.applications import (
    Application,
    calculate_fair_statistics,
    calculate_participation_fee,
    cancel_application,
    create_application,
    determine_application_status,
    generate_registration_card,
    get_occupied_space,
    is_space_available,
    validate_vendor_data,
)

__all__ = [
    "Application",
    "calculate_fair_statistics",
    "calculate_participation_fee",
    "cancel_application",
    "create_application",
    "determine_application_status",
    "generate_registration_card",
    "get_occupied_space",
    "is_space_available",
    "validate_vendor_data",
]
