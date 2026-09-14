"""Сервис регистрации продавцов на ярмарку (FairVendor).

Практическая работа № 1.
Дисциплина: Технологии разработки приложений на базе фреймворков.
Студент: Мишуков Владислав Романович, группа ЭФБО-11-24.

Данный модуль реализует базовый программный сценарий регистрации продавца
с использованием простых типов данных, условных конструкций и функций.
"""

from datetime import date


def validate_vendor_data(vendor_name: str, inn: str, has_documents: bool) -> bool:
    """Проверяет корректность регистрационных данных продавца.

    Параметры:
        vendor_name: наименование бренда или ФИО мастера.
        inn: индивидуальный номер налогоплательщика (строка из 10 или 12 цифр).
        has_documents: флаг наличия обязательных регистрационных документов.

    Возвращает:
        True, если данные валидны, иначе False.
    """
    # Проверка заполненности имени
    clean_name = vendor_name.strip()
    is_name_valid = len(clean_name) > 0

    # Проверка ИНН: должен содержать только цифры и иметь длину 10 или 12 знаков
    is_digits = inn.isdigit()
    inn_length = len(inn)
    is_inn_valid = is_digits and (inn_length == 10 or inn_length == 12)

    # Итоговая валидация с учетом документов
    is_valid = is_name_valid and is_inn_valid and has_documents

    if not is_name_valid:
        print("[Ошибка валидации]: наименование продавца не может быть пустым.")
    elif not is_inn_valid:
        print(f"[Ошибка валидации]: некорректный ИНН '{inn}'. Ожидается 10 или 12 цифр.")
    elif not has_documents:
        print("[Ошибка валидации]: отсутствует обязательный пакет документов.")
    else:
        print(f"[Успех]: реквизиты продавца '{clean_name}' успешно проверены.")

    return is_valid


def calculate_participation_fee(
    base_rate_per_sqm: float,
    category: str,
    space_sqm: float,
    is_first_time: bool,
) -> float:
    """Рассчитывает стоимость участия продавца на ярмарке.

    Параметры:
        base_rate_per_sqm: базовая ставка аренды за 1 кв. метр (руб.).
        category: категория товаров ('Ремесла', 'Продукты питания', 'Сувениры').
        space_sqm: запрашиваемая площадь стенда (кв. метры).
        is_first_time: признак первого участия (дает скидку 15%).

    Возвращает:
        Итоговая стоимость аренды торгового места в рублях.
    """
    normalized_category = category.strip().lower()

    # Определение коэффициента категории
    if normalized_category == "ремесла" or normalized_category == "ремесленные изделия":
        category_coefficient = 1.0
    elif normalized_category == "продукты питания" or normalized_category == "фермерские товары":
        # Повышенный коэффициент из-за требований к санитарному контролю и электропитанию
        category_coefficient = 1.3
    elif normalized_category == "сувениры":
        category_coefficient = 1.1
    else:
        category_coefficient = 1.2

    initial_fee = base_rate_per_sqm * space_sqm * category_coefficient

    # Расчет скидки для новых участников
    if is_first_time:
        discount_rate = 0.15
        discount_amount = initial_fee * discount_rate
        final_fee = initial_fee - discount_amount
    else:
        final_fee = initial_fee

    return round(final_fee, 2)


def determine_application_status(
    is_data_valid: bool,
    requested_space: float,
    available_space: float,
    is_fee_paid: bool,
) -> str:
    """Определяет текущий статус заявки на участие.

    Параметры:
        is_data_valid: результат проверки регистрационных данных.
        requested_space: запрашиваемая площадь (кв. м).
        available_space: оставшаяся доступная площадь ярмарки (кв. м).
        is_fee_paid: факт оплаты регистрационного взноса.

    Возвращает:
        Строку с текущим статусом заявки.
    """
    if not is_data_valid:
        return "Отклонена: ошибки в регистрационных данных или документах"
    elif requested_space <= 0:
        return "Отклонена: некорректно указана площадь торгового места"
    elif requested_space > available_space:
        return "Отклонена: на ярмарке недостаточно свободной торговой площади"
    elif not is_fee_paid:
        return "На рассмотрении: ожидается оплата регистрационного сбора"
    else:
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
    """Формирует форматированную текстовую карточку заявки на регистрацию.

    Возвращает:
        Многострочную строку с информацией о заявке.
    """
    card_border = "=" * 65
    formatted_date = fair_date_value.strftime("%d.%m.%Y")
    formatted_fee = f"{total_fee:,.2f} руб.".replace(",", " ")

    card_text = (
        f"\n{card_border}\n"
        f"          КАРТОЧКА РЕГИСТРАЦИИ УЧАСТНИКА ЯРМАРКИ #{app_id:04d}\n"
        f"{card_border}\n"
        f"  Ярмарка:             {fair_name}\n"
        f"  Дата проведения:     {formatted_date}\n"
        f"  Продавец (бренд):    {vendor_name}\n"
        f"  ИНН участника:       {inn}\n"
        f"  Категория продукции: {category}\n"
        f"  Площадь стенда:      {space_sqm:.1f} кв. м\n"
        f"  Стоимость участия:   {formatted_fee}\n"
        f"  Текущий статус:      {status}\n"
        f"{card_border}\n"
    )
    return card_text


def main() -> None:
    """Главный сценарий первичной обработки заявки продавца."""
    print("=================================================================")
    print(" Сервис регистрации продавцов на ярмарку (FairVendor) — ПР1")
    print(" Студент: Мишуков В. Р. | Группа: ЭФБО-11-24")
    print("=================================================================\n")

    # Исходные параметры ярмарки
    fair_title = "Осенняя ремесленная ярмарка Москвы 2026"
    fair_event_date = date(2026, 10, 15)
    base_rate = 1500.0  # руб. за 1 кв. м
    available_fair_space = 150.0  # кв. м доступно

    # Данные поступающей заявки продавца
    application_id = 101
    vendor_title = "Мастерская керамики «Глиняная сказка»"
    vendor_inn = "770198765432"
    has_cert_documents = True
    product_category = "Ремесленные изделия"
    requested_space = 12.0  # кв. м
    is_newcomer = True  # новичок ярмарки
    is_payment_received = True

    print(f"Поступила заявка #{application_id} от '{vendor_title}'...")

    # Шаг 1: Валидация данных продавца
    is_vendor_valid = validate_vendor_data(
        vendor_name=vendor_title,
        inn=vendor_inn,
        has_documents=has_cert_documents,
    )

    # Шаг 2: Расчет стоимости участия
    calculated_fee = calculate_participation_fee(
        base_rate_per_sqm=base_rate,
        category=product_category,
        space_sqm=requested_space,
        is_first_time=is_newcomer,
    )
    print(f"[Расчет]: стоимость аренды стенда составляет {calculated_fee:.2f} руб.")

    # Шаг 3: Определение вердикта по заявке
    verdict = determine_application_status(
        is_data_valid=is_vendor_valid,
        requested_space=requested_space,
        available_space=available_fair_space,
        is_fee_paid=is_payment_received,
    )
    print(f"[Решение]: {verdict}")

    # Шаг 4: Формирование официальной карточки
    registration_card = generate_registration_card(
        app_id=application_id,
        vendor_name=vendor_title,
        inn=vendor_inn,
        fair_name=fair_title,
        fair_date_value=fair_event_date,
        category=product_category,
        space_sqm=requested_space,
        total_fee=calculated_fee,
        status=verdict,
    )

    print(registration_card)


if __name__ == "__main__":
    main()
