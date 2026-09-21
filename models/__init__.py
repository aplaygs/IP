"""Пакет моделей предметной области «Сервис регистрации продавцов на ярмарку».

Экспортирует основные классы: Fair, Vendor (и подклассы CraftVendor,
FoodVendor, SouvenirVendor) и Application.
"""

from .applications import Application
from .fairs import Fair
from .vendors import CraftVendor, FoodVendor, SouvenirVendor, Vendor

__all__ = [
    "Fair",
    "Vendor",
    "CraftVendor",
    "FoodVendor",
    "SouvenirVendor",
    "Application",
]
