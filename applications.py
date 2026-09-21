"""Модуль управления заявками на участие в ярмарках.

Объединяет функционал первичного этапа (ПР1) с операциями над коллекциями,
проверкой доступности торговых площадей, расчетом сборов и аналитикой ярмарок.
"""

from datetime import date
from typing import Dict, List


def validate_vendor_data(
    vendor_name: str, inn: str, has_documents: bool
) -> bool:
    """Проверяет корректность регистрационных данных продавца (из ПР1).

    Параметры:
        vendor_name: наименование бренда или ФИО мастера.
        inn: индивидуальный номер налогоплательщика.
        has_documents: наличие обязательного пакета документов.

    Возвращает:
        True, если данные валидны, иначе False.
    """
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
    """Рассчитывает стоимость аренды торгового места на ярмарке (из ПР1).

    Параметры:
        base_rate_per_sqm: базовая арендная ставка за 1 кв.м (руб.).
        category: товарная категория продукции.
        space_sqm: запрашиваемая площадь стенда.
        is_first_time: флаг первого участия (скидка 15%).

    Возвращает:
        Итоговая стоимость аренды стенда в рублях.
    """
    norm_cat = category.strip().lower()
    if norm_cat in ("ремесла", "ремесленные изделия"):
        category_coefficient = 1.0
    elif norm_cat in ("продукты питания", "фермерские товары"):
        category_coefficient = 1.3
    elif norm_cat == "сувениры":
        category_coefficient = 1.1
    else:
        category_coefficient = 1.2

    initial_fee = base_rate_per_sqm * space_sqm * category_coefficient

    if is_first_time:
        final_fee = initial_fee * 0.85
    else:
        final_fee = initial_fee

    return round(final_fee, 2)


def determine_application_status(
    is_data_valid: bool,
    requested_space: float,
    available_space: float,
    is_fee_paid: bool,
) -> str:
    """Определяет текущий статус рассмотрения заявки (из ПР1).

    Параметры:
        is_data_valid: результат проверки регистрационных документов.
        requested_space: запрашиваемая площадь (кв. м).
        available_space: остаток свободной площади ярмарки.
        is_fee_paid: факт оплаты регистрационного сбора.

    Возвращает:
        Текстовый вердикт о состоянии заявки.
    """
    if not is_data_valid:
        return "Отклонена: ошибки в регистрационных данных или документах"
    if requested_space <= 0:
        return "Отклонена: некорректно указана площадь торгового места"
    if requested_space > available_space:
        return "Отклонена: на ярмарке недостаточно свободной торговой площади"
    if not is_fee_paid:
        return "На рассмотрении: ожидается оплата регистрационного сбора"
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
    """Формирует текстовую карточку участника ярмарки (из ПР1).

    Возвращает:
        Отформатированный многострочный текст карточки заявки.
    """
    border = "=" * 65
    date_str = fair_date_value.strftime("%d.%m.%Y")
    fee_str = f"{total_fee:,.2f}".replace(",", " ") + " руб."

    return (
        f"\n{border}\n"
        f"          КАРТОЧКА РЕГИСТРАЦИИ УЧАСТНИКА ЯРМАРКИ #{app_id:04d}\n"
        f"{border}\n"
        f"  Ярмарка:             {fair_name}\n"
        f"  Дата проведения:     {date_str}\n"
        f"  Продавец (бренд):    {vendor_name}\n"
        f"  ИНН участника:       {inn}\n"
        f"  Категория продукции: {category}\n"
        f"  Площадь стенда:      {space_sqm:.1f} кв. м\n"
        f"  Стоимость участия:   {fee_str}\n"
        f"  Текущий статус:      {status}\n"
        f"{border}\n"
    )


# ---------------------------------------------------------------------------
# Функции ПР2: работа с коллекциями, лимитами площадей и аналитикой ярмарок
# ---------------------------------------------------------------------------

def get_occupied_space(applications: List[Dict], fair_id: int) -> float:
    """Вычисляет суммарную занятую площадь на заданной ярмарке.

    Учитываются активные заявки участников ярмарки.

    Параметры:
        applications: список всех зарегистрированных заявок.
        fair_id: идентификатор ярмарки.

    Возвращает:
        Сумма занятых квадратных метров.
    """
    total_occupied = sum(
        app.get("requested_space", 0.0)
        for app in applications
        if app.get("fair_id") == fair_id
        and "Отклонена" not in app.get("status", "")
        and "Отменена" not in app.get("status", "")
    )
    return round(total_occupied, 2)


def is_space_available(
    applications: List[Dict],
    fair: Dict,
    requested_space: float,
) -> bool:
    """Проверяет, достаточно ли свободной площади на ярмарке для новой заявки.

    Параметры:
        applications: список существующих заявок.
        fair: словарь параметров целевой ярмарки.
        requested_space: требуемая площадь (кв. м).

    Возвращает:
        True, если площадь доступна, иначе False.
    """
    if requested_space <= 0:
        return False

    occupied = get_occupied_space(applications, fair["id"])
    available = fair.get("total_space", 0.0) - occupied
    return requested_space <= available


def create_application(
    applications: List[Dict],
    vendor: Dict,
    fair: Dict,
    requested_space: float,
    is_first_time: bool,
    is_paid: bool,
) -> Dict:
    """Создает и регистрирует новую заявку продавца на выбранную ярмарку.

    Параметры:
        applications: список зарегистрированных заявок.
        vendor: данные продавца.
        fair: данные ярмарки.
        requested_space: запрашиваемая площадь торгового стенда.
        is_first_time: флаг первого участия.
        is_paid: факт внесения регистрационного сбора.

    Возвращает:
        Словарь созданной заявки.

    Исключения:
        ValueError: если площадь некорректна или превышает доступный лимит.
    """
    if requested_space <= 0:
        raise ValueError(
            "Площадь торгового места должна быть положительным числом."
        )

    occupied = get_occupied_space(applications, fair["id"])
    available_space = fair.get("total_space", 0.0) - occupied

    if requested_space > available_space:
        raise ValueError(
            f"Недостаточно места на ярмарке '{fair['name']}'. "
            f"Доступно: {available_space:.1f} кв.м, "
            f"запрошено: {requested_space:.1f} кв.м."
        )

    # Проверка документов продавца
    is_valid = validate_vendor_data(
        vendor_name=vendor.get("name", ""),
        inn=vendor.get("inn", ""),
        has_documents=vendor.get("has_documents", False),
    )

    fee = calculate_participation_fee(
        base_rate_per_sqm=fair.get("base_rate", 1500.0),
        category=vendor.get("category", "Ремесла"),
        space_sqm=requested_space,
        is_first_time=is_first_time,
    )

    status = determine_application_status(
        is_data_valid=is_valid,
        requested_space=requested_space,
        available_space=available_space,
        is_fee_paid=is_paid,
    )

    next_id = max((app["id"] for app in applications), default=0) + 1

    new_app = {
        "id": next_id,
        "fair_id": fair["id"],
        "vendor_id": vendor["id"],
        "requested_space": requested_space,
        "is_first_time": is_first_time,
        "fee": fee,
        "status": status,
        "is_paid": is_paid,
    }
    applications.append(new_app)
    return new_app


def cancel_application(applications: List[Dict], application_id: int) -> bool:
    """Отменяет заявку на участие по ее идентификатору.

    Параметры:
        applications: список заявок.
        application_id: идентификатор заявки.

    Возвращает:
        True при успешной отмене, False если заявка не найдена.
    """
    for app in applications:
        if app.get("id") == application_id:
            app["status"] = "Отменена: бронирование отозвано участником"
            return True
    return False


def get_applications_by_fair(
    applications: List[Dict], fair_id: int
) -> List[Dict]:
    """Возвращает список заявок для конкретной ярмарки."""
    return [app for app in applications if app.get("fair_id") == fair_id]


def get_applications_by_vendor(
    applications: List[Dict], vendor_id: int
) -> List[Dict]:
    """Возвращает список заявок конкретного продавца."""
    return [app for app in applications if app.get("vendor_id") == vendor_id]


def calculate_fair_statistics(applications: List[Dict], fair: Dict) -> Dict:
    """Вычисляет сводную статистику по торговой площадке ярмарки.

    Демонстрирует агрегацию коллекций и расчет показателей.

    Параметры:
        applications: список всех заявок.
        fair: параметры ярмарки.

    Возвращает:
        Словарь аналитических метрик.
    """
    fair_apps = get_applications_by_fair(applications, fair["id"])
    occupied = get_occupied_space(applications, fair["id"])
    total_space = fair.get("total_space", 0.0)
    free_space = max(0.0, total_space - occupied)

    approved_apps = [
        app for app in fair_apps if "Одобрена" in app.get("status", "")
    ]
    total_revenue = sum(app.get("fee", 0.0) for app in approved_apps)

    return {
        "fair_name": fair.get("name", ""),
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
