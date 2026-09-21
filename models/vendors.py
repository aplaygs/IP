"""Модуль модели продавца (Vendor) и специализированных подклассов.

Определяет базовый класс Vendor, дочерние классы CraftVendor, FoodVendor,
SouvenirVendor, демонстрирующие наследование и полиморфизм тарифов,
а также операции над коллекциями объектов продавцов.
"""

from typing import Any, Dict, Generator, List, Optional


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


class Vendor:
    """Базовый класс продавца (участника ярмарочных мероприятий)."""

    def __init__(
        self,
        vendor_id: int,
        name: str,
        inn: str,
        category: str,
        has_documents: bool,
        experience_years: int = 0,
    ) -> None:
        """Инициализирует объект продавца с валидацией реквизитов."""
        if vendor_id <= 0:
            raise ValueError(
                "Идентификатор продавца должен быть положительным."
            )

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
            raise ValueError(
                "Стаж участия не может быть отрицательным числом."
            )

        self.id = vendor_id
        self.name = clean_name
        self.inn = inn.strip()
        self.category = category.strip()
        self.has_documents = has_documents
        self.experience_years = experience_years

    def get_category_coefficient(self) -> float:
        """Возвращает отраслевой тарифный коэффициент стоимости стенда."""
        norm_cat = self.category.strip().lower()
        if norm_cat in ("ремесла", "ремесленные изделия"):
            return 1.0
        elif norm_cat in ("продукты питания", "фермерские товары"):
            return 1.3
        elif norm_cat == "сувениры":
            return 1.1
        return 1.2

    def __getitem__(self, item: str) -> Any:
        """Поддержка доступа по ключу для обратной совместимости."""
        if hasattr(self, item):
            return getattr(self, item)
        raise KeyError(item)

    def __contains__(self, item: str) -> bool:
        """Проверка наличия атрибута как ключа словаря."""
        return hasattr(self, item)

    def __str__(self) -> str:
        """Возвращает строковое представление продавца."""
        docs_status = (
            "документы в порядке"
            if self.has_documents
            else "документы отсутствуют"
        )
        return (
            f"Продавец #{self.id}: «{self.name}» (ИНН: {self.inn}, "
            f"категория: {self.category}, стаж: {self.experience_years} лет, "
            f"{docs_status})"
        )

    def to_dict(self) -> Dict[str, Any]:
        """Преобразует объект продавца в словарь для сохранения в JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "inn": self.inn,
            "category": self.category,
            "has_documents": self.has_documents,
            "experience_years": self.experience_years,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Vendor":
        """Фабричный метод создания объекта Vendor из словаря данных."""
        norm_cat = data.get("category", "").strip().lower()
        if norm_cat in ("ремесла", "ремесленные изделия"):
            target_cls = CraftVendor
        elif norm_cat in ("продукты питания", "фермерские товары"):
            target_cls = FoodVendor
        elif norm_cat == "сувениры":
            target_cls = SouvenirVendor
        else:
            target_cls = cls

        return target_cls(
            vendor_id=data["id"],
            name=data["name"],
            inn=data["inn"],
            category=data.get("category", "Общая"),
            has_documents=data.get("has_documents", False),
            experience_years=data.get("experience_years", 0),
        )


class CraftVendor(Vendor):
    """Специализированный класс мастера-ремесленника (льготная ставка 1.0)."""

    def __init__(
        self,
        vendor_id: int,
        name: str,
        inn: str,
        has_documents: bool = True,
        experience_years: int = 0,
        category: str = "Ремесла",
    ) -> None:
        super().__init__(
            vendor_id=vendor_id,
            name=name,
            inn=inn,
            category=category,
            has_documents=has_documents,
            experience_years=experience_years,
        )

    def get_category_coefficient(self) -> float:
        """Полиморфное переопределение: фиксированный льготный тариф 1.0."""
        return 1.0

    def __str__(self) -> str:
        return f"[Ремесленник] {super().__str__()}"


class FoodVendor(Vendor):
    """Специализированный класс производителя продуктов питания (тариф 1.3)."""

    def __init__(
        self,
        vendor_id: int,
        name: str,
        inn: str,
        has_documents: bool = True,
        experience_years: int = 0,
        category: str = "Продукты питания",
    ) -> None:
        super().__init__(
            vendor_id=vendor_id,
            name=name,
            inn=inn,
            category=category,
            has_documents=has_documents,
            experience_years=experience_years,
        )

    def get_category_coefficient(self) -> float:
        """Полиморфное переопределение: повышенный санитарный тариф 1.3."""
        return 1.3

    def __str__(self) -> str:
        return f"[Фермер/Гастрономия] {super().__str__()}"


class SouvenirVendor(Vendor):
    """Специализированный класс сувенирной продукции (тариф 1.1)."""

    def __init__(
        self,
        vendor_id: int,
        name: str,
        inn: str,
        has_documents: bool = True,
        experience_years: int = 0,
        category: str = "Сувениры",
    ) -> None:
        super().__init__(
            vendor_id=vendor_id,
            name=name,
            inn=inn,
            category=category,
            has_documents=has_documents,
            experience_years=experience_years,
        )

    def get_category_coefficient(self) -> float:
        """Полиморфное переопределение: сувенирный тариф 1.1."""
        return 1.1

    def __str__(self) -> str:
        return f"[Сувениры] {super().__str__()}"


# ---------------------------------------------------------------------------
# Функции обработки коллекций объектов Vendor
# ---------------------------------------------------------------------------

def add_vendor(
    vendors: List[Any],
    name: str,
    inn: str,
    category: str,
    has_documents: bool,
    experience_years: int = 0,
) -> Any:
    """Добавляет нового продавца в коллекцию с контролем уникальности ИНН."""
    clean_inn = str(inn).strip()
    for existing in vendors:
        v_inn = (
            existing.inn if hasattr(existing, "inn") else existing.get("inn")
        )
        if v_inn == clean_inn:
            raise ValueError(
                f"Продавец с ИНН '{clean_inn}' уже зарегистрирован в системе."
            )

    next_id = max(
        (v.id if hasattr(v, "id") else v.get("id", 0) for v in vendors),
        default=0,
    ) + 1
    new_vendor = Vendor.from_dict({
        "id": next_id,
        "name": name,
        "inn": clean_inn,
        "category": category,
        "has_documents": has_documents,
        "experience_years": experience_years,
    })
    vendors.append(new_vendor)
    return new_vendor


def find_vendor_by_id(
    vendors: List[Any], vendor_id: int
) -> Optional[Any]:
    """Возвращает объект продавца по уникальному идентификатору."""
    for vendor in vendors:
        v_id = vendor.id if hasattr(vendor, "id") else vendor.get("id")
        if v_id == vendor_id:
            return vendor
    return None


get_vendor_by_id = find_vendor_by_id


def find_vendor_by_name(vendors: List[Any], query: str) -> List[Any]:
    """Поиск продавцов по подстроке наименования (регистронезависимо)."""
    search_query = query.strip().lower()
    if not search_query:
        return list(vendors)

    results = []
    for vendor in vendors:
        v_name = (
            vendor.name if hasattr(vendor, "name") else vendor.get("name", "")
        )
        if search_query in v_name.lower():
            results.append(vendor)
    return results


def filter_vendors_by_category(
    vendors: List[Any], category: str
) -> Generator[Any, None, None]:
    """Генератор поэлементного отбора продавцов заданной категории товаров."""
    normalized_target = category.strip().lower()
    for vendor in vendors:
        v_cat = (
            vendor.category
            if hasattr(vendor, "category")
            else vendor.get("category", "")
        )
        if v_cat.strip().lower() == normalized_target:
            yield vendor


def sort_vendors(
    vendors: List[Any],
    sort_by: str = "name",
    reverse: bool = False,
) -> List[Any]:
    """Сортирует продавцов с использованием анонимной lambda-функции."""
    if sort_by == "experience":
        key_function = lambda v: (  # noqa: E731
            v.experience_years
            if hasattr(v, "experience_years")
            else v.get("experience_years", 0)
        )
    elif sort_by == "id":
        key_function = lambda v: (  # noqa: E731
            v.id if hasattr(v, "id") else v.get("id", 0)
        )
    else:
        key_function = lambda v: (  # noqa: E731
            v.name.lower()
            if hasattr(v, "name")
            else v.get("name", "").lower()
        )

    return sorted(vendors, key=key_function, reverse=reverse)
