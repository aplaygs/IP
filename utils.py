"""Модуль вспомогательных функций и валидации ввода.

Предоставляет функции безопасного ввода числовых значений и дат с
обработкой исключений, а также форматирование денежных величин.
"""

from datetime import date, datetime
from typing import Optional


def input_int(
    prompt: str,
    min_value: Optional[int] = None,
    max_value: Optional[int] = None,
) -> int:
    """Запрашивает у пользователя ввод целого числа с валидацией границ.

    Параметры:
        prompt: сообщение приглашения ко вводу.
        min_value: минимально допустимое значение.
        max_value: максимально допустимое значение.

    Возвращает:
        Введенное корректное целое число.
    """
    while True:
        raw_input = input(prompt).strip()
        try:
            value = int(raw_input)
            if min_value is not None and value < min_value:
                print(f"[Ошибка]: значение должно быть не меньше {min_value}.")
                continue
            if max_value is not None and value > max_value:
                print(f"[Ошибка]: значение должно быть не больше {max_value}.")
                continue
            return value
        except ValueError:
            print("[Ошибка]: введено некорректное число. Повторите ввод.")


def input_float(
    prompt: str,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
) -> float:
    """Запрашивает у пользователя ввод вещественного числа.

    Параметры:
        prompt: сообщение приглашения ко вводу.
        min_value: минимально допустимое значение.
        max_value: максимально допустимое значение.

    Возвращает:
        Введенное корректное вещественное число.
    """
    while True:
        raw_input = input(prompt).strip().replace(",", ".")
        try:
            value = float(raw_input)
            if min_value is not None and value < min_value:
                print(f"[Ошибка]: значение должно быть не меньше {min_value}.")
                continue
            if max_value is not None and value > max_value:
                print(f"[Ошибка]: значение должно быть не больше {max_value}.")
                continue
            return value
        except ValueError:
            print("[Ошибка]: введено некорректное вещественное число.")


def input_date(prompt: str) -> date:
    """Запрашивает ввод даты в формате ДД.ММ.ГГГГ или ГГГГ-ММ-ДД.

    Параметры:
        prompt: сообщение приглашения ко вводу.

    Возвращает:
        Объект datetime.date.
    """
    while True:
        raw_input = input(prompt).strip()
        for date_format in ("%d.%m.%Y", "%Y-%m-%d"):
            try:
                parsed_datetime = datetime.strptime(raw_input, date_format)
                return parsed_datetime.date()
            except ValueError:
                continue
        print("[Ошибка]: неверный формат даты. Используйте ДД.ММ.ГГГГ.")


def format_currency(amount: float) -> str:
    """Форматирует числовое значение в читаемую строку валюты в рублях.

    Параметры:
        amount: сумма в рублях.

    Возвращает:
        Отформатированная строка, например '15 300.00 руб.'.
    """
    formatted = f"{amount:,.2f}".replace(",", " ")
    return f"{formatted} руб."
