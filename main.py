"""Точка запуска приложения «Сервис регистрации продавцов на ярмарку».

Практическая работа № 3. Объектно-ориентированное программирование (ООП).
Дисциплина: Технологии разработки приложений на базе фреймворков.
Студент: Мишуков Владислав Романович, группа ЭФБО-11-24.

Объединяет модели Fair, Vendor, Application и хранилище данных storage
в консольный интерфейс с поддержкой интерактивного меню и
демонстрационного сценария объектно-ориентированной архитектуры.
"""

import sys
from typing import List

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
from models.fairs import Fair
from models.vendors import (
    CraftVendor,
    FoodVendor,
    SouvenirVendor,
    Vendor,
    add_vendor,
    filter_vendors_by_category,
    find_vendor_by_name,
    get_vendor_by_id,
    sort_vendors,
)
from storage import (
    load_applications,
    load_fairs,
    load_vendors,
    save_applications,
    save_vendors,
)
from utils import format_currency, input_float, input_int

__all__ = [
    "validate_vendor_data",
    "calculate_participation_fee",
    "determine_application_status",
    "generate_registration_card",
]


def print_header() -> None:
    """Выводит информационный заголовок системы."""
    border = "=" * 67
    print(f"\n{border}")
    print("   СЕРВИС РЕГИСТРАЦИИ ПРОДАВЦОВ НА ЯРМАРКУ (FAIRVENDOR) — ПР3")
    print("   Студент: Мишуков В. Р. | Учебная группа: ЭФБО-11-24")
    print(f"{border}\n")


def display_fairs(
    fairs: List[Fair], applications: List[Application]
) -> None:
    """Отображает список ярмарок с информацией о доступных площадях."""
    print("\n--- Список ярмарок ---")
    if not fairs:
        print("В системе нет зарегистрированных ярмарок.")
        return

    for fair in fairs:
        occupied = get_occupied_space(applications, fair.id)
        free = fair.get_free_space(occupied)
        rate_str = format_currency(fair.base_rate)
        print(f"[{fair.id}] {fair.name}")
        print(f"    Локация: {fair.location} | Дата: {fair.date}")
        print(
            f"    Ставка: {rate_str}/кв.м | "
            f"Площадь: всего {fair.total_space:.1f} кв.м "
            f"(занято: {occupied:.1f} кв.м, свободно: {free:.1f} кв.м)"
        )


def display_vendors(vendors: List[Vendor]) -> None:
    """Отображает список зарегистрированных объектов продавцов."""
    print("\n--- Список зарегистрированных продавцов ---")
    if not vendors:
        print("Список продавцов пуст.")
        return

    for vendor in vendors:
        docs_status = (
            "Документы проверены"
            if vendor.has_documents
            else "Документы отсутствуют"
        )
        coeff = vendor.get_category_coefficient()
        print(f"[{vendor.id}] {vendor.name} (ИНН: {vendor.inn})")
        print(
            f"    Категория: {vendor.category} (тариф x{coeff:.1f}) | "
            f"Стаж: {vendor.experience_years} лет | {docs_status}"
        )


def display_applications(applications: List[Application]) -> None:
    """Отображает реестр поданных заявок на участие в ярмарках."""
    print("\n--- Реестр заявок на участие в ярмарках ---")
    if not applications:
        print("Заявок пока нет.")
        return

    for app in applications:
        fee_str = format_currency(app.fee)
        state_tag = "[ОТМЕНЕНА]" if app.is_cancelled else "[АКТИВНА]"
        print(
            f"Заявка #{app.id} {state_tag}: "
            f"«{app.vendor.name}» -> «{app.fair.name}»"
        )
        print(
            f"    Стенд: {app.requested_space:.1f} кв.м | "
            f"Сбор: {fee_str} | Статус: {app.status}"
        )


def handle_add_vendor(vendors: List[Vendor]) -> None:
    """Обрабатывает пользовательский ввод для добавления продавца."""
    print("\n--- Регистрация нового продавца ---")
    name = input("Введите наименование бренда или ФИО мастера: ").strip()
    inn = input("Введите ИНН (10 или 12 цифр): ").strip()
    category = input(
        "Введите категорию товаров (Ремесла / Продукты питания / Сувениры): "
    ).strip()
    experience = input_int(
        "Введите стаж участия в ярмарках (в годах): ", min_value=0
    )
    has_docs_input = input(
        "Имеются ли обязательные документы? (да/нет): "
    ).strip().lower()
    has_documents = has_docs_input in ("да", "yes", "+", "y", "1")

    try:
        new_vendor = add_vendor(
            vendors=vendors,
            name=name,
            inn=inn,
            category=category,
            has_documents=has_documents,
            experience_years=experience,
        )
        print(
            f"[Успех]: продавец «{new_vendor.name}» "
            f"успешно зарегистрирован с ID {new_vendor.id}."
        )
    except ValueError as err:
        print(f"[Ошибка валидации]: {err}")


def handle_create_application(
    applications: List[Application],
    vendors: List[Vendor],
    fairs: List[Fair],
) -> None:
    """Обрабатывает создание и регистрацию новой заявки."""
    print("\n--- Подача заявки на участие в ярмарке ---")
    display_vendors(vendors)
    vendor_id = input_int("\nВыберите ID продавца: ", min_value=1)
    vendor = get_vendor_by_id(vendors, vendor_id)
    if not vendor:
        print("[Ошибка]: продавец с указанным ID не найден.")
        return

    display_fairs(fairs, applications)
    fair_id = input_int("\nВыберите ID ярмарки: ", min_value=1)
    fair = next((f for f in fairs if f.id == fair_id), None)
    if not fair:
        print("[Ошибка]: ярмарка с указанным ID не найдена.")
        return

    requested_space = input_float(
        "Введите требуемую площадь стенда (кв. м): ", min_value=0.1
    )
    first_time_input = input(
        "Продавец участвует впервые (для скидки 15%)? (да/нет): "
    ).strip().lower()
    is_first_time = first_time_input in ("да", "yes", "+", "y", "1")
    is_paid_input = input(
        "Оплата регистрационного сбора внесена? (да/нет): "
    ).strip().lower()
    is_paid = is_paid_input in ("да", "yes", "+", "y", "1")

    try:
        new_app = create_application(
            applications=applications,
            vendor=vendor,
            fair=fair,
            requested_space=requested_space,
            is_first_time=is_first_time,
            is_paid=is_paid,
        )
        print(f"\n[Успех]: сформирована заявка #{new_app.id}.")
        print(new_app.generate_card())
    except ValueError as err:
        print(f"[Ошибка при создании заявки]: {err}")


def handle_show_statistics(
    fairs: List[Fair], applications: List[Application]
) -> None:
    """Выводит сводную аналитику по выбранной ярмарке."""
    print("\n--- Аналитика и статистика площадки ярмарки ---")
    for fair in fairs:
        print(f"[{fair.id}] {fair.name}")
    fair_id = input_int("Выберите ID ярмарки для аналитики: ", min_value=1)
    fair = next((f for f in fairs if f.id == fair_id), None)
    if not fair:
        print("[Ошибка]: ярмарка не найдена.")
        return

    stats = calculate_fair_statistics(applications, fair)
    revenue_str = format_currency(stats["total_revenue"])
    print(f"\nСтатистика для '{stats['fair_name']}':")
    print(f"  Общая площадь:         {stats['total_space']:.1f} кв.м")
    print(
        f"  Занятая площадь:       {stats['occupied_space']:.1f} кв.м "
        f"({stats['occupancy_rate']}%)"
    )
    print(f"  Свободная площадь:     {stats['free_space']:.1f} кв.м")
    print(f"  Всего поданных заявок: {stats['total_applications']}")
    print(f"  Утвержденных заявок:   {stats['approved_count']}")
    print(f"  Суммарная выручка:     {revenue_str}")


def run_demonstration() -> None:
    """Запускает демонстрационный сценарий всех возможностей ПР3 (ООП)."""
    print_header()
    print(">>> Запуск автоматического демонстрационного сценария ПР3 <<<\n")

    fairs = load_fairs()
    vendors = load_vendors()
    applications = load_applications(vendors=vendors, fairs=fairs)

    print(
        f"[Хранилище]: загружено {len(fairs)} ярмарок, "
        f"{len(vendors)} продавцов, {len(applications)} заявок."
    )

    # 1. Показ ярмарок (объекты Fair)
    display_fairs(fairs, applications)

    # 2. Показ продавцов (объекты Vendor и подклассы)
    display_vendors(vendors)

    # 3. Демонстрация полиморфизма специализированных подклассов
    print("\n--- Демонстрация полиморфизма подклассов Vendor ---")
    c_vendor = CraftVendor(101, "Глиняная сказка", "7701111111", True, 5)
    f_vendor = FoodVendor(102, "Алтайский мед", "7702222222", True, 3)
    s_vendor = SouvenirVendor(103, "Берестяной край", "7703333333", True, 7)
    for v in [c_vendor, f_vendor, s_vendor]:
        print(f"  {v} -> коэфф: {v.get_category_coefficient()}")

    # 4. Демонстрация поиска (подстрока)
    print("\n--- Демонстрация поиска продавцов по подстроке 'керамик' ---")
    found = find_vendor_by_name(vendors, "керамик")
    for f in found:
        print(f"  Найдено: {f.name} (ИНН: {f.inn})")

    # 5. Демонстрация фильтрации через генератор (yield)
    print("\n--- Демонстрация фильтрации (генератор, 'Ремесла') ---")
    crafts_generator = filter_vendors_by_category(vendors, "Ремесла")
    for craft_vendor in crafts_generator:
        print(f"  Генератор вернул: {craft_vendor.name}")

    # 6. Демонстрация сортировки через lambda
    print("\n--- Демонстрация сортировки по стажу (lambda, убывание) ---")
    sorted_by_exp = sort_vendors(vendors, sort_by="experience", reverse=True)
    for v in sorted_by_exp:
        print(f"  {v.name}: {v.experience_years} лет стажа")

    # 7. Демонстрация создания заявки с прямыми ссылками на объекты
    print("\n--- Демонстрация подачи заявки продавца #4 на ярмарку #1 ---")
    vendor_4 = get_vendor_by_id(vendors, 4)
    fair_1 = next(f for f in fairs if f.id == 1)

    is_avail = is_space_available(applications, fair_1, 10.0)
    print(f"Проверка доступности 10 кв.м: {is_avail}")

    new_app = create_application(
        applications=applications,
        vendor=vendor_4,
        fair=fair_1,
        requested_space=10.0,
        is_first_time=True,
        is_paid=True,
    )
    fee_fmt = format_currency(new_app.fee)
    print(
        f"Создана заявка #{new_app.id}: "
        f"«{new_app.vendor.name}» на «{new_app.fair.name}», сбор: {fee_fmt}"
    )

    # 8. Демонстрация генерации карточки из объекта Application
    print("\n--- Карточка заявки (метод generate_card) ---")
    print(new_app.generate_card())

    # 9. Вывод статистики площадки
    print("--- Сводная статистика ярмарки #1 после регистрации ---")
    stats = calculate_fair_statistics(applications, fair_1)
    print(
        f"Занято: {stats['occupied_space']:.1f} из {stats['total_space']:.1f} "
        f"кв.м ({stats['occupancy_rate']}%)"
    )
    print(
        f"Участников: {stats['approved_count']}, "
        f"Выручка: {format_currency(stats['total_revenue'])}"
    )

    # 10. Демонстрация отмены заявки через метод cancel()
    print("\n--- Демонстрация отмены заявки ---")
    cancel_application(applications, new_app.id)
    print(f"Заявка #{new_app.id} отменена: статус '{new_app.status}'")

    print("\n[Успех]: демонстрационный сценарий ПР3 успешно выполнен!")


def main() -> None:
    """Главная функция приложения с интерактивным меню."""
    if "--demo" in sys.argv or not sys.stdin.isatty():
        run_demonstration()
        return

    print_header()
    fairs = load_fairs()
    vendors = load_vendors()
    applications = load_applications(vendors=vendors, fairs=fairs)

    while True:
        print("\n=== Меню сервиса регистрации продавцов (ПР3 - ООП) ===")
        print("1. Показать список ярмарок")
        print("2. Показать список продавцов")
        print("3. Зарегистрировать нового продавца")
        print("4. Найти продавца по наименованию")
        print("5. Отсортировать продавцов по имени или стажу (lambda)")
        print("6. Показать реестр заявок")
        print("7. Подать заявку на участие в ярмарке")
        print("8. Отменить заявку на участие")
        print("9. Сводная статистика и аналитика ярмарки")
        print("0. Сохранить изменения и выйти")

        choice = input("\nВыберите пункт меню: ").strip()

        if choice == "1":
            display_fairs(fairs, applications)
        elif choice == "2":
            display_vendors(vendors)
        elif choice == "3":
            handle_add_vendor(vendors)
            save_vendors(vendors)
        elif choice == "4":
            query = input("Введите подстроку для поиска: ").strip()
            found = find_vendor_by_name(vendors, query)
            display_vendors(found)
        elif choice == "5":
            crit = input("Критерий сортировки (1 - имя, 2 - стаж): ").strip()
            sort_key = "experience" if crit == "2" else "name"
            rev_in = input("По убыванию? (да/нет): ").strip().lower()
            rev = rev_in in ("да", "yes", "+")
            sorted_res = sort_vendors(vendors, sort_by=sort_key, reverse=rev)
            display_vendors(sorted_res)
        elif choice == "6":
            display_applications(applications)
        elif choice == "7":
            handle_create_application(applications, vendors, fairs)
            save_applications(applications)
        elif choice == "8":
            app_id = input_int("Введите ID заявки для отмены: ", min_value=1)
            if cancel_application(applications, app_id):
                save_applications(applications)
                print(f"[Успех]: заявка #{app_id} успешно отменена.")
            else:
                print(f"[Ошибка]: заявка #{app_id} не найдена.")
        elif choice == "9":
            handle_show_statistics(fairs, applications)
        elif choice == "0":
            save_vendors(vendors)
            save_applications(applications)
            print("\nДанные успешно сохранены. Завершение работы программы.")
            break
        else:
            print("[Предупреждение]: неизвестная команда. Повторите выбор.")


if __name__ == "__main__":
    main()
