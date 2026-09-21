"""Модуль управления реестром продавцов и участников ярмарок.

Реэкспортирует классы и функции из models.vendors для обеспечения
обратной совместимости с кодом ПР1 и ПР2, а также поддержки ООП ПР3.
"""

from models.vendors import (
    CraftVendor,
    FoodVendor,
    SouvenirVendor,
    Vendor,
    add_vendor,
    filter_vendors_by_category,
    find_vendor_by_id,
    find_vendor_by_name,
    get_vendor_by_id,
    sort_vendors,
    validate_inn,
)

__all__ = [
    "Vendor",
    "CraftVendor",
    "FoodVendor",
    "SouvenirVendor",
    "validate_inn",
    "add_vendor",
    "get_vendor_by_id",
    "find_vendor_by_id",
    "find_vendor_by_name",
    "filter_vendors_by_category",
    "sort_vendors",
]
