"""Генератор официального отчета по Практической работе № 2 (ПР2) в формате ГОСТ.

Студент: Мишуков Владислав Романович
Группа: ЭФБО-11-24
Преподаватель: Ящун Татьяна Викторовна
Тема 433: Сервис регистрации продавцов на ярмарку (FairVendor)
"""

import base64
import io
import os
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    HRFlowable,
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from generate_report import MIREA_LOGO_B64


class GostNumberedCanvas(canvas.Canvas):
    """Холст с ГОСТ-нумерацией (титул без номера, со 2-й страницы по центру внизу)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            if self._pageNumber > 1:
                self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Times", 11)
        self.setFillColor(colors.black)
        # Номер страницы по центру внизу листа по ГОСТ 7.32
        self.drawCentredString(A4[0] / 2.0, 12 * mm, str(self._pageNumber))
        self.restoreState()


def create_gost_report_pr2(output_pdf_path: str):
    # Регистрация шрифтов Times New Roman
    font_dir = "/System/Library/Fonts/Supplemental"
    pdfmetrics.registerFont(TTFont("Times", os.path.join(font_dir, "Times New Roman.ttf")))
    pdfmetrics.registerFont(TTFont("Times-Bold", os.path.join(font_dir, "Times New Roman Bold.ttf")))
    pdfmetrics.registerFont(TTFont("Times-Italic", os.path.join(font_dir, "Times New Roman Italic.ttf")))
    pdfmetrics.registerFont(TTFont("Times-BoldItalic", os.path.join(font_dir, "Times New Roman Bold Italic.ttf")))

    # Поля страницы по ГОСТ 7.32: левое 30 мм, правое 15 мм, верхнее 20 мм, нижнее 20 мм
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=A4,
        leftMargin=30 * mm,
        rightMargin=15 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )

    styles = getSampleStyleSheet()

    # Стили по ГОСТ (строго черный цвет, гарнитура Times New Roman)
    style_univ = ParagraphStyle(
        "UnivTitle",
        parent=styles["Normal"],
        fontName="Times",
        fontSize=10,
        leading=13,
        alignment=TA_CENTER,
        textColor=colors.black,
    )

    style_univ_bold = ParagraphStyle(
        "UnivTitleBold",
        parent=style_univ,
        fontName="Times-Bold",
        fontSize=10.5,
        leading=13.5,
    )

    style_doc_title = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Times-Bold",
        fontSize=15,
        leading=19,
        alignment=TA_CENTER,
        textColor=colors.black,
    )

    style_doc_subtitle = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Times",
        fontSize=12,
        leading=16,
        alignment=TA_CENTER,
        textColor=colors.black,
    )

    style_theme = ParagraphStyle(
        "ThemeStyle",
        parent=styles["Normal"],
        fontName="Times",
        fontSize=12,
        leading=16,
        alignment=TA_CENTER,
        textColor=colors.black,
    )

    style_sign = ParagraphStyle(
        "SignStyle",
        parent=styles["Normal"],
        fontName="Times",
        fontSize=11,
        leading=14,
        textColor=colors.black,
    )

    style_sign_sub = ParagraphStyle(
        "SignSubStyle",
        parent=styles["Normal"],
        fontName="Times-Italic",
        fontSize=8.5,
        leading=10.5,
        alignment=TA_CENTER,
        textColor=colors.black,
    )

    style_h1 = ParagraphStyle(
        "GostH1",
        parent=styles["Normal"],
        fontName="Times-Bold",
        fontSize=13,
        leading=16.5,
        alignment=TA_LEFT,
        textColor=colors.black,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True,
    )

    style_body = ParagraphStyle(
        "GostBody",
        parent=styles["Normal"],
        fontName="Times",
        fontSize=11,
        leading=14.8,
        alignment=TA_JUSTIFY,
        firstLineIndent=12.5 * mm,
        textColor=colors.black,
        spaceAfter=3,
    )

    style_bullet = ParagraphStyle(
        "GostBullet",
        parent=styles["Normal"],
        fontName="Times",
        fontSize=11,
        leading=14.8,
        alignment=TA_JUSTIFY,
        leftIndent=12.5 * mm,
        firstLineIndent=-6 * mm,
        textColor=colors.black,
        spaceAfter=3,
    )

    style_center = ParagraphStyle(
        "GostCenter",
        parent=styles["Normal"],
        fontName="Times",
        fontSize=11,
        leading=15,
        alignment=TA_CENTER,
        textColor=colors.black,
    )

    story = []

    # =========================================================================
    # СТРАНИЦА 1: ТИТУЛЬНЫЙ ЛИСТ (С ГЕРБОМ РТУ МИРЭА)
    # =========================================================================
    logo_bytes = base64.b64decode(MIREA_LOGO_B64)
    logo_img = Image(io.BytesIO(logo_bytes), width=24 * mm, height=27.2 * mm)
    logo_img.hAlign = "CENTER"
    story.append(logo_img)
    story.append(Spacer(1, 2.5 * mm))

    story.append(Paragraph("МИНОБРНАУКИ РОССИИ", style_univ))
    story.append(
        Paragraph(
            "Федеральное государственное бюджетное образовательное учреждение<br/>"
            "высшего образования<br/>"
            "<b>«МИРЭА – Российский технологический университет»</b>",
            style_univ,
        )
    )
    story.append(Spacer(1, 1 * mm))
    story.append(Paragraph("РТУ МИРЭА", style_univ_bold))
    story.append(Spacer(1, 2 * mm))

    # Горизонтальная разделительная черта по ширине листа
    story.append(HRFlowable(width="100%", thickness=2, color=colors.black, spaceAfter=20 * mm))

    # Название практической работы строго по ТЗ
    story.append(Paragraph("Практическая работа № 2", style_doc_title))
    story.append(Spacer(1, 2.5 * mm))
    story.append(
        Paragraph(
            "по дисциплине «Технологии разработки приложений на базе фреймворков»",
            style_doc_subtitle,
        )
    )
    story.append(Spacer(1, 8 * mm))

    # Тема работы строго по методическим указаниям ПР2
    story.append(
        Paragraph(
            "<b>Тема работы:</b> Основы Python: коллекции, функции, циклы и расширенные возможности Python",
            style_theme,
        )
    )
    story.append(Spacer(1, 30 * mm))

    # Блок подписей (таблица)
    sign_table_data = [
        [
            Paragraph("Выполнил:", style_sign),
            Paragraph("студент группы ЭФБО-11-24", style_sign),
            Paragraph("", style_sign),
            Paragraph("Мишуков В.Р.", style_sign),
        ],
        [
            Paragraph("", style_sign_sub),
            Paragraph("(группа)", style_sign_sub),
            Paragraph("(подпись)", style_sign_sub),
            Paragraph("(Фамилия И.О.)", style_sign_sub),
        ],
        [
            Paragraph("", style_sign),
            Paragraph("", style_sign),
            Paragraph("", style_sign),
            Paragraph("", style_sign),
        ],
        [
            Paragraph("Принял:", style_sign),
            Paragraph("доц.", style_sign),
            Paragraph("", style_sign),
            Paragraph("Ящун Т.В.", style_sign),
        ],
        [
            Paragraph("", style_sign_sub),
            Paragraph("(должность)", style_sign_sub),
            Paragraph("(подпись)", style_sign_sub),
            Paragraph("(Фамилия И.О.)", style_sign_sub),
        ],
    ]

    t_sign = Table(
        sign_table_data,
        colWidths=[24 * mm, 62 * mm, 32 * mm, 47 * mm],
    )
    t_sign.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 1),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
                ("LINEBELOW", (2, 0), (2, 0), 0.75, colors.black),
                ("LINEBELOW", (2, 3), (2, 3), 0.75, colors.black),
            ]
        )
    )
    story.append(t_sign)

    story.append(Spacer(1, 25 * mm))
    story.append(Paragraph("Москва", style_center))
    story.append(Paragraph("2026", style_center))

    # =========================================================================
    # СТРАНИЦА 2: РАЗДЕЛ 1 (ИНДИВИДУАЛЬНЫЙ ПРОЕКТ)
    # =========================================================================
    story.append(PageBreak())

    story.append(Paragraph("1. Индивидуальный проект", style_h1))

    story.append(
        Paragraph(
            "• <b>Название проекта:</b> Сервис регистрации продавцов на ярмарку (FairVendor), тема № 433.",
            style_bullet,
        )
    )

    story.append(
        Paragraph(
            "• <b>Перечень функций, реализованных на этапе ПР2:</b><br/>"
            "&nbsp;&nbsp;1. <code>storage.py</code>: <code>safe_load_json()</code>, <code>safe_save_json()</code>, "
            "<code>load_fairs()</code>, <code>save_fairs()</code>, <code>load_vendors()</code>, <code>save_vendors()</code>, "
            "<code>load_applications()</code>, <code>save_applications()</code> — надежное персистентное сохранение "
            "и считывание данных ярмарок, участников и заявок в формате JSON с гарантированным закрытием файлов через "
            "контекстный менеджер <code>with open</code> и перехватом исключений <code>FileNotFoundError</code>, "
            "<code>json.JSONDecodeError</code>;<br/>"
            "&nbsp;&nbsp;2. <code>vendors.py</code>: <code>validate_inn()</code> (проверка 10- или 12-значного числового формата ИНН), "
            "<code>add_vendor()</code> (регистрация продавца в коллекции со строгой валидацией полей и контролем уникальности ИНН), "
            "<code>get_vendor_by_id()</code> (быстрая выборка продавца по идентификатору), <code>find_vendor_by_name()</code> "
            "(поиск участников по регистронезависимой подстроке имени бренда), <code>filter_vendors_by_category()</code> "
            "(поэлементная фильтрация продавцов с использованием генератора и оператора <code>yield</code>), "
            "<code>sort_vendors()</code> (сортировка участников по наименованию или стажу с применением анонимных <code>lambda</code>-функций);<br/>"
            "&nbsp;&nbsp;3. <code>applications.py</code>: <code>get_occupied_space()</code> (расчет суммарной занятой площади на ярмарке по активным заявкам), "
            "<code>is_space_available()</code> (проверка наличия достаточной свободной площади на площадке), "
            "<code>create_application()</code> (создание и добавление заявки с проверкой лимита мест, валидацией документов и вычислением сбора), "
            "<code>cancel_application()</code> (отзыв и аннулирование брони с освобождением торгового пространства), "
            "<code>calculate_fair_statistics()</code> (вычисление сводной аналитики: процент занятости, выручка, число одобренных заявок), "
            "а также функции ПР1 (<code>validate_vendor_data</code>, <code>calculate_participation_fee</code>, <code>determine_application_status</code>, <code>generate_registration_card</code>);<br/>"
            "&nbsp;&nbsp;4. <code>utils.py</code>: <code>input_int()</code>, <code>input_float()</code>, <code>input_date()</code> "
            "(безопасный консольный ввод с циклической валидацией и перехватом <code>ValueError</code>), <code>format_currency()</code> (финансовое форматирование);<br/>"
            "&nbsp;&nbsp;5. <code>main.py</code>: консольный интерфейс с интерактивным меню на 10 пунктов и демонстрационным режимом (<code>--demo</code>).",
            style_bullet,
        )
    )

    story.append(
        Paragraph(
            "• <b>Структура модулей проекта:</b> проект декомпозирован на слабосвязанные логические компоненты: "
            "<code>main.py</code> (точка входа, меню и диспетчеризация), <code>vendors.py</code> (управление участниками), "
            "<code>applications.py</code> (управление заявками и расчетом площадей), <code>storage.py</code> (работа с файловой подсистемой), "
            "<code>utils.py</code> (ввод-вывод и форматирование), каталог <code>data/</code> (файлы постоянного хранения), "
            "каталог <code>tests/</code> (набор тестов <code>test_vendors.py</code>, <code>test_applications.py</code>), "
            "<code>test_main.py</code> (обратная совместимость), <code>requirements.txt</code> и <code>.flake8</code>.",
            style_bullet,
        )
    )

    story.append(
        Paragraph(
            "• <b>Формат хранения данных:</b> данные персистентно хранятся в формате JSON в каталоге <code>data/</code>:<br/>"
            "&nbsp;&nbsp;1. <code>fairs.json</code> — список словарей ярмарок (ключи: <code>id</code>, <code>name</code>, <code>location</code>, <code>date</code>, <code>base_rate</code>, <code>total_space</code>);<br/>"
            "&nbsp;&nbsp;2. <code>vendors.json</code> — реестр продавцов (ключи: <code>id</code>, <code>name</code>, <code>inn</code>, <code>category</code>, <code>has_documents</code>, <code>experience_years</code>);<br/>"
            "&nbsp;&nbsp;3. <code>applications.json</code> — журнал заявок (ключи: <code>id</code>, <code>vendor_id</code>, <code>fair_id</code>, <code>requested_space</code>, <code>fee</code>, <code>status</code>).",
            style_bullet,
        )
    )

    story.append(
        Paragraph(
            "• <b>Ссылка на Git-репозиторий:</b> https://github.com/aplaygs/IP.git",
            style_bullet,
        )
    )

    # =========================================================================
    # СТРАНИЦА 3: РАЗДЕЛ 2 (РЕЗУЛЬТАТ РАБОТЫ) И РАЗДЕЛ 3 (ВЫВОД)
    # =========================================================================
    story.append(PageBreak())

    story.append(Paragraph("2. Результат работы", style_h1))
    story.append(Paragraph("В результате выполнения практической работы № 2 (ПР2):", style_body))

    story.append(
        Paragraph(
            "• освоены и применены на практике встроенные коллекции Python: динамические списки (<code>list</code>) "
            "и словари (<code>dict</code>) для хранения структурированных сущностей ярмарок, продавцов и заявок, а также множества (<code>set</code>);",
            style_bullet,
        )
    )

    story.append(
        Paragraph(
            "• исходный монолитный код первого этапа (ПР1) декомпозирован на логические модули по зонам ответственности: "
            "<code>vendors.py</code>, <code>applications.py</code>, <code>storage.py</code>, <code>utils.py</code> и <code>main.py</code>;",
            style_bullet,
        )
    )

    story.append(
        Paragraph(
            "• реализован переход от временных переменных в оперативной памяти к постоянному хранению данных в файлах "
            "<code>fairs.json</code>, <code>vendors.json</code>, <code>applications.json</code> с автоматической инициализацией и валидацией данных;",
            style_bullet,
        )
    )

    story.append(
        Paragraph(
            "• обеспечена надежная работа с файлами с использованием контекстного менеджера <code>with open()</code>, "
            "гарантирующего корректное освобождение дескрипторов при любых сценариях выполнения;",
            style_bullet,
        )
    )

    story.append(
        Paragraph(
            "• реализована отказоустойчивая обработка исключений: перехват <code>FileNotFoundError</code> и <code>json.JSONDecodeError</code> "
            "при сбоях чтения файлов, <code>ValueError</code> при некорректном пользовательском вводе и бизнес-валидации (дубликат ИНН, дефицит площади стенда);",
            style_bullet,
        )
    )

    story.append(
        Paragraph(
            "• применены расширенные возможности языка: генераторы с оператором <code>yield</code> для эффективной фильтрации "
            "участников по товарным категориям и анонимные <code>lambda</code>-функции для гибкой сортировки;",
            style_bullet,
        )
    )

    story.append(
        Paragraph(
            "• все ключевые функции снабжены стандартными аннотациями типов аргументов и возвращаемых значений, а также подробными docstring-комментариями;",
            style_bullet,
        )
    )

    story.append(
        Paragraph(
            "• исходный код проверен линтером <code>flake8</code>: устранены замечания PEP 8 (длина строк, неиспользуемые импорты), получен чистый вывод;",
            style_bullet,
        )
    )

    story.append(
        Paragraph(
            "• разработана система модульного тестирования на базе фреймворка <code>pytest</code> в каталоге <code>tests/</code> (20 тестов, 100% passed);",
            style_bullet,
        )
    )

    story.append(
        Paragraph(
            "• обновлена проектная документация <code>README.md</code>, зафиксирован единый итоговый коммит «Практика 2» и выполнен push в удаленный репозиторий GitHub.",
            style_bullet,
        )
    )

    story.append(Paragraph("3. Вывод", style_h1))
    story.append(
        Paragraph(
            "В ходе выполнения практической работы № 2 были освоены и закреплены ключевые конструкции языка Python, "
            "необходимые для разработки надежных прикладных систем: структуры данных (списки, словари), модульная декомпозиция программного кода, "
            "контекстные менеджеры для безопасного ввода-вывода, генераторы и лямбда-выражения. Реализована обработка исключительных "
            "ситуаций, исключающая аварийное завершение программы при ошибочных действиях пользователя или сбоях файловой системы. "
            "Индивидуальный проект «Сервис регистрации продавцов на ярмарку» развит до полнофункционального модульного консольного приложения "
            "с персистентным JSON-хранилищем, агрегацией аналитики и автоматизированным тестовым покрытием <code>pytest</code>. "
            "Код полностью соответствует стандарту PEP 8 и подготовлен к реализации объектно-ориентированной модели (ООП) на этапе ПР3.",
            style_body,
        )
    )

    story.append(Spacer(1, 10 * mm))
    story.append(Paragraph("Москва", style_center))
    story.append(Paragraph("2026", style_center))

    doc.build(story, canvasmaker=GostNumberedCanvas)
    print(f"Итоговый отчет по ГОСТ (ПР2) успешно сгенерирован: {output_pdf_path}")


if __name__ == "__main__":
    pdf_filename = "Отчет_Практическая_работа_2_Мишуков_В_Р.pdf"
    create_gost_report_pr2(pdf_filename)
