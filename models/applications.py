"""Модуль модели заявки (Application) и операций над заявками.

Определяет класс Application, связывающий объект продавца (Vendor) с
объектом ярмарки (Fair), реализует проверку доступности площадей,
расчет сборов, отмену бронирований и генерацию карточек.
"""

from datetime import date, datetime
from typing import Any, Dict, List
from models.fairs import Fair
from models.vendors import Vendor


class Application:
    """Класс заявки на участие, связывающий продавца и мероприятие."""

    def __init__(
        self,
        application_id: int,
        vendor: Vendor,
        fair: Fair,
        requested_space: float,
        fee: float = 0.0,
        status: str = "",
        is_cancelled: bool = False,
    ) -> None:
        """Инициализирует заявку с прямыми ссылками на Vendor и Fair."""
        if application_id <= 0:
            raise ValueError("Идентификатор заявки должен быть положительным.")
        if requested_space <= 0:
            raise ValueError(
                "Площадь торгового места должна быть положительным числом."
            )

        self.id = application_id
        self.vendor = vendor
        self.fair = fair
        self.requested_space = float(requested_space)
        self.fee = float(fee)
        self.status = status.strip()
        self.is_cancelled = is_cancelled

        if not self.status:
            self.status = "На рассмотрении"

    def cancel(self) -> None:
        """Отменяет заявку, освобождая торговое пространство ярмарки."""
        self.is_cancelled = True
        self.status = "Отменена: бронирование отозвано участником"

    def calculate_fee(self, is_first_time: bool = False) -> float:
        """Рассчитывает стоимость участия с учетом категории и скидки."""
        coeff = self.vendor.get_category_coefficient()
        initial_fee = self.fair.base_rate * self.requested_space * coeff

        if is_first_time:
            final_fee = initial_fee * 0.85
        else:
            final_fee = initial_fee

        self.fee = round(final_fee, 2)
        return self.fee

    def generate_card(self) -> str:
        """Формирует текстовую регистрационную карточку участника ярмарки."""
        card_border = "=" * 65
        fair_date_str = self.fair.date
        try:
            d_obj = datetime.strptime(fair_date_str, "%Y-%m-%d").date()
            formatted_date = d_obj.strftime("%d.%m.%Y")
        except ValueError:
            formatted_date = fair_date_str

        fee_str = f"{self.fee:,.2f} руб.".replace(",", " ")

        return (
            f"\n{card_border}\n"
            f"          КАРТОЧКА РЕГИСТРАЦИИ УЧАСТНИКА ЯРМАРКИ (ПР3)\n"
            f"{card_border}\n"
            f"Номер заявки:           #{self.id}\n"
            f"Участник (бренд):       {self.vendor.name}\n"
            f"ИНН налогоплательщика:  {self.vendor.inn}\n"
            f"Категория товаров:      {self.vendor.category}\n"
            f"Название ярмарки:       {self.fair.name}\n"
            f"Дата проведения:        {formatted_date}\n"
            f"Площадка проведения:    {self.fair.location}\n"
            f"Забронированная площадь:{self.requested_space:.1f} кв.м\n"
            f"Итоговый сбор за место: {fee_str}\n"
            f"Текущий статус заявки:  {self.status}\n"
            f"{card_border}\n"
        )

    def __getitem__(self, item: str) -> Any:
        """Поддержка доступа по ключу для обратной совместимости."""
        if item == "vendor_id":
            return self.vendor.id
        if item == "fair_id":
            return self.fair.id
        if hasattr(self, item):
            return getattr(self, item)
        raise KeyError(item)

    def __contains__(self, item: str) -> bool:
        """Проверка наличия ключа или атрибута."""
        if item in ("vendor_id", "fair_id"):
            return True
        return hasattr(self, item)

    def __str__(self) -> str:
        """Возвращает строковое представление заявки."""
        state = "ОТМЕНЕНА" if self.is_cancelled else "АКТИВНА"
        return (
            f"Заявка #{self.id} [{state}]: «{self.vendor.name}» -> "
            f"«{self.fair.name}» ({self.requested_space:.1f} кв.м, "
            f"{self.fee:,.2f} руб., статус: '{self.status}')"
        )

    def to_dict(self) -> Dict[str, Any]:
        """Преобразует объект заявки в словарь для сохранения в JSON."""
        return {
            "id": self.id,
            "vendor_id": self.vendor.id,
            "fair_id": self.fair.id,
            "requested_space": self.requested_space,
            "fee": self.fee,
            "status": self.status,
            "is_cancelled": self.is_cancelled,
        }

    @classmethod
    def from_dict(
        cls, data: Dict[str, Any], vendor: Vendor, fair: Fair
    ) -> "Application":
        """Создает объект Application, связывая его с Vendor и Fair."""
        is_cancelled = data.get("is_cancelled", False)
        status = data.get("status", "")
        if "Отменена" in status:
            is_cancelled = True

        return cls(
            application_id=data["id"],
            vendor=vendor,
            fair=fair,
            requested_space=float(data["requested_space"]),
            fee=float(data.get("fee", 0.0)),
            status=status,
            is_cancelled=is_cancelled,
        )


# ---------------------------------------------------------------------------
# Функции обработки коллекций объектов Application
# ---------------------------------------------------------------------------

def get_occupied_space(
    applications: List[Any], fair_id: int
) -> float:
    """Вычисляет суммарную занятую площадь на заданной ярмарке."""
    total_occupied = 0.0
    for app in applications:
        f_id = (
            app.fair.id if hasattr(app, "fair") else app.get("fair_id")
        )
        if f_id != fair_id:
            continue
        is_canc = (
            app.is_cancelled
            if hasattr(app, "is_cancelled")
            else app.get("is_cancelled", False)
        )
        status = (
            app.status if hasattr(app, "status") else app.get("status", "")
        )
        if is_canc or "Отклонена" in status or "Отменена" in status:
            continue
        req_space = (
            app.requested_space
            if hasattr(app, "requested_space")
            else app.get("requested_space", 0.0)
        )
        total_occupied += req_space
    return round(total_occupied, 2)


def is_space_available(
    applications: List[Any],
    fair: Any,
    requested_space: float,
) -> bool:
    """Проверяет доступность требуемой площади на ярмарке."""
    fair_id = fair.id if hasattr(fair, "id") else fair.get("id")
    total_space = float(
        fair.total_space
        if hasattr(fair, "total_space")
        else fair.get("total_space", 0.0)
    )
    occupied = get_occupied_space(applications, fair_id)
    if hasattr(fair, "is_space_available"):
        return fair.is_space_available(requested_space, occupied)
    if requested_space <= 0:
        return False
    return (occupied + requested_space) <= total_space


def create_application(
    applications: List[Any],
    vendor: Any,
    fair: Any,
    requested_space: float,
    is_first_time: bool = False,
    is_paid: bool = True,
) -> Application:
    """Создает и добавляет заявку в коллекцию с валидацией лимитов."""
    if requested_space <= 0:
        raise ValueError(
            "Площадь торгового места должна быть положительным числом."
        )

    fair_id = fair.id if hasattr(fair, "id") else fair.get("id")
    fair_name = fair.name if hasattr(fair, "name") else fair.get("name", "")
    fair_base_rate = float(
        fair.base_rate
        if hasattr(fair, "base_rate")
        else fair.get("base_rate", 1000.0)
    )
    fair_total_space = float(
        fair.total_space
        if hasattr(fair, "total_space")
        else fair.get("total_space", 0.0)
    )

    occupied = get_occupied_space(applications, fair_id)
    available_space = max(0.0, round(fair_total_space - occupied, 2))

    if requested_space > available_space:
        raise ValueError(
            f"Недостаточно места на ярмарке '{fair_name}'. "
            f"Доступно: {available_space:.1f} кв.м, "
            f"запрошено: {requested_space:.1f} кв.м."
        )

    # Приведение к объектам Fair и Vendor при необходимости
    if isinstance(fair, dict):
        fair_obj = Fair(
            fair_id=fair_id,
            name=fair_name,
            location=fair.get("location", "Площадка"),
            date=fair.get("date", "2026-10-01"),
            base_rate=fair_base_rate,
            total_space=fair_total_space,
        )
    else:
        fair_obj = fair

    if isinstance(vendor, dict):
        vendor_obj = Vendor.from_dict(vendor)
    else:
        vendor_obj = vendor

    next_id = max(
        (
            app.id if hasattr(app, "id") else app.get("id", 0)
            for app in applications
        ),
        default=0,
    ) + 1

    app = Application(
        application_id=next_id,
        vendor=vendor_obj,
        fair=fair_obj,
        requested_space=requested_space,
    )
    app.calculate_fee(is_first_time=is_first_time)

    # Определение статуса
    if not vendor_obj.has_documents or not validate_vendor_data(
        vendor_obj.name, vendor_obj.inn, vendor_obj.has_documents
    ):
        app.status = (
            "Отклонена: ошибки в регистрационных данных или документах"
        )
    elif not is_paid:
        app.status = "Ожидает оплаты: документы согласованы, ожидается оплата"
    else:
        app.status = "Одобрена: регистрация подтверждена, стенд забронирован"

    applications.append(app)
    return app


def cancel_application(
    applications: List[Any], application_id: int
) -> bool:
    """Отменяет заявку по идентификатору, освобождая занятую площадь."""
    for app in applications:
        app_id = app.id if hasattr(app, "id") else app.get("id")
        if app_id == application_id:
            if hasattr(app, "cancel"):
                app.cancel()
            else:
                app["is_cancelled"] = True
                app["status"] = "Отменена: бронирование отозвано участником"
            return True
    return False


def calculate_fair_statistics(
    applications: List[Any], fair: Any
) -> Dict[str, Any]:
    """Вычисляет сводную статистику по торговой площадке ярмарки."""
    fair_id = fair.id if hasattr(fair, "id") else fair.get("id")
    fair_name = fair.name if hasattr(fair, "name") else fair.get("name", "")
    total_space = float(
        fair.total_space
        if hasattr(fair, "total_space")
        else fair.get("total_space", 0.0)
    )

    fair_apps = [
        app for app in applications
        if (
            app.fair.id if hasattr(app, "fair") else app.get("fair_id")
        ) == fair_id
    ]
    occupied = get_occupied_space(applications, fair_id)
    free_space = max(0.0, round(total_space - occupied, 2))

    approved_apps = [
        app for app in fair_apps
        if not (
            app.is_cancelled
            if hasattr(app, "is_cancelled")
            else app.get("is_cancelled", False)
        )
        and "Одобрена" in (
            app.status if hasattr(app, "status") else app.get("status", "")
        )
    ]
    total_revenue = sum(
        (app.fee if hasattr(app, "fee") else app.get("fee", 0.0))
        for app in approved_apps
    )

    return {
        "fair_name": fair_name,
        "total_space": total_space,
        "occupied_space": occupied,
        "free_space": free_space,
        "occupancy_rate": round(
            (occupied / total_space * 100) if total_space > 0 else 0, 1
        ),
        "total_applications": len(fair_apps),
        "approved_count": len(approved_apps),
        "total_revenue": round(total_revenue, 2),
    }


# ---------------------------------------------------------------------------
# Функции обратной совместимости (из ПР1 и ПР2)
# ---------------------------------------------------------------------------

def validate_vendor_data(
    vendor_name: str, inn: str, has_documents: bool
) -> bool:
    """Проверяет корректность регистрационных данных продавца."""
    clean_name = vendor_name.strip()
    is_name_valid = len(clean_name) > 0
    clean_inn = inn.strip()
    is_inn_valid = clean_inn.isdigit() and (
        len(clean_inn) == 10 or len(clean_inn) == 12
    )
    return is_name_valid and is_inn_valid and has_documents


def calculate_participation_fee(
    base_rate_per_sqm: float,
    category: str,
    space_sqm: float,
    is_first_time: bool,
) -> float:
    """Рассчитывает стоимость аренды торгового места на ярмарке."""
    norm_cat = category.strip().lower()
    if norm_cat in ("ремесла", "ремесленные изделия"):
        coeff = 1.0
    elif norm_cat in ("продукты питания", "фермерские товары"):
        coeff = 1.3
    elif norm_cat == "сувениры":
        coeff = 1.1
    else:
        coeff = 1.2

    initial_fee = base_rate_per_sqm * space_sqm * coeff
    return round(initial_fee * 0.85 if is_first_time else initial_fee, 2)


def determine_application_status(
    is_valid_data: bool,
    space_sqm: float,
    available_space_sqm: float,
    is_fee_paid: bool,
) -> str:
    """Определяет статус рассмотрения заявки."""
    if not is_valid_data:
        return "Отклонена: ошибки в регистрационных данных или документах"
    if space_sqm > available_space_sqm:
        return "Отклонена: недостаточно свободной торговой площади на ярмарке"
    if not is_fee_paid:
        return "Ожидает оплаты: документы согласованы, ожидается оплата"
    return "Одобрена: регистрация подтверждена, стенд забронирован"


def generate_registration_card(
    app_id: int,
    vendor_name: str,
    inn: str,
    fair_name: str,
    fair_date_value: date,
    category: str,
    space_sqm: float,
    total_fee: float,
    status: str,
) -> str:
    """Генерирует карточку регистрации участника."""
    card_border = "=" * 65
    date_str = fair_date_value.strftime("%d.%m.%Y")
    fee_str = f"{total_fee:,.2f} руб.".replace(",", " ")

    return (
        f"\n{card_border}\n"
        f"          КАРТОЧКА РЕГИСТРАЦИИ УЧАСТНИКА ЯРМАРКИ\n"
        f"{card_border}\n"
        f"Номер заявки:           #{app_id}\n"
        f"Участник (бренд):       {vendor_name}\n"
        f"ИНН налогоплательщика:  {inn}\n"
        f"Категория товаров:      {category}\n"
        f"Название ярмарки:       {fair_name}\n"
        f"Дата проведения:        {date_str}\n"
        f"Забронированная площадь:{space_sqm:.1f} кв.м\n"
        f"Итоговый сбор за место: {fee_str}\n"
        f"Текущий статус заявки:  {status}\n"
        f"{card_border}\n"
    )
